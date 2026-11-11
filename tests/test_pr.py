from doppel.pr import PR, parse_diff

DIFF = """diff --git a/auth/session.py b/auth/session.py
--- a/auth/session.py
+++ b/auth/session.py
@@ -10,3 +10,4 @@ def f():
 x = 1
+TIMEOUT_SECONDS = 3600
@@ -40 +41 @@
-y
+    return refresh(token)
"""


def test_parse_diff():
    files, hunks, added = parse_diff(DIFF)
    assert files == {"auth/session.py"}
    assert hunks == {("auth/session.py", 10, 13), ("auth/session.py", 40, 41)}
    assert len(added) == 2


def test_from_dict_github_shape():
    pr = PR.from_dict(
        {
            "number": 7,
            "title": "t",
            "body": "Fixes #12 and see #3",
            "user": {"login": "bob"},
            "created_at": "2026-01-01T00:00:00Z",
            "diff": DIFF,
        }
    )
    assert pr.author == "bob" and pr.linked_issues == {12} and pr.mentions == {12, 3}
    assert pr.created_at.year == 2026 and "auth/session.py" in pr.files
