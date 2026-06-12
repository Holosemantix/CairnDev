# CairnDev Validation Scorecard

## Validation Task

```text
Describe the same implementation task used in both variants.
```

## Variants

| Variant | Path or commit | CairnDev artifacts | Notes |
| --- | --- | --- | --- |
| Without CairnDev |  | No contract or repo-local skills |  |
| With CairnDev |  | `AGENTS.md`, `.cairndev/contract.yaml`, dev/review skills |  |

## Functional Checks

| Check | Without CairnDev | With CairnDev |
| --- | --- | --- |
| Compile/type/syntax check |  |  |
| Project tests |  |  |
| `cairndev check` |  |  |
| Diff whitespace check |  |  |

## Implementation Shape

| Metric | Without CairnDev | With CairnDev |
| --- | --- | --- |
| Files changed |  |  |
| Lines changed |  |  |
| Tests added |  |  |
| Runtime dependencies added |  |  |
| Design docs updated |  |  |
| Public API changed |  |  |

## Boundary Review

| Review area | Without CairnDev | With CairnDev |
| --- | --- | --- |
| Coupling | pass/warn/fail | pass/warn/fail |
| Cohesion | pass/warn/fail | pass/warn/fail |
| Minimalism | pass/warn/fail | pass/warn/fail |
| Reliability | pass/warn/fail | pass/warn/fail |
| Testability | pass/warn/fail | pass/warn/fail |
| Extensibility | pass/warn/fail | pass/warn/fail |
| Dependency discipline | pass/warn/fail | pass/warn/fail |
| Observability | pass/warn/fail | pass/warn/fail |

## Blocking Findings

### Without CairnDev

- 

### With CairnDev

- 

## Non-Blocking Findings

### Without CairnDev

- 

### With CairnDev

- 

## Prompt Repetition

| Question | Without CairnDev | With CairnDev |
| --- | --- | --- |
| Did the user restate engineering taste? |  |  |
| Did the agent identify affected boundaries? |  |  |
| Did the agent name the smallest viable change? |  |  |
| Did the agent run tests and `cairndev check`? |  |  |

## Decision

```text
Go / continue / shrink / stop
```

## Notes

```text
Summarize what CairnDev improved, what it missed, and which check or skill should change next.
```
