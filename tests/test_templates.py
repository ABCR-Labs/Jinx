from jinx_pr.templates import TemplateModel, normalize_line, queue_common_lines


def test_normalize():
    assert normalize_line("## Testing - ran 12 tests in 3s") == "testing ran 0 tests in 0s"


def test_strip_removes_template_keeps_content(templates):
    body = "## Summary\nRaise session timeout to 1h\n## Testing\n- Ran the unit tests"
    assert templates.strip(body, "Claude_Code").strip() == "Raise session timeout to 1h"
    assert templates.template_share(body, "Claude_Code") == 0.75


def test_learn_needs_many_repos():
    rows = [("A", f"r{i % 6}", f"## Summary\nunique text {i}") for i in range(60)]
    rows += [("A", "r0", f"repo only line\nx{i}") for i in range(60)]
    tm = TemplateModel.learn(rows, min_count=5)
    assert "summary" in tm.lines_by_agent["A"]
    assert "repo only line" not in tm.lines_by_agent["A"]


def test_queue_common_lines():
    assert queue_common_lines(["a\nb", "a\nc", "a\nd", "e"], min_share=0.5) == {"a"}
