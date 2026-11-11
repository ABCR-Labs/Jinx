"""GitHub Action entry point: comment on a newly opened PR when likely duplicates are open.

Uses only the GitHub REST API with the workflow's GITHUB_TOKEN. No LLM or paid API calls."""

from __future__ import annotations

import json
import os
import sys
import urllib.request

from .pr import PR
from .scorer import Detector

MARKER = "<!-- jinx_pr:v1 -->"
API = os.environ.get("GITHUB_API_URL", "https://api.github.com")


class GitHub:
    def __init__(self, token: str, repo: str):
        self.token, self.repo = token, repo

    def call(self, method: str, path: str, body: dict | None = None):
        req = urllib.request.Request(
            f"{API}/repos/{self.repo}{path}",
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
        )
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or b"null")

    def pages(self, path: str, limit: int):
        out, page = [], 1
        while len(out) < limit:
            sep = "&" if "?" in path else "?"
            batch = self.call("GET", f"{path}{sep}per_page=100&page={page}")
            if not batch:
                break
            out.extend(batch)
            page += 1
        return out[:limit]


def pr_from_api(gh: GitHub, d: dict) -> PR:
    files = gh.pages(f"/pulls/{d['number']}/files", 300)
    diff = "".join(f"diff --git a/{f['filename']} b/{f['filename']}\n{f.get('patch') or ''}\n" for f in files)
    return PR.from_dict({**d, "diff": diff, "files": [f["filename"] for f in files]})


def render(new: PR, matches, threshold: float) -> str:
    rows = [m for m in matches if m.score >= threshold]
    lines = [MARKER, f"**Jinx:** this PR may duplicate {len(rows)} open PR(s).", ""]
    for m in rows:
        lines.append(f"- #{m.number} (score {m.score:.2f}): " + "; ".join(m.reasons))
    lines += ["", "_Automated hint, not a decision. A maintainer should confirm before closing anything._"]
    return "\n".join(lines)


def run(event: dict, gh: GitHub, threshold: float | None, max_open: int, top: int, embed: bool = False) -> str | None:
    new = pr_from_api(gh, event["pull_request"])
    open_prs = [
        d
        for d in gh.pages("/pulls?state=open&sort=created&direction=desc", max_open)
        if d["number"] != new.number
    ]
    queue = [pr_from_api(gh, d) for d in open_prs]
    embedder = None
    if embed:
        from .embed import Embedder

        embedder = Embedder()
    det = Detector(embedder=embedder)
    thr = det.threshold if threshold is None else threshold
    matches = det.rank(new, queue, top=top)
    if not any(m.score >= thr for m in matches):
        return None
    body = render(new, matches, thr)
    old = [c for c in gh.pages(f"/issues/{new.number}/comments", 300) if MARKER in (c.get("body") or "")]
    if old:
        gh.call("PATCH", f"/issues/comments/{old[0]['id']}", {"body": body})
    else:
        gh.call("POST", f"/issues/{new.number}/comments", {"body": body})
    return body


def main() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"]) as fh:
        event = json.load(fh)
    if "pull_request" not in event:
        print("jinx_pr: not a pull_request event, skipping")
        return 0
    thr = os.environ.get("INPUT_THRESHOLD") or None
    gh = GitHub(os.environ["INPUT_GITHUB_TOKEN"], os.environ["GITHUB_REPOSITORY"])
    body = run(
        event,
        gh,
        float(thr) if thr else None,
        int(os.environ.get("INPUT_MAX_OPEN_PRS", "200")),
        int(os.environ.get("INPUT_TOP", "3")),
        os.environ.get("INPUT_EMBED", "true").lower() == "true",
    )
    print(body or "jinx_pr: no likely duplicates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
