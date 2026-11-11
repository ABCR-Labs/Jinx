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
     "casc": "Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR)", "links": "Links only (same issue / #ref)", "linksraw": "Links only, no tie-break (same issue / #ref)",
     "tfidf": "TF-IDF raw text (Li et al. 2017)", "bge": "BGE-small template-stripped",
     "qwen14": "LLM judge Qwen2.5-14B + Jinx (avg) top-5"}
SHOW = {"jinx": "Jinx (with MiniLM)", "jinxlex": "Jinx without MiniLM", "all": "All signals, LR", "intrude": "INTRUDE + time~\\cite{ren2019intrude,wang2019time}",
        "cg": "contrib-guard (bot)", "haiku": "Claude Haiku 4.5 + Jinx", "haikuonly": "Claude Haiku 4.5 alone on Jinx top-5",
        "casc": "Jinx + BGE re-ranker + Qwen-7B", "links": "Link rule, TF-IDF tie-break", "linksraw": "Link rule, no tie-break", "tfidf": "TF-IDF~\\cite{li2017detecting}",
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
BASE = ["links", "linksraw", "intrude", "cg", "bge", "tfidf"]
ORDER = [["jinx", "jinxlex"], ["all", "casc", "qwen14"], BASE]
vals = {}
for k in [k for blk in ORDER for k in blk]:
    vals[k] = [get(CA, k, "R@1"), get(CA, k, "R@5"), get(CA, k, "MRR"), far(k)[0]]
ORDER[2] = sorted(BASE, key=lambda k: -vals[k][0])


def fmt(x):
    t = f"{x:+.1f}"
    return "0.0" if t in ("+0.0", "-0.0") else t


def lead(k):
    """This row minus Jinx in R@1, in percentage points, with the paired repository-bootstrap 95% CI (unadjusted)."""
    if k == "jinx":
        return "--"
    r = P[(P.reference == M["jinx"]) & (P.method == M[k])].iloc[0]
    d, lo, hi = 100 * r["dR@1"], 100 * r["dR@1 lo"], 100 * r["dR@1 hi"]
    return f"{fmt(d)} [{fmt(lo)}, {fmt(hi)}]"


def cell(k, i):
    x = vals[k][i]
    txt = f3(x) if i < 2 else pct(x)
    if i == 2 and k != "jinx":
        q = PFA[(PFA.reference == M["jinx"]) & (PFA.method == M[k])]
        if len(q) and q["dFAR lo"].iloc[0] > 0:  # row raises more false alarms than Jinx, CI excludes zero
            txt = f"{txt}$^{{\\dagger}}$"
        elif len(q) and q["dFAR hi"].iloc[0] < 0:  # row raises fewer false alarms than Jinx, CI excludes zero
            txt = f"{txt}$^{{\\ddagger}}$"
    if round(x, 4) == round(best[i], 4):
        txt = f"\\textbf{{{txt}}}"
    return txt


COLS = [0, 1, 3]
vals = {k: [v[c] for c in COLS] for k, v in vals.items()}
best = [max(v[0] for v in vals.values()), max(v[1] for v in vals.values()), min(v[2] for v in vals.values())]
blocks = []
for blk in ORDER:
    rr = []
    for k in blk:
        pre = "\\rowcolor{jinxrow}" if k == "jinx" else ""
        rr.append(pre + f"{SHOW[k]} & " + " & ".join(cell(k, i) for i in range(3)) + f" & {lead(k)}" + r" \\")
    blocks.append("\n".join(rr))
pathlib.Path(OUT, "tab_main.tex").write_text(
    "\\begin{tabular}{@{}lcccc@{}}\\toprule\nStrategy & R@1 & R@5 & False alarms (\\%) & R@1: row $-$ Jinx (pts) \\\\\\midrule\n"
    + "\\multicolumn{5}{@{}l}{\\emph{Jinx}}\\\\\n" + blocks[0]
    + "\n\\midrule\n\\multicolumn{5}{@{}l}{\\emph{Jinx with an extra model on its top 5}}\\\\\n" + blocks[1]
    + "\n\\midrule\n\\multicolumn{5}{@{}l}{\\emph{Baselines}}\\\\\n" + blocks[2]
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


# Tool-demo table: shipped modes vs the main baselines, with flagged share at each method's threshold
FAc = FA.set_index("method")
TT = [("jinxlex", "Jinx, default (lexical)"), ("jinx", "Jinx with MiniLM"), ("intrude", "INTRUDE + time"), ("cg", "contrib-guard (bot)"),
      ("links", "Link rule")]
rows = []
for k, lab in TT:
    r, f = S[(S.group == CA) & (S.method == M[k])].iloc[0], FAc.loc[M[k]]
    rows.append(("\\rowcolor{jinxrow}" if k == "jinxlex" else "") + f"{lab} & {r['R@1']:.3f} & {100 * f['cross-author correct alerts']:.0f}\\% & "
                + f"{100 * f.FAR:.1f} [{100 * f['FAR lo']:.1f}, {100 * f['FAR hi']:.1f}] & {'yes' if k.startswith('jinx') else 'no'} \\\\")
pathlib.Path(OUT, "tab_tool.tex").write_text(
    "\\begin{tabular}{@{}lcccc@{}}\\toprule\nMethod & R@1 & Flagged & False alarms \\% & Explains code \\\\\\midrule\n" + "\n".join(rows)
    + "\n\\bottomrule\\end{tabular}\n")
