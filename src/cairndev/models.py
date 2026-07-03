from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

Severity = Literal["info", "warning", "error"]
GoalStatus = Literal["active", "paused", "blocked", "complete"]


@dataclass(frozen=True)
class Finding:
    code: str
    severity: Severity
    message: str
    path: str | None = None
    line: int | None = None
    suggestion: str | None = None


@dataclass
class QualityBudget:
    max_python_file_lines: int = 400
    max_function_lines: int = 80
    max_class_methods: int = 12
    max_public_api_per_module: int = 12
    max_new_runtime_dependencies_per_change: int = 1
    require_tests_for_changed_public_behavior: bool = True
    require_adr_for_new_abstraction_layer: bool = True
    disallow_circular_imports: bool = True
    discourage_global_mutable_state: bool = True


@dataclass
class AgenticIterationPolicy:
    enabled: bool = False
    require_goal_file: bool = False
    goal_file: str = ".cairndev/goal.yaml"
    max_iterations_without_human_review: int = 6
    require_verification_each_iteration: bool = True
    min_success_criteria: int = 1
    min_pause_triggers: int = 1


@dataclass
class GoalState:
    schema_version: str = "0.1"
    objective: str = ""
    status: GoalStatus | str = "active"
    current_iteration: int = 0
    last_verified_iteration: int = 0
    last_human_review_iteration: int = 0
    success_criteria: list[str] = field(default_factory=list)
    pause_triggers: list[str] = field(default_factory=list)


@dataclass
class DesignContract:
    schema_version: str = "0.1"
    project_name: str = "unknown"
    budgets: QualityBudget = field(default_factory=QualityBudget)
    agentic_iteration: AgenticIterationPolicy = field(
        default_factory=AgenticIterationPolicy
    )
    principles: dict[str, Any] = field(default_factory=dict)
    commands: dict[str, str] = field(default_factory=dict)
    review_checklist: list[str] = field(default_factory=list)

    @staticmethod
    def default(project_name: str = "unknown") -> "DesignContract":
        return DesignContract(project_name=project_name)


@dataclass(frozen=True)
class CheckReport:
    root: Path
    findings: list[Finding]

    @property
    def error_count(self) -> int:
        return sum(1 for item in self.findings if item.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for item in self.findings if item.severity == "warning")

    @property
    def passed(self) -> bool:
        return self.error_count == 0
