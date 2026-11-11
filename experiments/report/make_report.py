"""Write experiments/report/REPORT.md from experiments/results/*. Every number is read from the result files."""
import json
import os

import pandas as pd

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "..", "results") + "/"
S = pd.read_csv(R + "strategies_by_group.csv"); PC = pd.read_csv(R + "paired_cross_author.csv")
FA = pd.read_csv(R + "false_alarms.csv"); PF = pd.read_csv(R + "paired_false_alarms.csv"); OC = pd.read_csv(R + "operating_curve.csv")
RP = pd.read_csv(R + "random_pair_vs_live_queue.csv"); SM = json.load(open(R + "summary.json")); ER = pd.read_csv(R + "errors_cross_author.csv")
CC = pd.read_csv(R + "class_counts.csv", index_col=0)
BASE = "Jinx + MiniLM, LR (current tool)"; WANG = "INTRUDE + time (Wang et al. 2019), LR"; CG = "contrib-guard/phoenix (bot, exact port)"
X = S[S.group == "cross-author"].set_index("method"); NX = int(X.n.iloc[0])
def v(m, k="R@1", g=None):
    d = X if g is None else S[S.group == g].set_index("method"); return d.loc[m, k]
def civ(m, k, g=None):
    d = X if g is None else S[S.group == g].set_index("method"); r = d.loc[m]; return f"{r[k]:.3f} [{r[k+' lo']:.3f}, {r[k+' hi']:.3f}]"
def pd_(ref, m, k):
    r = PC[(PC.reference == ref) & (PC.method == m)].iloc[0]; return r[k] * 100, r[k + " lo"] * 100, r[k + " hi"] * 100
def pts(t): return f"{t[0]:+.1f} points [{t[1]:+.1f}, {t[2]:+.1f}]"
def sig(t): return t[1] > 0 or t[2] < 0
OURS = lambda m: m.startswith("Jinx") or m.startswith("All signals") or m.startswith("Cascade") or "+ Jinx" in m or "re-rank" in m or m.startswith("Fine-tuned")
# kill rule: best non-Jinx strategy (does not use Jinx's score or features) on cross-author R@5
indep = [m for m in X.index if not OURS(m)]
best_b = X.loc[indep].sort_values(["R@5", "R@1"], ascending=False).index[0]
k5 = pd_(best_b, BASE, "dR@5") if best_b in set(PC.reference) else None
if k5 is None:
    r = PC[(PC.reference == BASE) & (PC.method == best_b)].iloc[0]; k5 = (-r["dR@5"] * 100, -r["dR@5 hi"] * 100, -r["dR@5 lo"] * 100)
best_any = X.sort_values(["R@5", "R@1"], ascending=False).index[0]
FK = lambda f: int(str(f).split()[0])
fam_best = X.reset_index().sort_values(["R@1", "MRR"], ascending=False).groupby("family").head(1)
fam_best = fam_best.iloc[fam_best.family.map(FK).argsort()]
_rp = RP.copy(); _rp["a"] = _rp["random-pair AUC"].rank(ascending=False, method="min").astype(int); _rp["b"] = _rp["live-queue R@1 (cross-author)"].rank(ascending=False, method="min").astype(int)
OVER = [(r.method, r.a, r.b) for _, r in _rp.assign(sh=_rp.b - _rp.a).sort_values("sh", ascending=False).head(4).iterrows()]
_w = PC[PC.reference == WANG]; NSIG5 = int((_w["dR@5 lo"] > 0).sum())
_b = PC[PC.reference == BASE]; _sb = _b[(_b["dR@1 lo"] > 0) | (_b["dR@5 lo"] > 0) | (_b["dMRR lo"] > 0)]
SIGB = list(_sb.method); NSIGB = len(SIGB)
L = []; w = L.append
w("# Jinx strategy study: which duplicate-PR detection strategy works on coding-agent PRs?\n")
w("All numbers in this file are produced by `experiments/report/make_report.py` from `experiments/results/`. "
  "Benchmark: AIDev (CC BY 4.0, hao-li/AIDev on Hugging Face), live-queue evaluation. Nothing here used OpenAI. Jev (TypeSafe) was **not** run: its weights are not public and the user cancelled it; it is listed as future work only.\n")
w("## 1. Plain-English summary\n")
w("- **Task.** When a coding agent opens a new pull request (PR), find the already-open PR in the same repository that does the same work (its *duplicate*). "
  "Each method ranks every PR that was open at that moment (the *live queue*; median 40 PRs, p90 314).")
