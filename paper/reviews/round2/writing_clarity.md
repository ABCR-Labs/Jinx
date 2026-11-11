# Round 2 review: Jinx papers (ABCR-Labs/Jinx `main`, commit 84c0351)

**Scope.** I reviewed `paper/empirical/main.tex` (IEEE, 5 pages) and `paper/tooldemo/main.tex` (ACM, 3 pages) for writing clarity, consistency between the two papers, and overlap between them. I rebuilt both papers from source in a clean copy. Both compile without errors, and the committed PDFs match the source text exactly.

**How claims were checked.** I checked numbers against `experiments/results/`, `experiments/results_grace7/`, `experiments/bench_v2/{eval2,ablations}.py`, `experiments/impact/duplicate_cost.py`, `paper/scripts/make_paper_extras.py` and `docs/venue_notes.md`. The raw AIDev data is not on this VM, so I did not recompute anything that needs it.

**Notation.** "E l.N" means `paper/empirical/main.tex` line N. "T l.N" means `paper/tooldemo/main.tex` line N.

---

## Blockers

### B1. The empirical paper still says it tested six bots; the study ran three
- **Where:** E l.33 ("six open-source duplicate-PR bots"), E l.65 ("contrib-guard in two versions, Simili, PRSense, PRism, vector-triage").
- **Evidence:** `experiments/bench_v2/eval2.py` l.67–69 defines only three bot strategies: contrib-guard/phoenix (exact port), Simili (re-implemented) and PRSense (re-implemented). `random_pair_vs_live_queue.csv` and `false_alarms.csv` also contain only these three. PRism, vector-triage and contrib-guard/balyakin exist only in `experiments/results_v1/` (the old benchmark). Round 1 flagged the same problem.
- **Fix:**
  - E l.33: "three open-source duplicate-PR bots".
  - E l.65: "existing bots (contrib-guard, ported exactly; Simili and PRSense, re-implemented with local models because they need a paid service)".
  - If you want to mention the other three, add one sentence: "PRism, vector-triage and a second contrib-guard were tested only on an earlier version of the benchmark."

### B2. The two papers still overlap too much to be submitted at the same time
- **Shared material:**
  - The same main table file (`generated/tab_main.tex`): E Table I and T Table 1, including the caption text.
  - The same false-alarm figure (`fig_far.pdf`): E Fig. 2 and T Fig. 3.
  - The same architecture figure (E Fig. 1, T Fig. 1).
  - The same cost numbers (17%, 54%) and replay numbers (46%, 35%) in E RQ1 and in T's abstract and §4.
- **Jinx is claimed in both:** the empirical paper still lists "Jinx, an open-source tool" as a contribution (E l.35) and opens with Jinx's architecture (E l.67–70). The tool demo relies on "our companion study" (T l.34) without citing it.
- **Why it matters:** `docs/venue_notes.md` says FSE Tool Demos rejects a tool that is "already the main contribution of a research paper". It also says the RENE main table should not be the other paper's main contribution.
- **Fix:**
  - *Empirical:* delete the contribution bullet at E l.35. Move the architecture figure out and describe Jinx in two sentences as "one of the learned combinations (released as a tool [cite tool demo, under review])".
  - *Tool demo:*
    - Cite the empirical paper as under review wherever T l.34 and §4 lean on it.
    - Replace Table 1 with a 4-row table (Jinx, Jinx without MiniLM, INTRUDE + time, contrib-guard) with these columns: false alarms, share of duplicates flagged at the shipped threshold, latency, and "explains code matches" (yes/no).
    - Drop `fig_far.pdf` from the tool demo, or plot only the tool-relevant methods with a different design.
    - Keep the cost and replay numbers in one paper only. I suggest the empirical one; the tool demo can cite it in one line.

### B3. The tool demo does not meet the venue's availability requirements
- **Where:** T l.87 (`uses: <owner>/jinx-pr@v1`) and T l.111 ("will be public with the camera-ready version, together with a short demo video").
- **Problem:** `docs/venue_notes.md` records two requirements:
  - ICPC Tool Demos: "source or binaries **must be publicly available**".
  - FSE Tool Demos: "link to source expected" and "link to a screencast expected".

  Neither venue reviews anonymously (ICPC "not anonymous", FSE "single-blind"), so there is no reason to hide the repository. As written, the paper can be rejected without review.
