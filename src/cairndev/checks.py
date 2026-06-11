from __future__ import annotations

import ast
import os
from pathlib import Path

from .contract import load_contract
from .models import CheckReport, Finding, QualityBudget

IGNORED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "venv",
    "__pycache__",
}
MUTABLE_NODE_TYPES = (ast.List, ast.Dict, ast.Set)
FOLLOWUP_MARKERS = ("TO" + "DO", "FIX" + "ME")
COMMENT_PREFIXES = ("#", "//", "/*", "*", "<!--", "-")


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORED_DIRS)
        current_path = Path(current)
        for filename in sorted(filenames):
            path = current_path / filename
            if path.is_file():
                files.append(path)
    return files


def run_checks(root: Path) -> CheckReport:
    root = root.resolve()
    contract = load_contract(root)
    findings: list[Finding] = []

    if not (root / "AGENTS.md").exists():
        findings.append(
            Finding(
                code="missing_agents_md",
                severity="warning",
                message="AGENTS.md is missing; Codex may not load persistent project guidance.",
                path="AGENTS.md",
                suggestion="Add AGENTS.md with repository expectations.",
            )
        )

    if not (root / ".cairndev" / "contract.yaml").exists():
        findings.append(
            Finding(
                code="missing_design_contract",
                severity="warning",
                message=".cairndev/contract.yaml is missing; using default quality budgets.",
                path=".cairndev/contract.yaml",
                suggestion="Run cairndev init or add a design contract.",
            )
        )

    if not (root / "tests").exists():
        findings.append(
            Finding(
                code="missing_tests_dir",
                severity="warning",
                message="tests/ directory is missing.",
                path="tests",
                suggestion="Add tests for public behavior.",
            )
        )

    for file_path in iter_files(root):
        rel = str(file_path.relative_to(root))
        if file_path.suffix == ".py":
            findings.extend(_check_python_file(root, file_path, contract.budgets))
        if file_path.suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".md"}:
            findings.extend(_check_todo_markers(root, file_path))
        if _is_large_dependency_manifest(file_path):
            findings.append(
                Finding(
                    code="large_dependency_manifest",
                    severity="warning",
                    message="Dependency manifest is unusually large.",
                    path=rel,
                )
            )

    return CheckReport(root=root, findings=findings)


def _is_large_dependency_manifest(file_path: Path) -> bool:
    manifests = {"package.json", "pyproject.toml", "requirements.txt"}
    return file_path.name in manifests and file_path.stat().st_size > 200_000


def _check_todo_markers(root: Path, file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return findings
    rel = str(file_path.relative_to(root))
    for index, line in enumerate(lines, start=1):
        if _has_followup_marker(line):
            findings.append(
                Finding(
                    code="todo_marker",
                    severity="info",
                    message="TODO/FIXME marker found; ensure follow-up is tracked intentionally.",
                    path=rel,
                    line=index,
                )
            )
    return findings


def _has_followup_marker(line: str) -> bool:
    stripped = line.lstrip()
    for prefix in COMMENT_PREFIXES:
        if stripped.startswith(prefix):
            remainder = stripped.removeprefix(prefix).lstrip(" :-*")
            upper = remainder.upper()
            return any(upper.startswith(marker) for marker in FOLLOWUP_MARKERS)
    upper = stripped.upper()
    return any(upper == marker or upper.startswith(f"{marker}:") for marker in FOLLOWUP_MARKERS)


def _check_python_file(root: Path, file_path: Path, budgets: QualityBudget) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(file_path.relative_to(root))
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    lines = text.splitlines()
    if len(lines) > budgets.max_python_file_lines:
        findings.append(
            Finding(
                code="python_file_too_long",
                severity="warning",
                message=(
                    f"Python file has {len(lines)} lines; "
                    f"budget is {budgets.max_python_file_lines}."
                ),
                path=rel,
                suggestion="Split responsibilities into smaller modules.",
            )
        )
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        findings.append(
            Finding(
                code="python_syntax_error",
                severity="error",
                message=str(exc),
                path=rel,
                line=exc.lineno,
            )
        )
        return findings

    public_api = 0
    for node in tree.body:
        if _is_public_symbol(node):
            public_api += 1
    if public_api > budgets.max_public_api_per_module:
        findings.append(
            Finding(
                code="too_many_public_symbols",
                severity="warning",
                message=(
                    f"Module exposes {public_api} public symbols; "
                    f"budget is {budgets.max_public_api_per_module}."
                ),
                path=rel,
                suggestion="Narrow the module API or split responsibilities.",
            )
        )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            findings.extend(_check_function_length(node, budgets, rel))
        if isinstance(node, ast.ClassDef):
            findings.extend(_check_class_width(node, budgets, rel))

    if budgets.discourage_global_mutable_state:
        findings.extend(_check_global_mutable_state(tree, rel))
    return findings


def _is_public_symbol(ast_node: ast.AST) -> bool:
    public_types = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    return isinstance(ast_node, public_types) and not ast_node.name.startswith("_")


def _check_function_length(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    budgets: QualityBudget,
    rel: str,
) -> list[Finding]:
    end = getattr(node, "end_lineno", node.lineno)
    length = end - node.lineno + 1
    if length <= budgets.max_function_lines:
        return []
    return [
        Finding(
            code="function_too_long",
            severity="warning",
            message=(
                f"Function {node.name} has {length} lines; "
                f"budget is {budgets.max_function_lines}."
            ),
            path=rel,
            line=node.lineno,
            suggestion="Extract cohesive helper functions.",
        )
    ]


def _check_class_width(node: ast.ClassDef, budgets: QualityBudget, rel: str) -> list[Finding]:
    methods = [
        child
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if len(methods) <= budgets.max_class_methods:
        return []
    return [
        Finding(
            code="class_too_broad",
            severity="warning",
            message=(
                f"Class {node.name} has {len(methods)} methods; "
                f"budget is {budgets.max_class_methods}."
            ),
            path=rel,
            line=node.lineno,
            suggestion="Split broad responsibilities.",
        )
    ]


def _check_global_mutable_state(tree: ast.Module, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, MUTABLE_NODE_TYPES):
            continue
        target_names = [getattr(target, "id", "") for target in node.targets]
        if any(name.isupper() for name in target_names):
            continue
        findings.append(
            Finding(
                code="global_mutable_state",
                severity="warning",
                message="Potential global mutable state at module level.",
                path=rel,
                line=node.lineno,
                suggestion="Prefer immutable constants or explicit state containers.",
            )
        )
    return findings
