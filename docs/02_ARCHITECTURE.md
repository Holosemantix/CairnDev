# CairnDev Architecture

## 1. Architecture overview

```text
repo/
  AGENTS.md                         # persistent agent guidance
  .cairndev/
    contract.yaml                    # machine-readable design contract
    adr/                             # design decisions
    reports/                         # generated quality reports
  .agents/
    skills/dev-quality-control/      # repo-local Codex skill
    plugins/marketplace.json         # local plugin marketplace entry
  plugins/cairndev-quality/          # shareable Codex plugin scaffold
  src/cairndev/                      # optional CLI implementation
```

## 2. Components

### 2.1 Design contract

File:

```text
.cairndev/contract.yaml
```

Purpose:

```text
- declare design principles;
- define budgets;
- define required commands;
- define review checklist;
- make project taste version-controlled.
```

### 2.2 Agent instructions

File:

```text
AGENTS.md
```

Purpose:

```text
- tell Codex how to work in this project;
- point Codex to the design contract;
- define default workflow before and after coding.
```

### 2.3 Skill

File:

```text
.agents/skills/dev-quality-control/SKILL.md
```

Purpose:

```text
- package the reusable workflow;
- let Codex invoke the quality-control behavior explicitly or implicitly;
- avoid stuffing too much text into AGENTS.md.
```

### 2.4 CLI

Command:

```bash
cairndev check .
cairndev summarize .
cairndev init --target .
```

Purpose:

```text
- provide deterministic checks;
- generate reports;
- bootstrap repo-local files;
- remain independent of any LLM provider.
```

### 2.5 Plugin scaffold

Directory:

```text
plugins/cairndev-quality/
```

Purpose:

```text
- package skills as a Codex plugin;
- enable local marketplace testing;
- later share across projects or teams.
```

## 3. Data flow

```text
Developer asks Codex to implement task
  ↓
Codex reads AGENTS.md
  ↓
Codex activates dev-quality-control skill
  ↓
Codex reads .cairndev/contract.yaml
  ↓
Codex writes plan constrained by design contract
  ↓
Codex implements smallest change
  ↓
Codex runs tests and cairndev check
  ↓
Codex summarizes violations and fixes or justifies them
```

## 4. Check types

MVP checks:

```text
- file length budget
- function length budget for Python
- class method count budget for Python
- broad TODO/FIXME markers
- likely global mutable state in Python
- missing tests directory
- missing design contract
- missing AGENTS.md
- dependency count drift placeholder
```

Later checks:

```text
- circular imports
- module dependency graph
- public API budget
- architecture boundary rules
- changed public behavior without tests
- package-level ownership map
- complexity scoring
- PR diff scoring
```

## 5. Design philosophy

The CLI should be intentionally conservative. It should not attempt to solve subjective design completely. Its job is to catch obvious drift and to force explicit justification when a change exceeds the project’s declared taste budget.

