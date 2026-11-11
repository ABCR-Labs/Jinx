"""Export experiments/results/* into html/data.json for the HTML report."""
import json
import os

import pandas as pd

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "..", "..", "results") + "/"
S = pd.read_csv(R + "strategies_by_group.csv"); PC = pd.read_csv(R + "paired_cross_author.csv"); FA = pd.read_csv(R + "false_alarms.csv")
PF = pd.read_csv(R + "paired_false_alarms.csv"); OC = pd.read_csv(R + "operating_curve.csv"); RP = pd.read_csv(R + "random_pair_vs_live_queue.csv")
SM = json.load(open(R + "summary.json")); CC = pd.read_csv(R + "class_counts.csv", index_col=0); ER = pd.read_csv(R + "errors_cross_author.csv")
r4 = lambda x: None if pd.isna(x) else round(float(x), 4)
out = {"groups": [], "rows": [], "paired": [], "fa": [], "oc": [], "rp": [], "classes": [], "latency": SM["latency"],
       "tau": SM["kendall_tau random-pair AUC vs live-queue cross-author R@1"][0], "n_methods": SM["n_methods"], "errors": ER.fillna("").to_dict("records")}
for g, d in S.groupby("group", sort=False): out["groups"].append({"group": g, "n": int(d.n.iloc[0])})
for _, r in S.iterrows():
    out["rows"].append({"g": r.group, "f": r.family, "m": r.method, **{k.replace("@", "").replace(" ", "_"): r4(r[k]) for k in ["R@1", "R@1 lo", "R@1 hi", "R@5", "R@5 lo", "R@5 hi", "MRR", "MRR lo", "MRR hi"]}})
for _, r in PC.iterrows(): out["paired"].append({"ref": r.reference, "m": r.method, **{k.replace("@", "").replace(" ", "_"): r4(r[k]) for k in PC.columns[2:]}})
for _, r in FA.iterrows(): out["fa"].append({"f": r.family, "m": r.method, "far": r4(r.FAR), "lo": r4(r["FAR lo"]), "hi": r4(r["FAR hi"]), "hit": r4(r["cross-author correct alerts"])})
for _, r in OC.iterrows(): out["oc"].append({"m": r.method, "t": r4(r["FAR target"]), "v": r4(r[OC.columns[-1]])})
for _, r in RP.iterrows(): out["rp"].append({"m": r.method, "auc": r4(r["random-pair AUC"]), "live": r4(r["live-queue R@1 (cross-author)"])})
for i, r in CC.iterrows(): out["classes"].append({"cls": i, "cross": int(r["cross-author"]), "self": int(r["self-replacement"])})
cf = R + "costs/modal_billing.json"; out["modal_cost"] = json.load(open(cf)) if os.path.exists(cf) else None
json.dump(out, open(H + "/data.json", "w")); print("html/data.json", len(out["rows"]), "rows")
