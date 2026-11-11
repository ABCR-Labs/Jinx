"""Extra number macros and figures for the papers (from experiments/results and experiments/label_audit)."""
import json
import os
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(H, "..", "..", "experiments")
RES = os.path.join(EXP, "results")
OUT = os.path.join(H, "..", "generated")
S = pd.read_csv(os.path.join(RES, "strategies_by_group.csv"))
SUM = json.loads(pathlib.Path(os.path.join(RES, "summary.json")).read_text())
CA = "cross-author"
JINX, INTR = "Jinx + MiniLM, LR (current tool)", "INTRUDE + time (Wang et al. 2019), LR"
mac = []


def nm(k, v):
    mac.append(f"\\newcommand{{\\{k}}}{{{v}}}")


def r1(group, method, col="R@1"):
    r = S[(S.group == group) & (S.method == method)]
    assert len(r) == 1, (group, method)
    return f"{float(r[col].iloc[0]):.3f}"


def find(sub):
    m = [x for x in S.method.unique() if sub in x]
    assert len(m) == 1, (sub, m)
    return m[0]


nm("kendallTau", f"{SUM['kendall_tau random-pair AUC vs live-queue cross-author R@1'][0]:.2f}")
nm("latJinx", f"{SUM['latency']['lexical features ms/query']['median']:.0f}")
nm("latJinxPninety", f"{SUM['latency']['lexical features ms/query']['p90']:.0f}")
for k, sub in [("ROneqwenSevenAvg", "LLM judge Qwen2.5-7B + Jinx (avg) top-5"), ("ROneqwenFourteenAvg", "LLM judge Qwen2.5-14B + Jinx (avg) top-5"),
               ("ROnehaikuOnly", "LLM judge Claude Haiku 4.5 re-rank top-5"), ("ROnecascade", "Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR)"),
               ("ROneminilm", "MiniLM template-stripped"), ("ROnebgeSmall", "BGE-small template-stripped"), ("ROnebgeDiff", "BGE-small on diff"),
               ("ROnetfidfStripped", "TF-IDF template-stripped"), ("ROnetfidfRaw", "TF-IDF raw text (Li et al. 2017)"),
               ("ROnecodesum", "Code overlap sum (files+hunks+lines)"), ("ROnejinxLex", "Jinx lexical, LR")]:
    nm(k, r1(CA, find(sub)))
for tag, g in [("ClassD", "cross-author, class D. no shared files (intent-level)"), ("ClassC", "cross-author, class C. same files, different code"),
               ("NoLink", "cross-author, no link at all (no #ref, no shared issue)"), ("SameCode", "cross-author, same code, different description"),
               ("CrossAgent", "cross-author, cross-agent")]:
    nm("ROnejinx" + tag, r1(g, JINX)); nm("ROneintrude" + tag, r1(g, INTR))
    if tag != "CrossAgent":
        nm("n" + tag, int(S[S.group == g].n.iloc[0]))
g_sc = "same code, different description (code twin, text TF-IDF < 0.3)"
nm("ROnejinxSameCodeAll", r1(g_sc, JINX)); nm("ROneintrudeSameCodeAll", r1(g_sc, INTR)); nm("nSameCodeAll", int(S[S.group == g_sc].n.iloc[0]))
nm("ROnehaikuClassD", r1("cross-author, class D. no shared files (intent-level)", find("LLM judge Claude Haiku 4.5 + Jinx (avg) top-5")))
for tag, f in [("Rand", "audit_random200_summary.json"), ("Cross", "audit_cross_summary.json")]:
    a = json.loads(pathlib.Path(os.path.join(EXP, "label_audit", f)).read_text())
    s, lo = a["precision_strict (duplicate+replacement) [mean, lo, hi]"], a["precision_loose (+subsumed) [mean, lo, hi]"]
    nm("audit" + tag + "Strict", f"{100 * s[0]:.1f}"); nm("audit" + tag + "StrictLo", f"{100 * s[1]:.1f}"); nm("audit" + tag + "StrictHi", f"{100 * s[2]:.1f}")
    nm("audit" + tag + "Loose", f"{100 * lo[0]:.1f}"); nm("audit" + tag + "N", a["n"])
c = json.loads(pathlib.Path(os.path.join(EXP, "label_audit", "clean_subset_results.json")).read_text())["audit-valid (duplicate+replacement)"]
nm("cleanN", c["n"])
for m, t in [("R@1", "RO"), ("R@5", "RF")]:
    d = c[f"Jinx - INTRUDE {m} [d, lo, hi]"]
    nm(f"clean{t}", f"{100 * d[0]:+.1f}"); nm(f"clean{t}Lo", f"{100 * d[1]:+.1f}"); nm(f"clean{t}Hi", f"{100 * d[2]:+.1f}")
nm("costHaiku", "7.25")  # data/llm_haiku45_cost.json
nm("costAudit", "0.82")  # experiments/label_audit/audit_*_summary.json (cost_usd sum)
rl0 = pd.read_csv(os.path.join(RES, "random_pair_vs_live_queue.csv"))
comb = rl0[rl0.method.str.contains("LR|Cascade|avg|boosting", regex=True)]
hi = comb[comb["random-pair AUC"] > 0.98]
nm("nComb", len(comb)); nm("nCombHiAUC", len(hi))
nm("combHiMin", f"{hi.iloc[:, 2].min():.3f}"); nm("combHiMax", f"{hi.iloc[:, 2].max():.3f}")
ca = S[S.group.str.startswith("cross-author, class A") & S.method.str.contains("LR|avg")]
nm("classAMin", f"{ca['R@1'].min():.2f}")
pathlib.Path(OUT, "numbers_extra.tex").write_text("\n".join(mac) + "\n")

plt.rcParams.update({"font.size": 8, "figure.dpi": 200})
oc = pd.read_csv(os.path.join(RES, "operating_curve.csv"))
fig, ax = plt.subplots(figsize=(3.4, 2.2))
for meth, lab in [(JINX, "Jinx"), (find("All signals, LR"), "All signals, LR"), (INTR, "INTRUDE + time"),
                  (find("contrib-guard/phoenix"), "contrib-guard"), (find("LLM judge Claude Haiku 4.5 + Jinx (avg) top-5"), "Haiku + Jinx")]:
    d = oc[oc.method == meth]
    if len(d):
        ax.plot(100 * d["FAR target"], d.iloc[:, 2], marker="o", ms=2.5, label=lab)
ax.set_xlabel("false alarms on no-duplicate PRs (%)"); ax.set_ylabel("cross-author detected@1")
ax.grid(alpha=.3); ax.legend(fontsize=6, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_operating.pdf"))
rl = pd.read_csv(os.path.join(RES, "random_pair_vs_live_queue.csv"))
fig, ax = plt.subplots(figsize=(3.4, 2.2))
ax.scatter(rl["random-pair AUC"], rl["live-queue R@1 (cross-author)"], s=6, alpha=.7)
for meth, lab in [(JINX, "Jinx"), (INTR, "INTRUDE+t"), (find("Recency only"), "recency")]:
    r = rl[rl.method == meth].iloc[0]
    ax.annotate(lab, (r["random-pair AUC"], r["live-queue R@1 (cross-author)"]), fontsize=6, xytext=(3, -6), textcoords="offset points")
ax.set_xlabel("random-pair AUC"); ax.set_ylabel("live-queue Recall@1 (cross-author)"); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_randlive.pdf"))
print(len(mac), "macros; figures written")
