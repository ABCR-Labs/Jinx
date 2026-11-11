# AgentDup: Phase 2 results (tool + live-queue benchmark)

All work: CPU only, $0, AIDev data only. Nothing pushed, published, submitted or registered. No OpenAI or Anthropic calls.

## 1. Verdict in one paragraph

**Kill rule: FAILED as written.** On cross-author pairs, AgentDup's Recall@5 beats the best baseline (classic INTRUDE-style features + time, trained the same way) by **+1.8 points, 95% CI -0.9 to +5.2**. That is not a CI-backed margin. Recall@5 is close to the ceiling for every method on these labels (0.86-0.97), so a large Recall@5 gain is not available on this benchmark.

What *is* CI-backed:
- **Ranking the right PR first.** On cross-author pairs: R@1 +7.9 points [+3.5, +12.5] (lexical) and +9.1 [+4.8, +12.9] (with embedding). MRR +5.2 [+1.9, +9.0].
- **Fewer false alarms.** At matched detection, false alarms drop from 4.1% to 2.5% (-1.6 points [-2.2, -1.0]).
- **Beats every existing bot, on Recall@5 too.** Against the best bot (contrib-guard), cross-author R@5 is +5.3 points [+1.2, +10.1] and R@1 +11.1 [+5.0, +16.6]. PRSense, PRism, Simili, vector-triage and contrib-guard all sit at R@5 0.86-0.92 and R@1 0.66-0.78; AgentDup is at 0.97 / 0.89-0.90.

So the honest claim is:
- AgentDup beats existing duplicate-PR **bots** clearly.
- It beats a re-trained **classic research detector** on top-1 ranking and false alarms, but not on Recall@5.

## 2. What was built (local only, `~/research/prdupecheck/agentdup/`)

- **Python library + CLI:** `agentdup check NEW.json --open-queue OPEN.jsonl [--diff] [--embed] [--json]` ranks likely duplicates with plain reasons ("shares 1 of 1 changed files (auth/session.py)", "100% of changed line ranges overlap", "same linked issue #9", "text similar after removing agent template"). `agentdup learn-templates` learns template lines from your own PRs.
- **Signals:**
  - learned template stripping: per-agent lines from 361k AIDev PRs, plus lines common in the current queue;
  - changed-file overlap, changed line-range overlap, identical added lines;
  - linked issue and explicit #reference;
  - author/agent/time context;
  - optional local MiniLM embedding.
- **GitHub Action:** `action.yml` (composite, Python 3.11) plus an example `.github/workflows/agentdup.yml`. It only uses `GITHUB_TOKEN` and posts or updates one comment. Not pushed, not on the Marketplace.
- **Quality:** 11 tests pass, ruff clean, `pip install -e .` works, README with a 30-second quickstart, MIT license.
- **Caveat:** the package's shipped default weights are still placeholders. The benchmark numbers come from logistic weights trained per fold (below). Before release, I will ship weights trained on all AIDev folds.

## 3. Benchmark setup (live-queue scoring)

- **Queries:** 1,867 labelled PRs from AIDev v5, where a comment says "duplicate of / superseded by #N" and #N is also an AIDev PR.
  - 1,525 self-replacement (same author);
  - 342 cross-author: 228 same agent, 114 different agent.
- **Negatives:** 2,965 merged PRs with no duplicate comment, used for false alarms.
- **Candidates:** for each query, every PR in the same repo that was open when it was created, or closed in the 7 days before. Median queue 40, p90 314, max 1,900. This is the "live queue", not random pairs.
- **Training:** trained methods (INTRUDE-style, time-aware, AgentDup) use logistic regression with 5-fold cross-validation **grouped by repository**, so there is no repo leakage.
- **CIs:** 95% repository-cluster bootstrap. Paired CIs compare methods on the same queries.
- **agent-human split:** not possible. In AIDev v5 every target PR outside the agent table is missing (1,920 such pairs), and the GitHub token is dead. So "agent-agent vs agent-human" is reported as same-agent vs cross-agent only.

