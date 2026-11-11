"""Dedup strategy study on the AIDev live-queue benchmark.
Strategies x duplicate classes; Recall@1/5, MRR with repo-cluster bootstrap CIs; paired tests; false alarms;
operating curves; random-pair vs live-queue evaluation; error analysis. Writes to jinx_pr/experiments/results/."""
import pickle, json, os, re, sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
from scipy.stats import kendalltau
D = "/home/ubuntu/research/prdupecheck/data/"
OUT = os.environ.get("OUT", "/home/ubuntu/research/prdupecheck/jinx_pr/experiments/results/"); os.makedirs(OUT, exist_ok=True)
NB = int(os.environ.get("NB", 2000))
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "repo_url", "title", "number", "user", "agent"]).set_index("id")
F = pd.read_parquet(D + "features.parquet")
F = F.merge(pd.read_parquet(D + "feat_bm25.parquet"), on=["qi", "cand"], how="left")
# QUEUE=open200 (default): only PRs still open when the new PR arrived, the 200 most recent (what the Action sees).
# QUEUE=grace7: the original queues, which also hold PRs closed in the previous 7 days (results_grace7/).
QUEUE = os.environ.get("QUEUE", "open200")
if QUEUE == "open200":
    F = F[F.cand_open > 0].copy(); F["_rk"] = F.groupby("qi").log_gap_hours.rank(method="first")
    CAP_DROPPED = sorted(int(q) for q in set(F[F.gold & (F._rk > 200)].qi)); F = F[F._rk <= 200].drop(columns="_rk").reset_index(drop=True)
else:
    CAP_DROPPED = []
qidx = np.array([Q[q]["q"] for q in F.qi])
# Forward-only mentions: count a link only if the new PR's own title/body names the older PR. The older PR's text in the
# AIDev snapshot may have been edited after the duplicate was found, which a live run would not see.
_P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body"]).set_index("id")
_REF = re.compile(r"(?:#|/pull/|/issues/)(\d+)")
_ment = {x["q"]: {int(m) for m in _REF.findall(f"{_P.title.get(x['q']) or ''}\n{_P.body.get(x['q']) or ''}")} for x in Q}
F["mention_ref"] = [float(int(n) in _ment[q]) for q, n in zip(qidx, _P.number.reindex(F.cand.values).values)]
EMBS = {}
for tag in ["bge_raw", "bge_stripped", "bge_diff", "bgebase_stripped", "unix_diff", "unix_stripped", "codebert_diff", "jinacode_diff"]:
    if os.path.exists(D + f"emb_{tag}.npz"):
        E = np.load(D + f"emb_{tag}.npz"); ix = {int(i): k for k, i in enumerate(E["ids"])}; M = E["emb"].astype(np.float32)
        a = np.array([ix[int(i)] for i in qidx]); b = np.array([ix[int(c)] for c in F.cand])
        F["cos_" + tag] = np.einsum("ij,ij->i", M[a], M[b]); EMBS[tag] = True
meta = pd.DataFrame([{"qi": i, "neg": x["neg"], "self": x["self"], "same_agent": x["same_agent"], "repo": P.repo_url[x["q"]],
                      "n": len(x["cand"])} for i, x in enumerate(Q)]).set_index("qi")
# keep labelled queries only if the true duplicate is still in the (real-use) queue; a closed one cannot be flagged live
meta = meta[meta.index.isin(set(F.qi)) & (meta.neg | meta.index.isin(set(F[F.gold].qi)))]; F = F[F.qi.isin(meta.index)].reset_index(drop=True)
meta["n"] = F.groupby("qi").size().reindex(meta.index)
gm = F[F.gold].set_index("qi")
meta["ref"] = (gm.mention_ref > 0).reindex(meta.index).fillna(False).astype(bool)
meta["issue"] = (gm.same_issue > 0).reindex(meta.index).fillna(False).astype(bool)
def code_class(r):
    if r.line_contain >= 0.5: return "A. code twin (>=50% identical changed lines)"
    if r.hunk_overlap > 0 or r.line_contain > 0: return "B. partial code overlap"
    if r.file_jacc > 0: return "C. same files, different code"
    return "D. no shared files (intent-level)"
