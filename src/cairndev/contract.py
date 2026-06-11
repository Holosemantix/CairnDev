from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields
from pathlib import Path
from typing import Any

import yaml

from .models import DesignContract, QualityBudget


def load_contract(root: Path) -> DesignContract:
    path = root / ".cairndev" / "contract.yaml"
    if not path.exists():
        return DesignContract.default(project_name=root.name)
    data = _mapping(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
    budgets = _load_budget(_mapping(data.get("budgets", {})))
    return DesignContract(
        schema_version=str(data.get("schema_version", "0.1")),
        project_name=str(data.get("project_name", root.name)),
        budgets=budgets,
        principles=dict(_mapping(data.get("principles", {}))),
        commands={
            str(key): str(value)
            for key, value in _mapping(data.get("commands", {})).items()
        },
        review_checklist=[str(item) for item in _sequence(data.get("review_checklist", []))],
    )


def _load_budget(data: Mapping[str, Any]) -> QualityBudget:
    defaults = QualityBudget()
    values: dict[str, Any] = {}
    for budget_field in fields(QualityBudget):
        value = data.get(budget_field.name, getattr(defaults, budget_field.name))
        default = getattr(defaults, budget_field.name)
        values[budget_field.name] = _coerce_budget_value(value, default)
    return QualityBudget(**values)


def _coerce_budget_value(value: Any, default: Any) -> Any:
    if isinstance(default, bool):
        return value if isinstance(value, bool) else default
    if isinstance(default, int):
        is_positive_int = isinstance(value, int) and not isinstance(value, bool) and value > 0
        return value if is_positive_int else default
    return value


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, str):
        return []
    return value if isinstance(value, Sequence) else []
