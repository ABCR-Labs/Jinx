# Review: figures, tables and tool demo — Jinx papers (branch `devin/paper-revision`, commit 3080800)

Reviewer role: data-visualisation and tool-demo reviewer (FSE/ICPC tool-demo lens).
Method: I rendered both committed PDFs to images (110 and 250 dpi), rebuilt both from source, read the TeX sources, `paper/scripts/*.py`, `src/jinx_pr/*`, `action.yml`, and checked every number I call wrong against `experiments/results/*.csv`, `summary.json` and `src/jinx_pr/data/weights*.json`. No commits, no API calls.

Build status: both papers rebuild cleanly (empirical 5 pages, tool demo 3 pages); all fonts embedded, no Type 3 fonts. The tool demo raises acmart warnings that matter for submission (see T3).

Numbering: **E** = empirical, **T** = tool demo, **B** = both. Findings are in priority order.

---

## Major

### B1. The headline numbers mix two different Jinx configurations, and the shipped tool runs the weaker one
- **Paper:** both. **Location:** E abstract (l.18), §VI-A/B (l.100, l.115), Table I row "Jinx (ours)"; T abstract (l.17), §3 (l.90, l.95), Table 1, Fig. 4 (pareto).
- **Problem (verified):**
  - Accuracy and false alarms come from `Jinx + MiniLM, LR (current tool)` (R@1 0.901, FAR 2.5%) — `make_paper_tables.py`, `M["jinx"]`.
  - The 22 ms latency comes from `summary.json["latency"]["lexical features ms/query"]` — lexical features only, no MiniLM encoding (`make_paper_extras.py`, `latJinx`). The pareto plot puts the MiniLM-variant accuracy at the lexical-only time (`make_figures.py`, `base = LAT["lexical features ms/query"]`).
  - The GitHub Action installs `pip install "${{ github.action_path }}"` with no `[embed]` extra and `action.py` never builds an embedder, so it uses `weights.json` (lexical). The CLI also uses lexical unless you pass `--embed`. So the tool a reader installs is `Jinx lexical, LR`: **R@1 0.889, FAR 3.2% [2.4, 4.2]**, not 0.901 / 2.5%.
- **Fix (pick one, then use it everywhere):**
  1. *Preferred:* report the shipped default. Set `M["jinx"] = "Jinx lexical, LR"` and keep 22 ms. Lexical Jinx still wins clearly: vs INTRUDE + time R@1 **+7.9 pts [+3.7, +12.7]**, MRR +5.2 [+1.9, +9.1]; vs contrib-guard R@1 **+11.1 [+5.4, +16.7]**, R@5 +5.3 [+1.2, +9.7] (`paired_cross_author.csv`). Add one row "Jinx + MiniLM (optional)" with its own measured CPU latency.
  2. Or make MiniLM the default in `action.yml` (`pip install "...[embed]"`) and measure the end-to-end CPU time with embedding, then report that time.
  - Rename the Table I row from "Jinx (ours)" to "Jinx (default, no embedding)" or "Jinx + MiniLM" so the row says which one it is.

### B2. Table I does not show Jinx's wins: every bold number belongs to another row
- **Paper:** both. **Location:** E Table I (l.95–97), T Table 1 (l.83); generator `make_paper_tables.py` (`best = …` over all rows).
- **Problem:** Bold marks the best value over *all* rows, so "All signals, LR" and the cascade take every bold cell. The shaded Jinx row has no bold number. A reader sees "Jinx is not best" — the opposite of the message. The owner asked for wins to be highlighted.
- **Fix:**
  - Bold the best value **among the baselines block** only, and mark Jinx cells that beat the best baseline with a green arrow, e.g. `0.901\,\textcolor{OKgreen}{$\blacktriangle$}`.
  - Add a final column "Δ R@1 vs INTRUDE + time (95% CI)" so the win is a number with a CI, e.g. Jinx `+9.1 [5.0, 13.1]`, contrib-guard `−3.2`.
  - Sort baselines by R@1. Today "Links only" (0.839) sits below INTRUDE (0.810) and contrib-guard (0.778).
  - Move "Links only" into the baselines as "Link rule (shared issue / #ref)". It is not a bot, but it beats both the classic detector and the best bot on R@1, so readers need to see it.
  - Replace the caption's last sentence with: "Rows: our tool; our tool with extra models added; baselines. Bold = best baseline per column; ▲ = Jinx beats every baseline."