### How each existing bot was run
| Tool | Run how | Why |
|---|---|---|
| contrib-guard (phoenix-assistant, npm v1.0, MIT) | exact Python port of its TF-IDF matcher; **checked against the real npm code on 15,444 pairs: max difference 4e-16** | needs GitHub API to run end to end |
| contrib-guard (balyakin, MIT) | **its own Python code** (`duplicate_detection.py`: title Jaccard, plus the "same files" rule) | - |
| PRSense v2.2 (MIT) | re-implementation: its scoring 0.45 text + 0.35 diff + 0.20 file Jaccard, with local MiniLM | its "local ONNX" embedder uses a placeholder hash tokenizer, not a real model; the other embedders are OpenAI or a Python server |
| PRism (MIT) | re-implementation of its embedding stage (`title\n\nbody`) with local MiniLM; LLM stage dropped | needs OpenAI (never allowed). Its model input is token-identical to the plain-text baseline, so its scores equal plain embedding |
| Simili-bot v0.2.3 (Apache-2.0) | re-implementation of its vector stage (`Title: ...\n\nBody: ...`) with local MiniLM | needs a Gemini/OpenAI key |
| vector-triage (MIT) | re-implementation of its engine: vector top-5 + SQLite FTS5 (porter, bm25 10/1) + RRF k=60 + 0.75 display filter, local MiniLM | needs GitHub Models. **Finding:** its keyword branch ANDs every term of title+body+files+diff (median 645 terms), so it matched **0 of 4,832** queries; it is effectively vector-only |

Every embedding baseline uses the same local model (all-MiniLM-L6-v2). This is fair between tools, but a stronger API embedding could score higher for PRism/Simili/vector-triage. That is a limitation to state in the paper.

## 4. Results

**all labelled** (n = 1867)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.772 [0.725, 0.817] | 0.911 [0.862, 0.948] | 0.837 |
| Plain embedding (MiniLM, raw text) | 0.721 [0.676, 0.768] | 0.885 [0.829, 0.930] | 0.797 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.722 [0.674, 0.775] | 0.885 [0.835, 0.930] | 0.796 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.721 [0.676, 0.768] | 0.885 [0.829, 0.930] | 0.797 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.729 [0.681, 0.775] | 0.883 [0.829, 0.928] | 0.801 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.721 [0.677, 0.768] | 0.886 [0.832, 0.932] | 0.796 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.721 [0.677, 0.767] | 0.886 [0.832, 0.932] | 0.796 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.781 [0.736, 0.825] | 0.925 [0.897, 0.950] | 0.845 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.680 [0.634, 0.722] | 0.846 [0.792, 0.890] | 0.756 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.837 [0.789, 0.878] | 0.949 [0.909, 0.977] | 0.889 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.848 [0.820, 0.877] | 0.965 [0.948, 0.980] | 0.902 |
| AgentDup (lexical) | 0.903 [0.875, 0.925] | 0.984 [0.974, 0.993] | 0.938 |
| AgentDup (+ local embedding) | 0.890 [0.839, 0.929] | 0.980 [0.968, 0.990] | 0.927 |
| ablation: no template stripping | 0.890 [0.839, 0.928] | 0.970 [0.948, 0.987] | 0.926 |
| ablation: no code overlap | 0.872 [0.825, 0.910] | 0.983 [0.968, 0.994] | 0.920 |
| ablation: no issue/reference links | 0.872 [0.822, 0.913] | 0.973 [0.949, 0.989] | 0.914 |
| ablation: no author/agent context | 0.892 [0.842, 0.931] | 0.980 [0.968, 0.989] | 0.928 |
| ablation: no time features | 0.836 [0.784, 0.876] | 0.951 [0.907, 0.981] | 0.889 |

**self-replacement (same author)** (n = 1525)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.776 [0.717, 0.828] | 0.909 [0.850, 0.956] | 0.838 |
| Plain embedding (MiniLM, raw text) | 0.721 [0.659, 0.771] | 0.880 [0.813, 0.933] | 0.795 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.725 [0.664, 0.779] | 0.890 [0.834, 0.938] | 0.799 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.721 [0.659, 0.771] | 0.880 [0.813, 0.933] | 0.795 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.730 [0.671, 0.779] | 0.881 [0.814, 0.936] | 0.800 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.723 [0.664, 0.775] | 0.884 [0.818, 0.937] | 0.796 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.723 [0.664, 0.775] | 0.884 [0.818, 0.937] | 0.796 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.782 [0.724, 0.834] | 0.927 [0.891, 0.957] | 0.846 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.683 [0.629, 0.736] | 0.843 [0.777, 0.894] | 0.757 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.839 [0.784, 0.887] | 0.949 [0.899, 0.983] | 0.890 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.857 [0.824, 0.891] | 0.968 [0.948, 0.984] | 0.908 |
| AgentDup (lexical) | 0.906 [0.874, 0.932] | 0.988 [0.976, 0.995] | 0.941 |
| AgentDup (+ local embedding) | 0.887 [0.827, 0.933] | 0.982 [0.968, 0.992] | 0.925 |
| ablation: no template stripping | 0.885 [0.827, 0.930] | 0.972 [0.946, 0.992] | 0.923 |
| ablation: no code overlap | 0.869 [0.813, 0.914] | 0.986 [0.969, 0.997] | 0.919 |
| ablation: no issue/reference links | 0.870 [0.808, 0.920] | 0.976 [0.948, 0.995] | 0.913 |
| ablation: no author/agent context | 0.889 [0.829, 0.936] | 0.982 [0.967, 0.993] | 0.927 |
| ablation: no time features | 0.836 [0.777, 0.886] | 0.950 [0.896, 0.985] | 0.889 |

