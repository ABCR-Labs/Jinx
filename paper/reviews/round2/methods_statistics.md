# Round 2 review: methods and statistics (ABCR-Labs/Jinx `main` @ 84c0351)

Review only. No pushes, no PRs, no API spend. I checked every claim against `experiments/results*/`, `experiments/label_audit/`, the scripts that produce them, and `src/jinx_pr/`. All `paper/generated/*.tex` macros match their source files. Where I recomputed something myself, I say so. I skipped anything that needs the raw AIDev data.

**Verdict.** The reframe is honest and most of it holds. The open-only-queue numbers, the cand_open ablations and the "no ranking gain" statements are all backed by the CSVs. Three problems remain:

- The LLM and re-ranker rows were not rerun on the new queues. The headline claim "an LLM judge lowers false alarms" rests on them. (B1)
- The cost (RQ1) figures count effort a warning could not have saved, and they come from a different sample than the rest of the paper. (B2)
- The replay reports Jinx alone, although the replay file shows other methods doing as well or better. (M1)

---

## Blockers

### B1. LLM, re-ranker and cascade scores are stale (grace-7 candidates), and missing scores lower false alarms by construction
- **Evidence:**
  - `experiments/results/scores/llm_haiku45.parquet` is identical to the copy in `results_grace7/scores/` (both have 4,587 pairs over 3,307 queries = 342 grace-7 cross-author + 2,965 negatives).
  - `claude_judge.py` l.10 judged Jinx's **grace-7** top 5 for cross-author queries and only the **top 1** for negatives.
  - In `eval2.py`, `rerank()` (l.109–118) gives a judged pair the score `10 + s` and leaves an unjudged pair at its raw Jinx score, which is below 1.
  - On open-only queues, the model was retrained and closed PRs were removed, so Jinx's top 5 changed. Any negative whose judged grace-7 top-1 is no longer in the new top 5 has no judged candidate. Its top score is then below 1, while the threshold is about 10.x (the median over training cross-author queries, which are nearly all judged). That negative can never raise an alarm.
  - The same applies to Qwen (43,591 pairs, unchanged), the cross-encoders, the fine-tuned re-ranker and every stacked cascade.
  - The PR says "All 66 strategies were rerun". In fact only the CPU strategies were rerun. The LLM and GPU rows reuse grace-7 candidate sets.
- **Affected claims:**
  - Abstract: "an LLM judge on Jinx's top five lowers this to \FARxhaiku\% (0.9%)".
  - RQ4, l.115: the 52% vs 35% at a 1% false-alarm budget.
  - Conclusion: "where an LLM judge helps".
  - Tool demo l.103: "false alarms fall to 0.9%".
  - Table I: ‡ marks on the Haiku and Qwen-14B rows.
- **Fix:**
  - Without new API calls, report the coverage: the share of open-only negatives and cross-author queries whose new top-1 (top-k) has a judge score. Then restrict every LLM, re-ranker and cascade comparison to fully covered queries, and count an uncovered top-1 as "judge abstains → use the Jinx score against the Jinx threshold", not as "no alarm".
  - Qwen and the cross-encoders can be re-scored on the new top-10 locally or on a GPU. If that isn't done, drop the 0.9% claim, or label it *"grace-7 candidate sets; not re-run"*.
  - Correct "All 66 strategies were rerun" in the PR, `CLAIMS.md` and §V.

### B2. RQ1 cost figures count effort a warning could not have saved, and come from the 342-pair grace-7 set
- **Evidence:** `experiments/impact/duplicate_cost.py`:
  - l.53–54 count human comments and reviews on the closed PR **before the duplicate comment**. They do not require them to come **after the new PR opened**. When the closed PR is the older one (the usual case), reviews it received before the duplicate existed are counted as cost of the duplicate. That feeds `dupEffort`: *"in 54% of cases someone had already commented on or reviewed the doomed PR"*, plus the totals of 320 comments and 304 reviews.
  - l.42–45 take the first comment containing the phrase, with **no `user_type` filter**. Comments by bots or agents (for example an agent writing "superseded by #N") are counted, yet the abstract and RQ1 say *"flagged by a person"*.
  - `duplicate_cost_summary.json` has cross-author n=**342** and all n=**1,867**, which is the grace-7 sample. The paper's benchmark is 313/1,767, and the replay uses 313.
  - `dupAllLines` ("8.0 million added lines were thrown away") sums the additions in `pr_commit_details` over closed PRs. The median is 180, so a few huge PRs dominate the total. In self-replacements the code often survives in the new PR, so it was not thrown away.
