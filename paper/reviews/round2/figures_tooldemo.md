# Round 2 review: figures, tables and tool demo (ABCR-Labs/Jinx `main` @ 84c0351)

I rendered both committed PDFs (110 and 250 dpi) and rebuilt them from source. Both build: the empirical paper is 5 pages, the tool demo 3. I checked the numbers against `experiments/results/`, `results_grace7/`, `action.yml`, `src/jinx_pr/` and `experiments/bench_v2/eval2.py`. No pushes and no API spend. The raw AIDev data was not used.

**Fixed since round 1:**
- The Jinx configuration is now the same in the table, the latency figures and the Action default.
- Table I has a difference column with CIs.
- The architecture steps are numbered to match the tool demo.
- The link rule is now listed as a baseline.
- The workflow is explained for safety.
- The CCS concepts and keywords are added.
- The bibliography TODOs are gone.

Labels: **E** = empirical, **T** = tool demo, **B** = both.

---

## Blocker

### B1. Table I prints at about 5 pt, and its CIs at about 3.5 pt
- **Where:** E Table I (l.84–86) and T Table 1 (l.94). Both come from `generated/tab_main.tex` through `\resizebox{\columnwidth}`.
- **Problem (measured):** The table's natural width is 503 pt. IEEE fits it into 252 pt and ACM into 241 pt, so it is scaled to about 0.50×. The numbers print at about 5 pt and the bracketed CIs at about 3.5 pt, which is unreadable on paper. The IEEE small-caps caption also runs to 6 lines.
- **Fix:**
  - Drop R@5 and MRR from the table. They range only 0.978–0.990 and 0.944–0.961 and carry no message; state them in one sentence.
  - Keep these columns: Strategy | R@1 | row − Jinx R@1 [CI] | False alarms % | row − Jinx FA [CI].
  - Remove the FAR CI brackets, since Fig. 2 already shows them.
  - Use `\small` with no `\resizebox`, or `table*` in E.
  - In the tool demo, cut to 5 rows: Jinx, Jinx without MiniLM, link rule, INTRUDE + time, contrib-guard.
  - Caption: "Cross-author pairs, real-use queues (n = 313). Differences are row minus Jinx with paired 95% CIs; bold = the CI excludes 0."

## Major

### B2. The "link rule" is not what the papers say it is
- **Where:** E abstract (l.19), l.88, l.110, l.135; T abstract (l.20), l.98, l.103; table row "Link rule (shared issue or #ref)"; Fig. 5 "Links only"; Fig. 6 "link rule".
- **Problem (verified):** `eval2.py` l.62 defines it as `same_issue + mention_ref + 1e-3 * text_tfidf_raw`, so ties are broken by TF-IDF. On the 118 pairs with no link at all it still reaches 0.856 R@1, which is TF-IDF doing the work. Newest-PR-first alone gets 0.314 on those pairs. Calling it "a rule that only checks for a shared issue or cross-reference" overstates how simple the baseline is that ties Jinx.
- **Fix:** Call it "link rule (shared issue or cross-reference, ties broken by TF-IDF)" in the table, all figures and the text. Also report the pure link rule, without the TF-IDF tie-break, as a separate row.

### T1. The tool demo's "quiet" pitch leaves out that the link rule is quieter and catches more at strict budgets
- **Where:** T title, abstract (l.20), §1 (l.34), §4 (l.103).
- **Problem (verified):**
  - Link rule false alarms are 1.2% against Jinx's 1.8%. The difference is −0.6 points (CI −1.3 to +0.05), so not significant, but it is lower.
  - The link rule's R@1 is 0.936 against Jinx's 0.927.
  - At a 1% false-alarm budget the link rule catches 44% of cross-author duplicates and Jinx 35% (`operating_curve.csv`).
  - The abstract compares Jinx only with contrib-guard (5.5%). A tool-track reviewer will ask why a maintainer should not use the link rule.
- **Fix:**
  - Abstract: "…raising 1.8% false alarms, about a third of the best existing bot (5.5%) and in the same range as a classic detector (2.0%) and a link rule (1.2%)."
  - Make the explanations the value: "Jinx matches the best simple baselines in recall and false alarms, and it adds what they lack: per-match reasons drawn from code (shared files, identical lines), a packaged Action, and a tunable threshold."
  - Retitle away from "Quiet" (for example "Explainable Duplicate Warnings…"), or justify the word against the link rule.

