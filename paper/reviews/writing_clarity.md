# Review: Jinx papers (branch `devin/paper-revision`, commit 3080800)

Scope: `paper/empirical/main.tex` (IEEE, 5 pages built) and `paper/tooldemo/main.tex` (ACM, 3 pages built). I rebuilt both PDFs from source in a clean copy: they compile with no errors and no undefined references, so "not built correctly" means content and layout problems, not a broken build. The acmart class does print warnings (finding 20). I read every page as an image and checked numbers against `experiments/results/*`, `src/jinx_pr/data/weights*.json`, `experiments/bench_v2/eval2.py` and `docs/venue_notes.md`. Line numbers refer to `main.tex` in each folder.

Severity: **major** = a reviewer would likely flag it, or the claim is wrong or misleading. **minor** = a clarity or polish fix.

---

## A. Correctness of claims (fix first)

### 1. [major, both] Headline accuracy and headline speed come from two different Jinx setups
- **Where:** Abstract (emp. l.18, tooldemo l.17), emp. RQ2 l.115, tooldemo l.95, Fig. pareto.
- **Problem:** The "Jinx" row (R@1 0.901, 2.5% false alarms) is `Jinx + MiniLM, LR (current tool)`, i.e. with the optional embedding model (`--embed`). The 22 ms / 229 ms latency is `summary.json → latency → "lexical features ms/query"`, which is the setup *without* MiniLM (`make_paper_extras.py` l.36, `make_figures.py` l.93). The default install and the CLI example in Fig. 2 use the lexical weights (`weights.json`), whose R@1 is **0.889** (`\ROnejinxLex`). So the papers pair the accuracy of one setup with the speed of another, and the Pareto figure puts the MiniLM model at the lexical time.
- **Fix:** Either (a) report the default (lexical) Jinx as the headline: R@1 0.889, FAR 3.2% (`false_alarms.csv`: "Jinx lexical, LR" 0.032), 22 ms; or (b) measure CPU latency with MiniLM switched on and report that. In both cases, add one sentence: "Jinx has two settings: the default uses only text and code signals (R@1 0.889, 22 ms per PR); with the optional local MiniLM model it reaches 0.901 (X ms)."

### 2. [major, both] At the shipped threshold, Jinx warns about fewer than half of the real duplicates
- **Where:** tooldemo §2.4 l.44, abstract l.17; emp. abstract l.18, Fig. operating.
- **Problem:** `weights.json` says: "intercept shifted so score 0.5 = median top-1 logit of cross-author queries". By design, about half of true cross-author duplicates score below 0.5. `false_alarms.csv` confirms this: at the 2.5% false-alarm point, Jinx ranks the right PR first **and** flags it for only **47.1%** of cross-author pairs (INTRUDE + time: 44.2%). The abstracts say only "ranks the true duplicate first for 0.901", so a reader will think 90% of duplicates get a warning comment. This is the number a maintainer actually experiences.
- **Fix (tooldemo l.44):** "Jinx flags a candidate when its score reaches 0.5. At this setting it flags the right PR for 47% of cross-author duplicates and raises a false alarm on 2.5% of PRs that have no duplicate. Maintainers who want more warnings can lower the threshold with `--threshold`; Fig. X shows the trade-off." Add the same two numbers to both abstracts. Mark this operating point (2.5%, 0.47) on Fig. operating.

### 3. [major, empirical] The number of bots tested is wrong
- **Where:** Contributions l.31 ("five open-source duplicate-PR bots"), Strategies l.79 ("contrib-guard (two versions), Simili, PRSense, PRism and vector-triage").
- **Problem:** The 66-strategy study (`eval2.py` l.53–55; `random_pair_vs_live_queue.csv`) has only **three** bots: contrib-guard/phoenix (exact port), Simili (re-implementation) and PRSense (re-implementation). PRism, vector-triage and contrib-guard/balyakin appear only in the earlier v1 benchmark (`experiments/results_v1/`), and no number from them is reported in the paper.
- **Fix:** Either add the three missing bots to the v2 evaluation (no API cost, they were already re-implemented with local MiniLM in v1), or change l.31 to "three open-source duplicate-PR bots" and l.79 to "contrib-guard (an exact port of its matching code), Simili and PRSense (re-implemented with local models because they need a paid service). Three more bots (a second contrib-guard, PRism, vector-triage) were tested on an earlier version of the benchmark; see the artifact."

