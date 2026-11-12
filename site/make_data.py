"""Write site/data.js from experiments/results/ so every number on the website comes from the result files."""
import json
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
R = ROOT / "experiments" / "results"
S = pd.read_csv(R / "strategies_by_group.csv")
X = S[S.group == "cross-author"].set_index("method")
FA = pd.read_csv(R / "false_alarms.csv").set_index("method")
OC = pd.read_csv(R / "operating_curve.csv")
COST = json.loads((R / "duplicate_cost_summary.json").read_text())["cross-author"]
LAT = json.loads((R / "package_latency.json").read_text())
NUM = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", (ROOT / "paper" / "generated" / "numbers_extra.tex").read_text()))

METHODS = [
    ("Jinx lexical, LR", "Jinx", "This tool (GitHub Action default)", True),
    ("Jinx + MiniLM, LR (current tool)", "Jinx + MiniLM", "This tool with its optional local text model", True),
    ("Links only (same issue / #ref)", "Link rule", "Same issue or #mention; text similarity breaks ties", False),
    ("INTRUDE + time (Wang et al. 2019), LR", "INTRUDE + time", "Classic research detector (Wang et al. 2019)", False),
    ("contrib-guard/phoenix (bot, exact port)", "contrib-guard", "Best existing open-source duplicate-PR bot we tested", False),
    ("Simili-bot (bot, re-impl)", "Simili-bot", "Existing duplicate-PR bot (re-implemented)", False),
    ("PRSense (bot, re-impl)", "PRSense", "Existing duplicate-PR bot (re-implemented)", False),
    ("TF-IDF raw text (Li et al. 2017)", "Text similarity", "Title and description word overlap (TF-IDF)", False),
]
col = "cross-author detected (top-1 correct, above thr)"
rows = []
for key, name, desc, ours in METHODS:
    oc = OC[OC.method == key].sort_values("FAR target")
    rows.append({
        "name": name, "desc": desc, "ours": ours,
        "top1": round(float(X.loc[key, "R@1"]) * 100, 1),
        "top1_lo": round(float(X.loc[key, "R@1 lo"]) * 100, 1),
        "top1_hi": round(float(X.loc[key, "R@1 hi"]) * 100, 1),
        "far": round(float(FA.loc[key, "FAR"]) * 100, 1),
        "far_lo": round(float(FA.loc[key, "FAR lo"]) * 100, 1),
        "far_hi": round(float(FA.loc[key, "FAR hi"]) * 100, 1),
        "curve": {f"{t:g}": round(float(v) * 100) for t, v in zip(oc["FAR target"], oc[col])},
    })
out = {
    "n_cross": int(X.n.iloc[0]),
    "methods": rows,
    "cost": {
        "after_1h": round(COST["share caught after >1h"] * 100),
        "after_1d": round(COST["share after >24h"] * 100),
        "after_7d": round(COST["share after >7d"] * 100),
        "reviewed_before": round(COST["share with >=1 human comment or review before flag"] * 100),
    },
    "latency_ms": LAT["lexical"]["median_ms"],
    "haiku": {"far": float(NUM["FARsubhaiku"]), "jinx_far_same_sample": float(NUM["FARsubjinx"]), "cents_per_pr": float(NUM["costHaikuPerPR"])},
}
(ROOT / "site" / "data.js").write_text("window.JINX = " + json.dumps(out, indent=1) + ";\n")
print("site/data.js:", len(rows), "methods")
