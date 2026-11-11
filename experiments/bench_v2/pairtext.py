"""Compact text view of a PR for pairwise models (cross-encoder, LLM judge)."""
import pickle, sys, pandas as pd
sys.path.insert(0, "/home/ubuntu/research/prdupecheck/jinx_pr/src")
from jinx_pr.templates import TemplateModel
D = "/home/ubuntu/research/prdupecheck/data/"
_pr = _diff = _files = _tm = None

def _load():
    global _pr, _diff, _files, _tm
    if _pr is None:
        _pr = pd.read_parquet(D + "pull_request.parquet", columns=["id", "number", "title", "body", "agent", "user"]).set_index("id")
        d = pickle.load(open(D + "difftext.pkl", "rb")); _diff = {k: "".join(v) if isinstance(v, list) else v for k, v in d.items()}
        _files = pickle.load(open(D + "diffs.pkl", "rb"))["files"]; _tm = TemplateModel.default()

def pr_text(i, body_chars=700, diff_lines=30, diff_chars=1200, with_author=False):
    _load(); r = _pr.loc[i]
    body = _tm.strip(r.body or "", r.agent or "").strip()[:body_chars]
    fs = sorted(_files.get(i, ()))[:15]
    added = [l for l in (_diff.get(i) or "").splitlines() if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    diff = "\n".join(added[:diff_lines])[:diff_chars]
    head = f"PR #{r.number}: {r.title or ''}"
    if with_author: head += f"\nAuthor: {r.user} ({r.agent})"
    return f"{head}\nDescription: {body}\nFiles: {', '.join(fs)}\nChanges:\n{diff}"