### T2. `embed: "true"` by default installs PyTorch with CUDA on every run, and cold-start time is not reported
- **Where:** `action.yml` l.19–30; T §3 (l.89–91, "0.7 s… once the model is loaded").
- **Problem (verified):**
  - `pip install ".[embed]"` pulls in sentence-transformers and then torch.
  - On Linux, torch 2.15 on PyPI requires `nvidia-cudnn-cu13`, `nvidia-nccl-cu13` and other CUDA packages, which are gigabytes of downloads.
  - `action.yml` has no pip or Hugging Face cache, so every PR run reinstalls torch and downloads MiniLM from the Hugging Face Hub.
  - The 0.7 s figure leaves out all of this.
  - The accuracy gain is small: lexical Jinx is 0.917 against 0.927 R@1 (difference +1.0 points, CI −0.9 to +2.7). False alarms are 1.9% against 1.8% (+0.16 points, CI −0.03 to +0.37).
- **Fix (either):**
  - Make `embed: "false"` the default and present MiniLM as an option ("no significant difference, 30× faster").
  - Or install CPU torch first (`pip install torch --index-url https://download.pytorch.org/whl/cpu`), add `actions/cache` for `~/.cache/pip` and `~/.cache/huggingface`, and report the total job time for a cold run and a warm run.
  - In both cases, add to T §3: "With `embed`, the runner downloads the MiniLM model (~90 MB) from Hugging Face; no PR content leaves the runner."

### T3. Install and availability statements cannot be checked by a reviewer
- **Where:** T l.87 (`<owner>/jinx-pr@v1`), l.91 (`pip install jinx-pr`), §6 (l.111); E Data Availability (l.138).
- **Problem (verified):** `https://pypi.org/pypi/jinx-pr/json` returns 404. The workflow uses a placeholder owner. Availability is promised only "with the camera-ready version". Tool tracks (FSE, ICSE and ICPC demos) usually require a tool link and a demo video at submission; check the target CFP.
- **Fix:**
  - Publish to PyPI, or write `pip install git+https://github.com/ABCR-Labs/Jinx`.
  - Tag `v1` and use `ABCR-Labs/Jinx@v1` in the snippet, or an anonymised mirror if the track is double-blind.
  - Put the video URL and repository URL in the abstract.
  - For E, give an anonymised artifact link now.

### T4. There is still no picture of the comment Jinx posts on a PR
- **Where:** T §2–3. Page 3 is about 75% empty.
- **Problem:** The PR comment is the main user interface and it is never shown. Fig. 2 is CLI output, and the mock-up in the architecture diagram is tiny. I raised this in round 1; it is the first thing a tool-track reviewer looks for.
- **Fix:** Add a screenshot of a real Jinx comment on a sandbox fork, replaying #44134 → #44110. Add callouts for the score, the reasons, the link to the older PR, and that Jinx updates the comment and never closes PRs. Caption: "The comment Jinx posts. The maintainer sees which open PR looks like a duplicate and why."

### E1. RQ1 cost figures use the 342-pair set; the rest of the paper uses 313
- **Where:** E abstract (l.19: 45%, 17%, 54%), l.79; T abstract (l.20: 17%, 54%).
- **Problem (verified):** In `duplicate_cost_summary.json`, the "cross-author" entry has n = 342 (0.453, 0.170, 0.541). That is the 7-day pair set, while the paper's cross-author set is n = 313. The replay in l.81 uses n = 313 (`replay_impact.csv`).
- **Fix:** Recompute the cost numbers on the 313 pairs, or say "(all 342 labelled cross-author pairs, before queue filtering)" at first use.

### E2. "The Qwen judges add nothing" contradicts Table I
- **Where:** E l.115; Table I row "Qwen2.5-14B + Jinx" (FAR 1.3‡).
- **Problem (verified):** Against Jinx, Qwen-14B + Jinx cuts false alarms by 0.44 points (CI −0.81 to −0.05), so it is significantly lower. Its R@1 is 1.0 point lower (CI −0.0 to +2.0).
- **Fix:** "Qwen2.5-14B also lowers false alarms slightly (1.3%, CI of the difference −0.8 to −0.1 points) but ranks slightly fewer duplicates first; the smaller Qwen judges change neither."

### E3. The replay result is not specific to Jinx
- **Where:** E l.81; T l.105.
- **Problem (verified, `replay_impact.csv`, cross-author, n = 313):**

| Detector | Right PR named when the duplicate opened | Of those people took over a day to notice |
|---|---|---|
| Jinx | 46.0% | 34.7% |
| INTRUDE + time | 47.3% | 36.7% |

- **Fix:**
  - E: "A warning at open time from Jinx would have named the right duplicate in 46% of cross-author cases (INTRUDE + time: 47%)…"
  - T: present the replay as the benefit of *any* open-time warning, then argue for Jinx on explanations and packaging.

