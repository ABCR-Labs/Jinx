"""Extra number macros and figures for the papers (from experiments/results and experiments/label_audit)."""
import json
import os
import pathlib

import numpy as np
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
PL = json.loads(pathlib.Path(os.path.join(RES, "package_latency.json")).read_text())  # end-to-end, installed package, 4 CPU threads
nm("latJinx", f"{PL['lexical']['median_ms']:.0f}"); nm("latJinxPninety", f"{PL['lexical']['p90_ms']:.0f}")
nm("latMini", f"{PL['minilm']['median_ms'] / 1000:.1f}"); nm("latMiniPninety", f"{PL['minilm']['p90_ms'] / 1000:.1f}")
nm("latQueries", PL["queries"])
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
# audit precision on the cross-author pairs that remain on open-only queues
_lab = pd.read_json(os.path.join(EXP, "label_audit", "audit_cross_labels.jsonl"), lines=True)
_lab = _lab[_lab.qi.isin(pd.read_parquet(os.path.join(RES, "ranks.parquet")).index)]
_v = _lab.label.isin(["duplicate", "replacement"]).values.astype(float)
_b = np.random.default_rng(0).choice(_v, (2000, len(_v))).mean(1)
nm("auditOpenN", len(_v)); nm("auditOpenStrict", f"{100 * _v.mean():.1f}")
nm("auditOpenStrictLo", f"{100 * np.quantile(_b, .025):.1f}"); nm("auditOpenStrictHi", f"{100 * np.quantile(_b, .975):.1f}")
nm("auditOpenLoose", f"{100 * _lab.label.isin(['duplicate', 'replacement', 'subsumed']).mean():.1f}")
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
# Queue construction: original queues (open + closed in the previous 7 days) vs real-use queues (open only, 200 most recent)
SG = pd.read_csv(os.path.join(EXP, "results_grace7", "strategies_by_group.csv"))
PG = pd.read_csv(os.path.join(EXP, "results_grace7", "paired_cross_author.csv"))
FG = pd.read_csv(os.path.join(EXP, "results_grace7", "false_alarms.csv"))
CG = "contrib-guard/phoenix (bot, exact port)"
for tag, m in [("jinx", JINX), ("intrude", INTR), ("cg", CG), ("links", "Links only (same issue / #ref)"),
               ("tfidf", "TF-IDF raw text (Li et al. 2017)"), ("all", "All signals, LR"), ("haiku", "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5")]:
    r = SG[(SG.group == CA) & (SG.method == m)]
    nm("Gseven" + tag, f"{float(r['R@1'].iloc[0]):.3f}")
    nm("FARGseven" + tag, f"{100 * float(FG[FG.method == m].FAR.iloc[0]):.1f}")
nm("nCrossGseven", int(SG[SG.group == CA].n.iloc[0])); nm("nPairsGseven", int(SG[SG.group == "all labelled"].n.iloc[0]))
r = PG[(PG.reference == JINX) & (PG.method == INTR)].iloc[0]
nm("dGsevenIntrude", f"{-100 * r['dR@1']:+.1f}"); nm("dGsevenIntrudeLo", f"{-100 * r['dR@1 hi']:+.1f}"); nm("dGsevenIntrudeHi", f"{-100 * r['dR@1 lo']:+.1f}")
AB = pd.read_csv(os.path.join(RES, "ablations.csv"))
ab = lambda st, m: f"{float(AB[(AB.setting == st) & (AB.method == m)]['R@1'].iloc[0]):.3f}"
nm("abJinxNoOpen", ab("benchmark queues (as in paper)", "Jinx without cand_open"))
nm("abIntrudeOpen", ab("benchmark queues (as in paper)", "INTRUDE + time + cand_open"))
nm("nGraceCand", 18)  # ablation log: cross-author gold pairs whose queue held a PR already closed at query time
nm("ROnehaikuAlone", r1(CA, find("LLM judge Claude Haiku 4.5 re-rank top-5")))
FA = pd.read_csv(os.path.join(RES, "false_alarms.csv")); PFA = pd.read_csv(os.path.join(RES, "paired_false_alarms.csv"))
for tag, m in [("links", "Links only (same issue / #ref)"), ("haiku", "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5"), ("qwen", "LLM judge Qwen2.5-14B + Jinx (avg) top-5"), ("cg", CG),
               ("tfidf", "TF-IDF raw text (Li et al. 2017)")]:
    nm("FARx" + tag, f"{100 * float(FA[FA.method == m].FAR.iloc[0]):.1f}")
    q = PFA[(PFA.reference == JINX) & (PFA.method == m)].iloc[0]
    nm("dFAR" + tag, f"{100 * q.dFAR:+.1f}"); nm("dFAR" + tag + "Lo", f"{100 * q['dFAR lo']:+.1f}"); nm("dFAR" + tag + "Hi", f"{100 * q['dFAR hi']:+.1f}")
