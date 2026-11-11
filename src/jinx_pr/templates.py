"""Agent boilerplate ("template") stripping.

A line is template text if, after normalisation, it occurs in many PRs of the same agent
across several repositories (learned offline), or in a large share of the current queue."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from importlib import resources

_URL = re.compile(r"https?://\S+")
_NUM = re.compile(r"\d+")
_HEX = re.compile(r"\b[0-9a-f]{7,40}\b")
_SYM = re.compile(r"[^a-z0-9 ]+")
_WS = re.compile(r"\s+")


def normalize_line(line: str) -> str:
    s = line.strip().lower()
    s = _URL.sub(" url ", s)
    s = _HEX.sub(" hex ", s)
    s = _NUM.sub("0", s)
    s = _SYM.sub(" ", s)
    return _WS.sub(" ", s).strip()


class TemplateModel:
    def __init__(self, lines_by_agent: dict | None = None, global_lines: Iterable[str] = ()):
        self.lines_by_agent = {a: set(v) for a, v in (lines_by_agent or {}).items()}
        self.global_lines = set(global_lines)

    @classmethod
    def learn(cls, prs: Iterable[tuple], min_share: float = 0.01, min_repos: int = 5, min_count: int = 20):
        """prs: iterable of (agent, repo, body)."""
        count = defaultdict(Counter)
        repos = defaultdict(lambda: defaultdict(set))
        n = Counter()
        for agent, repo, body in prs:
            n[agent] += 1
            for ln in {normalize_line(x) for x in (body or "").splitlines()}:
                if ln:
                    count[agent][ln] += 1
                    if len(repos[agent][ln]) < min_repos:
                        repos[agent][ln].add(repo)
        out = {}
        for agent, c in count.items():
            thr = max(min_count, min_share * n[agent])
            out[agent] = {ln for ln, k in c.items() if k >= thr and len(repos[agent][ln]) >= min_repos}
        shared = Counter(ln for v in out.values() for ln in v)
        return cls(out, {ln for ln, k in shared.items() if k >= 2})

    @classmethod
    def default(cls) -> TemplateModel:
        try:
            raw = resources.files("jinx_pr").joinpath("data/templates.json").read_text()
        except FileNotFoundError:
            return cls()
        return cls.from_json(raw)

    @classmethod
    def from_json(cls, raw: str) -> TemplateModel:
        d = json.loads(raw)
        return cls(d.get("agents", {}), d.get("global", []))

    def to_json(self) -> str:
        return json.dumps(
            {
                "agents": {a: sorted(v) for a, v in sorted(self.lines_by_agent.items())},
                "global": sorted(self.global_lines),
            },
            indent=0,
        )

    def is_template(self, norm: str, agent: str = "") -> bool:
        if not norm:
            return True
        if norm in self.global_lines:
            return True
        if agent:
            return norm in self.lines_by_agent.get(agent, ())
        return any(norm in v for v in self.lines_by_agent.values())

    def strip(self, body: str, agent: str = "", extra: set | None = None) -> str:
        keep = []
        for line in (body or "").splitlines():
            norm = normalize_line(line)
            if self.is_template(norm, agent) or (extra and norm in extra):
                continue
            keep.append(line)
        return "\n".join(keep)

    def template_share(self, body: str, agent: str = "") -> float:
        lines = [normalize_line(x) for x in (body or "").splitlines()]
        lines = [x for x in lines if x]
        return sum(self.is_template(x, agent) for x in lines) / len(lines) if lines else 0.0


def queue_common_lines(bodies: list[str], min_share: float = 0.2, min_docs: int = 3) -> set:
    """Lines repeated across a big share of the current queue (repo-level PR templates)."""
    c = Counter()
    for b in bodies:
        c.update({normalize_line(x) for x in (b or "").splitlines()} - {""})
    thr = max(min_docs, min_share * len(bodies))
    return {ln for ln, k in c.items() if k >= thr}
