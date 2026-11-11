# Review: Jinx papers (empirical + tool demo), branch `devin/paper-revision` @ 3080800

Reviewer stance: ICSE/FSE/MSR empirical-SE reviewer. Review only. No commits, no API spend.
I checked every number cited below against `experiments/results/*.csv`, `summary.json`, `experiments/label_audit/*`, the evaluation code (`experiments/bench_v2/eval2.py`, `experiments/bench_v1/build_bench.py`) and the tool code (`src/jinx_pr/*`). Where I recomputed something myself, I say so.

## Summary verdict

All the macros match the result files. I found no wrong number. The problems are in what the numbers are said to mean, and in two parts of the benchmark design that a hostile reviewer will find quickly:

1. Jinx's strongest feature (`cand_open`) exploits the 7-day "recently closed" rule that builds the benchmark queues. INTRUDE + time does not get this feature, and the deployed Action never sees closed PRs. (Finding 1)
2. The `mention_ref` link feature can read text that was written after the new PR existed. (Finding 2)
3. Readers will take "R@1 0.901 … with 2.5% false alarms" to mean 90% of duplicates are caught at 2.5% false alarms. At that threshold Jinx correctly flags **47.1%**. (Finding 3)
4. The "Jinx" row in the tables (with MiniLM), the 22 ms latency (lexical features only) and the shipped Action (lexical, no MiniLM) are three different setups. (Finding 4)

The writing is mostly plain and clear. The rendered PDFs still show `TODO`s, broken bibliography notes and ACM template placeholders. That is most likely what the owner means by "not built correctly".

Severity key: **MAJOR** = a reviewer could reject over it, or a claim is not supported. **minor** = presentation, or a fix that is cheap and still worth doing.

---

## A. Validity of the results (do these first)

### 1. MAJOR · both · `cand_open` + 7-day grace window gives Jinx an edge from how the benchmark was built
- **Where:** empirical §III-C "Building the live queue" (main.tex l.55), §IV Jinx paragraph (l.87), Table I. Tool demo §2.3 (l.41), §2.1 (l.35).
- **Problem:** Each queue holds open PRs **plus PRs closed in the last 7 days** (`build_bench.py` l.27, `GRACE = 7 days`). Jinx has a feature `cand_open` ("older PR still open"), and it has the **largest weight in the shipped model by far**: 1.85 in `weights_emb.json` and 1.89 in `weights.json`. The next largest are 0.91 and 0.84. The recently closed PRs are almost always wrong answers, so this feature mostly learns how the queues were built. Two consequences:
  - (a) The INTRUDE + time baseline does **not** get this feature (`eval2.py` l.65: `INTRUDE = [...]` + `log_gap_hours` only). Part of the +9.1-point R@1 gain may come from the queue rule, not from better duplicate detection.
  - (b) The deployed Action only fetches `state=open` PRs (`action.py` l.66). In real use `cand_open` is always 1, so the benchmark is easier than real use, and the 0.5 threshold was calibrated on a different score distribution.
- **Fix:** This needs no API money. Re-run `eval2.py` locally with three ablations and report them in a short "Robustness" paragraph:
  1. Queues with open PRs only (matches the Action).
  2. Jinx without `cand_open`.
  3. INTRUDE + time + `cand_open`.

  Add to Threats/Links: *"Queues also contain PRs closed in the previous seven days. Jinx's 'still open' signal can use this to rule them out, while a deployed Action only sees open PRs. Table X repeats the main comparison on open-only queues."* If the R@1 gain shrinks a lot under these ablations, the headline claim has to change.

