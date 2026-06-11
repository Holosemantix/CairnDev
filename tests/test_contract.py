from __future__ import annotations

from pathlib import Path

from cairndev.contract import load_contract


def test_load_contract_uses_defaults_when_file_is_missing(tmp_path: Path) -> None:
    contract = load_contract(tmp_path)
    assert contract.project_name == tmp_path.name
    assert contract.budgets.max_function_lines == 80


def test_load_contract_ignores_non_mapping_document(tmp_path: Path) -> None:
    _write_contract(tmp_path, "- not\n- a\n- mapping\n")

    contract = load_contract(tmp_path)
    assert contract.project_name == tmp_path.name
    assert contract.budgets.max_python_file_lines == 400


def test_load_contract_filters_unknown_and_invalid_budget_values(tmp_path: Path) -> None:
    _write_contract(
        tmp_path,
        """schema_version: "0.1"
project_name: "configured"

budgets:
  max_function_lines: invalid
  max_class_methods: 3
  discourage_global_mutable_state: false
  max_python_file_lines: 0
  unknown_budget: 10
""",
    )

    contract = load_contract(tmp_path)
    assert contract.project_name == "configured"
    assert contract.budgets.max_function_lines == 80
    assert contract.budgets.max_class_methods == 3
    assert contract.budgets.discourage_global_mutable_state is False
    assert contract.budgets.max_python_file_lines == 400


def test_load_contract_normalizes_commands_and_checklist(tmp_path: Path) -> None:
    _write_contract(
        tmp_path,
        """schema_version: "0.1"
commands:
  test: 42
review_checklist:
  - ok
  - 7
""",
    )

    contract = load_contract(tmp_path)
    assert contract.commands == {"test": "42"}
    assert contract.review_checklist == ["ok", "7"]


def _write_contract(tmp_path: Path, content: str) -> None:
    contract_dir = tmp_path / ".cairndev"
    contract_dir.mkdir()
    contract_dir.joinpath("contract.yaml").write_text(content, encoding="utf-8")
