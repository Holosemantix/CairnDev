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
- language-native style and tooling standards over custom house style;
- platform-adaptive user-facing interfaces across CLI, Windows, macOS, iOS, and Android;
- minimal dependencies;
- concise, self-explanatory variable names over vague abbreviations or comment-dependent code;
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
- binding business/domain logic directly to one UI toolkit, OS, shell, or device form factor.
- overriding established language style guides without a project-specific reason.

## Required workflow

For every non-trivial task:

1. Read `.cairndev/contract.yaml` if present.
2. Identify affected modules and boundaries.
3. Produce a concise implementation plan.
4. Name the smallest viable change.
5. Implement with tests.
6. Run the project’s test/lint commands.
7. Run `cairndev check .` if available.
8. Run configured language formatters/linters/type checkers when available.
9. Summarize design impact and any contract violations.

## When uncertain

Prefer a smaller reversible implementation and leave an explicit TODO in an ADR or task note, not in production code.

## Language Standards

Use the target language ecosystem's official or widely adopted style guides and
tooling as the baseline. CairnDev does not replace PEP 8, Ruff, TypeScript,
Effective Go, Google Java Style, Swift API Design Guidelines, or similar
language-native standards; it adds architecture and design-contract checks on
top. See `docs/09_LANGUAGE_STANDARDS.md`.
