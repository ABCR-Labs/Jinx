# AgentDup

Find likely **duplicate pull requests** in a repository's open-PR queue, built for PRs opened by coding agents
(Copilot, Codex, Devin, Claude Code, Cursor, Jules).

Agent PRs share long boilerplate ("## Summary ... ## Testing ... Generated with ..."), so plain text similarity
says two unrelated agent PRs look alike, and misses a real duplicate written in different words. AgentDup:

1. **removes agent template text** (lines learned from 361k agent PRs in the AIDev dataset, plus lines repeated
   across the current queue);
2. compares **what code is changed**: shared files, overlapping changed line ranges, identical added lines;
3. checks **links**: same linked issue, or one PR mentioning the other;
4. adds context (same author, time gap) and an optional **local** embedding model.

A small logistic model combines these into one score, and every match comes with plain reasons.
No LLM, no API key, runs on CPU.

## 30-second quickstart

```bash
pip install ./agentdup            # or: pip install "./agentdup[embed]" for the optional local embedding model
agentdup check examples/new_pr.json --open-queue examples/open_prs.jsonl
```

```
PR #103: checked 2 open PRs in 2 ms. 1 likely duplicate(s) (score >= 0.50).
  DUPLICATE? #101  score 0.82  Fix login timeout
               - shares 1 of 1 changed files (auth/session.py)
               - 100% of changed line ranges overlap
             #102  score 0.04  Add dark-mode toggle
               - weak match
```

Input is GitHub-API-shaped JSON (`number`, `title`, `body`, `user.login`, `created_at`) plus optional
`diff` (unified diff text), `files`, `agent`, `linked_issues`. The queue is a JSON list or JSON-lines file.
Add `--json` for machine-readable output, `--embed` to use the local embedding model.

## GitHub Action

`action.yml` runs AgentDup on `pull_request_target` (opened/reopened), compares the new PR with up to
`max-open-prs` open PRs, and posts (or updates) one comment when a score passes `threshold`.
It only reads PRs and writes one comment with the workflow token. See `.github/workflows/agentdup.yml`.

## Learn templates for your own PRs

```bash
agentdup learn-templates corpus.jsonl -o my_templates.json   # JSON-lines with agent, repo, body
agentdup check new.json --open-queue open.jsonl --templates my_templates.json
```

## Development

```bash
pip install pytest ruff && python -m pytest -q && ruff check src tests
```

## Benchmark and strategy study

`experiments/` holds the live-queue benchmark on AIDev and a comparison of 60+ duplicate-detection strategies (lexical, code overlap, embeddings, existing bots, learned models, cross-encoders, LLM judges, cascades). Read `experiments/report/REPORT.md` (or open `experiments/report/agentdup_strategy_report.html`). Raw results are in `experiments/results/`, run logs in `experiments/logs/`.
License: MIT.
