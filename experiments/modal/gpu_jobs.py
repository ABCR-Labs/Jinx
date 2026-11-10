"""GPU jobs on Modal for the AgentDup strategy study.
Data lives in the Modal volume `agentdup-data` (uploaded from data/modal_*.parquet).
  embed:  sentence-transformers encoders over 76,209 PRs (raw / stripped / diff views)
  rerank: cross-encoders over the AgentDup top-10 candidates of every query
  judge:  open LLM yes/no judges (Jev-style P(yes) from next-token logprobs) via vLLM over the top-10 candidates
usage: modal run gpu_jobs.py::embed --model M --variant V --tag T
       modal run gpu_jobs.py::rerank --model M --tag T
       modal run gpu_jobs.py::judge --model M --tag T [--topk 10]"""
import time, json, modal
app = modal.App("agentdup-study")
vol = modal.Volume.from_name("agentdup-data", create_if_missing=True)
hf = modal.Volume.from_name("agentdup-hf-cache", create_if_missing=True)
st_img = (modal.Image.debian_slim(python_version="3.11")
          .pip_install("torch==2.5.1", "sentence-transformers==3.3.1", "transformers==4.46.3", "pandas", "pyarrow", "numpy<2.1", "einops")
          .env({"HF_HOME": "/hf"}))
vllm_img = (modal.Image.debian_slim(python_version="3.11")
            .pip_install("vllm==0.8.5", "transformers==4.51.3", "pandas", "pyarrow")
            .env({"HF_HOME": "/hf", "VLLM_USE_V1": "0"}))
V = {"/data": vol, "/hf": hf}
SYS = ("You review pull requests for a code repository. Two PRs are duplicates if they try to make the same change "
       "or fix the same problem, so only one of them should be merged.")
def prompt(a, b):
    return f"NEW PR\n{a}\n\nOPEN PR\n{b}\n\nAre these two pull requests duplicates? Answer Yes or No."

@app.function(image=st_img, gpu="L4", volumes=V, timeout=3 * 3600)
def embed_job(model: str, variant: str, tag: str, maxlen: int = 512):
    import numpy as np, pandas as pd
    from sentence_transformers import SentenceTransformer
    E = pd.read_parquet("/data/modal_embed_texts.parquet")
    m = SentenceTransformer(model, device="cuda", trust_remote_code=True); m.max_seq_length = maxlen; m.half()
    t0 = time.time()
    X = m.encode(E[variant].tolist(), batch_size=128, normalize_embeddings=True, show_progress_bar=False).astype(np.float16)
    el = time.time() - t0
    np.savez(f"/data/emb_{tag}.npz", ids=E.id.values, emb=X); vol.commit()
    info = {"tag": tag, "model": model, "variant": variant, "maxlen": maxlen, "n": len(E), "dim": X.shape[1], "gpu": "L4",
            "seconds": round(el, 1), "ms_per_pr_gpu": round(1000 * el / len(E), 3)}
    print(info); return info

@app.function(image=st_img, gpu="L4", volumes=V, timeout=3 * 3600)
def rerank_job(model: str, tag: str, maxlen: int = 512):
    import numpy as np, pandas as pd
    from sentence_transformers import CrossEncoder
    T = pd.read_parquet("/data/modal_pairs.parquet"); _v = pd.read_parquet("/data/modal_pair_views.parquet"); P = dict(zip(_v.id.tolist(), _v["view"].tolist()))
    ce = CrossEncoder(model, device="cuda", max_length=maxlen, trust_remote_code=True); ce.model.half()
    t0 = time.time()
    s = ce.predict([(P[q], P[c]) for q, c in zip(T.q.tolist(), T.cand.tolist())], batch_size=64, show_progress_bar=False)
    el = time.time() - t0
    s = np.asarray(s, dtype=np.float32); s = s[:, -1] if s.ndim == 2 else s
    T[tag] = s; T[["qi", "cand", tag]].to_parquet(f"/data/rr_{tag}.parquet"); vol.commit()
    info = {"tag": tag, "model": model, "pairs": len(T), "gpu": "L4", "seconds": round(el, 1), "ms_per_pair_gpu": round(1000 * el / len(T), 3)}
    print(info); return info

