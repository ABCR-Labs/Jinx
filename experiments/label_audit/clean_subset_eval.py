"""Re-score key strategies on cross-author pairs whose silver label the audit judged valid (duplicate or replacement)."""
import json
import os

import numpy as np
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
R = pd.read_parquet(os.path.join(H, "..", "results", "ranks.parquet"))
A = pd.read_parquet(os.path.join(H, "audit_cross_pairs.parquet"))[["qi", "repo"]].merge(
    pd.read_json(os.path.join(H, "audit_cross_labels.jsonl"), lines=True)[["qi", "label"]], on="qi")
M = {"Jinx": "Jinx + MiniLM, LR (current tool)", "All signals, LR": "All signals, LR",
     "INTRUDE + time": "INTRUDE + time (Wang et al. 2019), LR", "contrib-guard": "contrib-guard/phoenix (bot, exact port)",
     "Claude Haiku + Jinx": "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5", "Links only": "Links only (same issue / #ref)"}
metrics = {"R@1": lambda r: (r == 1).astype(float), "R@5": lambda r: (r <= 5).astype(float), "MRR": lambda r: 1.0 / r}


def boot(df, f, n=2000):
    repos = df.repo.unique()
    g = {k: v.index.to_numpy() for k, v in df.groupby("repo")}
    rng = np.random.default_rng(0)
    out = []
    for _ in range(n):
        idx = np.concatenate([g[r] for r in rng.choice(repos, len(repos))])
        out.append(f(df.loc[idx]))
    return float(np.quantile(out, 0.025)), float(np.quantile(out, 0.975))


res = {}
for subset, keep in [("all cross-author", A.label.notna()), ("audit-valid (duplicate+replacement)", A.label.isin(["duplicate", "replacement"])),
                     ("audit-valid incl. subsumed", A.label.isin(["duplicate", "replacement", "subsumed"]))]:
    S = A[keep].reset_index(drop=True)
    rk = R.loc[S.qi]
    out = {"n": len(S)}
    for name, col in M.items():
        r = rk[col].to_numpy()
        out[name] = {m: round(float(fn(r).mean()), 3) for m, fn in metrics.items()}
    for m, fn in metrics.items():
        d = pd.DataFrame({"repo": S.repo, "a": fn(rk[M["Jinx"]].to_numpy()), "b": fn(rk[M["INTRUDE + time"]].to_numpy())})
        lo, hi = boot(d, lambda x: (x.a - x.b).mean())
        out[f"Jinx - INTRUDE {m} [d, lo, hi]"] = [round(float((d.a - d.b).mean()), 3), round(lo, 3), round(hi, 3)]
    res[subset] = out
with open(os.path.join(H, "clean_subset_results.json"), "w") as fh:
    json.dump(res, fh, indent=1)
for k, v in res.items():
    print(k, v["n"], {n: v[n]["R@1"] for n in M}, "dR@1", v["Jinx - INTRUDE R@1 [d, lo, hi]"], "dR@5", v["Jinx - INTRUDE R@5 [d, lo, hi]"])
