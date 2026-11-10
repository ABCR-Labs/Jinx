from __future__ import annotations

import math

from .pr import PR


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    i = len(a & b)
    return i / (len(a) + len(b) - i)


def containment(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def hunk_overlap(a: set, b: set) -> float:
    """Share of the smaller PR's hunks that overlap a hunk of the other PR in the same file."""
    if not a or not b:
        return 0.0
    small, other = (a, b) if len(a) <= len(b) else (b, a)
    by_file = {}
    for f, s, e in other:
        by_file.setdefault(f, []).append((s, e))
    hit = sum(1 for f, s, e in small if any(s < e2 and s2 < e for s2, e2 in by_file.get(f, ())))
    return hit / len(small)


def context_features(new: PR, cand: PR) -> dict:
    gap = 0.0
    if new.created_at and cand.created_at:
        gap = abs((new.created_at - cand.created_at).total_seconds()) / 3600.0
    still_open = 1.0
    if cand.closed_at and new.created_at and cand.closed_at <= new.created_at:
        still_open = 0.0
    return {
        "same_author": float(bool(new.author) and new.author == cand.author),
        "same_agent": float(bool(new.agent) and new.agent == cand.agent),
        "log_gap_hours": math.log1p(gap),
        "cand_open": still_open,
    }


def code_features(new: PR, cand: PR) -> dict:
    return {
        "file_jacc": jaccard(new.files, cand.files),
        "file_contain": containment(new.files, cand.files),
        "hunk_overlap": hunk_overlap(new.hunks, cand.hunks),
        "line_contain": containment(new.added, cand.added),
    }


def link_features(new: PR, cand: PR) -> dict:
    return {
        "same_issue": float(bool(new.linked_issues & cand.linked_issues)),
        "mention_ref": float(cand.number in new.mentions or new.number in cand.mentions),
    }
