# Tool-paper shortlist (2026-11-09)

## What HeapLens (Sachin, SPLASH'26 Tool Demo) actually is
- Incumbents already existed (Eclipse MAT, VisualVM, IntelliJ). Contribution = faster engine (14.8 GB dump in 9.5 s), in-editor source jump, LLM diagnosis panel, 2,900 installs, Zenodo archive.
- Lesson: "a tool already exists" is not disqualifying. A tool paper needs a head-to-head benchmark vs incumbents on real artifacts + adoption evidence.

## Issue mining (top open issues by +1, Nov 2026) - see top_issues.json
- claude-code: usage limits burn fast (697+1/1499 comments; 477/879), AGENTS.md support (459), multi-account, scroll bugs.
- codex: LSP integration (510), /undo (498), /rewind (230), IDE diff approval (241).
- ollama: reranking (290), MCP (222), context-window mgmt (78) + silent truncation issues.
- llama.cpp/cline/litellm: local models print tool calls as text/XML (60-comment threads).
- vllm/sglang: roadmaps only, little user pain.

## Collision check per candidate
| Idea | Pain evidence | Existing tools | Papers | Verdict |
|---|---|---|---|---|
| AgentDup GitHub Action (duplicate agent PRs) | GitHub "Eternal September" blog; "AI Slop is DDoSing OSS" 2607.04003; Godot policy | Simili, PRSense, vector-triage, PRism, contrib-guard: none benchmarked | 8 papers count problem, none detect | BUILD |
| Agent secret-leak scanner (.claude/settings.local.json etc.) | Ars/THN/GitGuardian this week: 1,122+ public repos | GitGuardian, gitleaks, agentleaks | Credential leakage in skills 2604.03070; Radware "new .env" | Maybe: benchmark of what scanners miss; needs GH token; crowding fast |
| Tool-call rescue library | llama.cpp, cline, litellm, hermes issues | toolcall-rescue, tool-call-repair, callpatch, openclaw, 5+ more | REALM'26 2609.26693; blog: lenient parser rescued 0/75 | Weak: gain may be ~0 |
| GGUF template/eos/tokenizer checker | Unsloth template fixes, Qwen eos issues | ggufdoctor, c4nary, Ingot reports | Broken on Arrival 2609.05881; EMNLP-industry'26 | Crowded |
| Agent token/cost profiler | claude-code usage-limit threads | ccusage, 15+ analyzers | TokenMeter, Tokenomics 2601.14470, 2604.22750 | Crowded |
| Agent undo/rewind | codex /undo, /rewind | mulligan, unwreck, git-rewind, pi-rewind | - | Product feature, crowded |
| AGENTS.md compliance checker | gemini/claude issues | agnix, agentlint, 5+ | 2611.04367, 2608.11727, 2605.10039, ContextCov | Crowded |
| PyTorch OOM analyzer | universal | memory_viz, Mosaic, Denpex, memviz-neo | several | Crowded |
| VRAM / will-it-fit calculator | universal | 10+ calculators, accuracy reports | - | Crowded |
| CI log root cause | universal | 5+ actions | LogDx-CI, LogSieve, LogSage, GHA-Agent | Crowded |

## Tool-demo venues
- ICPC 2027 Tool Demo: Nov 19, 2026
- EASE 2027: abstract Jan 15, paper Jan 22
- FSE 2027 Tool Demos: Jan 26, 2027 (4 pages)
- ICSE 2027 demos: closed (Oct 24); MSR 2027 data/tool: Nov 10 (too late)
- ACL 2027 demos: date not yet posted