### 4. [major, both] "Best of 66" and "fewer false alarms" claim too much
- **Where:** emp. Conclusion l.161 ("is the best of the 66 strategies we tested"), emp. abstract l.18 ("Jinx also raises fewer false alarms"), tooldemo l.17.
- **Problem:** `All signals, LR` is higher than Jinx on every column of Table I (0.906 / 0.974 / 0.935 / 1.6%), and Haiku + Jinx has fewer false alarms (1.8%). The R@1 differences are within noise (`paired_cross_author.csv`: All-LR − Jinx = +0.6 points, CI −1.2 to +2.5). Saying "best" is not supported, and "fewer false alarms" does not say fewer than which method.
- **Fix (l.161):** "...a cheap combination of text, code, link and timing signals is as accurate as any of the 66 strategies we tested (no strategy beats it with confidence)." Abstract: "Jinx also raises fewer false alarms than the classic detector (2.5% against 4.6%)". Add one sentence in RQ2 to explain why you ship Jinx and not All-signals LR (it needs six embedding models and BM25 indexes; Jinx needs at most one small local model).

### 5. [major, empirical] The "success test" is vague and called "pre-registered" with no record
- **Where:** l.92 (whole sentence in italics), abstract l.18, l.107, l.161.
- **Problem:** The test reads "by a meaningful, CI-backed margin ... we say so plainly". "Meaningful" has no number, "best baseline" is not defined, and the rule is not stored anywhere public. `REPORT.md` l.11 says it was "pre-registered by the user", and the best baseline was chosen as "the best baseline that does not use Jinx's own signals". A reviewer will ask where it is registered.
- **Fix:** Remove the italics and replace l.92 with: "Before running the study we fixed one success test: Jinx must beat the strongest baseline that does not use Jinx's signals (INTRUDE + time, Recall@5 0.953) on cross-author Recall@5, with a 95% confidence interval that lies entirely above zero." Write "fixed in advance" instead of "pre-registered", unless you can cite a time-stamped record (an OSF entry, or a commit hash plus date).

### 6. [major, both] Table I hides the real wins and mixes up its baselines
- **Where:** `generated/tab_main.tex`, emp. Table I l.95–97, tooldemo Table 1 l.83.
- **Problem:**
  1. The owner asked for "our wins to be highlighted". But the Jinx row has no bold value at all: every bold value goes to All-signals LR or the cascade, which are Jinx variants. A reader sees our tool winning nothing.
  2. "Claude Haiku 4.5 alone" sits in the baseline block, but it only re-ranks Jinx's top 5. Its R@5 (0.971) equals Jinx's by construction (`paired_cross_author.csv`: dR@5 = 0.0 exactly). It is not an independent baseline.
  3. "Links only" (R@1 0.839, 3.8% FA) beats the "classic detector" INTRUDE + time (0.810, 4.6%). The text never says so, and a reviewer will spot it.
- **Fix:**
  - Split the table into "Jinx and methods built on Jinx" and "Independent baselines".
  - In the Jinx row, mark each value that is significantly better than the best independent baseline (for example ▲ for a CI above zero: R@1 and MRR against INTRUDE + time; all four columns against contrib-guard).
  - Bold the best value *among independent baselines* and say so in the caption: "▲ = Jinx is better than every independent baseline, 95% CI above zero."
  - Move Haiku-alone into the Jinx block, with the footnote "re-ranks Jinx's top 5, so its Recall@5 equals Jinx's".
  - In RQ1 (l.100) add: "A simple rule that checks only for a shared issue or a mention already beats INTRUDE + time on Recall@1 (0.839 against 0.810), because agents often link the PR they replace."

### 7. [major, empirical] The RQ3 "classic detector wins" sentence mixes two populations
- **Where:** l.123.
- **Problem:** Every other result is on cross-author pairs. This sentence switches to "all relations" (n=287), where INTRUDE wins (0.826 vs 0.784). On cross-author pairs the result reverses (n=34: Jinx 0.941, INTRUDE 0.882; `CLAIM_AUDIT.md`). The next sentence ("This fits the trained Jinx weights...") is a guess that the paper does not test.
- **Fix:** "When two PRs make the same code change but describe it differently, the classic detector does better over all pairs (0.826 against 0.784, n=287, mostly self-replacements), while Jinx does better on the 34 cross-author pairs (0.941 against 0.882)." Delete the "fits the trained weights" sentence, or back it with the actual weight values.