- **Fix:**
  - Count only effort in the window [new PR opened, duplicate comment].
  - Require `user_type != "Bot"` for the flagging comment, and report how many flags came from bots.
  - Recompute on the 313/1,767 sample (needs raw data, but no money).
  - Drop "thrown away", or report the median and a trimmed total.
  - Until then, abstract: *"someone had commented on or reviewed the PR that was later closed (counting activity before the duplicate was flagged, which may include work done before the second PR existed)"*.

---

## Major

### M1. The replay shows Jinx alone, but INTRUDE and contrib-guard give at least as many correct warnings
- **Evidence:** `replay_impact.csv`, cross-author, correct warning at open:

  | Method | Correct warning at open | Human took > 24 h | False alarms per 100 PRs |
  |---|---|---|---|
  | Jinx | 46.0% | 34.7% | 1.75 |
  | INTRUDE + time | 47.3% | 36.7% | 2.03 |
  | contrib-guard | 46.3% | **49.0%** | 5.45 |

  Empirical l.81 and tool demo l.105 present Jinx's 46% / 35% as "the benefit" of Jinx.
- **Other gaps:**
  - The replay ignores **wrong warnings on duplicate PRs** (top-1 above the threshold but not the true duplicate; `replay.py` l.26 counts only `rank == 1`). The comment would point the maintainer at the wrong PR.
  - The replay conditions on duplicates that people eventually flagged, so it says nothing about duplicates nobody noticed.
  - It has no CIs.
- **Fix:**
  - Report all three methods in a small table with repo-bootstrap CIs, and add a "wrong-PR warnings" column.
  - Reword: *"A day-0 warning from any of the three detectors would have named the right PR for about 46% of cross-author duplicates; Jinx does so with the fewest false alarms (1.8 vs 2.0 vs 5.5 per 100)."*
  - Tool demo l.105: say the replay is not specific to Jinx.

### M2. Removing pairs whose duplicate was cut by the 200-PR cap inflates recall for the deployed tool
- **Evidence:** `eval2.py` l.39 drops a labelled query when the gold PR is not in the capped open queue. Paper l.55 / tool demo l.91: the cap removes 29 of 1,796 pairs. For cross-author pairs: 342 − 18 (gold closed at query time, `nGraceCand`) − 313 = **11 of 324 (3.4%)**, which is twice the overall rate (my arithmetic from the macros). For a deployed Action those 11 are misses, not exclusions.
- **Fix:** Report deployment recall with the cap-dropped pairs counted as misses (Jinx R@1 ≈ 290/324 = 0.895), and give the cap effect by relation. Keep "closed before the query" exclusions separate; those are defensible.

### M3. The tool demo's "quiet" pitch is weaker than the CSVs show
- **Evidence:**
  - From `false_alarms.csv` / `paired_false_alarms.csv`, at the median threshold these are all **quieter** than Jinx (1.75%):
    - link rule 1.15% (Δ −0.60 [−1.30, +0.05])
    - Jinx gradient boosting 1.11% (Δ −0.64 [−1.32, −0.04], significant)
    - Qwen-14B + Jinx 1.31% (significant)
    - Haiku + Jinx 0.92%
  - In `operating_curve.csv`, the link rule catches **more** than Jinx at the 1%, 2% and 5% budgets (0.438 / 0.613 / 0.703 vs 0.351 / 0.524 / 0.684).
  - Tool demo l.34 ("aims for a low false-alarm rate") and l.103 ("Where Jinx stands out is quietness") hold only against contrib-guard and TF-IDF.