### B3. Highlighting in Table I reverses colour meaning, and the Δ sign convention is backwards
- **Where:** `tab_main.tex` and its generator `make_paper_tables.py`; both table captions.
- **Problems:**
  - Green cells mark baselines with *significantly more* false alarms, so green means bad here, while every figure uses green for "good".
  - The ‡ mark appears only on rows that contain Jinx, so the reader cannot tell what Jinx itself wins.
  - The "Jinx − row" column makes a negative value mean the row is better.
  - The table prints "-0.0" and "[-0.0, +2.0]", which hides whether a CI includes zero.
- **Fix:**
  - Report "row − Jinx" with a header that says "+ = row better".
  - Bold a difference only when its CI excludes 0.
  - Use light orange for "worse than Jinx" and light blue for "better than Jinx", the same in every table.
  - Format with `f"{x:+.1f}".replace("-0.0", "0.0")`, and widen to 2 decimals when a CI bound rounds to 0.

### E4. Fig. 4 (random pairs vs queue): labels overlap and the key region is a blob
- **Where:** E Fig. 4 (l.101–102); `make_figures.py` §5.
- **Problems (seen at 250 dpi):**
  - The "INTRUDE + time" annotation is printed on top of the "LLM judge" legend entry.
  - The bottom annotation "3 combined methods with AUC > 0.98 / span Recall@1 0.92 to 0.93" crosses the x-axis and its tick labels.
  - The "Jinx" leader line points into an overplotted cluster.
  - The existing-bot points are hidden.
  - The y-label still says "live-queue", while the text says "real-use queues".
- **Fix:**
  - Move the legend below the axes (`loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3`).
  - Drop the bottom text box and put it in the caption.
  - Add a zoom inset for AUC 0.93–1.00 and R@1 0.80–0.95 with the 6–8 named methods.
  - Rename the y-axis "Recall@1 on real-use queues (cross-author)".

### E5. Fig. 5 heat map is still too small, and the bold marks mean little
- **Where:** E Fig. 5 (l.107–108); `make_figures.py` §2 (`figsize=(W, 2.6)`, cell text 6.5 pt).
- **Problems:**
  - `fig_heatmap.pdf` is still 331 pt wide in a 252 pt column, so it prints at 0.76× and the cells at about 4.9 pt. This was flagged in round 1.
  - Several cells per row are bold: 5 in row B and 4 in row C, where n = 10 and one PR is 0.10.
  - The caption says "small groups have wide uncertainty", but nothing in the figure shows it.
  - The text (l.110) says "the link rule does well" without the number: 0.88 against Jinx 0.72 on class D, n = 25.
- **Fix:**
  - Draw the figure at its final width (`fig.set_size_inches(3.5, 2.4)`, `bbox_inches=None`) and check that the PDF is at most 252 pt wide.
  - Drop the bold. Box only the cells whose paired CI against Jinx excludes 0, or show no winner at all.
  - Hatch the rows with n < 30.
  - Add the number to l.110: "the link rule reaches 0.88 (n = 25)".
  - Rename "Links only" to match B2.

### E6. Fig. 7 (accuracy vs time): points hide each other, and every difference is inside the CI
- **Where:** E Fig. 7 (l.117–120); `make_figures.py` §3.
- **Problems:**
  - The "Jinx (with MiniLM)" marker at about 700 ms is partly covered by the "+ Qwen 7B" square.
  - Leader lines cross each other ("+ BGE reranker" and "+ Qwen 7B").
  - The "link rule" reference line runs through the "+ BGE reranker" label.
  - The y-range is 0.91–0.94, but Jinx's own 95% CI is 0.889–0.958, so the plot ranks noise.
- **Fix (preferred):** Plot **false alarms against time**, since false alarms are where the methods differ significantly. Use the same labels and add CI whiskers.
- **Otherwise:**
  - Add `ax.axhspan(0.889, 0.958, alpha=.08)` labelled "Jinx 95% CI".
  - Label points directly with 4 pt offsets, and number any overlapping points.

### E7. Fig. 6 (operating curve): the legend covers a line and four curves look the same
- **Where:** E Fig. 6 (l.112–113); `make_figures.py` §4 (`loc="lower right"`).
- **Problems:**
  - The contrib-guard line, from (5%, 0.40) to (10%, 0.60), runs through the legend box.
  - The Jinx, All-signals LR, INTRUDE and link-rule curves lie within 0.05 of each other from 5% to 20%.
  - The y-label "cross-author duplicates caught at rank 1" is jargon.
- **Fix:**
  - Put the legend outside the plot, or label the end of each line.
  - Draw Jinx, Haiku + Jinx, the link rule and contrib-guard in colour, and the others in thin grey.
  - New y-label: "share of duplicates found and flagged".
  - Caption: "…At strict budgets (1–2%) the link rule and Haiku + Jinx find more duplicates than Jinx."

## Minor

