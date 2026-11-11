"""Build markdown tables + an HTML page with charts from experiments/results/*.csv."""
import json
import os

import pandas as pd

R = os.path.join(os.path.dirname(__file__), "..", "results") + "/"; O = os.path.dirname(__file__) + "/"
S = pd.read_csv(R + "strategies_by_group.csv"); PC = pd.read_csv(R + "paired_cross_author.csv")
FA = pd.read_csv(R + "false_alarms.csv"); OC = pd.read_csv(R + "operating_curve.csv"); RP = pd.read_csv(R + "random_pair_vs_live_queue.csv")
CC = pd.read_csv(R + "class_counts.csv"); SM = json.load(open(R + "summary.json"))
def ci(r, m): return f"{r[m]:.3f} [{r[m+' lo']:.2f}, {r[m+' hi']:.2f}]"
def group_table(g, top=None):
    d = S[S.group == g].sort_values(["R@1", "MRR"], ascending=False)
    if top: d = d.head(top)
    n = int(d.n.iloc[0]) if len(d) else 0
    rows = [f"| {r.family} | {r.method} | {ci(r,'R@1')} | {ci(r,'R@5')} | {ci(r,'MRR')} |" for _, r in d.iterrows()]
    return f"**{g}** (n = {n})\n\n| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
REP = ["All signals, LR", "Doppel + MiniLM, LR (current tool)", "Doppel lexical, LR", "INTRUDE + time (Wang et al. 2019), LR",
       "contrib-guard/phoenix (bot, exact port)", "TF-IDF raw text (Li et al. 2017)", "BM25 raw text", "BGE-small template-stripped",
       "Jina code embeddings v2 on diff", "Code overlap sum (files+hunks+lines)", "Links only (same issue / #ref)"]
def best_of_family(g):
    d = S[S.group == g]; return d.sort_values("R@1", ascending=False).groupby("family").head(1).sort_values("family")
out = []
for g in ["cross-author", "all labelled", "self-replacement", "cross-author, same agent", "cross-author, cross-agent", "cross-author, no #ref in text"]:
    out.append(group_table(g))
# class matrix: best strategy of each family per class (R@1)
groups = [g for g in S.group.unique() if g.startswith("class ") or g.startswith("cross-author, class ") or g.startswith("same ") or g.startswith("cross-author, same code")]
fams = sorted(S.family.unique())
mat = ["| Duplicate class | n | " + " | ".join(f.split(" ", 1)[1] for f in fams) + " | best overall |", "|---|---|" + "---|" * (len(fams) + 1)]
for g in groups:
    d = S[S.group == g]; cells = []
    for f in fams:
        x = d[d.family == f].sort_values("R@1", ascending=False)
        cells.append(f"{x['R@1'].iloc[0]:.2f}" if len(x) else "–")
    b = d.sort_values("R@1", ascending=False).iloc[0]
    mat.append(f"| {g} | {int(d.n.iloc[0])} | " + " | ".join(cells) + f" | {b.method} ({b['R@1']:.2f}) |")
out.append("**Best Recall@1 of each strategy family, per duplicate class**\n\n" + "\n".join(mat) + "\n")
# paired
for ref in PC.reference.unique():
    d = PC[PC.reference == ref].sort_values("dR@1", ascending=False)
    rows = [f"| {r.method} | {r['dR@1']*100:+.1f} [{r['dR@1 lo']*100:+.1f}, {r['dR@1 hi']*100:+.1f}] | {r['dR@5']*100:+.1f} [{r['dR@5 lo']*100:+.1f}, {r['dR@5 hi']*100:+.1f}] | {r['dMRR']*100:+.1f} [{r['dMRR lo']*100:+.1f}, {r['dMRR hi']*100:+.1f}] |" for _, r in d.iterrows()]
    out.append(f"**Paired difference vs `{ref}`, cross-author (points; CI excludes 0 = significant)**\n\n| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
d = FA.sort_values("FAR"); out.append("**False-alarm rate on 2,965 PRs with no duplicate** (threshold = median top-1 score of training-fold cross-author duplicates)\n\n| Family | Strategy | False-alarm rate | Cross-author correct alerts |\n|---|---|---|---|\n" +
    "\n".join(f"| {r.family} | {r.method} | {r.FAR*100:.1f}% | {r['cross-author correct alerts']*100:.1f}% |" for _, r in d.iterrows()) + "\n")
oc = OC.pivot(index="method", columns="FAR target", values=OC.columns[-1]).sort_values(0.05, ascending=False)
out.append("**Operating curve: share of cross-author duplicates caught (correct top-1 above threshold) at a fixed false-alarm rate**\n\n| Strategy | " + " | ".join(f"FAR {int(c*100)}%" for c in oc.columns) + " |\n|---|" + "---|" * len(oc.columns) + "\n" +
    "\n".join(f"| {m} | " + " | ".join(f"{v*100:.1f}%" for v in r) + " |" for m, r in oc.iterrows()) + "\n")
rp = RP.sort_values("random-pair AUC", ascending=False)
rp["rank AUC"] = rp["random-pair AUC"].rank(ascending=False).astype(int); rp["rank live"] = rp["live-queue R@1 (cross-author)"].rank(ascending=False, method="min").astype(int)
out.append(f"**Random-pair (classic) vs live-queue evaluation** (Kendall tau = {SM['kendall_tau random-pair AUC vs live-queue cross-author R@1'][0]:.2f})\n\n| Strategy | Random-pair AUC | rank | Live-queue cross-author R@1 | rank |\n|---|---|---|---|---|\n" +
    "\n".join(f"| {r.method} | {r['random-pair AUC']:.3f} | {r['rank AUC']} | {r['live-queue R@1 (cross-author)']:.3f} | {r['rank live']} |" for _, r in rp.iterrows()) + "\n")
lat = SM["latency"]
out.append("**Latency and cost**\n\n| Component | Numbers |\n|---|---|\n" + "\n".join(f"| {k} | {json.dumps(v)} |" for k, v in lat.items()) + "\n")
open(O + "tables.md", "w").write("\n\n".join(out)); print("tables.md", len(out))
# HTML with charts
x = S[S.group == "cross-author"].sort_values("R@1", ascending=True)
data = {"methods": x.method.tolist(), "fam": x.family.tolist(), "r1": x["R@1"].round(4).tolist(), "r1lo": x["R@1 lo"].round(4).tolist(), "r1hi": x["R@1 hi"].round(4).tolist(),
        "r5": x["R@5"].round(4).tolist(), "fa_m": d.method.tolist(), "fa": (d.FAR * 100).round(2).tolist(),
        "oc": {m: [float(v) for v in r] for m, r in oc.head(12).iterrows()}, "oc_x": [float(c) for c in oc.columns],
        "groups": {g: S[S.group == g].set_index("method")["R@1"].round(4).to_dict() for g in S.group.unique()}}
json.dump(data, open(O + "data.json", "w"))
print("data.json ok")
