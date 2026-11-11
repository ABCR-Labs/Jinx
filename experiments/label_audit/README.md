# Silver-label audit

Claude Haiku 4.5 (`claude-haiku-4-5`) read each labelled pair: the linking comment, both PRs' titles, the first 1,500
characters of each description, and the changed files. It assigned one of five labels: duplicate, replacement, subsumed, related, unclear.
This is an LLM audit, not human annotation.

| Sample | n | duplicate | replacement | subsumed | related | unclear | precision, strict (dup+repl) [95% CI] | precision incl. subsumed |
|---|---|---|---|---|---|---|---|---|
| random labelled pairs (seed 0) | 200 | 43 | 115 | 37 | 2 | 3 | 0.790 [0.735, 0.845] | 0.975 [0.950, 0.995] |
| all cross-author pairs | 342 | 93 | 197 | 39 | 9 | 4 | 0.848 [0.810, 0.886] | 0.962 [0.942, 0.980] |

**Does the main result survive on clean labels?** (`clean_subset_eval.py`, repository-cluster bootstrap, 2,000 resamples)

| Cross-author subset | n | Jinx R@1 | INTRUDE + time R@1 | Jinx - INTRUDE R@1 | Jinx - INTRUDE R@5 |
|---|---|---|---|---|---|
| all | 342 | 0.901 | 0.810 | +9.1 [+4.8, +13.0] | +1.8 [-1.1, +5.1] |
| audit-valid (dup+repl) | 290 | 0.914 | 0.838 | +7.6 [+3.1, +10.8] | +0.3 [-1.9, +2.6] |
| audit-valid incl. subsumed | 329 | 0.909 | 0.821 | +8.8 [+4.6, +12.5] | +1.5 [-1.0, +4.4] |

The Recall@1 gain holds and the Recall@5 kill rule still fails. Cost: $0.82 for 542 calls, plus $0.01 for a pilot.
Run: `ANTHROPIC_API_KEY=... python audit_silver.py 200 && python audit_silver.py cross && python clean_subset_eval.py`.
