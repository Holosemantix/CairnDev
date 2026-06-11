# AGENTS.md — CairnDev Working Agreement

Use this file as persistent guidance for Codex and other coding agents.

## Core rule

Before writing code, preserve the design contract. After writing code, verify the design contract.

## Engineering taste

Favor:

- low coupling and explicit module boundaries;
- small files, small functions, and narrow public APIs;
- boring, reliable abstractions over clever indirection;
- typed data contracts at boundaries;
- deterministic tests and reproducible commands;
- explicit errors over silent fallback;
- minimal dependencies;
- readable names over comments that explain confusing code;
- incremental changes that are easy to review and revert.

Avoid:

- broad manager/orchestrator classes;
- hidden global state;
- circular imports;
- new dependencies without justification;
- speculative abstraction;
- mixing I/O, business logic, and presentation in one module;
- creating large files when a small module will do;
- changing public behavior without tests or docs.

## Required workflow

For every non-trivial task:

1. Read `.cairndev/contract.yaml` if present.
2. Identify affected modules and boundaries.
3. Produce a concise implementation plan.
4. Name the smallest viable change.
5. Implement with tests.
6. Run the project’s test/lint commands.
7. Run `cairndev check .` if available.
8. Summarize design impact and any contract violations.

## When uncertain

Prefer a smaller reversible implementation and leave an explicit TODO in an ADR or task note, not in production code.

