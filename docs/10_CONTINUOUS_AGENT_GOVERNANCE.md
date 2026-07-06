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

Current agent engineering guidance and open-source usage converge on a few
practical ideas:

- Keep agent systems simple and composable before adding orchestration layers.
- Use ground-truth feedback from tools, tests, and the environment at each step.
- Add checkpoints, stop conditions, and human feedback points for long-running
  tasks.
- Use guardrails around risky inputs, outputs, and tool calls.
- Keep traces or durable records so runs can be debugged and resumed.
- Keep skills and reusable playbooks as explicit files, not only chat memory.
- Treat sandboxing and tool boundaries as part of the loop design.

These practices are useful, but the ecosystem is not mature enough to rely on
agent memory alone. CairnDev should encode the parts that are easy to verify
locally and leave subjective decisions to human review.

## Open-Source Landscape For Loop Engineering

The most useful projects to learn from are not interchangeable:

- OpenHands is a broad self-hosted control center and agent runtime. It is
  useful as a reference for sandboxed execution, multiple agent backends, and
  scheduled/webhook automations, but too large to embed in CairnDev.
- SWE-agent and mini-SWE-agent are strong references for repository-level
  agent-computer interfaces: small tools, explicit config, benchmarked issue
  resolution, and test-driven loops.
- Aider is a pragmatic reference for keeping developers in control: narrow file
  context, git-aware edits, tests/lint commands, and terminal-first workflow.
- LangGraph is a mature orchestration runtime for durable execution,
  persistence, interrupts, and human-in-the-loop workflows. CairnDev should
  remain compatible with it, not depend on it.
- AutoGen is useful when a project truly needs event-driven multi-agent
  collaboration, Docker code execution, MCP, and distributed runtimes.

CairnDev's role is therefore narrower: make any of these tools safer to use in
a repository by checking the durable goal, verification state, human-review
interval, loop trajectory, checkpoints, and required repo-local skills.

References:

- Anthropic, "Building effective agents":
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK, "Guardrails":
  https://openai.github.io/openai-agents-python/guardrails/
- OpenAI Agents SDK, "Tracing":
  https://openai.github.io/openai-agents-python/tracing/
- OpenHands:
  https://github.com/OpenHands/OpenHands
- SWE-agent:
  https://github.com/SWE-agent/SWE-agent
- Aider:
  https://github.com/Aider-AI/aider
- LangGraph:
  https://docs.langchain.com/oss/python/langgraph/overview
- Microsoft AutoGen:
  https://microsoft.github.io/autogen/stable/

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

For loop engineering, projects may also declare:

```yaml
verification:
  required_commands:
    - "pytest -q"
    - "cairndev check ."

loop_engineering:
  trajectory_file: ".cairndev/loop.md"
  checkpoint_files:
    - ".cairndev/goal.yaml"
    - ".cairndev/contract.yaml"
  required_skills:
    - "dev-quality-control"
    - "dev-quality-review"
```

The trajectory file is a durable, human-readable log of iteration decisions and
verification outcomes. Checkpoint files are the state files that must exist
before an agent can safely resume. Required skills are repo-local procedural
knowledge the agent must be able to load before performing long-running work.

## Check Behavior

`cairndev check .` reports errors when agentic iteration is enabled and:

- the goal file is missing;
- the goal path is not repo-local;
- the objective is empty;
- status is not `active`, `paused`, `blocked`, or `complete`;
- success criteria or pause triggers are missing;
- the current iteration is unverified;
- the configured human-review interval is exceeded.
- required verification commands are missing;
- declared loop trajectory or checkpoint files are missing;
- declared repo-local loop skills are missing.

This does not replace human judgment. It makes the minimum continuity contract
hard to forget across long runs, tool restarts, or context resets.

## Why Not Directly Embed A Runtime

OpenHands, LangGraph, AutoGen, SWE-agent, and Aider are all valuable, but they
solve different runtime problems. Embedding any one of them would make CairnDev
less provider-agnostic and would add operational complexity to a tool whose job
is to check contracts. The safer integration path is:

1. keep CairnDev as a local contract and verification gate;
2. expose repo-local skills and required commands that any coding agent can use;
3. let teams run OpenHands/LangGraph/AutoGen/SWE-agent/Aider around the repo when
   they need orchestration;
4. require `cairndev check .` and the declared project tests as the loop's
   non-negotiable stop gate.