**cross-author** (n = 342)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.757 [0.702, 0.811] | 0.921 [0.881, 0.956] | 0.832 |
| Plain embedding (MiniLM, raw text) | 0.725 [0.664, 0.791] | 0.906 [0.847, 0.949] | 0.807 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.711 [0.609, 0.811] | 0.865 [0.794, 0.936] | 0.784 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.725 [0.664, 0.791] | 0.906 [0.847, 0.949] | 0.807 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.725 [0.661, 0.797] | 0.892 [0.838, 0.936] | 0.804 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.713 [0.649, 0.782] | 0.895 [0.850, 0.933] | 0.799 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.713 [0.649, 0.782] | 0.895 [0.850, 0.933] | 0.799 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.778 [0.716, 0.839] | 0.918 [0.875, 0.957] | 0.843 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.664 [0.603, 0.726] | 0.863 [0.807, 0.913] | 0.754 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.827 [0.776, 0.880] | 0.947 [0.915, 0.973] | 0.882 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.810 [0.765, 0.853] | 0.953 [0.923, 0.979] | 0.873 |
| AgentDup (lexical) | 0.889 [0.845, 0.928] | 0.971 [0.951, 0.990] | 0.925 |
| AgentDup (+ local embedding) | 0.901 [0.865, 0.930] | 0.971 [0.951, 0.992] | 0.932 |
| ablation: no template stripping | 0.912 [0.877, 0.942] | 0.962 [0.939, 0.983] | 0.938 |
| ablation: no code overlap | 0.886 [0.848, 0.924] | 0.971 [0.949, 0.993] | 0.926 |
| ablation: no issue/reference links | 0.883 [0.849, 0.920] | 0.959 [0.936, 0.985] | 0.919 |
| ablation: no author/agent context | 0.904 [0.867, 0.936] | 0.971 [0.951, 0.990] | 0.934 |
| ablation: no time features | 0.833 [0.783, 0.884] | 0.956 [0.911, 0.986] | 0.889 |

**cross-author, same agent** (n = 228)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.776 [0.725, 0.832] | 0.930 [0.890, 0.961] | 0.844 |
| Plain embedding (MiniLM, raw text) | 0.737 [0.681, 0.800] | 0.917 [0.868, 0.951] | 0.816 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.732 [0.662, 0.805] | 0.899 [0.856, 0.939] | 0.809 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.737 [0.681, 0.800] | 0.917 [0.868, 0.951] | 0.816 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.750 [0.694, 0.806] | 0.899 [0.853, 0.936] | 0.823 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.737 [0.678, 0.794] | 0.908 [0.872, 0.940] | 0.816 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.737 [0.678, 0.794] | 0.908 [0.872, 0.940] | 0.816 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.811 [0.750, 0.859] | 0.925 [0.883, 0.956] | 0.861 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.671 [0.585, 0.741] | 0.860 [0.804, 0.906] | 0.755 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.846 [0.797, 0.897] | 0.952 [0.929, 0.976] | 0.895 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.825 [0.775, 0.874] | 0.961 [0.940, 0.982] | 0.883 |
| AgentDup (lexical) | 0.882 [0.828, 0.925] | 0.965 [0.939, 0.990] | 0.919 |
| AgentDup (+ local embedding) | 0.899 [0.851, 0.939] | 0.965 [0.937, 0.990] | 0.929 |
| ablation: no template stripping | 0.904 [0.854, 0.945] | 0.961 [0.934, 0.986] | 0.931 |
| ablation: no code overlap | 0.886 [0.843, 0.925] | 0.969 [0.944, 0.994] | 0.924 |
| ablation: no issue/reference links | 0.890 [0.840, 0.934] | 0.956 [0.928, 0.983] | 0.923 |
| ablation: no author/agent context | 0.904 [0.857, 0.942] | 0.969 [0.945, 0.991] | 0.933 |
| ablation: no time features | 0.846 [0.796, 0.896] | 0.961 [0.929, 0.985] | 0.897 |