- **Fix:**
  - Tool demo l.103: *"Jinx is about as quiet as the best methods we tested (1.8%, CI 1.2–2.5) and much quieter than the best existing bot (5.5%) and TF-IDF (3.5%). A link rule is as quiet but can only explain links; Jinx also explains code-level matches."*
  - Mention the link rule's operating-curve advantage in RQ4.

### M4. Train/serve skew: `mention_ref` is still two-way in the package
- **Evidence:**
  - Training and evaluation use forward-only mentions: `eval2.py` l.26–29, `train_package_weights.py` l.34–36.
  - The package still computes `cand.number in new.mentions or new.number in cand.mentions` (`src/jinx_pr/features.py` l.60, verified). This is also the feature the explanation "one PR links to the other" depends on.
  - On `reopened` events, or when an older PR's body is edited to say "see #new", the shipped model sees a feature it was never trained on, with weight 0.29 standardised.
  - Tool demo §2 and the paper (l.55) say links use the new PR's text only.
- **Fix:** Make the package feature forward-only, or retrain on the two-way feature and say so. Add a test that `features.py` reproduces `features.parquet` columns on the exported fixtures.

### M5. The threshold and operating-curve method mixes fold scales and sets thresholds on the evaluation negatives
- **Evidence:**
  - `eval2.py` l.220–226 (threshold at l.224): the operating-curve threshold is a quantile of **all test-fold negatives pooled**, scored by five different fold models. The same negatives are then used to evaluate, which is optimistic and unequal across methods with fold-dependent scales.
  - No CIs.
  - The macros `OCone*` (52 / 35 / 44%) are quoted as findings.
  - The median-threshold FAR (Table I) is fine: it is per fold and set on training folds.
- **Fix:** Compute operating-curve thresholds per fold from the **training-fold** negatives, then pool the test outcomes. Add repo-bootstrap CIs at 1% and 5%. Until then, call Fig. 6 "descriptive".

### M6. RQ3's random-pair text no longer matches the numbers
- **Evidence:**
  - l.104: *"Among strong methods, random-pair AUC is close to 1 and says little"*. But `nCombHiAUC = 3`: only 3 of 25 combined methods now exceed AUC 0.98.
  - My recomputation from `random_pair_vs_live_queue.csv`: among the 45 methods with R@1 ≥ 0.85, Kendall τ = 0.44 (p = 2.6e-5). AUC still orders the strong methods moderately well.
  - "mostly because weak methods are weak under both" is not tested anywhere.
  - Contribution bullet l.34 still says random pairs "change which method appears best". The best-AUC method (All signals LR, 0.986) is tied for third on live R@1 (0.927 vs best 0.942, inside every CI).
- **Fix:** *"The two scorings agree on the order (τ = 0.68 overall, 0.44 among the 45 methods with Recall@1 ≥ 0.85). Pairwise AUC differences among strong methods are small (0.95–0.99) and do not identify a winner, but neither does live-queue Recall@1, whose CIs overlap."* Drop "random pairs" from the bullet, or show a concrete rank reversal with CIs.

### M7. Many false-alarm comparisons are marked without correcting for multiple comparisons
- **Evidence:** 42 of 65 false-alarm differences against Jinx have a CI that excludes zero (`paired_false_alarms.csv`). Table I marks †/‡ per row with uncorrected 95% CIs. The Qwen-14B ‡ has an upper bound of −0.05 points. RQ2 says only that subgroups are exploratory.
- **Fix:** Apply Holm correction across the rows shown in Table I, or state *"† and ‡ use unadjusted 95% CIs; with 11 comparisons in the table, about one false flag is expected."* Make Jinx vs contrib-guard the one primary false-alarm comparison, and fix it in §V.

### M8. The label audit and clean-subset check use the old population
- **Evidence:** `auditCrossN = 342` (grace-7 cross-author set), and the paper reports *"For the 342 cross-author pairs …"* (l.62) next to `nCross = 313`. `cleanN = 264` is the 313 set filtered by grace-7 audit labels. That is fine, but the text doesn't explain it.
- **Fix:** Report the audit on the 313 pairs that remain: filter `audit_cross_labels.jsonl` to the 313 (no API needed), and recompute precision and its CI. Add *"(audited on the earlier 342-pair set; 313 remain on real-use queues)"*.

