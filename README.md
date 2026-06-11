# CairnDev Quality Plugin

**Taste-preserving development control for agentic coding.**

CairnDev is not another AutoDev agent. It is a lightweight, agent-agnostic
quality-control layer for Codex, Claude Code, GitHub Copilot, OpenHands, Aider,
or human developers.

Its job is to make recurring engineering taste portable and partly
machine-checkable:

- persistent project instructions in `AGENTS.md`;
- a machine-readable design contract in `.cairndev/contract.yaml`;
- repo-local Codex skills under `.agents/skills/`;
- an optional Codex plugin scaffold under `plugins/cairndev-quality/`;
- deterministic local checks through the `cairndev` CLI;
- ADR, task, and PR review templates.

## Install Locally

```bash
pip install -e .
cairndev check .
cairndev summarize .
```

For development without installing the package first:

```bash
PYTHONPATH=src python -m cairndev.cli check .
PYTHONPATH=src python -m cairndev.cli summarize .
```

## Bootstrap A Project

```bash
cairndev init --target /path/to/project
```

This creates the repo-local contract bundle:

```text
AGENTS.md
.cairndev/contract.yaml
.cairndev/adr/0001-architecture-contract.md
.agents/skills/dev-quality-control/SKILL.md
```

Existing files are preserved by default. Use `--force` only when you want to
replace the existing CairnDev files.

## Validate This Repo

```bash
python -m compileall -q src tests
python -m pytest -q
PYTHONPATH=src python -m cairndev.cli check .
```

Expected self-check shape:

```text
CairnDev report for /path/to/CairnDev
Status: PASS
Errors: 0  Warnings: 0

No findings.
```

## Design Stance

Existing AI coding agents already generate code, fix bugs, run tests, create
PRs, and orchestrate workflows. CairnDev should not compete there. Its role is
to preserve architecture invariants and review taste across projects and agents.

The CLI is intentionally small. It is a first guardrail, not a replacement for
linters, tests, security review, or human judgment.
