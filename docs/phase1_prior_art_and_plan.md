# PRDupeCheck: Phase 1 Report (prior art, data check, plan)

Date: 9 Nov 2026. Status: **plan only. No experiments, no paid API calls, no GPU runs yet.**

**Verdict, short version: PIVOT (a small one), then GO.** The plain idea ("run old duplicate-PR detectors on agent PRs") is only an audit, and it fails the "new method + new metric + impact" bar. The pivoted version passes it:
**(a)** a new evaluation metric that copies how a maintainer actually meets duplicates (the "live-queue" metric), and **(b)** a small agent-aware detector (**AgentDup**) that is scored with that metric against the classic detectors.
Target: **ICPC 2027 RENE** (paper due 18 Dec 2026). Chance of acceptance: **medium (about 40-50%)**. Reasons and risks are in Section 7.

---

## 1. Background and the problem

**Pull request (PR):** a proposed code change on GitHub that a maintainer reviews, then merges or closes.
**Duplicate PR:** a PR that does the same job as another PR (for example, both fix the same bug). Maintainers waste review time on the second one, and one of the two is closed.
**Duplicate-PR detector:** a tool that, when a new PR is opened, lists earlier PRs that may be doing the same thing.
**Coding agent:** an AI tool that writes code and opens PRs by itself (GitHub Copilot coding agent, OpenAI Codex, Devin, Claude Code, Cursor, Google Jules).

Classic detectors (2017-2024) were built and tested on PRs written by people. Agent PRs are different in three ways that matter here:

1. **Shared boilerplate (template text).** Each agent writes its PR description in a fixed style ("## Summary ... ## Testing ... Generated with Claude Code"). We measured this on AIDev: in samples of 3,000 PRs per agent, **11.8% to 22.3% of description lines are repeated template lines**. A text-similarity detector sees two Copilot PRs as "similar" just because they share the template.
2. **Duplicates come in a new shape.** The most common pattern is not "two strangers fix the same bug". It is "the agent (or its user) opens PR #12, it fails, and opens PR #13 that *supersedes* it", or "PR #20 *consolidates* #15, #16 and #17". In our data, more than half of duplicate comments are written by the PR's own author.
3. **Speed.** Agents open many PRs close together. The median time gap between a PR and the PR that replaces it is about **5.8 hours** in our data.

**Concrete example (made-up but typical):**

- PR #101 by Copilot: "Fix login timeout. ## Summary: This PR updates the session handler... ## Testing: Added unit tests." Changes `auth/session.py`.
- PR #102 by Copilot, same repo, same day: "Add dark-mode toggle. ## Summary: This PR updates the settings page... ## Testing: Added unit tests." Changes `ui/settings.tsx`.
- PR #103 by Devin, opened later: "Increase idle limit for user sessions." Changes the same lines of `auth/session.py` as #101.

A text-only detector says #101 and #102 look alike (shared template, many shared words) -> **false alarm**. It misses that #103 duplicates #101 (different words, same code) -> **missed duplicate**. A useful detector must ignore the template and look at what code is changed and which issue is being fixed.

How big is the problem? Ehsani et al. (MSR 2026) hand-labelled 600 failed agent PRs: **142 (23.7%) were closed as duplicates**, the second most common failure reason after "abandoned". Nakashima et al. found "implemented by other PRs/developers" behind 9.2% of rejected agent PRs (15.6% for human PRs).

---

## 2. Literature matrix

How we searched: arXiv listing search (queries: duplicate pull request, redundant/superseded PR, agentic PR, AIDev), Crossref and Semantic Scholar lookups by DOI and title, Research Square, venue pages, and citation chasing from the papers below. Google Scholar could not be scraped from this machine, so we used Semantic Scholar instead. ACL Anthology was not searched in depth (this is a software-engineering topic; no hits expected).
Every citation below was checked on a primary page (arXiv abstract page, DOI/Crossref record, or the PDF). "Full text" means we read the paper, not only the abstract.

### 2a. Classic duplicate-PR detection (human PRs)