meta["cls"] = gm.apply(code_class, axis=1).reindex(meta.index)
rng = np.random.default_rng(0); F["tie"] = rng.random(len(F)) * 1e-9; F["y"] = (F.gold | F.other_gold).astype(int)

S = {}  # name -> (family, column)
def add(name, fam, vals): F[name] = vals; S[name] = fam
add("Recency only (newest open PR first)", "0 trivial", -F.log_gap_hours)
add("TF-IDF raw text (Li et al. 2017)", "1 lexical", 0.5 * F.title_tfidf_raw + 0.5 * F.text_tfidf_raw)
add("TF-IDF template-stripped", "1 lexical", 0.5 * F.title_tfidf + 0.5 * F.text_tfidf)
add("BM25 raw text", "1 lexical", F.bm25_raw); add("BM25 template-stripped", "1 lexical", F.bm25_stripped)
add("BM25 on diff", "2 code", F.bm25_diff)
add("Changed-files Jaccard", "2 code", F.file_jacc); add("Hunk overlap", "2 code", F.hunk_overlap)
add("Identical changed lines", "2 code", F.line_contain)
add("Code overlap sum (files+hunks+lines)", "2 code", F.file_jacc + F.hunk_overlap + F.line_contain)
add("Links only (same issue / #ref)", "3 links", F.same_issue + F.mention_ref + 1e-3 * F.text_tfidf_raw)
add("Links only, no tie-break (same issue / #ref)", "3 links", F.same_issue + F.mention_ref)
add("MiniLM raw text", "4 embedding", F.cos_raw); add("MiniLM template-stripped", "4 embedding", F.emb_cos)
add("MiniLM on diff", "4 embedding", F.cos_diff)
for tag, nm in [("bge_raw", "BGE-small raw text"), ("bge_stripped", "BGE-small template-stripped"), ("bge_diff", "BGE-small on diff"), ("bgebase_stripped", "BGE-base template-stripped"), ("unix_diff", "UniXcoder (code model) on diff"), ("unix_stripped", "UniXcoder template-stripped text"), ("codebert_diff", "CodeBERT (mean-pooled) on diff"), ("jinacode_diff", "Jina code embeddings v2 on diff")]:
    if "cos_" + tag in F: add(nm, "4 embedding", F["cos_" + tag])
add("contrib-guard/phoenix (bot, exact port)", "5 existing bot", F.cg_phoenix)
add("Simili-bot (bot, re-impl)", "5 existing bot", F.cos_simili)
add("PRSense (bot, re-impl)", "5 existing bot", 0.45 * F.cos_raw + 0.35 * F.cos_diff + 0.20 * F.file_jacc)
g = F.groupby("qi")
def rr(col): return 1.0 / (60 + g[col].rank(ascending=False, method="average"))
txt_emb = "BGE-small raw text" if "BGE-small raw text" in S else "MiniLM raw text"
add("RRF hybrid: BM25 + embedding", "6 unsupervised hybrid", rr("BM25 raw text") + rr(txt_emb))
add("RRF hybrid: BM25 + embedding + code", "6 unsupervised hybrid", rr("BM25 raw text") + rr(txt_emb) + rr("Code overlap sum (files+hunks+lines)"))
add("RRF hybrid: text + code + links + recency", "6 unsupervised hybrid", rr("BM25 raw text") + rr(txt_emb) + rr("Code overlap sum (files+hunks+lines)") + rr("Links only (same issue / #ref)") + rr("Recency only (newest open PR first)"))

LEX = ["text_tfidf", "title_tfidf", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue", "mention_ref",
       "same_author", "same_agent", "log_gap_hours", "cand_open"]
