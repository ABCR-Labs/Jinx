"""Attach repo-grouped fold ids (identical to eval2.py) and labels to the top-10 pairs for fine-tuning on Modal."""
import pickle, numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
D = "/home/ubuntu/research/prdupecheck/data/"
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "repo_url"]).set_index("id")
repo = pd.Series([P.repo_url[x["q"]] for x in Q])
folds = list(GroupKFold(n_splits=5).split(np.arange(len(Q)), groups=repo))
fold = np.zeros(len(Q), int)
for k, (_, te) in enumerate(folds): fold[te] = k
F = pd.read_parquet(D + "features.parquet", columns=["qi", "cand", "gold", "other_gold"])
T = pd.read_parquet(D + "modal_pairs.parquet").merge(F, on=["qi", "cand"], how="left")
T["fold"] = fold[T.qi.values]; T["y"] = (T.gold | T.other_gold).astype(int)
T.to_parquet(D + "modal_pairs_folds.parquet"); print(T.groupby("fold").agg(n=("y", "size"), pos=("y", "sum")))
