"""What does a duplicate PR cost, and how long until a human notices? (AIDev only, no API.)

For every labelled duplicate query in the benchmark, the pair is (new PR, older PR). The "closed" PR is the one that got the
"duplicate of / superseded by #N" comment and was closed without merging. We measure, from AIDev tables:
  - detection delay: time from the new PR being opened (the first moment a tool could warn) to the human duplicate comment;
  - lifetime of the closed PR: opened -> closed;
  - effort spent on the closed PR before the duplicate comment: human comments and human reviews (work a day-0 warning
    could have saved), plus total commits and lines added to the closed PR.
Writes experiments/results/duplicate_cost.csv (one row per query) and duplicate_cost_summary.json.
"""
import json
import os
import pickle

import numpy as np
import pandas as pd

D = "/home/ubuntu/research/prdupecheck/data/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
pos = [(i, int(x["q"]), int(x["gold"]), bool(x["self"]), x["phrase"]) for i, x in enumerate(Q) if not x["neg"]]
ids = {p for _, a, b, _, _ in pos for p in (a, b)}
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "created_at", "closed_at", "merged_at", "repo_url"])
P = P[P.id.isin(ids)].set_index("id")
for c in ["created_at", "closed_at", "merged_at"]:
    P[c] = pd.to_datetime(P[c], utc=True)
C = pd.read_parquet(D + "pr_comments.parquet", columns=["pr_id", "created_at", "user_type", "body"])
C = C[C.pr_id.isin(ids)]
C["created_at"] = pd.to_datetime(C.created_at, utc=True)
# pr_timeline has no timestamps for reviews/commits; reviews carry submitted_at, commits carry no time (counted in total)
V = pd.read_parquet(D + "pr_reviews.parquet", columns=["pr_id", "user_type", "submitted_at"], filters=[("pr_id", "in", list(ids))])
V["submitted_at"] = pd.to_datetime(V.submitted_at, utc=True)
V = V[V.user_type != "Bot"]
ncommits = pd.read_parquet(D + "pr_commits.parquet", columns=["pr_id", "sha"], filters=[("pr_id", "in", list(ids))]).groupby("pr_id").sha.nunique()
add = pd.read_parquet(D + "pr_commit_details.parquet", columns=["pr_id", "additions"], filters=[("pr_id", "in", list(ids))])
lines = add.groupby("pr_id").additions.sum()

rows = []
for qi, q, g, self_, phrase in pos:
    # the PR carrying the duplicate phrase is the one that was closed in favour of the other
    hit = C[C.pr_id.isin([q, g]) & C.body.fillna("").str.contains(phrase, regex=False)]
    if hit.empty:
        continue
    h = hit.sort_values("created_at").iloc[0]
    closed = int(h.pr_id)
    t_new = P.created_at[q]
    rows.append({
        "qi": qi, "self": self_, "closed_pr": closed, "closed_is_new": closed == q,
        "closed_merged": pd.notna(P.merged_at.get(closed)),
        "delay_h": (h.created_at - t_new).total_seconds() / 3600,
        "closed_life_h": (P.closed_at[closed] - P.created_at[closed]).total_seconds() / 3600 if pd.notna(P.closed_at[closed]) else np.nan,
        "human_comments": int(((C.pr_id == closed) & (C.user_type != "Bot") & (C.created_at < h.created_at)).sum()),
        "reviews": int(((V.pr_id == closed) & (V.submitted_at < h.created_at)).sum()),
        "commits": int(ncommits.get(closed, 0)),
        "lines_added": int(lines.get(closed, 0)),
    })
R = pd.DataFrame(rows)
R.to_csv(os.path.join(OUT, "duplicate_cost.csv"), index=False)


def summ(x):
    d = x[x.delay_h >= 0]
    return {
        "n": len(x), "n_delay_nonneg": len(d),
        "delay_h median": float(d.delay_h.median()), "delay_h p75": float(d.delay_h.quantile(.75)), "delay_h mean": float(d.delay_h.mean()),
        "share caught after >1h": float((d.delay_h > 1).mean()), "share after >24h": float((d.delay_h > 24).mean()),
        "share after >7d": float((d.delay_h > 168).mean()),
        "closed_life_h median": float(x.closed_life_h.median()),
        "closed PR unmerged share": float((~x.closed_merged).mean()),
        "human comments before flag (total)": int(x.human_comments.sum()), "reviews before flag (total)": int(x.reviews.sum()),
        "commits on closed PR (total)": int(x.commits.sum()), "lines added (total)": int(x.lines_added.sum()),
        "lines added median": float(x.lines_added.median()),
        "share with >=1 human comment or review before flag": float(((x.human_comments + x.reviews) > 0).mean()),
    }


S = {"all": summ(R), "cross-author": summ(R[~R.self]), "same-author": summ(R[R.self])}
with open(os.path.join(OUT, "duplicate_cost_summary.json"), "w") as fh:
    json.dump(S, fh, indent=1)
print(json.dumps(S, indent=1))
