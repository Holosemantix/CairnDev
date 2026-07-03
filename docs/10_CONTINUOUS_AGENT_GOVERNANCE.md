# Continuous Agent Governance

## Conclusion

Multi-round agentic development needs an explicit project state file. Chat
history, context compaction, and informal summaries are useful working memory,
but they are not a durable source of truth.

CairnDev therefore treats long-running work as a contract plus state problem:

```text
.cairndev/contract.yaml   # policy, budgets, required checks
.cairndev/goal.yaml       # durable objective, iteration state, pause triggers
AGENTS.md                 # human-readable workflow
cairndev check .          # deterministic gate
```

## Research Summary

Current agent engineering guidance is converging on a few practical ideas:

- Keep agent systems simple and composable before adding orchestration layers.
- Use ground-truth feedback from tools, tests, and the environment at each step.
- Add checkpoints, stop conditions, and human feedback points for long-running
  tasks.
- Use guardrails around risky inputs, outputs, and tool calls.
- Keep traces or durable records so runs can be debugged and resumed.

These practices are useful, but the ecosystem is not mature enough to rely on
agent memory alone. CairnDev should encode the parts that are easy to verify
locally and leave subjective decisions to human review.

References:

- Anthropic, "Building effective agents":
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK, "Guardrails":
  https://openai.github.io/openai-agents-python/guardrails/
- OpenAI Agents SDK, "Tracing":
  https://openai.github.io/openai-agents-python/tracing/

## Contract Policy

Projects opt in through `.cairndev/contract.yaml`:

```yaml
agentic_iteration:
  enabled: true
  require_goal_file: true
  goal_file: ".cairndev/goal.yaml"
  max_iterations_without_human_review: 6
  require_verification_each_iteration: true
  min_success_criteria: 1
  min_pause_triggers: 1
```

The policy is intentionally small:

- `enabled` keeps the feature opt-in for existing projects.
- `goal_file` points to a repo-local YAML file.
- `max_iterations_without_human_review` prevents indefinite autonomous drift.
- `require_verification_each_iteration` enforces a verification checkpoint.
- `min_success_criteria` and `min_pause_triggers` prevent vague goal files.

## Goal State

The goal file stores the durable task state:

```yaml
schema_version: "0.1"
objective: "Build the backend service."
status: active
current_iteration: 3
last_verified_iteration: 3
last_human_review_iteration: 1

success_criteria:
  - "End-to-end analysis, simulation, and backtest paths are verified."

pause_triggers:
  - "Scope, safety boundary, deployment posture, or public behavior changes."
  - "Required verification cannot run or fails."
```

Agents should update `current_iteration` when starting a new implementation
slice and update `last_verified_iteration` only after the required checks pass.
Human review should update `last_human_review_iteration`.

## Check Behavior

`cairndev check .` reports errors when agentic iteration is enabled and:

- the goal file is missing;
- the goal path is not repo-local;
- the objective is empty;
- status is not `active`, `paused`, `blocked`, or `complete`;
- success criteria or pause triggers are missing;
- the current iteration is unverified;
- the configured human-review interval is exceeded.

This does not replace human judgment. It makes the minimum continuity contract
hard to forget across long runs, tool restarts, or context resets.
