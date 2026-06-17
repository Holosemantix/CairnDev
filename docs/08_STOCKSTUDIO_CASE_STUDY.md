# StockStudio Case Study

StockStudio is a live example of using CairnDev as a lightweight design-control layer during agentic development.

The project is an internal A-share medium/low-frequency research, portfolio construction, risk alerting, and paper-trading platform. It is useful as a CairnDev example because the product has real architectural pressure:

- evidence-backed Agent outputs;
- point-in-time data and `available_at` constraints;
- risk and compliance veto paths;
- human approval before portfolio actions;
- no live auto trading in early phases;
- cross-platform client adaptation across CLI, Windows, macOS, iOS, and Android.

## What CairnDev Constrained

The first development pass established project-local guidance before feature work:

- `AGENTS.md` made the non-negotiable project rules explicit.
- `.cairndev/contract.yaml` converted engineering taste into a machine-readable contract.
- repo-local `dev-quality-control` and `dev-quality-review` skills made the workflow repeatable.
- `docs/CODEX_FINAL_EXECUTION_SPEC.md` became the highest-priority product source.

This let implementation start from explicit constraints instead of a broad prompt.

## Phase 0 Outcome

The initial StockStudio scaffold focused on the smallest useful foundation:

- FastAPI application factory with `/health`.
- Pydantic contracts for timestamped evidence and Agent findings.
- Compliance text guardrails for forbidden market-facing claims.
- Portfolio risk checks with pass/review/reject decisions.
- SQLAlchemy/Alembic starting point.
- Deterministic tests.

The old conflicting design document was removed so agents would not read stale guidance.

## Phase 1 Outcome

The next slice added platform-neutral market-data contracts rather than real data-source integrations:

- `AssetRecord`.
- `DailyBarRecord`.
- `TradingCalendarSession`.
- `DataSourceSkill` as a narrow ingestion boundary.
- daily-bar quality checks for duplicates, timestamp violations, and suspended trading activity.

This kept business rules in core modules and left AKShare/Tushare adapters for a later step.

## Cross-platform Contract

During development, StockStudio added a cross-platform requirement:

```text
CLI + Windows + macOS + iOS + Android
```

CairnDev captured this in two places:

- CairnDev's default contract template, so future projects can inherit the same principle.
- StockStudio's local contract and platform design docs.

The design decision was:

```text
one backend and one core domain model
many client entries
no duplicated business rules per platform
```

The staged route is:

1. API-first core.
2. CLI-first operations.
3. Responsive Web/PWA-first UI.
4. Desktop shell only when needed.
5. Mobile shell only when needed.

## Verification Pattern

Each meaningful change used the same verification loop:

```bash
pytest -q
cairndev check .
python -m compileall -q src tests
```

When local shell tools differed across environments, the documented module entry point was used instead of changing the project contract ad hoc.

## Lessons

- A final product spec should be copied into the target repository, not left as an external prompt.
- Stale design documents should be removed or clearly deprecated.
- Cross-platform support is cheapest when enforced as an architecture boundary early.
- CairnDev is most useful when it shapes the next smallest reversible implementation, not when it tries to generate the whole product at once.
