"""Figures for both papers, drawn from experiments/results (vector PDF, colour-blind-safe palette)."""
import json
import os
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(H, "..", "..", "experiments", "results")
OUT = os.path.join(H, "..", "generated")
S = pd.read_csv(os.path.join(RES, "strategies_by_group.csv"))
P = pd.read_csv(os.path.join(RES, "paired_cross_author.csv"))
LAT = json.loads(pathlib.Path(RES, "summary.json").read_text())["latency"]
CA = "cross-author"
JINX, INTR = "Jinx + MiniLM, LR (current tool)", "INTRUDE + time (Wang et al. 2019), LR"
CG = "contrib-guard/phoenix (bot, exact port)"
HAIKU = "LLM judge Qwen2.5-14B + Jinx (avg) top-5"  # LLM judge shown in figures (Haiku scores cover too few open-only candidates)
OK = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "red": "#D55E00", "purple": "#CC79A7",
      "sky": "#56B4E9", "yellow": "#F0E442", "grey": "#7F7F7F", "black": "#000000"}
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7,
                     "ytick.labelsize": 7, "font.family": "serif", "pdf.fonttype": 42, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
W = 3.45
MC = {"Jinx": OK["blue"], "Qwen-14B + Jinx": OK["purple"], "Link rule": OK["green"], "INTRUDE + time": OK["orange"],
      "contrib-guard": OK["red"]}
mcol = lambda lab: MC.get(lab, OK["grey"])


def r1(group, meth, col="R@1"):
    r = S[(S.group == group) & (S.method == meth)]
    return float(r[col].iloc[0]) if len(r) else np.nan


def save(fig, name):
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)


LINKS, TFIDF, ALL = "Links only (same issue / #ref)", "TF-IDF raw text (Li et al. 2017)", "All signals, LR"
EXP = os.path.join(H, "..", "..", "experiments")
SG = pd.read_csv(os.path.join(EXP, "results_grace7", "strategies_by_group.csv"))
FA = pd.read_csv(os.path.join(RES, "false_alarms.csv"))

# 1. Queue construction: Recall@1 on the original queues (open + closed in the last 7 days) vs real-use queues (open only)
QM = [(JINX, "Jinx"), (ALL, "All-signals LR"), (HAIKU, "Qwen-14B + Jinx"), (INTR, "INTRUDE + time"), (CG, "contrib-guard"),
      (LINKS, "Link rule"), (TFIDF, "TF-IDF")]
fig, ax = plt.subplots(figsize=(W, 2.15))
for y, (m, lab) in enumerate(QM):
    gr = SG[(SG.group == CA) & (SG.method == m)].iloc[0]
    g = gr["R@1"]
    ax.plot([gr["R@1 lo"], gr["R@1 hi"]], [y + 0.18, y + 0.18], color=OK["orange"], lw=1.0, alpha=0.8, zorder=2)
    r = S[(S.group == CA) & (S.method == m)].iloc[0]
    col = OK["blue"] if m == JINX else OK["black"]
    ax.plot([g, r["R@1"]], [y, y], color=OK["grey"], lw=1, alpha=0.6, zorder=1)
    ax.plot([r["R@1 lo"], r["R@1 hi"]], [y, y], color=OK["sky"], lw=3.2, alpha=0.55, solid_capstyle="round", zorder=2)
    ax.scatter(g, y, s=26, facecolor="white", edgecolor=OK["orange"], lw=1.4, zorder=3)
    ax.scatter(r["R@1"], y, s=30, color=OK["blue"], edgecolor="black" if m == JINX else "none", zorder=4)
    ax.annotate(f"{g:.2f}", (min(g, r["R@1 lo"]), y), xytext=(-5, 0), textcoords="offset points", ha="right", va="center", fontsize=6.3, color=OK["orange"])
    ax.annotate(f"{r['R@1']:.2f}", (r["R@1 hi"], y), xytext=(3, 0), textcoords="offset points", ha="left", va="center", fontsize=6.3, color=OK["blue"])
ax.set_yticks(range(len(QM)), [lab for _, lab in QM])
for t in ax.get_yticklabels():
    if t.get_text() == "Jinx":
        t.set_fontweight("bold")