| Paper (verified) | What it does | Data | What it does NOT do | Threat to us |
|---|---|---|---|---|
| Li, Yin, Yu, Wang, Wang. "Detecting Duplicate Pull-requests in GitHub." Internetware 2017. DOI 10.1145/3131704.3131725. *(abstract only; paywalled)* | First detector: TF-IDF text similarity of title + description, ranks earlier PRs. | Human PRs, a few large projects. | No code, no issues, no agents. | Low. It is our simplest baseline. |
| Yu, Li, Yin, Wang, Wang. "A Dataset of Duplicate Pull-Requests in GitHub." MSR 2018. DOI 10.1145/3196398.3196455. | DupPR dataset of duplicate pairs labelled from maintainer comments. | 2,323 pairs, 26 repos (count from INTRUDE paper). Repo whystar/MSR2018-DupPR, **MIT license** (checked LICENSE file). | No agents (pre-2019). | Low. Shows comment-based labels are an accepted method; usable as a human reference set. |
| Ren, Zhou, Kästner, Wasowski. "Identifying Redundancies in Fork-based Development" (INTRUDE). SANER 2019. DOI 10.1109/saner.2019.8668023. **Full text.** | 9 "clues" (title, description, patch text, changed files, changed code location, issue reference...) fed to a classifier. 57-83% precision. | DupPR (1,174 train / 1,149 test positive pairs) + **100,000 random negative pairs**. Code at github.com/luyaor/INTRUDE (no license file found). | Negatives are random pairs (easy). No template handling. Drops same-author pairs. | Medium. Already uses issue ref + code location, so "use diff + issue" alone is NOT new. Its random-negative protocol is what our new metric challenges. |
| Wang, Xu, Xia, Wang, Li. "Duplicate Pull Request Detection: When Time Matters." Internetware 2019. DOI 10.1145/3361242.3361254. *(abstract)* | Adds a time feature to INTRUDE-style features. | Human PRs (exact repos not checked; PDF could not be downloaded). | No agents, no templates. | Low-medium. Time feature is not new; we use it as a baseline feature. |
| Zhang, Chen, Gu, Zou, Xie, Jia. "How do Multiple Pull Requests Change the Same Code: A Study of Competing Pull Requests in GitHub." ICSME 2018. DOI 10.1109/icsme.2018.00032. *(abstract)* | Empirical study of PRs that change the same code. | Human PRs. | No detector, no agents. | Low. Supports the code-overlap idea. |
| Li, Yu, Zhou, Wang, Yin. "Redundancy, Context, and Preference: An Empirical Study of Duplicate Pull Requests in OSS Projects." IEEE TSE 2022. DOI 10.1109/tse.2020.3018726. *(abstract)* | Why duplicates happen, which one maintainers keep. | Human PRs, 26 repos. | No detector, no agents. | Low. Gives the "which PR is kept" framing. |
| Jiang, Li, Guo, Li, Zhang, Li. "DupHunter: Detecting Duplicate Pull Requests in Fork-Based Development." IEEE TSE 2023. DOI 10.1109/tse.2023.3235942. *(abstract; paywalled)* | Graph/embedding detector, beats INTRUDE. | Human PRs. | No agents; no public code found yet. | Medium. Strong baseline we may not be able to rerun exactly. |
| Liao, Liu, Lan, Sun. "DupLLM: Duplicate Pull Requests Detection Based on Large Language Model." APSEC 2024. DOI 10.1109/apsec65559.2024.00023. *(abstract; paywalled)* | LLM writes a summary of each PR; summaries are embedded and compared. Reports P@1 = 0.929. | Human PRs. | No agents. Agent PRs already *are* LLM text, so LLM summaries may make all agent PRs look alike. | Medium. Closest "modern" baseline. We will re-implement it from the paper description with an open model. |
| Galbraith, Greer. "Detecting Duplicate Effort in GitHub Contributions." ENASE 2025. DOI 10.5220/0013289000003928. **Full text.** | Joins issues and PRs; title + description similarity; labels from regex on comments. Accuracy 93.9%, recall 90.5%. | 15 human repos. | No code features, no agents, no template handling. | **Medium-high for the "linked issue" idea**: issue + PR text is already done. We must not claim it as new. |
| Ben Chekaya, Garrouch, Omri. "Duplicate Pull Requests in Code Management Platforms: A Systematic Literature Review." Research Square preprint 2026, DOI 10.21203/rs.3.rs-8732393/v1. *(not peer-reviewed)* | Reviews 11 primary studies; recall 55-83% (TF-IDF) up to ~92% (newer). | - | Nothing on agent PRs in the abstract. | Low. Useful to show the field has not looked at agents. |

### 2b. Agent-PR studies (2026)

