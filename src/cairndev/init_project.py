from __future__ import annotations

from pathlib import Path

DEFAULT_AGENTS = """# AGENTS.md - CairnDev Working Agreement

Before writing code, read `.cairndev/contract.yaml` and preserve the design contract.

Favor low coupling, high cohesion, concise self-explanatory variable names,
minimal dependencies, small files, explicit errors, deterministic tests, and
reversible changes.

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
  naming:
    description: "Variable names should be concise, self-explanatory, and free of vague filler."
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
  cross_platform_adaptivity:
    description: "User-facing interfaces should be designed for CLI, Windows, macOS, iOS, and Android adaptation without coupling business logic to a single platform."
    severity: warning

platform_targets:
  cli: true
  desktop:
    - Windows
    - macOS
  mobile:
    - iOS
    - Android
  expectations:
    - "Keep core domain logic independent from UI, OS, shell, filesystem path, and device assumptions."
    - "Expose reusable service/API contracts that can support CLI, desktop, and mobile clients."
    - "Use responsive layouts and adaptive interaction patterns for user-facing screens."
    - "Avoid platform-specific behavior unless isolated behind a narrow adapter."

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
  - "Are variable names concise and self-explanatory without hiding intent behind vague abbreviations?"
  - "Is the implementation minimal and reversible?"
  - "Are public behavior changes tested?"
  - "Does user-facing behavior remain adaptable across CLI, Windows, macOS, iOS, and Android?"
"""

DEFAULT_SKILL = """---
name: dev-quality-control
description: >
  Use before and during implementation when architecture quality, low coupling,
  extensibility, reusability, reliability, minimal code, clear variable naming,
  design review, or Codex task planning matters.
---

# Dev Quality Control Skill

## Purpose

Make the repository's design contract executable during implementation.
Do not rely on chat history or memory. Treat `AGENTS.md` and
`.cairndev/contract.yaml` as the source of truth for the current project.

## Required Discovery

Before editing non-trivial code:

1. Read `AGENTS.md`.
2. Read `.cairndev/contract.yaml` if present.
3. Inspect the local code paths that the task may touch.
4. Identify affected modules, public APIs, data boundaries, I/O boundaries,
   runtime dependencies, and expected test surface.
5. Identify new or changed names at public and data boundaries that must remain
   self-explanatory.
6. If the task changes architecture, extension points, or cross-module
   ownership, inspect existing ADRs before deciding.

## Implementation Plan

Before editing, provide a concise plan:

```text
Plan:
1. ...
2. ...

Design constraints:
- ...

Smallest viable change:
- ...

Tests:
- ...

Risks:
- ...
```

The plan must explicitly state whether the change adds or changes public
behavior, introduces an abstraction, adds a dependency, or crosses a module
boundary.

## Implementation Rules

- Prefer narrow functions, explicit data contracts, and clear module ownership.
- Use concise, self-explanatory variable names; avoid vague filler such as data,
  item, tmp, or obj in meaningful logic, and avoid nonstandard abbreviations
  unless the local domain makes them obvious.
- Keep I/O, domain logic, presentation, and orchestration separate.
- Do not introduce broad manager/orchestrator classes.
- Do not add runtime dependencies without a current, concrete need and explicit
  justification.
- Do not add an abstraction unless it removes real complexity or serves at
  least one current use.
- Preserve existing public APIs unless the task requires a breaking change.
- Cover public behavior changes with deterministic tests.
- Use explicit errors and actionable diagnostics instead of silent fallback.
- Keep edits scoped to the smallest reversible change that satisfies the task.
- If existing code violates the contract, fix only the part needed for the task
  unless the user asks for a broader refactor.

## Decision Gates

Stop and revise the plan, or ask the user when needed, if:

- the implementation would mix responsibilities across module boundaries;
- public behavior would change without tests;
- a new abstraction layer would be added without an ADR when the contract
  requires one;
- a new dependency is avoidable;
- new or changed names make the behavior hard to understand from names and
  types;
- the requested change conflicts with `AGENTS.md` or `.cairndev/contract.yaml`;
- verification cannot be run and the residual risk is material.

## Verification

After editing:

1. Run the project's declared test command when available.
2. Run `cairndev check .` when available.
3. If the `cairndev` executable is not installed, use the documented local
   module entry point when this repository provides one.
4. Fix failures or report a concrete reason they remain.

## Final Report

Summarize:

- files changed;
- design impact;
- tests and checks run;
- CairnDev findings or contract violations;
- naming issues or why none remain;
- dependency changes;
- ADR changes or why none were needed;
- remaining risks.
"""

DEFAULT_REVIEW_SKILL = """---
name: dev-quality-review
description: >
  Use after code changes or before a pull request to review architecture,
  coupling, cohesion, naming clarity, reliability, tests, dependency drift,
  minimalism, and contract compliance.
---

# Dev Quality Review Skill

## Purpose

Review a change against the repository's design contract. Treat review as a
blocking quality gate when the change violates reliability, coupling, API, or
test expectations.

## Required Discovery

1. Read `AGENTS.md`.
2. Read `.cairndev/contract.yaml` if present.
3. Inspect the changed files and relevant surrounding code.
4. Identify public API changes, new dependencies, new abstractions, data
   boundary changes, I/O boundary changes, naming clarity for nontrivial
   variables, and test coverage.
5. Run the declared test command and `cairndev check .` when available, unless
   the user only asked for a static review.

## Blocking Criteria

Request changes when any of these are true:

- public behavior changed without deterministic tests;
- module boundaries became less explicit or more circular;
- I/O, business logic, and presentation were mixed without justification;
- a broad manager/orchestrator object was introduced;
- a new dependency was added without a concrete current need;
- an abstraction was added for speculative future use;
- names are vague enough to obscure public behavior, data contracts, or
  reviewability;
- errors became silent, ambiguous, or hard to diagnose;
- the change violates a contract budget and does not justify the violation;
- verification failed and the failure is relevant to the change.

## Review Rubric

Evaluate each area as `pass`, `warn`, or `fail`, using concrete file and line
evidence:

```text
Coupling:
Cohesion:
Naming clarity:
Minimalism:
Reliability:
Testability:
Extensibility:
Dependency discipline:
Observability:
```

## Output Format

Lead with findings, ordered by severity:

```text
Blocking findings:
- ...

Non-blocking findings:
- ...

Open questions:
- ...

Verification:
- ...

Design summary:
- ...
```

If there are no blocking findings, say so clearly and still mention residual
test or design risk.
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
        (target / ".agents" / "skills" / "dev-quality-review" / "SKILL.md", DEFAULT_REVIEW_SKILL),
    ]
    for path, content in files:
        if path.exists() and not force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(path)
    return created