OC = pd.read_csv(os.path.join(RES, "operating_curve.csv")); occ = OC.columns[2]
oc = lambda m, t: f"{100 * float(OC[(OC.method == m) & (OC['FAR target'] == t)][occ].iloc[0]):.0f}"
for tag, m in [("jinx", JINX), ("haiku", "LLM judge Claude Haiku 4.5 + Jinx (avg) top-5"), ("qwen", "LLM judge Qwen2.5-14B + Jinx (avg) top-5"), ("intrude", INTR), ("links", "Links only (same issue / #ref)"),
               ("cg", CG)]:
    nm("OCone" + tag, oc(m, 0.01)); nm("OCfive" + tag, oc(m, 0.05))
# Impact: cost of duplicates and a replay of day-0 warnings
DC = json.loads(pathlib.Path(os.path.join(RES, "duplicate_cost_summary.json")).read_text())
x = DC["cross-author"]
nm("dupDelayMedMin", f"{60 * x['delay_h median']:.0f}"); nm("dupDelayMeanH", f"{x['delay_h mean']:.0f}")
nm("dupLateOneH", f"{100 * x['share caught after >1h']:.0f}"); nm("dupLateOneD", f"{100 * x['share after >24h']:.0f}")
nm("dupLateSevenD", f"{100 * x['share after >7d']:.0f}"); nm("dupEffort", f"{100 * x['share with >=1 human comment or review before flag']:.0f}")
nm("dupComments", x["human comments before flag (total)"]); nm("dupReviews", x["reviews before flag (total)"])
nm("dupLifeH", f"{x['closed_life_h median']:.0f}"); nm("dupLinesMed", f"{x['lines added median']:.0f}")
nm("dupCommits", f"{x['commits on closed PR (total)']:,}".replace(",", "{,}"))
a = DC["all"]
nm("dupAllLateOneD", f"{100 * a['share after >24h']:.0f}"); nm("dupAllLines", f"{a['lines added (total)'] / 1e6:.1f}")
RP = pd.read_csv(os.path.join(RES, "replay_impact.csv"))
rp = RP[(RP.method == JINX) & (RP.group == CA)].iloc[0]
nm("replayWarn", f"{100 * rp['correct warning at open']:.0f}"); nm("replayWarnLate", f"{100 * rp['correct warning, human took >24h']:.0f}")
nm("replayHours", f"{rp['hours saved (sum, correct warnings)']:,.0f}".replace(",", "{,}"))
nm("replayEffort", int(rp["reviews+comments before flag avoided"])); nm("replayFA", f"{rp['false alarms per 100 PRs without duplicate']:.1f}")
nm("replayWarnLo", f"{100 * rp['correct warning lo']:.0f}"); nm("replayWarnHi", f"{100 * rp['correct warning hi']:.0f}")
nm("replayWrong", f"{100 * rp['wrong-PR warning at open']:.0f}")
for tag, m in [("Intrude", INTR), ("Cg", CG)]:
    r_ = RP[(RP.method == m) & (RP.group == CA)].iloc[0]
    nm("replayWarn" + tag, f"{100 * r_['correct warning at open']:.0f}"); nm("replayFA" + tag, f"{r_['false alarms per 100 PRs without duplicate']:.1f}")
nm("dupN", x["n"])
nm("dupBotOnly", DC["pairs skipped because only a bot wrote the duplicate comment"])
# queue cap, bootstrap count, link rule without tie-break, judge coverage
SJ = json.loads(pathlib.Path(os.path.join(RES, "summary.json")).read_text())
nm("nBoot", f"{SJ['n_bootstrap']:,}".replace(",", "{,}"))
nm("capAll", SJ["cap_dropped"]["all"]); nm("capCross", SJ["cap_dropped"]["cross-author"])
_j = S[(S.group == CA) & (S.method == JINX)].iloc[0]
nm("ROnejinxDeployed", f"{_j['R@1'] * _j.n / (_j.n + SJ['cap_dropped']['cross-author']):.3f}")
nm("ROnelinksraw", f"{float(S[(S.group == CA) & (S.method == 'Links only, no tie-break (same issue / #ref)')]['R@1'].iloc[0]):.3f}")
nm("ROnecgClassD", f"{float(S[(S.group == 'cross-author, class D. no shared files (intent-level)') & (S.method == CG)]['R@1'].iloc[0]):.2f}")
_cov = SJ.get("judge_coverage", {}).get("LLM judge Claude Haiku 4.5 + Jinx (avg) top-5", 1.0)
nm("judgeCovHaiku", f"{100 * _cov:.0f}")
nm("judgeNote", "" if _cov > 0.99 else f"Haiku was run on an earlier candidate set and scored {100 * _cov:.0f}\\% of the current top-5 candidates; the rest keep Jinx's score, so its results are approximate.")
pathlib.Path(OUT, "numbers_extra.tex").write_text("\n".join(mac) + "\n")
print(len(mac), "macros")
