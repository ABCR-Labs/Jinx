# Jinx demo video script (about 3.5 minutes)

`video/make_video.py` builds `video/jinx_demo.mp4` (1920x1080, captions, no voice-over yet) from the real
screenshots of the live Action run on ABCR-Labs/Jinx (demo PRs #12-#15 for issue #11) and the CLI fixture. Read the
captions below as the voice-over when recording audio.

| Time | On screen | Voice-over / caption |
|---|---|---|
| 0:00-0:12 | Banner | "Jinx: explainable duplicate warnings for pull requests from coding agents." |
| 0:12-0:34 | PR list with demo PRs #12-#15 | "Coding agents open many pull requests. Some redo work that is already open, and a maintainer may review both before noticing. Here are four demo PRs: three for the same issue and one unrelated." |
| 0:34-0:59 | `.github/workflows/jinx.yml` | "Jinx is a GitHub Action. It uses the workflow's own token, needs no API key, reads PR metadata and diffs through the API, and never runs the PR's code." |
| 0:59-1:34 | Jinx comment on #15 | "PR #15 redoes open PR #12. Jinx compares it with every open PR: same linked issue, shared files, overlapping lines, identical added lines, similar text after removing agent boilerplate. It explains the match and never closes anything." |
| 1:34-1:59 | Quiet cases (#13, #14) | "An unrelated docs PR got no comment. A PR for the same issue written very differently scored 0.30, below the default threshold, so it was missed. The threshold trades misses against false alarms." |
| 1:59-2:24 | Terminal: install + `jinx check` on the transformers fixture | "This is a real agent PR from huggingface/transformers, from AIDev. Jinx finds its twin among 19 open PRs in about 10 ms on a CPU." |
| 2:24-2:54 | False-alarm figure | "On real AIDev queues, Jinx ranks the right PR first 93% of the time, tied with a link rule and a classic detector. Its false alarms are 1.8 per 100 clean PRs, about a third of the best existing bot's." |
| 2:54-3:16 | Limitations | "Jinx is not more accurate than the best baselines; it packages them with explanations." |
| 3:16-3:28 | Links | "Jinx is open source. Thanks for watching." |

Numbers must match `paper/generated/numbers.tex` and `numbers_extra.tex` at recording time.
