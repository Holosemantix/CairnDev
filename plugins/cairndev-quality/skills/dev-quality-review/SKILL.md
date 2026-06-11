---
name: dev-quality-review
description: Use after code changes or before a pull request to review architecture, coupling, reliability, tests, dependency drift, and minimalism.
---

# Dev Quality Review Skill

Review the change against the repo's design contract.

## Steps

1. Read `.cairndev/contract.yaml`.
2. Inspect changed files.
3. Check whether the change is minimal and reversible.
4. Check whether public behavior changes have tests.
5. Check whether dependencies were added.
6. Run `cairndev check .` if available.
7. Produce a review with:
   - pass/fail summary;
   - blocking issues;
   - non-blocking improvements;
   - architectural risks;
   - suggested smaller alternative if the change is overbuilt.

## Review rubric

```text
Coupling: pass / warn / fail
Cohesion: pass / warn / fail
Minimalism: pass / warn / fail
Reliability: pass / warn / fail
Testability: pass / warn / fail
Extensibility: pass / warn / fail
Dependency discipline: pass / warn / fail
```