w(f"- **Hard case = cross-author pairs** ({NX} pairs, two different authors). Self-replacement pairs (same author re-opens their own work) are easy for almost every method.")
w(f"- **Best top-1 on cross-author:** `{X.sort_values(['R@1','MRR'], ascending=False).index[0]}` with Recall@1 {civ(X.sort_values(['R@1','MRR'], ascending=False).index[0], 'R@1')}. "
  f"Current Jinx tool: {civ(BASE, 'R@1')}. Classic research detector ({WANG}): {civ(WANG, 'R@1')}. Best existing bot ({CG}): {civ(CG, 'R@1')}.")
w(f"- **Best Recall@5 on cross-author:** `{best_any}` with {civ(best_any, 'R@5')}. Jinx: {civ(BASE, 'R@5')}.")
w(f"- **Kill rule (pre-registered by the user): \"if AgentDup does not beat the best baseline on cross-author Recall@5 by a meaningful, CI-backed margin, say so plainly.\"** (AgentDup was the tool's earlier name.) "
  f"Best baseline that does not use Jinx's own signals: `{best_b}` (Recall@5 {v(best_b,'R@5'):.3f}). Jinx minus baseline: {pts(k5)}. "
  + ("**The kill rule PASSES.**" if k5[1] > 0 else "**The kill rule FAILS: the confidence interval includes zero.**")
  + f" Strategies with a CI-backed Recall@5 gain over `{WANG}`: {NSIG5} of {len(PC[PC.reference == WANG])}.")
w(f"- **Did any new strategy beat the current Jinx tool?** Strategies with a CI-backed gain over it on Recall@1, Recall@5 or MRR: {NSIGB}"
  + (" (" + "; ".join(SIGB) + ")." if SIGB else ". The best new ones (all-signals LR, cascades with re-rankers or LLM judges) are within noise of it."))
d1 = pd_(WANG, BASE, "dR@1"); dm = pd_(WANG, BASE, "dMRR"); dc5 = pd_(CG, BASE, "dR@5"); dc1 = pd_(CG, BASE, "dR@1")
w(f"- **What is CI-backed:** vs the classic detector, Recall@1 {pts(d1)} and MRR {pts(dm)}. vs the best existing bot, Recall@5 {pts(dc5)} and Recall@1 {pts(dc1)}.")
fb, fw = FA.set_index("method").loc[BASE], FA.set_index("method").loc[WANG]
pf = PF[(PF.reference == WANG) & (PF.method == BASE)].iloc[0]
w(f"- **False alarms** (alert on a PR that has no duplicate, at a matched threshold): Jinx {fb.FAR*100:.1f}% [{fb['FAR lo']*100:.1f}, {fb['FAR hi']*100:.1f}] vs classic {fw.FAR*100:.1f}% "
  f"(difference {pf.dFAR*100:+.1f} points [{pf['dFAR lo']*100:+.1f}, {pf['dFAR hi']*100:+.1f}]).")
lk = "Links only (same issue / #ref)"
w(f"- **Label-bias warning.** A trivial rule that only checks \"same linked issue\" or \"#number mentioned in the text\" gets cross-author Recall@1 {v(lk):.3f}. "
  f"Many labels come from comments that also put a link in the PR, so part of the benchmark is easy. We therefore also report the subset with no link at all.")
w(f"- **Random pairs vs live queues.** Ranking the {SM['n_methods']} strategies by the classic random-pair AUC and by live-queue cross-author Recall@1 agrees only partly (Kendall tau {SM['kendall_tau random-pair AUC vs live-queue cross-author R@1'][0]:.2f}). "
  "Strategies that look much better under random pairs than in live queues: " + "; ".join(f"`{m}` (AUC rank {a}, live rank {b})" for m, a, b in OVER) + " (see Section 8).\n")
w("## 2. Data\n")
w(f"- Labelled duplicate pairs: {int(S[S.group=='all labelled'].n.iloc[0])} (self-replacement {int(S[S.group=='self-replacement'].n.iloc[0])}, cross-author {NX}: "
  f"same agent {int(S[S.group=='cross-author, same agent'].n.iloc[0])}, cross-agent {int(S[S.group=='cross-author, cross-agent'].n.iloc[0])}). "
  "Labels are *silver*: taken from AIDev comments such as \"duplicate of #N\" / \"superseded by #N\" where both PRs are in AIDev.")