INTRUDE = ["title_tfidf_raw", "text_tfidf_raw", "file_jacc", "file_contain", "hunk_overlap", "line_contain", "same_issue_text", "mention_ref"]
ALL = LEX + ["emb_cos", "cos_raw", "cos_diff", "bm25_raw", "bm25_stripped", "bm25_diff", "text_tfidf_raw", "title_tfidf_raw"] + ["cos_" + t for t in EMBS]
for c in ["bm25_raw", "bm25_stripped", "bm25_diff"]:
    F[c + "_n"] = F[c] / (g[c].transform("max") + 1e-9)  # per-queue normalised BM25 for learners
ALL = [c + "_n" if c.startswith("bm25") else c for c in ALL]
TRAINED = {"INTRUDE + time (Wang et al. 2019), LR": ("7 supervised", INTRUDE + ["log_gap_hours"], "lr"),
           "Jinx lexical, LR": ("7 supervised", LEX, "lr"),
           "Jinx + MiniLM, LR (current tool)": ("7 supervised", LEX + ["emb_cos"], "lr"),
           "All signals, LR": ("7 supervised", ALL, "lr"),
           "Jinx features, gradient boosting": ("7 supervised", LEX + ["emb_cos"], "gb"),
           "All signals, gradient boosting": ("7 supervised", ALL, "gb")}
folds = list(GroupKFold(n_splits=5).split(meta.index, groups=meta.repo))
GBIMP = {}
for name, (fam, cols, kind) in TRAINED.items():
    F[name] = np.nan; S[name] = fam
    for tr, te in folds:
        m = F.qi.isin(set(meta.index[tr])) & ~F.other_gold; T = F[m]
        X = pd.concat([T[T.y == 1], T[T.y == 0].groupby("qi", group_keys=False).apply(lambda d: d.sample(min(len(d), 100), random_state=0))])
        tem = F.qi.isin(set(meta.index[te]))
        if kind == "lr":
            sc = StandardScaler().fit(X[cols]); mdl = LogisticRegression(C=1.0, class_weight="balanced", max_iter=3000).fit(sc.transform(X[cols]), X.y)
            F.loc[tem, name] = mdl.predict_proba(sc.transform(F.loc[tem, cols]))[:, 1]
        else:
            mdl = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, class_weight="balanced", random_state=0).fit(X[cols], X.y)
            F.loc[tem, name] = mdl.predict_proba(F.loc[tem, cols])[:, 1]
BASE = "Jinx + MiniLM, LR (current tool)"
# top-10 of the current tool for re-rankers
F["_r"] = F.groupby("qi")[BASE].rank(ascending=False, method="first")
F.loc[F._r <= 10, ["qi", "cand", BASE, "_r"]].rename(columns={BASE: "base", "_r": "rank"}).to_parquet(D + "top10.parquet")
xq_all = meta.index[(~meta.neg) & (meta.self == False)]
COVER = {}
def rerank(name, file, col, k, combine=False, scope=None, sig=False, fam="8 re-ranker on top-k"):
    if not os.path.exists(D + file): return
    R_ = pd.read_parquet(D + file)[["qi", "cand", col]]
    if scope is not None: R_ = R_[R_.qi.isin(scope)]
    x = F[["qi", "cand", BASE, "_r"]].merge(R_, on=["qi", "cand"], how="left")
    covered = x.qi.isin(set(R_.qi))
    s = x[col].values.astype(float)
    if sig: s = 1 / (1 + np.exp(-s))
    if combine: s = 0.5 * s + 0.5 * x[BASE].values
    inband = covered & (x._r <= k)
    COVER[name] = float((inband & ~np.isnan(s)).sum() / max(inband.sum(), 1))
    val = np.where(inband, 10 + np.where(np.isnan(s), x[BASE].values, s), x[BASE].values)
    add(name, fam, val)
negset = set(meta.index[meta.neg])
rerank("Cross-encoder ms-marco MiniLM (CPU) re-rank top-10", "ce_scores.parquet", "ce", 10, sig=True)
for tag, nm in [("ce_msmarco", "ms-marco MiniLM"), ("ce_bgebase", "BGE-reranker-base"), ("ce_bgem3", "BGE-reranker-v2-m3")]:
    rerank(f"Cross-encoder {nm} re-rank top-10", f"rr_{tag}.parquet", tag, 10, sig=True)
    rerank(f"Cross-encoder {nm} + Jinx (avg) top-10", f"rr_{tag}.parquet", tag, 10, combine=True, sig=True)
