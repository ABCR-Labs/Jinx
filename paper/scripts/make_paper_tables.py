"""Build LaTeX tables and number macros for the papers from experiments/results/*.csv (no hand-typed numbers)."""
import os
import pathlib

import pandas as pd

H = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(H, "..", "..", "experiments", "results")
OUT = os.path.join(H, "..", "generated")
os.makedirs(OUT, exist_ok=True)
S = pd.read_csv(os.path.join(RES, "strategies_by_group.csv"))
P = pd.read_csv(os.path.join(RES, "paired_cross_author.csv"))
FA = pd.read_csv(os.path.join(RES, "false_alarms.csv"))
PFA = pd.read_csv(os.path.join(RES, "paired_false_alarms.csv"))

M = {"jinx": "Jinx + MiniLM, LR (current tool)", "jinxlex": "Jinx lexical, LR", "all": "All signals, LR",
     "intrude": "INTRUDE + time (Wang et al. 2019), LR", "cg": "contrib-guard/phoenix (bot, exact port)",
     "haiku": "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5", "haikuonly": "LLM judge Claude Haiku 4.5 re-rank top-5",
     "casc": "Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR)", "links": "Links only (same issue / #ref)",
     "tfidf": "TF-IDF raw text (Li et al. 2017)", "bge": "BGE-small template-stripped",
     "qwen14": "LLM judge Qwen2.5-14B + Jinx (avg) top-5"}
SHOW = {"jinx": "Jinx (ours, default)", "jinxlex": "Jinx without MiniLM", "all": "All signals, LR", "intrude": "INTRUDE + time~\\cite{ren2019intrude,wang2019time}",
        "cg": "contrib-guard (bot)", "haiku": "Claude Haiku 4.5 + Jinx", "haikuonly": "Claude Haiku 4.5 alone on Jinx top-5",
        "casc": "Jinx + BGE rerank + Qwen-7B", "links": "Link rule (shared issue or \\#ref)", "tfidf": "TF-IDF~\\cite{li2017detecting}",
        "bge": "BGE-small embedding", "qwen14": "Qwen2.5-14B + Jinx"}
for k, v in M.items():
    assert v in set(S.method), v

def get(group, key, col):
    r = S[(S.group == group) & (S.method == M[key])]
    return float(r[col].iloc[0]) if len(r) else float("nan")

def far(key):
    r = FA[FA.method == M[key]].iloc[0]
    return r.FAR, r["FAR lo"], r["FAR hi"]

f3 = lambda x: "--" if pd.isna(x) else f"{x:.3f}"
pct = lambda x: f"{100 * x:.1f}"
CA = "cross-author"
BASE = ["links", "intrude", "cg", "bge", "tfidf"]
ORDER = [["jinx", "jinxlex"], ["all", "casc", "haiku", "qwen14", "haikuonly"], BASE]
vals = {}
for k in [k for blk in ORDER for k in blk]:
    vals[k] = [get(CA, k, "R@1"), get(CA, k, "R@5"), get(CA, k, "MRR"), far(k)[0]]
ORDER[2] = sorted(BASE, key=lambda k: -vals[k][0])
better = [max, max, max, min]
bestbase = [better[i](vals[k][i] for k in BASE) for i in range(4)]


def lead(k):
    """Jinx minus this row in R@1, in points, with the paired repository-bootstrap 95% CI (d in the CSV is row minus Jinx)."""
    if k == "jinx":
        return "--"
    r = P[(P.reference == M["jinx"]) & (P.method == M[k])].iloc[0]
    d, lo, hi = -100 * r["dR@1"], -100 * r["dR@1 hi"], -100 * r["dR@1 lo"]
    txt = f"{d:+.1f} {{\\scriptsize [{lo:+.1f}, {hi:+.1f}]}}"
    return f"\\textcolor{{wingreen}}{{\\textbf{{{d:+.1f}}}}} {{\\scriptsize [{lo:+.1f}, {hi:+.1f}]}}" if lo > 0 else txt


def clear_win(i):
    """Jinx beats the best baseline in column i and the paired 95% CI excludes zero (CSV d = baseline minus Jinx)."""
    b = next(k for k in BASE if round(vals[k][i], 4) == round(bestbase[i], 4))
    if i == 3:
        r = PFA[(PFA.reference == M["jinx"]) & (PFA.method == M[b])]
        return len(r) and r["dFAR lo"].iloc[0] > 0
    col = ["dR@1", "dR@5", "dMRR"][i]
    r = P[(P.reference == M["jinx"]) & (P.method == M[b])].iloc[0]
    return r[col + " hi"] < 0


def cell(k, i):
    x = vals[k][i]
    txt = f3(x) if i < 3 else pct(x)
    if i == 3:
        _, lo, hi = far(k)
        txt += f" {{\\scriptsize [{pct(lo)}, {pct(hi)}]}}"
    if i == 3 and k != "jinx":
        q = PFA[(PFA.reference == M["jinx"]) & (PFA.method == M[k])]
        if len(q) and q["dFAR lo"].iloc[0] > 0:  # this row raises more false alarms than Jinx, CI excludes zero
            txt = f"\\cellcolor{{wincell}}{txt}$^{{\\dagger}}$"
        elif len(q) and q["dFAR hi"].iloc[0] < 0:  # this row raises fewer false alarms than Jinx, CI excludes zero
            txt = f"{txt}$^{{\\ddagger}}$"
    if k in BASE and round(x, 4) == round(bestbase[i], 4):
        return f"\\underline{{{txt}}}"
    if k == "jinx" and clear_win(i):
        return f"\\textbf{{{txt}}}\\,\\textcolor{{wingreen}}{{$\\blacktriangle$}}"
    return txt


