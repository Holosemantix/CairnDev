# PR Checklist

## Behavior

- [ ] The change solves the stated task.
- [ ] Public behavior changes are tested.
- [ ] Edge cases are handled explicitly.

## Architecture

- [ ] Module boundaries are preserved.
- [ ] No unnecessary abstraction was added.
- [ ] No hidden global mutable state was introduced.
- [ ] New public APIs are narrow and documented.

## Reliability

- [ ] Tests pass.
- [ ] Linters/type checks pass where available.
- [ ] Errors are actionable.

## Minimalism

- [ ] The PR is small enough to review.
- [ ] New dependencies are justified.
- [ ] Follow-up work is tracked separately.

## CairnDev

- [ ] `cairndev check .` passes or exceptions are justified.
