"""Claude Haiku 4.5 judge on open-only queues: Jinx top-5 for every cross-author query and for a random sample of
no-duplicate queries. Reuses earlier verdicts for identical (query, candidate) pairs; hard budget stop.
usage: haiku_open.py N_NEG BUDGET_USD   (DRY=1 only prints the plan)"""
import concurrent.futures as cf
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from claude_prompt import MODEL, PRICE_IN, PRICE_OUT, judge
from pairtext import D, pr_text

n_neg, BUDGET = int(sys.argv[1]), float(sys.argv[2])
Q = pickle.load(open(D + "bench.pkl", "rb"))["queries"]  # noqa: SIM115
T = pd.read_parquet(D + "top10.parquet")
T = T[T["rank"] <= 5].copy()
T["q"] = [int(Q[i]["q"]) for i in T.qi]
neg = np.array([bool(Q[i]["neg"]) for i in T.qi])
cross = np.array([not Q[i]["neg"] and not Q[i]["self"] for i in T.qi])
negq = np.sort(T.qi[neg].unique())
sample = np.sort(np.random.default_rng(7).choice(negq, min(n_neg, len(negq)), replace=False))
sel = T[cross | T.qi.isin(sample)].reset_index(drop=True)
out_f = D + "llm_haiku45_open.parquet"
cols = ["qi", "cand", "p_yes", "verdict", "in_tok", "out_tok", "ms", "new"]
if os.path.exists(out_f):
    done = pd.read_parquet(out_f)
else:
    old = pd.read_parquet(D + "llm_haiku45.parquet").assign(new=False)
    done = old.merge(sel[["qi", "cand"]], on=["qi", "cand"])[cols]
key = set(zip(done.qi, done.cand))
todo = sel[[k not in key for k in zip(sel.qi, sel.cand)]]
cost = 7.2527 / 4587
print(f"pairs {len(sel)} (cross {cross.sum()}, neg queries {len(sample)}/{len(negq)}), reused {len(done)}, "
      f"todo {len(todo)}, est ${len(todo) * cost:.2f}", flush=True)
json_meta = {"model": MODEL, "neg_sample": [int(x) for x in sample], "n_neg_total": len(negq)}
pd.Series(json_meta["neg_sample"]).to_frame("qi").to_parquet(D + "llm_haiku45_open_negsample.parquet")
if os.environ.get("DRY"):
    sys.exit()
V = pd.read_parquet(D + "modal_pair_views.parquet")
P = dict(zip(V.id.tolist(), V.view.tolist()))
for i in set(todo.q) | set(todo.cand):
    if int(i) not in P:
        P[int(i)] = pr_text(int(i))
rows = list(done[cols].itertuples(index=False))
spent, t0 = 0.0, time.time()
with cf.ThreadPoolExecutor(8) as ex:
    for s in range(0, len(todo), 200):
        ch = todo.iloc[s:s + 200]
        res = list(ex.map(lambda qc: judge(P[int(qc[0])], P[int(qc[1])]), zip(ch.q, ch.cand)))
        rows += [(qi, c, *r, True) for qi, c, r in zip(ch.qi, ch.cand, res)]
        R = pd.DataFrame(rows, columns=cols)
        R.to_parquet(out_f)
        spent = float((R.in_tok[R.new] * PRICE_IN + R.out_tok[R.new] * PRICE_OUT).sum())
        print(len(R), "/", len(sel), f"new spend ${spent:.2f}", round(time.time() - t0), "s", flush=True)
        if spent >= BUDGET:
            print("BUDGET STOP", flush=True)
            break
pd.Series({**{k: v for k, v in json_meta.items() if k != "neg_sample"}, "pairs": len(rows),
           "new_usd": spent, "budget": BUDGET, "neg_sample_n": len(sample),
           "new_pairs": int(sum(r[-1] for r in rows)), "reused_pairs": int(sum(not r[-1] for r in rows))}).to_json(D + "llm_haiku45_open_cost.json")
print("done", len(rows), f"${spent:.2f}", flush=True)