import glob
ftf = sorted(glob.glob(D + "rr_ft_fold*.parquet"))
if len(ftf) == 5:
    pd.concat([pd.read_parquet(f) for f in ftf]).to_parquet(D + "rr_ft.parquet")
    rerank("Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10", "rr_ft.parquet", "ft", 10, sig=True, fam="10 stacked cascade (ours)")
LLMS = [("qwen15", "Qwen2.5-1.5B"), ("qwen7", "Qwen2.5-7B"), ("qwencoder7", "Qwen2.5-Coder-7B"), ("qwen14", "Qwen2.5-14B")]
for tag, nm in LLMS:
    for k in [5, 10]:
        rerank(f"LLM judge {nm} re-rank top-{k}", f"llm_{tag}.parquet", "p_yes", k, fam="9 LLM judge on top-k")
        rerank(f"LLM judge {nm} + Jinx (avg) top-{k}", f"llm_{tag}.parquet", "p_yes", k, combine=True, fam="9 LLM judge on top-k")
rerank("LLM judge Claude Haiku 4.5 re-rank top-5", "llm_haiku45.parquet", "p_yes", 5, scope=set(xq_all) | negset, fam="9 LLM judge on top-k")
rerank("LLM judge Claude Haiku 4.5 + Jinx (avg) top-5", "llm_haiku45.parquet", "p_yes", 5, combine=True, scope=set(xq_all) | negset, fam="9 LLM judge on top-k")
# stacked re-ranker: per-fold LR over Jinx score + cross-encoder + LLM judge scores on the top-10 (repo-grouped folds)
def stack(name, files):
    x = F[["qi", "cand", BASE, "_r", "y", "other_gold"]].copy(); cols = [BASE]
    for f, col in files:
        if not os.path.exists(D + f): return
        R_ = pd.read_parquet(D + f)[["qi", "cand", col]].rename(columns={col: f}); x = x.merge(R_, on=["qi", "cand"], how="left"); cols.append(f)
    top = (x._r <= 10) & x[cols].notna().all(1); x["s"] = np.nan
    for tr, te in folds:
        trm = top & x.qi.isin(set(meta.index[tr])) & ~x.other_gold; tem = top & x.qi.isin(set(meta.index[te]))
        sc = StandardScaler().fit(x.loc[trm, cols]); mdl = LogisticRegression(C=1.0, class_weight="balanced", max_iter=3000).fit(sc.transform(x.loc[trm, cols]), x.loc[trm, "y"])
        x.loc[tem, "s"] = mdl.predict_proba(sc.transform(x.loc[tem, cols]))[:, 1]
    COVER[name] = float(top.sum() / max((x._r <= 10).sum(), 1))
    add(name, "10 stacked cascade (ours)", np.where(x.s.notna(), 10 + x.s.fillna(0), np.where(x._r <= 10, 10 + x[BASE], x[BASE])))
stack("Cascade: Jinx + BGE-reranker-base (stacked LR)", [("rr_ce_bgebase.parquet", "ce_bgebase")])
stack("Cascade: Jinx + Qwen2.5-7B judge (stacked LR)", [("llm_qwen7.parquet", "p_yes")])
stack("Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR)", [("llm_qwencoder7.parquet", "p_yes")])
stack("Cascade: Jinx + Qwen2.5-14B judge (stacked LR)", [("llm_qwen14.parquet", "p_yes")])
stack("Cascade: Jinx + fine-tuned BGE-reranker (stacked LR)", [("rr_ft.parquet", "ft")])
stack("Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR)", [("rr_ft.parquet", "ft"), ("llm_qwen7.parquet", "p_yes")])
stack("Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR)", [("rr_ce_bgebase.parquet", "ce_bgebase"), ("llm_qwen7.parquet", "p_yes")])
METHODS = list(S)
def ranks(col):
    s = F[~F.other_gold][["qi", "gold", col, "tie"]].copy(); s["v"] = s[col] + s.tie
    gv = s[s.gold].set_index("qi").v; s = s.join(gv.rename("gv"), on="qi"); s = s[s.gv.notna()]
    return (s.v > s.gv).groupby(s.qi).sum() + 1
