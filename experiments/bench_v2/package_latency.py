"""End-to-end CPU latency of the installed package (Detector.rank) per new PR, with and without the MiniLM embedder.

Times 300 random open-only queues (at most 200 open PRs each) (4 CPU threads), including feature extraction, embedding and scoring.
Excludes GitHub API calls, pip install and the one-off model download/load.
Writes experiments/results/package_latency.json.
"""
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
import torch

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(H, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from jinx_pr import PR, Detector
from jinx_pr.embed import Embedder

D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
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



torch.set_num_threads(4)
rng = np.random.default_rng(1)
# open-only queues, at most the 200 most recent open PRs (what the Action sees)
O = F[F.cand_open > 0]
O = O[O.groupby("qi").log_gap_hours.rank(method="first") <= 200].groupby("qi").cand.apply(list)
idx = rng.choice(np.array(O.index), 300, replace=False)
cases = [(PR.from_dict(as_dict(Q[i]["q"])), [PR.from_dict(as_dict(int(c))) for c in O[i]]) for i in idx]
out = {"queries": len(cases), "cpu_threads": 4, "queue_median": float(np.median([len(c) for _, c in cases]))}
for name, det in [("lexical", Detector()), ("minilm", Detector(embedder=Embedder()))]:
    det.rank(*cases[0])
    ms = []
    for new, queue in cases:
        t0 = time.perf_counter()
        det.rank(new, queue)
        ms.append(1000 * (time.perf_counter() - t0))
    out[name] = {"median_ms": round(float(np.median(ms)), 1), "p90_ms": round(float(np.percentile(ms, 90)), 1)}
    print(name, out[name], flush=True)
with open(os.path.join(ROOT, "experiments", "results", "package_latency.json"), "w") as fh:
    json.dump(out, fh, indent=1)
