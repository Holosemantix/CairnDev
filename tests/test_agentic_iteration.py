from __future__ import annotations

from pathlib import Path

from cairndev.checks import run_checks
from cairndev.init_project import init_project


def test_agentic_iteration_requires_goal_state_when_enabled(tmp_path: Path) -> None:
    _write_agentic_project(tmp_path)

    codes = _finding_codes(tmp_path)

    assert "missing_goal_state" in codes


def test_agentic_iteration_requires_verified_current_iteration(tmp_path: Path) -> None:
    _write_agentic_project(tmp_path)
    _write_goal_state(
        tmp_path,
        current_iteration=2,
        last_verified_iteration=1,
        last_human_review_iteration=2,
    )

    codes = _finding_codes(tmp_path)

    assert "goal_iteration_unverified" in codes


def test_agentic_iteration_requires_human_review_within_budget(tmp_path: Path) -> None:
    _write_agentic_project(tmp_path, max_iterations_without_human_review=2)
    _write_goal_state(
        tmp_path,
        current_iteration=5,
        last_verified_iteration=5,
        last_human_review_iteration=2,
    )

    codes = _finding_codes(tmp_path)

    assert "goal_human_review_due" in codes


def test_agentic_iteration_checks_declared_loop_files(tmp_path: Path) -> None:
    _write_agentic_project(tmp_path)
    _write_goal_state(
        tmp_path,
        current_iteration=2,
        last_verified_iteration=2,
        last_human_review_iteration=2,
        loop_engineering="""loop_engineering:
  trajectory_file: ".cairndev/missing-loop.md"
  checkpoint_files:
    - ".cairndev/missing-checkpoint.yaml"
""",
    )

    codes = _finding_codes(tmp_path)

    assert "missing_loop_trajectory" in codes
    assert "missing_loop_checkpoint" in codes


def test_agentic_iteration_checks_declared_loop_skills(tmp_path: Path) -> None:
    _write_agentic_project(tmp_path)
    _write_goal_state(
        tmp_path,
        current_iteration=2,
        last_verified_iteration=2,
        last_human_review_iteration=2,
        loop_engineering="""loop_engineering:
  required_skills:
    - "missing-loop-skill"
""",
    )

    codes = _finding_codes(tmp_path)

    assert "missing_loop_skill" in codes


def test_init_project_agentic_iteration_state_passes_checks(tmp_path: Path) -> None:
    init_project(tmp_path)
    (tmp_path / "tests").mkdir()

    report = run_checks(tmp_path)

    assert report.error_count == 0


def _finding_codes(tmp_path: Path) -> set[str]:
    return {finding.code for finding in run_checks(tmp_path).findings}


def _write_agentic_project(
    tmp_path: Path,
    max_iterations_without_human_review: int = 6,
) -> None:
    (tmp_path / "AGENTS.md").write_text("# ok\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    _write_agent_skill(tmp_path, "dev-quality-control")
    _write_agent_skill(tmp_path, "dev-quality-review")
    contract_dir = tmp_path / ".cairndev"
    contract_dir.mkdir()
    contract_dir.joinpath("contract.yaml").write_text(
        f"""schema_version: "0.1"
project_name: "test-project"

budgets: {{}}

agentic_iteration:
  enabled: true
  require_goal_file: true
  goal_file: ".cairndev/goal.yaml"
  max_iterations_without_human_review: {max_iterations_without_human_review}
  require_verification_each_iteration: true
  min_success_criteria: 1
  min_pause_triggers: 1
""",
        encoding="utf-8",
    )


def _write_goal_state(
    tmp_path: Path,
    current_iteration: int,
    last_verified_iteration: int,
    last_human_review_iteration: int,
    loop_engineering: str = "",
) -> None:
    tmp_path.joinpath(".cairndev", "goal.yaml").write_text(
        f"""schema_version: "0.1"
objective: "Build the service."
status: active
current_iteration: {current_iteration}
last_verified_iteration: {last_verified_iteration}
last_human_review_iteration: {last_human_review_iteration}
success_criteria:
  - "End-to-end path works."
pause_triggers:
  - "Scope changes."
verification:
  required_commands:
    - "pytest -q"
{loop_engineering}
""",
        encoding="utf-8",
    )


def _write_agent_skill(tmp_path: Path, skill_name: str) -> None:
    path = tmp_path / ".agents" / "skills" / skill_name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nname: {skill_name}\n---\n", encoding="utf-8")
