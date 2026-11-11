"""Find real false alarms of the shipped lexical Jinx on open-only queues of no-duplicate PRs (for the tool-demo example)."""
import os
import pickle
import sys

import numpy as np
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "..", "src"))
from jinx_pr import PR, Detector

D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
F = pd.read_parquet(D + "features.parquet", columns=["qi", "cand", "cand_open", "log_gap_hours"])
O = F[F.cand_open > 0]
O = O[O.groupby("qi").log_gap_hours.rank(method="first") <= 200].groupby("qi").cand.apply(list)
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "created_at", "closed_at",
                                                           "repo_url", "html_url"]).set_index("id")
with open(D + "diffs.pkl", "rb") as fh:
    diffs = pickle.load(fh)
ri = pd.read_parquet(D + "related_issue.parquet")
links = ri[ri.source == "body"].groupby("pr_id").issue_id.apply(set).to_dict()


def iso(v):
    return None if pd.isna(v) else pd.Timestamp(v).isoformat()


def as_pr(i):
    r = pr.loc[i]
    return PR.from_dict({"number": int(r.number), "title": r.title or "", "body": r.body or "", "author": r.user or "", "agent": r.agent or "",
                         "created_at": iso(r.created_at), "closed_at": iso(r.closed_at), "html_url": r.html_url or "",
                         "files": sorted(diffs["files"].get(i, ())), "hunks": sorted(list(h) for h in diffs["hunks"].get(i, ())),
                         "added_hashes": sorted(int(a) for a in diffs["added"].get(i, ())),
                         "linked_issues": sorted(int(x) for x in links.get(i, set()))})


det = Detector()
neg = [i for i, x in enumerate(Q) if x["neg"] and i in O.index]
rng = np.random.default_rng(7)
found = 0
for i in rng.permutation(neg)[:400]:
    new = as_pr(Q[i]["q"])
    m = det.rank(new, [as_pr(int(c)) for c in O[i]], top=1)
    if m and m[0].score >= 0.5:
        found += 1
        print(f"--- {pr.repo_url[Q[i]['q']]}  new #{new.number} {new.title[:60]}")
        print(f"    flagged #{m[0].number} score {m[0].score:.2f} {m[0].title[:60]}")
        for r in m[0].reasons:
            print(f"     - {r}")
        if found >= 6:
            break
