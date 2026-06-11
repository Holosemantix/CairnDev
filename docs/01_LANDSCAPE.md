# AutoDev Landscape and Collision Analysis

## 1. Mature or fast-maturing categories

### 1.1 Commercial coding agents

Examples:

- OpenAI Codex
- Claude Code
- GitHub Copilot cloud agent
- Cursor / Windsurf-like IDE agents
- Devin-like cloud software engineers
- Replit Agent / app builders

Capabilities already common:

```text
read codebase
edit files
run commands/tests
create branches
make commits
open PRs
iterate on review comments
use repository instructions
connect external tools through MCP or integrations
```

Collision risk: extremely high if CairnDev claims to be a full AutoDev agent.

### 1.2 Open-source coding agents

Examples:

- OpenHands
- SWE-agent / mini-SWE-agent
- Aider
- MetaGPT
- AutoGen/CrewAI-based coding workflows

Capabilities:

```text
repo-level issue solving
terminal editing
multi-agent planning
software-company-style roles
benchmarking on SWE-bench-style tasks
custom workflows and SDKs
```

Collision risk: high if CairnDev claims to implement the development loop itself.

### 1.3 Agent customization mechanisms

Examples:

```text
AGENTS.md / CLAUDE.md
Codex skills
Codex plugins
Claude Code skills/hooks/subagents
GitHub Copilot custom instructions/prompt files/custom agents
MCP servers
repo-local rules files
```

These provide integration surfaces, not the full design-quality artifact by themselves.

## 2. What remains underserved

The recurring gap is not lack of agents. It is lack of **portable engineering taste**.

Most agents can follow a prompt like:

```text
Use low coupling, extensible design, reusable components, high reliability, and minimal code.
```

But that does not guarantee:

```text
- the instruction persists across sessions;
- the instruction is adapted to the repo’s current architecture;
- changes are checked against a machine-readable contract;
- design tradeoffs are recorded;
- architectural drift is detected;
- different agents follow the same standard;
- quality constraints are versioned with the repo.
```

## 3. CairnDev differentiation

CairnDev should be a **design contract layer**:

```text
Task request
→ read design contract
→ plan smallest acceptable change
→ implement
→ run tests/checks
→ score against design contract
→ record ADR when needed
```

It is closer to “architecture governance for coding agents” than “AutoDev”.

## 4. Use existing tools instead of replacing them

| Layer | Use existing | CairnDev role |
|---|---|---|
| Code generation | Codex / Claude Code / Copilot / Aider | Provide taste contract and review gates |
| PR automation | Copilot cloud agent / Codex GitHub integration | Provide PR checklist and quality report |
| Multi-agent orchestration | OpenHands / MetaGPT / AutoGen / CrewAI | Provide shared design rules across agents |
| Repo issue solving | SWE-agent / OpenHands | Provide architecture constraints and post-check |
| Tool integration | MCP | Optional future interface for quality reports |
| CI | GitHub Actions / local hooks | Run `cairndev check` |

## 5. Go / No-Go

Go if:

```text
- the tool is useful in your next 3 real Codex projects;
- it reduces repeated prompt instructions;
- it catches design drift before review;
- it produces better task plans and smaller PRs;
- it remains model/tool agnostic.
```

No-Go if:

```text
- it becomes a generic coding agent;
- it only stores prompts with no checks;
- it requires users to adopt a heavy framework;
- it conflicts with existing linters and build systems;
- it slows down development without improving design quality.
```

