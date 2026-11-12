from __future__ import annotations

import argparse
import json
import sys
import time
from importlib.metadata import PackageNotFoundError, version

from .pr import PR
from .scorer import Detector
from .templates import TemplateModel


def _load(path: str):
    with open(path) as fh:
        raw = fh.read().strip()
    if not raw:
        return []
    if raw[0] in "[{":
        try:
            d = json.loads(raw)
            return d if isinstance(d, list) else [d]
        except json.JSONDecodeError:
            pass
    return [json.loads(x) for x in raw.splitlines() if x.strip()]


def _attach_diff(d: dict, diff_path: str | None) -> dict:
    if diff_path:
        with open(diff_path) as fh:
            d = {**d, "diff": fh.read()}
    return d


def cmd_check(a) -> int:
    t0 = time.perf_counter()
    new = PR.from_dict(_attach_diff(_load(a.new_pr)[0], a.diff))
    queue = [PR.from_dict(d) for d in _load(a.open_queue)]
    embedder = None
    if a.embed:
        from .embed import Embedder

        embedder = Embedder(a.embed)
    templates = None
    if a.templates:
        with open(a.templates) as fh:
            templates = TemplateModel.from_json(fh.read())
    det = Detector(templates=templates, embedder=embedder)
    thr = det.threshold if a.threshold is None else a.threshold
    matches = det.rank(new, queue, top=a.top)
    ms = (time.perf_counter() - t0) * 1000
    if a.json:
        print(
            json.dumps(
                {
                    "pr": new.number,
                    "threshold": thr,
                    "ms": round(ms, 1),
                    "matches": [m.to_dict() | {"flag": m.score >= thr} for m in matches],
                },
                indent=2,
            )
        )
        return 0
    flagged = [m for m in matches if m.score >= thr]
    print(
        f"PR #{new.number}: checked {len(queue)} open PRs in {ms:.0f} ms. "
        f"{len(flagged)} likely duplicate(s) (score >= {thr:.2f})."
    )
    for m in matches:
        mark = "DUPLICATE?" if m.score >= thr else "          "
        print(f"  {mark} #{m.number}  score {m.score:.2f}  {m.title[:70]}")
        for r in m.reasons:
            print(f"               - {r}")
    return 0


def cmd_learn(a) -> int:
    rows = _load(a.corpus)
    tm = TemplateModel.learn(
        ((d.get("agent", ""), d.get("repo", ""), d.get("body", "")) for d in rows),
        min_share=a.min_share,
        min_repos=a.min_repos,
    )
    with open(a.output, "w") as fh:
        fh.write(tm.to_json())
    print(f"learned {sum(len(v) for v in tm.lines_by_agent.values())} template lines -> {a.output}")
    return 0


def _installed_version() -> str:
    try:
        return version("jinx-pr")
    except PackageNotFoundError:
        return "unknown"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="jinx", description="Find likely duplicate PRs in an open-PR queue.")
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {_installed_version()}")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="rank open PRs that may duplicate a new PR")
    c.add_argument("new_pr", help="JSON file with the new PR (GitHub API shape; optional files/diff/agent)")
    c.add_argument("--open-queue", required=True, help="JSON list or JSON-lines file of open PRs")
    c.add_argument("--diff", help="unified diff file for the new PR")
    c.add_argument("--top", type=int, default=5)
    c.add_argument("--threshold", type=float)
    c.add_argument(
        "--embed",
        nargs="?",
        const="sentence-transformers/all-MiniLM-L6-v2",
        help="also use a local embedding model (needs jinx-pr[embed])",
    )
    c.add_argument("--templates", help="template file from `jinx learn-templates`")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=cmd_check)
    lt = sub.add_parser("learn-templates", help="learn agent boilerplate lines from a PR corpus")
    lt.add_argument("corpus", help="JSON-lines with agent, repo, body")
    lt.add_argument("-o", "--output", required=True)
    lt.add_argument("--min-share", type=float, default=0.01)
    lt.add_argument("--min-repos", type=int, default=5)
    lt.set_defaults(fn=cmd_learn)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
