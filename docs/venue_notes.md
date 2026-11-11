## Venues (checked 10 Nov 2026 on the official call pages)

| | ICPC 2027 Tool Demonstration | FSE 2027 Tool Demonstrations | ICPC 2027 RENE (empirical paper) |
|---|---|---|---|
| Deadline (AoE) | **Thu 19 Nov 2026** (notification 14 Jan, camera-ready 28 Jan) | **Tue 26 Jan 2027** (notification 17 Mar, camera-ready 2 Apr) | abstract 11 Dec, paper 18 Dec 2026 |
| Length | 4 pages + 1 page references, IEEE `\documentclass[10pt, conference]{IEEEtran}` | 4 pages + 1 page references, ACM format | new replication / negative result: 10 + 2 pages, IEEE |
| Review | not anonymous | single-blind | not anonymous |
| Tool / artifact | source or binaries **must be publicly available** (GitHub, Zenodo, Figshare or website) | availability, maturity, user base, link to source expected | - |
| Video | optional but encouraged: 3-5 min screencast URL in the abstract (YouTube or tool site) | link to a screencast expected; demo walkthrough appendix (not counted) | - |
| Proceedings | ICPC proceedings (ACM/IEEE DL) | main FSE proceedings, ACM DL; one author must register (not one-day) and present | ICPC proceedings |
| Overlap rule | IEEE/ACM plagiarism + submission policies | "must present new content ... not previously published as a main contribution in any venue"; tool must not already be a main contribution of a research paper | "must not be under review or submitted for review elsewhere" |

### Dual-submission overlap
- A Tool Demo paper and the RENE paper must not be the same paper. Safe split:
  - **Tool Demo** = the tool: design, the GitHub Action workflow, the live-queue head-to-head against existing bots, latency, a short adoption/usage story.
  - **RENE** = the empirical study: do classic duplicate-PR detectors (Li 2017, INTRUDE 2019, time-aware 2019) replicate on agent PRs, live-queue vs random-pair evaluation, template effects, label-noise analysis, negative results.
- Shared benchmark numbers would appear in both. Under the RENE rule ("must not be under review ... elsewhere") the main results table of one paper should not be the main contribution of the other. Each paper should cite the other as under review, and the RENE paper should treat AgentDup as one row, not its contribution.
- FSE Tool Demos explicitly forbids a tool that is already the main contribution of a research paper. If AgentDup becomes the main contribution of an ICPC paper, FSE Tool Demos is closed, and vice versa.
