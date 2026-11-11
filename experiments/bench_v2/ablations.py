"""Robustness checks requested by the review panel (CPU only, no API).

1. cand_open: Jinx without the "older PR still open" signal, and INTRUDE + time given that signal.
2. Link leakage: replace the symmetric mention_ref with a forward-only mention (the new PR's own title/body names the older PR).
3. Deployment-like queues: only PRs that were open when the new PR arrived (no 7-day grace window), the 200 most recent.
Same 5 repository-grouped folds, LR training, ranking, median thresholds and repository-cluster bootstrap as eval2.py.
Writes experiments/results/ablations.csv and ablations_paired.csv.
"""
import os
import pickle
import re

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

D = "/home/ubuntu/research/prdupecheck/data/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "repo_url", "number", "title", "body"]).set_index("id")
F0 = pd.read_parquet(D + "features.parquet")
meta = pd.DataFrame([{"qi": i, "neg": x["neg"], "self": x["self"], "repo": P.repo_url[x["q"]]} for i, x in enumerate(Q)]).set_index("qi")
folds = list(GroupKFold(n_splits=5).split(meta.index, groups=meta.repo))
REF = re.compile(r"(?:#|/pull/|/issues/)(\d+)")
ment = {}
for x in Q:
    r = P.loc[x["q"]]
    ment[x["q"]] = {int(m) for m in REF.findall(f"{r.title or ''}\n{r.body or ''}")}
qid = np.array([Q[q]["q"] for q in F0.qi])
cnum = P.number.reindex(F0.cand.values).values
F0["mention_fwd"] = [float(int(n) in ment[q]) for q, n in zip(qid, cnum)]
F0["y"] = (F0.gold | F0.other_gold).astype(int)
F0["tie"] = np.random.default_rng(0).random(len(F0)) * 1e-9

LEX = ["text_tfidf", "title_tfidf", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue", "mention_ref",
       "same_author", "same_agent", "log_gap_hours", "cand_open"]
JINX = LEX + ["emb_cos"]
INTR = ["title_tfidf_raw", "text_tfidf_raw", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue_text", "mention_ref",
        "log_gap_hours"]


def fwd(cols):
    return [("mention_fwd" if c == "mention_ref" else c) for c in cols]


def drop(cols, c):
    return [x for x in cols if x != c]


def boot(vals, repos, nb=1000, seed=5):
    rs = np.random.default_rng(seed)
    codes, u = pd.factorize(repos.values)
    vals = np.asarray(vals, float)
    sums = np.zeros((len(u), vals.shape[1]))
    np.add.at(sums, codes, vals)
    cnt = np.bincount(codes, minlength=len(u)).astype(float)
    W = rs.multinomial(len(u), np.full(len(u), 1.0 / len(u)), size=nb).astype(float)
    return np.percentile((W @ sums) / (W @ cnt)[:, None], [2.5, 97.5], axis=0)


def train(F, cols):
    s = pd.Series(np.nan, index=F.index)
    for tr, te in folds:
        m = F.qi.isin(set(meta.index[tr])) & ~F.other_gold
        T = F[m]
        X = pd.concat([T[T.y == 1], T[T.y == 0].groupby("qi", group_keys=False).apply(lambda d: d.sample(min(len(d), 100), random_state=0))])
        sc = StandardScaler().fit(X[cols])
        mdl = LogisticRegression(C=1.0, class_weight="balanced", max_iter=3000).fit(sc.transform(X[cols]), X.y)
        tem = F.qi.isin(set(meta.index[te]))
        s[tem] = mdl.predict_proba(sc.transform(F.loc[tem, cols]))[:, 1]
    return s


def ranks(F, col):
    s = F[~F.other_gold][["qi", "gold", "tie"]].copy()
    s["v"] = F[col] + s.tie
    gv = s[s.gold].set_index("qi").v
    s = s.join(gv.rename("gv"), on="qi")
    s = s[s.gv.notna()]
    return (s.v > s.gv).groupby(s.qi).sum() + 1