- **Fix:** Publish the repo, the Marketplace listing and the video before submission. Put the real `ABCR-Labs/jinx-pr@v1` in the YAML, and put the repository URL and video URL in the abstract and in §6.

---

## Major

### M1. The cost numbers and audit numbers come from the old pair set, not the one the paper uses
- **Where:**
  - Cost numbers: E l.19 (abstract), E l.79 (RQ1), T l.20 (abstract).
  - Audit numbers: E l.62, T l.108.
- **Evidence:**
  - `duplicate_cost_summary.json` has `"all": n = 1867` and `"cross-author": n = 342`. Those are the 7-day-window pairs. Every other result in both papers uses 1,767 pairs and 313 cross-author pairs.
  - The macros `\dupLateOneH`, `\dupLateOneD`, `\dupEffort`, `\dupLinesMed` and `\dupAllLines` all come from that file (`make_paper_extras.py` l.108–114).
  - The label audit also covers 342 cross-author pairs (`\auditCrossN`). E l.62 even prints "For the 342 cross-author pairs", directly after the paper says there are 313.
- **Fix:** Rerun `experiments/impact/duplicate_cost.py` on the 1,767 open-only pairs. It needs only the local AIDev parquet files and no API. Then regenerate the macros. If that is not possible before the deadline, add the n in both places: "(measured on all 1,867 labelled pairs, 342 cross-author, before the open-only filter)". For the audit: "The audit covered the 342 cross-author pairs of the first benchmark design; 264 of the 313 pairs used here were judged valid."

### M2. "8.0 million added lines were thrown away" overstates the waste
- **Where:** E l.79.
- **Evidence:** `duplicate_cost_summary.json` gives 8.03 M lines in total, of which 7.27 M come from self-replacements. In a self-replacement the same author re-opens a PR, usually with the same change, so most of those lines were not lost. The total is also taken over the old 1,867 pairs (M1).
- **Fix:** "The closed cross-author PRs had a median of 127 added lines; we do not know how much of that code was reused in the PR that was kept." Drop the 8.0 M total, or say clearly that most of it is self-replacement code that was usually resubmitted.

### M3. "Closed PRs are always wrong answers" is false, and the ablation's setting is not stated
- **Where:** E l.99.
- **Evidence:** In the 7-day design, the true duplicate was itself already closed at query time for 18 cross-author pairs. `ablations.py` l.141 prints this count, and it is stored as `\nGraceCand = 18` in `make_paper_extras.py` l.91. The ablation numbers that follow (0.839, 0.892) are from the 7-day queues (`ablations.csv`, setting "benchmark queues"), but the sentence does not say so.
- **Fix:** "In the 7-day design, closed PRs were almost always wrong answers (the true duplicate was already closed in only 18 of 342 cross-author pairs), and Jinx has a signal for 'the older PR is still open'. In that design, removing the signal drops Jinx from 0.901 to 0.839, and adding it to INTRUDE + time lifts that method from 0.810 to 0.892."

### M4. "The Qwen judges add nothing" contradicts Table I
- **Where:** E l.115.
- **Evidence:** Table I marks Qwen2.5-14B + Jinx with ‡, meaning significantly fewer false alarms than Jinx (1.3% against 1.8%). `false_alarms.csv` also gives Qwen2.5-7B + Jinx 1.5% and Qwen2.5-Coder-7B + Jinx 1.4%.
- **Fix:** "...and the Qwen judges do not change Recall@1. Like Haiku, the larger Qwen models lower false alarms (Qwen2.5-14B + Jinx: 1.3%), and they run on a local GPU without API cost."

### M5. The tool demo's main pitch ("quiet") is stronger than the data
- **Where:** T title l.15, T l.34, T l.103 ("Where Jinx stands out is quietness").
- **Evidence (`false_alarms.csv`):**
  - The link rule has fewer false alarms than Jinx: 1.2% against 1.8%.
  - INTRUDE + time is not clearly different: 2.0%.
  - "Jinx features, gradient boosting" is lower still: 1.1%.
  - Jinx is clearly quieter only than contrib-guard (5.5%) and TF-IDF (3.5%). The other two bots are also well above Jinx: Simili 4.5%, PRSense 4.7%.