@app.function(image=vllm_img, gpu="L40S", volumes=V, timeout=6 * 3600)
def judge_job(model: str, tag: str, topk: int = 10, maxlen: int = 4096):
    import math, numpy as np, pandas as pd
    from vllm import LLM, SamplingParams
    T = pd.read_parquet("/data/modal_pairs.parquet"); T = T[T["rank"] <= topk].reset_index(drop=True)
    _v = pd.read_parquet("/data/modal_pair_views.parquet"); P = dict(zip(_v.id.tolist(), _v["view"].tolist()))
    llm = LLM(model=model, max_model_len=maxlen, dtype="bfloat16", gpu_memory_utilization=0.9, enable_prefix_caching=True, seed=0)
    tok = llm.get_tokenizer()
    def ids(w): return tok.encode(w, add_special_tokens=False)[0]
    yes, no = {ids("Yes"), ids(" Yes"), ids("yes")}, {ids("No"), ids(" No"), ids("no")}
    msgs = [[{"role": "system", "content": SYS}, {"role": "user", "content": prompt(P[q][:3000], P[c][:3000])}] for q, c in zip(T.q.tolist(), T.cand.tolist())]
    sp = SamplingParams(max_tokens=1, temperature=0.0, logprobs=20)
    t0 = time.time(); outs = llm.chat(msgs, sp, use_tqdm=False); el = time.time() - t0
    py, ntok = [], []
    for o in outs:
        lp = o.outputs[0].logprobs[0]
        ly = [v.logprob for k, v in lp.items() if k in yes]; ln = [v.logprob for k, v in lp.items() if k in no]
        a = np.logaddexp.reduce(ly) if ly else -30.0; b = np.logaddexp.reduce(ln) if ln else -30.0
        py.append(float(1 / (1 + math.exp(b - a)))); ntok.append(len(o.prompt_token_ids))
    T["p_yes"] = py; T["prompt_tokens"] = ntok
    T[["qi", "cand", "rank", "p_yes", "prompt_tokens"]].to_parquet(f"/data/llm_{tag}.parquet"); vol.commit()
    info = {"tag": tag, "model": model, "pairs": len(T), "gpu": "L40S", "seconds": round(el, 1), "ms_per_pair_gpu_batched": round(1000 * el / len(T), 3),
            "prompt_tokens_total": int(sum(ntok))}
    print(info); return info

@app.local_entrypoint()
def embed(model: str, variant: str, tag: str, maxlen: int = 512):
    print(json.dumps(embed_job.remote(model, variant, tag, maxlen)))

@app.local_entrypoint()
def rerank(model: str, tag: str, maxlen: int = 512):
    print(json.dumps(rerank_job.remote(model, tag, maxlen)))

@app.local_entrypoint()
def judge(model: str, tag: str, topk: int = 10):
    print(json.dumps(judge_job.remote(model, tag, topk)))

EMBED_PLAN = [("BAAI/bge-small-en-v1.5", "raw", "bge_raw"), ("BAAI/bge-small-en-v1.5", "stripped", "bge_stripped"),
              ("BAAI/bge-small-en-v1.5", "diff", "bge_diff"), ("BAAI/bge-base-en-v1.5", "stripped", "bgebase_stripped"),
              ("microsoft/unixcoder-base", "diff", "unix_diff"), ("microsoft/unixcoder-base", "stripped", "unix_stripped"),
              ("microsoft/codebert-base", "diff", "codebert_diff"), ("jinaai/jina-embeddings-v2-base-code", "diff", "jinacode_diff")]

@app.local_entrypoint()
def embed_all():
    for r in embed_job.starmap([(m, v, t, 512) for m, v, t in EMBED_PLAN], return_exceptions=True):
        print(json.dumps(r if isinstance(r, dict) else {"error": repr(r)[:500]}), flush=True)

RERANK_PLAN = [("cross-encoder/ms-marco-MiniLM-L6-v2", "ce_msmarco"), ("BAAI/bge-reranker-base", "ce_bgebase"),
               ("BAAI/bge-reranker-v2-m3", "ce_bgem3")]

@app.local_entrypoint()
def rerank_all():
    for r in rerank_job.starmap([(m, t, 512) for m, t in RERANK_PLAN], return_exceptions=True):
        print(json.dumps(r if isinstance(r, dict) else {"error": repr(r)[:500]}), flush=True)