### 2. MAJOR · both · Link feature can use text written after the new PR (timing leakage)
- **Where:** empirical §IV (l.77 "one mentions the other"), §VI-C "Links make part of the benchmark easy" (l.123), §VII-B (l.141–142). Tool demo Fig. 2.
- **Problem:** `features.py` l.60: `mention_ref = cand.number in new.mentions or new.number in cand.mentions`. The second half means the *older* PR's text mentions the *newer* PR's number. That text can only have been written after the newer PR existed. AIDev stores the final title/body, so such edits leak the label. The repo's own report already says so: `docs/phase2_benchmark_report.md` l.248, *"AIDev stores the final body, so some of these were edited in later."* The papers don't mention it. "Links only" reaches R@1 0.839, above every existing bot.
- **Fix:** In the evaluation, use only the forward direction (`cand.number in new.mentions`) and report how many gold pairs depend on the backward direction. Add to §VII-B: *"AIDev stores the final text of each PR, so some mentions were added after the duplicate was found. We therefore count only mentions in the new PR, and we also report pairs with no link at all."* The no-link subset (n=140, Jinx 0.821 vs 0.643) is the cleanest result you have. Put it in the abstract.

### 3. MAJOR · both · R@1 and false-alarm rate are presented as if they described the same alerts
- **Where:** empirical abstract (l.18), §V (l.90), Conclusion (l.161). Tool demo abstract (l.17): *"Jinx ranks the true duplicate first for 0.901 of the pairs … with 2.5% false alarms"*. Tool demo §2.4 (l.44).
- **Problem:** Each strategy's threshold is the **median** training-fold top-1 score of cross-author duplicates (`eval2.py` l.194–199). So by design only about half of duplicates pass the threshold. `false_alarms.csv`, column *cross-author correct alerts*: Jinx flags the right PR for **47.1%** of cross-author duplicates at its 2.5% false-alarm rate (INTRUDE + time 44.2% at 4.6%; all-signals LR 48.8% at 1.6%). Tool demo §2.4 says the same thing about the shipped threshold 0.5. A reader will take the abstract to mean "catches 90%, 2.5% false alarms".
- **Fix:** Add a macro `\alertJinx{47.1}` (from `false_alarms.csv`) and rewrite:
  - §V: *"To count false alarms we set, for each strategy, the threshold at which half of the training-fold cross-author duplicates would be flagged, and count how often the top candidate of a no-duplicate query passes it."*
  - Tool demo abstract: *"Jinx ranks the true duplicate first for 0.901 of the pairs (best existing bot 0.778; classic detector 0.810). At its default threshold it warns on 2.5% of PRs that have no duplicate and gives a correct warning for 47% of cross-author duplicates; the rest still appear in its ranked list."*
  - Fig. 6 (operating curve) is the honest view. Mark Jinx's default point (2.5%, 0.471) on it.

### 4. MAJOR · both · The evaluated, timed and shipped setups are different
- **Where:** empirical abstract ("needs 22 ms per PR"), §VI-B (l.115), Fig. 3. Tool demo abstract, §2.3, §3, Fig. 4.
- **Problem:**
  - The "Jinx" row is `Jinx + MiniLM, LR (current tool)`, which uses `weights_emb.json` and the MiniLM embedding.
  - The 22 ms (p90 229 ms) is `summary.json → latency → "lexical features ms/query"`, which is `t_lex` only (`eval2.py` l.237). It excludes MiniLM encoding and GitHub API calls.
  - The Action never builds an embedder (no `embed` in `action.py` or `action.yml`). So it runs the **lexical** model: R@1 0.889, false alarms 3.2% (`false_alarms.csv`).
  - Fig. 3 plots MiniLM accuracy at the lexical latency (`make_figures.py` l.93: `base = LAT["lexical features ms/query"]`).
- **Fix:** Pick one setup, then make the tables, the latency and the Action match it. Cheapest option: report the shipped lexical Jinx as "Jinx" (R@1 0.889; R@1 vs Jinx+MiniLM −1.2 points [−3.2, +1.0], recomputed from `paired_cross_author.csv`), and keep "Jinx + MiniLM (optional)" as a second row. Otherwise, time MiniLM encoding on CPU and turn on `--embed` in the Action. Either way, say what the time includes: *"22 ms for feature computation and scoring on one CPU core, excluding GitHub API calls."*

