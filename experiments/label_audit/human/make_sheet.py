"""Build the 100-pair human label sheets (one per labeller) and the hidden Haiku key.

Sample: 100 of the 313 open-only cross-author pairs that make up the papers' main result (seed 0)."""

import json
import os
import pickle
import re

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
D = os.environ.get("DATA", os.path.join(ROOT, "..", "data")) + "/"
LABELS = [
    "yes - same change",
    "yes - replacement (redone the same work)",
    "partly - one PR contains the other",
    "no - related but different work",
    "no - unrelated",
    "unclear",
]
TO_AUDIT = dict(zip(LABELS, ["duplicate", "replacement", "subsumed", "related", "related", "unclear"]))

Q = pickle.load(open(D + "bench.pkl", "rb"))["queries"]
ranks = pd.read_parquet(os.path.join(ROOT, "experiments/results/ranks.parquet"))
cross = sorted(i for i in ranks.index if not Q[i]["neg"] and not Q[i]["self"])
A = pd.read_parquet(os.path.join(HERE, "..", "audit_cross_pairs.parquet")).set_index("qi").loc[cross]
H = {j["qi"]: j["label"] for j in map(json.loads, open(os.path.join(HERE, "..", "audit_cross_labels.jsonl")))}
S = A.sample(100, random_state=0).reset_index()


def field(prompt, who, name):
    blk = prompt.split(f"## {who} PR")[1].split("## NEWER PR")[0] if who == "OLDER" else prompt.split("## NEWER PR")[1]
    m = re.search(rf"^{name}: (.*)$", blk, re.M)
    return m.group(1).strip() if m else ""


rows = []
for k, r in S.iterrows():
    repo = r.repo.split("/repos/")[1]
    rows.append({
        "id": k + 1,
        "repository": repo,
        "older PR": f"https://github.com/{repo}/pull/{r.old}",
        "newer PR": f"https://github.com/{repo}/pull/{r.new}",
        "older title": field(r.prompt, "OLDER", "Title"),
        "newer title": field(r.prompt, "NEWER", "Title"),
        "comment that linked them": r.phrase,
    })
sheet = pd.DataFrame(rows)
pd.DataFrame({"id": sheet.id, "qi": S.qi, "haiku": [H[q] for q in S.qi]}).to_csv(
    os.path.join(HERE, "key_do_not_open.csv"), index=False)
sheet.to_csv(os.path.join(HERE, "pairs.csv"), index=False)

HELP = [
    "Jinx label check: 100 pull-request pairs",
    "",
    "Each row is a pair of PRs in the same repository. Someone later commented on one of them with words like",
    "'duplicate of #N' or 'superseded by #N'. We use those comments as duplicate labels; this sheet checks them.",
    "",
    "For each row: open both PR links, read the titles, descriptions and changed files, then pick one label.",
    "",
    "  yes - same change: both PRs try to make the same change or fix the same problem.",
    "  yes - replacement: the newer PR redoes the same work (new approach, rebase, cleanup) and replaces the older one.",
    "  partly - one PR contains the other: one PR's change is a part of the other, bigger PR.",
    "  no - related but different work: same area, but each PR should be reviewed on its own.",
    "  no - unrelated: the link comment looks wrong.",
    "  unclear: you cannot tell from the PRs.",
    "",
    "Work alone: do not discuss rows with the other labeller until both sheets are done.",
    "Typical time: 1 to 2 hours. Notes are optional. Send the finished file back as-is.",
]
for who in ["A", "B"]:
    wb = Workbook()
    h = wb.active
    h.title = "How to label"
    for i, t in enumerate(HELP, 1):
        h.cell(i, 1, t).font = Font(bold=(i == 1), size=14 if i == 1 else 11)
    h.column_dimensions["A"].width = 120
    ws = wb.create_sheet("Pairs")
    cols = list(sheet.columns) + ["label", "notes"]
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="4F46E5")
    for row in sheet.itertuples(index=False):
        ws.append(list(row) + ["", ""])
    for r in range(2, len(sheet) + 2):
        for c in (3, 4):
            cell = ws.cell(r, c)
            cell.hyperlink, cell.style = cell.value, "Hyperlink"
        ws.cell(r, 8).fill = PatternFill("solid", fgColor="FEF3C7")
    lists = wb.create_sheet("lists")
    for i, v in enumerate(LABELS, 1):
        lists.cell(i, 1, v)
    lists.sheet_state = "hidden"
    dv = DataValidation(type="list", formula1=f"=lists!$A$1:$A${len(LABELS)}", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H2:H{len(sheet) + 1}")
    for col, w in zip("ABCDEFGHI", [5, 28, 44, 44, 50, 50, 30, 38, 40]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "C2"
    wb.save(os.path.join(HERE, f"label_sheet_{who}.xlsx"))
json.dump(TO_AUDIT, open(os.path.join(HERE, "label_map.json"), "w"), indent=1)
print(len(sheet), "pairs;", sheet.repository.nunique(), "repositories")