ax.invert_yaxis()
ax.set_xlim(0.68, 1.0)
ax.set_xlabel("cross-author Recall@1")
ax.grid(axis="x", alpha=0.3, lw=0.4)
ax.scatter([], [], s=26, facecolor="white", edgecolor=OK["orange"], lw=1.4, label="7-day queue (also PRs closed in last 7 days), 95% CI")
ax.scatter([], [], s=30, color=OK["blue"], label="open-only queue (what a deployed tool sees), 95% CI")
ax.legend(frameon=False, fontsize=6.3, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1, handletextpad=0.3)
save(fig, "fig_queues.pdf")

# 1b. False alarms with 95% CIs (real-use queues)
FM = [(HAIKU, "Qwen-14B + Jinx"), (LINKS, "Link rule"), (ALL, "All-signals LR"), (JINX, "Jinx"), ("Jinx lexical, LR", "Jinx without MiniLM"),
      (INTR, "INTRUDE + time"), (TFIDF, "TF-IDF"), (CG, "contrib-guard")]
fig, ax = plt.subplots(figsize=(W, 1.9))
for y, (m, lab) in enumerate(FM):
    r = FA[FA.method == m].iloc[0]
    c = mcol(lab)
    ax.barh(y, 100 * r.FAR, color=c, alpha=0.85, height=0.62)
    ax.plot([100 * r["FAR lo"], 100 * r["FAR hi"]], [y, y], color="black", lw=0.9)
    ax.annotate(f"{100 * r.FAR:.1f}%", (100 * r["FAR hi"], y), xytext=(3, 0), textcoords="offset points", va="center", fontsize=6.3)
ax.set_yticks(range(len(FM)), [lab for _, lab in FM])
for t in ax.get_yticklabels():
    if t.get_text() == "Jinx":
        t.set_fontweight("bold")
ax.invert_yaxis()
ax.set_xlim(0, 8.5)
ax.set_xlabel("false alarms (% of PRs with no duplicate)")
ax.grid(axis="x", alpha=0.3, lw=0.4)
save(fig, "fig_far.pdf")

# 2. Heatmap: Recall@1 per duplicate kind and method
G = [("cross-author, class A. code twin (>=50% identical changed lines)", "A: code twin"),
     ("cross-author, class B. partial code overlap", "B: partial overlap"),
     ("cross-author, class C. same files, different code", "C: same files, diff. code"),
     ("cross-author, class D. no shared files (intent-level)", "D: no shared files"),
     ("cross-author, no link at all (no #ref, no shared issue)", "no link at all"),
     ("cross-author, cross-agent", "different agents"),
     ("self-replacement", "self-replacement")]
MM = [(JINX, "Jinx"), ("All signals, LR", "All-signals LR"), (HAIKU, "Qwen-14B + Jinx"), (INTR, "INTRUDE + time"),
      (CG, "contrib-guard"), ("Links only (same issue / #ref)", "Link rule*"), ("BGE-small template-stripped", "BGE embedding"),
      ("TF-IDF raw text (Li et al. 2017)", "TF-IDF")]
A = np.array([[r1(g, m) for m, _ in MM] for g, _ in G])
fig = plt.figure(figsize=(W, 2.9))
ax = fig.add_axes([0.33, 0.25, 0.56, 0.73])
im = ax.imshow(A, cmap="YlGnBu", vmin=0.3, vmax=1.0, aspect="auto")
ns = [int(S[S.group == g].n.iloc[0]) for g, _ in G]
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if np.isnan(A[i, j]):
            ax.text(j, i, "n/a", ha="center", va="center", fontsize=6, color=OK["grey"])
            continue
        ax.text(j, i, f"{A[i, j]:.2f}".lstrip("0") if A[i, j] < 1 else "1.0", ha="center", va="center", fontsize=6.5,
                color="white" if A[i, j] > 0.75 else "black",
                fontweight="bold" if ns[i] >= 30 and round(A[i, j], 3) == round(np.nanmax(A[i]), 3) else "normal")
ax.set_yticks(range(len(G)), [f"{lab} (n={n}{', small' if n < 30 else ''})" for (_, lab), n in zip(G, ns)], fontsize=7)
ax.set_xticks(range(len(MM)), [m[1] for m in MM], fontsize=7, rotation=40, ha="right", rotation_mode="anchor")
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, len(G), fill=False, ec=OK["red"], lw=1.6))
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, cax=fig.add_axes([0.91, 0.25, 0.025, 0.73]))
cb.set_label("Recall@1")
fig.savefig(os.path.join(OUT, "fig_heatmap.pdf"), bbox_inches=None)
plt.close(fig)