### 5. MAJOR · empirical · The pre-registered test failed, and the headline moved to Recall@1
- **Where:** abstract (l.18), §V (l.92), §VI-A (l.107), §VII-D (l.148).
- **Problem:** This is the first thing a hostile reviewer will raise. The only test fixed in advance was cross-author Recall@5 against the best baseline, and it failed. The abstract then leads with R@1 and false alarms, which were not fixed in advance. Other gaps:
  - No public, dated pre-registration exists. `REPORT.md` l.11 says *"pre-registered by the user"*.
  - "Meaningful margin" is never given a number.
  - "Best baseline" is chosen as the best one *not using Jinx's signals* (REPORT.md). The paper doesn't say this.
  - §VII-D claims that fixing the main comparison handles multiple comparisons, but every R@1 and false-alarm claim is post-hoc.
- **Fix:**
  - Either link a dated commit or OSF entry, or replace "pre-registered" with *"fixed before we ran the study (recorded in commit `<sha>`, dated …)"*.
  - In §V, state the margin and how the baseline was chosen.
  - Add one sentence in §V: *"Only the Recall@5 test was planned in advance; all Recall@1, MRR and false-alarm comparisons are exploratory."*
  - Reorder the abstract so the failed test comes **before** the R@1 gain. Suggested abstract sentence: *"Our planned test asked whether Jinx finds more duplicates in its top five than the best earlier detector; it does not (+1.8 points, 95% CI −0.9 to +5.2). In exploratory analyses Jinx ranks the true duplicate first more often (0.901 vs 0.810) and raises fewer false alarms (2.5% vs 4.6%)."*

### 6. MAJOR · both · "LLM judges do not improve on it" and "best of the 66 strategies" go against the result files
- **Where:** empirical abstract ("LLM judges do not improve on it"), §VI-B (l.110 "LLM judges do not help either"), Conclusion (l.161 "is the best of the 66 strategies"). Tool demo §3 (l.95 "none of them ranks more duplicates first").
- **Problem:** For R@1 the differences are tiny: Haiku+Jinx −0.3 [−2.3, +2.4], all-signals LR +0.6 [−1.2, +2.5] (`paired_cross_author.csv`, reference = Jinx). But for false alarms they are **significantly better than Jinx** (`paired_false_alarms.csv`):
  - all-signals LR: −0.98 points [−1.62, −0.44]
  - Haiku+Jinx: −0.78 [−1.30, −0.35]

  In `operating_curve.csv`, Haiku+Jinx catches more than Jinx at every budget from 2% upward (0.497 vs 0.436 at 2%, 0.713 vs 0.632 at 5%, 0.827 vs 0.749 at 10%). All-signals LR beats Jinx at every budget. Also, "no difference found" does not prove "no improvement".
- **Fix:**
  - Abstract: *"LLM judges and larger models do not rank more duplicates first, though Claude Haiku and the all-signals model raise somewhat fewer false alarms, at much higher cost."*
  - Conclusion: *"… is the best of the cheap, CPU-only strategies we tested."*
  - State plainly why you ship Jinx and not the all-signals LR: it needs BM25 plus several neural encoders, including code models run on a GPU (`ALL` in `eval2.py` l.66).
  - For the null claims, use the CI: *"the R@1 difference is within ±2.5 points"*.

### 7. MAJOR · empirical · RQ4 (random pairs vs live queue) claims more than the data shows
- **Where:** contributions bullet 4 (l.33), §VI-D (l.129), Fig. 5 and its x-axis label, Conclusion's last sentence, abstract's last sentence.
- **Problem:**
  1. Kendall τ = 0.75 (p ≈ 9e-19, `summary.json`) is **strong** agreement, not "only partly".
  2. The strategy with the best random-pair AUC (all-signals LR, 0.991) is also the one with the best live R@1 (0.906). Random pairs would have picked the same winner.
  3. These are not the classic random pairs from INTRUDE (100k pairs from across the dataset). `eval2.py` l.218–224 compares the gold PR against **one random wrong candidate from the same live queue**. The x-axis label "AUC on random PR pairs (the usual evaluation)" is therefore wrong.
  4. Among the top methods the spread is 0.85–0.91, which is about the width of one method's CI (Jinx [0.868, 0.931]). I recomputed τ among the 24 methods with AUC > 0.98: τ = 0.32 (p = 0.03). That is the real, narrower finding.
