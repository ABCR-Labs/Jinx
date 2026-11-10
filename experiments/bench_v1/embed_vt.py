# vector-triage's embedding text (ingest/pr.go BuildPRContent, MaxDiffChars=4000), embedded with the local MiniLM.
import pickle, numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer
D = "/home/ubuntu/research/prdupecheck/data/"
need = sorted(pickle.load(open(D + "bench.pkl", "rb"))["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body"]).set_index("id").loc[need]
files = pickle.load(open(D + "diffs.pkl", "rb"))["files"]; diff = pickle.load(open(D + "difftext.pkl", "rb"))
def content(i, t, b):
    t, b = (t or "").strip(), (b or "").strip()
    if not t and not b: return ""
    if not t: return b
    if not b: return "PR: " + t
    parts = ["PR: " + t, "Description: " + b]
    fs = sorted(files.get(i, ()))
    if fs: parts.append("Files changed: " + ", ".join(fs))
    if diff.get(i): parts.append("Diff summary: " + diff[i][:4000])
    return "\n\n".join(parts)
txt = {i: content(i, t, b) for i, t, b in zip(pr.index, pr.title, pr.body)}
pickle.dump(txt, open(D + "vt_text.pkl", "wb"))
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
v = m.encode([txt[i][:3000] for i in need], batch_size=128, normalize_embeddings=True, show_progress_bar=False)
np.savez(D + "emb_vt.npz", ids=np.array(need), vt=v.astype(np.float16)); print("done")
