# Jinx project checklist

Owner: **D** = Devin, **H** = Harshul. Update this file in every PR.

## 1. Research question and results
- [x] D: prior art and gap (`docs/phase1_prior_art_and_plan.md`)
- [x] D: live-queue benchmark on AIDev: 4,832 queries, 1,867 duplicate pairs (342 cross-author), 2,965 no-duplicate PRs
- [x] D: 66-strategy study with repository-cluster CIs, per-class results, false alarms, latency, cost (`experiments/report/`)
- [x] D: pre-registered kill rule tested and reported (fails on cross-author Recall@5)
- [ ] H: accept the narrower claim (beats bots; better Recall@1/MRR and fewer false alarms than INTRUDE + time)

## 2. Benchmark (artifact)
- [ ] D: release files (queries, queues, labels, features) + data card + Zenodo-ready bundle
- [ ] D: label audit, Claude Haiku on 200 random pairs (about $1) + spot checks; report silver-label precision
- [ ] D: limitation noted: no agent-human pairs (no working GitHub token)

## 3. Tool (Jinx)
- [x] D: library, CLI, GitHub Action, README, 11 unit tests
- [x] D: renamed AgentDup -> Jinx (`jinx-pr` / `jinx_pr` / `jinx`)
- [ ] D: ship trained weights (`src/jinx_pr/data/weights*.json` are placeholders)
- [ ] D: feature-parity check: package features == benchmark features
- [ ] D: end-to-end CLI tests on real AIDev PRs
- [ ] D: run the Action on a private sandbox repo with test PRs
- [ ] D: clean Ruff warnings in `experiments/` scripts
- [ ] H: rename GitHub repo `ABCR-Labs/agentdup` -> `jinx-pr` (Settings; Devin lacks admin)
- [ ] H: approve making the repo public (needed by both tool tracks)

## 4. Repo organization
- [x] D: one repo layout: `src/`, `tests/`, `experiments/`, `docs/`, `paper/`
- [ ] D/H: review and merge PRs (one commit each)

## 5. Papers
- [x] D: `paper/` set up: IEEE (empirical) and ACM (tool demo) templates, `refs.bib`, tables and numbers generated from results
- [ ] D: verify every `refs.bib` entry (author names marked TODO)
- [ ] D: empirical paper full draft (RQ1-RQ4) -> PDF
- [ ] D: claims ledger complete (`paper/CLAIMS.md`) + independent review
- [ ] D: tool-demo paper draft (4+1 pages) + architecture figure
- [ ] D: demo video script; H: record or approve a screencast
- [ ] H: choose venue(s): ICPC Tool Demo (19 Nov), ICPC RENE (abstract 11 Dec, paper 18 Dec), FSE Tool Demos (26 Jan)
- [ ] H: approve submission (nothing is submitted without approval)

## 6. Budget
- Spent: Anthropic $7.25 (cap $20); Modal about $8.5 (cap $20). Planned: about $1 (label audit).
