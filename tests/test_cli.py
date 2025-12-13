import sys
from emojify_cli.cli import main

def test_cli_version(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["emojify", "--version"])
    try:
        main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert "emojify" in out