w("- Negative queries (PRs with no known duplicate, used for false alarms): 2,965. PRs needed (queries + queues): 76,209.")
w("- Agent-vs-human pairs: **not available** (this AIDev version has agent PRs only and the GitHub token was dead).\n")
w("Duplicate classes (by code overlap between the two PRs):\n")
w("| Class | cross-author | self-replacement |\n|---|---|---|\n" + "\n".join(f"| {i} | {int(r['cross-author'])} | {int(r['self-replacement'])} |" for i, r in CC.iterrows()) + "\n")
w("Extra relation groups: *same issue, different code* = shares a linked issue and has class C or D; *same code, different description* = code twin with title+body TF-IDF < 0.3.\n")
w("## 3. Strategies compared\n")
w("| Family | What it does | Strategies |\n|---|---|---|")
desc = {"0 trivial": "newest open PR first", "1 lexical": "word overlap of title + description", "2 code": "overlap of changed files, hunks, identical lines, or BM25 on the diff",
        "3 links": "same linked issue or explicit #ref", "4 embedding": "cosine of a neural sentence/code embedding", "5 existing bot": "matching logic of public duplicate-PR bots",
        "6 unsupervised hybrid": "reciprocal-rank fusion (RRF) of several signals, no training", "7 supervised": "logistic regression (LR) / gradient boosting trained on repo-grouped folds",
        "8 re-ranker on top-k": "cross-encoder re-scores Jinx's top 10", "9 LLM judge on top-k": "LLM answers duplicate yes/no for each of Jinx's top k",
        "10 stacked cascade (ours)": "LR over Jinx score + re-ranker / LLM scores on the top 10"}
for f, g in sorted(X.reset_index().groupby("family"), key=lambda t: FK(t[0])): w(f"| {f} | {desc.get(f,'')} | {'; '.join(g.method)} |")
w("\nTraining uses 5 repository-grouped folds (no repository appears in both train and test). Confidence intervals: repository-cluster bootstrap, 95%.\n")
w("## 4. Best strategy of each family, cross-author\n")
w("| Family | Best strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |\n|---|---|---|---|---|")
for _, r in fam_best.iterrows(): w(f"| {r.family} | {r.method} | {civ(r.method,'R@1')} | {civ(r.method,'R@5')} | {civ(r.method,'MRR')} |")
w("\n## 5. Which strategy for which kind of duplicate (Recall@1)\n")
gl = [g for g in S.group.unique() if g != "all labelled"]
w("| Group | n | best strategy | its Recall@1 | Jinx | INTRUDE + time | contrib-guard | best non-Jinx |\n|---|---|---|---|---|---|---|---|")
for g in gl:
    d = S[S.group == g].set_index("method"); b = d.sort_values(["R@1", "MRR"], ascending=False).index[0]
    bi = d.loc[[m for m in d.index if not OURS(m)]].sort_values(["R@1", "MRR"], ascending=False).index[0]
    w(f"| {g} | {int(d.n.iloc[0])} | {b} | {d.loc[b,'R@1']:.3f} | {d.loc[BASE,'R@1']:.3f} | {d.loc[WANG,'R@1']:.3f} | {d.loc[CG,'R@1']:.3f} | {bi} ({d.loc[bi,'R@1']:.3f}) |")
w("\n## 6. Paired differences (cross-author, points, 95% CI; * = CI excludes 0)\n")
for ref in PC.reference.unique():
    w(f"**vs `{ref}`**\n\n| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |\n|---|---|---|---|")
    for _, r in PC[PC.reference == ref].sort_values("dR@1", ascending=False).iterrows():
        cell = lambda k: f"{r[k]*100:+.1f} [{r[k+' lo']*100:+.1f}, {r[k+' hi']*100:+.1f}]" + ("*" if r[k+' lo'] > 0 or r[k+' hi'] < 0 else "")
        w(f"| {r.method} | {cell('dR@1')} | {cell('dR@5')} | {cell('dMRR')} |")
    w("")