**cross-author, cross-agent** (n = 114)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.719 [0.622, 0.852] | 0.904 [0.807, 0.988] | 0.808 |
| Plain embedding (MiniLM, raw text) | 0.702 [0.582, 0.820] | 0.886 [0.778, 0.955] | 0.787 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.667 [0.500, 0.875] | 0.798 [0.669, 0.947] | 0.734 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.702 [0.582, 0.820] | 0.886 [0.778, 0.955] | 0.787 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.675 [0.556, 0.829] | 0.877 [0.771, 0.951] | 0.766 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.667 [0.547, 0.817] | 0.868 [0.764, 0.940] | 0.764 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.667 [0.547, 0.817] | 0.868 [0.764, 0.940] | 0.764 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.711 [0.618, 0.842] | 0.904 [0.800, 1.000] | 0.806 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.649 [0.541, 0.784] | 0.868 [0.771, 0.961] | 0.752 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.789 [0.711, 0.878] | 0.939 [0.852, 0.990] | 0.856 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.781 [0.697, 0.871] | 0.939 [0.852, 0.990] | 0.853 |
| AgentDup (lexical) | 0.904 [0.846, 0.968] | 0.982 [0.958, 1.000] | 0.937 |
| AgentDup (+ local embedding) | 0.904 [0.863, 0.958] | 0.982 [0.958, 1.000] | 0.939 |
| ablation: no template stripping | 0.930 [0.898, 0.973] | 0.965 [0.933, 1.000] | 0.952 |
| ablation: no code overlap | 0.886 [0.815, 0.963] | 0.974 [0.936, 1.000] | 0.928 |
| ablation: no issue/reference links | 0.868 [0.808, 0.974] | 0.965 [0.932, 1.000] | 0.912 |
| ablation: no author/agent context | 0.904 [0.852, 0.974] | 0.974 [0.945, 1.000] | 0.938 |
| ablation: no time features | 0.807 [0.721, 0.909] | 0.947 [0.862, 1.000] | 0.872 |

**cross-author, no explicit #ref to gold** (n = 199)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.683 [0.602, 0.770] | 0.879 [0.819, 0.942] | 0.772 |
| Plain embedding (MiniLM, raw text) | 0.709 [0.627, 0.785] | 0.879 [0.790, 0.943] | 0.783 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.693 [0.617, 0.788] | 0.854 [0.783, 0.934] | 0.769 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.709 [0.627, 0.785] | 0.879 [0.790, 0.943] | 0.783 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.709 [0.632, 0.783] | 0.859 [0.783, 0.925] | 0.782 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.704 [0.626, 0.776] | 0.859 [0.783, 0.922] | 0.781 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.704 [0.626, 0.776] | 0.859 [0.783, 0.922] | 0.781 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.714 [0.645, 0.797] | 0.874 [0.800, 0.936] | 0.788 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.628 [0.528, 0.705] | 0.819 [0.740, 0.889] | 0.715 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.744 [0.661, 0.831] | 0.910 [0.857, 0.954] | 0.818 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.714 [0.632, 0.788] | 0.920 [0.872, 0.963] | 0.803 |
| AgentDup (lexical) | 0.834 [0.779, 0.884] | 0.960 [0.937, 0.987] | 0.888 |
| AgentDup (+ local embedding) | 0.854 [0.808, 0.897] | 0.960 [0.935, 0.992] | 0.901 |
| ablation: no template stripping | 0.869 [0.811, 0.914] | 0.945 [0.917, 0.974] | 0.908 |
| ablation: no code overlap | 0.829 [0.774, 0.879] | 0.960 [0.935, 0.994] | 0.890 |
| ablation: no issue/reference links | 0.849 [0.800, 0.897] | 0.945 [0.916, 0.986] | 0.893 |
| ablation: no author/agent context | 0.859 [0.814, 0.904] | 0.960 [0.939, 0.986] | 0.904 |
| ablation: no time features | 0.759 [0.676, 0.843] | 0.925 [0.852, 0.978] | 0.831 |

