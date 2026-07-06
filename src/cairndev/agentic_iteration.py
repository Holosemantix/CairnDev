from __future__ import annotations

from pathlib import Path

from .contract import load_goal_state
from .models import AgenticIterationPolicy, Finding, GoalState

VALID_GOAL_STATUSES = {"active", "paused", "blocked", "complete"}


def check_agentic_iteration_state(
    root: Path,
    policy: AgenticIterationPolicy,
) -> list[Finding]:
    if not policy.enabled:
        return []

    goal_file = Path(policy.goal_file)
    findings = _check_goal_file_path(goal_file, policy.goal_file)
    if findings:
        return findings

    goal_path = root / goal_file
    goal_rel = goal_file.as_posix()
    if policy.require_goal_file and not goal_path.exists():
        return [
            Finding(
                code="missing_goal_state",
                severity="error",
                message="Agentic iteration is enabled but the goal state file is missing.",
                path=goal_rel,
                suggestion="Create the goal state file or disable agentic_iteration.",
            )
        ]
    if not goal_path.exists():
        return []
    if not goal_path.is_file():
        return [
            Finding(
                code="invalid_goal_state_path",
                severity="error",
                message="Configured goal state path does not point to a file.",
                path=goal_rel,
                suggestion="Point agentic_iteration.goal_file at a YAML file.",
            )
        ]

    goal_state = load_goal_state(root, goal_rel)
    if goal_state is None:
        return []
    return _check_goal_state(root, goal_state, policy, goal_rel)


def _check_goal_file_path(goal_file: Path, raw_goal_file: str) -> list[Finding]:
    if goal_file.is_absolute() or ".." in goal_file.parts or not goal_file.name:
        return [
            Finding(
                code="invalid_goal_state_path",
                severity="error",
                message="agentic_iteration.goal_file must be a relative file path.",
                path=".cairndev/contract.yaml",
                suggestion=f"Use a repo-local file path instead of {raw_goal_file!r}.",
            )
        ]
    return []


