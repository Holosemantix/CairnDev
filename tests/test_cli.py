from __future__ import annotations

from pathlib import Path

from cairndev.cli import main


def test_cli_check_json(capsys) -> None:
    root = Path(__file__).resolve().parents[1] / "examples" / "sample_project"
    code = main(["check", str(root), "--json"])
    captured = capsys.readouterr()
    assert code == 0
    assert '"passed": true' in captured.out