- **Replay evidence (`replay_impact.csv`):** INTRUDE + time warns correctly on 47.3% of cross-author duplicates, against 46.0% for Jinx. So the benefit claimed at T l.105 is not specific to Jinx.
- **Fix:**
  - Keep the title, but make the claim precise. T l.103: "Jinx raises about a third of the false alarms of the best existing bot (1.8% against 5.5%) and is as quiet as the best research detector (INTRUDE + time, 2.0%). A rule that fires only on a shared issue or cross-reference is quieter still (1.2%), but it says nothing when no link exists and gives no code-level reason."
  - T l.105: "...46% of cases; the research detector would do about the same (47%). What Jinx adds is the packaging: reasons a maintainer can check, a CI Action and no API key."
  - E l.81: report the replay for both methods.

### M6. One idea goes by six names
- **Where:** "live queue" / *LiveQueue* (E l.32, l.46), "real-use queues" (Table I caption, Fig. 3 legend, T Table 1), "open-only queues" (E l.27, T l.48), "the real open-PR queue" (E l.41, l.135), "PRs that were really open" (T l.20), "benchmark queues (as in paper)" (`ablations.csv`). The old design is also called "the queue design of our first draft" (E l.57), "queues with PRs closed in last 7 days" (Fig. 3) and "the seven-day window" (E l.127).
- **Problem:** A general reader cannot tell whether these are the same thing. This matters most in a paper whose title is about how the queue is built.
- **Fix:** Define two names once, in §III-C, and use only those in the text, captions, figure legends and both papers:
  - **open-only queue:** the PRs open when the new PR arrived, at most 200.
  - **7-day queue:** the same, plus PRs closed in the previous 7 days.

  Keep *LiveQueue* only as the benchmark's name. Apply the same rule to method names: "Link rule" (Table I) vs "Links only" (heatmap); "cross-agent" (`tab_classes`) vs "different agents" (heatmap); "Claude Haiku 4.5 + Jinx" vs "Haiku + Jinx".

### M7. The empirical abstract is long and leans on undefined terms
- **Where:** E l.19 (about 270 words).
- **Problems:**
  - Terms that are not defined: embeddings, re-rankers, LLM judges, Recall@1, "points".
  - Wording that is unclear: "the open-PR queue ... holds PRs closed in the previous seven days" (a queue of open PRs that holds closed PRs), "flagged by a person" (a comment marking the duplicate), and "doomed PR" (emotive).
  - The cost finding comes first, but the title promises a finding about the queue.
- **Suggested replacement (about 190 words; update the cost numbers after M1):**
  > Coding agents open many pull requests (PRs) that repeat work already waiting for review. A duplicate-PR detector must spot such a PR when it opens, by comparing it with the PRs that are open in the repository at that moment. We test how well detectors do this on agent PRs, using 1,767 duplicate pairs (313 opened by different authors) and 2,965 PRs with no duplicate from the public AIDev dataset. We compare 66 strategies, from word matching and existing bots to neural text models and large language models (LLMs). Our main finding is that the way the test queue is built decides the winner. If the queue also keeps PRs closed in the last seven days, our learned detector, Jinx, ranks the right PR first 9 points more often than a classic research detector. If the queue holds only open PRs, as a real tool sees it, Jinx, the classic detector and a simple rule that checks for a shared issue or a link all rank the right PR first 91–94% of the time, with no clear winner. The methods differ more in false alarms (1.8% for Jinx against 5.5% for the best existing bot) than in ranking. Duplicates are also costly: 17% are noticed only after a day. Duplicates that change different files remain hard for every method.

### M8. The intro and Threats sections narrate the team's own process
- **Where:** E l.27 ("An independent review of our own draft asked whether this design favoured Jinx ... It did."), E l.127 ("none of us saw its effect until an independent review").
- **Problem:** Reviewers do not need the backstory, and "It did." reads as a fragment. It also invites the question of what else was missed.
- **Fix:**
  - E l.27: "A common way to build such a benchmark keeps recently closed PRs in each queue. We show that this choice favours any detector that knows whether a PR is still open, including our own: with closed PRs in the queue Jinx wins clearly, and with open PRs only the advantage disappears."
  - E l.127: "Queue design. Our first design, documented in the data card, kept PRs closed in the last seven days; RQ3 shows its effect. Other choices, such as the 200-PR cap, may also matter."

