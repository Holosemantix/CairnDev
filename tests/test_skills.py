from __future__ import annotations

from pathlib import Path

from cairndev.init_project import init_project


ROOT = Path(__file__).resolve().parents[1]


def test_repo_and_plugin_control_skills_are_in_sync() -> None:
    repo_skill = ROOT / ".agents" / "skills" / "dev-quality-control" / "SKILL.md"
    plugin_skill = (
        ROOT / "plugins" / "cairndev-quality" / "skills" / "dev-quality-control" / "SKILL.md"
    )

    assert repo_skill.read_text(encoding="utf-8") == plugin_skill.read_text(encoding="utf-8")


def test_repo_and_plugin_review_skills_are_in_sync() -> None:
    repo_skill = ROOT / ".agents" / "skills" / "dev-quality-review" / "SKILL.md"
    plugin_skill = (
        ROOT / "plugins" / "cairndev-quality" / "skills" / "dev-quality-review" / "SKILL.md"
    )

    assert repo_skill.read_text(encoding="utf-8") == plugin_skill.read_text(encoding="utf-8")


def test_control_skill_contains_executable_agent_protocol() -> None:
    skill = (ROOT / ".agents" / "skills" / "dev-quality-control" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    required = [
        "Do not rely on chat history or memory.",
        ".cairndev/goal.yaml",
        "Identify affected modules, public APIs, data boundaries, I/O boundaries",
        "Smallest viable change:",
        "The plan must explicitly state whether the change adds or changes public",
        "concise, self-explanatory variable names",
        "## Decision Gates",
        "new or changed names make the behavior hard to understand",
        "Run `cairndev check .` when available.",
        "current iteration, and pause state",
    ]
    for text in required:
        assert text in skill


def test_review_skill_defines_blocking_quality_gate() -> None:
    skill = (
        ROOT / "plugins" / "cairndev-quality" / "skills" / "dev-quality-review" / "SKILL.md"
    ).read_text(encoding="utf-8")

    required = [
        "blocking quality gate",
        ".cairndev/goal.yaml",
        "## Blocking Criteria",
        "public behavior changed without deterministic tests",
        "names are vague enough to obscure public behavior",
        "Naming clarity:",
        "Dependency discipline:",
        "Lead with findings, ordered by severity",
        "beyond its human-review interval",
    ]
    for text in required:
        assert text in skill


def test_init_project_writes_executable_control_skill(tmp_path: Path) -> None:
    init_project(tmp_path)
    skill = (tmp_path / ".agents" / "skills" / "dev-quality-control" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "Do not rely on chat history or memory." in skill
    assert ".cairndev/goal.yaml" in skill
    assert "## Required Discovery" in skill
    assert "concise, self-explanatory variable names" in skill
    assert "## Decision Gates" in skill
    assert "Run `cairndev check .` when available." in skill
    assert "current iteration, and pause state" in skill


def test_init_project_writes_executable_review_skill(tmp_path: Path) -> None:
    init_project(tmp_path)
    skill = (tmp_path / ".agents" / "skills" / "dev-quality-review" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "blocking quality gate" in skill
    assert ".cairndev/goal.yaml" in skill
    assert "## Blocking Criteria" in skill
    assert "Naming clarity:" in skill
    assert "Lead with findings, ordered by severity" in skill
