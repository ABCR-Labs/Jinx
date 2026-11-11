# AgentDup strategy study: which duplicate-PR detection strategy works on coding-agent PRs?

All numbers in this file are produced by `experiments/report/make_report.py` from `experiments/results/`. Benchmark: AIDev (CC BY 4.0, hao-li/AIDev on Hugging Face), live-queue evaluation. Nothing here used OpenAI. Jev (TypeSafe) was **not** run: its weights are not public and the user cancelled it; it is listed as future work only.

## 1. Plain-English summary

- **Task.** When a coding agent opens a new pull request (PR), find the already-open PR in the same repository that does the same work (its *duplicate*). Each method ranks every PR that was open at that moment (the *live queue*; median 40 PRs, p90 314).
- **Hard case = cross-author pairs** (342 pairs, two different authors). Self-replacement pairs (same author re-opens their own work) are easy for almost every method.
- **Best top-1 on cross-author:** `All signals, LR` with Recall@1 0.906 [0.872, 0.937]. Current AgentDup tool: 0.901 [0.868, 0.931]. Classic research detector (INTRUDE + time (Wang et al. 2019), LR): 0.810 [0.767, 0.857]. Best existing bot (contrib-guard/phoenix (bot, exact port)): 0.778 [0.727, 0.840].
- **Best Recall@5 on cross-author:** `All signals, LR` with 0.974 [0.956, 0.989]. AgentDup: 0.971 [0.952, 0.991].
- **Kill rule (pre-registered by the user): "if AgentDup does not beat the best baseline on cross-author Recall@5 by a meaningful, CI-backed margin, say so plainly."** Best baseline that does not use AgentDup's own signals: `INTRUDE + time (Wang et al. 2019), LR` (Recall@5 0.953). AgentDup minus baseline: +1.8 points [-0.9, +5.2]. **The kill rule FAILS: the confidence interval includes zero.** Strategies with a CI-backed Recall@5 gain over `INTRUDE + time (Wang et al. 2019), LR`: 0 of 60.
- **Did any new strategy beat the current AgentDup tool?** Strategies with a CI-backed gain over it on Recall@1, Recall@5 or MRR: 0. The best new ones (all-signals LR, cascades with re-rankers or LLM judges) are within noise of it.
- **What is CI-backed:** vs the classic detector, Recall@1 +9.1 points [+5.0, +13.1] and MRR +5.9 points [+2.7, +9.3]. vs the best existing bot, Recall@5 +5.3 points [+1.2, +9.7] and Recall@1 +12.3 points [+6.8, +17.0].
- **False alarms** (alert on a PR that has no duplicate, at a matched threshold): AgentDup 2.5% [1.9, 3.3] vs classic 4.6% (difference -2.1 points [-2.7, -1.5]).
- **Label-bias warning.** A trivial rule that only checks "same linked issue" or "#number mentioned in the text" gets cross-author Recall@1 0.839. Many labels come from comments that also put a link in the PR, so part of the benchmark is easy. We therefore also report the subset with no link at all.
- **Random pairs vs live queues.** Ranking the 61 strategies by the classic random-pair AUC and by live-queue cross-author Recall@1 agrees only partly (Kendall tau 0.76). Strategies that look much better under random pairs than in live queues: `LLM judge Qwen2.5-1.5B re-rank top-10` (AUC rank 44, live rank 59); `LLM judge Qwen2.5-Coder-7B re-rank top-10` (AUC rank 15, live rank 28); `All signals, gradient boosting` (AUC rank 2, live rank 14); `LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10` (AUC rank 4, live rank 15) (see Section 8).

## 2. Data

- Labelled duplicate pairs: 1867 (self-replacement 1525, cross-author 342: same agent 228, cross-agent 114). Labels are *silver*: taken from AIDev comments such as "duplicate of #N" / "superseded by #N" where both PRs are in AIDev.
- Negative queries (PRs with no known duplicate, used for false alarms): 2,965. PRs needed (queries + queues): 76,209.
- Agent-vs-human pairs: **not available** (this AIDev version has agent PRs only and the GitHub token was dead).

Duplicate classes (by code overlap between the two PRs):

| Class | cross-author | self-replacement |
|---|---|---|
| A. code twin (>=50% identical changed lines) | 139 | 855 |
| B. partial code overlap | 164 | 537 |
| C. same files, different code | 10 | 34 |
| D. no shared files (intent-level) | 29 | 99 |

Extra relation groups: *same issue, different code* = shares a linked issue and has class C or D; *same code, different description* = code twin with title+body TF-IDF < 0.3.

## 3. Strategies compared

| Family | What it does | Strategies |
|---|---|---|
| 0 trivial | newest open PR first | Recency only (newest open PR first) |
| 1 lexical | word overlap of title + description | TF-IDF raw text (Li et al. 2017); TF-IDF template-stripped; BM25 raw text; BM25 template-stripped |
| 2 code | overlap of changed files, hunks, identical lines, or BM25 on the diff | BM25 on diff; Changed-files Jaccard; Hunk overlap; Identical changed lines; Code overlap sum (files+hunks+lines) |
| 3 links | same linked issue or explicit #ref | Links only (same issue / #ref) |
| 4 embedding | cosine of a neural sentence/code embedding | MiniLM raw text; MiniLM template-stripped; MiniLM on diff; BGE-small raw text; BGE-small template-stripped; BGE-small on diff; BGE-base template-stripped; UniXcoder (code model) on diff; UniXcoder template-stripped text; CodeBERT (mean-pooled) on diff; Jina code embeddings v2 on diff |
| 5 existing bot | matching logic of public duplicate-PR bots | contrib-guard/phoenix (bot, exact port); Simili-bot (bot, re-impl); PRSense (bot, re-impl) |
| 6 unsupervised hybrid | reciprocal-rank fusion (RRF) of several signals, no training | RRF hybrid: BM25 + embedding; RRF hybrid: BM25 + embedding + code; RRF hybrid: text + code + links + recency |
| 7 supervised | logistic regression (LR) / gradient boosting trained on repo-grouped folds | INTRUDE + time (Wang et al. 2019), LR; AgentDup lexical, LR; AgentDup + MiniLM, LR (current tool); All signals, LR; AgentDup features, gradient boosting; All signals, gradient boosting |
| 8 re-ranker on top-k | cross-encoder re-scores AgentDup's top 10 | Cross-encoder ms-marco MiniLM re-rank top-10; Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10; Cross-encoder BGE-reranker-base re-rank top-10; Cross-encoder BGE-reranker-base + AgentDup (avg) top-10; Cross-encoder BGE-reranker-v2-m3 re-rank top-10; Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 |
| 9 LLM judge on top-k | LLM answers duplicate yes/no for each of AgentDup's top k | LLM judge Qwen2.5-1.5B re-rank top-5; LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5; LLM judge Qwen2.5-1.5B re-rank top-10; LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10; LLM judge Qwen2.5-7B re-rank top-5; LLM judge Qwen2.5-7B + AgentDup (avg) top-5; LLM judge Qwen2.5-7B re-rank top-10; LLM judge Qwen2.5-7B + AgentDup (avg) top-10; LLM judge Qwen2.5-Coder-7B re-rank top-5; LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5; LLM judge Qwen2.5-Coder-7B re-rank top-10; LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10; LLM judge Claude Haiku 4.5 re-rank top-5; LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 |
| 10 stacked cascade (ours) | LR over AgentDup score + re-ranker / LLM scores on the top 10 | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10; Cascade: AgentDup + BGE-reranker-base (stacked LR); Cascade: AgentDup + Qwen2.5-7B judge (stacked LR); Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR); Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR); Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR); Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) |

Training uses 5 repository-grouped folds (no repository appears in both train and test). Confidence intervals: repository-cluster bootstrap, 95%.

## 4. Best strategy of each family, cross-author