### M9. The success test is still vague and cannot be passed on this data
- **Where:** E l.75.
- **Problem:** "A clear, CI-backed gain over the best baseline on cross-author Recall@5" leaves "clear" and "best baseline" undefined. Recall@5 is now 0.978–0.990 for every strong method (Table I), so no method could show a clear gain.
- **Fix:** "Before the study we fixed one success test: Jinx's cross-author Recall@5 must beat the strongest baseline that does not use Jinx's signals, with a 95% confidence interval above zero. It fails in every setting. On open-only queues, all strong methods find the duplicate in their top five at least 98% of the time, so this test cannot separate them."

### M10. Table I's highlighting is hard to read and partly reversed
- **Where:** E Table I and T Table 1 (`generated/tab_main.tex`); captions at E l.85 and T l.94.
- **Problems:**
  - Green is used to mark a *baseline's* worse value (contrib-guard 5.5%, TF-IDF 3.5%). Most readers take green to mean "good".
  - The underlined "best baseline" values (Link rule: R@1 0.936, MRR 0.957, false alarms 1.2%) are all better than Jinx's, and the caption does not say so.
  - "-0.0" appears in the last column.
  - The tool-demo abstract (T l.20) says Jinx ranks first "as often as the best methods (0.927; ... a link rule 0.936)", which reads like a contradiction.
- **Fix:**
  - Mark the Jinx cell instead, for example "1.8 ▼†". Caption: "† Jinx has significantly fewer false alarms than this row (paired 95% CI)." Or use orange/red for the baseline cells.
  - Print "0.0" instead of "-0.0".
  - T l.20: "Jinx's ranking is statistically tied with the best methods we tested (Recall@1 0.927; classic detector 0.914; link rule 0.936)".

### M11. The empirical Strategies section is one 130-word sentence
- **Where:** E l.65.
- **Problem:** Seven families, about 25 named models and nested brackets ("logistic regression (LR) or gradient boosting over the INTRUDE signals plus a time feature ..., which we call INTRUDE + time, over the Jinx signals, and over all signals").
- **Fix:** Use a 7-row table (family | what it compares | examples), or seven bullets with one line each. Define INTRUDE + time in its own sentence: "INTRUDE [7] is a classic research detector that combines text, code and issue signals; we add the time between the PRs [8] and call it INTRUDE + time."

### M12. The tool demo still has no demonstration of the tool in use
- **Where:** T §3–§4. The paper uses 3 of the 4 allowed pages.
- **Problem:** There is no screenshot of the GitHub PR comment, no walkthrough of what a maintainer sees, and no example of a false alarm and how its reasons let a maintainer dismiss it quickly. Fig. 2 shows only CLI output in lexical mode, while the default Action uses MiniLM.
- **Fix:** Use the space freed by B2 for:
  1. A screenshot of a Jinx comment on a sandbox PR, which is the main demo figure.
  2. A short scenario of four or five sentences: a PR opens, the comment appears, the maintainer reads the reasons and closes one PR, and Jinx updates its comment on reopen.
  3. One real false alarm from `alerts.parquet` with its reasons.

### M13. The empirical paper is still about half the length of its target track
- **Where:** E l.1 says "ICPC 2027 RENE, IEEE 10+2 pages"; the PDF is 5 pages.
- **Fix:** Either target a short-paper track, or use the extra pages for material that already exists:
  - A worked example pair, with a timeline figure of an open-only queue next to a 7-day queue.
  - The error analysis in `errors_cross_author.csv`.
  - The full ablation table (`ablations.csv`: forward-only mentions, open-only, without MiniLM).
  - Results by queue size.

  For a general reader, the timeline figure would explain the paper's main idea better than any paragraph.

---

## Minor

### m1. Terms used without a definition (both papers)
Add a short clause at first use:
- **embedding:** "a small neural model that maps text to a vector so that similar texts are close".
- **re-ranker / cross-encoder:** "a model that reads both PRs together and re-scores the top few candidates".
- **LLM judge:** "a large language model asked whether two PRs are duplicates".
- **BM25, TF-IDF:** "word-overlap scores that weight rare words more".
- **template-stripped:** "with agent boilerplate removed".
- **AUC** (E l.104, Fig. 4): "the chance that a random duplicate pair scores higher than a random non-duplicate pair".
- **Kendall τ:** "rank agreement, from −1 to 1".
- **MRR:** state the formula in words ("1 divided by the rank of the true duplicate, averaged").
- **"points":** "percentage points".
- **paired differences:** "both methods scored on the same queries".
- **INTRUDE:** say in the tool demo what it is.
- **#ref** (Fig. 1, Table I): "a mention of the other PR's number".

