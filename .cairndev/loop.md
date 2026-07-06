# CairnDev Loop Trajectory

Use this file for durable summaries of long-running agentic development loops.
Record only high-signal facts that help the next iteration resume safely:

- iteration number;
- smallest implemented change;
- verification commands and result;
- design impact or contract risk;
- human review decision when one happens.

## Iteration 2

- Smallest change: added optional loop engineering state to `.cairndev/goal.yaml`
  with trajectory, checkpoints, required skills, and verification command checks.
- Research decision: do not embed OpenHands, LangGraph, AutoGen, SWE-agent, or
  Aider as runtime dependencies; reuse their mature patterns as local contract
  checks so CairnDev stays lightweight and provider-agnostic.
- Verification: `python3 -m compileall -q src tests`, `python3 -m ruff check .`,
  `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest pytest -q`, and
  `PYTHONPATH=src python3 -m cairndev.cli check .` passed.
- Design impact: CairnDev now checks loop trajectory, checkpoint, skill, and
  verification-command continuity without adding new runtime dependencies.
