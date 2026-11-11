"""Export the LiveQueue benchmark as release files (Parquet + manifest) for Zenodo / Hugging Face.

python experiments/bench_v2/export_release.py [out_dir]   (default: ../release/livequeue_v1 next to the repo)
"""
import hashlib
import json
import os
import pickle
import sys

import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, "..", "..", "..", "release", "livequeue_v1")
os.makedirs(OUT, exist_ok=True)
with open(D + "bench.pkl", "rb") as fh:
    B = pickle.load(fh)
Q = B["queries"]
need = sorted(B["need"])
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "state", "created_at",
                                                          "closed_at", "merged_at", "repo_url", "html_url"]).set_index("id").loc[need]
with open(D + "diffs.pkl", "rb") as fh:
    DF = pickle.load(fh)
ri = pd.read_parquet(D + "related_issue.parquet")
links = ri[ri.source == "body"].groupby("pr_id").issue_id.apply(sorted).to_dict()

queries = pd.DataFrame([{
    "qi": i, "repo": P.repo_url[x["q"]].replace("https://api.github.com/repos/", ""), "query_id": int(x["q"]),
    "query_number": int(P.number[x["q"]]), "has_duplicate": not x["neg"],
    "gold_id": None if x["neg"] else int(x["gold"]), "gold_number": None if x["neg"] else int(P.number[x["gold"]]),
    "other_gold_ids": sorted(int(o) for o in x["others"]), "label_phrase": x["phrase"],
    "relation": None if x["neg"] else ("self-replacement" if x["self"] else ("cross-author, same agent" if x["same_agent"] else "cross-author, cross-agent")),
    "queue_ids": [int(c) for c in x["cand"]], "queue_size": len(x["cand"])} for i, x in enumerate(Q)])
prs = P.reset_index().rename(columns={"user": "author"})
prs["repo_url"] = prs.repo_url.str.replace("https://api.github.com/repos/", "", regex=False)
prs["files"] = [sorted(DF["files"].get(i, ())) for i in prs.id]
prs["hunks"] = [[{"path": h[0], "start": int(h[1]), "end": int(h[2])} for h in sorted(DF["hunks"].get(i, ()))] for i in prs.id]
prs["added_line_hashes"] = [sorted(int(a) for a in DF["added"].get(i, ())) for i in prs.id]
prs["linked_issue_ids"] = [links.get(i, []) for i in prs.id]
for c in ["created_at", "closed_at", "merged_at"]:
    prs[c] = pd.to_datetime(prs[c], utc=True)
F = pd.read_parquet(D + "features.parquet")
keep = ["qi", "cand", "gold", "other_gold", "text_tfidf", "title_tfidf", "emb_cos", "file_jacc", "file_contain", "hunk_overlap",
        "line_contain", "same_issue", "mention_ref", "same_author", "same_agent", "log_gap_hours", "cand_open", "text_tfidf_raw",
        "title_tfidf_raw", "same_issue_text", "cos_raw", "cos_diff"]
queries.to_parquet(os.path.join(OUT, "queries.parquet"), index=False)
prs.to_parquet(os.path.join(OUT, "prs.parquet"), index=False)
F[keep].to_parquet(os.path.join(OUT, "pair_features.parquet"), index=False)
man = {}
for f in sorted(os.listdir(OUT)):
    if f.endswith(".parquet"):
        with open(os.path.join(OUT, f), "rb") as fh:
            man[f] = {"sha256": hashlib.sha256(fh.read()).hexdigest(), "bytes": os.path.getsize(os.path.join(OUT, f))}
man["counts"] = {"queries": len(queries), "with_duplicate": int(queries.has_duplicate.sum()),
                 "no_duplicate": int((~queries.has_duplicate).sum()), "prs": len(prs), "pairs": len(F),
                 "repos": int(queries.repo.nunique())}
with open(os.path.join(OUT, "MANIFEST.json"), "w") as fh:
    json.dump(man, fh, indent=1)
print(json.dumps(man, indent=1))
