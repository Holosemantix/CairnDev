# CairnDev Quality Plugin

**Taste-preserving development control for agentic coding.**

CairnDev is not another AutoDev agent. It is a lightweight, agent-agnostic
quality-control layer for Codex, Claude Code, GitHub Copilot, OpenHands, Aider,
or human developers.

Its job is to make recurring engineering taste portable and partly
machine-checkable:

- persistent project instructions in `AGENTS.md`;
- a machine-readable design contract in `.cairndev/contract.yaml`;
- durable multi-round goal state in `.cairndev/goal.yaml`;
- repo-local Codex skills under `.agents/skills/`;
- an optional Codex plugin scaffold under `plugins/cairndev-quality/`;
- deterministic local checks through the `cairndev` CLI;
- ADR, task, and PR review templates.

## Example Case Study

StockStudio is a live example of CairnDev guiding a larger product from final
specification to a tested scaffold and phased architecture:

- [StockStudio case study](docs/08_STOCKSTUDIO_CASE_STUDY.md)
- [Language standards baseline](docs/09_LANGUAGE_STANDARDS.md)

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
.cairndev/goal.yaml
.cairndev/adr/0001-architecture-contract.md
.agents/skills/dev-quality-control/SKILL.md
.agents/skills/dev-quality-review/SKILL.md
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

Naming clarity is part of the design contract: variables should be concise and
self-explanatory, not vague placeholders that need comments to explain intent.

For long-running automated work, CairnDev keeps the durable objective,
success criteria, verification iteration, and human pause triggers in
`.cairndev/goal.yaml`. See
[Continuous Agent Governance](docs/10_CONTINUOUS_AGENT_GOVERNANCE.md).
