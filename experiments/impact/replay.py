"""Replay: if Jinx had commented when each new PR was opened, what would maintainers have gained?

Uses the per-query scores and per-fold thresholds that eval2.py writes (results/alerts.parquet: repository-grouped
out-of-fold models, real-use queues) and the human detection delays from duplicate_cost.py (results/duplicate_cost.csv).
A "correct warning" means the top-scoring open PR is the true duplicate and its score passes the threshold.
Writes results/replay_impact.csv.
"""
import os
import pickle

import numpy as np
import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
A = pd.read_parquet(os.path.join(R, "alerts.parquet"))
C = pd.read_csv(os.path.join(R, "duplicate_cost.csv")).set_index("qi")

with open("/home/ubuntu/research/prdupecheck/data/bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
neg = {i for i, x in enumerate(Q) if x["neg"]}
_P = pd.read_parquet("/home/ubuntu/research/prdupecheck/data/pull_request.parquet", columns=["id", "repo_url"]).set_index("id").repo_url
REPO = {i: _P.get(int(x["q"])) for i, x in enumerate(Q)}


def boot(v, idx, nb=2000, seed=3):
    """Repository-cluster bootstrap 95% CI of a mean."""
    df = pd.DataFrame({"v": np.asarray(v, float), "r": [REPO[i] for i in idx]})
    g = df.groupby("r").v.agg(["sum", "count"]); rng = np.random.default_rng(seed); k = len(g)
    s = np.array([g.iloc[rng.integers(0, k, k)].sum() for _ in range(nb)])
    return np.quantile(s[:, 0] / s[:, 1], [0.025, 0.975])


self_ = {i for i, x in enumerate(Q) if x["self"] and not x["neg"]}
rows = []
for m, g in A.groupby("method"):
    g = g.set_index("qi")
    alert = g.top1 >= g.thr
    pos = g[~g.index.isin(neg) & g["rank"].notna()]
    ok = (pos.top1 >= pos.thr) & (pos["rank"] == 1)
    wrong = (pos.top1 >= pos.thr) & (pos["rank"] != 1)
    for grp, idx in [("all duplicates", pos.index), ("cross-author", pos.index[~pos.index.isin(self_)])]:
        d = C.reindex(idx)
        late = d.delay_h > 1
        okg = ok.reindex(idx)
        rows.append({
            "method": m, "group": grp, "n": len(idx),
            "correct warning at open": okg.mean(),
            "correct warning lo": boot(okg.values, idx)[0], "correct warning hi": boot(okg.values, idx)[1],
            "wrong-PR warning at open": wrong.reindex(idx).mean(),
            "correct warning, human took >1h": okg[late.values].mean(),
            "correct warning, human took >24h": okg[(d.delay_h > 24).values].mean(),
            "hours saved (sum, correct warnings)": float(d.delay_h.clip(lower=0)[okg.values].sum()),
            "hours saved per warned duplicate (median)": float(d.delay_h.clip(lower=0)[okg.values].median()),
            "reviews+comments before flag avoided": int((d.reviews + d.human_comments)[okg.values].sum()),
            "false alarms per 100 PRs without duplicate": 100 * alert[alert.index.isin(neg)].mean(),
        })
out = pd.DataFrame(rows)
out.to_csv(os.path.join(R, "replay_impact.csv"), index=False)
print(out.to_string())