def far(F, col, R, xq):
    t1 = F.groupby("qi")[col].max()
    out, hit = [], []
    for tr, te in folds:
        trx = [q for q in meta.index[tr] if q in xq]
        thr = np.quantile(t1.reindex(trx).dropna().values, 0.5)
        ten = [q for q in meta.index[te] if meta.neg[q] and q in t1.index]
        tex = [q for q in meta.index[te] if q in xq]
        out += list(t1.reindex(ten).values >= thr)
        hit += list((t1.reindex(tex).values >= thr) & (R.reindex(tex).values == 1))
    return float(np.mean(out)), float(np.mean(hit))


def queue_open200(F):
    G = F[F.cand_open > 0].copy()
    G["_r"] = G.groupby("qi").log_gap_hours.rank(method="first")
    return G[G._r <= 200].drop(columns="_r")


SETTINGS = {
    "benchmark queues (as in paper)": (lambda F: F, {"Jinx": JINX, "INTRUDE + time": INTR, "Jinx without cand_open": drop(JINX, "cand_open"),
                                                      "INTRUDE + time + cand_open": INTR + ["cand_open"]}),
    "forward-only mentions": (lambda F: F, {"Jinx": fwd(JINX), "INTRUDE + time": fwd(INTR)}),
    "open-only queues, top 200": (queue_open200, {"Jinx": drop(JINX, "cand_open"), "INTRUDE + time": INTR}),
    "open-only queues, top 200, forward-only mentions": (queue_open200, {"Jinx": fwd(drop(JINX, "cand_open")), "INTRUDE + time": fwd(INTR),
                                                                          "Jinx without MiniLM": fwd(drop(LEX, "cand_open"))}),
}
rows, prs = [], []
for sname, (qf, methods) in SETTINGS.items():
    F = qf(F0).reset_index(drop=True)
    answerable = set(F[F.gold].qi)
    xq = set(meta.index[(~meta.neg) & (meta.self == False)]) & answerable
    xl = sorted(xq)
    R = {}
    for mname, cols in methods.items():
        F[mname] = train(F, cols)
        R[mname] = ranks(F, mname)
        r = R[mname].reindex(xl).values
        v = np.stack([r <= 1, r <= 5, 1 / r], 1).astype(float)
        lo, hi = boot(v, meta.repo.reindex(xl), nb=500, seed=1)
        fa, alerts = far(F, mname, R[mname], xq)
        rows.append({"setting": sname, "method": mname, "n cross-author": len(xl), "R@1": v[:, 0].mean(), "R@1 lo": lo[0], "R@1 hi": hi[0],
                     "R@5": v[:, 1].mean(), "MRR": v[:, 2].mean(), "FAR": fa, "cross-author correct alerts": alerts})
        print(rows[-1], flush=True)
    a, b = R["Jinx"].reindex(xl).values, R["INTRUDE + time"].reindex(xl).values
    d = np.stack([(a <= 1).astype(float) - (b <= 1), (a <= 5).astype(float) - (b <= 5), 1 / a - 1 / b], 1)
    lo, hi = boot(d, meta.repo.reindex(xl))
    prs.append({"setting": sname, "n cross-author": len(xl), "dR@1": d[:, 0].mean(), "dR@1 lo": lo[0], "dR@1 hi": hi[0],
                "dR@5": d[:, 1].mean(), "dR@5 lo": lo[1], "dR@5 hi": hi[1], "dMRR": d[:, 2].mean(), "dMRR lo": lo[2], "dMRR hi": hi[2]})
    print(prs[-1], flush=True)
pd.DataFrame(rows).to_csv(os.path.join(OUT, "ablations.csv"), index=False)
pd.DataFrame(prs).to_csv(os.path.join(OUT, "ablations_paired.csv"), index=False)
gold = F0[F0.gold]
xa = gold.qi.isin(meta.index[(~meta.neg) & (meta.self == False)])
print("cross-author gold pairs with symmetric mention:", int((gold[xa].mention_ref > 0).sum()), "forward:", int((gold[xa].mention_fwd > 0).sum()))
print("cross-author gold closed at query time (grace window):", int((gold[xa].cand_open == 0).sum()))
