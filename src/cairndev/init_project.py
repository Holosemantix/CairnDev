from __future__ import annotations

from pathlib import Path

DEFAULT_AGENTS = """# AGENTS.md - CairnDev Working Agreement

Before writing code, read `.cairndev/contract.yaml` and preserve the design contract.

Favor low coupling, high cohesion, minimal dependencies, small files, explicit errors,
deterministic tests, and reversible changes.

After coding, run the test command and `cairndev check .` if available.
"""

DEFAULT_CONTRACT_TEMPLATE = """schema_version: "0.1"
project_name: "{project_name}"

principles:
  low_coupling:
    description: "Modules should expose narrow APIs and avoid circular dependencies."
    severity: error
  high_cohesion:
    description: "A file/module should have one clear responsibility."
    severity: warning
  minimalism:
    description: "Prefer the smallest correct implementation; avoid speculative layers."
    severity: warning
  reliability:
    description: "Public behavior should be covered by deterministic tests."
    severity: error
  extensibility:
    description: "Extension points should be explicit and justified by current needs."
    severity: warning
  reusability:
    description: "Shared logic should be factored only after at least two real uses."
    severity: warning
  observability:
    description: "Errors should be explicit and diagnostics should be actionable."
    severity: warning

budgets:
  max_python_file_lines: 400
  max_function_lines: 80
  max_class_methods: 12
  max_public_api_per_module: 12
  max_new_runtime_dependencies_per_change: 1
  require_tests_for_changed_public_behavior: true
  require_adr_for_new_abstraction_layer: true
  disallow_circular_imports: true
  discourage_global_mutable_state: true

commands:
  test: "pytest -q"
  quality_check: "cairndev check ."

review_checklist:
  - "Does this change preserve low coupling?"
  - "Is the implementation minimal and reversible?"
  - "Are public behavior changes tested?"
"""

DEFAULT_SKILL = """---
name: dev-quality-control
description: Use for design-sensitive implementation, refactoring, and review tasks.
---

Read AGENTS.md and .cairndev/contract.yaml before coding.
Plan the smallest viable change, implement with tests, run the test command,
run cairndev check ., and summarize design impact.
"""

DEFAULT_ADR = """# ADR 0001: Architecture Contract as a First-Class Development Artifact

Status: accepted

## Context

Agentic coding tools can implement changes quickly, but project-level design taste is often
repeated manually in prompts. The same preferences should be versioned with the repository
instead of restated in every task.

## Decision

Represent engineering taste as a repo-local, machine-readable design contract in
`.cairndev/contract.yaml`, plus human-readable instructions in `AGENTS.md` and a reusable
Codex skill.

## Consequences

- Agents can read the same contract before every task.
- A CLI can check a subset of the contract deterministically.
- Human review can focus on meaningful architectural tradeoffs.
- The contract must remain small enough to be read and followed.
"""


def init_project(target: Path, force: bool = False) -> list[Path]:
    target = target.resolve()
    created: list[Path] = []
    files = [
        (target / "AGENTS.md", DEFAULT_AGENTS),
        (
            target / ".cairndev" / "contract.yaml",
            DEFAULT_CONTRACT_TEMPLATE.format(project_name=target.name),
        ),
        (target / ".cairndev" / "adr" / "0001-architecture-contract.md", DEFAULT_ADR),
        (target / ".agents" / "skills" / "dev-quality-control" / "SKILL.md", DEFAULT_SKILL),
    ]
    for path, content in files:
        if path.exists() and not force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(path)
    return created
