"""Export a few real AIDev live-queue queries as CLI fixtures and check package/benchmark feature parity.

Writes tests/fixtures/aidev/<kind>_new.json, <kind>_queue.jsonl and expected.json.
"""
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(H, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from jinx_pr import PR, Detector

D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
OUT = os.path.join(ROOT, "tests", "fixtures", "aidev")
LEX = ["text_tfidf", "title_tfidf", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue", "mention_ref",
       "same_author", "same_agent", "log_gap_hours", "cand_open"]
with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
F = pd.read_parquet(D + "features.parquet")
need = sorted({x["q"] for x in Q} | {int(c) for x in Q for c in x["cand"]})
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "created_at", "closed_at",
                                                           "repo_url", "html_url"]).set_index("id").loc[need]
with open(D + "diffs.pkl", "rb") as fh:
    diffs = pickle.load(fh)
ri = pd.read_parquet(D + "related_issue.parquet")
links = ri[ri.source == "body"].groupby("pr_id").issue_id.apply(set).to_dict()


def iso(v):
    return None if pd.isna(v) else pd.Timestamp(v).isoformat()


def as_dict(i):
    r = pr.loc[i]
    return {"number": int(r.number), "title": r.title or "", "body": r.body or "", "author": r.user or "", "agent": r.agent or "",
            "created_at": iso(r.created_at), "closed_at": iso(r.closed_at), "html_url": r.html_url or "",
            "files": sorted(diffs["files"].get(i, ())), "hunks": sorted(list(h) for h in diffs["hunks"].get(i, ())),
            "added_hashes": sorted(int(a) for a in diffs["added"].get(i, ())), "linked_issues": sorted(int(x) for x in links.get(i, set()))}


# Parity: package features (from JSON round-trip) == benchmark features.parquet, on 200 random queries.
rng = np.random.default_rng(0)
det = Detector()
worst = 0.0
for qi in rng.choice(len(Q), 200, replace=False):
    x = Q[qi]
    new = PR.from_dict(as_dict(x["q"]))
    queue = [PR.from_dict(as_dict(int(c))) for c in x["cand"]]
    got = pd.DataFrame(det.featurize(new, queue))[LEX].to_numpy()
    ref = F[F.qi == qi].set_index("cand").loc[[int(c) for c in x["cand"]], LEX].to_numpy()
    worst = max(worst, float(np.abs(got - ref).max()))
print("feature parity on 200 queries: max |package - benchmark| =", f"{worst:.2e}")
assert worst < 1e-6

kinds = {"cross_author": lambda x: not x["neg"] and not x["self"], "self_replacement": lambda x: not x["neg"] and x["self"],
         "no_duplicate": lambda x: x["neg"]}
expected = {}
for kind, ok in kinds.items():
    for qi, x in enumerate(Q):
        if not ok(x) or not 8 <= len(x["cand"]) <= 25:
            continue
        new, cand = as_dict(x["q"]), [as_dict(int(c)) for c in x["cand"]]
        m = det.rank(PR.from_dict(new), [PR.from_dict(c) for c in cand], top=1)[0]
        gold = F[(F.qi == qi) & F.gold].cand
        want = int(pr.number[int(gold.iloc[0])]) if len(gold) else None
        if (want is None and m.score < det.threshold) or (want is not None and m.number == want and m.score >= det.threshold):
            break
    with open(os.path.join(OUT, f"{kind}_new.json"), "w") as fh:
        json.dump(new, fh, indent=1)
    with open(os.path.join(OUT, f"{kind}_queue.jsonl"), "w") as fh:
        fh.write("\n".join(json.dumps(c) for c in cand) + "\n")
    expected[kind] = {"query_index": qi, "repo": pr.repo_url[x["q"]], "pr": new["number"], "queue_size": len(cand),
                      "expected_duplicate": want}
    print(kind, expected[kind], "top1", m.number, round(m.score, 3))
with open(os.path.join(OUT, "expected.json"), "w") as fh:
    json.dump(expected, fh, indent=1)
