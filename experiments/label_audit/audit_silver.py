"""Audit silver duplicate labels: Claude Haiku 4.5 reads 200 random labelled pairs and says what the relation really is.

Usage: python audit_silver.py [n_pairs|cross]   (needs ANTHROPIC_API_KEY; about $0.0016 per pair)
  n_pairs: random labelled pairs (seed 0, default 200); cross: all cross-author pairs.
Writes audit_<tag>_pairs.parquet (inputs), audit_<tag>_labels.jsonl (one line per pair), audit_<tag>_summary.json.
"""
import json
import os
import pickle
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import anthropic
import numpy as np
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
D = os.environ.get("JINX_DATA", "/home/ubuntu/research/prdupecheck/data/")
MODEL = "claude-haiku-4-5"
PRICE_IN, PRICE_OUT = 1.0, 5.0  # USD per million tokens
ARG = sys.argv[1] if len(sys.argv) > 1 else "200"
TAG = "cross" if ARG == "cross" else f"random{ARG}"
LABELS = ["duplicate", "replacement", "subsumed", "related", "unclear"]
SYS = """You audit labels in a dataset of duplicate GitHub pull requests (PRs). A maintainer or author left a comment
such as "superseded by #N" or "closing in favor of #N" linking an OLDER PR to a NEWER PR. Decide what the relation
really is, from the NEWER PR's point of view when it was opened (the older PR was still open):
- duplicate: both PRs make essentially the same change or fix the same problem.
- replacement: the newer PR is a revised/redone version of the older PR's work (same goal, new attempt).
- subsumed: the newer PR is larger work that happens to include the older PR's change.
- related: same area but different goals; the newer PR does NOT redo the older PR's work.
- unclear: not enough information.
Answer with JSON only: {"label": "<one of the five>", "reason": "<at most 20 words>"}"""

with open(D + "bench.pkl", "rb") as fh:
    Q = pickle.load(fh)["queries"]
pos = [i for i, x in enumerate(Q) if not x["neg"]]
if ARG == "cross":
    pick = [i for i in pos if not Q[i]["self"]]
else:
    pick = sorted(np.random.default_rng(0).choice(pos, min(int(ARG), len(pos)), replace=False).tolist())
ids = sorted({Q[i]["q"] for i in pick} | {Q[i]["gold"] for i in pick})
P = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "repo_url"]).set_index("id").loc[ids]
with open(D + "diffs.pkl", "rb") as fh:
    FILES = pickle.load(fh)["files"]


def card(i, tag):
    r = P.loc[i]
    files = sorted(FILES.get(i, ()))
    fl = ", ".join(files[:20]) + (f" (+{len(files) - 20} more)" if len(files) > 20 else "")
    return (f"## {tag} PR #{r.number} by {r.user} ({r.agent})\nTitle: {r.title}\nChanged files: {fl or 'unknown'}\n"
            f"Description (truncated):\n{(r.body or '')[:1500]}\n")


rows = []
for i in pick:
    x = Q[i]
    rows.append({"qi": i, "repo": P.repo_url[x["q"]], "new": int(P.number[x["q"]]), "old": int(P.number[x["gold"]]),
                 "self": bool(x["self"]), "same_agent": bool(x["same_agent"]), "phrase": x["phrase"],
                 "prompt": f"Repository: {P.repo_url[x['q']].replace('https://api.github.com/repos/', '')}\n"
                           f"Linking comment on the older PR: \"{x['phrase']}\"\n\n" + card(x["gold"], "OLDER") + "\n" + card(x["q"], "NEWER")})
pd.DataFrame(rows).to_parquet(os.path.join(H, f"audit_{TAG}_pairs.parquet"))
cl = anthropic.Anthropic()


def ask(r):
    for attempt in range(5):
        try:
            t0 = time.perf_counter()
            m = cl.messages.create(model=MODEL, max_tokens=80, system=SYS, messages=[{"role": "user", "content": r["prompt"]}])
            txt = m.content[0].text.strip()
            try:
                out = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
            except ValueError:
                out = {"label": "unclear", "reason": "unparsable: " + txt[:60]}
            if out.get("label") not in LABELS:
                out["label"] = "unclear"
            return {"qi": r["qi"], **out, "in_tok": m.usage.input_tokens, "out_tok": m.usage.output_tokens,
                    "ms": (time.perf_counter() - t0) * 1000}
        except anthropic.APIError:
            time.sleep(2 ** attempt)
    return {"qi": r["qi"], "label": "unclear", "reason": "api error", "in_tok": 0, "out_tok": 0, "ms": 0}


with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(ask, rows))
with open(os.path.join(H, f"audit_{TAG}_labels.jsonl"), "w") as fh:
    fh.writelines(json.dumps(r) + "\n" for r in res)
L = pd.DataFrame(rows)[["qi", "self"]].merge(pd.DataFrame(res), on="qi")
valid_strict = L.label.isin(["duplicate", "replacement"])
valid_loose = L.label.isin(["duplicate", "replacement", "subsumed"])


def ci(v):
    b = [np.random.default_rng(s).choice(v, len(v)).mean() for s in range(2000)]
    return [float(np.mean(v)), float(np.quantile(b, 0.025)), float(np.quantile(b, 0.975))]


cost = L.in_tok.sum() / 1e6 * PRICE_IN + L.out_tok.sum() / 1e6 * PRICE_OUT
S = {"model": MODEL, "n": len(L), "label_counts": L.label.value_counts().to_dict(),
     "precision_strict (duplicate+replacement) [mean, lo, hi]": ci(valid_strict.to_numpy()),
     "precision_loose (+subsumed) [mean, lo, hi]": ci(valid_loose.to_numpy()),
     "by relation": {k: {"n": len(g), "labels": g.label.value_counts().to_dict()}
                     for k, g in L.groupby(L["self"].map({True: "self-replacement", False: "cross-author"}))},
     "cost_usd": round(float(cost), 4), "input_tokens": int(L.in_tok.sum()), "output_tokens": int(L.out_tok.sum())}
with open(os.path.join(H, f"audit_{TAG}_summary.json"), "w") as fh:
    json.dump(S, fh, indent=1)
print(json.dumps(S, indent=1))