---

## Minor

- **m1. "Closed PRs are always wrong answers" (l.99) is false.** `nGraceCand` = 18 cross-author gold PRs were already closed at query time. The value is also hard-coded in `make_paper_extras.py` l.91 instead of being read from a file. Fix: *"Recently closed PRs are almost always wrong answers (18 of 342 cross-author duplicates were already closed)"*, and write the 18 to `ablations.csv` or a JSON file.
- **m2. The open-only ablation and the main run disagree by one query.** Jinx forward-only R@1 is 0.930 in `ablations.csv` vs 0.927 in Table I (the same setting, apart from dropping the constant `cand_open`). The likely cause is tie-breaking or sampling differences. Fix: make the ablation import the eval2 pipeline, or say which run is canonical.
- **m3. Pre-registered test, l.75.** "It fails in every setting" is correct (`dRFIntrude` +0.3 [−0.8, +1.5]). Also, Jinx vs contrib-guard R@5 is +1.0 [**+0.0**, +2.5]: the lower bound rounds to 0. The text at l.88 ("so does Recall@5") is correct only if the bound is ≤ 0. Print three decimals or say "touches zero".
- **m4. Class D (l.110).** The best method is the link rule, 0.88 [0.73, 1.00], n=25. Name it with its CI. The heatmap and `tab_classes.tex` leave out the link rule, so they bold contrib-guard's 0.84 as the best value.
- **m5. Latency (Fig. 3, tool demo l.91).**
  - `package_latency.py` times `Detector.rank` on the bench.pkl queues (`Q[i]["cand"]`, the uncapped grace-7 queues with a median of 36.5 PRs), not the open-only queues.
  - It excludes GitHub API time. `action.py` makes one `/files` call per open PR, so about 200 calls for a full queue.
  - It excludes MiniLM model download and load, and pip-installing torch, in a cold Action run.

  Fix: time on open-only queues, and report Action wall-clock time from a sandbox run, or state these exclusions in the caption.
- **m6. Shipped threshold.** The intercept shift is set on in-sample cross-author top-1 scores from all 4,280 queries (`train_package_weights.py` l.47). The 1.8% false-alarm rate quoted in the tool demo (l.48) is the cross-validated rate, not the shipped model's. Fix: *"1.8% under cross-validation; the shipped model's threshold is set the same way on all data."*
- **m7. Constant feature.** `cand_open` is constant on open-only training data (coef 0.0, scale 1.0 in both weights files). Drop it from `LEX` in `train_package_weights.py` and the package so the explanation and feature code don't suggest it matters.
- **m8. Negatives are merged PRs.** This threat is still missing from §VII. Add: *"No-duplicate queries are merged PRs; PRs that are later closed may draw more false alarms."*
- **m9. Data Availability / Availability.** Both say "will be released with the camera-ready version". Double-blind venues usually expect an anonymised artefact link at submission.

- **m10. Bootstrap count.** The paper (l.73) says "2,000 bootstrap samples drawn by repository". `eval2.py` defaults to `NB=500` (`os.environ.get("NB", 500)`), and `ablations.py` hard-codes `nb=500`. Fix: rerun with `NB=2000` and record `NB` in `summary.json`, or change the text to 500 for each script that uses it. With CI bounds as close to zero as +0.0 (m3) and −0.05 (M7), the extra samples matter.

---

## What I verified as correct
- Table I values, all paired R@1/R@5 CIs vs Jinx, and the false-alarm CIs (`strategies_by_group.csv`, `paired_*.csv`, `false_alarms.csv`).
- Grace-7 numbers (`results_grace7/`) and the cand_open ablations (`ablations.csv`): 0.839 and 0.892.
- `dGsevenIntrude` +9.1 [+5.0, +13.1].
- Open-only Jinx − INTRUDE R@1 +1.3 [−0.7, +3.1].
- `kendallTau` 0.68.
- The duplicate-cost and replay macros match their files. The issues above are with how the files are produced and interpreted.
- Shipped weights are trained on open-only, forward-only data, and the Action's `embed` input defaults to `true`.
