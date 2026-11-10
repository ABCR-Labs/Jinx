from agentdup import action


class FakeGH:
    def __init__(self, prs, files):
        self.prs, self.files, self.posted = prs, files, []

    def pages(self, path, limit):
        if path.startswith("/pulls?"):
            return self.prs
        if path.endswith("/files"):
            return self.files[int(path.split("/")[2])]
        return []

    def call(self, method, path, body=None):
        self.posted.append((method, path, body))


def test_action_posts_comment():
    def pr(n, t, b):
        return {
            "number": n,
            "title": t,
            "body": b,
            "user": {"login": f"u{n}"},
            "created_at": f"2026-01-0{n}T00:00:00Z",
        }

    files = {
        1: [{"filename": "auth.py", "patch": "@@ -1,3 +1,4 @@\n+TIMEOUT = 3600 # seconds"}],
        2: [{"filename": "auth.py", "patch": "@@ -1,3 +1,4 @@\n+TIMEOUT = 3600 # seconds"}],
        3: [{"filename": "README.md", "patch": "@@ -1 +1 @@\n+typo fixed here"}],
    }
    gh = FakeGH([pr(1, "Fix timeout", "Fixes #9"), pr(3, "Docs", "typo")], files)
    body = action.run({"pull_request": pr(2, "Fix session timeout", "Fixes #9")}, gh, None, 50, 3)
    assert body and "#1" in body and gh.posted[0][0] == "POST"
