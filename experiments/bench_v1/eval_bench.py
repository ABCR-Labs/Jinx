"""Live-queue scoring: Recall@1/5, MRR, split by relation type, repo-cluster bootstrap CIs, false alarms."""
import pickle, json, sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
D = "/home/ubuntu/research/prdupecheck/data/"
OUT = "/home/ubuntu/research/prdupecheck/results/"
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "repo_url"]).set_index("id").repo_url
F = pd.read_parquet(D + (sys.argv[1] if len(sys.argv) > 1 else "features.parquet"))
OUT = OUT + (sys.argv[2] if len(sys.argv) > 2 else "")
meta = pd.DataFrame([{"qi": i, "neg": x["neg"], "self": x["self"], "same_agent": x["same_agent"], "repo": pr[x["q"]],
                      "n": len(x["cand"])} for i, x in enumerate(Q)]).set_index("qi")
gm = F[F.gold].set_index("qi")
meta["ref"] = (gm.mention_ref > 0).reindex(meta.index).fillna(False)
rng = np.random.default_rng(0)
F["tie"] = rng.random(len(F)) * 1e-9
F["y"] = (F.gold | F.other_gold).astype(int)
LEX = ["text_tfidf", "title_tfidf", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue",
       "mention_ref", "same_author", "same_agent", "log_gap_hours", "cand_open"]
FULL = LEX + ["emb_cos"]
INTRUDE = ["title_tfidf_raw", "text_tfidf_raw", "file_jacc", "file_contain", "hunk_overlap", "line_contain",
           "same_issue_text", "mention_ref"]
TRAINED = {
    "Ren et al. 2019 (INTRUDE clues, LR)": INTRUDE,
    "Wang et al. 2019 (INTRUDE + time, LR)": INTRUDE + ["log_gap_hours"],
    "Jinx (lexical)": LEX,
    "Jinx (+ local embedding)": FULL,
    "ablation: no template stripping": [c for c in FULL if c not in ("text_tfidf", "title_tfidf", "emb_cos")] + ["text_tfidf_raw", "title_tfidf_raw", "cos_raw"],
    "ablation: no code overlap": [c for c in FULL if c not in ("file_jacc", "file_contain", "hunk_overlap", "line_contain")],
    "ablation: no issue/reference links": [c for c in FULL if c not in ("same_issue", "mention_ref")],
    "ablation: no author/agent context": [c for c in FULL if c not in ("same_author", "same_agent")],
    "ablation: no time features": [c for c in FULL if c not in ("log_gap_hours", "cand_open")],
}
# untrained scores (tools' documented scoring with a local model)
F["Li et al. 2017 (TF-IDF title+description)"] = 0.5 * F.title_tfidf_raw + 0.5 * F.text_tfidf_raw
F["Plain embedding (MiniLM, raw text)"] = F.cos_raw
F["PRSense v2.2 (re-impl, local MiniLM)"] = 0.45 * F.cos_raw + 0.35 * F.cos_diff + 0.20 * F.file_jacc
F["PRism (re-impl: embedding stage, local MiniLM)"] = F.cos_prism
F["Simili-bot (re-impl: vector stage, local MiniLM)"] = F.cos_simili
if "vt_rrf" in F:
    # as shipped: results outside vector/FTS top-5 or below display similarity 0.75 are never shown -> ranked last
    F["vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM)"] = F.vt_rrf * (F.vt_display >= 0.75) + 1e-6 * F.vt_vec
    F["vector-triage, no 0.75 filter (re-impl, local MiniLM)"] = F.vt_rrf + 1e-6 * F.vt_vec
F["contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)"] = F.cg_phoenix
F["contrib-guard/balyakin (tool's own code: title Jaccard + same files)"] = F.cg_balyakin + 1e-3 * F.cg_balyakin_files
F["cg_bal_strict"] = F.cg_balyakin * F.cg_balyakin_files
if "vt_display" in F:
    DEFAULT_THR_VT = {"vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM)": ("vt_dup", 0.92)}
    F["vt_dup"] = F.vt_display * (F.vt_rrf > 0)
UNTRAINED = [c for c in F.columns if "(" in c and c not in TRAINED]
# documented defaults: PRSense possibleThreshold 0.82; PRism duplicate-threshold 0.85 (action.yml); Simili similarity_threshold 0.65
# (config.go); contrib-guard/phoenix SIMILARITY_THRESHOLD 0.4 (code); balyakin strict policy title>=0.9 & same files
DEFAULT_THR = {"PRSense v2.2 (re-impl, local MiniLM)": 0.82, "PRism (re-impl: embedding stage, local MiniLM)": 0.85,
               "Simili-bot (re-impl: vector stage, local MiniLM)": 0.65,
               "contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)": 0.4,
               "contrib-guard/balyakin (tool's own code: title Jaccard + same files)": ("cg_bal_strict", 0.9)}