- **Fix:**
  - Rename the measure to "pairwise AUC (one gold vs one random queue PR)".
  - Change the bullet to *"evidence that pairwise AUC saturates (24 strategies above 0.98) and cannot separate the strongest methods, while live-queue Recall@1 still can"*.
  - In §VI-D, replace "agree only partly" with *"agree overall (τ = 0.75), but pairwise AUC cannot tell the strong methods apart: among the 24 strategies with AUC above 0.98 the agreement is weak (τ = 0.32)"*. Add the second τ as a macro.
  - Conclusion: replace "random-pair AUC is a poor guide" with *"pairwise AUC is too saturated to choose among strong detectors."*

### 8. MAJOR · empirical · The novelty claim against prior work is too strong
- **Where:** Introduction ¶3 (l.26 "most detectors were scored on random pairs"), Related Work §VIII-A (l.152 "None of this work … scores against live queues").
- **Problem:** Li et al. 2017 [6] already ranked candidates for each new PR. Their abstract: *"For a new-arriving pull-request, we compare the textual similarity between it and other existing pull-requests, and then return a candidate list of the most similar ones … 55.3%–71.0% of the duplicates can be found."* A reviewer who knows that paper will treat the framing as a misrepresentation. OpenAlex also lists *PR-DupliChecker: detecting duplicate pull requests in fork-based workflows* (2024), which is not cited.
- **Fix:** Intro: *"Earlier work either classified balanced sets of PR pairs (e.g. INTRUDE) or ranked all earlier PRs of a project [6]. None restricted candidates to the PRs that were still open when the new PR arrived, measured false alarms on PRs that have no duplicate, or studied agent PRs."* Change §VIII-A to match, and cite and position PR-DupliChecker after checking it.

### 9. MAJOR · empirical · Statistical reporting gaps
- **Where:** Table I, §VI-C, Fig. 4, §VII-D.
- **Problem:**
  - Table I gives CIs only for false alarms. R@1, R@5 and MRR have none. The CIs exist in `strategies_by_group.csv` (Jinx R@1 [0.868, 0.931]; INTRUDE [0.767, 0.857]).
  - RQ3 compares classes C (n=10) and D (n=29) with no CIs. For example, class C "Jinx 0.700 vs INTRUDE 0.400" rests on 10 pairs; the best class-C methods have CI [0.5, 1.0].
  - There are more than 65 paired comparisons and about 15 subgroups, with no correction for multiple comparisons.
  - The paper never gives the number of repositories, or the share of the largest repository. Readers need both to judge the cluster bootstrap.
- **Fix:**
  - Put CIs in Table I, as in the false-alarm column, or add a Δ-vs-INTRUDE column (see 13).
  - In RQ3, give CIs, and say *"(n=10; too few to compare methods)"* for class C.
  - Use Holm correction for the secondary comparisons, or label them exploratory (see 5).
  - In §III, report the number of repositories and the largest repository's share of queries.

### 10. MAJOR · empirical · RQ3 leaves out that the link-only rule is best on class D
- **Where:** §VI-C (l.121), Fig. 4.
- **Problem:** On cross-author class D (no shared files, n=29), **Links only** and the fine-tuned BGE re-ranker reach R@1 **0.759**. Jinx, all-signals LR and Haiku+Jinx reach 0.655 (`strategies_by_group.csv`). Fig. 4 even puts Links only 0.76 in bold, but the text names only Jinx, INTRUDE and Haiku. That suggests the "intent duplicates" Jinx misses are often found through explicit links, which ties back to Finding 2.
- **Fix:** Add: *"On class D the best strategy is the link-only rule (0.759, 95% CI 0.58–0.90). When two PRs share no files, an explicit link is often the only signal, and Jinx's learned weights give links too little weight here."* Then point to Finding 2's forward-only check.

