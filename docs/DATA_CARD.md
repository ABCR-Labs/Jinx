# LiveQueue benchmark: data card (working name)

**What it is.** A benchmark for duplicate pull-request (PR) detection on PRs opened by coding agents, scored the way
a detector is used: at the moment a new PR is opened, against the PRs actually open in that repository (its
*live queue*).

| | |
|---|---|
| Source | AIDev v5, https://huggingface.co/datasets/hao-li/AIDev (Li et al., arXiv:2602.09185), CC BY 4.0 |
| Time span | agent PRs up to 31 Mar 2026 (AIDev cutoff) |
| Agents | OpenAI Codex, Copilot, Devin, Cursor, Claude Code, Jules (as labelled by AIDev) |
| Queries | 4,832: 1,867 with a duplicate in the queue, 2,965 without |
| Relations (with duplicate) | 1,525 self-replacement (same author), 342 cross-author (228 same agent, 114 cross-agent) |
| PRs | 76,209 (queries + queue members), 672 repositories |
| Queue size | median 40, p90 314, max about 1,900 |
| Candidate pairs | 572,074 |
| Human annotation | none (silver labels; see audit below) |

## How it is built (`experiments/bench_v1/build_bench.py`)

1. **Silver pairs.** PR comments in AIDev (`pr_comments.parquet`) are matched with a strict pattern that requires an
   explicit PR reference (`data/count_dups.py`):
   `(duplicate[sd]? (of|by)|dupe of|supersed(ed|es)? by|superseeded by|in favou?r of|replaced by|same as)\s*(pr\s*)?(#N | github.com/.../pull/N)`.
   This gives 3,798 (PR, referenced PR) pairs. Pairs whose referenced PR is not in AIDev (for example, human PRs) are
   dropped.
2. **Query and gold.** In each pair, the later-created PR is the query and the earlier one is the gold duplicate.
3. **Live queue.** The query's queue is every AIDev PR in the same repository created before the query and still open
   at that moment (or closed less than 7 days before it). A pair is kept only if the gold PR is in the queue. Other
   silver partners of the same query are marked `other_gold` and are not counted as errors.
4. **No-duplicate queries.** 3,000 merged PRs are sampled (seed 0) from the same repositories, excluding any PR with
   a duplicate-like comment (a broader keyword pattern) or that appears in a silver pair. The 2,965 with a non-empty
   queue are kept.
5. **Taxonomy** (`experiments/bench_v2/eval2.py`, `code_class`): A code twin (at least 50% identical changed lines),
   B partial code overlap, C same files with different code, D no shared files (intent-level). Extra groups: same issue
   with different code; same code with a different description (code twin with text TF-IDF < 0.3); pairs with no link
   at all (no `#ref`, no shared issue).

## Release files (`experiments/bench_v2/export_release.py`)

- `queries.parquet`: one row per query, with `repo`, `query_id`/`query_number`, `has_duplicate`, `gold_id`/`gold_number`, `other_gold_ids`, `label_phrase`, `relation`, `queue_ids` and `queue_size`.
- `prs.parquet`: one row per PR, with title, body, author, agent, timestamps, `files`, `hunks` (path, start, end), `added_line_hashes` and `linked_issue_ids`. Code is stored as line ranges and hashes, not source text.
- `pair_features.parquet`: per (query, candidate) signals used by the strategies.
- `MANIFEST.json`: SHA-256 and size of each file, plus counts.

Total about 680 MB. These files are not in git; they are meant for a Zenodo or Hugging Face release after approval.

## Known limitations

- **Silver labels.** Labels come from comments, not from annotators. Some "in favor of" links join a small fix to a
  larger PR that includes it (subsumed), which is not a clean duplicate. An LLM audit (Claude Haiku 4.5,
  `experiments/label_audit/`) judged 79.0% [73.5, 84.5] of 200 random labels a duplicate or replacement, rising to 97.5% if
  subsumed is counted. For all 342 cross-author pairs the figures are 84.8% and 96.2%. The main Recall@1 result holds on the audit-valid
  subset.
- **Link bias.** Many duplicate PRs reference each other, so a trivial links-only rule reaches 0.839 cross-author
  Recall@1. Results on the no-link subset are reported separately.
- **Agent PRs only.** AIDev has no matching human PRs for the same repositories and time, so agent-vs-human pairs
  could not be built (the GitHub token for extra retrieval was invalid).
- **Missed duplicates.** Duplicates that nobody commented on are invisible, so no-duplicate queries may contain a few
  unlabelled duplicates (false alarms are slightly overstated).
- **Self-replacement dominates** (82% of labelled pairs). Results are reported per relation.

## License and attribution

Derived from AIDev (CC BY 4.0). Redistribution must credit Li et al. and keep the license. PR text is public GitHub
content as included in AIDev.
