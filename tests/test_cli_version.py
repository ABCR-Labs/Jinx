import pytest

from jinx_pr import __version__
from jinx_pr.cli import main


def test_cli_version(capsys):
    with pytest.raises(SystemExit):
        main(["--version"])
    assert __version__ in capsys.readouterr().out
