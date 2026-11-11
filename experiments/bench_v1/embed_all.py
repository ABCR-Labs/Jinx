# Local MiniLM embeddings (CPU) for every PR in the benchmark, in the text formats each tool uses.
import pickle, numpy as np, pandas as pd, time, sys
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/jinx_pr/src")
from sentence_transformers import SentenceTransformer
from jinx_pr.templates import TemplateModel
D = "/home/ubuntu/research/prdupecheck/data/"
need = sorted(pickle.load(open(D + "bench.pkl", "rb"))["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body", "agent"]).set_index("id").loc[need]
pr["body"] = pr.body.fillna(""); pr["title"] = pr.title.fillna("")
diff = pickle.load(open(D + "difftext.pkl", "rb"))
files = pickle.load(open(D + "diffs.pkl", "rb"))["files"] if len(sys.argv) > 1 else {}
tm = TemplateModel.default()
variants = {
    "raw": [f"{t}\n{b}" for t, b in zip(pr.title, pr.body)],                      # plain / PRSense text
    "prism": [f"{t}\n\n{b}" for t, b in zip(pr.title, pr.body)],
    "simili": [f"Title: {t}\n\n" + (f"Body: {b.strip()}\n\n" if b.strip() else "") for t, b in zip(pr.title, pr.body)],
    "stripped": [f"{t}\n{tm.strip(b, a)}" for t, b, a in zip(pr.title, pr.body, pr.agent)],
    "diff": [diff.get(i, "") for i in need],
}
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
out = {"ids": np.array(need)}
for k, texts in variants.items():
    t0 = time.time()
    out[k] = m.encode([x[:3000] for x in texts], batch_size=128, normalize_embeddings=True, show_progress_bar=False).astype(np.float16)
    print(k, out[k].shape, round(time.time() - t0), "s", flush=True)
    np.savez(D + "emb.npz", **out)
print("done")
