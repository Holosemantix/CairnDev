from __future__ import annotations

from pathlib import Path

from cairndev.contract import load_contract, load_goal_state


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


def test_load_contract_parses_agentic_iteration_policy(tmp_path: Path) -> None:
    _write_contract(
        tmp_path,
        """schema_version: "0.1"
agentic_iteration:
  enabled: true
  require_goal_file: true
  goal_file: ".cairndev/work-goal.yaml"
  max_iterations_without_human_review: 3
  require_verification_each_iteration: false
  min_success_criteria: 2
  min_pause_triggers: 2
""",
    )

    policy = load_contract(tmp_path).agentic_iteration
    assert policy.enabled is True
    assert policy.require_goal_file is True
    assert policy.goal_file == ".cairndev/work-goal.yaml"
    assert policy.max_iterations_without_human_review == 3
    assert policy.require_verification_each_iteration is False
    assert policy.min_success_criteria == 2
    assert policy.min_pause_triggers == 2


def test_load_goal_state_reads_durable_iteration_state(tmp_path: Path) -> None:
    goal_dir = tmp_path / ".cairndev"
    goal_dir.mkdir()
    goal_dir.joinpath("goal.yaml").write_text(
        """schema_version: "0.1"
objective: "Ship the backend service."
status: active
current_iteration: 4
last_verified_iteration: 4
last_human_review_iteration: 2
success_criteria:
  - "End-to-end path works."
pause_triggers:
  - "Scope changes."
""",
        encoding="utf-8",
    )

    goal = load_goal_state(tmp_path)
    assert goal is not None
    assert goal.objective == "Ship the backend service."
    assert goal.current_iteration == 4
    assert goal.success_criteria == ["End-to-end path works."]
    assert goal.pause_triggers == ["Scope changes."]


def _write_contract(tmp_path: Path, content: str) -> None:
    contract_dir = tmp_path / ".cairndev"
    contract_dir.mkdir()
    contract_dir.joinpath("contract.yaml").write_text(content, encoding="utf-8")
