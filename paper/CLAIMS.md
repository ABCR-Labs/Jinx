# Claims ledger

Every number in either paper must come from a file below. Numbers in the LaTeX come from `paper/generated/numbers.tex`, built by `paper/scripts/make_paper_tables.py`.

| Claim | Value | Source |
|---|---|---|
| Strategies compared | 66 | `experiments/results/strategies_by_group.csv` (unique `method`) |
| Duplicate pairs / cross-author / self | 1,867 / 342 / 1,525 | same file, `n` per group |
| No-duplicate queries | 2,965 | `bench.pkl` (`neg=True`); hard-coded in the script |
| Jinx cross-author R@1 / R@5 | 0.901 / 0.971 | `strategies_by_group.csv` |
| INTRUDE + time R@1 / R@5 | 0.810 / 0.953 | same |
| contrib-guard R@1 / R@5 | 0.778 / 0.918 | same |
| Jinx - INTRUDE, R@5 | +1.8 [-0.9, +5.2] (kill rule fails) | `paired_cross_author.csv` |
| Jinx - INTRUDE, R@1 | +9.1 [+5.0, +13.1] | same |
| Jinx - contrib-guard, R@5 | +5.3 [+1.2, +9.7] | same |
| False alarms Jinx / INTRUDE | 2.5% / 4.6% | `false_alarms.csv` |
| Strategies with CI-backed R@5 gain over INTRUDE | 0 of 65 | `paired_cross_author.csv` |
| Links-only R@1 (label bias) | 0.839 | `strategies_by_group.csv` |
| 23.7% of failed agent PRs are duplicates | 142 / 600 | Ehsani et al. 2026 (arXiv:2601.15195) |
| Jinx median CPU latency | 22 ms/query (p90 229) | `experiments/results/summary.json` -> `latency` -> `lexical features ms/query` |
| Silver-label precision, strict (random 200) | 0.790 [0.735, 0.845] | `experiments/label_audit/audit_random200_summary.json` |
| Silver-label precision, strict (cross-author 342) | 0.848 [0.810, 0.886] | `experiments/label_audit/audit_cross_summary.json` |
| Jinx - INTRUDE R@1 on audit-valid cross-author (n=290) | +7.6 [+3.1, +10.8] | `experiments/label_audit/clean_subset_results.json` |
