"""Zero-shot cross-encoder (ms-marco MiniLM-L6) re-ranking of Jinx's top-10 for every benchmark query."""
import pickle, time, json, numpy as np, pandas as pd, torch
from sentence_transformers import CrossEncoder
from pairtext import pr_text, D
torch.set_num_threads(4)
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
T = pd.read_parquet(D + "top10.parquet")
ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", device="cpu", max_length=512)
cache = {}
def tx(i):
    if i not in cache: cache[i] = pr_text(int(i))
    return cache[i]
pairs = [(tx(Q[q]["q"]), tx(c)) for q, c in zip(T.qi, T.cand)]
t0 = time.time(); s = ce.predict(pairs, batch_size=32, show_progress_bar=False); el = time.time() - t0
T["ce"] = s; T[["qi", "cand", "ce"]].to_parquet(D + "ce_scores.parquet")
json.dump({"pairs": len(T), "seconds": el, "ms_per_pair": 1000 * el / len(T)}, open(D + "ce_timing.json", "w"))
print("ce done", len(T), round(el), "s", round(1000 * el / len(T), 1), "ms/pair")
