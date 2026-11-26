# 0002 — Single repository with area folders

- **Status:** Accepted
- **Date:** 2026-11-25
- **Related tasks:** OPS-01

## Context
The project has a backend, a frontend, shared contracts, experiments and a tracking file whose status drives the README. Members work through forks.

## Options considered
1. **One repository with folders** (`backend/`, `frontend/`, `contracts/`, `experiments/`, `docs/`) — one history and one automation; contracts shared in one place.
2. **Permanent branches per area** — separate histories; the generated README and workflows would have to stay in sync on every branch.

## Decision
Option 1. Work branches are prefixed by area. CI filters by path where useful.

## Consequences
One place for contracts and tracking; members must keep changes small to avoid conflicts in shared files.
