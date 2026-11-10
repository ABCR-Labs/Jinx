"""Extra lexical/code strategy features per (query, candidate): BM25 on raw and template-stripped text, BM25 on diff text."""
import pickle, sys, math, collections, os, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/agentdup/src")
from agentdup.text import tokens
from agentdup.templates import TemplateModel
D = "/home/ubuntu/research/prdupecheck/data/"
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]; need = sorted(B["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body", "agent"]).set_index("id").loc[need]
pr["body"] = pr.body.fillna(""); pr["title"] = pr.title.fillna("")
tm = TemplateModel.default()
diff = pickle.load(open(D + "difftext.pkl", "rb")); diff = {k: "".join(v) if isinstance(v, list) else v for k, v in diff.items()}
RAW = {i: tokens(f"{t} {b}") for i, t, b in zip(pr.index, pr.title, pr.body)}
STR = {i: tokens(f"{t} {tm.strip(b, a)}") for i, t, b, a in zip(pr.index, pr.title, pr.body, pr.agent)}
DIF = {i: tokens((diff.get(i) or "")[:20000]) for i in need}

def bm25(qt, docs, k1=1.2, b=0.75):
    n = len(docs); avg = (sum(map(len, docs)) / max(n, 1)) or 1.0
    df = collections.Counter(t for d in docs for t in set(d)); out = []
    for d in docs:
        tf = collections.Counter(d); s = 0.0
        for t in set(qt):
            if tf[t]:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg))
        out.append(s)
    return out

def one(qi):
    x = Q[qi]; q = x["q"]; c = [int(v) for v in x["cand"]]
    r = bm25(RAW[q], [RAW[v] for v in c]); s = bm25(STR[q], [STR[v] for v in c]); d = bm25(DIF[q], [DIF[v] for v in c])
    return [(qi, v, a, b_, e) for v, a, b_, e in zip(c, r, s, d)]

if __name__ == "__main__":
    with Pool(4) as p: res = p.map(one, range(len(Q)), chunksize=16)
    df = pd.DataFrame([t for rs in res for t in rs], columns=["qi", "cand", "bm25_raw", "bm25_stripped", "bm25_diff"])
    df.to_parquet(D + "feat_bm25.parquet"); print("rows", len(df))