### m2. Long sentences
- E l.73 packs five ideas into one paragraph: cross-validation, three metrics, threshold, flagged vs ranked, bootstrap. Split it into three short paragraphs: metrics, false alarms, statistics.
- E l.79: split after "(mean 46 hours)".
- T l.91 mixes security, the `embed` switch, latency, the CLI and the 200-PR cap. Split it into "Security", "Speed" and "Limits" sentences.
- E l.115: one sentence carries four numbers and two CIs. Move the CI into Table I.

### m3. Fig. 4 (random pairs vs open-only queue) is hard to read
- **Problems:**
  - The annotation "span Recall@1 0.92 to 0.93" overlaps the x-axis tick labels.
  - The "INTRUDE + time" label runs into the "LLM judge" legend entry.
  - About 30 points overlap inside the yellow band.
  - E l.104 says "hides differences in the other direction", which a general reader will not follow.
- **Fix:**
  - Move the legend below the plot and add a zoom panel for AUC > 0.95.
  - Caption: "Random-pair AUC (x) and open-only-queue Recall@1 (y) agree on which methods are weak, but among strong methods AUC is near 1 and does not predict the ranking."
  - Text: "Random pairs have the opposite problem: they make strong methods look the same."

### m4. Fig. 5 (heatmap) labels and bolding
- "Links only" on the "no link at all" row (0.86) is really TF-IDF: the rule's score is shared issue + mention + 0.001 × TF-IDF (`eval2.py`, `Links only` definition), so without links it falls back to TF-IDF. Rename the column "Link rule (else TF-IDF)", or grey out that cell.
- Rows C (n=10) and D (n=25): drop the bold, since one pair changes the value by 4–10 points. Add "(small)" to their row labels.
- E l.110 says the link rule "does well" on D. Add that contrib-guard does too (0.84): both beat Jinx (0.72), which is worth stating.

### m5. Fig. 6 (operating curve)
The legend sits on top of the curves between 2% and 10%. Move it outside the axes. Mark the shipped setting (Jinx at 1.8% false alarms, 46% flagged) with a star, so readers can link this figure to the tool demo's threshold.

### m6. Fig. 7 (Pareto)
The y-axis runs from 0.91 to 0.94, so differences of 1–2 points, which Table I shows are not significant, look large. Either add 95% CI bars or start the axis at 0.85 and add "differences in Recall@1 are within noise" to the caption. The "+ BGE reranker (top-10)" label sits on the dashed link-rule line; nudge it.

### m7. Tool-demo latency misses CI start-up time
T l.91 says "0.7 s at the median ... once the model is loaded" (`package_latency.json`: 706.7 ms median, 3.68 s p90, 300 queries). A real Action run also installs the package and downloads MiniLM. Report one measured end-to-end Action run time, or add: "the first run also downloads the 90 MB model; GitHub's cache avoids this afterwards" (only if the Action really caches it).

### m8. Tool-demo template leftovers
- The running header still reads "Conference'17, July 2017, Washington, DC, USA". Set `\acmConference`.
- acmart warns "ACM reference format is mandatory" because `printacmref=false`, and "No city present for an affiliation" (×3).
- The `review` option prints line numbers. Keep it only if the venue asks for it.

### m9. Wording that a general reader may stumble on
- E l.93 "cry wolf": use "raise false alarms".
- E l.19 "doomed PR": use "the PR that was later closed".
- E l.135 "rewarded a signal that a deployed tool cannot use" is inaccurate: a deployed tool can use "is the PR open", it just never sees closed PRs. Write "rewarded a signal that only helps when closed PRs are in the queue".
- T l.34 "it should be right when it speaks, quiet otherwise" is fine, but follow it with the measured numbers.

---

## What improved since round 1
- References are complete: no TODOs print, and arXiv IDs have been added.
- The tool demo now has CCS concepts, keywords and figure descriptions.
- Latency is reported separately for the two modes and measured end to end.
- The shipped threshold and "flags about half" are stated.
- The claim about bots comparing only titles has been softened ("mostly").
- The `pull_request_target` safety note was added.
- Main claims are now framed as ties, not wins.