| Paper (verified arXiv id) | What it does | Data | What it does NOT do | Threat to us |
|---|---|---|---|---|
| Ehsani et al. "Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub." arXiv:2601.15195 (MSR 2026). **Full text.** | Hand-labels why 600 agent PRs failed. Duplicate = 142 (23.7%). Says agents should check for ongoing work. | 600 PRs from AIDev; CSV in replication package (no license file; evaluation use only). | No detector. Labels give the duplicate PR but **not its partner PR**. | Low. It is our motivation and our human reference labels. |
| Abujadallah, Arabat, Sayagh. "Understanding the Rejection of Fixes Generated by Agentic Pull Requests - Insights from the AIDev Dataset." arXiv:2606.13468. **Full text.** | Why agent fix-PRs are rejected; "superseded" = 18 of 306 (5.9%). Calls for duplicate-PR research to be redone for agents. | 306 PRs from AIDev. | No detector. (Scout note said a figshare label file exists; **we did not find the link**, so we do not rely on it.) | Low. Supports the gap. |
| Nakashima et al. "Why Agentic-PRs Get Rejected: A Comparative Study of Coding Agents." arXiv:2602.04226. **Full text.** | Rejection reasons per agent **and for human PRs**. "Implemented by other PRs/developers": 9.2% of rejected agent PRs vs 15.6% of rejected human PRs. | 654 rejected PRs, Zenodo, CC BY 4.0. | No detector. | Low. Gives a small human-vs-agent comparison. |
| Alam, Mondal, Roy. "Why Are AI Agent Involved Pull Requests (Fix-Related) Remain Unmerged?" arXiv:2602.00164. **Full text.** | Unmerged fix PRs; the top reason is "Resolved by Another Pull Request": 72 of 326 (22.1%). | 326 PRs; Zenodo CC BY 4.0. | No detector. | Low. |
| Xu et al. "AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates." arXiv:2607.04697. **Full text.** | Co-active agent PRs that touch the same files; replays 747 merges to measure conflicts. | AIDev. | Studies *conflicts*, not *duplicates*. | Medium. Closest data work; we must show duplicates are a different relation from "touch the same file". |
| Sarkar. "Before the Pull Request: Mining Multi-Agent Coordination." arXiv:2606.19616. **Full text.** | Coordination layer so agents don't redo each other's work *before* a PR exists. | Synthetic multi-agent runs. | No PR-level detector, no real GitHub labels. | Medium (validity): some duplicate work never becomes a PR. We frame our tool as the safety net *after* PR creation. |
| Khemissi et al. "Humans Integrate, Agents Fix: How Agent-Authored Pull Requests Are Referenced in Practice." arXiv:2604.04059. *(full text, skim)* | Why PRs reference agent PRs (4.2% agent-to-agent). | AIDev. | No duplicate detection. | Low. |
| Li et al. "AIDev: Studying AI Coding Agents on GitHub." arXiv:2602.09185. | Dataset paper. | AIDev. | No duplicate study. | None (data source). |

### 2c. Neighbouring field: duplicate bug-report detection

| Paper | Relevance |
|---|---|
| Zhang et al. "Duplicate Bug Report Detection: How Far Are We?" TOSEM, arXiv:2212.00548. | Showed that old benchmarks overstate results and simple methods are competitive once the test setup is realistic. **Same argument as our new metric**, but for bug reports, not PRs and not agents. |
| CUPID, arXiv:2308.10022. | LLM + classic retrieval for duplicate bug reports. Template for an "LLM step + cheap retrieval" baseline. |

### What is still open (plain statement)

- **No paper tests any duplicate-PR detector on agent PRs.** Our arXiv / Crossref / Semantic Scholar search found none as of 9 Nov 2026. (This is a search result, not proof; the AIDev area is busy, so we re-check before submission.)
- **No paper handles agent template text** in duplicate detection.
- **No paper evaluates duplicate-PR detectors the way they are used**: at the moment a PR is opened, against the PRs actually open in that repo. Classic work uses random negative pairs (INTRUDE: 100k random merged pairs), which are mostly easy.
- **No paper separates the new agent relations** (self-supersede, consolidation, cross-agent duplicate) from classic "two people did the same work".

---

## 3. Gap / New metric / Impact

### (1) The gap (from the matrix)
All 10 detector/study papers in 2a use human PRs. All 8 agent-PR papers in 2b *measure* duplicates (up to 23.7% of failed agent PRs) but none *detects* them. And the standard way to score detectors (random negatives, pairs only) was never checked against the real situation of a busy repo full of same-template agent PRs.

### (2) What we introduce, and how we show it is better

