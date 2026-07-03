# Codex Execution Plan

## Step 1: Make the CLI installable

Implement `pyproject.toml` and a console script:

```bash
cairndev --help
```

## Step 2: Load contract

Implement loading `.cairndev/contract.yaml` and defaults when absent.

## Step 3: Implement checks

Start with deterministic static checks:

```text
missing AGENTS.md
missing .cairndev/contract.yaml
missing tests directory
Python file too long
Python function too long
Python class too broad
TODO/FIXME markers
obvious global mutable state
```

## Step 4: Add continuous-agent state checks

Represent multi-round work with `.cairndev/goal.yaml` and validate it when
`agentic_iteration.enabled` is true:

```text
missing goal state
empty durable objective
missing success criteria
missing human pause triggers
unverified current iteration
human review interval exceeded
```

## Step 5: Reports

Output both text and JSON:

```bash
cairndev check .
cairndev check . --json
```

## Step 6: Init command

Generate repo-local artifacts:

```bash
cairndev init --target .
```

## Step 7: Tests

Add tests for:

```text
contract loading
file scanning
function length detection
missing required files
CLI JSON output
init command idempotency
agentic iteration state validation
```

## Step 8: Plugin packaging

Verify plugin scaffold:

```text
plugins/cairndev-quality/.codex-plugin/plugin.json
plugins/cairndev-quality/skills/dev-quality-control/SKILL.md
plugins/cairndev-quality/skills/dev-quality-review/SKILL.md
.agents/plugins/marketplace.json
```
