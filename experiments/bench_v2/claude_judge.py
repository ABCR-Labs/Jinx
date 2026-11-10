"""Claude Haiku 4.5 duplicate judge on AgentDup top-K candidates (cross-author queries) + top-1 of negative queries.
Asks for a JSON verdict with a 0-100 duplicate probability; logs tokens and cost; hard budget stop.
usage: claude_judge.py TAG K BUDGET_USD"""
import json, os, re, sys, time, concurrent.futures as cf, pandas as pd, anthropic
D = "/home/ubuntu/research/prdupecheck/data/"
tag, K, BUDGET = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5")
PRICE_IN, PRICE_OUT = 1.0 / 1e6, 5.0 / 1e6
T = pd.read_parquet(D + "modal_pairs.parquet"); _v = pd.read_parquet(D + "modal_pair_views.parquet"); P = dict(zip(_v.id.tolist(), _v.view.tolist()))
sel = pd.concat([T[~T.neg & ~T.self & (T["rank"] <= K)], T[T.neg & (T["rank"] <= 1)]]).reset_index(drop=True)
out_f = D + f"llm_{tag}.parquet"
done = pd.read_parquet(out_f) if os.path.exists(out_f) else pd.DataFrame(columns=["qi", "cand", "p_yes", "verdict", "in_tok", "out_tok", "ms"])
key = set(zip(done.qi, done.cand)); todo = sel[[k not in key for k in zip(sel.qi, sel.cand)]]
SYS = ("You review pull requests for a code repository. Two PRs are duplicates if they try to make the same change or fix the same "
       "problem, so only one of them should be merged. Reply with only a JSON object: "
       '{"duplicate": "yes" or "no", "probability": integer 0-100 that they are duplicates}.')
cl = anthropic.Anthropic(max_retries=8)
spent = float(((done.in_tok * PRICE_IN) + (done.out_tok * PRICE_OUT)).sum()) if len(done) else 0.0
def one(q, c):
    msg = f"NEW PR\n{P[q][:3000]}\n\nOPEN PR\n{P[c][:3000]}\n\nAre these two pull requests duplicates?"
    t0 = time.perf_counter()
    r = cl.messages.create(model=MODEL, max_tokens=40, system=SYS, messages=[{"role": "user", "content": msg}])
    ms = 1000 * (time.perf_counter() - t0); txt = r.content[0].text
    m = re.search(r'"probability"\s*:\s*(\d+)', txt); v = re.search(r'"duplicate"\s*:\s*"(\w+)"', txt)
    p = int(m.group(1)) / 100 if m else (1.0 if v and v.group(1).lower() == "yes" else 0.0)
    return p, (v.group(1).lower() if v else txt[:20]), r.usage.input_tokens, r.usage.output_tokens, ms
rows = list(done.itertuples(index=False)); t_all = time.time()
with cf.ThreadPoolExecutor(8) as ex:
    for start in range(0, len(todo), 200):
        chunk = todo.iloc[start:start + 200]
        res = list(ex.map(lambda qc: one(*qc), zip(chunk.q.tolist(), chunk.cand.tolist())))
        for (qi, c), r in zip(zip(chunk.qi, chunk.cand), res): rows.append((qi, c, *r))
        D_ = pd.DataFrame(rows, columns=["qi", "cand", "p_yes", "verdict", "in_tok", "out_tok", "ms"]); D_.to_parquet(out_f)
        spent = float((D_.in_tok * PRICE_IN + D_.out_tok * PRICE_OUT).sum())
        print(len(D_), "/", len(sel), f"${spent:.2f}", round(time.time() - t_all), "s", flush=True)
        if spent >= BUDGET: print("BUDGET STOP", flush=True); break
json.dump({"model": MODEL, "pairs": len(rows), "usd": spent, "budget": BUDGET}, open(D + f"llm_{tag}_cost.json", "w"))
print("done", len(rows), f"${spent:.2f}", flush=True)