**self-replacement, no explicit #ref to gold** (n = 1077)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.771 [0.699, 0.826] | 0.910 [0.832, 0.960] | 0.836 |
| Plain embedding (MiniLM, raw text) | 0.717 [0.647, 0.776] | 0.883 [0.806, 0.939] | 0.794 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.722 [0.652, 0.783] | 0.893 [0.818, 0.945] | 0.799 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.717 [0.647, 0.776] | 0.883 [0.806, 0.939] | 0.794 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.722 [0.652, 0.781] | 0.885 [0.804, 0.939] | 0.797 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.721 [0.650, 0.782] | 0.887 [0.809, 0.941] | 0.795 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.721 [0.649, 0.781] | 0.887 [0.809, 0.941] | 0.794 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.767 [0.694, 0.823] | 0.932 [0.908, 0.957] | 0.839 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.679 [0.609, 0.736] | 0.851 [0.766, 0.906] | 0.758 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.800 [0.721, 0.859] | 0.934 [0.858, 0.981] | 0.863 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.827 [0.795, 0.862] | 0.961 [0.934, 0.984] | 0.889 |
| AgentDup (lexical) | 0.892 [0.864, 0.917] | 0.989 [0.982, 0.995] | 0.934 |
| AgentDup (+ local embedding) | 0.868 [0.784, 0.923] | 0.982 [0.972, 0.992] | 0.914 |
| ablation: no template stripping | 0.863 [0.781, 0.920] | 0.975 [0.950, 0.992] | 0.910 |
| ablation: no code overlap | 0.853 [0.781, 0.905] | 0.991 [0.984, 0.997] | 0.911 |
| ablation: no issue/reference links | 0.868 [0.785, 0.922] | 0.984 [0.971, 0.994] | 0.914 |
| ablation: no author/agent context | 0.868 [0.783, 0.924] | 0.982 [0.970, 0.993] | 0.914 |
| ablation: no time features | 0.798 [0.717, 0.858] | 0.937 [0.856, 0.985] | 0.863 |

**False alarms on 2,965 PRs with no duplicate**

| Method | FAR, threshold set for 50% cross-author detection | correct top-1 alerts (cross-author) | FAR at tool default | correct alerts at default |
|---|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.094 | 0.424 | - | - |
| Plain embedding (MiniLM, raw text) | 0.121 | 0.427 | - | - |
| PRSense v2.2 (re-impl, local MiniLM) | 0.127 | 0.371 | 0.036 | 0.190 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.121 | 0.427 | 0.046 | 0.243 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.111 | 0.436 | 0.377 | 0.620 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.126 | 0.412 | 0.019 | 0.108 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.126 | 0.412 | - | - |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.117 | 0.418 | 0.282 | 0.594 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.146 | 0.430 | 0.020 | 0.170 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.041 | 0.433 | - | - |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.046 | 0.442 | - | - |
| AgentDup (lexical) | 0.032 | 0.468 | - | - |
| AgentDup (+ local embedding) | 0.025 | 0.471 | - | - |
| ablation: no template stripping | 0.023 | 0.480 | - | - |
| ablation: no code overlap | 0.035 | 0.477 | - | - |
| ablation: no issue/reference links | 0.038 | 0.462 | - | - |
| ablation: no author/agent context | 0.026 | 0.468 | - | - |
| ablation: no time features | 0.034 | 0.444 | - | - |


### Ablations (cross-author, R@1 / R@5)
- **No time features:** 0.833 / 0.956. This is the biggest single drop; time gap and "candidate still open" matter most.
- **No issue/reference links:** 0.883 / 0.959.
- **No code overlap:** 0.886 / 0.971.
- **No template stripping:** 0.912 / 0.962. R@1 is *higher* without stripping. Template stripping does not help on cross-author pairs, only on self-replacement (R@1 0.906 vs 0.885). This is a negative result to report, and it weakens the "agent-aware" pitch.

### Label bias check
- **Explicit #references:** in 42% of cross-author pairs, the new PR's body already mentions the duplicate (#N). AIDev stores the final body, so some of these were edited in later.
- **Without those pairs** (post-hoc subset, n = 199): AgentDup R@5 0.960 vs 0.920 for the best baseline: +4.0 points [+0.5, +10.0]. R@1 is +12.1 [+6.0, +20.4].
- **This doesn't change the verdict.** It is post-hoc, so it can't rescue the kill rule. But it shows the gap grows on the harder, more realistic cases.