R = {c: ranks(c) for c in METHODS}
pd.DataFrame(R).to_parquet(OUT + "ranks.parquet")
def boot(vals, repos, nb=NB, seed=1):
    """Repository-cluster bootstrap: resample repos with replacement (multinomial weights), 95% percentile CI of the mean."""
    rs = np.random.default_rng(seed); codes, u = pd.factorize(repos.values); vals = np.asarray(vals, float)
    sums = np.zeros((len(u), vals.shape[1])); np.add.at(sums, codes, vals); cnt = np.bincount(codes, minlength=len(u)).astype(float)
    W = rs.multinomial(len(u), np.full(len(u), 1.0 / len(u)), size=nb).astype(float)
    out = (W @ sums) / (W @ cnt)[:, None]
    return np.percentile(out, [2.5, 97.5], axis=0)
lab = ~meta.neg
GROUPS = {"all labelled": lab, "self-replacement": lab & (meta.self == True), "cross-author": lab & (meta.self == False),
          "cross-author, same agent": lab & (meta.self == False) & (meta.same_agent == True),
          "cross-author, cross-agent": lab & (meta.self == False) & (meta.same_agent == False),
          "cross-author, no #ref in text": lab & (meta.self == False) & ~meta.ref,
          "cross-author, shares linked issue": lab & (meta.self == False) & meta.issue,
          "cross-author, no link at all (no #ref, no shared issue)": lab & (meta.self == False) & ~meta.ref & ~meta.issue}
meta["txt"] = gm.text_tfidf_raw.reindex(meta.index)
GROUPS["same issue, different code (classes C/D, shares linked issue)"] = lab & meta.issue & meta.cls.isin(["C. same files, different code", "D. no shared files (intent-level)"])
GROUPS["same code, different description (code twin, text TF-IDF < 0.3)"] = lab & (meta.cls == "A. code twin (>=50% identical changed lines)") & (meta.txt < 0.3)
GROUPS["cross-author, same code, different description"] = GROUPS["same code, different description (code twin, text TF-IDF < 0.3)"] & (meta.self == False)
for c in sorted(meta.cls.dropna().unique()):
    GROUPS["class " + c] = lab & (meta.cls == c)
    GROUPS["cross-author, class " + c] = lab & (meta.self == False) & (meta.cls == c)
rows = []
for gname, msk in GROUPS.items():
    qs = meta.index[msk]
    if len(qs) == 0: continue
    for c in METHODS:
        if "Claude" in c and (meta.self.reindex(qs) == True).any(): continue  # Claude was only run on cross-author + negative queries
        r = R[c].reindex(qs).values; v = np.stack([r <= 1, r <= 5, 1 / r], 1).astype(float)
        lo, hi = boot(v, meta.repo.reindex(qs))
        rows.append({"group": gname, "n": len(qs), "family": S[c], "method": c, "R@1": v[:, 0].mean(), "R@1 lo": lo[0], "R@1 hi": hi[0],
                     "R@5": v[:, 1].mean(), "R@5 lo": lo[1], "R@5 hi": hi[1], "MRR": v[:, 2].mean(), "MRR lo": lo[2], "MRR hi": hi[2]})
