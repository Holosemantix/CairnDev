# CairnLab A/B Validation

## Question

Does CairnDev improve agent implementation quality beyond ordinary tests and
simple static rules?

## Task

Both variants implemented the same CairnLab feature:

```text
Add `cairn transition explain`, a plan-only command that explains whether a
claim lifecycle transition would be allowed or blocked, including current state,
requested state, blocking reasons, required actions, and proposed event type.
```

This task intentionally touches three surfaces:

- I/O: Typer CLI text and JSON output;
- business boundary: converting `TransitionDecision` into a stable explanation;
- tests: CLI behavior, plan-only behavior, and explanation behavior.

It is a useful validation task because a careless implementation can pass tests
while still mixing CLI rendering, explanation formatting, and transition logic.

## Setup

Two temporary copies of CairnLab were created:

```text
without_cairndev: no `.cairndev/contract.yaml`, no repo-local skills
with_cairndev: initialized with CairnDev contract and dev/review skills
```

The `with_cairndev` variant used:

```text
.agents/skills/dev-quality-control/SKILL.md
.agents/skills/dev-quality-review/SKILL.md
.cairndev/contract.yaml
```

## Functional Result

Both implementations passed ordinary project checks.

```text
without_cairndev:
python -m compileall -q src tests
python -m pytest -q
65 passed

after CairnDev guidance:
python -m compileall -q src tests
python -m pytest -q
67 passed
```

This matters: ordinary tests alone did not prove the better architecture.

## Static Check Result

`cairndev check` found hard, deterministic differences:

```text
without_cairndev:
Status: PASS
Warnings: 21
Key warning: missing_design_contract

with_cairndev:
Status: PASS
Warnings: 20
Key difference: contract and repo-local skills present
```

The deterministic checker caught missing project-level CairnDev artifacts. It did
not directly judge whether the CLI mixed responsibilities; that is the job of the
agent review protocol.

## Review Result

### Without CairnDev

The implementation passed tests but put explanation construction, payload
building, text rendering, event-type extraction, and summary rules directly in
`src/cairnlab/cli.py`.

`dev-quality-review` would request changes because:

- the CLI stopped being a thin command facade;
- reusable explanation behavior had no module boundary;
- design docs were not updated for a new CLI command;
- tests covered only the CLI JSON path, not reusable explanation behavior or
  text rendering;
- future agents had no machine-readable contract or repo-local review skill.

Rubric:

```text
Coupling: fail
Cohesion: fail
Minimalism: warn
Reliability: warn
Testability: warn
Extensibility: fail
Dependency discipline: pass
Observability: warn
```

### With CairnDev

The accepted implementation split responsibilities:

```text
src/cairnlab/transition_explain.py   typed explanation and rendering
src/cairnlab/cli.py                  thin command facade
docs/design/modules/cli_surface.md   documented command and plan-only behavior
docs/design/modules/transition_authority.md clarified authority boundary
tests/test_transition_explain.py     pure logic + JSON/text CLI tests
```

Rubric:

```text
Coupling: pass
Cohesion: pass
Minimalism: pass
Reliability: pass
Testability: pass
Extensibility: pass
Dependency discipline: pass
Observability: pass
```

## Conclusion

The validation supports CairnDev's intended role:

- `dev-quality-control` improves how the agent plans and implements changes.
- `dev-quality-review` catches architecture problems that tests and simple
  static checks miss.
- `cairndev check` verifies hard prerequisites such as contract and skill
  presence, plus measurable code-budget drift.

CairnDev is therefore not just a linter. It is a small system of persistent
project constraints, agent execution protocols, review protocols, and
deterministic guardrails.

## Next Validation

Run the same scorecard on at least two more projects or feature types:

```text
1. A small web app or CLI tool.
2. A game/app prototype or OpenClaw-adjacent plugin.
```

Each validation should compare:

- plan quality;
- boundary preservation;
- tests added;
- dependency drift;
- review findings;
- whether the user had to restate engineering taste manually.
