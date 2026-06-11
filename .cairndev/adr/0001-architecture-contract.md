# ADR 0001: Architecture Contract as a First-Class Development Artifact

Status: accepted
Date: 2026-06-09

## Context

Agentic coding tools can implement changes quickly, but project-level design taste is often repeated manually in prompts. The same preferences—low coupling, extensibility, reusability, reliability, minimalism—should not need to be restated in every task.

## Decision

Represent engineering taste as a repo-local, machine-readable design contract in `.cairndev/contract.yaml`, plus human-readable instructions in `AGENTS.md` and a reusable Codex skill.

## Consequences

- Agents can read the same contract before every task.
- A CLI can check a subset of the contract deterministically.
- Human review can focus on meaningful architectural tradeoffs rather than repeated style reminders.
- The contract must remain small, otherwise it becomes noise.
