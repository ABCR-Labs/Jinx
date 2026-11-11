"""End-to-end CLI tests on real AIDev live queues (tests/fixtures/aidev, CC BY 4.0)."""

import json
from pathlib import Path

import pytest

from jinx_pr.cli import main

FIX = Path(__file__).parent / "fixtures" / "aidev"
EXPECTED = json.loads((FIX / "expected.json").read_text())


@pytest.mark.parametrize("kind", sorted(EXPECTED))
def test_cli_on_real_queue(kind, capsys):
    exp = EXPECTED[kind]
    assert main(["check", str(FIX / f"{kind}_new.json"), "--open-queue", str(FIX / f"{kind}_queue.jsonl"), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["pr"] == exp["pr"]
    flagged = [m["number"] for m in out["matches"] if m["flag"]]
    if exp["expected_duplicate"] is None:
        assert flagged == []
    else:
        assert out["matches"][0]["number"] == exp["expected_duplicate"]
        assert flagged[0] == exp["expected_duplicate"]
        assert out["matches"][0]["reasons"]


def test_shipped_weights_are_trained():
    from jinx_pr.scorer import load_weights

    for name in ["weights.json", "weights_emb.json"]:
        w = load_weights(name)
        assert "placeholder" not in w.get("note", "")
        assert len(w["coef"]) == len(w["features"]) == len(w["mean"]) == len(w["scale"])
