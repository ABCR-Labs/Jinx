"""Embed benchmark PR texts with a local sentence-transformers model. usage: embed_model.py MODEL VARIANT TAG [maxlen]"""
import pickle, sys, time, numpy as np, pandas as pd, torch
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/jinx_pr/src")
from sentence_transformers import SentenceTransformer
from jinx_pr.templates import TemplateModel
torch.set_num_threads(4)
D = "/home/ubuntu/research/prdupecheck/data/"
model, variant, tag = sys.argv[1:4]; maxlen = int(sys.argv[4]) if len(sys.argv) > 4 else 256
need = sorted(pickle.load(open(D + "bench.pkl", "rb"))["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body", "agent"]).set_index("id").loc[need]
pr["body"] = pr.body.fillna(""); pr["title"] = pr.title.fillna("")
if variant == "raw":
    texts = [f"{t}\n{b}" for t, b in zip(pr.title, pr.body)]
elif variant == "stripped":
    tm = TemplateModel.default(); texts = [f"{t}\n{tm.strip(b, a)}" for t, b, a in zip(pr.title, pr.body, pr.agent)]
elif variant == "diff":
    diff = pickle.load(open(D + "difftext.pkl", "rb")); diff = {k: "".join(v) if isinstance(v, list) else v for k, v in diff.items()}
    texts = [diff.get(i, "") or t for i, t in zip(need, pr.title)]
m = SentenceTransformer(model, device="cpu", trust_remote_code=True); m.max_seq_length = maxlen
t0 = time.time()
E = m.encode([x[:4000] for x in texts], batch_size=64, normalize_embeddings=True, show_progress_bar=False).astype(np.float16)
el = time.time() - t0
np.savez(D + f"emb_{tag}.npz", ids=np.array(need), emb=E)
print(tag, model, variant, E.shape, round(el), "s", round(1000 * el / len(texts), 2), "ms/PR", flush=True)
