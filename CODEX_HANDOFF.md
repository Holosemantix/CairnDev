# Codex Handoff: CairnDev Quality Plugin

## Objective

Build a reusable quality-control plugin for agentic software development. The plugin should help Codex and other AI coding tools preserve high-quality architecture across projects: low coupling, high cohesion, extensibility, reusability, reliability, minimalism, testability, and small readable code.

## Important non-goals

Do not build another autonomous coding agent. Do not build an IDE. Do not implement a web app generator. Do not replace Codex, Claude Code, Copilot, OpenHands, Aider, SWE-agent, or MetaGPT.

## Phase 0 deliverable

Make this repo installable and useful as a local guardrail:

```bash
pip install -e .
cairndev check .
cairndev summarize .
pytest -q
```

## Phase 1 deliverable

Make it easy to drop into any project:

```bash
cairndev init --target /path/to/project
```

This should copy or generate:

```text
AGENTS.md
.cairndev/contract.yaml
.cairndev/adr/0001-architecture-contract.md
.agents/skills/dev-quality-control/SKILL.md
```

## Phase 2 deliverable

Create a valid Codex plugin folder from `plugins/cairndev-quality/` and verify that the local marketplace entry in `.agents/plugins/marketplace.json` points to it.

## Core implementation tasks

1. Finish `src/cairndev/models.py`.
2. Finish `src/cairndev/checks.py`.
3. Finish `src/cairndev/cli.py`.
4. Add tests for all default checks.
5. Ensure generated files are deterministic.
6. Keep dependencies minimal.
7. Update README with exact commands and sample output.

## Acceptance criteria

The following should pass in a fresh clone:

```bash
python -m compileall src
pip install -e .
pytest -q
cairndev check examples/sample_project
cairndev summarize examples/sample_project
```

## Design invariant

CairnDev must be strict enough to shape Codex behavior, but simple enough not to become a heavyweight framework.