### Speed (CPU)
- **Lexical scoring:** 22 ms for the median PR, 229 ms at p90, 7.3 s worst case (queue of 1,900, pure Python).
- **Embedding:** MiniLM embeds about 50-90 PR texts per second on 8 CPUs, so the Action's first run on a large repo costs seconds, then queue vectors can be cached.

## 5. Threats
1. **Silver labels.** The labels come from comments, which only exist when a human noticed, so easy duplicates are over-represented. This is also why R@5 saturates.
2. **Re-implementations.** Four of the bots are re-implementations with a local model, not the shipped product. Only the two contrib-guard tools ran as their own logic.
3. **No adoption evidence yet.** The HeapLens model needs installs or users. That needs a public repo and maintainers who agree, which requires your OK.

## Venues (checked 10 Nov 2026 on the official call pages)

| | ICPC 2027 Tool Demonstration | FSE 2027 Tool Demonstrations | ICPC 2027 RENE (empirical paper) |
|---|---|---|---|
| Deadline (AoE) | **Thu 19 Nov 2026** (notification 14 Jan, camera-ready 28 Jan) | **Tue 26 Jan 2027** (notification 17 Mar, camera-ready 2 Apr) | abstract 11 Dec, paper 18 Dec 2026 |
| Length | 4 pages + 1 page references, IEEE `\documentclass[10pt, conference]{IEEEtran}` | 4 pages + 1 page references, ACM format | new replication / negative result: 10 + 2 pages, IEEE |
| Review | not anonymous | single-blind | not anonymous |
| Tool / artifact | source or binaries **must be publicly available** (GitHub, Zenodo, Figshare or website) | availability, maturity, user base, link to source expected | - |
| Video | optional but encouraged: 3-5 min screencast URL in the abstract (YouTube or tool site) | link to a screencast expected; demo walkthrough appendix (not counted) | - |
| Proceedings | ICPC proceedings (ACM/IEEE DL) | main FSE proceedings, ACM DL; one author must register (not one-day) and present | ICPC proceedings |
| Overlap rule | IEEE/ACM plagiarism + submission policies | "must present new content ... not previously published as a main contribution in any venue"; tool must not already be a main contribution of a research paper | "must not be under review or submitted for review elsewhere" |

### Dual-submission overlap
- A Tool Demo paper and the RENE paper must not be the same paper. Safe split:
  - **Tool Demo** = the tool: design, the GitHub Action workflow, the live-queue head-to-head against existing bots, latency, a short adoption/usage story.
  - **RENE** = the empirical study: do classic duplicate-PR detectors (Li 2017, INTRUDE 2019, time-aware 2019) replicate on agent PRs, live-queue vs random-pair evaluation, template effects, label-noise analysis, negative results.
- Shared benchmark numbers would appear in both. Under the RENE rule ("must not be under review ... elsewhere") the main results table of one paper should not be the main contribution of the other. Each paper should cite the other as under review, and the RENE paper should treat AgentDup as one row, not its contribution.
- FSE Tool Demos explicitly forbids a tool that is already the main contribution of a research paper. If AgentDup becomes the main contribution of an ICPC paper, FSE Tool Demos is closed, and vice versa.


## 6. Feasibility and recommendation
- **ICPC Tool Demo (19 Nov, 9 days): feasible but weak.**
  - A 4+1 page draft is doable: the tool, benchmark and tables exist.
  - **The tool must be public at submission**, which needs your OK to push.
  - There would be no adoption evidence, and the headline vs classic detectors is "top-1 and false alarms", not Recall@5.
  - I'd rate acceptance low to medium.
- **Recommended: FSE 2027 Tool Demos (26 Jan).** Use Nov-Jan to:
  - (a) ship trained weights and a release;
  - (b) with your OK, make the repo public and run the Action in shadow mode (no comments) on a few willing repos, for real usage numbers;
  - (c) add a 3-5 min screencast.
- **RENE (18 Dec)** stays a separate empirical paper:
  - its topic: classic detectors on agent PRs, live-queue vs random-pair evaluation, the template-stripping negative result, label bias;
  - AgentDup appears only as one compared method;
  - FSE forbids a tool that is already the main contribution of another paper, so RENE must not present AgentDup as its contribution.