### E8. Fig. 3 (two queue designs) compares different pair sets, and the orange points have no CI
- **Where:** E Fig. 3 (l.96–97).
- **Fix:**
  - Add to the caption: "Orange: n = 342 pairs; blue: n = 313 (pairs whose duplicate was still open)." Better, also plot the orange design on the same 313 pairs.
  - Add CIs to the orange points from `results_grace7/strategies_by_group.csv`.
  - Move the orange value labels left of their CI bars; for Jinx and All-signals LR they now sit on the blue bar.
- Otherwise this is the clearest figure in the paper, and it carries the paper's main message.

### B4. The architecture diagram wraps badly in the IEEE paper
- **Where:** `figures/arch.tex`; E Fig. 1.
- **Problem:** In Times, the `\large` titles wrap: "① Read / PRs", "② Clean / text", "④ Score / + explain". The monospace example wraps mid-phrase: "- links to the other / PR", "- 100% identical / lines". The tool-demo version, set in Biolinum, is fine.
- **Fix:** Widen the boxes (Read 22 mm, Clean 24 mm, Score 26 mm, Report 34 mm), or use `\normalsize` titles. Shorten the example lines to "- links the other PR" and "- 100% same lines".

### B5. Colour and names change from figure to figure
- **Where:** all figures.
- **Problem:** Orange means contrib-guard in Figs. 2 and 6, INTRUDE in Fig. 6, and the 7-day design in Fig. 3. The same baseline is called "Link rule", "Links only" and "link rule", and the same judge "Haiku + Jinx" and "Claude Haiku 4.5 + Jinx". The queue is called "live queue", "LiveQueue" and "real-use queues".
- **Fix:**
  - Fix one colour per method in `make_figures.py`: Jinx `#0072B2`, Haiku + Jinx `#CC79A7`, link rule `#009E73`, INTRUDE `#E69F00`, contrib-guard `#D55E00`, everything else grey.
  - Use a different encoding for the 7-day design, such as hollow grey markers.
  - Pick one name per method and per queue type and use it everywhere.

### T5. The workflow says "updates it on later runs", but it only runs on opened and reopened
- **Where:** T l.50 and l.77–78.
- **Fix:** Add `synchronize` and `edited` to `types:`. The marker-based update already exists (`action.py` `MARKER`). Otherwise remove "and updates it on later runs".

### T6. The safety paragraph is missing two sentences
- **Where:** T l.91.
- **Fix:** Add: "`issues: write` is needed because GitHub creates PR comments through the issues API. PR titles and bodies are treated as data only; they are never placed in a shell command (`action.yml` passes only the action inputs through `env`)."

### T7. The threshold sentence mixes the shipped threshold with the cross-validation one
- **Where:** T l.48.
- **Problem:** The 1.8% comes from per-fold thresholds (the median top score in the training folds, `eval2.py`). The shipped 0.5 comes from an intercept shift on all the data (`weights_emb.json` "note").
- **Fix:** "The shipped threshold 0.5 is set the same way (the median top score of cross-author duplicates); in cross-validation this rule flagged about half of them with 1.8% false alarms."

### T8. ACM template leftovers
- **Where:** T preamble.
- **Problems:** The running header says "Conference'17, July 2017, Washington, DC, USA". The build warns "ACM reference format is mandatory" (`printacmref=false`) and "No city present" three times.
- **Fix:** Set `\acmConference{…}` for the target venue, or use the `nonacm` option until the venue is fixed. Add `\city{}`. Consider the CCS concept "Software and its engineering → Software maintenance tools" over "Software evolution".

### B6. Captions to tighten
- **E Fig. 2 / T Fig. 3:** add "Lower is better. Jinx in blue." In T, add the threshold sentence from E.
- **E Fig. 4:** say the y-axis uses open-only queues.
- **E Fig. 7:** say that the GPU and API times are added to the MiniLM-Jinx time, and that the link rule needs no model.
- **Table rows:** state that re-rankers of Jinx's top 5 keep Jinx's R@5 by design (0.990), since several rows show the same value.

### E9. References still incomplete
- **Where:** E refs.
- **Problem:** [14] has no author first names. [4] and [19] have no venue or arXiv ID. [1] has no arXiv ID (T prints arXiv:2602.09185).
- **Fix:** Complete the `refs.bib` entries `benchekaya2026slr`, `nakashima2026rejected`, `khemissi2026humans` and `li2026aidev`.

---

### What a tool-track reviewer will still ask
1. Where can I install it today, and where is the video? (T3)
2. What does the PR comment look like? (T4)
3. Why use this instead of a shared-issue rule? (T1, B2)
4. How long does a full Action run take on a cold runner? (T2)
5. Has anyone used it on a live repository? The paper says future work. Even a one-week run on 2–3 sandbox or friendly repositories, counting comments, true and false warnings and maintainer reactions, would make the paper much stronger.
