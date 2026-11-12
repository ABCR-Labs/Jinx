import pytest

from jinx_pr.cli import main


def test_prints_version(capsys):
    with pytest.raises(SystemExit):
        main(["-V"])
    assert capsys.readouterr().out.startswith("jinx ")
