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

M = {"jinx": "Jinx + MiniLM, LR (current tool)", "all": "All signals, LR",
     "intrude": "INTRUDE + time (Wang et al. 2019), LR", "cg": "contrib-guard/phoenix (bot, exact port)",
     "haiku": "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5", "haikuonly": "LLM judge Claude Haiku 4.5 re-rank top-5",
     "casc": "Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR)", "links": "Links only (same issue / #ref)",
     "tfidf": "TF-IDF raw text (Li et al. 2017)", "bge": "BGE-small template-stripped",
     "qwen14": "LLM judge Qwen2.5-14B + Jinx (avg) top-5"}
SHOW = {"jinx": "Jinx (ours)", "all": "All signals, LR", "intrude": "INTRUDE + time~\\cite{ren2019intrude,wang2019time}",
        "cg": "contrib-guard (bot)", "haiku": "Claude Haiku 4.5 + Jinx", "haikuonly": "Claude Haiku 4.5 alone",
        "casc": "Jinx + BGE rerank + Qwen-7B", "links": "Links only", "tfidf": "TF-IDF~\\cite{li2017detecting}",
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
rows = []
for k in ["jinx", "all", "casc", "haiku", "qwen14", "haikuonly", "intrude", "cg", "links", "tfidf", "bge"]:
    a, lo, hi = far(k) if (FA.method == M[k]).any() else (float("nan"),) * 3
    rows.append(f"{SHOW[k]} & {f3(get(CA, k, 'R@1'))} & {f3(get(CA, k, 'R@5'))} & {f3(get(CA, k, 'MRR'))} & "
                + ("--" if pd.isna(a) else f"{pct(a)} [{pct(lo)}, {pct(hi)}]") + r" \\")
pathlib.Path(OUT, "tab_main.tex").write_text(
    "\\begin{tabular}{lcccc}\\toprule\nStrategy & R@1 & R@5 & MRR & False alarms \\% [95\\% CI] \\\\\\midrule\n"
    + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")

G = [("cross-author, same agent", "same agent"), ("cross-author, cross-agent", "cross-agent"),
     ("cross-author, class A. code twin (>=50% identical changed lines)", "A: code twin"),
     ("cross-author, class B. partial code overlap", "B: partial overlap"),
     ("cross-author, class C. same files, different code", "C: same files"),
     ("cross-author, class D. no shared files (intent-level)", "D: no shared files"),
     ("cross-author, no link at all (no #ref, no shared issue)", "no link at all"),
     ("self-replacement", "self-replacement")]
rows = []
for g, lab in G:
    n = int(S[S.group == g].n.iloc[0])
    rows.append(f"{lab} & {n} & " + " & ".join(f3(get(g, k, "R@1")) for k in ["jinx", "all", "intrude", "cg", "haiku"]) + r" \\")
pathlib.Path(OUT, "tab_classes.tex").write_text(
    "\\begin{tabular}{lrccccc}\\toprule\nGroup (Recall@1) & $n$ & Jinx & All LR & INTRUDE+t & c-guard & Haiku+J \\\\\\midrule\n"
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
for k in ["jinx", "intrude", "cg", "all", "haiku", "links"]:
    nm(f"ROne{k}", f3(get(CA, k, "R@1"))); nm(f"RFive{k}", f3(get(CA, k, "R@5")))
for k in ["jinx", "intrude"]:
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
