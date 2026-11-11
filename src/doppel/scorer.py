from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from importlib import resources

from .agents import guess_agent
from .features import code_features, context_features, link_features
from .pr import PR
from .templates import TemplateModel, queue_common_lines
from .text import TfIdf, cosine, tokens

FEATURES = [
    "text_tfidf",
    "title_tfidf",
    "emb_cos",
    "file_jacc",
    "file_contain",
    "hunk_overlap",
    "line_contain",
    "same_issue",
    "mention_ref",
    "same_author",
    "same_agent",
    "log_gap_hours",
    "cand_open",
]


@dataclass
class Match:
    number: int
    score: float
    reasons: list = field(default_factory=list)
    features: dict = field(default_factory=dict)
    title: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "score": round(self.score, 4),
            "title": self.title,
            "url": self.url,
            "reasons": self.reasons,
            "features": {k: round(v, 4) for k, v in self.features.items()},
        }


def load_weights(name: str) -> dict:
    return json.loads(resources.files("doppel").joinpath(f"data/{name}").read_text())


class Detector:
    """Rank the open-PR queue by how likely each PR duplicates a new PR.

    Score = logistic model over template-stripped text similarity, code overlap (files, changed line
    ranges, identical added lines), shared linked issue, explicit #references and author/time context."""

    def __init__(
        self,
        weights: dict | None = None,
        templates: TemplateModel | None = None,
        embedder=None,
        strip_templates: bool = True,
    ):
        self.embedder = embedder
        if weights is None:
            weights = load_weights("weights_emb.json" if embedder else "weights.json")
        self.w = weights
        self.templates = templates if templates is not None else TemplateModel.default()
        self.strip_templates = strip_templates
        self.threshold = float(weights.get("threshold", 0.5))

    def _clean(self, pr: PR, extra: set) -> str:
        agent = pr.agent or guess_agent(pr.author, pr.body)
        body = self.templates.strip(pr.body, agent, extra) if self.strip_templates else pr.body
        return f"{pr.title}\n{body}"

    def featurize(self, new: PR, queue: list[PR]) -> list[dict]:
        queue = [c for c in queue if c.number != new.number]
        if not queue:
            return []
        extra = queue_common_lines([c.body for c in queue] + [new.body]) if self.strip_templates else set()
        texts = [self._clean(p, extra) for p in [new] + queue]
        toks = [tokens(t) for t in texts]
        ttoks = [tokens(p.title) for p in [new] + queue]
        tf, tt = TfIdf(toks), TfIdf(ttoks)
        vecs = [tf.vec(t) for t in toks]
        tvecs = [tt.vec(t) for t in ttoks]
        emb = None
        if self.embedder is not None and "emb_cos" in self.w["features"]:
            emb = self.embedder.encode(texts)
        rows = []
        for i, c in enumerate(queue, start=1):
            f = {
                "text_tfidf": cosine(vecs[0], vecs[i]),
                "title_tfidf": cosine(tvecs[0], tvecs[i]),
                "emb_cos": float(sum(a * b for a, b in zip(emb[0], emb[i]))) if emb is not None else 0.0,
            }
            f.update(code_features(new, c))
            f.update(link_features(new, c))
            f.update(context_features(new, c))
            rows.append(f)
        return rows

    def score_rows(self, rows: list[dict]) -> list[float]:
        names, coef, mean, scale = self.w["features"], self.w["coef"], self.w["mean"], self.w["scale"]
        out = []
        for f in rows:
            z = self.w["intercept"] + sum(
                c * (f.get(n, 0.0) - m) / s for n, c, m, s in zip(names, coef, mean, scale)
            )
            out.append(1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z)))))
        return out

    def rank(self, new: PR, queue: list[PR], top: int = 5) -> list[Match]:
        queue = [c for c in queue if c.number != new.number]
        rows = self.featurize(new, queue)
        scores = self.score_rows(rows)
        order = sorted(range(len(queue)), key=lambda i: -scores[i])[:top]
        return [
            Match(
                queue[i].number,
                scores[i],
                explain(new, queue[i], rows[i]),
                rows[i],
                queue[i].title,
                queue[i].url,
            )
            for i in order
        ]


def explain(new: PR, cand: PR, f: dict) -> list[str]:
    r = []
    if f["mention_ref"]:
        r.append(f"one PR links to the other (#{cand.number})")
    shared_issue = sorted(new.linked_issues & cand.linked_issues)
    if shared_issue:
        r.append("same linked issue: " + ", ".join(f"#{i}" for i in shared_issue[:3]))
    shared = sorted(new.files & cand.files)
    if shared:
        names = ", ".join(shared[:3]) + (" ..." if len(shared) > 3 else "")
        r.append(f"shares {len(shared)} of {len(new.files)} changed files ({names})")
    if f["hunk_overlap"] > 0:
        r.append(f"{f['hunk_overlap']:.0%} of changed line ranges overlap")
    if f["line_contain"] > 0:
        r.append(f"{f['line_contain']:.0%} of added lines are identical")
    sim = max(f["text_tfidf"], f.get("emb_cos", 0.0))
    if sim >= 0.3:
        r.append(f"similar title/description after removing agent template text ({sim:.2f})")
    if f["same_author"]:
        r.append("same author (possible re-opened or replacement PR)")
    return r or ["weak match"]
