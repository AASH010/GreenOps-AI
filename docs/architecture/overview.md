# Architecture overview

Direction only; tasks and status live in [`TRACKING.md`](../../TRACKING.md).

## Four planes

| Plane | Components | Responsibility |
|---|---|---|
| Local Data & Safety | Collectors and adapters, validation, topology cache, local monitoring, policy checks, **Local Safety Guard** | Read approved data, validate it, keep essential monitoring and safety working during cloud disconnection |
| Cloud Intelligence | FastAPI services, Researcher orchestrator, forecasting, optimization, case management, dashboard APIs | Historical analysis, AI-assisted investigation, planning, reporting, persistent services |
| Digital Twin & Experiment | Simulator, workload replay, thermal and energy approximation, experiment runner | Test candidate policies and scenarios without changing live infrastructure |
| Operator Experience | React and TypeScript cockpit, topology and analytics views, research timeline, Decision Certificates | Make state, evidence, alternatives and recommendations understandable and reviewable |

The MVP is a **modular monolith** (Python and FastAPI for backend, AI, simulation and optimization; PostgreSQL for structured state; containers for reproducibility). Services are split only when a measured need appears.

## Workflow

Connect → Observe → Understand → Research → Explore → Verify → Decide → Learn. The first proof is one vertical slice: a **workload-imbalance / thermal-pressure** case flows from telemetry and topology to detection, evidence, competing hypotheses, active experiment selection, Digital Twin comparison, verification and an auditable Decision Certificate.

## Operating Researcher

One deterministic orchestrator with modular stages (discovery, evidence, hypotheses, experiment selection, simulation, verification, memory) — not a fleet of independent agents. "Continuous" means it continuously observes and prioritizes cases; experiments run only when expected information value and operational relevance justify the cost, and only inside the sandbox. An LLM may draft hypotheses and explanations; deterministic code validates schemas, evidence references, permissions, budgets, constraints and stop conditions.

| Autonomy level | Allowed in the MVP |
|---|---|
| Observe | Read approved data and monitor state |
| Investigate | Collect evidence, correlate signals, draft hypotheses |
| Experiment | Run bounded Digital Twin experiments within a configured research budget |
| Recommend | Prepare evidence-backed recommendations and decision reports |
| Execute | **None.** Any future execution needs explicit operator approval, policy allowlists, rollback planning and independent local enforcement |

## Safety boundary
No production control: no chillers, CRAC/CRAH, UPS, switchgear or power distribution; no autonomous shutdown or reboot; no unrestricted workload migration. Cooling, UPS, switchgear and server-power actions are advisory or sandbox-only. The Local Safety Guard is deterministic, independent of any LLM, and keeps working without cloud connectivity. `backend/app/safety/guard.py` is the first draft; the contracts enforce `sandbox_only` and `high_impact_execution = blocked`.

## Provenance labels
Every metric is `MEASURED`, `REPLAYED`, `ESTIMATED` or `SIMULATED`, and the label is always visible. Simplified power and thermal models are acceptable if their assumptions are visible; nothing implies CFD-grade fidelity or measured savings.

## Huawei Cloud services
ECS, RDS for PostgreSQL and OBS are the intended core building blocks, subject to account access, quotas and regional availability. ModelArts and MaaS/Pangu are optional. IAM/CTS, VPC and AOM/Cloud Eye are named only for the exact supported feature used. CCE, DCS and CodeArts Agent are optional or development-support capabilities. A local container fallback is kept, and each service is labelled **implemented**, **planned** or **optional** in the final presentation (task CLD-07).