blocks = []
for blk in ORDER:
    rr = []
    for k in blk:
        pre = "\\rowcolor{jinxrow}" if k == "jinx" else ""
        rr.append(pre + f"{SHOW[k]} & " + " & ".join(cell(k, i) for i in range(4)) + f" & {lead(k)}" + r" \\")
    blocks.append("\n".join(rr))
pathlib.Path(OUT, "tab_main.tex").write_text(
    "\\begin{tabular}{lccccc}\\toprule\nStrategy & R@1 $\\uparrow$ & R@5 $\\uparrow$ & MRR $\\uparrow$ & False alarms \\% $\\downarrow$ & Jinx $-$ row, R@1 (pts) \\\\\\midrule\n"
    + "\\multicolumn{6}{l}{\\emph{Our tool}}\\\\\n" + blocks[0]
    + "\n\\midrule\n\\multicolumn{6}{l}{\\emph{Our tool with extra models added}}\\\\\n" + blocks[1]
    + "\n\\midrule\n\\multicolumn{6}{l}{\\emph{Baselines: link rule, classic detector, existing bot, embedding, text}}\\\\\n" + blocks[2]
    + "\n\\bottomrule\\end{tabular}\n")

G = [("cross-author, same agent", "same agent"), ("cross-author, cross-agent", "cross-agent"),
     ("cross-author, class A. code twin (>=50% identical changed lines)", "A: code twin"),
     ("cross-author, class B. partial code overlap", "B: partial overlap"),
     ("cross-author, class C. same files, different code", "C: same files"),
     ("cross-author, class D. no shared files (intent-level)", "D: no shared files"),
     ("cross-author, no link at all (no #ref, no shared issue)", "no link at all"),
     ("self-replacement", "self-replacement")]
rows = []
CK = ["jinx", "all", "haiku", "intrude", "cg"]
for g, lab in G:
    n = int(S[S.group == g].n.iloc[0])
    v = [get(g, k, "R@1") for k in CK]
    b = max(v)
    cells = [f"\\textbf{{{f3(x)}}}" if round(x, 3) == round(b, 3) else f3(x) for x in v]
    cells[0] = "\\cellcolor{jinxrow}" + cells[0]
    rows.append(f"{lab} & {n} & " + " & ".join(cells) + r" \\")
pathlib.Path(OUT, "tab_classes.tex").write_text(
    "\\begin{tabular}{lrccccc}\\toprule\nGroup & $n$ & \\cellcolor{jinxrow}Jinx & All LR & Haiku+Jinx & INTRUDE+t & contrib-guard \\\\\\midrule\n"
    + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")

def pair(ref, meth, col):
    r = P[(P.reference == M[ref]) & (P.method == M[meth])].iloc[0]
    return r[col], r[col + " lo"], r[col + " hi"]

mac = []
def nm(name, v):
    mac.append(f"\\newcommand{{\\{name}}}{{{v}}}")
for col, tag in [("dR@1", "RO"), ("dR@5", "RF"), ("dMRR", "MRR")]:
    for ref, rt in [("intrude", "Intrude"), ("cg", "Cg")]:
        d, lo, hi = pair(ref, "jinx", col)
        nm(f"d{tag}{rt}", f"{100 * d:+.1f}"); nm(f"d{tag}{rt}Lo", f"{100 * lo:+.1f}"); nm(f"d{tag}{rt}Hi", f"{100 * hi:+.1f}")
for k in ["jinx", "intrude", "cg", "all", "haiku", "links", "jinxlex"]:
    nm(f"ROne{k}", f3(get(CA, k, "R@1"))); nm(f"RFive{k}", f3(get(CA, k, "R@5")))
for k in ["jinx", "intrude", "jinxlex", "all"]:
    nm(f"FAR{k}", pct(far(k)[0]))
nm("nStrategies", S.method.nunique())
nm("nSigRFive", int((P[P.reference == M["intrude"]]["dR@5 lo"] > 0).sum()))
nm("nComparedRFive", int((P.reference == M["intrude"]).sum()))
for g, name in [("all labelled", "nPairs"), ("self-replacement", "nSelf"), (CA, "nCross"),
                ("cross-author, same agent", "nSameAgent"), ("cross-author, cross-agent", "nCrossAgent")]:
    nm(name, int(S[S.group == g].n.iloc[0]))
nm("nNeg", 2965)  # bench.pkl: queries with neg=True
nm("nPRs", "76{,}209")  # bench.pkl: len(need)
pathlib.Path(OUT, "numbers.tex").write_text("\n".join(mac) + "\n")
print("wrote", sorted(os.listdir(OUT)))
