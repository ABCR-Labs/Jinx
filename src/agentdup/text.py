from __future__ import annotations

import math
import re
from collections import Counter

_TOK = re.compile(r"[a-z][a-z0-9_]+")
STOP = frozenset(
    [
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "from",
        "are",
        "was",
        "were",
        "will",
        "into",
        "have",
        "has",
        "not",
        "but",
        "you",
        "your",
        "our",
        "its",
        "can",
        "all",
        "any",
        "pr",
        "pull",
        "request",
        "adds",
        "add",
        "added",
        "update",
        "updated",
        "updates",
        "fix",
        "fixes",
        "fixed",
        "change",
        "changes",
        "changed",
    ]
)


def tokens(text: str) -> list[str]:
    out = []
    for t in _TOK.findall((text or "").lower()):
        for p in re.split(r"_+", t) if "_" in t else (t,):
            if len(p) > 2 and p not in STOP:
                out.append(p)
    return out


class TfIdf:
    """TF-IDF fitted on the documents at hand (the open queue plus the new PR)."""

    def __init__(self, docs: list[list[str]]):
        n = len(docs)
        df = Counter()
        for d in docs:
            df.update(set(d))
        self.idf = {t: math.log((1 + n) / (1 + k)) + 1.0 for t, k in df.items()}

    def vec(self, toks: list[str]) -> dict:
        tf = Counter(toks)
        v = {t: (1 + math.log(k)) * self.idf.get(t, 1.0) for t, k in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}


def cosine(a: dict, b: dict) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())
