"""Build live-queue benchmark from AIDev v5 (agent PRs only).
query = later PR of a silver pair; queue = PRs in the same repo opened before the query
and still open at that moment (or closed < 7 days before it)."""
import pandas as pd, numpy as np, re, pickle, collections
D = "/home/ubuntu/research/prdupecheck/data/"
GRACE = pd.Timedelta(days=7)
pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user", "state", "created_at", "closed_at", "merged_at", "repo_url"])
for c in ["created_at", "closed_at", "merged_at"]:
    pr[c] = pd.to_datetime(pr[c], utc=True)
key = {(r, n): i for i, r, n in zip(pr.id, pr.repo_url, pr.number)}
s = pd.read_csv(D + "silver_pairs_strict.csv")
s["other_id"] = [key.get((r, int(n))) for r, n in zip(s.repo, s.other)]
print("silver pairs", len(s), "other in AIDev", s.other_id.notna().sum())
s_out = s[s.other_id.isna()]
s = s[s.other_id.notna()].copy(); s["other_id"] = s.other_id.astype(int)
s = s[s.pr_id != s.other_id]
P = pr.set_index("id")
pairs = {}
for a, b, ph in zip(s.pr_id, s.other_id, s.phrase):
    q, g = (a, b) if P.at[a, "created_at"] > P.at[b, "created_at"] else (b, a)
    pairs[(q, g)] = ph
print("unique (query, gold) pairs", len(pairs))
byrepo = {r: g.sort_values("created_at") for r, g in pr.groupby("repo_url")}

def queue(q):
    r = P.at[q, "repo_url"]; t = P.at[q, "created_at"]; g = byrepo[r]
    m = (g.created_at < t) & (g.closed_at.isna() | (g.closed_at > t - GRACE)) & (g.id != q)
    return g.id[m].to_numpy()

dup_comment = re.compile(r"(duplicate|dupe|supersed|in favou?r of|replaced by|same as|overlap|already (addressed|fixed|implemented|done|covered|handled|merged)|covered (by|in)|consolidat|resolved (in|by))", re.I)
c = pd.read_parquet(D + "pr_comments.parquet", columns=["pr_id", "body"])
flagged = set(c.pr_id[c.body.fillna("").str.contains(dup_comment)])
flagged |= set(s_out.pr_id) | {q for q, _ in pairs} | {g for _, g in pairs}

queries, dropped = [], 0
golds = collections.defaultdict(set)
for (q, g) in pairs: golds[q].add(g)
for (q, g), ph in pairs.items():
    cand = queue(q)
    if g not in set(cand):
        dropped += 1; continue
    queries.append(dict(q=q, gold=g, others=golds[q] - {g}, cand=cand, phrase=ph,
                        self=P.at[q, "user"] == P.at[g, "user"],
                        same_agent=P.at[q, "agent"] == P.at[g, "agent"], neg=False))
print("pairs with gold in live queue", len(queries), "dropped (gold not in queue)", dropped)
rng = np.random.default_rng(0)
repos = sorted({P.at[x["q"], "repo_url"] for x in queries})
pool = pr[pr.repo_url.isin(repos) & pr.merged_at.notna() & ~pr.id.isin(flagged)]
negs = pool.sample(n=min(3000, len(pool)), random_state=0)
nq = 0
for q in negs.id:
    cand = queue(q)
    if len(cand) == 0: continue
    queries.append(dict(q=q, gold=None, others=set(), cand=cand, phrase=None, self=None, same_agent=None, neg=True)); nq += 1
print("negative queries (merged, no duplicate comment, non-empty queue)", nq)
need = set()
for x in queries: need.add(x["q"]); need.update(x["cand"].tolist())
print("PRs needed", len(need))
qs = [x for x in queries if not x["neg"]]
print("self", sum(x["self"] for x in qs), "cross-author", sum(not x["self"] for x in qs),
      "cross-author same agent", sum((not x["self"]) and x["same_agent"] for x in qs),
      "cross-agent", sum(not x["same_agent"] for x in qs))
ql = np.array([len(x["cand"]) for x in qs]); print("queue size median", np.median(ql), "p90", np.percentile(ql, 90), "max", ql.max())
print("agent-other pairs not scorable (target PR not in AIDev)", len(s_out), "of which cross-author", int((s_out.commenter != s_out.pr_author).sum()))
pickle.dump(dict(queries=queries, need=need, n_out=len(s_out)), open(D + "bench.pkl", "wb"))
