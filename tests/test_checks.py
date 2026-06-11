from __future__ import annotations

from pathlib import Path

from cairndev.checks import iter_files, run_checks
from cairndev.init_project import init_project


def test_sample_project_passes_without_errors() -> None:
    root = Path(__file__).resolve().parents[1] / "examples" / "sample_project"
    report = run_checks(root)
    assert report.error_count == 0


def test_iter_files_prunes_ignored_directories(tmp_path: Path) -> None:
    kept = tmp_path / "src" / "kept.py"
    ignored = tmp_path / "node_modules" / "bad.py"
    kept.parent.mkdir()
    ignored.parent.mkdir()
    kept.write_text("x = 1\n", encoding="utf-8")
    ignored.write_text("this is not valid python", encoding="utf-8")

    files = {path.relative_to(tmp_path).as_posix() for path in iter_files(tmp_path)}
    assert files == {"src/kept.py"}

def test_missing_contract_warns(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "AGENTS.md").write_text("# ok\n", encoding="utf-8")
    report = run_checks(tmp_path)
    assert any(item.code == "missing_design_contract" for item in report.findings)


def test_init_project_creates_expected_files(tmp_path: Path) -> None:
    created = init_project(tmp_path)
    created_names = {path.relative_to(tmp_path).as_posix() for path in created}
    assert created_names == {
        "AGENTS.md",
        ".cairndev/adr/0001-architecture-contract.md",
        ".cairndev/contract.yaml",
        ".agents/skills/dev-quality-control/SKILL.md",
        ".agents/skills/dev-quality-review/SKILL.md",
    }
    contract = (tmp_path / ".cairndev" / "contract.yaml").read_text(encoding="utf-8")
    assert f'project_name: "{tmp_path.name}"' in contract


def test_init_project_is_idempotent_without_force(tmp_path: Path) -> None:
    init_project(tmp_path)
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# custom\n", encoding="utf-8")

    assert init_project(tmp_path) == []
    assert agents.read_text(encoding="utf-8") == "# custom\n"

    assert agents in init_project(tmp_path, force=True)
    assert "CairnDev Working Agreement" in agents.read_text(encoding="utf-8")


def test_python_budget_checks_respect_contract(tmp_path: Path) -> None:
    _write_project_contract(
        tmp_path,
        """
  max_function_lines: 3
  max_class_methods: 1
  max_public_api_per_module: 1
""",
    )
    (tmp_path / "module.py").write_text(
        """def first():
    x = 1
    y = 2
    return x + y


def second():
    return 1


class Wide:
    def one(self):
        return 1

    def two(self):
        return 2
""",
        encoding="utf-8",
    )

    codes = {item.code for item in run_checks(tmp_path).findings}
    assert "function_too_long" in codes
    assert "class_too_broad" in codes
    assert "too_many_public_symbols" in codes


def test_global_mutable_state_warns_for_lowercase_assignment(tmp_path: Path) -> None:
    _write_project_contract(tmp_path)
    (tmp_path / "state.py").write_text("cache = []\nCONSTANT = {}\n", encoding="utf-8")

    findings = [
        item for item in run_checks(tmp_path).findings if item.code == "global_mutable_state"
    ]
    assert len(findings) == 1
    assert findings[0].line == 1


def test_followup_marker_ignores_explanatory_prose(tmp_path: Path) -> None:
    _write_project_contract(tmp_path)
    (tmp_path / "notes.md").write_text(
        "This paragraph mentions TODO/FIXME as prose.\n"
        "- TODO: track this intentionally\n",
        encoding="utf-8",
    )

    findings = [item for item in run_checks(tmp_path).findings if item.code == "todo_marker"]
    assert len(findings) == 1
    assert findings[0].line == 2


def _write_project_contract(tmp_path: Path, budget_lines: str = "") -> None:
    (tmp_path / "AGENTS.md").write_text("# ok\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    contract_dir = tmp_path / ".cairndev"
    contract_dir.mkdir()
    contract_dir.joinpath("contract.yaml").write_text(
        f"""schema_version: "0.1"
project_name: "test-project"

budgets:{budget_lines or " {}"}
""",
        encoding="utf-8",
    )
