"""Render benchmark CSV/JSON results as Markdown tables for the report."""
import json, sys, pandas as pd
R = "/home/ubuntu/research/prdupecheck/results/" + (sys.argv[1] if len(sys.argv) > 1 else "")
res = pd.read_csv(R + "ranking.csv"); fa = pd.read_csv(R + "false_alarms.csv"); s = json.load(open(R + "summary.json"))
def f(x): return f"{x:.3f}"
out = []
for g in res.group.unique():
    d = res[res.group == g]
    out.append(f"\n**{g}** (n = {int(d.n.iloc[0])})\n\n| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |\n|---|---|---|---|")
    for _, r in d.iterrows():
        out.append(f"| {r.method} | {f(r['R@1'])} [{f(r['R@1 lo'])}, {f(r['R@1 hi'])}] | {f(r['R@5'])} [{f(r['R@5 lo'])}, {f(r['R@5 hi'])}] | {f(r.MRR)} |")
out.append("\n**False alarms on 2,965 PRs with no duplicate**\n\n| Method | FAR, threshold set for 50% cross-author detection | correct top-1 alerts (cross-author) | FAR at tool default | correct alerts at default |\n|---|---|---|---|---|")
for _, r in fa.iterrows():
    g = lambda k: "-" if pd.isna(r.get(k)) else f(r[k])
    out.append(f"| {r.method} | {g('FAR@50%train-detection')} | {g('cross-author correct alerts')} | {g('FAR@tool default')} | {g('cross-author correct alerts@default')} |")
out.append("\n```json\n" + json.dumps(s, indent=1, default=float) + "\n```")
open(R + "tables.md", "w").write("\n".join(out)); print(R + "tables.md")
