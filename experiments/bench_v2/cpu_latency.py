"""CPU latency (4 threads) of the re-rankers on 200 sampled top-10 pairs; per-pair ms and per-query (10 pairs) ms."""
import json, time, numpy as np, pandas as pd, torch
from sentence_transformers import CrossEncoder
torch.set_num_threads(4)
D = "/home/ubuntu/research/prdupecheck/data/"
T = pd.read_parquet(D + "modal_pairs.parquet").sample(200, random_state=0); _v = pd.read_parquet(D + "modal_pair_views.parquet")
P = dict(zip(_v.id.tolist(), _v["view"].tolist())); pairs = [(P[q], P[c]) for q, c in zip(T.q.tolist(), T.cand.tolist())]
out = {}
for m in ["cross-encoder/ms-marco-MiniLM-L6-v2", "BAAI/bge-reranker-base"]:
    ce = CrossEncoder(m, device="cpu", max_length=512); ce.predict(pairs[:10], batch_size=10)
    t0 = time.perf_counter(); ce.predict(pairs, batch_size=10, show_progress_bar=False); el = time.perf_counter() - t0
    out[m] = {"cpu_threads": 4, "pairs": len(pairs), "ms_per_pair": round(1000 * el / len(pairs), 1), "ms_per_query_top10": round(10000 * el / len(pairs), 1)}
    print(m, out[m], flush=True)
json.dump(out, open(D + "modal_info_cpu_rerankers.json", "w"), indent=1)
