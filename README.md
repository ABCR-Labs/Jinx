# Jinx

Find likely **duplicate pull requests** in a repository's open-PR queue, built for PRs opened by coding agents
(Copilot, Codex, Devin, Claude Code, Cursor, Jules).

Agent PRs share long boilerplate ("## Summary ... ## Testing ... Generated with ..."), so plain text similarity
says two unrelated agent PRs look alike, and misses a real duplicate written in different words. Jinx:

1. **removes agent template text** (lines learned from 361k agent PRs in the AIDev dataset, plus lines repeated
   across the current queue);
2. compares **what code is changed**: shared files, overlapping changed line ranges, identical added lines;
3. checks **links**: same linked issue, or one PR mentioning the other;
4. adds context (same author, time gap) and an optional **local** embedding model.

A small logistic model combines these into one score, and every match comes with plain reasons.
No LLM, no API key, runs on CPU. (Formerly named AgentDup.)

## 30-second quickstart

```bash
pip install .                   # from the repo root; pip install ".[embed]" adds the optional local embedding model
jinx check examples/new_pr.json --open-queue examples/open_prs.jsonl --top 2
```

The example is a real live queue from AIDev (huggingface/transformers #44134 and the 19 PRs open when it was created; CC BY 4.0).

```
PR #44134: checked 19 open PRs in 12 ms. 1 likely duplicate(s) (score >= 0.50).
  DUPLICATE? #44110  score 1.00  refactor(tvp): use capture_outputs for output tracing
               - one PR links to the other (#44110)
               - shares 1 of 1 changed files (src/transformers/models/tvp/modeling_tvp.py)
               - 100% of changed line ranges overlap
               - 100% of added lines are identical
               - similar title/description after removing agent template text (0.92)
             #44133  score 0.08  refactor(poolformer): use capture_outputs for output tracing
               - similar title/description after removing agent template text (0.50)
               - same author (possible re-opened or replacement PR)
```

Input is GitHub-API-shaped JSON (`number`, `title`, `body`, `user.login`, `created_at`) plus optional
`diff` (unified diff text), `files`, `agent`, `linked_issues`. The queue is a JSON list or JSON-lines file.
Add `--json` for machine-readable output, `--embed` to use the local embedding model.

## Shipped weights

`src/jinx_pr/data/weights.json` (lexical) and `weights_emb.json` (with `--embed`) are logistic models trained on all
4,832 AIDev live-queue queries by `experiments/bench_v2/train_package_weights.py`, with the same recipe as the
cross-validated benchmark. Score 0.5 is set by the benchmark threshold rule (2.5% false alarms on PRs with no
duplicate in cross-validation); pass `--threshold` to trade recall for fewer alerts. `tests/test_e2e_aidev.py` runs the CLI on three
real AIDev queues.

## GitHub Action

`action.yml` runs Jinx on `pull_request_target` (opened/reopened), compares the new PR with up to
`max-open-prs` open PRs, and posts (or updates) one comment when a score passes `threshold`.
It only reads PRs and writes one comment with the workflow token. See `.github/workflows/jinx.yml`.

## Learn templates for your own PRs

```bash
jinx learn-templates corpus.jsonl -o my_templates.json   # JSON-lines with agent, repo, body
jinx check new.json --open-queue open.jsonl --templates my_templates.json
```

## Development

```bash
pip install pytest ruff && python -m pytest -q && ruff check src tests
```

## Benchmark and strategy study

`experiments/` holds the live-queue benchmark on AIDev and a comparison of 60+ duplicate-detection strategies (lexical, code overlap, embeddings, existing bots, learned models, cross-encoders, LLM judges, cascades). Read `experiments/report/REPORT.md` (or open `experiments/report/jinx_strategy_report.html`). Raw results are in `experiments/results/`, run logs in `experiments/logs/`.
License: MIT.
