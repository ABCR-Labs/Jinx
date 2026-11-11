from __future__ import annotations

import re
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timezone

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
CLOSING = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:[\w.-]+/[\w.-]+)?#(\d+)", re.IGNORECASE
)
MENTION = re.compile(r"(?:^|[\s(\[])#(\d+)\b|/(?:pull|issues)/(\d+)\b")
MIN_LINE = 8


def line_hash(path: str, line: str) -> int:
    return zlib.crc32(f"{path}\0{line.strip()}".encode("utf-8", "ignore"))


def parse_time(v) -> datetime | None:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(str(v).replace("Z", "+00:00"))


def parse_diff(diff: str):
    """Changed files, old-side hunk ranges and hashed added lines from a unified diff."""
    files, hunks, added = set(), set(), set()
    cur = None
    for raw in diff.splitlines():
        if raw.startswith("diff --git "):
            parts = raw.split(" b/", 1)
            cur = parts[1].strip() if len(parts) == 2 else None
            if cur:
                files.add(cur)
        elif raw.startswith("+++ "):
            p = raw[4:].strip()
            if p != "/dev/null":
                cur = p.removeprefix("b/")
                files.add(cur)
        elif raw.startswith("--- "):
            continue
        elif cur and raw.startswith("@@"):
            m = HUNK.match(raw)
            if m:
                s = int(m.group(1))
                n = int(m.group(2) or 1)
                hunks.add((cur, s, s + max(n, 1)))
        elif cur and raw.startswith("+") and len(raw[1:].strip()) >= MIN_LINE:
            added.add(line_hash(cur, raw[1:]))
    return files, hunks, added


@dataclass
class PR:
    number: int
    title: str = ""
    body: str = ""
    author: str = ""
    agent: str = ""
    created_at: datetime | None = None
    closed_at: datetime | None = None
    files: set = field(default_factory=set)
    hunks: set = field(default_factory=set)
    added: set = field(default_factory=set)
    linked_issues: set = field(default_factory=set)
    url: str = ""

    def __post_init__(self):
        self.title = self.title or ""
        self.body = self.body or ""
        self.created_at = parse_time(self.created_at)
        self.closed_at = parse_time(self.closed_at)
        self.files = set(self.files)
        self.hunks = {tuple(h) for h in self.hunks}
        self.added = set(self.added)
        self.linked_issues = {int(i) for i in self.linked_issues} | {
            int(i) for i in CLOSING.findall(self.body)
        }

    @property
    def mentions(self) -> set:
        return {int(a or b) for a, b in MENTION.findall(f"{self.title}\n{self.body}")}

    @classmethod
    def from_dict(cls, d: dict) -> PR:
        files, hunks, added = set(d.get("files") or []), set(), set()
        if d.get("diff"):
            f2, hunks, added = parse_diff(d["diff"])
            files |= f2
        hunks |= {tuple(h) for h in d.get("hunks") or []}
        user = d.get("author") or d.get("user") or ""
        if isinstance(user, dict):
            user = user.get("login", "")
        return cls(
            number=int(d["number"]),
            title=d.get("title") or "",
            body=d.get("body") or "",
            author=user,
            agent=d.get("agent") or "",
            created_at=d.get("created_at"),
            closed_at=d.get("closed_at"),
            files=files,
            hunks=hunks,
            added=added | set(d.get("added_hashes") or []),
            linked_issues=set(d.get("linked_issues") or []),
            url=d.get("html_url") or d.get("url") or "",
        )