### 11. MAJOR · both · Label validity depends on one LLM, which is also a competitor
- **Where:** empirical §III-E (l.70), §VI-A clean subset (l.107), §VII-A (l.139). Tool demo §4.
- **Problem:**
  - (a) Claude Haiku 4.5 audits the labels **and** competes as a judge (Haiku+Jinx). The clean-subset result then filters on Haiku's own judgements.
  - (b) The audit prompt shows the linking comment ("superseded by #N") to the model (`audit_silver.py` l.61–62). That pushes it toward "duplicate/replacement".
  - (c) No human check yet. `CLAIM_AUDIT.md` says *"a human read of 30 audit labels"* is still to do.
  - (d) "Cross-author" means a different GitHub login. The tool demo's own Fig. 2 example begins *"Migrated from …/pull/44110 (original account: @fumadari)"* (`examples/new_pr.json`). That is one person using two accounts, counted as cross-author.
- **Fix:** This costs no API money. Two authors label 100 random cross-author pairs without seeing the comment. Report Cohen's κ and agreement with Haiku. Add to §VII-A: *"The auditing model is also one of the compared judges and saw the closing comment, so the audit may be biased toward accepting labels. A human check of 100 pairs gives κ = …"*. Also add: *"We define cross-author by GitHub account; some pairs are one person using two accounts."*

### 12. minor · empirical · Negative queries are a biased sample
- **Where:** §III-C (l.55), §VII-A.
- **Problem:** No-duplicate queries are **merged** PRs with no duplicate-like comment (`build_bench.py` l.48). Merged PRs differ from typical incoming PRs: they are higher quality and have fewer competitors. So the false-alarm rate may not carry over.
- **Fix:** Add a threat sentence: *"No-duplicate queries are merged PRs; incoming PRs that are later closed may trigger false alarms more often."* If cheap, also report false alarms on a sample of unmerged PRs with no duplicate comment.

---

## B. Tables and figures (owner asked: wins highlighted, sharper, clearer)

### 13. MAJOR · both · Table I never highlights a Jinx win, and mixes in rows that depend on Jinx
- **Where:** `paper/generated/tab_main.tex` (built by `make_paper_tables.py`). Empirical Table I (l.95–97), tool demo Table 1 (l.83).
- **Problem:**
  - All-signals LR has the best value in every column, so the Jinx row has no bold. The owner's request ("our wins highlighted") is not met.
  - "Claude Haiku 4.5 alone" sits in the *baselines* block, but it re-ranks Jinx's top 5. Its R@5 (0.971) equals Jinx's by construction, and the same holds for every top-5 re-ranker.
  - The table has no cost column, although cost is where Jinx clearly wins.
- **Fix:**
  - (a) Add a column **Δ R@1 vs INTRUDE+time [95% CI]**, and mark † when the CI excludes zero. The data is in `paired_cross_author.csv`.
  - (b) Add **Runs on / ms per PR**: Jinx "CPU, 22 ms" (once Finding 4 is fixed), all-signals LR "GPU encoders", Haiku "API, ~4.6 s, $7.25".
  - (c) Bold the best value in each block, not only the best overall. Shade the Jinx row as now, and add a caption note: *"†: 95% CI of the difference vs INTRUDE + time excludes zero."*
  - (d) Move "Haiku alone" into block 2 and footnote: *"Re-rankers reorder Jinx's top 5, so their R@5 equals Jinx's."*

  Example row: `\rowcolor{jinxrow}\textbf{Jinx (ours)} & 0.901 & 0.971 & 0.932 & 2.5 & \textbf{+9.1}\textsuperscript{†} & CPU, 22\,ms \\`

### 14. minor · both · Forest plot (Fig. 2 / Fig. 3) leaves out the clearest win
- **Where:** `fig_forest.pdf`, `make_figures.py` l.42–58.
- **Problem:** The false-alarm difference is significant and in Jinx's favour, but it is not shown. From `paired_false_alarms.csv`: Jinx − INTRUDE = **−2.1 points [−2.7, −1.6]**; Jinx − contrib-guard = **−9.2 [−12.1, −6.4]**.
- **Fix:** Add a fourth row, "fewer false alarms", with the sign flipped so that right means better. Then the plot shows three green wins out of four against INTRUDE. State in the caption that rows are cross-author pairs and that the false-alarm row uses 2,965 no-duplicate queries.

