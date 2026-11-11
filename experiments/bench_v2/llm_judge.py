"""Open LLM judge (Qwen2.5 Instruct, local CPU): P(yes) that two PRs are duplicates, one forward pass per pair.
usage: llm_judge.py MODEL TAG K NNEG   -> scores Doppel top-K for cross-author queries and top-1 for NNEG negative queries."""
import pickle, sys, time, json, os, numpy as np, pandas as pd, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pairtext import pr_text, D
torch.set_num_threads(int(os.environ.get("THREADS", 8)))
model, tag, K, NNEG = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
B = pickle.load(open(D + "bench.pkl", "rb")); Q = B["queries"]
T = pd.read_parquet(D + "top10.parquet")
xq = [i for i, x in enumerate(Q) if not x["neg"] and not x["self"]]
nq = [i for i, x in enumerate(Q) if x["neg"]]
rng = np.random.default_rng(0); nq = sorted(rng.choice(nq, NNEG, replace=False).tolist())
sel = pd.concat([T[T.qi.isin(xq) & (T["rank"] <= K)], T[T.qi.isin(nq) & (T["rank"] <= 1)]])
out_f = D + f"llm_{tag}.parquet"
done = pd.read_parquet(out_f) if os.path.exists(out_f) else pd.DataFrame(columns=["qi", "cand", "p_yes", "ms"])
key = set(zip(done.qi, done.cand)); todo = sel[[k not in key for k in zip(sel.qi, sel.cand)]]
tok = AutoTokenizer.from_pretrained(model); lm = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.bfloat16).eval()
yes = [tok.encode(w, add_special_tokens=False)[0] for w in ["Yes", " Yes"]]; no = [tok.encode(w, add_special_tokens=False)[0] for w in ["No", " No"]]
SYS = "You review pull requests for a code repository. Two PRs are duplicates if they try to make the same change or fix the same problem, so only one of them should be merged."
rows = list(done.itertuples(index=False)); t_all = time.time()
for n, (qi, c) in enumerate(zip(todo.qi, todo.cand)):
    msg = [{"role": "system", "content": SYS},
           {"role": "user", "content": f"NEW PR\n{pr_text(int(Q[qi]['q']))}\n\nOPEN PR\n{pr_text(int(c))}\n\nAre these two pull requests duplicates? Answer Yes or No."}]
    ids = tok.apply_chat_template(msg, add_generation_prompt=True, return_tensors="pt")
    if not torch.is_tensor(ids): ids = ids["input_ids"]
    ids = ids[:, -2048:]
    t0 = time.perf_counter()
    with torch.no_grad(): lg = lm(ids).logits[0, -1].float()
    ms = 1000 * (time.perf_counter() - t0)
    py, pn = torch.logsumexp(lg[yes], 0), torch.logsumexp(lg[no], 0)
    rows.append((qi, c, float(torch.sigmoid(py - pn)), ms))
    if n % 100 == 0:
        pd.DataFrame(rows, columns=["qi", "cand", "p_yes", "ms"]).to_parquet(out_f)
        print(n, "/", len(todo), round(time.time() - t_all), "s", flush=True)
pd.DataFrame(rows, columns=["qi", "cand", "p_yes", "ms"]).to_parquet(out_f); print("done", len(rows), flush=True)