### B3. "All signals, LR" beats Jinx on every column, and neither paper says why it is not the shipped tool
- **Paper:** both. **Location:** E Table I, §VI-B (l.110 "within noise of Jinx"), Fig. 4 (heat map), Fig. 6 (operating curve); T Table 1.
- **Problem (verified):** All-signals LR has R@1 0.906, R@5 0.974, MRR 0.935 and FAR **1.6% vs 2.5%**, and it is above Jinx at every false-alarm budget in Fig. 6 (0.41 vs 0.30 at 1%; 0.56 vs 0.44 at 2%). The paired R@1 difference is +0.6 pts [−1.2, +2.5], so it is a tie on R@1. But the false-alarm gap is visible, and any reviewer will ask why you ship the weaker model.
- **Fix:** add one sentence in E §IV after l.87 and in T §2.4: "We ship the smaller model because the all-signals model also needs [list the extra signals, e.g. embeddings of the diff on a GPU / X ms more per PR]; it is not reliably better on Recall@1 (+0.6 points, 95% CI −1.2 to +2.5)." If the extra signals are cheap, ship all-signals LR instead and update B1.

### E1. RQ3 text says "no method handles class D", but the link rule does best on class D
- **Paper:** empirical (and T §4). **Location:** E §VI-C l.121; Fig. 4 row "D: no shared files"; T l.98.
- **Problem (verified):** cross-author class D (n=29): Links only **0.759**, Jinx 0.655, Haiku + Jinx 0.655, INTRUDE 0.517 (`strategies_by_group.csv`). Fig. 4 already bolds 0.76 under "Links only", but the text lists only Jinx, INTRUDE and Haiku. With n=29 a 3-PR difference changes the result by 0.10.
- **Fix:** replace the last two sentences of l.121 with: "…drops most for PRs that share no files at all (class D, n=29): Jinx 0.655, INTRUDE + time 0.517. Here the simple link rule does best (0.759), because these PRs often name the same issue. With only 29 pairs these differences are a few PRs each. These are duplicates of intent rather than of code, and no method ranks more than three in four of them first." In T §4 add "(a simple shared-issue rule does better here)".

