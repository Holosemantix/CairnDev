---
name: dev-quality-control
description: Use for software development tasks that must preserve architecture quality, low coupling, extensibility, reusability, reliability, and minimal code. Trigger before coding, refactoring, PR review, or design-sensitive implementation.
---

# Dev Quality Control Skill

## Purpose

Help Codex implement software changes while preserving the repo's design contract.

## Required workflow

1. Read `AGENTS.md`.
2. Read `.cairndev/contract.yaml` if present.
3. Identify affected modules and public APIs.
4. Propose the smallest viable implementation plan.
5. Implement with tests.
6. Run the project's test command.
7. Run `cairndev check .` if available.
8. Summarize:
   - files changed;
   - design impact;
   - tests run;
   - CairnDev violations;
   - dependency changes;
   - any ADR needed.

## Design rules

- Prefer narrow functions and explicit data boundaries.
- Avoid speculative layers.
- Do not add runtime dependencies without justification.
- Keep I/O, domain logic, and presentation separate.
- Preserve existing public APIs unless the task explicitly requires a breaking change.
- When changing architecture, add or update an ADR.
- If a quality check fails, fix it or provide a clear justification.

## Output format for implementation plan

```text
Plan:
1. ...
2. ...

Design constraints:
- ...

Tests:
- ...

Risks:
- ...
```
