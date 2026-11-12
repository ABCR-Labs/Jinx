"""Shared Claude duplicate-judge prompt (same wording as claude_judge.py)."""
import os
import re
import time

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5")
PRICE_IN, PRICE_OUT = 1.0 / 1e6, 5.0 / 1e6
SYS = ("You review pull requests for a code repository. Two PRs are duplicates if they try to make the same change or fix the same "
       "problem, so only one of them should be merged. Reply with only a JSON object: "
       '{"duplicate": "yes" or "no", "probability": integer 0-100 that they are duplicates}.')
_cl = None


def judge(new_view, open_view):
    global _cl
    _cl = _cl or anthropic.Anthropic(max_retries=8)
    msg = f"NEW PR\n{new_view[:3000]}\n\nOPEN PR\n{open_view[:3000]}\n\nAre these two pull requests duplicates?"
    t0 = time.perf_counter()
    r = _cl.messages.create(model=MODEL, max_tokens=40, system=SYS, messages=[{"role": "user", "content": msg}])
    ms = 1000 * (time.perf_counter() - t0)
    txt = r.content[0].text
    m = re.search(r'"probability"\s*:\s*(\d+)', txt)
    v = re.search(r'"duplicate"\s*:\s*"(\w+)"', txt)
    p = int(m.group(1)) / 100 if m else (1.0 if v and v.group(1).lower() == "yes" else 0.0)
    return p, (v.group(1).lower() if v else txt[:20]), r.usage.input_tokens, r.usage.output_tokens, ms
