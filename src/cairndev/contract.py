from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields
from pathlib import Path
from typing import Any

import yaml

from .models import (
    AgenticIterationPolicy,
    DesignContract,
    GoalState,
    LoopEngineeringState,
    QualityBudget,
)


def load_contract(root: Path) -> DesignContract:
    path = root / ".cairndev" / "contract.yaml"
    if not path.exists():
        return DesignContract.default(project_name=root.name)
    data = _mapping(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    budgets = _load_budget(_mapping(data.get("budgets", {})))
    agentic_iteration = _load_agentic_iteration_policy(
        _mapping(data.get("agentic_iteration", {}))
    )
    return DesignContract(
        schema_version=str(data.get("schema_version", "0.1")),
        project_name=str(data.get("project_name", root.name)),
        budgets=budgets,
        agentic_iteration=agentic_iteration,
        principles=dict(_mapping(data.get("principles", {}))),
        commands={
            str(key): str(value)
            for key, value in _mapping(data.get("commands", {})).items()
        },
        review_checklist=[str(item) for item in _sequence(data.get("review_checklist", []))],
    )


def load_goal_state(root: Path, goal_file: str = ".cairndev/goal.yaml") -> GoalState | None:
    path = root / goal_file
    if not path.exists():
        return None
    data = _mapping(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    return GoalState(
        schema_version=str(data.get("schema_version", "0.1")),
        objective=str(data.get("objective", "")),
        status=str(data.get("status", "active")),
        current_iteration=_positive_int_or_default(data.get("current_iteration"), 0),
        last_verified_iteration=_positive_int_or_default(
            data.get("last_verified_iteration"), 0
        ),
        last_human_review_iteration=_positive_int_or_default(
            data.get("last_human_review_iteration"), 0
        ),
        success_criteria=[str(item) for item in _sequence(data.get("success_criteria", []))],
        pause_triggers=[str(item) for item in _sequence(data.get("pause_triggers", []))],
        verification_required_commands=_verification_commands(data),
        loop_engineering=_loop_engineering_state(data),
    )


def _load_budget(data: Mapping[str, Any]) -> QualityBudget:
    defaults = QualityBudget()
    values: dict[str, Any] = {}
    for budget_field in fields(QualityBudget):
        value = data.get(budget_field.name, getattr(defaults, budget_field.name))
        default = getattr(defaults, budget_field.name)
        values[budget_field.name] = _coerce_budget_value(value, default)
    return QualityBudget(**values)


def _load_agentic_iteration_policy(data: Mapping[str, Any]) -> AgenticIterationPolicy:
    defaults = AgenticIterationPolicy()
    return AgenticIterationPolicy(
        enabled=_bool_or_default(data.get("enabled"), defaults.enabled),
        require_goal_file=_bool_or_default(
            data.get("require_goal_file"), defaults.require_goal_file
        ),
        goal_file=_text_or_default(data.get("goal_file"), defaults.goal_file),
        max_iterations_without_human_review=_positive_int_or_default(
            data.get("max_iterations_without_human_review"),
            defaults.max_iterations_without_human_review,
        ),
        require_verification_each_iteration=_bool_or_default(
            data.get("require_verification_each_iteration"),
            defaults.require_verification_each_iteration,
        ),
        min_success_criteria=_positive_int_or_default(
            data.get("min_success_criteria"), defaults.min_success_criteria
        ),
        min_pause_triggers=_positive_int_or_default(
            data.get("min_pause_triggers"), defaults.min_pause_triggers
        ),
    )


def _verification_commands(data: Mapping[str, Any]) -> list[str]:
    verification = _mapping(data.get("verification", {}))
    return [
        command
        for item in _sequence(verification.get("required_commands", []))
        if (command := str(item).strip())
    ]


def _loop_engineering_state(data: Mapping[str, Any]) -> LoopEngineeringState:
    loop_engineering = _mapping(data.get("loop_engineering", {}))
    trajectory_file = loop_engineering.get("trajectory_file")
    return LoopEngineeringState(
        trajectory_file=str(trajectory_file).strip()
        if isinstance(trajectory_file, str) and trajectory_file.strip()
        else None,
        checkpoint_files=_string_list(loop_engineering.get("checkpoint_files", [])),
        required_skills=_string_list(loop_engineering.get("required_skills", [])),
    )


def _string_list(value: Any) -> list[str]:
    return [text for item in _sequence(value) if (text := str(item).strip())]


def _coerce_budget_value(value: Any, default: Any) -> Any:
    if isinstance(default, bool):
        return _bool_or_default(value, default)
    if isinstance(default, int):
        return _positive_int_or_default(value, default)
    return value


def _bool_or_default(value: Any, default: bool) -> bool:
    return value if isinstance(value, bool) else default


def _positive_int_or_default(value: Any, default: int) -> int:
    is_positive_int = isinstance(value, int) and not isinstance(value, bool) and value > 0
    return value if is_positive_int else default


def _text_or_default(value: Any, default: str) -> str:
    if not isinstance(value, str):
        return default
    stripped = value.strip()
    return stripped or default


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, str):
        return []
    return value if isinstance(value, Sequence) else []
