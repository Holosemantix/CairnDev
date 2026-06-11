Use the dev-quality-control workflow.

Task:
<describe task here>

Before coding:
1. Read AGENTS.md.
2. Read .cairndev/contract.yaml.
3. Identify affected modules and boundaries.
4. Propose the smallest implementation plan.
5. State any design risks.

During coding:
1. Keep the change minimal and reversible.
2. Add tests for public behavior.
3. Avoid new runtime dependencies unless justified.

After coding:
1. Run tests.
2. Run cairndev check . if available.
3. Summarize design impact, tests run, and remaining risks.
