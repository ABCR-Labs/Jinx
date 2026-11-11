"""Map a PR author / description to the agent names used in the AIDev dataset."""

from __future__ import annotations

_LOGINS = {
    "copilot": "Copilot",
    "copilot-swe-agent[bot]": "Copilot",
    "devin-ai-integration[bot]": "Devin",
    "chatgpt-codex-connector[bot]": "OpenAI_Codex",
    "google-labs-jules[bot]": "Google_Jules",
    "cursor[bot]": "Cursor",
    "cursoragent": "Cursor",
    "claude[bot]": "Claude_Code",
}
_SIGNATURES = [
    ("generated with [claude code]", "Claude_Code"),
    ("claude.ai/code", "Claude_Code"),
    ("co-authored-by: claude", "Claude_Code"),
    ("chatgpt.com/codex", "OpenAI_Codex"),
    ("app.devin.ai", "Devin"),
    ("cursor.com/agents", "Cursor"),
    ("jules.google", "Google_Jules"),
    ("copilot coding agent", "Copilot"),
]


def guess_agent(author: str = "", body: str = "") -> str:
    a = (author or "").lower()
    if a in _LOGINS:
        return _LOGINS[a]
    b = (body or "").lower()
    for sig, name in _SIGNATURES:
        if sig in b:
            return name
    return ""
