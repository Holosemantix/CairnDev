# Codex Plugin and Skill Spec

## 0. Role split

CairnDev's main contribution is the agent workflow, not a replacement for
linters or type checkers. Use each layer for a different job:

```text
AGENTS.md / .cairndev/contract.yaml
  source of truth for project constraints

Codex skills / plugin
  agent execution protocol for planning, implementation, and review

cairndev check / hooks / CI
  deterministic guardrails for hard, measurable drift
```

Keep `cairndev check` small and deterministic. Put judgment-heavy questions,
such as whether an abstraction is justified or a module boundary is clean, in
the skill protocol so the agent must reason from the local project contract.

## 1. Repo-local skill first

Use repo-local skills before publishing a plugin.

Path:

```text
.agents/skills/dev-quality-control/SKILL.md
```

This is enough for local Codex usage.

## 2. Plugin later

Package stable skills under:

```text
plugins/cairndev-quality/
  .codex-plugin/plugin.json
  skills/dev-quality-control/SKILL.md
  skills/dev-quality-review/SKILL.md
```

## 3. Local marketplace

Path:

```text
.agents/plugins/marketplace.json
```

Purpose:

```text
Expose the local plugin to Codex’s plugin browser for repo-scoped testing.
```

## 4. Plugin contents

The plugin should contain only reusable workflows, not project-specific secrets or private implementation details.

Recommended skills:

```text
dev-quality-control: use before and during implementation
dev-quality-review: use after implementation or before PR
```

Optional later:

```text
mcp server: expose cairndev check results as structured tools
hooks: run cairndev check after file edits or before commits
```

## 5. Skill trigger language

Use trigger words in the skill description:

```text
quality, architecture, low coupling, extensible, reusable, reliable, minimal code, clear variable naming, self-explanatory names, design review, PR review, Codex task planning
```

## 6. Boundaries

The skill should never instruct Codex to:

```text
- rewrite the whole codebase without approval;
- add dependencies without justification;
- bypass tests;
- change architecture silently;
- invent requirements not present in the task;
- perform security-sensitive operations without explicit approval.
```

