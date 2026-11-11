"""Export compact PR texts for GPU jobs on Modal: embedding inputs (raw/stripped/diff) and pair-judge views."""
import pickle, sys, pandas as pd
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/jinx_pr/src")
from jinx_pr.templates import TemplateModel
import pairtext
from pairtext import pr_text, D
need = sorted(pickle.load(open(D + "bench.pkl", "rb"))["need"])
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "title", "body", "agent"]).set_index("id").loc[need]
pr["body"] = pr.body.fillna(""); pr["title"] = pr.title.fillna("")
tm = TemplateModel.default()
diff = pickle.load(open(D + "difftext.pkl", "rb")); diff = {k: "".join(v) if isinstance(v, list) else v for k, v in diff.items()}
E = pd.DataFrame({"id": need,
                  "raw": [f"{t}\n{b}"[:4000] for t, b in zip(pr.title, pr.body)],
                  "stripped": [f"{t}\n{tm.strip(b, a)}"[:4000] for t, b, a in zip(pr.title, pr.body, pr.agent)],
                  "diff": [(diff.get(i, "") or t)[:4000] for i, t in zip(need, pr.title)]})
E.to_parquet(D + "modal_embed_texts.parquet"); print("embed texts", E.shape, flush=True)
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
T = pd.read_parquet(D + "top10.parquet")
ids = sorted(set(int(Q[q]["q"]) for q in T.qi.unique()) | set(int(c) for c in T.cand))
P = pd.DataFrame({"id": ids, "view": [pr_text(i) for i in ids]})
P.to_parquet(D + "modal_pair_views.parquet")
pairs = T.copy(); pairs["q"] = [int(Q[q]["q"]) for q in pairs.qi]
pairs["self"] = [bool(Q[q]["self"]) for q in pairs.qi]; pairs["neg"] = [bool(Q[q]["neg"]) for q in pairs.qi]
pairs.to_parquet(D + "modal_pairs.parquet"); print("pair views", P.shape, "pairs", pairs.shape, flush=True)