### 15. minor · empirical · Fig. 3 (accuracy vs time) has no CIs, an unclear legend, and a wrong Jinx point
- **Where:** `fig_pareto.pdf`, `make_figures.py` l.93–125.
- **Problem:**
  - Every point lies within Jinx's own R@1 CI [0.868, 0.931]. Without error bars the plot shows differences that are not significant.
  - The "runs on" legend sits inside the data area at y≈0.82, where it looks like three more data points.
  - The "+ Claude Haiku" label is far from its marker.
  - Haiku time = 5 × the median time per call, as if the calls ran one after another. That should be stated.
  - The Jinx point is wrong (Finding 4).
- **Fix:**
  - Add vertical 95% CI bars (`R@1 lo/hi` from `strategies_by_group.csv`).
  - Move the legend above the plot (`loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3`).
  - Place labels next to their markers.
  - Add points for Jinx lexical and Haiku alone.
  - Caption: *"API time assumes the five calls run one after another."*

### 16. minor · empirical · Fig. 5 (random vs live) is crowded at the top right and mislabelled
- **Where:** `fig_randlive.pdf`, `make_figures.py` l.162–177.
- **Problem:**
  - About 25 points overlap in the region 0.97–0.99 × 0.79–0.91, which is the region the argument is about.
  - "learned" (dark blue) and "cascade" (teal) are hard to tell apart.
  - The "INTRUDE + time" label crosses data points.
  - The x-axis label is wrong (Finding 7).
- **Fix:**
  - Add an inset or second panel zoomed to AUC 0.97–1.0, with CI bars.
  - Use a different marker shape for each family (circle, square, triangle, diamond…) as well as colour.
  - Use leader lines placed away from the cluster.
  - Rename the axis to *"pairwise AUC (gold vs one random queue PR)"*.

### 17. minor · empirical · Fig. 4 (heatmap) shows small groups as if they were as reliable as large ones
- **Where:** `fig_heatmap.pdf`, `make_figures.py` l.73–90, caption (l.119).
- **Problem:**
  - Rows with n=10 and n=29 look just as certain as the row with n=1,525.
  - The self-replacement row is a different population from the other rows (which are cross-author), with no visual break.
  - The row is called "different agents" while the text says "cross-agent".
  - Bolding the best value per row rewards ties and noise. For example, in row C, Haiku+Jinx 0.80 = 8 of 10.
- **Fix:**
  - Hatch or grey the cells in rows with n < 30, and add to the caption: *"Rows with fewer than 30 pairs are hatched; differences there are not reliable."*
  - Draw a horizontal rule above the self-replacement row.
  - Use one name for that group throughout.
  - Put CIs for rows A–D in the supplementary material, or add an appendix table built from `tab_classes.tex`.

### 18. minor · both · Architecture figure: unreadable output box, and text that doesn't match the tool
- **Where:** `paper/figures/arch.tex`. Empirical Fig. 1 (l.84), tool demo Fig. 1 (l.29).
- **Problem:**
  - The yellow output box is set in about 4 pt type, which can't be read in print.
  - Its mock text "Jinx: possible duplicate" differs from the real CLI output ("DUPLICATE? #44110 score 1.00", which I reproduced by running `jinx_pr.cli` on `examples/`).
  - "#ref" is jargon.
  - MiniLM is shown as "optional", but the results use it (Finding 4).
- **Fix:**
  - Use at least 7 pt in all boxes, or replace the mock output with a short label such as "ranked list + one reason per signal".
  - Copy the real output wording.
  - Change "#ref" to "mentions the other PR".
  - Label the arrows with step numbers 1–5 so they match tool demo §2 ("five steps").
  - The colour scheme is good. Keep it.