res = pd.DataFrame(rows); res.to_csv(OUT + "strategies_by_group.csv", index=False)
cls_counts = meta[lab].groupby(["cls", "self"]).size().unstack().rename(columns={True: "self-replacement", False: "cross-author"})
cls_counts.to_csv(OUT + "class_counts.csv")
# paired vs current tool and vs Wang on cross-author
xq = meta.index[GROUPS["cross-author"]]; pr_rows = []
for ref in [BASE, "INTRUDE + time (Wang et al. 2019), LR", "contrib-guard/phoenix (bot, exact port)"]:
    for c in METHODS:
        if c == ref: continue
        a, b = R[c].reindex(xq).values, R[ref].reindex(xq).values
        d = np.stack([(a <= 1).astype(float) - (b <= 1), (a <= 5).astype(float) - (b <= 5), 1 / a - 1 / b], 1)
        lo, hi = boot(d, meta.repo.reindex(xq), nb=max(NB, 1000), seed=5)
        pr_rows.append({"reference": ref, "method": c, "dR@1": d[:, 0].mean(), "dR@1 lo": lo[0], "dR@1 hi": hi[0], "dR@5": d[:, 1].mean(),
                        "dR@5 lo": lo[1], "dR@5 hi": hi[1], "dMRR": d[:, 2].mean(), "dMRR lo": lo[2], "dMRR hi": hi[2]})
pd.DataFrame(pr_rows).to_csv(OUT + "paired_cross_author.csv", index=False)
# false alarms (threshold per fold at 50% of training cross-author top-1 scores) + operating curve on negatives
negq = meta.index[meta.neg]; fa = []; curve = []; FARR = {}
ALERT_METHODS = {BASE, "INTRUDE + time (Wang et al. 2019), LR", "contrib-guard/phoenix (bot, exact port)"}; alerts = []
for c in METHODS:
    t1 = F.groupby("qi")[c].max(); far, hit, fq = [], [], []
    for tr, te in folds:
        trx = [q for q in meta.index[tr] if q in set(xq)]; thr = np.quantile(t1.reindex(trx).values, 0.5)
        ten = [q for q in meta.index[te] if meta.neg[q]]; tex = [q for q in meta.index[te] if q in set(xq)]
        far += list(t1.reindex(ten).values >= thr); hit += list((t1.reindex(tex).values >= thr) & (R[c].reindex(tex).values == 1)); fq += ten
        if c in ALERT_METHODS:
            alerts += [{"method": c, "qi": q, "top1": t1.get(q, np.nan), "thr": thr, "rank": R[c].get(q, np.nan)} for q in meta.index[te]]
    FARR[c] = np.array(far, float)
    lo, hi = boot(FARR[c][:, None], meta.repo.reindex(fq))
    fa.append({"family": S[c], "method": c, "FAR": np.mean(far), "FAR lo": lo[0], "FAR hi": hi[0], "cross-author correct alerts": np.mean(hit)})
    for target in [0.01, 0.02, 0.05, 0.10, 0.20]:
        det, fal, dq, nq = [], [], [], []
        for tr, te in folds:
            nv = np.sort(t1.reindex([q for q in meta.index[tr] if meta.neg[q]]).values); thr = nv[min(int((1 - target) * len(nv)), len(nv) - 1)]
            tex = [q for q in meta.index[te] if q in set(xq)]; ten = [q for q in meta.index[te] if meta.neg[q]]
            det += list((t1.reindex(tex).values > thr) & (R[c].reindex(tex).values == 1)); dq += tex
            fal += list(t1.reindex(ten).values > thr); nq += ten
        det = np.array(det, float); lo, hi = boot(det[:, None], meta.repo.reindex(dq))
        curve.append({"method": c, "FAR target": target, "cross-author detected (top-1 correct, above thr)": det.mean(),
                      "detected lo": lo[0], "detected hi": hi[0], "realised FAR": float(np.mean(fal))})
fpd = []
for ref in [BASE, "INTRUDE + time (Wang et al. 2019), LR", "contrib-guard/phoenix (bot, exact port)"]:
    for c in METHODS:
        if c == ref: continue
        d = (FARR[c] - FARR[ref])[:, None]; lo, hi = boot(d, meta.repo.reindex(fq), nb=max(NB, 1000), seed=7)
        fpd.append({"reference": ref, "method": c, "dFAR": d.mean(), "dFAR lo": lo[0], "dFAR hi": hi[0]})