# 3. Accuracy vs. cost: per-PR latency (log) vs. cross-author Recall@1
PL = json.loads(pathlib.Path(RES, "package_latency.json").read_text())
lex, mini = PL["lexical"]["median_ms"], PL["minilm"]["median_ms"]
pts = [("Jinx without MiniLM", "Jinx lexical, LR", lex, "CPU"), ("Jinx (with MiniLM)", JINX, mini, "CPU"),
       ("+ MiniLM cross-enc. (top-10)", "Cross-encoder ms-marco MiniLM + Jinx (avg) top-10", mini + LAT["cpu_rerankers"]["cross-encoder/ms-marco-MiniLM-L6-v2"]["ms_per_query_top10"], "CPU"),
       ("+ BGE reranker (top-10)", "Cross-encoder BGE-reranker-base + Jinx (avg) top-10", mini + 10 * LAT["gpu_ce_bgebase"]["ms_per_pair_gpu"], "GPU"),
       ("+ Qwen 7B (top-5)", "LLM judge Qwen2.5-7B + Jinx (avg) top-5", mini + 5 * LAT["gpu_qwen7"]["ms_per_pair_gpu_batched"], "GPU"),
       ("+ Qwen 14B (top-5)", "LLM judge Qwen2.5-14B + Jinx (avg) top-5", mini + 5 * LAT["gpu_qwen14"]["ms_per_pair_gpu_batched"], "GPU")]
sty = {"CPU": (OK["blue"], "o"), "GPU": (OK["orange"], "s")}
fig, ax = plt.subplots(figsize=(W, 2.0))
ys = []
for k, (lab, m, ms, hw) in enumerate(pts):
    c, mk = sty[hw]
    y = r1(CA, m)
    ys.append(y)
    big = lab.startswith("Jinx")
    rr = S[(S.group == CA) & (S.method == m)].iloc[0]
    ax.plot([ms, ms], [rr["R@1 lo"], rr["R@1 hi"]], color=c, lw=0.8, alpha=0.5, zorder=2)
    ax.scatter(ms, y, color=c, marker=mk, s=38 if big else 22, zorder=3, edgecolor="black" if big else "none")
    pts[k] = (lab, m, ms, hw, y, big)
order = sorted(range(len(pts)), key=lambda k: pts[k][4])
lo_y, hi_y = 0.875, 0.965
for rank, k in enumerate(order):
    lab, m, ms, hw, y, big = pts[k]
    ty = lo_y + (hi_y - lo_y) * rank / (len(order) - 1)
    ax.annotate(lab, (ms, y), xytext=(2.5e4, ty), ha="left", va="center", fontsize=6, fontweight="bold" if big else "normal",
                arrowprops={"arrowstyle": "-", "color": OK["grey"], "lw": 0.5, "shrinkA": 0, "shrinkB": 3})
for m, lab, ls, va, dy in [(INTR, "INTRUDE + time", ":", "top", -0.001), (LINKS, "link rule", "--", "bottom", 0.001)]:
    ax.axhline(r1(CA, m), color=mcol("INTRUDE + time" if m == INTR else "Link rule"), ls=ls, lw=0.9)
    ax.text(3, r1(CA, m) + dy, lab, fontsize=6, color=OK["grey"], va=va)
ax.set_xscale("log")
ax.set_xlim(2.5, 1.2e6)
ax.set_xlabel("time per new PR in ms (log scale)")
ax.set_ylim(0.85, 0.98)
ax.set_xticks([10, 100, 1000, 10000])
ax.set_ylabel("cross-author Recall@1")
ax.grid(alpha=0.3, which="major", lw=0.4)
for hw, (c, mk) in sty.items():
    ax.scatter([], [], color=c, marker=mk, s=22, label=hw)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), frameon=False, ncol=3, title=None, fontsize=6.3)
save(fig, "fig_pareto.pdf")

# 4. Operating curves at fixed false-alarm budgets
oc = pd.read_csv(os.path.join(RES, "operating_curve.csv"))
fig, ax = plt.subplots(figsize=(W, 2.0))
lines = [(JINX, "Jinx", OK["blue"], "o", 2.2), ("All signals, LR", "All-signals LR", OK["grey"], "^", 1.0),
         (HAIKU, "Qwen-14B + Jinx", OK["purple"], "D", 1.2), (INTR, "INTRUDE + time", OK["orange"], "s", 1.4), (CG, "contrib-guard", OK["red"], "v", 1.4),
         (LINKS, "Link rule", OK["green"], "x", 1.2)]