### 19. minor · empirical · Fig. 6 (operating curve) should show where Jinx actually runs
- **Where:** `fig_operating.pdf`, §VI-D (l.134).
- **Problem:** The text says Jinx and all-signals LR beat INTRUDE and contrib-guard at every budget. That is true. But the plot also shows Haiku+Jinx and all-signals LR **above** Jinx, and the text doesn't mention it. The shipped lexical model is missing from the plot.
- **Fix:**
  - Add Jinx lexical.
  - Mark the default threshold as a point at (2.5%, 0.471).
  - Add one sentence: *"Adding Claude Haiku or all signals catches more duplicates at the same false-alarm budget (e.g. 0.71 and 0.70 vs 0.63 at 5%), at a much higher cost."*
  - The x positions are categorical. Use markers without connecting lines, or a real log axis.

---

## C. Tool-demo paper

### 20. MAJOR · tooldemo · The CLI example is trivial and comes from the training data, and there is no real GitHub screenshot
- **Where:** Fig. 2 (l.49–62), §2.6, §4.
- **Problem:**
  - The example's new PR literally says *"Migrated from …/pull/44110"*, so it is the easiest kind of case.
  - The shipped weights were trained on **all 4,832 benchmark queries** (`weights.json` → `note`), so this PR is in the training data.
  - Tool-demo reviewers expect to see the tool in use (the Action comment on a PR). The paper shows only a terminal.
  - About 1 of 4 pages is empty.
- **Fix:**
  - Replace Fig. 2 with a cross-author pair that has no link and that Jinx ranks first under cross-validation. `errors_cross_author.csv` and the ranks file make this easy to find.
  - Add a screenshot of the real Action comment on a sandbox repository. This needs no API money, only a test repo.
  - Use the free space for a short usage walk-through (*"Maya maintains …"*) and a tool comparison table: Jinx vs contrib-guard, Simili, PRSense, PRism, vector-triage, doppelgänger, CodeRabbit "Related PRs". Columns: uses code? explains matches? needs paid API? runs in CI?

### 21. MAJOR · tooldemo · Uncited claims about other tools, the 200-PR limit, and Action security
- **Where:** §1 ¶2 (l.24), §2.1 (l.35), §2.6 workflow (l.65–79).
- **Problem:**
  - (a) *"Commercial AI review tools document duplicate detection for issues, not for PRs"* and the CodeRabbit claim have no citation or URL.
  - (b) The Action reads at most 200 open PRs, but the benchmark's 90th-percentile queue is **314** (`REPORT.md` l.7). So for more than 10% of queries the deployed tool would not see the full queue, and the paper doesn't say how this affects accuracy.
  - (c) `pull_request_target` with write permissions is a known risky setup. Reviewers will ask whether Jinx checks out untrusted code.
- **Fix:**
  - (a) Cite each tool's documentation URL with an access date, or delete the claim.
  - (b) Say how PRs are chosen when there are more than 200 (most recent first, per `action.py` `sort=created&direction=desc`), and report recall on queues truncated to 200. The benchmark can compute this offline.
  - (c) Add: *"Jinx reads PR metadata and diffs through the API and never checks out or runs PR code, so `pull_request_target` does not expose secrets to forked PRs."*

---

## D. Build, writing and presentation

### 22. MAJOR · both · The rendered PDFs show TODOs, broken references and template placeholders
- **Where:** empirical References [5], [14], [20] print *"tODO: verify author first names"* and *"tODO: authors"* (from `note=` fields in `refs.bib` l.10, 12, 20). Data Availability (l.164) shows a red `[TODO: …]`. The tool demo has six red TODOs (l.17 ×2, l.80, l.95, l.98, l.101), the header *"Conference'17, July 2017, Washington, DC, USA"*, the line *"ACM Reference Format … https://doi.org/10.1145/nnnnnnn.nnnnnnn"*, review-mode line numbers, and no CCS concepts or keywords. acmart's own log warns: *"ACM keywords are mandatory…"*, *"CCS concepts are mandatory…"*, 4× *"possible image without description"*. I rebuilt both papers in a temporary copy: they compile, with one small overfull vbox in the tool demo.
- **Fix:**
  - Remove the `note=` fields, and fill in the missing author names (CUPID, arXiv 2308.10022: probably T. Zhang, I. C. Irsan, F. Thung, D. Lo; please verify).
  - In the tool demo, add `\acmConference`, `\settopmatter{printacmref=false}`, `\renewcommand\footnotetextcopyrightpermission[1]{}`, `\begin{CCSXML}…`, `\keywords{duplicate pull requests, coding agents, GitHub Actions}`, and `\Description{…}` for each figure.
  - Turn off `review` mode for the shared PDF.
  - Replace TODO URLs with an anonymised link (e.g. anonymous.4open.science) and remove the video TODO from the abstract until a URL exists.
  - Have `make` fail if the log contains "TODO".