pd.DataFrame(fpd).to_csv(OUT + "paired_false_alarms.csv", index=False)
pd.DataFrame(alerts).to_parquet(OUT + "alerts.parquet")
pd.DataFrame(fa).to_csv(OUT + "false_alarms.csv", index=False); pd.DataFrame(curve).to_csv(OUT + "operating_curve.csv", index=False)
# random-pair (classic) evaluation vs live-queue: AUC of gold vs one random non-gold candidate from the same queue
rp = F[~F.other_gold & F.qi.isin(xq)]  # cross-author queries, same set as the live-queue column used for tau
negs = rp[~rp.gold].groupby("qi", group_keys=False).apply(lambda d: d.sample(1, random_state=0)); pos = rp[rp.gold]
rpair = []
for c in METHODS:
    y = np.r_[np.ones(len(pos)), np.zeros(len(negs))]; s = np.r_[pos[c].values, negs[c].values]
    rpair.append({"method": c, "random-pair AUC": roc_auc_score(y, s),
                  "live-queue R@1 (cross-author)": float((R[c].reindex(xq) <= 1).mean())})
rpair = pd.DataFrame(rpair); rpair.to_csv(OUT + "random_pair_vs_live_queue.csv", index=False)
tau = kendalltau(rpair["random-pair AUC"], rpair["live-queue R@1 (cross-author)"])
# error analysis for the current tool on cross-author
er = []
for q in xq:
    if R[BASE][q] > 1:
        x = Q[q]; s = F[(F.qi == q) & ~F.other_gold].sort_values(BASE, ascending=False).iloc[0]; t = int(s.cand)
        er.append({"qi": q, "rank of true duplicate": int(R[BASE][q]), "class": meta.cls[q], "queue size": meta.n[q],
                   "top-1 same author as new PR": bool(P.user[t] == P.user[x["q"]]), "new PR": f"#{P.number[x['q']]} {P.title[x['q']]}"[:90],
                   "true duplicate": f"#{P.number[x['gold']]} {P.title[x['gold']]}"[:90], "ranked first instead": f"#{P.number[t]} {P.title[t]}"[:90]})
pd.DataFrame(er).to_csv(OUT + "errors_cross_author.csv", index=False)
lat = {"lexical features ms/query": {"median": float(F.groupby("qi").t_lex.sum().median() * 1000), "p90": float(F.groupby("qi").t_lex.sum().quantile(0.9) * 1000)}}
for f in ["ce_timing.json"]:
    if os.path.exists(D + f): lat["cross-encoder"] = json.load(open(D + f))
for f in sorted(os.listdir(D)):
    if f.startswith("modal_info_") and f.endswith(".json"): lat[f[11:-5]] = json.load(open(D + f))
if os.path.exists(D + "llm_haiku45.parquet"):
    L = pd.read_parquet(D + "llm_haiku45.parquet"); lat["claude haiku45 API"] = {"pairs": len(L), "ms/pair median": float(L.ms.median()), "ms/pair p90": float(L.ms.quantile(.9))}
    if os.path.exists(D + "llm_haiku45_cost.json"): lat["claude haiku45 API"].update(json.load(open(D + "llm_haiku45_cost.json")))
json.dump({"latency": lat, "kendall_tau random-pair AUC vs live-queue cross-author R@1": [tau.statistic, tau.pvalue],
           "classes": {str(k): v for k, v in meta[lab].cls.value_counts().items()}, "n_methods": len(METHODS),
           "gb_features": ALL, "n_bootstrap": NB, "judge_coverage": COVER,
           "cap_dropped": {"all": len(CAP_DROPPED), "cross-author": sum(1 for q in CAP_DROPPED if not Q[q]["self"])}}, open(OUT + "summary.json", "w"), indent=1, default=float)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
for gname in ["cross-author", "all labelled"]:
    print("\n==", gname); print(res[res.group == gname].sort_values("R@1", ascending=False)[["family", "method", "R@1", "R@5", "MRR"]].round(3).to_string(index=False))
print(cls_counts); print(pd.DataFrame(fa).sort_values("FAR").round(3).to_string(index=False)); print("tau", tau)
