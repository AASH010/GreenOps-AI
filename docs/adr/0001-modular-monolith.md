# 0001 — Modular monolith for the MVP

- **Status:** Accepted
- **Date:** 2026-11-25
- **Related tasks:** PLT-01, RES-01

## Context
Three students must deliver one end-to-end vertical slice. The Researcher, detection, forecasting, optimization and simulation share data and need reproducible runs.

## Options considered
1. **Modular monolith** (Python and FastAPI, PostgreSQL, containers) — one deployable, in-process calls, easy local reproduction; module boundaries kept by packages and contracts.
2. **Microservices or a fleet of agents** — independent deployment, but more operations, more integration failures and harder reproducibility for a small team.

## Decision
Option 1. Split a module out only when a measured need appears. The Researcher is one deterministic orchestrator with modular stages.

## Consequences
Simple setup and testing; modules must stay decoupled through versioned contracts so a later split remains possible.
