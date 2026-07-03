# Validation Protocol

## 1. Validation question

Does CairnDev measurably improve Codex outputs across real projects by reducing architectural drift and repeated prompt overhead?

## 2. Initial personal validation

Use CairnDev in three projects:

```text
1. cairnlab
2. a small web app or mini tool
3. a game/app prototype or OpenClaw-adjacent plugin
```

For each project, run two tasks with and without CairnDev.

Record:

```text
- number of files changed
- lines changed
- tests added
- new dependencies added
- review comments required
- design violations detected
- whether the implementation was smaller
- whether Codex followed architecture boundaries
- whether you had to restate your preferences manually
- whether Codex preserved the durable goal across multiple turns
- whether `.cairndev/goal.yaml` made context reset recovery accurate
```

## 3. Minimal metrics

```yaml
prompt_repetition_reduction:
  description: "How often did user need to restate design taste?"
architecture_violation_count:
  description: "Obvious boundary/coupling/minimalism violations."
pr_size:
  description: "Files and lines changed."
test_coverage_delta:
  description: "Tests added or updated for changed behavior."
dependency_delta:
  description: "New runtime dependencies."
human_review_effort:
  description: "Subjective review effort 1-5."
accepted_without_major_rewrite:
  description: "Whether the result could be accepted after small fixes."
goal_drift_count:
  description: "Times the agent's implementation deviated from the durable objective."
unverified_iteration_count:
  description: "Iterations where work continued without passing required checks."
```

## 4. Go criteria

Continue building if:

```text
- it reduces repeated prompt text in all 3 projects;
- it catches at least one meaningful design violation per project;
- it makes Codex plans more explicit and constrained;
- it preserves long-running objectives without repeated manual reminders;
- it does not create heavy process overhead;
- you would actually keep copying it into new projects.
```

## 5. No-Go criteria

Stop or shrink the project if:

```text
- it becomes prompt boilerplate only;
- checks are noisy and ignored;
- it slows down development without improving review quality;
- existing linters/templates already cover the useful parts;
- the goal state becomes stale paperwork rather than an enforced check;
- you do not use it voluntarily after the first three projects.
```
