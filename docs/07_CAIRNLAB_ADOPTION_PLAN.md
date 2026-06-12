# CairnLab Adoption Plan

## Status

CairnDev is ready to use for day-to-day development in `../CairnLab`.

The current working system has three active layers:

```text
AGENTS.md + .cairndev/contract.yaml
  Persistent project constraints and machine-readable budgets.

.dev / review repo-local skills
  Agent execution protocol for planning, implementation, and review.

cairndev check
  Deterministic guardrail for required artifacts and measurable code drift.
```

This is enough to guide Codex on CairnLab tasks now. It is not yet a fully
non-bypassable CI gate; that comes later.

## What Is Already Proven

The CairnLab A/B validation showed the important difference:

- without CairnDev, a feature passed tests while mixing explanation behavior into
  the CLI layer;
- with CairnDev, the same feature kept CLI as I/O, added a small typed
  explanation module, updated design docs, and added broader tests;
- `dev-quality-review` caught the architectural issue that ordinary tests and
  simple static checks did not catch.

The validation is recorded in:

```text
docs/06_CAIRNLAB_AB_VALIDATION.md
templates/VALIDATION_SCORECARD.md
```

## How To Use It In CairnLab

For each non-trivial CairnLab task, use this workflow:

```text
1. Read CairnLab AGENTS.md.
2. Read CairnLab .cairndev/contract.yaml.
3. Use dev-quality-control before and during implementation.
4. Identify affected modules, public APIs, data boundaries, I/O boundaries, and tests.
5. Implement the smallest viable change.
6. Run CairnLab tests.
7. Run CairnDev check against CairnLab.
8. Use dev-quality-review before commit or PR.
```

The expected commands are:

```bash
cd /opt/workspace/explorer-env/dataset/ag_data/code/CairnLab
python -m pytest -q
PYTHONPATH=/opt/workspace/explorer-env/dataset/ag_data/code/CairnDev/src python -m cairndev.cli check .
```

If `cairndev` is installed globally, the second command can be replaced with:

```bash
cairndev check .
```

## CairnLab-Specific Boundaries

CairnLab should keep these boundaries explicit:

```text
models
  portable data contracts only

authority
  deterministic allowed/blocked transition decisions

transition_explain
  render or package TransitionDecision output; never decide semantics

cli
  command facade only: parse, call public APIs, render

adapters
  translate external metadata into ClaimCase; never decide lifecycle authority
```

Any CairnLab change that touches CLI commands, transition semantics, adapter
contracts, storage layout, or public model fields should update the matching
`docs/design/modules/*` document in the same change.

## Next Execution Queue

### 1. Use CairnDev For The Next Real CairnLab Feature

Recommended task:

```text
Extend transition explain with an allowed-path fixture and README-style example.
```

Acceptance:

- CLI remains thin;
- explanation behavior stays in `transition_explain.py`;
- tests cover allowed and blocked paths;
- design docs are updated if command behavior changes;
- `pytest` and `cairndev check` pass.

### 2. Add CI Or Pre-Commit Enforcement

Goal: make the deterministic layer harder to skip.

Minimal version:

```text
python -m pytest -q
PYTHONPATH=/path/to/CairnDev/src python -m cairndev.cli check .
```

This should run in either a local script, pre-commit hook, or GitHub Actions
workflow. Keep it simple until the workflow proves useful.

### 3. Improve CairnDev Contract Precision

CairnLab currently uses legacy-tolerant budgets because it already has large
adapter and model modules. The next CairnDev improvement should support
path-specific budget overrides or known-debt exemptions so new code can remain
strict without forcing immediate refactors of historical modules.

Acceptance:

- contract can declare path-specific budgets;
- legacy files can be tracked as known debt;
- new files still use strict defaults;
- tests cover default and path-specific behavior.

### 4. Run Two More A/B Validations

Use the scorecard on two different project types:

```text
1. A small CLI or web app.
2. A game/app prototype or OpenClaw-adjacent plugin.
```

Acceptance:

- both validations compare with/without CairnDev;
- `dev-quality-review` findings are recorded;
- repeated misses become either skill changes or deterministic checks.

## Current Limitations

CairnDev is usable, but the following are still open:

- skills guide agent behavior but do not by themselves block commits;
- `cairndev check` is deterministic and intentionally shallow;
- global `cairndev` may not be installed in every environment, so development
  mode may still be needed;
- path-specific contract tuning is not implemented yet.

These limitations are acceptable for current CairnLab development because the
agent workflow, review workflow, and deterministic check are already present and
validated.

## Decision

Use CairnDev as the default development workflow for `../CairnLab` starting now.

Do not wait for CI or path-specific budgets before using it. Those are the next
hardening steps, not prerequisites for day-to-day use.