### 8. [major, empirical] RQ4 and the Conclusion overstate the random-pair finding
- **Where:** l.129 ("agree only partly (Kendall τ = 0.75)"), l.161 ("random-pair AUC is a poor guide"), contribution l.33.
- **Problem:** τ = 0.75 (p ≈ 9e-19, `summary.json`) means strong agreement across all 66 strategies. The real finding is narrower: AUC saturates for strong methods (21 of 25 combined methods have AUC > 0.98) while live-queue R@1 still spans 0.851–0.906. The bug-report analogy (l.26) also leads the reader to expect a big ranking change that the data does not show.
- **Fix (l.129):** "Over all 66 strategies the two rankings agree well (Kendall τ = 0.75). The problem is at the top: 21 of the 25 combined methods reach an AUC above 0.98, so random pairs cannot tell them apart, while their live-queue Recall@1 still ranges from 0.851 to 0.906." Conclusion: "Random-pair AUC separates weak from strong methods but cannot choose among strong ones."

---

## B. Dual submission and venue fit

### 9. [major, both] The two papers overlap too much for two separate submissions
- **Where:** tooldemo Table 1 is the same file as emp. Table I (`generated/tab_main.tex`). tooldemo Fig. 3 = emp. Fig. 2 (forest), tooldemo Fig. 4 = emp. Fig. 3 (pareto), and Fig. 1 is identical in both. Both abstracts lead with the same three numbers (0.901 / 0.778 / 0.810). The empirical paper lists Jinx as a contribution (l.35) and puts its architecture in Fig. 1.
- **Problem:** `docs/venue_notes.md` (your own notes from the call pages) says: FSE Tool Demos rejects a tool that is "already the main contribution of a research paper", and RENE requires that the main results table of one paper is not the main contribution of the other. As written, Jinx is a main contribution of both papers, and both have the same main table and figures.
- **Fix:**
  - *Empirical:* drop the Jinx contribution bullet (l.35) and move Fig. 1 out (replace it with a figure of the live-queue set-up, see finding 12). Call the method "the learned signal combination (released as Jinx [cite demo])", and frame the paper around detectors on agent PRs, the live-queue vs random-pair evaluation, and the negative results.
  - *Tool demo:* replace Table 1 with a 4-row table (Jinx default, Jinx + MiniLM, INTRUDE + time, best bot), add threshold, false alarms and flagged recall, and cite the empirical paper for the full 66-strategy table. Drop the forest plot. Use the space for tool-only material (finding 21).
  - Each paper should cite the other as "under review".

