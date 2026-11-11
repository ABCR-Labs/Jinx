# Jinx project checklist

Owner: **D** = Devin, **H** = Harshul. Update this file in every PR.

## 1. Research question and results
- [x] D: prior art and gap (`docs/phase1_prior_art_and_plan.md`)
- [x] D: live-queue benchmark on AIDev: 4,832 queries, 1,867 duplicate pairs (342 cross-author), 2,965 no-duplicate PRs
- [x] D: 66-strategy study with repository-cluster CIs, per-class results, false alarms, latency, cost (`experiments/report/`)
- [x] D: pre-registered kill rule tested and reported (fails on cross-author Recall@5)
- [ ] H: accept the narrower claim (beats bots; better Recall@1/MRR and fewer false alarms than INTRUDE + time)

## 2. Benchmark (artifact)
- [x] D: release files (queries, queues, labels, features) + data card (`docs/DATA_CARD.md`, `experiments/bench_v2/export_release.py`)
- [ ] H: approve uploading the release (Zenodo / Hugging Face, about 680 MB)
- [x] D: label audit, Claude Haiku on 200 random + all 342 cross-author pairs ($0.82): strict precision 79% / 85% (`experiments/label_audit/`)
- [ ] D: human spot-check of 30 audit labels
- [x] D: limitation noted: no agent-human pairs (no working GitHub token)

## 3. Tool (Jinx)
- [x] D: library, CLI, GitHub Action, README, 11 unit tests
- [x] D: renamed AgentDup -> Jinx (`jinx-pr` / `jinx_pr` / `jinx`)
- [x] D: ship trained weights (`experiments/bench_v2/train_package_weights.py`)
- [x] D: feature-parity check: package features == benchmark features (0 difference on 200 queries)
- [x] D: end-to-end CLI tests on real AIDev PRs (`tests/test_e2e_aidev.py`)
- [ ] D: run the Action on a private sandbox repo with test PRs
- [ ] D: clean Ruff warnings in `experiments/` scripts
- [ ] H: rename GitHub repo `ABCR-Labs/agentdup` -> `jinx-pr` (Settings; Devin lacks admin)
- [ ] H: approve making the repo public (needed by both tool tracks)

## 4. Repo organization
- [x] D: one repo layout: `src/`, `tests/`, `experiments/`, `docs/`, `paper/`
- [x] D/H: review and merge PRs #1-#6 (one commit each)

## 5. Papers
- [x] D: `paper/` set up: IEEE (empirical) and ACM (tool demo) templates, `refs.bib`, tables and numbers generated from results
- [ ] D: verify every `refs.bib` entry (author names marked TODO)
- [x] D: empirical paper first full draft (RQ1-RQ4) -> PDF (3 pages; expand to venue length once chosen)
- [x] D: claim audit of the empirical draft (`paper/CLAIM_AUDIT.md`): 4 wording fixes, no number changes
- [ ] D: independent re-review after venue-length expansion
- [x] D: tool-demo paper first draft (2 pages, ACM) + TikZ architecture figure; expand after sandbox/pilot results
- [x] D: demo video script (`paper/tooldemo/VIDEO_SCRIPT.md`)
- [x] D: plain-English rewrite of both papers, colour architecture diagram (`paper/figures/arch.tex`), 5 vector figures (`paper/scripts/make_figures.py`), highlighted tables
- [x] D: 3-reviewer panel (methods, writing, figures/tool demo); reports in `paper/reviews/`
- [ ] H: record or approve a screencast (after the sandbox Action run)
- [ ] H: choose venue(s): ICPC Tool Demo (19 Nov), ICPC RENE (abstract 11 Dec, paper 18 Dec), FSE Tool Demos (26 Jan)
- [ ] H: approve submission (nothing is submitted without approval)

## 6. Budget
- Spent: Anthropic $8.08 (cap $20); Modal about $8.5 (cap $20).
- [x] D: review-panel fixes: real-use queues (open PRs only, 200 most recent, forward-only mentions) are now the main benchmark; all 66 strategies rerun; 7-day-window results kept in `experiments/results_grace7/` and reported as RQ3
- [x] D: impact analysis: duplicate cost (`experiments/impact/duplicate_cost.py`) and day-0 warning replay (`experiments/impact/replay.py`)
- [x] D: shipped weights retrained on real-use queues; Action `embed` input (MiniLM on by default); end-to-end package latency (`experiments/bench_v2/package_latency.py`)
- [ ] H: 100-pair human label check (two labellers)
- [ ] H: GitHub token (read-only, public repos) for a shadow-mode run on live repos
- [x] D: second review round on the reframed papers (fixes below)


## Round-2 review (paper/reviews/round2/)
- [x] LLM/re-ranker rows: unscored candidates now keep Jinx's score; judge coverage stored in `summary.json`
- [x] Cost analysis on the open-only sample, human flags only, effort counted only after the second PR opened
- [x] Replay compares Jinx, INTRUDE + time and contrib-guard, with repo-bootstrap CIs and wrong-PR warnings
- [x] 200-PR cap misses reported (11 cross-author); deployed Recall@1 with them counted as misses
- [x] Package `mention_ref` is forward-only, matching training; Action default `embed: "false"`
- [x] Link rule without TF-IDF tie-break reported; table redesigned; consistent figure colours and names
- [x] Empirical paper no longer claims Jinx as a contribution; tool demo cites the study; shared table/figure removed from the demo
- [ ] Decide: re-run Claude Haiku on open-only top-5 candidates (~$1.2) — current scores cover 30%, so Haiku results are omitted
- [ ] Make repo public, publish `jinx-pr` on PyPI, record demo video, add an Action PR-comment screenshot (tool-track availability)
- [ ] Human 100-pair label check