if "vt_display" in F: DEFAULT_THR.update(DEFAULT_THR_VT)
qrepo = F.qi.map(meta.repo)
folds = list(GroupKFold(n_splits=5).split(meta.index, groups=meta.repo))
for name, cols in TRAINED.items():
    F[name] = np.nan
    if F[cols].isna().any().any(): continue
    for tr, te in folds:
        trq = set(meta.index[tr]); m = F.qi.isin(trq) & ~F.other_gold
        T = F[m]
        pos = T[T.y == 1]
        neg = T[T.y == 0].groupby("qi", group_keys=False).apply(lambda d: d.sample(min(len(d), 100), random_state=0))
        X = pd.concat([pos, neg])
        sc = StandardScaler().fit(X[cols]); lr = LogisticRegression(C=1.0, class_weight="balanced", max_iter=3000)
        lr.fit(sc.transform(X[cols]), X.y)
        te_m = F.qi.isin(set(meta.index[te]))
        F.loc[te_m, name] = lr.predict_proba(sc.transform(F.loc[te_m, cols]))[:, 1]
METHODS = [c for c in UNTRAINED + list(TRAINED) if F[c].notna().all()]
print("skipped (embeddings not ready):", [c for c in UNTRAINED + list(TRAINED) if c not in METHODS])

def ranks(col):
    s = F[~F.other_gold][["qi", "gold", col, "tie"]].copy(); s["v"] = s[col] + s.tie
    gv = s[s.gold].set_index("qi").v
    s = s.join(gv.rename("gv"), on="qi"); s = s[s.gv.notna()]
    return (s.v > s.gv).groupby(s.qi).sum() + 1

def top1(col):
    return F.groupby("qi")[col].max()

GROUPS = {"all labelled": lambda m: ~m.neg, "self-replacement (same author)": lambda m: (~m.neg) & (m.self == True),
          "cross-author": lambda m: (~m.neg) & (m.self == False),
          "cross-author, same agent": lambda m: (~m.neg) & (m.self == False) & (m.same_agent == True),
          "cross-author, cross-agent": lambda m: (~m.neg) & (m.self == False) & (m.same_agent == False),
          "cross-author, no explicit #ref to gold": lambda m: (~m.neg) & (m.self == False) & (~m.ref),
          "self-replacement, no explicit #ref to gold": lambda m: (~m.neg) & (m.self == True) & (~m.ref)}
R = {c: ranks(c) for c in METHODS}

def boot(vals, repos, nb=2000, seed=1):
    rs = np.random.default_rng(seed); u = repos.unique(); idx = {r: np.where(repos.values == r)[0] for r in u}
    out = []
    for _ in range(nb):
        pick = np.concatenate([idx[r] for r in rs.choice(u, len(u))]); out.append(vals[pick].mean(0))
    return np.percentile(np.array(out), [2.5, 97.5], axis=0)

rows = []
for gname, fn in GROUPS.items():
    qs = meta.index[fn(meta)]
    for c in METHODS:
        r = R[c].reindex(qs).values
        v = np.stack([r <= 1, r <= 5, 1 / r], 1).astype(float)
        lo, hi = boot(v, meta.repo.reindex(qs), nb=500)
        rows.append({"group": gname, "method": c, "n": len(qs), "R@1": v[:, 0].mean(), "R@5": v[:, 1].mean(), "MRR": v[:, 2].mean(),
                     "R@5 lo": lo[1], "R@5 hi": hi[1], "R@1 lo": lo[0], "R@1 hi": hi[0]})
res = pd.DataFrame(rows)
# paired bootstrap: Jinx vs best baseline on cross-author R@5
xq = meta.index[GROUPS["cross-author"](meta)]
base = [c for c in METHODS if not c.startswith("Jinx") and not c.startswith("ablation")]
cross = res[res.group == "cross-author"].set_index("method")
best = cross.loc[base, "R@5"].idxmax()
paired = {}
for ours in [m for m in ["Jinx (lexical)", "Jinx (+ local embedding)"] if m in METHODS]:
    d = np.stack([(R[ours].reindex(xq).values <= 5).astype(float) - (R[best].reindex(xq).values <= 5).astype(float),
                  1 / R[ours].reindex(xq).values - 1 / R[best].reindex(xq).values], 1)
    lo, hi = boot(d, meta.repo.reindex(xq), nb=5000, seed=7)
    r1 = (R[ours].reindex(xq).values <= 1).astype(float) - (R[best].reindex(xq).values <= 1).astype(float)
    lo1, hi1 = boot(r1[:, None], meta.repo.reindex(xq), nb=5000, seed=8)
    paired[ours] = {"vs": best, "dR@5": d[:, 0].mean(), "dR@5 CI": [lo[0], hi[0]], "dMRR": d[:, 1].mean(), "dMRR CI": [lo[1], hi[1]],
                    "dR@1": r1.mean(), "dR@1 CI": [lo1[0], hi1[0]]}
    for gname in ["cross-author, no explicit #ref to gold"]:
        gq = meta.index[GROUPS[gname](meta)]; cg = res[res.group == gname].set_index("method")
        b2 = cg.loc[base, "R@5"].idxmax()
        dd = np.stack([(R[ours].reindex(gq).values <= k).astype(float) - (R[b2].reindex(gq).values <= k).astype(float) for k in (1, 5)]
                      + [1 / R[ours].reindex(gq).values - 1 / R[b2].reindex(gq).values], 1)
        l2, h2 = boot(dd, meta.repo.reindex(gq), nb=5000, seed=9)
        paired[ours][gname] = {"vs": b2, "n": len(gq), "dR@1": dd[:, 0].mean(), "dR@1 CI": [l2[0], h2[0]], "dR@5": dd[:, 1].mean(),
                               "dR@5 CI": [l2[1], h2[1]], "dMRR": dd[:, 2].mean(), "dMRR CI": [l2[2], h2[2]]}