**New metric: "live-queue" scoring (LQ@k and false-alert budget).**
For each new PR, the detector only sees the PRs that were really open (or closed in the last 7 days) in the same repo at that moment. It must put the true duplicate in its top k. We report:
- **LQ-Recall@k** (k = 1, 5): share of real duplicates found in the top k;
- **Precision at a fixed alert budget**: if the tool may post at most 1 warning per 20 new PRs, how many warnings are right;
- results split by relation type (self-supersede / same-agent other-author / cross-agent / agent-vs-human).

How we show the metric is better than the classic one (random-negative pair F1):
- **It catches errors the old metric misses.** We count how many top false alarms in the live queue are same-agent, same-template PRs. Random negatives almost never contain them, so the old metric cannot see this failure. Test: the share of "template" false alarms in live-queue vs random-pair evaluation.
- **It changes the conclusion.** We report whether the ranking of detectors changes between the two metrics (Kendall's tau between the two rankings). If the ranking flips, the old metric gives the wrong advice for agent repos.
- **It agrees better with human decisions.** On the Ehsani 142 human-labelled duplicates (and their 458 non-duplicate failed PRs), we check which score, computed per PR, better separates "human said duplicate" from "human said other reason" (AUC). This uses existing human labels only.

**New method: AgentDup (a small CPU tool, no paid model).**
1. **Template stripping:** learn each agent's repeated lines from AIDev itself (lines that appear in many PRs of that agent) and remove them before any text comparison. No hand-written rules per agent.
2. **Code-change match:** overlap of changed files and of changed line ranges (hunks), plus a "containment" score so a consolidation PR that includes another PR's change is matched.
3. **Linked-issue match:** same linked issue (from AIDev `related_issue`). Not new on its own (INTRUDE, Galbraith & Greer), but a useful feature.
4. **Open embedding model** (e.g. a small code/text embedding model run on CPU) on the stripped text.
5. A small classifier (logistic regression / gradient boosting) trained with **repo-grouped cross-validation** (test repos never seen in training).

Expected (NOT measured yet): AgentDup beats Li 2017, INTRUDE, the time-aware variant, and a DupLLM-style baseline on LQ-Recall@5 on cross-author duplicates, and produces fewer template false alarms. If it does not, we still have a negative result plus a metric, which RENE accepts, but the paper is weaker.

**Why this is not "fixing an eval prompt":** there is no prompt. The contributions are a scoring protocol (a new metric) and a detector built from code-change and template features. Both are reusable on any repo.

### (3) Impact: who changes what
- **Maintainers of busy repos with agent PRs** (e.g. openclaw had 418 of our duplicate pairs): run AgentDup as a GitHub Action that comments "possible duplicate of #N" when a PR opens, instead of noticing by hand days later.
- **Agent builders (Copilot, Codex, Devin, Claude Code harnesses):** call the same check *before* opening a PR ("is there an open PR for this issue already?"), which is exactly what Ehsani et al. recommend.
- **Researchers:** stop scoring duplicate-PR detectors with random negatives; use live-queue scoring. We release the scoring script and the label-extraction script (derived from public comments; no new annotation).

All three parts are met **only in the pivoted form**. The original "run old detectors on agent PRs" form fails part (2) -> that is why the verdict is PIVOT.

---

## 4. Data feasibility: how many labelled duplicates really exist

All counts below were measured on the downloaded files (read-only).

| Source | What it gives | Count | Quality |
|---|---|---|---|
| AIDev v5 `pull_request` (HF: hao-li/AIDev, **CC BY 4.0**, cutoff 31 Mar 2026) | Agent PRs | 361,296 (Claude Code 172,597; Copilot 98,384; Codex 62,731; Cursor 12,908; Devin 11,219; Jules 3,457). Full table `all_pull_request`: 7,685,281. | - |
| Ehsani et al. 600-PR CSV | Human label "Duplicate PRs" | **142 PRs** (131 found in AIDev v5) | Gold, but **no partner PR** given. Only 47 of 131 have a comment with a PR number. So these are 142 PR-level labels, **not** 142 pairs. |
| AIDev comments, strict phrases + PR number ("duplicate of #N", "superseded by #N", "in favor of #N", "replaced by #N", "same as #N") | Directed pairs | **3,798 pairs**, 3,766 PRs, 1,408 repos | Silver. Mix: superseded by 1,813; in favor of 1,209; duplicate of 473; replaced by 189; other 114. 2,017 comments are by the PR's own author. Only 68 by bots. |
| ... of which the other PR is also an AIDev agent PR | agent-agent pairs | 1,878 (1,533 same author; **345 different author**) | The other 1,920 point to PRs not in AIDev (mostly human PRs, or agents not tracked); need GitHub API to fetch them. |
| Broader phrases (adds "already fixed in #N", "covered by #N", "resolved in #N"...), closed-unmerged PRs only | PRs | 5,011 PRs (2,424 with the comment written by someone other than the author) | Noisier; upper bound. |
| AIDev timeline `marked_as_duplicate` events | GitHub's own duplicate mark | 48 events, 47 PRs | Very clean, very small. |
| AIDev `related_issue`: issues linked to 2+ PRs | Candidate groups | 9,377 issues, 30,234 PRs | **Not labels.** Many are follow-up PRs, not duplicates. Used only for candidate search and as a feature. |
| DupPR (Yu et al. 2018), MIT | Human duplicate pairs | 2,323 pairs, 26 repos | Gold-ish (comment-based); used to check that our re-implemented baselines behave as published. |

**Bottom line:** there are enough labels. The hard, interesting subset (different-author duplicates) is about **345 agent-agent pairs + up to ~1,900 agent-vs-other pairs**, before cleaning. The 3,798 figure must not be reported as "3,798 duplicates": about half are self-supersede, which we will report as its own (easy) category.

**Label check without new annotation:** the user said small self spot-checks are fine. I will read a random 100 silver pairs and report precision of the extraction rule (this is a check of my own script, not a new labelled dataset). We also report agreement of silver labels with the 48 timeline marks and the Ehsani labels where they overlap.

**Data dependency:** PR diffs for pairs and human PRs outside AIDev need the GitHub REST API (free, public data). The stored token `GH_TOKEN_HARSHUL` returned **401 Bad credentials** today, and unauthenticated calls are rate-limited after a few calls. AIDev's `pr_commit_details` table (12.45 GB, 12.1M rows) has per-file patches for agent PRs, so most diffs can come from AIDev itself; the API is only needed for non-AIDev targets.

---

## 5. Experiment plan (needs your OK before anything runs)

**Datasets:** AIDev v5 (CC BY 4.0) tables `pull_request`, `pr_comments`, `pr_timeline`, `related_issue`, `pr_commit_details`; Ehsani 600 CSV (evaluation only, no redistribution); DupPR (MIT) as sanity check.

**Tasks:**
- T1 (main): live-queue ranking. For each labelled PR, rank the PRs open in its repo at its creation time.
- T2 (classic, for comparison): pair classification with random negatives, as in INTRUDE.
- T3 (human agreement): per-PR "has a duplicate" score vs Ehsani labels (AUC).

**Baselines:**
1. Li 2017: TF-IDF on title + description.
2. INTRUDE: run the public code (github.com/luyaor/INTRUDE) or re-implement its 9 clues.
3. Wang 2019: INTRUDE clues + time.
4. DupLLM-style: open LLM writes a summary, then embed and compare (re-implementation from the paper; noted as such).
5. Galbraith & Greer style: issue + PR text similarity.
6. Plain embedding similarity (no template stripping).
7. DupHunter only if code is found; otherwise listed as "not reproducible".

**Our method:** AgentDup (Section 3).

**Metrics:** LQ-Recall@1/@5, MRR (mean reciprocal rank: 1 / position of the true duplicate, averaged), precision at a fixed alert budget, classic pair F1, AUC vs human labels, Kendall's tau between metric rankings. All with bootstrap 95% confidence intervals and split by agent and relation type.

**Ablations:** AgentDup without template stripping / without code-change match / without linked issue / without time / without embeddings; raw vs stripped text for every baseline.

**Compute and cost estimate:**

| Item | Where | Estimated cost |
|---|---|---|
| Label extraction, TF-IDF, INTRUDE features, AgentDup training, all metrics | This VM, CPU | $0 |
| Small open embedding model on ~100k PR texts | CPU (a few hours) or 1 GPU hour | $0 on CPU; about $1-2 on GPU |
| DupLLM-style summaries with an open 7-8B model (~30k PRs) | GPU (e.g. 1x A10G/L4 for ~2-3 h) | **about $3-6, hard stop at $10** |
| Anthropic (optional, only if you want a Claude-based DupLLM baseline) | Claude Haiku, ~30k PRs x ~1.5k input / 150 output tokens | about $15-70 depending on model; **I propose NOT doing this**, or capping at $20 with a subset |
| OpenAI | - | $0 (not used) |

I will post an exact estimate again and wait for your OK before any GPU or Anthropic run.

**Timeline (to 18 Dec):** week 1 labels + baselines; week 2 AgentDup + live-queue scoring; week 3 ablations + error analysis; week 4 writing (abstract due 11 Dec).

---

## 6. Venues (all checked on the official call pages, 9 Nov 2026)

| Venue | Deadline (AoE) | Length / format | Proceedings | Fit |
|---|---|---|---|---|
| **ICPC 2027 RENE** (Replications and Negative Results) - **primary** | Abstract 11 Dec 2026; paper **18 Dec 2026**; notification 14 Jan 2027; camera-ready 29 Jan 2027 | New replication / negative-result papers: up to **10 + 2 pages** (refs). Author-side negative results: 4 + 1. IEEE `IEEEtran` conference template. | Electronic proceedings in the ACM / IEEE Digital Libraries (per call page). | Good. The call requires a replication to use **new data** and go beyond a rerun, which our new metric + detector does. Scout notes confirmed. |
| ICPC 2027 ERA (Early Research Achievements) - stretch alternative | Optional abstract 19 Nov 2026; paper **26 Nov 2026** | 4 + 1 pages, IEEE `IEEEtran`, double-anonymous | ICPC proceedings (ACM / IEEE) | Good for "new idea + early results", but only 17 days. |
| ICSE 2027 AGENT workshop | 20 Nov 2026 | Short papers up to 5 pages, IEEE | Published by IEEE (per page) | Topic fits best, but 11 days is too tight for real results. |
| **EASE 2027 Short Papers and Emerging Results** - fallback | Abstract 22 Feb 2027; paper **1 Mar 2027** | **6 pages total incl. references**, ACM template | ACM ICPS, open access; an ACM article fee may apply depending on author's institution | Good fallback. Scout "Mar 1" confirmed. |
| EASE 2027 RENE - second fallback | Abstract 22 Feb 2027; paper 1 Mar 2027 | 10 + 2 pages, ACM | ACM ICPS | Same fit as ICPC RENE. |

Checked and not chosen: MSR 2027 technical (deadline passed, 23 Oct), FORGE 2027 (passed, 30 Oct), MSR 2027 Data & Tool Showcase (10 Nov - tomorrow), NLBSE 2027 and LLM4Code 2027 (13 Nov, too soon; LLM4Code publisher/page limit not shown on the page), AGENTVERIFY 2027 (13 Nov; publisher not confirmed), RAISE 2027 (20 Nov). MSR Mining Challenge excluded (competition).
Note: the same paper cannot be under review at two venues at once; pick one at a time.

---

## 7. Verdict

**PIVOT -> GO** with the live-queue metric + AgentDup framing, target ICPC 2027 RENE (18 Dec 2026), fallback EASE 2027 (1 Mar 2027).

**Acceptance confidence: medium (about 40-50%).**
- For: clear gap (no detector work on agent PRs), large public labelled data, strong motivation numbers (23.7% of failed agent PRs), a real tool, a metric argument that RENE reviewers like, cheap compute.
- Against: the method parts are individually known (diff overlap, issue links, embeddings); the novelty rests on template stripping + the live-queue metric, and on the results being clear. Silver labels will draw reviewer questions.

**Top 3 risks**
1. **Label noise and "easy" duplicates.** About half the silver pairs are self-supersede, which any detector finds. If the hard cross-author subset is too small or too noisy after the spot-check, the gains may not be significant. Mitigation: report per relation type; use the 48 timeline marks and the Ehsani labels as clean checks.
2. **No clear win.** Classic INTRUDE features (files + locations) may already work well on agent PRs, so AgentDup's gain may be small. Then the paper becomes mainly the metric + negative result. Still fits RENE, but weaker.
3. **Being scooped / access.** The AIDev area is very active; someone may publish agent duplicate detection before December. Also, several baselines (Li 2017, DupHunter, DupLLM) are paywalled and have no public code, so we re-implement from descriptions, and the GitHub token is currently broken for fetching non-AIDev PRs.

**What I need from you to start Phase 2:**
1. OK to start the CPU-only work (cost $0).
2. Yes/no on the small GPU run for the DupLLM-style baseline (about $3-6, stop at $10). I suggest no Anthropic spend.
3. A working GitHub token (the stored `GH_TOKEN_HARSHUL` gives 401), or OK to rely only on AIDev's own diff table.

I have stopped here and will not run any experiment until you say go.