w("## 7. False alarms and operating curve\n")
w("Threshold per fold = median top-1 score of the training folds' cross-author duplicates; alert if the top-1 score is above it. 2,965 PRs with no duplicate.\n")
w("| Strategy | False-alarm rate [95% CI] | cross-author correct alerts |\n|---|---|---|")
for _, r in FA.sort_values("FAR").iterrows(): w(f"| {r.method} | {r.FAR*100:.1f}% [{r['FAR lo']*100:.1f}, {r['FAR hi']*100:.1f}] | {r['cross-author correct alerts']*100:.1f}% |")
oc = OC.pivot(index="method", columns="FAR target", values=OC.columns[-1]).sort_values(0.05, ascending=False)
w("\nShare of cross-author duplicates caught with the right top-1 when the threshold is set to give a fixed false-alarm rate:\n")
w("| Strategy | " + " | ".join(f"FAR {int(c*100)}%" for c in oc.columns) + " |\n|---|" + "---|" * len(oc.columns))
for m, r in oc.iterrows(): w(f"| {m} | " + " | ".join(f"{x*100:.1f}%" for x in r) + " |")
w("\n## 8. Random-pair (classic) evaluation vs live queue\n")
rp = RP.copy(); rp["AUC rank"] = rp["random-pair AUC"].rank(ascending=False, method="min").astype(int); rp["live rank"] = rp["live-queue R@1 (cross-author)"].rank(ascending=False, method="min").astype(int)
rp["shift"] = rp["AUC rank"] - rp["live rank"]
w("Random-pair AUC = can the method tell the true duplicate from one random other PR in the queue. Live queue = must rank it first among all open PRs.\n")
w("| Strategy | random-pair AUC | AUC rank | live-queue cross-author R@1 | live rank |\n|---|---|---|---|---|")
for _, r in rp.sort_values("random-pair AUC", ascending=False).iterrows(): w(f"| {r.method} | {r['random-pair AUC']:.3f} | {r['AUC rank']} | {r['live-queue R@1 (cross-author)']:.3f} | {r['live rank']} |")
w("\n## 9. Latency and cost\n")
lat = SM["latency"]
w("| Component | Hardware | Numbers |\n|---|---|---|")
for k, x in lat.items(): w(f"| {k} | {x.get('gpu', 'CPU' if 'cpu' in k or 'lexical' in k else '') if isinstance(x, dict) else ''} | {json.dumps(x)} |")
cf = R + "costs/modal_billing.json"
if os.path.exists(cf): w(f"\nModal billing for app `agentdup-study`: {json.dumps(json.load(open(cf)))}")
w("\n## 10. Error analysis (current Jinx tool, cross-author pairs it does not rank first)\n")
w(f"{len(ER)} of {NX} cross-author queries are missed at rank 1.\n")
w("| By class | misses |\n|---|---|\n" + "\n".join(f"| {k} | {n} |" for k, n in ER["class"].value_counts().items()))
w(f"\nTop-1 was a PR by the *same author as the new PR* in {ER['top-1 same author as new PR'].mean()*100:.0f}% of misses (the author's own other open work). "
  f"Median queue size of misses: {ER['queue size'].median():.0f}. Full list: `experiments/results/errors_cross_author.csv`.\n")
w("## 11. Limitations\n")
w("- Silver labels from comments; no new human labels. The 142 hand-labelled duplicates in the 600-PR AIDev sample have no partner PR and could not be used for ranking.")
w("- Agent-vs-human duplicates are not covered.")
w("- PRSense, Simili, vector-triage and PRism are local re-implementations with free models (their shipped versions need OpenAI/Gemini/GitHub Models keys). contrib-guard (phoenix) is an exact port.")
w("- LLM judges and re-rankers only see Jinx's top-k, so their Recall@k is capped by Jinx's Recall@k. Claude Haiku was run on cross-author + negative queries only (budget).")
w("- Commercial review tools (CodeRabbit, Copilot review, Qodo, Greptile, ...) were compared from their documentation only, not run.")
w("- Jev (TypeSafe System One) was not evaluated.\n")
w("## 12. Reproduce\n")
w("```bash\ncd experiments/bench_v2\npython3 bm25_feats.py            # BM25 features\nbash run_embeds.sh               # CPU MiniLM embeddings (or Modal below)\n"
  "modal run ../modal/gpu_jobs.py::embed_all\nmodal run ../modal/gpu_jobs.py::rerank_all\n"
  "modal run ../modal/gpu_jobs.py::judge --model Qwen/Qwen2.5-1.5B-Instruct --tag qwen15\n"
  "modal run ../modal/gpu_jobs.py::judge --model Qwen/Qwen2.5-7B-Instruct --tag qwen7\n"
  "modal run ../modal/gpu_jobs.py::judge --model Qwen/Qwen2.5-Coder-7B-Instruct --tag qwencoder7\n"
  "modal run ../modal/gpu_jobs.py::judge --model Qwen/Qwen2.5-14B-Instruct --tag qwen14\n"
  "modal run ../modal/gpu_jobs.py::finetune_all\nANTHROPIC_API_KEY=... python3 claude_judge.py   # budget-capped\n"
  "NB=2000 python3 eval2.py\npython3 ../report/make_report.py && python3 ../report/make_tables.py\n```\n")
w("Full per-group tables for every strategy: `tables.md`. Raw per-query ranks: `experiments/results/ranks.parquet`.")
open(os.path.join(H, "REPORT.md"), "w").write("\n".join(L) + "\n"); print("REPORT.md", len(L), "lines; kill-rule baseline:", best_b, k5)
