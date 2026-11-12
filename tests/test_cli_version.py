import pytest

from jinx_pr import __version__
from jinx_pr.cli import main


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0
    assert capsys.readouterr().out.strip() == f"jinx {__version__}"
