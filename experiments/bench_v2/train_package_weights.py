"""Train the shipped Jinx weights on the full AIDev live-queue benchmark (same recipe as eval2.py folds).

Writes src/jinx_pr/data/weights.json (lexical) and weights_emb.json (lexical + MiniLM), then checks that
jinx_pr.Detector.score_rows reproduces sklearn's probabilities exactly.
"""
import json
import os
import pickle
import re
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(H, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from jinx_pr.scorer import Detector

D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
LEX = ["text_tfidf", "title_tfidf", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue", "mention_ref",
       "same_author", "same_agent", "log_gap_hours", "cand_open"]
with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
F = pd.read_parquet(D + "features.parquet")
# Same real-use queues as eval2.py: only PRs open when the new PR arrived (the 200 most recent), forward-only mentions,
# and labelled queries only when the true duplicate is in that queue.
F = F[F.cand_open > 0]
F = F[F.groupby("qi").log_gap_hours.rank(method="first") <= 200]
F = F[F.qi.isin({i for i, q in enumerate(Q) if q["neg"]} | set(F[F.gold].qi))].reset_index(drop=True)
_P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body"]).set_index("id")
_REF = re.compile(r"(?:#|/pull/|/issues/)(\d+)")
_ment = {x["q"]: {int(m) for m in _REF.findall(f"{_P.title.get(x['q']) or ''}\n{_P.body.get(x['q']) or ''}")} for x in Q}
F["mention_ref"] = [float(int(n) in _ment[Q[qi]["q"]]) for qi, n in zip(F.qi, _P.number.reindex(F.cand.values).values)]
F["y"] = (F.gold | F.other_gold).astype(int)
T = F[~F.other_gold]
X = pd.concat([T[T.y == 1], T[T.y == 0].groupby("qi", group_keys=False)[T.columns].apply(lambda d: d.sample(min(len(d), 100), random_state=0))])
cross = {i for i, q in enumerate(Q) if not q["neg"] and not q["self"]}

for fname, cols in [("weights.json", LEX), ("weights_emb.json", LEX + ["emb_cos"])]:
    sc = StandardScaler().fit(X[cols])
    mdl = LogisticRegression(C=1.0, class_weight="balanced", max_iter=3000).fit(sc.transform(X[cols]), X.y)
    z = mdl.decision_function(sc.transform(F[cols]))
    top1 = pd.Series(z).groupby(F.qi.values).max()
    z_thr = float(np.quantile(top1[top1.index.isin(cross)], 0.5))
    # Shift the intercept so the benchmark operating point is score 0.5; ranking is unchanged.
    w = {"features": cols, "coef": mdl.coef_[0].tolist(), "intercept": float(mdl.intercept_[0]) - z_thr,
         "mean": sc.mean_.tolist(), "scale": sc.scale_.tolist(), "threshold": 0.5,
         "note": f"LR trained on all {F.qi.nunique()} AIDev real-use-queue queries (open PRs only, 200 most recent) ({len(X)} pairs); intercept shifted so "
                 "score 0.5 = median top-1 logit of cross-author queries (the benchmark false-alarm operating point). "
                 "Built by experiments/bench_v2/train_package_weights.py"}
    rows = F[cols].to_dict("records")
    ours = np.array(Detector(weights=w).score_rows(rows))
    ref = 1 / (1 + np.exp(-np.clip(z - z_thr, -30, 30)))
    diff = float(np.abs(ours - ref).max())
    assert diff < 1e-6, diff
    with open(os.path.join(ROOT, "src", "jinx_pr", "data", fname), "w") as fh:
        json.dump(w, fh, indent=1)
    print(fname, "pairs", len(X), "logit shift", round(z_thr, 3), "max |package - sklearn|", f"{diff:.2e}")
