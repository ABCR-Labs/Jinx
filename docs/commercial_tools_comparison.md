# AgentDup vs. commercial PR tools (CodeRabbit and others)

Checked on 9-10 Nov 2026 from each vendor's own docs (and source code where it is open). "Not found" means I searched the vendor's full docs for duplicate / similar PR / related PR and found no duplicate-PR feature. It does not prove that no hidden feature exists.

## Short answer

None of the big AI code-review tools detects **duplicate pull requests** against the open-PR queue as a documented feature.
- They review the code *inside* one PR.
- Where duplicate detection exists (CodeRabbit, Qodo/PR-Agent, Dosu), it is for **issues**, not PRs.
- The closest PR feature is CodeRabbit's "Related PRs". It lists PRs that touched the same code areas, as context for the reviewer. It is not a duplicate alarm.
- The tools that really target duplicate PRs are the small open-source bots we already benchmarked: Simili, PRSense, PRism, vector-triage and contrib-guard.

## Comparison table

| Tool | Duplicate **PR** detection? | Duplicate **issue** detection? | How it matches | Cost / runs where | Explains why? | Evidence |
|---|---|---|---|---|---|---|
| **AgentDup (ours)** | Yes: new PR vs. every open PR in the repo, ranked | No | Template-stripped text + shared files + shared hunks/lines + linked issue + time/author context, logistic regression; optional local MiniLM | Free, CPU, GitHub Action with `GITHUB_TOKEN`, no LLM | Yes (shared files, lines, issue, text) | Our benchmark |
| **CodeRabbit** | No. "Related PRs" in the walkthrough = "Merged and open PRs that touched the same areas of the codebase" (context only, on by default) | Yes, "Issue Enrichment → Duplicate Detection" (GitHub, open beta) | Not documented (LLM-based SaaS) | Paid SaaS, closed source | Lists links only | docs.coderabbit.ai/pr-reviews/walkthroughs, /issues/enrichment |
| **Qodo Merge / PR-Agent** | No | Yes, `/similar_issue` tool | OpenAI `text-embedding-ada-002` + Pinecone / LanceDB / Qdrant (seen in pr-agent 0.50.0 source) | Needs an OpenAI key | No | pr_agent/tools/pr_similar_issue.py |
| **GitHub (native)** | Manual only: a maintainer types "Duplicate of #N" | Manual only | None (a human decides) | Free | n/a | docs.github.com "Marking issues or pull requests as a duplicate" |
| **GitHub Copilot code review** | Not found | Not found | Reviews the code of one PR | Paid Copilot plan | n/a | docs.github.com Copilot code review |
| **Greptile** | Not found | Not found | Codebase-aware LLM review | Paid SaaS | n/a | docs.greptile.com (full docs searched) |
| **Graphite (Diamond)** | Not found | Not found | LLM review + stacked PRs | Paid SaaS | n/a | Graphite docs (full docs searched) |
| **Ellipsis** | Not found | Not found | LLM review | Paid SaaS | n/a | docs.ellipsis.dev (full docs searched) |
| **Sourcery** | Not found (only *code* duplication inside a PR) | Not found | LLM + rules review | Paid SaaS | n/a | docs.sourcery.ai (full docs searched) |
| **Dosu** | Not found | Its "Triage" agent template "flags duplicates" on issues | LLM agent | Paid SaaS | Not documented | docs.dosu.dev |
| Simili-bot | Yes | Yes | Embeddings (Gemini/OpenAI) + LLM | Needs paid key | Partly | Benchmarked (re-impl) |
| PRSense | Yes | No | Text 0.45 + diff 0.35 + files 0.20 | Local ONNX (placeholder tokenizer) or API | Score only | Benchmarked (re-impl) |
| PRism | Yes | No | OpenAI embedding + LLM check | Needs OpenAI | LLM text | Benchmarked (re-impl) |
| vector-triage | Yes | Yes | GitHub Models embedding + SQLite FTS5, RRF | Needs GitHub Models | No | Benchmarked (re-impl) |
| contrib-guard (phoenix) | Yes | No | TF-IDF title+body, threshold 0.4 | Free | Score only | Benchmarked (exact port) |
| contrib-guard (balyakin) | Yes | No | Title Jaccard + same files | Free | Score only | Benchmarked (own code) |

## What this means for the paper

1. **Positioning:** the market leaders review code inside one PR. They do not answer "is this PR already open somewhere else?" That gap gets bigger with coding agents, because several agents (or several runs of one agent) often open PRs for the same issue.
2. **Head-to-head:** the fair head-to-head is against the tools that actually do duplicate-PR detection, which we already ran. AgentDup beats the best of them (contrib-guard) by +5.3 points Recall@5 and +12.3 points Recall@1 on cross-author pairs, both CI-backed.
3. **CodeRabbit "Related PRs":** this is the only commercial feature near our task. Measuring it would need CodeRabbit installed on real repos (a paid or trial account, and a public action), so it needs your approval. Without that, we describe it in related work as context, not a duplicate detector.
4. **Claims to avoid:** "CodeRabbit misses duplicates". We haven't tested it, and its PR feature isn't built for duplicates.
