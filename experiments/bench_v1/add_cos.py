"""Add embedding-cosine columns (from emb.npz / emb_vt.npz) and vector-triage BM25 to the lexical feature table."""
import pickle, sys, numpy as np, pandas as pd, collections, math
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/doppel/src")
from doppel.text import tokens
D = "/home/ubuntu/research/prdupecheck/data/"
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
F = pd.read_parquet(D + "features_lex.parquet")
OUTF = sys.argv[1] if len(sys.argv) > 1 else "features.parquet"
E = np.load(D + "emb.npz"); idx = {int(i): k for k, i in enumerate(E["ids"])}
qid = np.array([idx[Q[q]["q"]] for q in F.qi]); cid = np.array([idx[int(c)] for c in F.cand])
def cos(M):
    M = M.astype(np.float32); return np.einsum("ij,ij->i", M[qid], M[cid])
for col, key in [("cos_raw", "raw"), ("cos_prism", "prism"), ("cos_simili", "simili"), ("cos_diff", "diff"), ("emb_cos", "stripped")]:
    F[col] = cos(E[key]) if key in E.files else (cos(E["raw"]) if key == "prism" and "raw" in E.files else np.nan)
try:
    VT = np.load(D + "emb_vt.npz")["vt"]; F["vt_vec"] = cos(VT)
    # vector-triage engine.go: vector top-5 + FTS5 top-5 (title/body columns, porter unicode61, bm25 weights 10/1,
    # query = AND of all non-stopword terms of the PR content), RRF k=60, display = max(vec, |bm25|/(1+|bm25|)).
    import sqlite3, re
    txt = pickle.load(open(D + "vt_text.pkl", "rb"))
    pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body"]).set_index("id")
    STOP = set("a an and are as at be by for from has he in is it its of on or that the to was were will with this these those".split())
    WORD = re.compile(r"\w+")
    def fts_query(t):
        terms = [w for w in WORD.findall(t.lower()) if w not in STOP]
        return " AND ".join('"' + w.replace('"', '""') + '"' for w in terms)
    con = sqlite3.connect(":memory:")
    con.execute("create virtual table f using fts5(title, body, tokenize='porter unicode61')")
    rrf = np.zeros(len(F)); disp = np.zeros(len(F)); ftsn = np.zeros(len(F))
    vec = F.vt_vec.values
    for qi, g in F.groupby("qi").indices.items():
        cands = F.cand.values[g]
        con.execute("delete from f")
        con.executemany("insert into f(rowid, title, body) values (?,?,?)",
                        [(k, pr.title.get(int(c)) or "", pr.body.get(int(c)) or "") for k, c in enumerate(cands)])
        q = fts_query(txt[Q[qi]["q"]])
        hits = con.execute("select rowid, bm25(f, 10.0, 1.0) s from f where f match ? order by s asc limit 5", (q,)).fetchall() if q else []
        order = np.argsort(-vec[g], kind="stable")[:5]
        for r, k in enumerate(order):
            rrf[g[k]] += 1 / (60 + r + 1)
        for r, (k, sc) in enumerate(hits):
            rrf[g[k]] += 1 / (60 + r + 1); ftsn[g[k]] = abs(sc) / (1 + abs(sc))
        disp[g] = np.maximum(vec[g], ftsn[g])
    F["vt_rrf"] = rrf; F["vt_fts"] = ftsn; F["vt_display"] = disp
    print("queries with any FTS hit:", int((F.groupby("qi").vt_fts.max() > 0).sum()), "of", F.qi.nunique())
except FileNotFoundError:
    print("no vector-triage embeddings yet")
F.to_parquet(D + OUTF); print("rows", len(F), "cols", list(F.columns))