bots = [c for c in base if not c.startswith(("Li et al", "Ren et al", "Wang et al", "Plain embedding"))]
bestbot = cross.loc[bots, "R@5"].idxmax()
for ours in [m for m in ["Jinx (lexical)", "Jinx (+ local embedding)"] if m in METHODS]:
    for gname in ["cross-author", "cross-author, no explicit #ref to gold"]:
        gq = meta.index[GROUPS[gname](meta)]
        dd = np.stack([(R[ours].reindex(gq).values <= k).astype(float) - (R[bestbot].reindex(gq).values <= k).astype(float) for k in (1, 5)]
                      + [1 / R[ours].reindex(gq).values - 1 / R[bestbot].reindex(gq).values], 1)
        l2, h2 = boot(dd, meta.repo.reindex(gq), nb=5000, seed=11)
        paired[ours]["vs best existing bot, " + gname] = {"vs": bestbot, "n": len(gq), "dR@1": dd[:, 0].mean(), "dR@1 CI": [l2[0], h2[0]],
            "dR@5": dd[:, 1].mean(), "dR@5 CI": [l2[1], h2[1]], "dMRR": dd[:, 2].mean(), "dMRR CI": [l2[2], h2[2]]}
pd.DataFrame(R).to_parquet(OUT + "ranks.parquet")
# false alarms: threshold per fold so that 50% of training cross-author queries alert (top-1 >= thr)
fa = []; FARQ = {}
negq = meta.index[meta.neg]
for c in METHODS:
    t1 = top1(c); far, hit, alert, farq = [], [], [], []
    for tr, te in folds:
        trq, teq = meta.index[tr], meta.index[te]
        trx = [q for q in trq if q in set(xq)]
        thr = np.quantile(t1.reindex(trx).values, 0.5)
        ten = [q for q in teq if meta.neg[q]]; tex = [q for q in teq if q in set(xq)]
        far += list(t1.reindex(ten).values >= thr); farq += ten
        hit += list((t1.reindex(tex).values >= thr) & (R[c].reindex(tex).values == 1))
    row = {"method": c, "FAR@50%train-detection": np.mean(far), "cross-author correct alerts": np.mean(hit)}
    FARQ[c] = pd.Series(np.array(far, float), index=farq)
    if c in DEFAULT_THR:
        col, thr = DEFAULT_THR[c] if isinstance(DEFAULT_THR[c], tuple) else (c, DEFAULT_THR[c])
        fl = F.groupby("qi")[col].max() >= thr
        row["FAR@tool default"] = fl.reindex(negq).mean()
        row["cross-author correct alerts@default"] = np.mean(fl.reindex(xq).values & (R[c].reindex(xq).values == 1))
    fa.append(row)
fa = pd.DataFrame(fa)
for ours in [m for m in ["Jinx (lexical)", "Jinx (+ local embedding)"] if m in METHODS]:
    bfa = fa[fa.method.isin(base)].set_index("method")["FAR@50%train-detection"].idxmin()
    d = (FARQ[ours] - FARQ[bfa].reindex(FARQ[ours].index)).values[:, None]
    lo, hi = boot(d, meta.repo.reindex(FARQ[ours].index), nb=5000, seed=10)
    paired[ours]["FAR"] = {"vs lowest-FAR baseline": bfa, "dFAR": float(d.mean()), "dFAR CI": [lo[0], hi[0]]}
lat = (F.groupby("qi").t_lex.sum() * 1000)
import os; os.makedirs(OUT, exist_ok=True)
res.to_csv(OUT + "ranking.csv", index=False); fa.to_csv(OUT + "false_alarms.csv", index=False)
json.dump({"paired": paired, "best_baseline_cross_author_R@5": best,
           "lexical_feature_ms_per_query": {"median": float(lat.median()), "p90": float(lat.quantile(0.9)), "max": float(lat.max())},
           "queue_size": {"median": float(meta.n.median()), "p90": float(meta.n.quantile(0.9))}},
          open(OUT + "summary.json", "w"), indent=1, default=float)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
for g in GROUPS:
    print("\n==", g); print(res[res.group == g].drop(columns="group").round(3).to_string(index=False))
print(fa.round(3).to_string(index=False)); print(json.dumps(paired, indent=1, default=float)); print(lat.describe().round(1))