for m, lab, c, mk, lw in lines:
    d = oc[oc.method == m].sort_values("FAR target")
    if len(d):
        ax.plot(100 * d["FAR target"], d.iloc[:, 2], color=c, marker=mk, ms=3.5, lw=lw, label=lab)
ax.set_xscale("log")
ax.set_xticks([1, 2, 5, 10, 20], ["1%", "2%", "5%", "10%", "20%"])
ax.set_xlabel("allowed false-alarm rate")
ax.set_ylabel("cross-author duplicates\ncaught at rank 1")
ax.set_ylim(0, 0.9)
ax.grid(alpha=0.3, lw=0.4)
RP = pd.read_csv(os.path.join(RES, "replay_impact.csv"))
jr = RP[(RP.method == JINX) & (RP.group == "cross-author")]
if len(jr):
    jr = jr.iloc[0]
    ax.scatter(jr["false alarms per 100 PRs without duplicate"], jr["correct warning at open"], marker="*", s=70, color=OK["blue"],
               edgecolor="black", lw=0.5, zorder=5, label="Jinx shipped threshold")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=6.3, ncol=4, columnspacing=0.8, handletextpad=0.3)
save(fig, "fig_operating.pdf")

# 5. Random-pair AUC vs. live-queue Recall@1, coloured by strategy family
rl = pd.read_csv(os.path.join(RES, "random_pair_vs_live_queue.csv"))


def fam(m):
    for key, f in [("LLM judge", "LLM judge"), ("Cascade", "cascade / re-ranker"), ("Cross-encoder", "cascade / re-ranker"),
                   ("contrib-guard", "existing bot"), ("Simili", "existing bot"), ("PRSense", "existing bot"), ("PRism", "existing bot"),
                   ("vector-triage", "existing bot"), ("doppel", "existing bot"), (", LR", "learned (LR / GBDT)"), ("boosting", "learned (LR / GBDT)"),
                   ("MiniLM", "embedding"), ("BGE", "embedding"), ("UniXcoder", "embedding"), ("CodeBERT", "embedding"), ("Jina", "embedding")]:
        if key in m:
            return f
    return "simple rule"


rl["fam"] = rl.method.map(fam)
FC = {"simple rule": OK["grey"], "embedding": OK["sky"], "existing bot": OK["red"], "learned (LR / GBDT)": OK["blue"],
      "cascade / re-ranker": OK["green"], "LLM judge": OK["purple"]}
fig, ax = plt.subplots(figsize=(W, 2.25))
for f, c in FC.items():
    d = rl[rl.fam == f]
    ax.scatter(d["random-pair AUC"], d["live-queue R@1 (cross-author)"], s=12, color=c, label=f, alpha=0.85, edgecolor="none")
comb = rl[rl.method.str.contains("LR|Cascade|avg|boosting", regex=True)]
hi = comb[comb["random-pair AUC"] > 0.98]
ax.axvspan(0.98, 1.0, color=OK["yellow"], alpha=0.25, lw=0)
pathlib.Path(OUT, "randlive_band.tex").write_text(
    f"\\newcommand{{\\bandN}}{{{len(hi)}}}\\newcommand{{\\bandLo}}{{{hi.iloc[:, 2].min():.2f}}}\\newcommand{{\\bandHi}}{{{hi.iloc[:, 2].max():.2f}}}\n")
for m, lab, dx, dy in [(JINX, "Jinx", -22, 4), (INTR, "INTRUDE + time", -70, -22), ("Recency only (newest open PR first)", "recency", 4, 0)]:
    r = rl[rl.method == m].iloc[0]
    ax.annotate(lab, (r["random-pair AUC"], r["live-queue R@1 (cross-author)"]), xytext=(dx, dy), textcoords="offset points",
                fontsize=6.5, arrowprops={"arrowstyle": "-", "lw": 0.5})
ax.set_xlabel("AUC on random PR pairs (the usual evaluation)")
ax.set_ylabel("open-only queue Recall@1\n(cross-author)")
ax.grid(alpha=0.3, lw=0.4)
ax.legend(frameon=False, fontsize=6.3, loc="upper center", bbox_to_anchor=(0.45, -0.25), ncol=3, handletextpad=0.2, columnspacing=0.6)
save(fig, "fig_randlive.pdf")
print("figures written")