### E2. Fig. 4 heat map prints at about 5 pt and puts small-sample rows on an equal footing
- **Paper:** empirical. **Location:** Fig. 4 (l.118); `make_figures.py` §2.
- **Problems:**
  - `fig_heatmap.pdf` is 331 pt wide but is placed at `\columnwidth` (≈252 pt), so it shrinks to 0.76×. Cell text set at 6.5 pt prints at **~4.9 pt**, and tick labels at ~5 pt, below the usual 6–7 pt floor. (Bbox-tight layout plus the long y-labels and colour bar make the PDF wider than `W=3.45 in`.)
  - Bold-on-white versus regular-on-white text inside dark cells is hard to tell apart at print size; ties make 2–3 bold cells per row.
  - Row C has n=10 and row D n=29, but they get the same visual weight as n=1525.
  - The orange-red outline (#D55E00) on the Jinx column sits next to dark-blue cells; fine for colour-blind readers, but thin (1.6 pt) after scaling.
  - The heat map shows absolute Recall@1, so the message "where does Jinx win?" requires comparing numbers across cells.
- **Fix:**
  - Use `figsize=(W, 2.6)` *with* `fig.savefig(..., bbox_inches=None)` and `constrained_layout=True`, or set `width=\linewidth` only after checking the PDF is ≤252 pt wide. Target ≥6.5 pt printed text.
  - Plot **difference from INTRUDE + time** with a diverging, colour-blind-safe map (`cmap="RdBu"`, centre 0, range ±0.3) and print the Jinx value only in its own first column. Then Jinx's wins appear as a blue column.
  - Grey out or hatch rows with n < 30 (`ax.add_patch(Rectangle(..., hatch='///', fill=False))`) and add "(small n)" to their labels.
  - Mark the best cell with a black box (`Rectangle(..., ec='black', lw=1.2)`) rather than bold, keeping one rule per row.
  - Drop the unused `tab_classes.tex` (built but never `\input`), or use it instead of the heat map in the tool demo.

### E3. Fig. 3 / T Fig. 4 (accuracy vs time): the legend looks like data, and labels are far from their points
- **Paper:** both. **Location:** E Fig. 3 (l.112), T Fig. 4 (l.92); `make_figures.py` §3.
- **Problems (seen at 250 dpi):**
  - The legend ("runs on ● CPU ■ GPU ◆ API") sits inside the plot at y≈0.82, x≈150–15,000 ms. Its markers look like three more strategies.
  - Labels are placed by hand coordinates (`TXT`) and several sit closer to another point than to their own: "+ Qwen 7B (top-5)" sits right under Jinx (its point is at 330 ms); "+ BGE reranker (top-10)" is at 0.880 while its point is at 0.871; leader lines are 0.5 pt grey and almost invisible.
  - The y-axis runs 0.80–0.915, so a 0.01 gap looks large; the paired 95% CIs are about ±2–4 pts (Jinx R@1 CI 0.868–0.931), so all re-ranked points lie inside Jinx's CI. The figure makes noise look like a ranking.
  - x-axis mixes CPU, batched-GPU and API wall-clock times; see B1 for the Jinx point.
- **Fix:**
  - Move the legend outside: `ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=False, title=None)` and put "runs on:" in the label text.
  - Label points directly next to the marker (offset 4–6 pt, no leader lines), or number them 1–7 and give the key in the caption.
  - Add a light horizontal band for Jinx's 95% CI (`ax.axhspan(0.868, 0.931, color=OK["blue"], alpha=0.08)`) and say in the caption: "The shaded band is Jinx's 95% CI; every re-ranked variant falls inside it."
  - Draw INTRUDE + time as a point at its own latency instead of a line, so the plot shows both baselines' cost.

### E4. Fig. 5 (random pairs vs live queue): the key region is unreadable and τ = 0.75 is described as weak agreement
- **Paper:** empirical. **Location:** Fig. 5 (l.126), §VI-D l.129; `make_figures.py` §5.
- **Problems:**
  - All the methods the figure is about (21 combined methods with AUC > 0.98) sit inside a yellow band 0.02 wide, overplotted into one blob. The "Jinx" label points into the blob; the "INTRUDE + time" label overlaps other dots; the text box at the bottom says what the figure should show.
  - "The two rankings agree only partly (Kendall τ = 0.75)". τ = 0.75 over 66 methods (p ≈ 9e−19, `summary.json`) is strong overall agreement. The real finding is narrower: random-pair AUC cannot separate the strong methods.
- **Fix:**
  - Replace with a two-panel figure: left = the current scatter (small, for context); right = a zoom on AUC 0.97–1.00 with the combined methods labelled, or a rank-vs-rank slope chart for the 25 combined methods only. Compute τ within those 25 and report it.
  - Replace l.129 sentence 2 with: "Over all 66 strategies the two rankings broadly agree (Kendall τ = 0.75). The problem is at the top: 21 of the 25 combined methods reach an AUC above 0.98, so random pairs cannot tell them apart, yet their live-queue Recall@1 ranges from 0.851 to 0.906." Update the Abstract and Conclusion ("random-pair AUC is a poor guide…") to "random-pair AUC cannot separate the strong methods".

### E5. Fig. 6 (operating curve) supports a different message than the text gives
- **Paper:** empirical. **Location:** Fig. 6 (l.131), l.134.
- **Problem (verified, `operating_curve.csv`):** The text says Jinx and all-signals LR beat INTRUDE and contrib-guard at every budget — true. But the figure's most visible fact is that **Haiku + Jinx and All-signals LR are above Jinx** at every budget from 2% up (at 10%: Haiku + Jinx 0.83, All LR 0.78, Jinx 0.75). The reader is left to work out that the heavier models help here, which contradicts "LLM judges do not improve on it" in the abstract. Also, the y-label "cross-author duplicates caught at rank 1" is two lines of jargon, and legend markers overlap the Jinx and Haiku lines at 5–20%.
- **Fix:**
  - Add one sentence to l.134: "At a fixed false-alarm budget, adding Claude Haiku helps (0.83 against 0.75 at 10%), so an LLM judge is worth its cost when false alarms matter most." Qualify the abstract: "LLM judges do not rank more duplicates first."
  - Move the legend outside on the right or label line ends directly. Y-label: "share of duplicates found (ranked first and flagged)".
  - Use a linear x-axis with ticks at 1, 2, 5, 10, 20% (only 5 points), or keep log but add minor gridlines.

### B4. Architecture diagram: good start, but the step count, output text size and red colour need fixing
- **Paper:** both. **Location:** `figures/arch.tex`; E Fig. 1 (l.84), T Fig. 1 (l.29), T l.32 "Fig. 1 shows the five steps".
- **Problems:**
  - T says "five steps" and has five subsections (Reading, Cleaning, Comparing, Scoring and explaining, Reporting), but the diagram has six boxes with different names (Input, Clean text, Pair signals, Score, Explain, comment box). The reader cannot map one to the other.
  - The example comment uses `\ttfamily\tiny` (5 pt); natural width is 471 pt, so it prints at ~5.4 pt in E and ~5 pt in T. That is the part a demo reviewer wants to read.
  - "Explain" is red (red fill = error). The output box is pale yellow with grey text "PR comment (Action) or CLI" in `\tiny`.
  - Missing the two things that make Jinx different: the template list is *learned from the repository's PRs*, and the model is *trained offline on LiveQueue and shipped with the package*. Also no threshold (score ≥ 0.5 → comment).
  - Jargon in boxes: "#ref", "→ 0–1", "open".
- **Fix:**
  - Number the boxes ①–⑤ and use the same names as T §2.1–2.5: ① Read PRs ② Clean text ③ Compare each pair ④ Score + explain ⑤ Post one comment. In T l.32 write "Fig. 1 shows the five steps; the numbers match §2.1–2.5."
  - Raise all text one size (`\scriptsize`→`\footnotesize`, `\tiny`→`\scriptsize`) and the comment box to `\scriptsize\ttfamily`; let the figure take two lines if needed.
  - Use Okabe–Ito colours to match the plots: Input `#0072B2`, Clean `#E69F00`, Signals `#009E73`, Score `#CC79A7`, Report `#56B4E9`; keep fills at 15–20%.
  - Add a small dashed box under ② "boilerplate lines learned from this repo's PRs" and under ④ "weights trained on LiveQueue, shipped in the package; comment if score ≥ 0.5".
  - Replace "#ref" with "mentions the other PR", "→ 0–1" with "score from 0 to 1", "open" with "older PR still open".

### B5. Figure text uses a different font from the body and is set from fixed point sizes that get rescaled
- **Paper:** both. **Location:** all matplotlib figures; `make_figures.py` rcParams.
- **Problem:** Plots use DejaVu Serif (`font.family: serif`); the IEEE body is Times (Nimbus Roman) and ACM is Libertine. The figures are drawn at `W = 3.45 in` (248 pt) but placed at `\columnwidth` (IEEE 252 pt, ACM ≈241 pt), and PDF widths range 230–331 pt, so each figure is scaled by a different factor (0.73× to 1.10×). Text size varies from figure to figure.
- **Fix:** set `"font.family": "serif", "font.serif": ["Times", "Nimbus Roman", "TeX Gyre Termes"]` for E (or `"text.usetex": True`) and Libertine for T; draw each figure at its exact final width (E 3.5 in, T 3.33 in), save with `bbox_inches=None`, and include with `\includegraphics{...}` at natural size (no `width=`). Then 7 pt in the script is 7 pt on paper.

### T1. The tool demo shows no picture of the tool in use
- **Paper:** tool demo. **Location:** §2.5–2.6, Figs. 1–2.
- **Problem:** The main user-facing output — the comment Jinx posts on a GitHub PR — is never shown. Fig. 2 is a CLI transcript, and Fig. 1 has a 5 pt mock-up. Tool-demo reviewers judge usefulness from what the maintainer sees. The paper uses ~2.4 of its 4 pages, so there is room.
- **Fix:** add a full-width or column-width screenshot of a real Jinx comment on a sandbox PR (ideally the huggingface/transformers #44134 example replayed in a fork), with callouts for: score, reasons, link to the older PR, "Jinx never closes or labels PRs". Caption: "The comment Jinx posts on a new PR. The maintainer sees the likely duplicate and why, and decides." This also answers the TODO in §4 about a sandbox run.

### T2. Installation instructions do not work today
- **Paper:** tool demo. **Location:** §2.6 l.65–80, §5 l.101.
- **Problems (verified):**
  - `pip install jinx-pr`: `https://pypi.org/pypi/jinx-pr/json` returns 404; the package is not on PyPI. The README uses `pip install .`.
  - `uses: ABCR-Labs/jinx-pr@v1`: the code lives in `ABCR-Labs/agentdup` (`action.yml` at repo root); no `jinx-pr` repo or `v1` tag is referenced in the repo.
  - The YAML block is set as running `verbatim` text, so it breaks across columns around Table 1 (lines 107–116 on p.1, 160–162 on p.2), and the `[TODO: confirm…]` line prints in red.
- **Fix:** publish to PyPI (or write `pip install git+https://github.com/ABCR-Labs/<repo>@v1`), create the `v1` tag in the repo that holds `action.yml`, and put the workflow in a non-breaking float: `\begin{figure}[t]\begin{verbatim}...\end{verbatim}\caption{The complete workflow file a repository adds.}\end{figure}`. Add the two inputs a maintainer will want: `threshold` and `max-open-prs` (they exist in `action.yml`). Add one line on how a reviewer can try Jinx in two minutes without a repo: `jinx check examples/new_pr.json --open-queue examples/open_prs.jsonl` (both files are in `examples/`), and make the video (`VIDEO_SCRIPT.md`) follow the numbered steps of Fig. 1 and end on the PR-comment screenshot (T1).

### T3. Security of `pull_request_target` is not addressed
- **Paper:** tool demo. **Location:** §2.6 workflow (l.67–78).
- **Problem:** `pull_request_target` runs with a write token on PRs from forks. Reviewers who know GitHub Actions will flag this. Jinx's `action.yml` does not check out the PR's code (it installs from `github.action_path` and reads PRs through the API), which is the safe pattern — but the paper does not say so. `issues: write` also needs a reason.
- **Fix:** add after the workflow: "Jinx uses `pull_request_target` so that it can comment on PRs from forks. It never checks out or runs the PR's code; it only reads PR metadata and diffs through the API, so the write token is not exposed to untrusted code. `issues: write` is needed because GitHub posts PR comments through the issues API."

### T4. ACM template problems that will cost points at submission
- **Paper:** tool demo. **Location:** preamble l.3–15; build log.
- **Problems (from rebuild log):** "CCS concepts are mandatory", "ACM keywords are mandatory", "No city present for an affiliation" ×3, image-description warnings ×4; header shows "Conference'17, July 2017, Washington, DC, USA" and a placeholder DOI. Abstract ends with red "Video: [TODO: URL]. Tool: [TODO: URL]."
- **Fix:** add `\begin{CCSXML}…\end{CCSXML}\ccsdesc[500]{Software and its engineering~Software maintenance tools}` and `\keywords{duplicate pull requests, coding agents, GitHub Actions, code review}`; add `\city{…}`; add `\Description{…}` to each figure; set `\acmConference{FSE Companion '27}{…}` or use `nonacm` until the venue is fixed; check whether the target demo track is double-blind before submission (author names are shown now).

### T5. The tool demo spends its table on research comparisons, not on the tool
- **Paper:** tool demo. **Location:** Table 1 (l.83), §3 (l.85–95).
- **Problem:** Table 1 is the same 11-row table as the empirical paper, including cascades and Qwen-14B. A demo reviewer wants: does it work, how does it compare with tools a maintainer could install, what does it cost. A feature comparison is missing, and §1 para 2 lists six bots in prose.
- **Fix:** replace Table 1 with two small tables:
  - Results (4 rows): Jinx (default), contrib-guard (best bot), INTRUDE + time, TF-IDF; columns R@1, FAR, time per PR. Same highlighting rules as B2.
  - Feature matrix (rows = Jinx, contrib-guard, Simili, PRSense, PRism, vector-triage, doppelgänger, CodeRabbit Related PRs; columns = uses code diff ✓/✗, explains match, runs locally/no API key, GitHub Action, tested on agent PRs). Move §1 para 2 content into it.

---

## Minor

### E6. Top-5 re-rankers have the same R@5 as Jinx by construction
- **Location:** E Table I rows "Claude Haiku 4.5 alone", "Qwen2.5-14B + Jinx", "Claude Haiku 4.5 + Jinx" (all R@5 0.971 = Jinx).
- **Fix:** add a table note: "Re-rankers reorder Jinx's top 5, so their Recall@5 equals Jinx's by design." Otherwise readers read the tie as a result.

### E7. CIs are shown for false alarms only
- **Location:** Table I (both papers). The key metric is R@1, but only FAR has brackets; R@1 CIs exist in `strategies_by_group.csv` (`R@1 lo/hi`; Jinx 0.868–0.931).
- **Fix:** add R@1 CIs in `\scriptsize` brackets, or add the Δ column from B2 (preferred; it is the paired comparison).

### E8. Fig. 2 (forest plot) leaves out the false-alarm win
- **Location:** E Fig. 2 (l.102), T Fig. 3 (l.87); `make_figures.py` §1.
- **Problem:** The figure has one clear message, which is good, but it shows only R@1/R@5/MRR. The false-alarm reduction (2.5% vs 4.6%, from `paired_false_alarms.csv`) is one of Jinx's two main wins and is absent. Green labels on green bars are low-contrast; the x-label is 7.5 pt and long.
- **Fix:** add a fourth row "fewer false alarms (pts)" with sign flipped so right = better; print the value labels in black; x-label "Jinx minus baseline (percentage points); right of 0 = Jinx better". Caption: "…green = the whole 95% interval is above zero (a clear win); grey = could be zero."

### E9. "Nearly half as many false alarms" is the wrong direction
- **Location:** E §VI-A l.105.
- **Problem:** 2.5 / 4.6 = 0.54, i.e. slightly *more* than half.
- **Fix:** "…and it raises about half as many false alarms (2.5% against 4.6%)."

### E10. Fig. 1 caption and placement
- **Location:** E l.84–87. The architecture figure floats to the top of p.3 inside §IV "Strategies", one page after the text that motivates it. Caption repeats the text.
- **Fix:** move `\begin{figure*}` to just before §III so it lands on p.2, or cite it in the Introduction contribution bullet for Jinx. Caption: "Jinx in five steps. Numbers match §IV. Colours mark the step type, not quality."

### E11. Visible "TODO" text in the reference list
- **Location:** E refs [5], [14], [20] print "tODO: verify author first names" / "tODO: authors"; [3], [17], [18] have incomplete author lists and no venue or arXiv ID (IEEEtran drops the `eprint` field that ACM prints).
- **Fix:** complete the `author` fields in `paper/refs.bib` (entries `abujadallah2026rejection`, `benchekaya2026slr`, `cupid2023`, `alam2026unmerged`, `xu2026conflicts`, `sarkar2026before`), delete the `note={TODO…}` fields, and add `howpublished={arXiv:XXXX.XXXXX}` so the IEEE style prints the ID.

### E12. RQ3 "code twin" claim needs its scope
- **Location:** E l.121 "every combined method ranks them first at least 0.91 of the time".
- **Check:** `classAMin` is computed over methods whose name contains "LR" or "avg" (`make_paper_extras.py`), so it is true for that set. Say so: "every learned or re-ranked method". Fig. 4 shows TF-IDF 0.86 and BGE 0.81 for code twins, which a reader may otherwise see as a contradiction.

### E13. Claim about Jinx weights has no figure or number
- **Location:** E l.123 "the trained Jinx weights … give identical changed lines little weight".
- **Fix:** add a small horizontal bar chart of the standardised LR weights from `src/jinx_pr/data/weights_emb.json` (12–13 bars, sorted, coloured by signal group text/code/context using the diagram colours). This is cheap, needs no new run, explains the model to non-experts, and supports the explanation feature in the tool demo. It can replace Fig. 6 in the tool demo if space is short.

### T6. The CLI example in Fig. 2 should show the default configuration
- **Location:** T Fig. 2 (l.49–62).
- **Problem:** The example is good (real PR, clear reasons). But it does not say whether `--embed` was used, and "12 ms" is a single run. Line wraps ("refactor(tvp): use / capture_outputs…") break the visual alignment.
- **Fix:** add "(default settings, no embedding model)" to the caption if true; shorten the title to fit one line, or use `fancyvrb` with `fontsize=\scriptsize`; colour the "DUPLICATE?" line with `\textcolor` via `fancyvrb`'s `commandchars` so the match stands out.

### B6. Small wording fixes in captions (plain English)
- E Fig. 3 caption: "Times are medians; GPU times use batching" → "Times are median milliseconds per new PR. GPU times assume many PRs are scored together."
- E Fig. 6 caption: "Share of cross-author duplicates ranked first and flagged, for a given false-alarm budget" → "If a maintainer accepts a given share of false alarms (x-axis), how many real duplicates does each tool find and flag? Higher is better."
- E Fig. 5 caption: replace "still separates them" with "spreads them out", and say "Each dot is one of the 66 strategies."
- Table I caption: define R@1, R@5 and MRR in one short phrase each, since table readers often skip §V.

---

## Summary for the authors
- **Fix first:** B1 (configuration mismatch), B2 (wins not highlighted), B3 (why not ship all-signals LR), E1 (class D claim), T1–T3 (screenshot, install, security).
- **Figures to redraw:** heat map as a difference map at true size (E2), accuracy-vs-time legend and labels (E3), random-pair zoom (E4), operating-curve legend (E5), diagram numbering and text size (B4), fonts (B5).
- **Suggested new visuals:** LR weight bar chart (E13), feature-comparison table (T5), PR-comment screenshot (T1).