def _check_goal_state(
    root: Path,
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> list[Finding]:
    findings: list[Finding] = []
    _extend_if_missing_goal_objective(findings, goal_state, goal_rel)
    _extend_if_invalid_goal_status(findings, goal_state, goal_rel)
    _extend_if_missing_goal_lists(findings, goal_state, policy, goal_rel)
    _extend_if_invalid_goal_iterations(findings, goal_state, policy, goal_rel)
    _extend_if_missing_verification_commands(findings, goal_state, policy, goal_rel)
    _extend_loop_engineering_findings(findings, root, goal_state, goal_rel)
    return findings


def _extend_if_missing_goal_objective(
    findings: list[Finding],
    goal_state: GoalState,
    goal_rel: str,
) -> None:
    if goal_state.objective.strip():
        return
    findings.append(
        Finding(
            code="missing_goal_objective",
            severity="error",
            message="Goal state objective is missing.",
            path=goal_rel,
            suggestion="Set objective to the durable outcome the agent should preserve.",
        )
    )


def _extend_if_invalid_goal_status(
    findings: list[Finding],
    goal_state: GoalState,
    goal_rel: str,
) -> None:
    if goal_state.status in VALID_GOAL_STATUSES:
        return
    findings.append(
        Finding(
            code="invalid_goal_status",
            severity="error",
            message=f"Goal status must be one of {sorted(VALID_GOAL_STATUSES)}.",
            path=goal_rel,
            suggestion="Use active, paused, blocked, or complete.",
        )
    )


def _extend_if_missing_goal_lists(
    findings: list[Finding],
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> None:
    success_criteria = [item for item in goal_state.success_criteria if item.strip()]
    pause_triggers = [item for item in goal_state.pause_triggers if item.strip()]
    if len(success_criteria) < policy.min_success_criteria:
        findings.append(
            Finding(
                code="missing_goal_success_criteria",
                severity="error",
                message="Goal state does not define enough success criteria.",
                path=goal_rel,
                suggestion="List concrete conditions that mean the long-running goal is met.",
            )
        )
    if len(pause_triggers) < policy.min_pause_triggers:
        findings.append(
            Finding(
                code="missing_goal_pause_triggers",
                severity="error",
                message="Goal state does not define enough human pause triggers.",
                path=goal_rel,
                suggestion="List conditions that require human review before continuing.",
            )
        )


def _extend_if_invalid_goal_iterations(
    findings: list[Finding],
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> None:
    if goal_state.current_iteration < 1:
        findings.append(
            Finding(
                code="invalid_goal_iteration",
                severity="error",
                message="current_iteration must be a positive integer.",
                path=goal_rel,
            )
        )
        return
    if goal_state.last_verified_iteration > goal_state.current_iteration:
        findings.append(
            Finding(
                code="invalid_goal_iteration",
                severity="error",
                message="last_verified_iteration cannot exceed current_iteration.",
                path=goal_rel,
            )
        )
    if goal_state.last_human_review_iteration > goal_state.current_iteration:
        findings.append(
            Finding(
                code="invalid_goal_iteration",
                severity="error",
                message="last_human_review_iteration cannot exceed current_iteration.",
                path=goal_rel,
            )
        )
    _extend_if_goal_needs_verification(findings, goal_state, policy, goal_rel)
    _extend_if_goal_needs_human_review(findings, goal_state, policy, goal_rel)


def _extend_if_goal_needs_verification(
    findings: list[Finding],
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> None:
    if not policy.require_verification_each_iteration:
        return
    if goal_state.last_verified_iteration >= goal_state.current_iteration:
        return
    findings.append(
        Finding(
            code="goal_iteration_unverified",
            severity="error",
            message="Current agentic iteration has not been marked verified.",
            path=goal_rel,
            suggestion="Run the required checks and update last_verified_iteration.",
        )
    )


def _extend_if_goal_needs_human_review(
    findings: list[Finding],
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> None:
    iterations_since_review = (
        goal_state.current_iteration - goal_state.last_human_review_iteration
    )
    if iterations_since_review <= policy.max_iterations_without_human_review:
        return
    findings.append(
        Finding(
            code="goal_human_review_due",
            severity="error",
            message="Agentic iteration has exceeded the human review interval.",
            path=goal_rel,
            suggestion="Pause for human review or update last_human_review_iteration.",
        )
    )


def _extend_if_missing_verification_commands(
    findings: list[Finding],
    goal_state: GoalState,
    policy: AgenticIterationPolicy,
    goal_rel: str,
) -> None:
    if not policy.require_verification_each_iteration:
        return
    if goal_state.verification_required_commands:
        return
    findings.append(
        Finding(
            code="missing_goal_verification_commands",
            severity="warning",
            message="Goal state does not list required verification commands.",
            path=goal_rel,
            suggestion="Add verification.required_commands to the goal state.",
        )
    )


def _extend_loop_engineering_findings(
    findings: list[Finding],
    root: Path,
    goal_state: GoalState,
    goal_rel: str,
) -> None:
    loop_state = goal_state.loop_engineering
    if loop_state.trajectory_file is not None:
        _extend_missing_repo_file(
            findings,
            root,
            loop_state.trajectory_file,
            goal_rel,
            "missing_loop_trajectory",
            "Configured loop trajectory file is missing.",
        )
    for checkpoint_file in loop_state.checkpoint_files:
        _extend_missing_repo_file(
            findings,
            root,
            checkpoint_file,
            goal_rel,
            "missing_loop_checkpoint",
            "Configured loop checkpoint file is missing.",
        )
    for skill_name in loop_state.required_skills:
        _extend_missing_loop_skill(findings, root, skill_name, goal_rel)


def _extend_missing_repo_file(
    findings: list[Finding],
    root: Path,
    repo_file: str,
    goal_rel: str,
    code: str,
    message: str,
) -> None:
    path = Path(repo_file)
    if _invalid_repo_path(path) or not (root / path).is_file():
        findings.append(
            Finding(
                code=code,
                severity="error",
                message=message,
                path=goal_rel,
                suggestion=f"Create {repo_file!r} or remove it from loop_engineering.",
            )
        )


def _extend_missing_loop_skill(
    findings: list[Finding],
    root: Path,
    skill_name: str,
    goal_rel: str,
) -> None:
    skill_path = Path(".agents") / "skills" / skill_name / "SKILL.md"
    if _invalid_repo_path(skill_path) or not (root / skill_path).is_file():
        findings.append(
            Finding(
                code="missing_loop_skill",
                severity="error",
                message=f"Configured loop engineering skill is missing: {skill_name}.",
                path=goal_rel,
                suggestion=f"Create {skill_path.as_posix()} or remove it from the goal.",
            )
        )


def _invalid_repo_path(path: Path) -> bool:
    return path.is_absolute() or ".." in path.parts or not path.name
