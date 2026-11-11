# Jinx demo video script (target 3-4 minutes)

Record after the sandbox Action run (CHECKLIST: "Action run on a private test repo"). Screen + voice-over, 1080p.

| Time | On screen | Voice-over |
|---|---|---|
| 0:00-0:25 | GitHub PR list in a repo with two agent PRs for the same issue | "Coding agents open many PRs. Some redo work that is already open. A maintainer reviews both before noticing." |
| 0:25-0:50 | `.github/workflows/jinx.yml` (8 lines) | "Jinx is a GitHub Action. Add this file; it uses the workflow's own token, needs no API key, and sends no code anywhere." |
| 0:50-1:40 | Agent opens a second PR; Jinx comment appears with ranked match and reasons | "When a PR opens, Jinx compares it with every open PR: same files, overlapping lines, shared issue, similar text after removing agent boilerplate. It explains each match and never closes anything." |
| 1:40-2:10 | Terminal: `pip install jinx-pr`; `jinx check new.json --open-queue open.jsonl` on the transformers fixture | "The same check runs locally. This is a real agent PR from huggingface/transformers; Jinx finds its twin in 12 ms." |
| 2:10-2:20 | Same CLI on the no-duplicate fixture | "And when nothing is duplicated, it stays quiet." |
| 2:20-3:10 | Results table (cross-author Recall@1, false alarms, latency) | "On 342 cross-author duplicates from real agent PRs, Jinx ranks the right PR first 90% of the time, versus 78% for the best existing bot, with 2.5% false alarms, on a CPU." |
| 3:10-3:30 | Limitations slide | "It still misses duplicates that change different files. Labels come from PR comments." |
| 3:30-3:45 | Repo URL, PyPI name | "Jinx is open source. Links below." |

Numbers must match `paper/generated/numbers.tex` at recording time.
