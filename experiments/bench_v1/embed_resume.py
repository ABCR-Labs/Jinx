# Resume embeddings: keep variants already saved in emb.npz, compute the rest, then the vector-triage text.
import pickle, numpy as np, pandas as pd, time, sys
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/jinx_pr/src")
from sentence_transformers import SentenceTransformer
from jinx_pr.templates import TemplateModel
D = "/home/ubuntu/research/prdupecheck/data/"
need = sorted(pickle.load(open(D + "bench.pkl", "rb"))["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body", "agent"]).set_index("id").loc[need]
pr["body"] = pr.body.fillna(""); pr["title"] = pr.title.fillna("")
diff = pickle.load(open(D + "difftext.pkl", "rb"))
diff = {k: "".join(v) if isinstance(v, list) else v for k, v in diff.items()}
files = pickle.load(open(D + "diffs.pkl", "rb"))["files"]
tm = TemplateModel.default()
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
old = dict(np.load(D + "emb.npz")); assert list(old["ids"]) == need
raw = [f"{t}\n{b}" for t, b in zip(pr.title, pr.body)]
prism = [f"{t}\n\n{b}" for t, b in zip(pr.title, pr.body)]
tok = m.tokenizer
same = sum(tok(a[:3000])["input_ids"][:256] == tok(b[:3000])["input_ids"][:256] for a, b in zip(raw[:2000], prism[:2000]))
print("prism tokens identical to raw on", same, "/ 2000", flush=True)
vt = []
for i, t, b in zip(need, pr.title, pr.body):
    parts = ["PR: " + t, "Description: " + b]
    fs = sorted(files.get(i, ()))
    if fs: parts.append("Files changed: " + ", ".join(fs))
    if diff.get(i): parts.append("Diff summary: " + diff[i][:4000])
    vt.append("\n\n".join(parts))
pickle.dump(dict(zip(need, vt)), open(D + "vt_text.pkl", "wb"))
variants = {
    "prism": prism,
    "simili": [f"Title: {t}\n\n" + (f"Body: {b.strip()}\n\n" if b.strip() else "") for t, b in zip(pr.title, pr.body)],
    "stripped": [f"{t}\n{tm.strip(b, a)}" for t, b, a in zip(pr.title, pr.body, pr.agent)],
    "diff": [diff.get(i, "") for i in need],
    "vt": vt,
}
out = dict(old)
for k, texts in variants.items():
    if k in out: continue
    if k == "prism" and same == 2000:
        out[k] = out["raw"]; print("prism = raw (identical model input)", flush=True); continue
    t0 = time.time()
    out[k] = m.encode([x[:3000] for x in texts], batch_size=64, normalize_embeddings=True, show_progress_bar=False).astype(np.float16)
    print(k, out[k].shape, round(time.time() - t0), "s", flush=True)
    np.savez(D + "emb.npz", **out)
np.savez(D + "emb_vt.npz", vt=out["vt"])
np.savez(D + "emb.npz", **{k: v for k, v in out.items() if k != "vt"})
print("done", flush=True)
