import json

from conftest import make

from agentdup import Detector
from agentdup.cli import main
from agentdup.features import hunk_overlap


def test_hunk_overlap():
    assert hunk_overlap({("a", 1, 5)}, {("a", 4, 9), ("b", 1, 5)}) == 1.0
    assert hunk_overlap({("a", 1, 5)}, {("a", 5, 9)}) == 0.0


def test_template_lookalike_loses_to_code_duplicate(templates):
    new = make(
        103,
        "Increase idle limit for user sessions",
        "Users get logged out too early.",
        ["auth/session.py"],
        [("auth/session.py", 10, 14)],
        author="devin",
        agent="Devin",
        created="2026-01-02T10:00:00Z",
    )
    real = make(
        101,
        "Fix login timeout",
        "Session handler drops users after 5 minutes.",
        ["auth/session.py"],
        [("auth/session.py", 9, 12)],
    )
    lookalike = make(
        102,
        "Add dark-mode toggle",
        "Adds a toggle to the settings page.",
        ["ui/settings.tsx"],
        [("ui/settings.tsx", 1, 30)],
    )
    det = Detector(templates=templates)
    ranked = det.rank(new, [lookalike, real], top=2)
    assert ranked[0].number == 101
    assert any("changed files" in r for r in ranked[0].reasons)


def test_same_issue_reason(templates):
    new = make(5, "Handle empty cart", "x", ["cart.py"], issues={42}, created="2026-01-03T00:00:00Z")
    old = make(4, "Empty cart crash", "y", ["cart.py"], issues={42})
    m = Detector(templates=templates).rank(new, [old])[0]
    assert "same linked issue: #42" in m.reasons


def test_cli_json(tmp_path, capsys):
    new = {
        "number": 3,
        "title": "Fix login timeout",
        "body": "Fixes #9",
        "files": ["auth.py"],
        "created_at": "2026-01-02T00:00:00Z",
    }
    q = [
        {
            "number": 1,
            "title": "Fix login timeout bug",
            "body": "Closes #9",
            "files": ["auth.py"],
            "created_at": "2026-01-01T00:00:00Z",
        },
        {
            "number": 2,
            "title": "Docs",
            "body": "typo",
            "files": ["README.md"],
            "created_at": "2026-01-01T00:00:00Z",
        },
    ]
    (tmp_path / "new.json").write_text(json.dumps(new))
    (tmp_path / "q.jsonl").write_text("\n".join(json.dumps(x) for x in q))
    assert (
        main(["check", str(tmp_path / "new.json"), "--open-queue", str(tmp_path / "q.jsonl"), "--json"]) == 0
    )
    out = json.loads(capsys.readouterr().out)
    assert out["matches"][0]["number"] == 1 and out["matches"][0]["flag"]