| Family | Best strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 0 trivial | Recency only (newest open PR first) | 0.193 [0.131, 0.282] | 0.450 [0.324, 0.615] | 0.316 [0.231, 0.431] |
| 1 lexical | TF-IDF template-stripped | 0.760 [0.707, 0.824] | 0.930 [0.894, 0.967] | 0.835 [0.789, 0.884] |
| 2 code | BM25 on diff | 0.585 [0.499, 0.686] | 0.781 [0.678, 0.878] | 0.678 [0.586, 0.773] |
| 3 links | Links only (same issue / #ref) | 0.839 [0.783, 0.902] | 0.924 [0.879, 0.967] | 0.882 [0.837, 0.933] |
| 4 embedding | BGE-small template-stripped | 0.763 [0.704, 0.822] | 0.915 [0.860, 0.956] | 0.830 [0.779, 0.876] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.778 [0.727, 0.840] | 0.918 [0.873, 0.960] | 0.843 [0.796, 0.892] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.757 [0.691, 0.827] | 0.921 [0.880, 0.965] | 0.831 [0.780, 0.884] |
| 7 supervised | All signals, LR | 0.906 [0.872, 0.937] | 0.974 [0.956, 0.989] | 0.935 [0.911, 0.956] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | 0.871 [0.832, 0.909] | 0.971 [0.952, 0.991] | 0.918 [0.891, 0.944] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 0.898 [0.863, 0.937] | 0.971 [0.952, 0.991] | 0.932 [0.907, 0.960] |
| 10 stacked cascade (ours) | Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.901 [0.859, 0.934] | 0.974 [0.956, 0.994] | 0.931 [0.902, 0.956] |

## 5. Which strategy for which kind of duplicate (Recall@1)

| Group | n | best strategy | its Recall@1 | AgentDup | INTRUDE + time | contrib-guard | best non-AgentDup |
|---|---|---|---|---|---|---|---|
| self-replacement | 1525 | AgentDup lexical, LR | 0.906 | 0.887 | 0.857 | 0.782 | INTRUDE + time (Wang et al. 2019), LR (0.857) |
| cross-author | 342 | All signals, LR | 0.906 | 0.901 | 0.810 | 0.778 | Links only (same issue / #ref) (0.839) |
| cross-author, same agent | 228 | All signals, LR | 0.908 | 0.899 | 0.825 | 0.811 | Links only (same issue / #ref) (0.851) |
| cross-author, cross-agent | 114 | Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.921 | 0.904 | 0.781 | 0.711 | Links only (same issue / #ref) (0.816) |
| cross-author, no #ref in text | 199 | All signals, LR | 0.864 | 0.854 | 0.714 | 0.714 | BGE-base template-stripped (0.754) |
| cross-author, shares linked issue | 99 | Cascade: AgentDup + BGE-reranker-base (stacked LR) | 0.960 | 0.939 | 0.889 | 0.828 | Links only (same issue / #ref) (0.919) |
| cross-author, no link at all (no #ref, no shared issue) | 140 | Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | 0.843 | 0.821 | 0.643 | 0.664 | BGE-base template-stripped (0.700) |
| same issue, different code (classes C/D, shares linked issue) | 35 | Links only (same issue / #ref) | 0.943 | 0.914 | 0.857 | 0.829 | Links only (same issue / #ref) (0.943) |
| same code, different description (code twin, text TF-IDF < 0.3) | 287 | AgentDup lexical, LR | 0.861 | 0.784 | 0.826 | 0.446 | INTRUDE + time (Wang et al. 2019), LR (0.826) |
| cross-author, same code, different description | 34 | LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 0.971 | 0.941 | 0.882 | 0.706 | Code overlap sum (files+hunks+lines) (0.912) |
| class A. code twin (>=50% identical changed lines) | 994 | AgentDup lexical, LR | 0.949 | 0.925 | 0.930 | 0.796 | INTRUDE + time (Wang et al. 2019), LR (0.930) |
| cross-author, class A. code twin (>=50% identical changed lines) | 139 | LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 0.978 | 0.971 | 0.957 | 0.892 | INTRUDE + time (Wang et al. 2019), LR (0.957) |
| class B. partial code overlap | 701 | All signals, LR | 0.880 | 0.870 | 0.782 | 0.767 | Links only (same issue / #ref) (0.797) |
| cross-author, class B. partial code overlap | 164 | All signals, LR | 0.909 | 0.896 | 0.762 | 0.720 | Links only (same issue / #ref) (0.799) |
| class C. same files, different code | 44 | AgentDup lexical, LR | 0.886 | 0.841 | 0.682 | 0.682 | BM25 raw text (0.727) |
| cross-author, class C. same files, different code | 10 | LLM judge Claude Haiku 4.5 re-rank top-5 | 0.800 | 0.700 | 0.400 | 0.500 | Links only (same issue / #ref) (0.600) |
| class D. no shared files (intent-level) | 128 | TF-IDF template-stripped | 0.812 | 0.742 | 0.641 | 0.773 | TF-IDF template-stripped (0.812) |
| cross-author, class D. no shared files (intent-level) | 29 | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.759 | 0.655 | 0.517 | 0.655 | Links only (same issue / #ref) (0.759) |

## 6. Paired differences (cross-author, points, 95% CI; * = CI excludes 0)

**vs `AgentDup + MiniLM, LR (current tool)`**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +0.6 [-1.2, +2.5] | +0.3 [-0.8, +1.1] | +0.2 [-0.9, +1.4] |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | +0.0 [-2.2, +1.8] | +0.3 [+0.0, +1.0] | -0.1 [-1.3, +0.9] |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | -0.3 [-2.4, +2.1] | +0.0 [+0.0, +0.0] | -0.2 [-1.3, +1.0] |
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | -0.3 [-2.3, +2.4] | +0.0 [+0.0, +0.0] | -0.0 [-1.1, +1.4] |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | -0.6 [-3.0, +2.2] | +0.0 [+0.0, +0.0] | -0.3 [-1.5, +1.1] |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | -0.6 [-2.3, +1.3] | +0.0 [+0.0, +0.0] | -0.4 [-1.3, +0.5] |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | -0.9 [-2.5, +1.2] | +0.0 [+0.0, +0.0] | -0.6 [-1.4, +0.5] |
| AgentDup lexical, LR | -1.2 [-3.2, +1.0] | +0.0 [-0.8, +0.9] | -0.7 [-1.9, +0.5] |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | -1.2 [-2.9, +0.8] | +0.0 [+0.0, +0.0] | -0.7 [-1.6, +0.3] |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | -1.5 [-3.4, +0.9] | +0.0 [+0.0, +0.0] | -0.7 [-1.7, +0.5] |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | -1.8 [-4.3, +0.4] | +0.3 [+0.0, +1.0] | -1.0 [-2.3, +0.2] |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | -2.0 [-3.9, +0.5] | +0.0 [+0.0, +0.0] | -1.0 [-2.0, +0.3] |
| All signals, gradient boosting | -2.3 [-5.5, +1.2] | -1.2 [-2.6, +0.4] | -1.7 [-4.0, +0.6] |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | -2.6 [-4.9, +0.0] | +0.0 [+0.0, +0.0] | -1.5 [-2.7, -0.0]* |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | -2.9 [-5.5, -0.3]* | +0.0 [-0.8, +0.9] | -1.5 [-2.8, -0.0]* |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | -2.9 [-5.5, +0.7] | +0.0 [+0.0, +0.0] | -1.7 [-3.2, +0.4] |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | -3.2 [-8.4, +1.4] | -0.6 [-3.1, +1.4] | -2.0 [-5.7, +0.9] |
| AgentDup features, gradient boosting | -3.5 [-6.8, +0.0] | -1.5 [-4.3, +0.4] | -2.5 [-5.0, +0.2] |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | -4.7 [-7.2, -1.1]* | +0.0 [+0.0, +0.0] | -2.7 [-4.2, -0.6]* |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | -5.0 [-7.6, -1.3]* | -0.3 [-1.5, +0.9] | -2.8 [-4.4, -0.7]* |
| LLM judge Claude Haiku 4.5 re-rank top-5 | -5.8 [-9.0, -1.2]* | +0.0 [+0.0, +0.0] | -3.0 [-4.8, -0.4]* |
| Links only (same issue / #ref) | -6.1 [-10.9, -0.4]* | -4.7 [-9.0, -0.7]* | -5.0 [-9.2, -0.5]* |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | -6.1 [-8.8, -3.1]* | +0.0 [+0.0, +0.0] | -3.3 [-4.8, -1.6]* |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | -8.5 [-13.7, -3.7]* | -1.8 [-3.5, -0.4]* | -5.6 [-8.9, -2.6]* |
| INTRUDE + time (Wang et al. 2019), LR | -9.1 [-13.1, -5.0]* | -1.8 [-5.2, +0.9] | -5.9 [-9.3, -2.7]* |
| LLM judge Qwen2.5-7B re-rank top-5 | -9.1 [-13.1, -4.9]* | +0.0 [+0.0, +0.0] | -5.6 [-8.1, -3.2]* |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | -9.6 [-14.8, -5.2]* | -0.6 [-1.8, +0.5] | -5.5 [-8.4, -2.9]* |
| LLM judge Qwen2.5-7B re-rank top-10 | -10.8 [-14.7, -6.7]* | -2.9 [-5.9, -1.0]* | -7.4 [-10.3, -4.9]* |
| contrib-guard/phoenix (bot, exact port) | -12.3 [-17.0, -6.8]* | -5.3 [-9.7, -1.2]* | -9.0 [-13.4, -4.8]* |
| BGE-small template-stripped | -13.7 [-19.0, -8.3]* | -5.6 [-11.2, -1.2]* | -10.2 [-14.9, -6.0]* |
| TF-IDF template-stripped | -14.0 [-19.0, -8.2]* | -4.1 [-7.7, -0.7]* | -9.8 [-14.0, -5.4]* |
| BGE-base template-stripped | -14.0 [-19.7, -8.4]* | -6.1 [-12.2, -1.5]* | -10.4 [-15.5, -6.0]* |
| RRF hybrid: BM25 + embedding + code | -14.3 [-20.7, -7.8]* | -5.0 [-9.8, -0.9]* | -10.2 [-15.5, -5.2]* |
| TF-IDF raw text (Li et al. 2017) | -14.3 [-19.2, -8.5]* | -5.0 [-8.8, -1.3]* | -10.0 [-14.3, -5.7]* |
| BGE-small raw text | -14.9 [-20.2, -9.0]* | -5.0 [-10.5, -0.7]* | -10.9 [-15.3, -6.5]* |
| MiniLM template-stripped | -14.9 [-20.5, -8.5]* | -7.3 [-12.7, -3.2]* | -11.2 [-16.0, -6.7]* |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -15.2 [-19.9, -10.5]* | -1.8 [-3.4, -0.3]* | -9.1 [-11.8, -6.3]* |
| BM25 template-stripped | -16.4 [-21.6, -11.2]* | -6.1 [-10.6, -1.7]* | -11.8 [-16.3, -7.3]* |
| RRF hybrid: BM25 + embedding | -16.7 [-21.4, -11.2]* | -6.1 [-10.9, -1.4]* | -11.6 [-15.8, -7.0]* |
| MiniLM raw text | -17.5 [-22.9, -11.6]* | -6.4 [-12.2, -2.1]* | -12.6 [-17.5, -8.2]* |
| Simili-bot (bot, re-impl) | -17.5 [-23.2, -11.2]* | -7.9 [-13.4, -3.6]* | -12.8 [-17.9, -8.2]* |
| RRF hybrid: text + code + links + recency | -18.7 [-28.2, -9.7]* | -5.3 [-8.8, -1.3]* | -13.1 [-19.9, -6.4]* |
| PRSense (bot, re-impl) | -19.0 [-27.8, -10.1]* | -10.5 [-17.9, -3.9]* | -14.8 [-22.8, -7.4]* |
| BM25 raw text | -19.0 [-24.5, -13.6]* | -7.3 [-12.0, -2.5]* | -13.6 [-17.9, -9.1]* |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -19.3 [-25.9, -12.5]* | -3.2 [-6.9, -0.3]* | -12.3 [-16.9, -7.8]* |
| UniXcoder template-stripped text | -26.3 [-33.5, -17.7]* | -15.5 [-22.1, -7.8]* | -21.3 [-27.7, -13.7]* |
| BM25 on diff | -31.6 [-40.2, -22.3]* | -19.0 [-29.5, -9.6]* | -25.5 [-34.6, -16.5]* |
| Code overlap sum (files+hunks+lines) | -32.5 [-39.9, -24.3]* | -17.5 [-26.6, -9.9]* | -25.9 [-33.4, -18.9]* |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -33.3 [-39.4, -26.6]* | +0.0 [+0.0, +0.0] | -20.0 [-23.2, -16.0]* |
| Jina code embeddings v2 on diff | -38.0 [-47.2, -25.9]* | -27.5 [-37.2, -16.6]* | -32.4 [-41.4, -21.2]* |
| BGE-small on diff | -38.6 [-47.6, -27.2]* | -27.5 [-37.5, -15.8]* | -33.2 [-42.1, -22.3]* |
| Hunk overlap | -38.9 [-46.9, -29.6]* | -21.1 [-28.9, -13.1]* | -31.6 [-39.3, -23.6]* |
| Changed-files Jaccard | -38.9 [-45.8, -30.9]* | -23.7 [-32.3, -15.4]* | -31.5 [-38.6, -24.1]* |
| Cross-encoder BGE-reranker-base re-rank top-10 | -39.8 [-47.5, -31.7]* | -9.6 [-13.8, -6.5]* | -28.1 [-33.4, -22.5]* |
| Identical changed lines | -42.1 [-48.6, -33.8]* | -26.3 [-33.4, -16.9]* | -35.5 [-41.5, -27.5]* |
| UniXcoder (code model) on diff | -42.4 [-51.4, -30.6]* | -33.0 [-43.8, -19.4]* | -37.4 [-47.0, -25.1]* |
| MiniLM on diff | -42.4 [-50.7, -31.9]* | -30.7 [-41.2, -17.4]* | -36.7 [-45.4, -25.9]* |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -45.9 [-52.1, -38.8]* | -10.2 [-13.5, -6.7]* | -30.9 [-34.7, -26.4]* |
| CodeBERT (mean-pooled) on diff | -52.0 [-60.9, -41.0]* | -45.9 [-57.1, -32.0]* | -48.5 [-58.2, -36.5]* |
| Recency only (newest open PR first) | -70.8 [-77.3, -61.9]* | -52.0 [-63.9, -36.8]* | -61.7 [-69.9, -51.1]* |

**vs `INTRUDE + time (Wang et al. 2019), LR`**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +9.6 [+5.6, +13.4]* | +2.0 [-0.8, +5.3] | +6.2 [+2.9, +9.1]* |
| AgentDup + MiniLM, LR (current tool) | +9.1 [+5.0, +13.1]* | +1.8 [-0.9, +5.2] | +5.9 [+2.7, +9.3]* |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | +9.1 [+4.3, +13.1]* | +2.0 [-0.6, +5.4] | +5.8 [+2.3, +9.1]* |
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | +8.8 [+5.2, +13.2]* | +1.8 [-0.9, +5.2] | +5.9 [+3.0, +9.5]* |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | +8.8 [+4.8, +12.8]* | +1.8 [-0.9, +5.2] | +5.7 [+2.6, +8.8]* |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | +8.5 [+4.3, +12.6]* | +1.8 [-0.9, +5.2] | +5.5 [+2.2, +8.8]* |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | +8.5 [+4.3, +12.8]* | +1.8 [-0.9, +5.2] | +5.7 [+2.6, +8.9]* |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | +8.2 [+4.2, +12.4]* | +1.8 [-0.9, +5.2] | +5.4 [+2.2, +8.8]* |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | +7.9 [+3.8, +12.0]* | +1.8 [-0.9, +5.2] | +5.2 [+2.0, +8.6]* |
| AgentDup lexical, LR | +7.9 [+3.7, +12.7]* | +1.8 [-0.8, +5.0] | +5.2 [+1.9, +9.1]* |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | +7.6 [+4.1, +11.2]* | +1.8 [-0.9, +5.2] | +5.2 [+2.3, +8.3]* |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | +7.3 [+2.3, +11.4]* | +2.0 [-0.6, +5.4] | +5.0 [+1.5, +8.1]* |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | +7.0 [+3.6, +10.7]* | +1.8 [-0.9, +5.2] | +4.9 [+2.0, +8.1]* |
| All signals, gradient boosting | +6.7 [+3.2, +10.8]* | +0.6 [-1.6, +3.2] | +4.2 [+1.6, +7.0]* |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | +6.4 [+3.0, +9.9]* | +1.8 [-0.9, +5.2] | +4.5 [+1.7, +7.3]* |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | +6.1 [+2.3, +10.7]* | +1.8 [-0.9, +5.2] | +4.3 [+1.2, +7.8]* |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | +6.1 [+1.6, +10.5]* | +1.8 [-0.7, +4.9] | +4.5 [+1.2, +7.7]* |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | +5.8 [+0.0, +11.2] | +1.2 [-2.5, +5.3] | +3.9 [-0.8, +8.2] |
| AgentDup features, gradient boosting | +5.6 [+1.9, +9.6]* | +0.3 [-1.6, +2.5] | +3.5 [+1.0, +6.2]* |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | +4.4 [+0.6, +9.0]* | +1.8 [-0.9, +5.2] | +3.3 [+0.3, +6.8]* |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | +4.1 [+0.5, +8.2]* | +1.5 [-1.6, +5.1] | +3.2 [+0.2, +6.5]* |
| LLM judge Claude Haiku 4.5 re-rank top-5 | +3.2 [-0.4, +8.3] | +1.8 [-0.9, +5.2] | +3.0 [+0.1, +6.7]* |
| Links only (same issue / #ref) | +2.9 [-1.1, +7.8] | -2.9 [-5.8, +0.7] | +0.9 [-1.9, +4.2] |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | +2.9 [-0.9, +7.0] | +1.8 [-0.9, +5.2] | +2.6 [-0.4, +6.0] |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | +0.6 [-4.1, +4.8] | +0.0 [-3.2, +3.6] | +0.3 [-2.9, +2.9] |
| LLM judge Qwen2.5-7B re-rank top-5 | +0.0 [-4.9, +5.0] | +1.8 [-0.9, +5.2] | +0.4 [-3.3, +4.1] |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | -0.6 [-4.8, +2.9] | +1.2 [-1.6, +4.4] | +0.5 [-2.0, +2.6] |
| LLM judge Qwen2.5-7B re-rank top-10 | -1.8 [-6.1, +2.4] | -1.2 [-4.4, +2.0] | -1.5 [-5.0, +1.4] |
| contrib-guard/phoenix (bot, exact port) | -3.2 [-7.0, +1.1] | -3.5 [-6.5, -0.5]* | -3.0 [-5.9, +0.0] |
| BGE-small template-stripped | -4.7 [-9.5, +0.4] | -3.8 [-7.2, -0.8]* | -4.3 [-8.2, -0.6]* |
| TF-IDF template-stripped | -5.0 [-8.6, -1.0]* | -2.3 [-4.5, +0.0] | -3.8 [-6.5, -1.0]* |
| BGE-base template-stripped | -5.0 [-9.8, +0.0] | -4.4 [-8.0, -1.3]* | -4.4 [-8.2, -0.8]* |
| RRF hybrid: BM25 + embedding + code | -5.3 [-11.4, +0.6] | -3.2 [-6.2, +0.3] | -4.2 [-9.0, +0.1] |
| TF-IDF raw text (Li et al. 2017) | -5.3 [-8.9, -1.3]* | -3.2 [-5.8, -0.6]* | -4.1 [-6.8, -1.3]* |
| BGE-small raw text | -5.8 [-10.6, -0.5]* | -3.2 [-6.9, +0.0] | -5.0 [-8.7, -1.2]* |
| MiniLM template-stripped | -5.8 [-10.0, -0.6]* | -5.6 [-8.7, -3.0]* | -5.3 [-8.7, -1.8]* |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -6.1 [-10.9, -1.8]* | +0.0 [-3.0, +3.8] | -3.1 [-6.6, -0.0]* |
| BM25 template-stripped | -7.3 [-11.9, -2.6]* | -4.4 [-7.7, -0.3]* | -5.8 [-9.3, -2.1]* |
| RRF hybrid: BM25 + embedding | -7.6 [-11.9, -2.8]* | -4.4 [-7.6, -0.5]* | -5.7 [-8.9, -2.1]* |
| MiniLM raw text | -8.5 [-12.5, -4.0]* | -4.7 [-8.4, -1.8]* | -6.6 [-10.0, -3.5]* |
| Simili-bot (bot, re-impl) | -8.5 [-13.2, -3.1]* | -6.1 [-9.3, -3.4]* | -6.9 [-10.6, -3.3]* |
| RRF hybrid: text + code + links + recency | -9.6 [-18.6, -1.6]* | -3.5 [-6.6, +0.4] | -7.1 [-13.7, -1.3]* |
| PRSense (bot, re-impl) | -9.9 [-18.2, -2.0]* | -8.8 [-15.3, -3.3]* | -8.9 [-16.6, -2.5]* |
| BM25 raw text | -9.9 [-14.8, -5.1]* | -5.6 [-9.4, -1.1]* | -7.6 [-11.2, -3.8]* |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -10.2 [-16.9, -3.9]* | -1.5 [-6.0, +2.8] | -6.3 [-11.6, -1.5]* |
| UniXcoder template-stripped text | -17.3 [-23.8, -9.5]* | -13.7 [-20.0, -6.6]* | -15.3 [-21.2, -8.4]* |
| BM25 on diff | -22.5 [-31.0, -13.6]* | -17.3 [-27.5, -8.5]* | -19.5 [-28.3, -11.2]* |
| Code overlap sum (files+hunks+lines) | -23.4 [-30.9, -16.3]* | -15.8 [-25.1, -7.7]* | -20.0 [-27.8, -13.5]* |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -24.3 [-31.2, -16.8]* | +1.8 [-0.9, +5.2] | -14.0 [-18.3, -9.0]* |
| Jina code embeddings v2 on diff | -28.9 [-38.1, -17.9]* | -25.7 [-35.5, -15.3]* | -26.4 [-35.6, -16.3]* |
| BGE-small on diff | -29.5 [-38.5, -19.1]* | -25.7 [-36.1, -14.1]* | -27.2 [-36.3, -17.2]* |
| Hunk overlap | -29.8 [-37.9, -21.4]* | -19.3 [-27.5, -10.8]* | -25.7 [-33.4, -18.0]* |
| Changed-files Jaccard | -29.8 [-36.5, -22.8]* | -21.9 [-31.1, -13.9]* | -25.6 [-32.7, -19.0]* |
| Cross-encoder BGE-reranker-base re-rank top-10 | -30.7 [-39.4, -22.6]* | -7.9 [-12.9, -3.4]* | -22.1 [-28.4, -16.4]* |
| Identical changed lines | -33.0 [-38.8, -25.8]* | -24.6 [-32.2, -15.1]* | -29.5 [-35.2, -22.2]* |
| UniXcoder (code model) on diff | -33.3 [-42.4, -22.3]* | -31.3 [-42.6, -17.7]* | -31.5 [-41.1, -19.9]* |
| MiniLM on diff | -33.3 [-41.4, -24.1]* | -28.9 [-39.7, -16.1]* | -30.8 [-39.2, -21.0]* |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -36.8 [-43.0, -30.6]* | -8.5 [-12.4, -3.6]* | -24.9 [-28.9, -20.7]* |
| CodeBERT (mean-pooled) on diff | -43.0 [-51.6, -33.0]* | -44.2 [-55.9, -30.0]* | -42.5 [-52.3, -31.1]* |
| Recency only (newest open PR first) | -61.7 [-68.7, -52.0]* | -50.3 [-63.0, -34.0]* | -55.7 [-64.5, -44.3]* |

**vs `contrib-guard/phoenix (bot, exact port)`**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +12.9 [+7.5, +17.3]* | +5.6 [+1.2, +10.0]* | +9.2 [+5.1, +13.1]* |
| AgentDup + MiniLM, LR (current tool) | +12.3 [+6.8, +17.0]* | +5.3 [+1.2, +9.7]* | +9.0 [+4.8, +13.4]* |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | +12.3 [+5.8, +17.6]* | +5.6 [+1.5, +10.0]* | +8.8 [+4.2, +13.3]* |
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | +12.0 [+6.7, +17.3]* | +5.3 [+1.2, +9.7]* | +8.9 [+5.0, +13.7]* |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | +12.0 [+6.6, +17.0]* | +5.3 [+1.2, +9.7]* | +8.7 [+4.7, +13.0]* |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | +11.7 [+6.3, +16.5]* | +5.3 [+1.2, +9.7]* | +8.5 [+4.2, +13.1]* |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | +11.7 [+6.5, +16.7]* | +5.3 [+1.2, +9.7]* | +8.7 [+4.8, +13.0]* |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | +11.4 [+6.2, +16.2]* | +5.3 [+1.2, +9.7]* | +8.4 [+4.2, +13.0]* |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | +11.1 [+5.9, +15.9]* | +5.3 [+1.2, +9.7]* | +8.3 [+4.1, +12.7]* |
| AgentDup lexical, LR | +11.1 [+5.4, +16.7]* | +5.3 [+1.2, +9.7]* | +8.2 [+3.9, +13.2]* |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | +10.8 [+6.0, +15.2]* | +5.3 [+1.2, +9.7]* | +8.2 [+4.3, +12.5]* |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | +10.5 [+4.3, +15.8]* | +5.6 [+1.5, +10.0]* | +8.0 [+3.5, +12.2]* |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | +10.2 [+5.5, +14.8]* | +5.3 [+1.2, +9.7]* | +7.9 [+4.1, +12.3]* |
| All signals, gradient boosting | +9.9 [+6.0, +13.8]* | +4.1 [+0.6, +8.0]* | +7.3 [+4.2, +10.4]* |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | +9.6 [+4.9, +13.9]* | +5.3 [+1.2, +9.7]* | +7.5 [+3.8, +11.5]* |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | +9.4 [+5.2, +13.8]* | +5.3 [+1.2, +9.7]* | +7.3 [+3.6, +11.9]* |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | +9.4 [+3.6, +14.8]* | +5.3 [+1.2, +9.8]* | +7.5 [+3.3, +11.8]* |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | +9.1 [+3.3, +14.5]* | +4.7 [-0.3, +10.0] | +6.9 [+1.9, +12.1]* |
| AgentDup features, gradient boosting | +8.8 [+4.7, +12.6]* | +3.8 [+0.8, +6.9]* | +6.5 [+3.7, +9.5]* |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | +7.6 [+3.3, +12.6]* | +5.3 [+1.2, +9.7]* | +6.3 [+2.6, +11.1]* |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | +7.3 [+3.3, +11.8]* | +5.0 [+0.6, +9.7]* | +6.2 [+2.6, +10.6]* |
| LLM judge Claude Haiku 4.5 re-rank top-5 | +6.4 [+1.6, +12.2]* | +5.3 [+1.2, +9.7]* | +6.0 [+2.3, +10.9]* |
| Links only (same issue / #ref) | +6.1 [+1.9, +11.3]* | +0.6 [-0.7, +2.3] | +3.9 [+1.5, +6.8]* |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | +6.1 [+0.7, +11.1]* | +5.3 [+1.2, +9.7]* | +5.7 [+1.6, +10.1]* |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | +3.8 [-1.9, +8.9] | +3.5 [-0.4, +8.0] | +3.3 [-0.2, +6.4] |
| INTRUDE + time (Wang et al. 2019), LR | +3.2 [-1.1, +7.0] | +3.5 [+0.5, +6.5]* | +3.0 [-0.0, +5.9] |
| LLM judge Qwen2.5-7B re-rank top-5 | +3.2 [-3.3, +9.5] | +5.3 [+1.2, +9.7]* | +3.4 [-1.5, +8.6] |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | +2.6 [-2.3, +6.7] | +4.7 [+0.4, +9.4]* | +3.5 [+0.0, +6.5]* |
| LLM judge Qwen2.5-7B re-rank top-10 | +1.5 [-4.5, +6.7] | +2.3 [-2.7, +7.2] | +1.5 [-3.2, +6.0] |
| BGE-small template-stripped | -1.5 [-5.6, +2.1] | -0.3 [-3.8, +2.9] | -1.3 [-4.6, +1.6] |
| TF-IDF template-stripped | -1.8 [-5.1, +1.8] | +1.2 [-0.3, +3.1] | -0.8 [-2.8, +1.2] |
| BGE-base template-stripped | -1.8 [-5.9, +1.6] | -0.9 [-4.9, +2.7] | -1.4 [-4.3, +1.1] |
| RRF hybrid: BM25 + embedding + code | -2.0 [-7.6, +2.7] | +0.3 [-3.1, +3.8] | -1.2 [-5.5, +2.5] |
| TF-IDF raw text (Li et al. 2017) | -2.0 [-5.6, +1.5] | +0.3 [-1.1, +1.7] | -1.1 [-3.1, +0.9] |
| BGE-small raw text | -2.6 [-6.5, +0.8] | +0.3 [-3.4, +3.6] | -1.9 [-4.7, +0.5] |
| MiniLM template-stripped | -2.6 [-5.5, +0.6] | -2.0 [-5.5, +0.8] | -2.3 [-4.5, +0.0] |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -2.9 [-8.7, +1.5] | +3.5 [-0.5, +8.4] | -0.1 [-4.4, +3.8] |
| BM25 template-stripped | -4.1 [-8.6, -0.5]* | -0.9 [-3.1, +1.6] | -2.8 [-5.4, -0.4]* |
| RRF hybrid: BM25 + embedding | -4.4 [-7.7, -1.5]* | -0.9 [-2.8, +1.7] | -2.7 [-4.4, -0.8]* |
| MiniLM raw text | -5.3 [-8.3, -2.4]* | -1.2 [-4.4, +1.6] | -3.6 [-5.9, -1.5]* |
| Simili-bot (bot, re-impl) | -5.3 [-8.7, -2.0]* | -2.6 [-5.9, +0.3] | -3.9 [-6.5, -1.5]* |
| RRF hybrid: text + code + links + recency | -6.4 [-15.1, +1.0] | +0.0 [-3.8, +4.5] | -4.1 [-10.6, +1.5] |
| PRSense (bot, re-impl) | -6.7 [-14.2, +0.4] | -5.3 [-12.7, +1.2] | -5.9 [-13.2, +0.4] |
| BM25 raw text | -6.7 [-12.2, -2.7]* | -2.0 [-4.6, +0.7] | -4.6 [-7.8, -1.9]* |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -7.0 [-13.1, -1.5]* | +2.0 [-3.5, +7.4] | -3.3 [-8.6, +1.5] |
| UniXcoder template-stripped text | -14.0 [-19.1, -8.5]* | -10.2 [-15.7, -4.1]* | -12.3 [-17.1, -7.1]* |
| BM25 on diff | -19.3 [-27.1, -11.1]* | -13.7 [-24.7, -4.7]* | -16.5 [-25.3, -8.5]* |
| Code overlap sum (files+hunks+lines) | -20.2 [-27.5, -13.1]* | -12.3 [-22.4, -2.9]* | -17.0 [-25.1, -9.7]* |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -21.1 [-28.2, -13.1]* | +5.3 [+1.2, +9.7]* | -11.0 [-16.0, -4.9]* |
| Jina code embeddings v2 on diff | -25.7 [-33.7, -16.0]* | -22.2 [-32.2, -11.8]* | -23.4 [-32.0, -13.6]* |
| BGE-small on diff | -26.3 [-34.2, -17.0]* | -22.2 [-33.1, -10.6]* | -24.2 [-33.1, -14.5]* |
| Hunk overlap | -26.6 [-34.5, -18.7]* | -15.8 [-25.1, -6.3]* | -22.6 [-30.7, -14.6]* |
| Changed-files Jaccard | -26.6 [-33.6, -19.9]* | -18.4 [-28.1, -9.4]* | -22.6 [-29.9, -15.7]* |
| Cross-encoder BGE-reranker-base re-rank top-10 | -27.5 [-37.9, -17.9]* | -4.4 [-10.5, +1.2] | -19.1 [-26.4, -12.3]* |
| Identical changed lines | -29.8 [-36.1, -22.2]* | -21.1 [-29.1, -10.7]* | -26.5 [-32.5, -18.6]* |
| UniXcoder (code model) on diff | -30.1 [-38.1, -20.2]* | -27.8 [-39.0, -14.2]* | -28.5 [-37.5, -17.6]* |
| MiniLM on diff | -30.1 [-37.5, -21.3]* | -25.4 [-36.3, -12.1]* | -27.8 [-36.0, -18.0]* |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -33.6 [-40.3, -26.4]* | -5.0 [-10.4, +1.4] | -21.9 [-26.4, -16.9]* |
| CodeBERT (mean-pooled) on diff | -39.8 [-47.7, -29.8]* | -40.6 [-52.7, -26.4]* | -39.5 [-48.9, -28.2]* |
| Recency only (newest open PR first) | -58.5 [-65.5, -49.0]* | -46.8 [-59.8, -29.5]* | -52.7 [-61.3, -40.5]* |

## 7. False alarms and operating curve

Threshold per fold = median top-1 score of the training folds' cross-author duplicates; alert if the top-1 score is above it. 2,965 PRs with no duplicate.

| Strategy | False-alarm rate [95% CI] | cross-author correct alerts |
|---|---|---|
| AgentDup features, gradient boosting | 1.3% [0.9, 1.9] | 46.2% |
| All signals, LR | 1.6% [1.1, 2.1] | 48.8% |
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 1.8% [1.3, 2.3] | 48.5% |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | 2.4% [1.8, 3.1] | 45.6% |
| All signals, gradient boosting | 2.4% [1.8, 3.2] | 49.7% |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | 2.5% [1.9, 3.0] | 45.9% |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | 2.5% [1.9, 3.0] | 45.9% |
| AgentDup + MiniLM, LR (current tool) | 2.5% [1.9, 3.3] | 47.1% |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | 2.5% [2.0, 3.2] | 46.2% |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | 2.8% [2.2, 3.5] | 45.3% |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | 2.8% [2.2, 3.5] | 45.3% |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | 2.8% [2.2, 3.5] | 46.2% |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 3.1% [2.5, 3.9] | 46.2% |
| AgentDup lexical, LR | 3.2% [2.4, 4.2] | 46.8% |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | 3.7% [3.0, 4.6] | 44.2% |
| Links only (same issue / #ref) | 3.8% [3.0, 4.8] | 46.2% |
| LLM judge Qwen2.5-7B re-rank top-5 | 4.0% [3.2, 4.7] | 43.3% |
| LLM judge Qwen2.5-7B re-rank top-10 | 4.0% [3.3, 4.8] | 43.0% |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | 4.2% [3.5, 5.0] | 44.2% |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | 4.3% [3.5, 5.0] | 43.0% |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | 4.5% [3.7, 5.3] | 45.6% |
| INTRUDE + time (Wang et al. 2019), LR | 4.6% [3.7, 5.7] | 44.2% |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 4.7% [3.9, 5.6] | 45.0% |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | 5.0% [3.9, 6.1] | 44.2% |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | 5.0% [3.9, 6.1] | 44.2% |
| LLM judge Claude Haiku 4.5 re-rank top-5 | 5.4% [4.6, 6.1] | 57.3% |
| BGE-small template-stripped | 6.4% [5.3, 7.5] | 42.1% |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | 6.9% [5.7, 8.0] | 44.7% |
| BGE-small raw text | 6.9% [5.7, 8.1] | 43.3% |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | 6.9% [5.9, 8.1] | 46.8% |
| BGE-base template-stripped | 7.3% [5.9, 8.7] | 43.6% |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | 8.8% [7.6, 9.9] | 45.9% |
| TF-IDF template-stripped | 8.9% [7.4, 10.3] | 42.7% |
| TF-IDF raw text (Li et al. 2017) | 9.4% [7.8, 10.9] | 42.4% |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 10.7% [8.4, 13.1] | 43.0% |
| Simili-bot (bot, re-impl) | 11.1% [9.3, 12.8] | 43.6% |
| contrib-guard/phoenix (bot, exact port) | 11.7% [8.9, 14.6] | 41.8% |
| MiniLM template-stripped | 11.9% [10.1, 13.6] | 43.6% |
| Jina code embeddings v2 on diff | 12.0% [8.9, 16.0] | 33.0% |
| MiniLM raw text | 12.1% [10.2, 13.9] | 42.7% |
| BGE-small on diff | 12.1% [9.5, 15.3] | 32.7% |
| PRSense (bot, re-impl) | 12.7% [10.5, 15.2] | 37.1% |
| Cross-encoder ms-marco MiniLM re-rank top-10 | 13.4% [10.9, 15.9] | 40.9% |
| MiniLM on diff | 15.2% [11.5, 20.2] | 30.1% |
| CodeBERT (mean-pooled) on diff | 15.3% [12.0, 18.7] | 26.0% |
| UniXcoder (code model) on diff | 16.1% [12.9, 19.9] | 29.2% |
| BM25 on diff | 17.5% [13.0, 22.1] | 30.4% |
| RRF hybrid: BM25 + embedding + code | 18.0% [15.3, 21.0] | 49.4% |
| BM25 template-stripped | 18.7% [11.6, 28.3] | 39.8% |
| BM25 raw text | 21.0% [12.8, 32.1] | 38.6% |
| Changed-files Jaccard | 24.4% [20.8, 28.4] | 33.9% |
| LLM judge Qwen2.5-1.5B re-rank top-5 | 24.4% [21.3, 27.5] | 32.5% |
| UniXcoder template-stripped text | 24.8% [19.5, 30.4] | 36.8% |
| Code overlap sum (files+hunks+lines) | 25.1% [21.2, 29.7] | 30.7% |
| LLM judge Qwen2.5-1.5B re-rank top-10 | 25.7% [22.5, 28.9] | 25.7% |
| Hunk overlap | 29.6% [26.0, 32.9] | 26.3% |
| RRF hybrid: text + code + links + recency | 31.7% [26.2, 37.1] | 44.2% |
| Identical changed lines | 32.0% [27.8, 36.5] | 24.3% |
| RRF hybrid: BM25 + embedding | 37.3% [34.0, 40.8] | 62.9% |
| Recency only (newest open PR first) | 44.1% [36.9, 51.4] | 5.6% |
| Cross-encoder BGE-reranker-base re-rank top-10 | 45.1% [42.1, 47.6] | 26.3% |

Share of cross-author duplicates caught with the right top-1 when the threshold is set to give a fixed false-alarm rate:

| Strategy | FAR 1% | FAR 2% | FAR 5% | FAR 10% | FAR 20% |
|---|---|---|---|---|---|
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 31.3% | 49.7% | 71.3% | 82.7% | 86.5% |
| All signals, LR | 40.6% | 56.1% | 70.2% | 77.8% | 83.9% |
| All signals, gradient boosting | 23.4% | 44.7% | 69.0% | 76.9% | 83.0% |
| AgentDup features, gradient boosting | 39.2% | 58.8% | 68.4% | 76.3% | 82.5% |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | 23.1% | 40.4% | 64.0% | 74.9% | 81.3% |
| AgentDup + MiniLM, LR (current tool) | 30.1% | 43.6% | 63.2% | 74.9% | 81.0% |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 23.7% | 33.0% | 62.6% | 73.4% | 83.0% |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | 19.9% | 38.6% | 61.7% | 74.9% | 81.0% |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | 19.9% | 38.6% | 61.7% | 74.9% | 80.7% |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | 19.0% | 42.1% | 59.9% | 69.6% | 81.0% |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | 22.2% | 43.6% | 59.9% | 73.7% | 80.7% |
| AgentDup lexical, LR | 19.0% | 35.4% | 58.8% | 72.2% | 78.7% |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | 28.4% | 42.7% | 57.0% | 74.0% | 80.1% |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | 28.4% | 42.7% | 57.0% | 74.3% | 80.4% |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | 20.5% | 31.3% | 55.3% | 71.6% | 82.7% |
| LLM judge Qwen2.5-7B re-rank top-5 | 14.6% | 24.9% | 50.9% | 62.9% | 72.5% |
| Links only (same issue / #ref) | 22.8% | 33.3% | 50.9% | 58.2% | 68.4% |
| LLM judge Qwen2.5-7B re-rank top-10 | 14.6% | 24.3% | 49.4% | 62.3% | 71.1% |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 17.5% | 26.9% | 48.8% | 58.5% | 69.9% |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | 14.6% | 23.4% | 47.1% | 63.7% | 78.4% |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | 17.3% | 24.0% | 46.8% | 60.5% | 73.4% |
| INTRUDE + time (Wang et al. 2019), LR | 12.9% | 22.2% | 46.5% | 57.6% | 68.4% |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | 17.3% | 23.7% | 46.2% | 58.2% | 71.1% |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | 9.6% | 19.9% | 45.3% | 64.9% | 77.2% |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | 9.6% | 19.9% | 45.3% | 64.9% | 77.2% |
| BGE-small template-stripped | 6.1% | 14.0% | 37.1% | 52.0% | 61.1% |
| BGE-small raw text | 5.8% | 12.6% | 36.5% | 50.3% | 59.6% |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | 5.0% | 15.5% | 36.3% | 52.3% | 66.4% |
| BGE-base template-stripped | 4.1% | 10.2% | 33.3% | 48.8% | 60.2% |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | 5.8% | 14.0% | 33.3% | 58.8% | 78.7% |
| TF-IDF template-stripped | 10.2% | 17.3% | 33.0% | 47.1% | 56.1% |
| TF-IDF raw text (Li et al. 2017) | 10.2% | 15.5% | 32.7% | 46.2% | 55.8% |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | 5.8% | 14.0% | 28.7% | 50.0% | 75.1% |
| Simili-bot (bot, re-impl) | 5.3% | 12.3% | 26.6% | 38.0% | 52.3% |
| MiniLM raw text | 5.0% | 12.3% | 25.7% | 37.1% | 53.8% |
| MiniLM template-stripped | 6.4% | 12.0% | 24.9% | 38.3% | 55.0% |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 6.7% | 13.7% | 24.0% | 39.5% | 53.5% |
| Jina code embeddings v2 on diff | 5.6% | 10.8% | 23.1% | 31.0% | 37.1% |
| PRSense (bot, re-impl) | 7.0% | 11.7% | 22.8% | 34.2% | 48.0% |
| Cross-encoder ms-marco MiniLM re-rank top-10 | 3.5% | 8.8% | 22.5% | 35.1% | 46.2% |
| BGE-small on diff | 2.6% | 9.1% | 22.2% | 29.8% | 36.8% |
| contrib-guard/phoenix (bot, exact port) | 5.0% | 9.6% | 20.8% | 36.8% | 56.1% |
| UniXcoder (code model) on diff | 4.1% | 10.8% | 20.5% | 25.4% | 32.7% |
| MiniLM on diff | 1.2% | 7.9% | 19.3% | 26.9% | 33.0% |
| CodeBERT (mean-pooled) on diff | 5.8% | 9.6% | 18.4% | 24.3% | 27.2% |
| Code overlap sum (files+hunks+lines) | 7.0% | 8.2% | 15.2% | 20.8% | 29.5% |
| LLM judge Qwen2.5-1.5B re-rank top-5 | 4.1% | 7.6% | 14.6% | 19.6% | 29.8% |
| BM25 on diff | 4.4% | 7.3% | 14.0% | 21.9% | 31.9% |
| BM25 template-stripped | 2.9% | 4.1% | 11.7% | 26.9% | 40.9% |
| UniXcoder template-stripped text | 3.5% | 7.9% | 11.4% | 18.1% | 32.5% |
| RRF hybrid: text + code + links + recency | 0.0% | 0.0% | 11.1% | 17.5% | 30.7% |
| BM25 raw text | 2.9% | 3.8% | 10.5% | 23.1% | 37.4% |
| LLM judge Qwen2.5-1.5B re-rank top-10 | 3.5% | 5.8% | 9.4% | 16.1% | 23.7% |
| LLM judge Claude Haiku 4.5 re-rank top-5 | 5.6% | 5.6% | 5.6% | 70.5% | 77.8% |
| Cross-encoder BGE-reranker-base re-rank top-10 | 1.2% | 1.2% | 2.3% | 4.7% | 13.2% |
| Hunk overlap | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Changed-files Jaccard | 0.0% | 0.0% | 0.0% | 17.0% | 27.8% |
| Identical changed lines | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| RRF hybrid: BM25 + embedding | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| RRF hybrid: BM25 + embedding + code | 0.0% | 0.0% | 0.0% | 0.0% | 45.6% |
| Recency only (newest open PR first) | 0.0% | 0.0% | 0.0% | 0.6% | 1.8% |

## 8. Random-pair (classic) evaluation vs live queue

Random-pair AUC = can the method tell the true duplicate from one random other PR in the queue. Live queue = must rank it first among all open PRs.

| Strategy | random-pair AUC | AUC rank | live-queue cross-author R@1 | live rank |
|---|---|---|---|---|
| All signals, LR | 0.991 | 1 | 0.906 | 1 |
| All signals, gradient boosting | 0.989 | 2 | 0.877 | 14 |
| AgentDup + MiniLM, LR (current tool) | 0.986 | 3 | 0.901 | 2 |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-10 | 0.984 | 4 | 0.874 | 15 |
| LLM judge Claude Haiku 4.5 + AgentDup (avg) top-5 | 0.984 | 5 | 0.898 | 4 |
| LLM judge Qwen2.5-Coder-7B + AgentDup (avg) top-5 | 0.984 | 6 | 0.880 | 13 |
| Cascade: AgentDup + Qwen2.5-Coder-7B judge (stacked LR) | 0.984 | 7 | 0.886 | 11 |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-10 | 0.984 | 8 | 0.889 | 9 |
| LLM judge Qwen2.5-7B + AgentDup (avg) top-5 | 0.983 | 9 | 0.892 | 8 |
| AgentDup lexical, LR | 0.983 | 10 | 0.889 | 9 |
| LLM judge Claude Haiku 4.5 re-rank top-5 | 0.982 | 11 | 0.842 | 22 |
| Cascade: AgentDup + Qwen2.5-7B judge (stacked LR) | 0.982 | 12 | 0.895 | 6 |
| Cross-encoder BGE-reranker-v2-m3 + AgentDup (avg) top-10 | 0.982 | 13 | 0.871 | 16 |
| AgentDup features, gradient boosting | 0.982 | 14 | 0.865 | 19 |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.982 | 15 | 0.804 | 28 |
| Cascade: AgentDup + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.982 | 16 | 0.901 | 2 |
| Cascade: AgentDup + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.981 | 17 | 0.898 | 4 |
| Cascade: AgentDup + fine-tuned BGE-reranker (stacked LR) | 0.981 | 18 | 0.895 | 6 |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.981 | 19 | 0.839 | 23 |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-5 | 0.981 | 20 | 0.854 | 20 |
| LLM judge Qwen2.5-1.5B + AgentDup (avg) top-10 | 0.981 | 21 | 0.851 | 21 |
| Cascade: AgentDup + BGE-reranker-base (stacked LR) | 0.979 | 22 | 0.883 | 12 |
| Cross-encoder BGE-reranker-base + AgentDup (avg) top-10 | 0.978 | 23 | 0.871 | 16 |
| Cross-encoder ms-marco MiniLM + AgentDup (avg) top-10 | 0.978 | 24 | 0.868 | 18 |
| LLM judge Qwen2.5-7B re-rank top-5 | 0.975 | 25 | 0.810 | 26 |
| INTRUDE + time (Wang et al. 2019), LR | 0.974 | 26 | 0.810 | 26 |
| LLM judge Qwen2.5-7B re-rank top-10 | 0.972 | 27 | 0.792 | 29 |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.968 | 28 | 0.816 | 25 |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.968 | 29 | 0.749 | 38 |
| Simili-bot (bot, re-impl) | 0.960 | 30 | 0.725 | 41 |
| Links only (same issue / #ref) | 0.959 | 31 | 0.839 | 23 |
| MiniLM raw text | 0.958 | 32 | 0.725 | 41 |
| BGE-small raw text | 0.958 | 33 | 0.751 | 36 |
| BGE-small template-stripped | 0.958 | 34 | 0.763 | 31 |
| MiniLM template-stripped | 0.958 | 35 | 0.751 | 36 |
| TF-IDF template-stripped | 0.957 | 36 | 0.760 | 32 |
| BGE-base template-stripped | 0.957 | 37 | 0.760 | 32 |
| TF-IDF raw text (Li et al. 2017) | 0.955 | 38 | 0.757 | 34 |
| PRSense (bot, re-impl) | 0.953 | 39 | 0.711 | 44 |
| contrib-guard/phoenix (bot, exact port) | 0.952 | 40 | 0.778 | 30 |
| Cross-encoder ms-marco MiniLM re-rank top-10 | 0.951 | 41 | 0.708 | 46 |
| LLM judge Qwen2.5-1.5B re-rank top-5 | 0.938 | 42 | 0.567 | 50 |
| RRF hybrid: BM25 + embedding | 0.937 | 43 | 0.734 | 40 |
| LLM judge Qwen2.5-1.5B re-rank top-10 | 0.923 | 44 | 0.442 | 59 |
| RRF hybrid: BM25 + embedding + code | 0.910 | 45 | 0.757 | 34 |
| Code overlap sum (files+hunks+lines) | 0.904 | 46 | 0.576 | 49 |
| Cross-encoder BGE-reranker-base re-rank top-10 | 0.893 | 47 | 0.503 | 55 |
| BM25 template-stripped | 0.891 | 48 | 0.737 | 39 |
| Hunk overlap | 0.886 | 49 | 0.512 | 53 |
| BM25 raw text | 0.885 | 50 | 0.711 | 44 |
| Changed-files Jaccard | 0.873 | 51 | 0.512 | 53 |
| BM25 on diff | 0.869 | 52 | 0.585 | 48 |
| RRF hybrid: text + code + links + recency | 0.850 | 53 | 0.713 | 43 |
| Jina code embeddings v2 on diff | 0.844 | 54 | 0.520 | 51 |
| BGE-small on diff | 0.842 | 55 | 0.515 | 52 |
| UniXcoder template-stripped text | 0.841 | 56 | 0.637 | 47 |
| Identical changed lines | 0.838 | 57 | 0.480 | 56 |
| MiniLM on diff | 0.805 | 58 | 0.477 | 57 |
| UniXcoder (code model) on diff | 0.781 | 59 | 0.477 | 57 |
| CodeBERT (mean-pooled) on diff | 0.653 | 60 | 0.380 | 60 |
| Recency only (newest open PR first) | 0.641 | 61 | 0.193 | 61 |

## 9. Latency and cost

| Component | Hardware | Numbers |
|---|---|---|
| lexical features ms/query | CPU | {"median": 22.004112499416806, "p90": 228.5285644975381} |
| cpu_rerankers | CPU | {"cross-encoder/ms-marco-MiniLM-L6-v2": {"cpu_threads": 4, "pairs": 200, "ms_per_pair": 45.7, "ms_per_query_top10": 457.5}, "BAAI/bge-reranker-base": {"cpu_threads": 4, "pairs": 200, "ms_per_pair": 286.1, "ms_per_query_top10": 2861.4}} |
| gpu_bge_diff | L4 | {"tag": "bge_diff", "model": "BAAI/bge-small-en-v1.5", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 144.0, "ms_per_pr_gpu": 1.89} |
| gpu_bge_raw | L4 | {"tag": "bge_raw", "model": "BAAI/bge-small-en-v1.5", "variant": "raw", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 125.0, "ms_per_pr_gpu": 1.64} |
| gpu_bge_stripped | L4 | {"tag": "bge_stripped", "model": "BAAI/bge-small-en-v1.5", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 120.7, "ms_per_pr_gpu": 1.583} |
| gpu_bgebase_stripped | L4 | {"tag": "bgebase_stripped", "model": "BAAI/bge-base-en-v1.5", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 244.3, "ms_per_pr_gpu": 3.205} |
| gpu_ce_bgebase | L4 | {"tag": "ce_bgebase", "model": "BAAI/bge-reranker-base", "pairs": 43591, "gpu": "L4", "seconds": 137.5, "ms_per_pair_gpu": 3.154} |
| gpu_ce_bgem3 | L4 | {"tag": "ce_bgem3", "model": "BAAI/bge-reranker-v2-m3", "pairs": 43591, "gpu": "L4", "seconds": 445.7, "ms_per_pair_gpu": 10.224} |
| gpu_ce_msmarco | L4 | {"tag": "ce_msmarco", "model": "cross-encoder/ms-marco-MiniLM-L6-v2", "pairs": 43591, "gpu": "L4", "seconds": 41.6, "ms_per_pair_gpu": 0.954} |
| gpu_codebert_diff | L4 | {"tag": "codebert_diff", "model": "microsoft/codebert-base", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 262.1, "ms_per_pr_gpu": 3.44} |
| gpu_finetune_bgebase | L4 | {"gpu": "L4", "folds": [{"fold": 0, "base": "BAAI/bge-reranker-base", "train_pairs": 34896, "test_pairs": 8695, "train_s": 678.1, "predict_s": 121.0}, {"fold": 1, "base": "BAAI/bge-reranker-base", "train_pairs": 34892, "test_pairs": 8699, "train_s": 668.5, "predict_s": 120.4}, {"fold": 2, "base": "BAAI/bge-reranker-base", "train_pairs": 34821, "test_pairs": 8770, "train_s": 668.3, "predict_s": 121.9}, {"fold": 3, "base": "BAAI/bge-reranker-base", "train_pairs": 34868, "test_pairs": 8723, "train_s": 668.1, "predict_s": 118.9}, {"fold": 4, "base": "BAAI/bge-reranker-base", "train_pairs": 34887, "test_pairs": 8704, "train_s": 674.0, "predict_s": 121.1}], "train_s_total": 3357.0, "predict_ms_per_pair_gpu": 13.84} |
| gpu_jinacode_diff | L4 | {"tag": "jinacode_diff", "model": "jinaai/jina-embeddings-v2-base-code", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 620.2, "ms_per_pr_gpu": 8.138} |
| gpu_qwen15 | L40S | {"tag": "qwen15", "model": "Qwen/Qwen2.5-1.5B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 687.2, "ms_per_pair_gpu_batched": 15.766, "prompt_tokens_total": 49530439} |
| gpu_qwen7 | L40S | {"tag": "qwen7", "model": "Qwen/Qwen2.5-7B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 2567.3, "ms_per_pair_gpu_batched": 58.895, "prompt_tokens_total": 49530439} |
| gpu_qwencoder7 | L40S | {"tag": "qwencoder7", "model": "Qwen/Qwen2.5-Coder-7B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 2478.3, "ms_per_pair_gpu_batched": 56.854, "prompt_tokens_total": 49530439} |
| gpu_unix_diff | L4 | {"tag": "unix_diff", "model": "microsoft/unixcoder-base", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 284.0, "ms_per_pr_gpu": 3.727} |
| gpu_unix_stripped | L4 | {"tag": "unix_stripped", "model": "microsoft/unixcoder-base", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 247.7, "ms_per_pr_gpu": 3.251} |
| claude haiku45 API |  | {"pairs": 4587, "ms/pair median": 912.8988000011304, "ms/pair p90": 977.3896139959106, "model": "claude-haiku-4-5", "usd": 7.252751, "budget": 15.0} |

Modal billing for app `agentdup-study`: {"source": "modal billing report --start 2026-11-10 -r h --show-resources, app agentdup-study, hours up to 2026-11-10T23:00Z (Qwen2.5-14B still running after that)", "by_resource_usd": {"Network Egress": 0.077, "Memory": 0.312, "L40S": 4.82, "CPU": 0.28, "L4": 1.401}, "total_usd": 6.89}

## 10. Error analysis (current AgentDup tool, cross-author pairs it does not rank first)

34 of 342 cross-author queries are missed at rank 1.

| By class | misses |
|---|---|
| B. partial code overlap | 17 |
| D. no shared files (intent-level) | 10 |
| A. code twin (>=50% identical changed lines) | 4 |
| C. same files, different code | 3 |

Top-1 was a PR by the *same author as the new PR* in 44% of misses (the author's own other open work). Median queue size of misses: 104. Full list: `experiments/results/errors_cross_author.csv`.

## 11. Limitations

- Silver labels from comments; no new human labels. The 142 hand-labelled duplicates in the 600-PR AIDev sample have no partner PR and could not be used for ranking.
- Agent-vs-human duplicates are not covered.
- PRSense, Simili, vector-triage and PRism are local re-implementations with free models (their shipped versions need OpenAI/Gemini/GitHub Models keys). contrib-guard (phoenix) is an exact port.
- LLM judges and re-rankers only see AgentDup's top-k, so their Recall@k is capped by AgentDup's Recall@k. Claude Haiku was run on cross-author + negative queries only (budget).
- Commercial review tools (CodeRabbit, Copilot review, Qodo, Greptile, ...) were compared from their documentation only, not run.
- Jev (TypeSafe System One) was not evaluated.

## 12. Reproduce

```bash
cd experiments/bench_v2
python3 bm25_feats.py            # BM25 features
bash run_embeds.sh               # CPU MiniLM embeddings (or Modal below)
modal run ../modal/gpu_jobs.py::embed_all
modal run ../modal/gpu_jobs.py::rerank_all
modal run ../modal/gpu_jobs.py::judge --model Qwen/Qwen2.5-7B-Instruct --tag qwen7
modal run ../modal/gpu_jobs.py::finetune_all
ANTHROPIC_API_KEY=... python3 claude_judge.py   # budget-capped
NB=2000 python3 eval2.py
python3 ../report/make_report.py && python3 ../report/make_tables.py
```

Full per-group tables for every strategy: `tables.md`. Raw per-query ranks: `experiments/results/ranks.parquet`.
