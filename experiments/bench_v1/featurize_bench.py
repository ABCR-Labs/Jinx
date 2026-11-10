"""Compute per-(query, candidate) features for AgentDup and every baseline on the live-queue benchmark."""
import pickle, numpy as np, pandas as pd, sys, math, collections, time
from multiprocessing import Pool
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/agentdup/src")
from agentdup import PR, Detector
from agentdup.pr import CLOSING
from agentdup.text import tokens
from agentdup.scorer import FEATURES
sys.path.insert(0, '/home/ubuntu/research/prdupecheck/bench')
from ported import phoenix_scores, balyakin_scores
D = "/home/ubuntu/research/prdupecheck/data/"
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]; need = sorted(B["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "created_at", "closed_at", "repo_url"]).set_index("id").loc[need]
diffs = pickle.load(open(D + "diffs.pkl", "rb"))
ri = pd.read_parquet(D + "related_issue.parquet"); ri = ri[ri.source == "body"]
links = ri.groupby("pr_id").issue_id.apply(set).to_dict()
E = np.load(D + "emb.npz"); EIDX = {int(i): k for k, i in enumerate(E["ids"])}
EMB = {k: E[k].astype(np.float32) for k in E.files if k != "ids"}
VT = np.load(D + "emb_vt.npz")["vt"].astype(np.float32) if len(sys.argv) > 1 else None
VTTXT = pickle.load(open(D + "vt_text.pkl", "rb")) if len(sys.argv) > 1 else {}

def ts(v):
    return None if pd.isna(v) else pd.Timestamp(v).to_pydatetime()

OBJ, TXT_ISSUES = {}, {}
for i, r in zip(pr.index, pr.itertuples()):
    OBJ[i] = PR(number=int(r.number), title=r.title or "", body=r.body or "", author=r.user or "", agent=r.agent or "",
                created_at=ts(r.created_at), closed_at=ts(r.closed_at), files=diffs["files"].get(i, ()),
                hunks=diffs["hunks"].get(i, ()), added=diffs["added"].get(i, ()), linked_issues=links.get(i, set()))
    TXT_ISSUES[i] = {int(x) for x in CLOSING.findall(r.body or "")}
W0 = {"features": FEATURES, "coef": [0.0] * len(FEATURES), "intercept": 0.0, "mean": [0.0] * len(FEATURES), "scale": [1.0] * len(FEATURES)}
DET = Detector(weights=W0)
RAW = Detector(weights=W0, strip_templates=False)

def bm25(qt, docs, k1=1.2, b=0.75):
    n = len(docs); avg = sum(map(len, docs)) / max(n, 1) or 1.0
    df = collections.Counter(t for d in docs for t in set(d)); qs = set(qt); out = []
    for d in docs:
        tf = collections.Counter(d); s = 0.0
        for t in qs:
            if tf[t]:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg))
        out.append(s)
    return out

def one(qi):
    x = Q[qi]; q = x["q"]; cand = [int(c) for c in x["cand"]]
    new, queue = OBJ[q], [OBJ[c] for c in cand]
    t0 = time.perf_counter(); rows = DET.featurize(new, queue); t_lex = time.perf_counter() - t0
    raw = RAW.featurize(new, queue)
    qe = EIDX[q]; ce = [EIDX[c] for c in cand]
    cos = collections.defaultdict(lambda: np.zeros(len(cand)), {k: EMB[k][ce] @ EMB[k][qe] for k in EMB})
    out = []
    vt_bm = None
    ph = phoenix_scores(f"{new.title} {new.body}", [f"{o.title} {o.body}" for o in queue])
    ba = balyakin_scores(new.title, new.files, [(o.title, o.files) for o in queue])
    if VT is not None:
        vt_vec = VT[ce] @ VT[qe]
        vt_bm = bm25(tokens(VTTXT[q]), [tokens(VTTXT[c]) for c in cand])
    for j, c in enumerate(cand):
        f = rows[j]; f["emb_cos"] = float(cos["stripped"][j])
        d = {"qi": qi, "cand": c, "gold": c == x["gold"], "other_gold": c in x["others"],
             **f, "text_tfidf_raw": raw[j]["text_tfidf"], "title_tfidf_raw": raw[j]["title_tfidf"],
             "same_issue_text": float(bool(TXT_ISSUES[q] & TXT_ISSUES[c])),
             "cos_raw": float(cos["raw"][j]), "cos_prism": float(cos["prism"][j]), "cos_simili": float(cos["simili"][j]),
             "cos_diff": float(cos["diff"][j]), "cg_phoenix": ph[j], "cg_balyakin": ba[j][0], "cg_balyakin_files": ba[j][1], "t_lex": t_lex / len(cand)}
        if VT is not None:
            d["vt_vec"] = float(vt_vec[j]); d["vt_bm25"] = vt_bm[j]
        out.append(d)
    return out

if __name__ == "__main__":
    t0 = time.time()
    import os
    lim = int(os.environ.get("LIMIT", len(Q))); procs = int(os.environ.get("PROCS", 6))
    with Pool(procs) as p:
        res = p.map(one, range(lim), chunksize=8)
    df = pd.DataFrame([r for rs in res for r in rs])
    print("rows", len(df), "queries", df.qi.nunique(), "s", round(time.time() - t0))
    df.to_parquet(D + os.environ.get("OUTF", "features.parquet"))