### 10. [major, empirical] Length and framing do not match the target track
- **Where:** l.1 says the target is ICPC 2027 RENE, 10 + 2 pages. The built PDF is about 4.5 pages.
- **Problem:** RENE is a track for replications and negative results. The paper is framed as "here is a better tool". Its strongest RENE-style results are buried: the fixed success test fails, LLM judges do not help, classic detectors only partly hold up on agent PRs, and random-pair AUC saturates. At 4.5 pages it also lacks the depth a 10-page track expects: no worked examples, no error analysis, no description of the queue construction rules, and no per-repository spread.
- **Fix:** Retitle along the lines of "Do Duplicate-PR Detectors Work on Coding-Agent PRs? A Live-Queue Replication with Negative Results". Lead the abstract with the replication question. Use the free pages for: (a) a worked example pair; (b) the error analysis that already exists in `REPORT.md` §10 (34 misses; in 44% of them the top-ranked PR is the new PR author's own other open work; median queue size of misses is 104); (c) results by queue size; (d) more detail on how the queue is built. If the team wants to stay at about 5 pages, pick a short-paper track instead.

---

## C. Clarity for a non-expert reader

### 11. [major, empirical] The abstract is long and full of undefined terms
- **Where:** l.18 (about 230 words).
- **Problem:** "Recall@5", "re-rankers", "LLM judges", "embeddings", "pre-registered success test" and "classic research detector" appear with no explanation. The order of problem → gap → contribution → result gets lost.
- **Suggested replacement (about 170 words, numbers via macros):**
  > Coding agents now open pull requests (PRs) at large scale, and many repeat work that is already waiting for review. Existing duplicate-PR detectors were built for PRs written by people and were tested on random pairs of PRs. We test them the way a maintainer uses them: when a new PR arrives, the detector must find its duplicate among the PRs open in that repository at that moment. From the AIDev dataset we build 1,867 such cases (342 where two different authors opened the PRs) and 2,965 PRs with no duplicate. Across 66 strategies, from text matching and existing bots to embedding models and large language models (LLMs), a simple learned mix of text, code, link and timing signals puts the true duplicate first for 90% of cross-author cases, against 78% for the best existing bot and 81% for a classic research detector, in 22 ms per PR on a CPU. LLMs add cost but not accuracy. Two negative results stand out: no method clearly beats the classic detector at placing the duplicate in its top five, and duplicates that change different files remain unsolved.

  (Adjust "90%" and "22 ms" after fixing finding 1.)

### 12. [major, empirical] There is no concrete example of the problem
- **Where:** Introduction l.22–36.
- **Problem:** A non-expert never sees what a duplicate agent PR looks like, or what "the live queue" means in practice. The tooldemo already has a real pair (huggingface/transformers #44134 / #44110).
- **Fix:** Add a small Fig. 1 that shows a timeline. PR A is opened, PRs B and C are still open, then new PR #44134 arrives, and the detector must pick #44110 out of 19 open PRs. Mark random-pair evaluation ("is this one pair a duplicate?") against live-queue evaluation ("which of these 19 is it?"). Add one sentence in l.24: "For example, in huggingface/transformers an agent opened #44134 with the same one-file refactor as the still-open #44110."

### 13. [minor, both] Technical terms are used before they are defined
- **Where and fix** (one short clause each, at first use):
  - TF-IDF / BM25 (emp. l.75, tooldemo l.41): "word-overlap scores that give rare words more weight".
  - embedding (l.78): "a small neural model that turns text into a vector, so that similar meanings get nearby vectors".
  - cross-encoder / re-ranker (l.81): "a model that reads both PRs together and re-scores the top few candidates".
  - LR (l.80): spell out "logistic regression" in the tooldemo too. GBDT appears in the Fig. randlive legend but never in the text: write "gradient boosting".
  - AUC (l.129, Fig. randlive axis): "the chance that a random duplicate pair scores higher than a random non-duplicate pair".
  - Kendall τ (l.129): "rank agreement from −1 to 1".
  - MRR "points" (l.105): say "MRR is shown ×100".
  - "silver labels" (l.53): already defined, good. "subsumed" (l.70): already defined, good.
  - "cascade" (l.110, Table I): "Jinx first, then a slower model re-checks its top candidates".
  - Fig. 1 box "#ref": write "mentions the other PR".

### 14. [minor, empirical] Long, crowded sentences
- **l.26:** "Second, most detectors were scored on *random pairs*: a balanced set ..., often 100,000 random pairs as in INTRUDE." → Split into: "Second, most detectors were scored on random pairs. INTRUDE, for example, was tested on 100,000 pairs, half duplicates and half not."
- **l.70:** This 6-clause sentence lists every audit input and every label. → "We asked Claude Haiku 4.5 to label each pair as *duplicate*, *replacement*, *subsumed* (one PR's change is inside the other's larger work), *related* or *unclear*. It saw the closing comment, both titles, the start of both descriptions and the changed files."
- **l.110:** Seven numbers in one paragraph. → Move them into Table I or a small table, and keep one sentence: "No embedding, re-ranker or LLM judge ranks more duplicates first than Jinx (Table I)."
- **l.107:** "The results hold when..." contains two CIs. → Keep the R@1 gain in the text and move the R@5 gain to the table caption.

### 15. [minor, both] Emphasis and typography
- Emp. l.92: the whole success-test sentence is in italics (the owner asked for no whole-paragraph emphasis). Use roman text (finding 5).
- Emp. l.30–35: italics on *LiveQueue* and on many defined terms is fine at first use. Also italicising every later use (*Recall@1*, *MRR*, *query*, *no-duplicate queries*) makes the text noisy, so drop the repeats.
- Table I: "**Jinx (ours)**" is bold, but the caption says "Best value per column in bold". Use shading only.
- l.105: "nearly half as many false alarms (2.5% against 4.6%)": the ratio is 0.54. Write "about half as many".
- Fig. heatmap row "different agents" vs Table classes "cross-agent": use one term.

---

## D. Figures

### 16. [major, both] Fig. pareto (accuracy vs. time): detached labels, legend in the data area, wrong Jinx time
- **Problem:**
  - "+ Qwen 7B (top-5)" is printed under the Jinx marker, far from its own square at (≈300 ms, 0.892). "+ Claude Haiku" and "+ MiniLM cross-enc." also need leader lines to be read.
  - The "runs on CPU / GPU / API" legend sits inside the plot, at y≈0.82, where it looks like data.
  - Jinx + MiniLM is drawn at the lexical-only time (finding 1).
  - Text l.115 and tooldemo l.95 say "up to two orders of magnitude". Haiku is 913 ms per pair × 5 ≈ 4.6 s ≈ **200×** the 22 ms.
- **Fix:** Use direct labels next to each marker, with short leader lines (or `adjustText`). Move the legend outside, above the axes, in one row. Draw Jinx default and Jinx + MiniLM as two points. Text: "up to about 200 times slower".

### 17. [major, empirical] Fig. randlive (AUC vs. R@1): the key region cannot be read
- **Problem:** The point of the figure is the 25 combined methods inside the yellow band (AUC 0.98–1.0), but they are drawn as one overlapping blob. The "learned (LR / GBDT)" colour is invisible under the other points. The INTRUDE leader line crosses the cluster, and the Jinx label points at no single dot.
- **Fix:** Add a right-hand zoom panel (x 0.97–1.0, y 0.84–0.91) with marker shape per family. Label Jinx, All-LR, INTRUDE + time and the best LLM judge there. Draw the main panel in grey with the band outlined. Caption: "Right: zoom on the 25 combined methods; AUC barely changes (0.977–0.991) while Recall@1 ranges over 5.5 points."

### 18. [minor, empirical] Fig. heatmap: contradicts the text and is hard to read
- **Problem:**
  - Row D is bold at **Links only 0.76**, above Jinx (0.66). Yet the text says "no method we tried handles them well" and never mentions Links. In `eval2.py` l.48, Links-only = shared issue + mention + 0.001 × TF-IDF, so on pairs without links it becomes TF-IDF ranking. The "Links only" column on the "no link at all" row is therefore just TF-IDF on raw text.
  - Bolding the best value in row C (n=10) and row D (n=29) suggests differences that are 1–3 pairs.
  - Cell text is about 5 pt at column width.
- **Fix:** Rename the column "Links, else TF-IDF". Grey out or hatch rows with n < 30 and add "(small n)" to the label. Drop the bold on those rows. Make it `figure*` or drop to 6 columns so the text is 7 pt or more. Add to l.121: "On class D, the links-then-text rule does best (0.76), which suggests these pairs are found mainly through references, not code."

### 19. [minor, empirical] Fig. operating and Fig. forest: missing the shipped setting and the false-alarm gain
- **Operating:**
  - The legend box covers the All-LR and Haiku curves between 2% and 10%.
  - Haiku + Jinx is above Jinx from 5% onward (0.713 vs 0.632 at 5%; 0.827 vs 0.749 at 10%; `operating_curve.csv`), and the text does not say so.
  - **Fix:** Move the legend below the axis. Add a star at Jinx's shipped point (2.5%, 0.47). Add to l.134: "Haiku + Jinx catches more at budgets of 5% or more, at about 200 times the cost."
- **Forest:** False alarms are a headline claim but have no row. **Fix:** Add a "False alarms (lower is better)" row from `paired_false_alarms.csv`, with the sign flipped so that right = better. Label the x-axis "Jinx minus baseline (percentage points; MRR ×100)".

---

## E. Build quality and tool-demo content

### 20. [major, both] TODO text and placeholders are visible in the PDFs
- **Empirical references:**
  - [5], [14] and [20] print "tODO: verify author first names" / "tODO: authors". These come from `note={TODO...}` fields in `refs.bib` l.10, 12, 20.
  - [17] "Xu et al." and [18] "Sarkar" have no venue or arXiv ID.
  - [3] mixes initials and full names.
  - The Data Availability section is a red TODO.
- **Tool demo:** six red TODOs (video URL, tool URL ×2, repository/tag, companion citation, pilot results).
- **Tool demo acmart warnings:** CCS concepts and keywords are "mandatory for papers over two pages", and no figure has a `\Description` (alt text). The `review` option adds line numbers, and the header still says "Conference'17, Washington, DC".
- **Fix:** Move the TODOs out of `note=` into LaTeX comments, and fill in authors from arXiv. Add `\begin{CCSXML}...`, `\keywords{duplicate pull requests, coding agents, GitHub Actions}`, a `\Description{...}` for every figure, and `\acmConference[FSE '27]{...}`. Remove `review` before the final build. If the target is the ICPC tool demo (deadline 19 Nov), it must be IEEE format, not ACM.

### 21. [major, tooldemo] It reads as a short version of the empirical paper, not a tool demo
- **Where:** §3 Evaluation l.82–95. The paper uses 3 of the 4 allowed pages.
- **Problem:** There is no screenshot of the actual PR comment, no walkthrough of a maintainer's view, no setup or config options (`--threshold`, `max_open_prs`, `--embed`), no evaluation of the explanations, and no live usage (marked TODO). Reviewers of demo papers look for these.
- **Fix:** Use the page freed by finding 9 for:
  1. A screenshot of the Jinx comment on a sandbox PR, which is the main demo figure.
  2. A short "Using Jinx" scenario: what the maintainer sees, how to change the threshold, and what happens on reopen.
  3. Run time vs. queue size (you have queue p50 40 / p90 314; the latency p90 of 229 ms comes from large queues).
  4. Design choices: why `pull_request_target` is safe here (the Action reads the PR through the API and never checks out PR code, so say so explicitly), and why it never closes or labels a PR.

### 22. [minor, tooldemo] Claims about other tools that the paper's own code contradicts
- **Where:** l.24.
- **Problem:**
  - "Small open-source bots ... compare only the titles and descriptions of PRs" is false for two of them. PRSense as evaluated uses 0.35 × diff similarity + 0.20 × changed-file Jaccard (`eval2.py` l.55), and contrib-guard/balyakin uses title Jaccard + same files (`results_v1/ranking.csv`).
  - The claims about commercial tools (CodeRabbit "Related PRs", "document duplicate detection for issues, not for PRs") have no citation. `docs/commercial_tools_comparison.md` says they were checked from documentation only.
- **Fix:** "Most small open-source bots ... compare the PR text, and a few add a simple changed-file overlap; none uses line-level code overlap, issue links and timing together." Add footnote URLs for the documentation pages, plus "as documented on [date]".

### 23. [minor, tooldemo] Training vs. test data, and the 200-PR cap, are not stated
- **Where:** §2.4 l.44, §2.1 l.35, Introduction l.26 ("tuned and tested on agent PRs").
- **Problem:**
  - The shipped weights were trained on all 4,832 queries (`weights.json` note), while the reported numbers come from 5-fold cross-validation that holds out whole repositories. The text reads as if the same model was tuned and tested on the same data.
  - The Action reads at most 200 open PRs, but the queue p90 is 314 and the maximum is about 1,900 (`DATA_CARD.md`). In large repositories older duplicates are never seen.
- **Fix:** "The reported numbers come from five-fold cross-validation that holds out whole repositories; the shipped model is then retrained on all data." "By default the Action reads the 200 most recent open PRs (configurable with `max-open-prs`); in 10% of our queues more than 314 PRs were open."

### 24. [minor, empirical] The label audit uses the same model that is tested as a judge
- **Where:** §III-E l.70; Threats l.139.
- **Problem:** Claude Haiku 4.5 decides which labels count as "valid" (clean subset, l.107), and it is also one of the judges being compared. A reader may suspect circularity. The planned 30-pair human check (CHECKLIST) is not mentioned.
- **Fix:** Add to Threats: "The audit model (Claude Haiku 4.5) is also one of the judges we evaluate; the clean-subset analysis compares only Jinx and INTRUDE + time, neither of which uses it." Run and report the 30-pair human spot-check before submission (κ against the audit).

---

## Summary of priorities
1. Fix the numbers that are mismatched or wrong: findings 1, 2, 3, 4, 7, 8.
2. Split the two papers' contributions before submitting both: findings 9 and 10.
3. Restructure Table I so the wins are visible and honest: finding 6.
4. Rewrite the abstract, add a worked example, define terms: findings 11–14.
5. Rework the figures: findings 16–19.
6. Remove TODOs and fix the acmart metadata; add tool-demo content: findings 20–23.