### 23. minor · both · Plain language: long abstract, italic full sentence, unexplained terms
- **Where:**
  - Empirical abstract (l.18, about 230 words, 10 numbers).
  - §V l.92: a whole sentence in italics. The owner asked not to emphasise whole sentences or paragraphs.
  - Table I caption: three lines of small caps.
  - "cries wolf" (l.134).
  - "LR", "MRR", "cascade" and "re-ranker" are used in the abstract or early text before being explained.
  - "#ref", "self-replacement" and "silver" are used in figures and need a gloss.
- **Fix:**
  - Cut the abstract to about 170 words with at most 6 numbers.
  - Write the l.92 test as normal text: *Before running the study we fixed one success test: Jinx must beat the best baseline on cross-author Recall@5, and the 95% confidence interval of the gain must exclude zero (margin: … points).*
  - Shorten the Table I caption to *"Cross-author results (n=342). Shaded: our tool. Bold: best in each block. †: 95% CI of the gain over INTRUDE + time excludes zero."*
  - Replace "cries wolf" with "raises false alarms".
  - Define "re-ranker" as *"a model that re-scores only the top few candidates"* at first use.
  - Suggested abstract opening: *"Coding agents open many pull requests (PRs) that repeat work already waiting for review. We test duplicate-PR detectors the way a maintainer would use them: when a PR arrives, the tool must find its duplicate among the PRs open at that moment."*

### 24. minor · empirical · Unused space, missing error analysis, and the byline
- **Where:** whole paper. The PDF is about 4.4 pages. The comment at l.1 says the target is IEEE 10+2.
- **Problem:** The space is there for the ablations in Findings 1, 2 and 21, the human label check (11), and a short error analysis. `errors_cross_author.csv` already lists Jinx's misses with what it ranked first instead, but the paper says nothing about why Jinx fails. The byline is "Harshul Jain, Saurabh Yergattikar, Tanya Sah". Please confirm it is intended, since other papers from this group use a different co-author list.
- **Fix:** Add §VI-E "Where Jinx fails". Sort the 34 cross-author misses into groups such as "top-ranked PR from the same author", "class D" and "queue > 100", with one example each. Confirm the byline.

---

## What a hostile reviewer attacks first, in order
1. "The pre-registered test failed and the authors switched metrics" (5).
2. "The gain over INTRUDE comes from a feature that uses how the queues were built" (1), and "link features read text written after the PR" (2).
3. "Prior work already ranked candidates for each new PR" (8).
4. "The labels are checked only by an LLM that is also a competitor, and it saw the label comment" (11).
5. "τ = 0.75 is agreement, not disagreement" (7).
6. Tool demo: "trivial in-sample example, no real deployment, TODO links" (20, 22).

## Fixes that need no new data (about a day)
3, 4 (text option), 5, 6, 7, 8, 13, 14, 15–19, 22, 23.

## Fixes that need local re-runs, with no API or GPU money
1 (ablations), 2 (forward-only mentions), 9 (CIs, Holm), 10, 21b (truncate queues to 200).
The benchmark data path in `build_bench.py` (`/home/ubuntu/research/prdupecheck/data/`) is not in this VM, so I could not run these myself.

## Needs people's time
11 (human label check of 100 pairs), 20 (Action screenshot on a sandbox repo).
