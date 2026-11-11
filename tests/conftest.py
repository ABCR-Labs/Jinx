import pytest

from jinx_pr import PR, TemplateModel

TEMPLATE = "## Summary\n{0}\n\n## Testing\n- Ran the unit tests\n\nGenerated with [Claude Code](https://claude.ai/code)"


@pytest.fixture
def templates():
    return TemplateModel(
        {"Claude_Code": {"summary", "testing", "ran the unit tests", "generated with claude code url"}}
    )


def make(
    number,
    title,
    what,
    files,
    hunks=(),
    author="alice",
    agent="Claude_Code",
    created="2026-01-01T10:00:00Z",
    issues=(),
    added=(),
):
    return PR(
        number=number,
        title=title,
        body=TEMPLATE.format(what),
        author=author,
        agent=agent,
        created_at=created,
        files=set(files),
        hunks=set(hunks),
        linked_issues=set(issues),
        added=set(added),
    )
