# GreenOps AI — Tracking

> **SYNTRIX** · product **GreenOps AI** · *Autonomous Data-Center Operations*
>
> This file is the **tracking source** for the progress and milestone views in `README.md`. It lists tracked tasks, owners, milestones and exit gates. It is **not** a project plan: it fixes no dates and no effort estimates. Version 0.1 · last updated 2026-11-25.

## 1. Tracking Contract

- A **task row** has exactly eight columns: `ID | Task | Pri | MS | Owner | Depends | Done when | Status`. Its ID starts with one of the 16 area prefixes below.
- `Pri`: **P0** MVP proof · **P1** essential · **P2** optional (tracked, excluded from the headline progress).
- `MS`: milestone `M01`–`M11` (`M11` is the optional milestone).
- `Owner`: `Member 1`, `Member 2` or `Member 3` (table in section 2). Paired work names the accountable owner in the task.
- `Status`: `todo`, `doing`, `blocked`, `done`. A task is `done` only when it is implemented, tested, documented and reviewed, and the status is changed in the same pull request.
- `Depends`: comma-separated task IDs or `—`. A task may not depend on a task in a later milestone, and a core task may not depend on an optional one.
- A **gate** is a checklist line `- [ ] Mxx-Gy …` in section 4.
- **Actual progress** = done P0/P1 tasks ÷ all P0/P1 tasks. A milestone is **complete** only when all its core tasks are done **and** every gate is ticked. Commits never count as progress.
- `scripts/update_status.py --validate` enforces this contract; the automation is described in `docs/workflows.md`.

## 2. Owners

| Owner | Accountability |
|---|---|
| Member 1 | Platform & Data — backend, ingestion, data model, APIs, safety guard, cloud packaging |
| Member 2 | Intelligence & Research — detection, forecasting, optimizer, Operating Researcher, evaluation |
| Member 3 | Digital Twin & Product — simulation, visualization, operator workflow, validation and demo |

Member 2 and Member 3 pair on simulation and optimization; Member 1 owns API contracts and supports integration. No feature is complete until it works across its agreed interface.

## 3. Work Areas

| Area | Name | Prefix |
|---|---|---|
| A01 | Platform & API | PLT |
| A02 | Telemetry, Topology & Data | DAT |
| A03 | Operations Cockpit | COK |
| A04 | Anomaly & Situation Detection | DET |
| A05 | Forecasting & Capacity | FOR |
| A06 | Operating Researcher | RES |
| A07 | Digital Twin Scenario Lab | TWN |
| A08 | Workload & Resource Optimization | OPT |
| A09 | Decision & Governance | DEC |
| A10 | Safety Guard | SAF |
| A11 | Evaluation | EVL |
| A12 | Cloud & Packaging | CLD |
| A13 | AI Development Assistants | DEV |
| A14 | Security & Data Protection | SEC |
| A15 | Repository, Automation & Docs | OPS |
| A16 | Usability & Demo | UXV |

## 4. Milestones

The ten gates follow the milestone-based delivery plan: indicative checkpoints, **not promised dates**. If time becomes limited, the end-to-end product journey is preserved and depth in secondary integrations is reduced.

| ID | Name | Objective | Depends on |
|---|---|---|---|
| M01 | Week 1 — Scenario, repo, schemas, baseline | One scenario, data dictionary, trace, API contract and reproducible setup | — |
| M02 | Week 2 — Telemetry, topology, cockpit skeleton | Validated import and visible assets and KPIs with provenance | M01 |
| M03 | Week 3 — Detection and case lifecycle | A known trigger creates a case with evidence | M02 |
| M04 | Week 4 — Hypotheses and forecasting | Two falsifiable hypotheses and a forecast compared with baselines | M03 |
| M05 | Week 5 — Digital Twin replay | Repeatable baseline run with saved seed and configuration | M04 |
| M06 | Week 6 — Optimizer and constraints | Candidate alternatives and hard-constraint rejection | M05 |
| M07 | Week 7 — Active experiment selection | The Researcher ranks and chooses experiments under budget | M06 |
| M08 | Week 8 — Verification and memory | Decision Certificate with uncertainty and limitations | M07 |
| M09 | Week 9 — Integration and safety | End-to-end flow; the local guard survives cloud loss | M08 |
| M10 | Week 10 — Evaluation and demo | A/B/C results, ablations, reproducible demo and honest limitations | M09 |
| M11 | Optional extensions | Optional integrations and models, each judged individually | M03 |

**Exit gates**

M01 — Scenario, repo, schemas, baseline
- [ ] M01-G1 One vertical-slice scenario (workload imbalance / thermal pressure) is defined and agreed (TWN-01)
- [ ] M01-G2 Data dictionary and the seven contracts are drafted, with fixtures and passing tests
- [ ] M01-G3 A sample replay trace with its topology exists and is documented (DAT-02)
- [ ] M01-G4 API contract v0 is reviewed by all three members (PLT-03)
- [ ] M01-G5 One documented command reproduces the setup from a clean checkout (PLT-02)

M02 — Telemetry, topology, cockpit skeleton
- [ ] M02-G1 The trace is imported and validated; bad rows are rejected with reasons
- [ ] M02-G2 The cockpit shows assets and KPIs of the scenario
- [ ] M02-G3 Every visible metric carries a provenance label

M03 — Detection and case lifecycle
- [ ] M03-G1 The known injected condition opens a case with evidence references
- [ ] M03-G2 Normal data opens no case
- [ ] M03-G3 Repeated signals collapse into one case (deduplication and cooldown)

M04 — Hypotheses and forecasting
- [ ] M04-G1 A case shows two or more falsifiable hypotheses with evidence references and missing evidence
- [ ] M04-G2 The forecast is compared with simple baselines and its unreliable regions are described
- [ ] M04-G3 Detection usefulness is reported on labelled scenarios

M05 — Digital Twin replay
- [ ] M05-G1 A baseline run repeats exactly from a saved seed and configuration
- [ ] M05-G2 Simulated outputs are labelled SIMULATED with visible assumptions
- [ ] M05-G3 The experiment harness runs with one command

M06 — Optimizer and constraints
- [ ] M06-G1 Explainable candidate alternatives are produced for the scenario
- [ ] M06-G2 A candidate that violates a hard constraint is rejected with a reason
- [ ] M06-G3 The conventional optimizer baseline for System A is documented

M07 — Active experiment selection
- [ ] M07-G1 The Researcher ranks and chooses experiments within a research budget
- [ ] M07-G2 Selection reason, budget and seed are recorded for every experiment

M08 — Verification and memory
- [ ] M08-G1 A Decision Certificate shows uncertainty, assumptions and limitations
- [ ] M08-G2 An operator can accept, reject, defer or request more investigation
- [ ] M08-G3 The case and its applicability limits are stored in research memory
- [ ] M08-G4 Audit records exist for every decision and experiment

M09 — Integration and safety
- [ ] M09-G1 The flow from connection to Decision Certificate runs end to end
- [ ] M09-G2 Local monitoring and the Safety Guard keep working when the cloud is unreachable
- [ ] M09-G3 An attempted high-impact action is blocked and audited
- [ ] M09-G4 The platform runs on ECS with RDS for PostgreSQL, or each service is honestly labelled planned
- [ ] M09-G5 The demo also runs locally with containers

M10 — Evaluation and demo
- [ ] M10-G1 Systems A, B and C are run on matched scenarios with the four ablations
- [ ] M10-G2 The core pass condition (C versus B on a pre-registered metric) is assessed and reported, including negative results
- [ ] M10-G3 The demo is reproducible and every value is labelled measured, replayed, estimated or simulated
- [ ] M10-G4 Limitations and failed cases are documented

M11 — Optional extensions *(not counted in the headline progress)*
- [ ] M11-G1 Each optional item that is claimed has its own run evidence; unclaimed items stay marked optional

## 5. Task Register

Columns: `ID | Task | Pri | MS | Owner | Depends | Done when | Status`.

### A01 — Platform & API (PLT)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| PLT-01 | Backend skeleton: FastAPI modular monolith layout, environment configuration, health endpoint, error model | P0 | M01 | Member 1 | — | runs locally and in a container · smoke test passes | todo |
| PLT-02 | Reproducible setup: container image and compose file for backend and PostgreSQL | P0 | M01 | Member 1 | PLT-01 | one documented command starts the stack from a clean checkout · verified on a clean machine | todo |
| PLT-03 | API contract v0 (OpenAPI skeleton for ingestion, assets, cases, experiments, certificates) | P0 | M01 | Member 1 | DAT-01 | reviewed by all three members · contract tests run against fixtures | todo |
| PLT-04 | PostgreSQL schema and migrations | P0 | M02 | Member 1 | DAT-01, PLT-02 | tables for assets, telemetry summaries, cases, hypotheses, experiments, results, certificates, audit · migrations apply cleanly | todo |
| PLT-05 | Telemetry ingestion API (validated, idempotent) | P0 | M02 | Member 1 | PLT-04, DAT-03 | duplicate and malformed records handled · tests | todo |
| PLT-06 | Assets and topology API | P0 | M02 | Member 1 | PLT-04, DAT-06 | returns the scenario topology with provenance · tests | todo |
| PLT-07 | Case lifecycle API | P0 | M03 | Member 1 | PLT-04, RES-01 | create, update status, list; transitions validated · tests | todo |
| PLT-08 | Audit-log writer and audit endpoints | P0 | M08 | Member 1 | PLT-04 | decisions, experiments and guard events recorded append-only · completeness test | todo |
| PLT-09 | Authentication and role-based authorization | P1 | M09 | Member 1 | PLT-03, SEC-02 | viewer, operator and admin roles · authorization tests | todo |
| PLT-10 | Reviewed API documentation | P1 | M10 | Member 1 | PLT-03, PLT-07, PLT-08 | generated documentation matches behaviour · check in CI | todo |

### A02 — Telemetry, Topology & Data (DAT)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| DAT-01 | Data dictionary and the TelemetryRecord and Asset contracts | P0 | M01 | Member 1 | — | timestamp, unit, entity id, source and provenance defined · schemas, fixtures and tests reviewed by the team | todo |
| DAT-02 | Sample replay trace and topology for the scenario | P0 | M01 | Member 1 | DAT-01, TWN-01 | labelled synthetic trace with the injected condition, and its topology, in `data/` · dataset documented | todo |
| DAT-03 | CSV and trace replay importer with validation | P0 | M02 | Member 1 | DAT-01, DAT-02 | checks timestamps, units, missing values and provenance; rejects bad rows with reasons · tests | todo |
| DAT-04 | Provenance labels end to end | P0 | M02 | Member 1 | DAT-01 | every stored and displayed metric carries MEASURED, REPLAYED, ESTIMATED or SIMULATED · tests | todo |
| DAT-05 | Data-quality gates and missing-data indicators | P0 | M02 | Member 1 | DAT-03 | quality status per entity and window visible to detection and the UI · tests | todo |
| DAT-06 | Topology model | P0 | M02 | Member 1 | DAT-01, DAT-02 | site, zone, rack, server and workload-to-host mapping · validation tests | todo |
| DAT-07 | First practical adapter (Prometheus-compatible metrics import) | P1 | M09 | Member 1 | DAT-03, DAT-04 | imports metrics from a test endpoint with labels preserved · limits documented | todo |
| DAT-08 | Additional telemetry sources | P2 | M11 | Member 1 | DAT-07 | Kubernetes Metrics API, IPMI/Redfish, PDU/BMS/DCIM as feasible · each marked implemented or not | todo |
| DAT-09 | Commercial and environmental context | P2 | M11 | Member 1 | DAT-03 | tariff, carbon intensity and water-use indicators available for later comparisons | todo |

### A03 — Operations Cockpit (COK)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| COK-01 | React and TypeScript application skeleton | P0 | M02 | Member 3 | PLT-03 | routing, API client and layout · build passes | todo |
| COK-02 | Topology and asset view | P0 | M02 | Member 3 | COK-01, PLT-06 | racks and servers visible with provenance labels | todo |
| COK-03 | KPI panels | P0 | M02 | Member 3 | COK-01, PLT-05 | utilization, capacity, performance, energy, temperature and alarms with data-quality status | todo |
| COK-04 | Case list and case detail | P0 | M03 | Member 3 | COK-01, PLT-07 | shows evidence, data quality and status | todo |
| COK-05 | Research timeline and hypotheses view | P0 | M04 | Member 3 | COK-04, RES-02 | shows hypotheses with supporting, weakening and missing evidence | todo |
| COK-06 | Candidate comparison panels | P0 | M06 | Member 3 | COK-04, OPT-01 | performance, energy, thermal and SLA trade-offs with assumptions and uncertainty visible | todo |
| COK-07 | Decision Certificate view and review controls | P0 | M08 | Member 3 | COK-04, DEC-02 | operator can accept, reject, defer or request more investigation | todo |
| COK-08 | History and learning search view | P1 | M09 | Member 3 | COK-04, RES-07 | search past cases and compare recurring situations | todo |
| COK-09 | Safety-boundary demonstration view | P1 | M09 | Member 3 | COK-07, SAF-04 | a blocked high-impact action is shown with the guard's reason | todo |

### A04 — Anomaly & Situation Detection (DET)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| DET-01 | Deterministic detection rules for workload imbalance and thermal pressure | P0 | M03 | Member 2 | DAT-05 | transparent rules or statistics with documented thresholds · unit tests on labelled traces | todo |
| DET-02 | Case creation with persistence thresholds, deduplication, cooldowns and a priority queue | P0 | M03 | Member 2 | DET-01, PLT-07 | repeated signals create one case; cooldown respected · tests | todo |
| DET-03 | Evidence collection | P0 | M03 | Member 2 | DET-02, DAT-06 | relevant time windows, topology, workload context and telemetry quality attached as references | todo |
| DET-04 | Injected-condition acceptance test | P0 | M03 | Member 2 | DET-02, DET-03 | the known injected condition reliably opens a case; normal data does not | todo |
| DET-05 | Noise-control tuning | P1 | M09 | Member 2 | DET-04, EVL-07 | low-value cases suppressed · false positives reported | todo |
| DET-06 | Optional machine-learning anomaly model | P2 | M11 | Member 2 | DET-05 | added only if it contributes clear value over the rules | todo |

### A05 — Forecasting & Capacity (FOR)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| FOR-01 | Baseline forecasting model | P0 | M04 | Member 2 | DAT-03 | forecasts workload and resource pressure on replayed traces · tests | todo |
| FOR-02 | Comparison with simple baselines | P0 | M04 | Member 2 | FOR-01 | compared with naive and seasonal baselines; unreliable regions described | todo |
| FOR-03 | Capacity-risk and SLA-impact estimate | P1 | M06 | Member 2 | FOR-01, OPT-02 | estimates labelled ESTIMATED with uncertainty | todo |
| FOR-04 | Dedicated forecasting model on a cloud ML service | P2 | M11 | Member 2 | FOR-02, CLD-08 | only if it beats the baseline of FOR-02; result recorded either way | todo |

### A06 — Operating Researcher (RES)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| RES-01 | Researcher architecture and the ResearchCase, Hypothesis, ExperimentSpec and ExperimentResult contracts | P0 | M01 | Member 2 | DAT-01 | one deterministic orchestrator with stages for discovery, evidence, hypotheses, experiment selection, simulation, verification and memory · schemas, fixtures and tests | todo |
| RES-02 | Competing falsifiable hypotheses | P0 | M04 | Member 2 | RES-01, DET-03 | two or more per case, each with supporting, weakening and missing evidence; abstains when data is insufficient | todo |
| RES-03 | Deterministic hypothesis validator | P0 | M04 | Member 2 | RES-02 | rejects invalid schemas and evidence references that do not exist · tests | todo |
| RES-04 | Experiment candidates and information-value ranking | P0 | M07 | Member 2 | RES-02, TWN-05, OPT-01 | ranks by ability to distinguish hypotheses, relevance, cost and risk · ranking tests | todo |
| RES-05 | Research budget, stop conditions and cooldowns | P0 | M07 | Member 2 | RES-04 | selection reason, budget and seed recorded for every experiment; budget exhaustion stops research | todo |
| RES-06 | Verification stage | P0 | M08 | Member 2 | RES-05, OPT-02 | baseline versus candidate comparison, constraint check, uncertainty, model mismatch and limitations recorded | todo |
| RES-07 | Research memory | P0 | M08 | Member 2 | RES-06, PLT-08 | stores cases, configurations, outcomes, failures and applicability limits; searchable | todo |
| RES-08 | Safe pause and queue on cloud loss | P1 | M09 | Member 2 | RES-05, SAF-03 | research pauses or queues and later resumes · test | todo |
| RES-09 | Ablation switches | P1 | M10 | Member 2 | RES-07 | switches for no active selection, no competing hypotheses, no research memory and no uncertainty reporting | todo |
| RES-10 | LLM-assisted hypothesis drafting and explanations | P2 | M11 | Member 2 | RES-03 | an LLM may draft; deterministic validators still gate every output; evidence references required | todo |

### A07 — Digital Twin Scenario Lab (TWN)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| TWN-01 | Scenario definition: workload imbalance and thermal pressure | P0 | M01 | Member 3 | — | one scenario with the injected condition, expected behaviour and acceptance check, agreed by the team | todo |
| TWN-02 | Simulator foundation decision | P0 | M01 | Member 3 | TWN-01 | build or adopt (for example OpenDC) with license and fit verified · recorded as an ADR | todo |
| TWN-03 | Workload replay engine | P0 | M05 | Member 3 | TWN-02, DAT-03 | a baseline run repeats from a saved seed and configuration | todo |
| TWN-04 | Simplified power and thermal model | P0 | M05 | Member 3 | TWN-02 | assumptions visible; outputs labelled SIMULATED; not CFD-grade | todo |
| TWN-05 | Experiment runner | P0 | M05 | Member 3 | TWN-03, TWN-04 | bounded, resource-limited, reproducible configurations; sandbox only | todo |
| TWN-06 | Model-mismatch and sensitivity analysis | P1 | M06 | Member 3 | TWN-05 | compares simulation with available measured or replayed observations; sensitivity to assumptions reported | todo |
| TWN-07 | Repeatability tests | P1 | M10 | Member 3 | TWN-05 | the same seed and configuration give identical results across runs | todo |

### A08 — Workload & Resource Optimization (OPT)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| OPT-01 | Candidate placement and scheduling alternatives | P0 | M06 | Member 2 | DET-03, TWN-05 | explainable alternatives for the scenario · tests | todo |
| OPT-02 | Hard-constraint model | P0 | M06 | Member 2 | DAT-06 | capacity, SLA, thermal and energy constraints; rejected candidates carry reasons · tests | todo |
| OPT-03 | Energy and thermal trade-off scoring | P0 | M06 | Member 2 | OPT-01, TWN-04 | scores labelled ESTIMATED or SIMULATED; cooling suggestions stay advisory | todo |
| OPT-04 | Conventional optimizer baseline for System A | P0 | M06 | Member 2 | OPT-02 | documented conventional optimizer used by System A | todo |
| OPT-05 | Candidate actions executed in the experiment runner | P1 | M07 | Member 3 | OPT-01, TWN-05 | candidates run in the sandbox and feed verification; paired with Member 2 | todo |

### A09 — Decision & Governance (DEC)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| DEC-01 | DecisionCertificate contract | P0 | M01 | Member 1 | DAT-01 | schema, fixture and tests; fields for recommendation, rationale, evidence, uncertainty, trade-offs, constraints, assumptions, limitations and review state | todo |
| DEC-02 | Decision Certificate generator | P0 | M08 | Member 2 | DEC-01, RES-06 | certificate generated from verified results with uncertainty and limitations · schema validation test | todo |
| DEC-03 | Operator review states | P0 | M08 | Member 3 | DEC-01, PLT-07 | accept, reject, defer or request investigation, recorded with outcome and timestamp | todo |
| DEC-04 | Case outcome and applicability limits | P1 | M08 | Member 2 | RES-07, DEC-03 | outcome stored for future investigations | todo |
| DEC-05 | Approval and allowlist design for any future execution | P1 | M09 | Member 1 | SAF-01, DEC-03 | written design with explicit approval, policy allowlists, rollback planning and independent local enforcement; nothing executes in the MVP | todo |

### A10 — Safety Guard (SAF)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| SAF-01 | Safety boundary specification | P0 | M01 | Member 1 | — | lists blocked actions (cooling plant, UPS, switchgear, power distribution, server shutdown or reboot, production migration) and the advisory and sandbox actions | todo |
| SAF-02 | Local Safety Guard | P0 | M09 | Member 1 | SAF-01, DEC-01 | deterministic validators for schemas, experiment limits and safety constraints; independent of any LLM; deny by default · tests | todo |
| SAF-03 | Guard and monitoring survive cloud loss | P0 | M09 | Member 1 | SAF-02 | local monitoring and the guard keep working with the cloud unreachable · automated test | todo |
| SAF-04 | Blocked high-impact action is audited | P0 | M09 | Member 1 | SAF-02, PLT-08 | an attempted high-impact action is refused and recorded with the rule | todo |
| SAF-05 | No model output can override the guard | P1 | M09 | Member 1 | SAF-02 | tests with adversarial model outputs · guard decision unchanged | todo |
| SAF-06 | Safety and resilience test report | P1 | M10 | Member 1 | SAF-03, SAF-04 | blocked unsafe actions, permission boundaries, missing or invalid data, cloud interruption, audit completeness | todo |

### A11 — Evaluation (EVL)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| EVL-01 | Evaluation protocol and pre-registered metrics | P0 | M01 | Member 2 | — | metrics per dimension, A/B/C definitions and the core pass condition recorded before any result | todo |
| EVL-02 | Baseline workflow, scenario and seed set | P0 | M01 | Member 2 | EVL-01, TWN-01 | System A defined; scenarios, seeds, constraints and compute budgets fixed | todo |
| EVL-03 | Experiment harness | P0 | M05 | Member 2 | EVL-02, TWN-05 | identical traces, initial states, seeds, constraints and disclosed budgets; one reproducible command | todo |
| EVL-04 | Run Systems A, B and C on matched scenarios | P0 | M10 | Member 2 | EVL-03, OPT-04, RES-09 | results for all three systems recorded with seeds and configurations | todo |
| EVL-05 | Ablations | P0 | M10 | Member 2 | EVL-04, RES-09 | no active selection, no competing hypotheses, no research memory, no uncertainty reporting | todo |
| EVL-06 | Evaluation report | P0 | M10 | Member 2 | EVL-04, EVL-05 | measured, replayed, estimated and simulated values labelled; failed cases and negative results included | todo |
| EVL-07 | Detection usefulness on labelled scenarios | P1 | M04 | Member 2 | DET-04 | surfaced, missed and noisy cases reported | todo |
| EVL-08 | Diagnosis quality | P1 | M10 | Member 2 | EVL-04 | hypotheses compared with known scenario causes; correct, incorrect and inconclusive counted | todo |
| EVL-09 | Competitor edition and prior-art review | P1 | M10 | Member 3 | — | EcoStruxure IT, Turbonomic, Dynatrace, DeepMind cooling work and OpenDC reviewed by edition; differentiation wording checked | todo |
| EVL-10 | Commercial viability feedback | P1 | M10 | Member 3 | UXV-02 | mentor and user feedback on fit, deployment, integration burden and willingness to pay recorded as assumptions | todo |

### A12 — Cloud & Packaging (CLD)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| CLD-01 | Cloud readiness check | P0 | M01 | Member 1 | — | account access, region, quotas, credits and availability of ECS, RDS for PostgreSQL and OBS confirmed in writing | todo |
| CLD-02 | ECS deployment of backend and dashboard | P0 | M09 | Member 1 | CLD-01, PLT-02 | stack reachable over a secured endpoint · external reachability test | todo |
| CLD-03 | RDS for PostgreSQL provisioning and migrations | P0 | M09 | Member 1 | CLD-01, PLT-04 | private connectivity; migrations applied; database not publicly exposed | todo |
| CLD-04 | OBS for traces, simulation outputs and reports | P1 | M09 | Member 1 | CLD-01, TWN-03 | artifacts stored and retrieved by the platform; access limited | todo |
| CLD-05 | Repeatable deployment scripts and local container fallback | P0 | M09 | Member 1 | CLD-02, CLD-03 | clean redeploy succeeds; the demo also runs locally with containers | todo |
| CLD-06 | Access control and audit for cloud operations | P1 | M09 | Member 1 | CLD-02 | only the exact supported IAM, CTS and monitoring features are used; documented | todo |
| CLD-07 | Service status labels and deployment evidence | P1 | M10 | Member 1 | CLD-05 | each Huawei Cloud service labelled implemented, planned or optional; dated logs and screenshots without secrets | todo |
| CLD-08 | ModelArts compatibility and value test | P2 | M11 | Member 1 | CLD-01 | only for a justified machine-learning task; outcome recorded | todo |
| CLD-09 | MaaS and Pangu models compatibility test | P2 | M11 | Member 1 | CLD-01 | only for drafting and explanations; deterministic code keeps calculations and safety checks | todo |
| CLD-10 | Container orchestration and cache | P2 | M11 | Member 1 | CLD-05 | CCE or DCS only if deployment complexity requires it | todo |
| CLD-11 | Cost and quota tracking | P1 | M10 | Member 1 | CLD-01 | note updated at each milestone | todo |

### A13 — AI Development Assistants (DEV)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| DEV-01 | Evaluate AI development assistants | P1 | M01 | Member 1 | — | tool-agnostic note on capabilities, permissions and constraints; any provider-offered assistant is a candidate | todo |
| DEV-02 | Operating rules for assistants | P1 | M01 | Member 1 | DEV-01 | restricted permissions; human confirmation for resource creation; review and tests before merge | todo |
| DEV-03 | Evidence log of assisted work | P1 | M05 | Member 1 | DEV-02 | recorded cycles for requirements, code, tests, debugging and documentation | todo |
| DEV-04 | Separation check | P1 | M09 | Member 1 | DEV-02 | assistants are not part of the product runtime, the Researcher or the Safety Guard | todo |

### A14 — Security & Data Protection (SEC)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| SEC-01 | Data-handling policy | P0 | M01 | Member 1 | — | data permissioned, minimized and protected; synthetic data only in the public repository | todo |
| SEC-02 | Secrets and configuration baseline | P0 | M02 | Member 1 | SEC-01 | secrets only from the environment or a secret store, none in the repository · scan passes | todo |
| SEC-03 | Threat model | P1 | M09 | Member 1 | SEC-01 | tampered telemetry, forged evidence, prompt injection on model paths, unauthorized approvals | todo |
| SEC-04 | Secret and dependency scanning in CI | P1 | M09 | Member 1 | OPS-05, SEC-02 | scans run on pull requests | todo |
| SEC-05 | Audit completeness check | P1 | M09 | Member 1 | PLT-08 | every decision, experiment and guard event has an audit record | todo |

### A15 — Repository, Automation & Docs (OPS)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| OPS-01 | Repository skeleton and conventions | P0 | M01 | Member 1 | — | layout, ignore files, editor config and `.env.example` · every referenced path exists | todo |
| OPS-02 | Tracking contract and parser | P0 | M01 | Member 1 | OPS-01 | validates IDs, dependencies, owners, statuses and milestones · unit tests including malformed tables | todo |
| OPS-03 | Status generator | P0 | M01 | Member 1 | OPS-02 | generates badges, bars, task map and milestone cards and refreshes README blocks · golden tests | todo |
| OPS-04 | `progress.yml` workflow | P0 | M01 | Member 1 | OPS-03 | loop-safe, fork-safe, minimal permissions · dry run passes locally; GitHub run recorded separately | todo |
| OPS-05 | `pr-checks.yml` workflow | P0 | M01 | Member 1 | OPS-01 | tracking validation, lint and tests on every pull request; frontend build when it changes | todo |
| OPS-06 | Code quality tooling | P1 | M01 | Member 1 | OPS-05 | lint, format and type checks per stack | todo |
| OPS-07 | README, setup.md and docs index | P0 | M01 | Member 1 | OPS-03 | required sections present; setup matches the actual commands | todo |
| OPS-08 | Commit convention and pull request template | P0 | M01 | Member 1 | — | documentation and template in place | todo |
| OPS-09 | Workflow documentation and tests | P1 | M01 | Member 1 | OPS-04 | triggers, permissions and fork behaviour documented | todo |
| OPS-10 | License file and notices | P0 | M01 | Member 1 | — | all-rights-reserved notice for The SYNTRIX authors; written ownership agreement among members still pending | todo |
| OPS-11 | Architecture Decision Records | P1 | M01 | Member 1 | OPS-01 | template and first records | todo |
| OPS-12 | Demo package and evidence index | P1 | M10 | Member 1 | CLD-07, EVL-06 | script, architecture diagram, recording and evidence index | todo |

### A16 — Usability & Demo (UXV)

| ID | Task | Pri | MS | Owner | Depends | Done when | Status |
|---|---|---|---|---|---|---|---|
| UXV-01 | Operator user journey | P0 | M01 | Member 3 | TWN-01 | roles, tasks and the nine-step demo story documented | todo |
| UXV-02 | Usability checks | P1 | M10 | Member 3 | COK-07 | task completion, clarity of recommendations and whether the certificate supports review observed with users | todo |
| UXV-03 | End-to-end acceptance test of the demo flow | P0 | M09 | Member 3 | COK-07, SAF-04, DET-04 | one scripted run covers connection to decision and passes repeatedly | todo |
| UXV-04 | Demo script and recording | P0 | M10 | Member 3 | UXV-03 | nine-step story rehearsed and recorded; every value labelled measured, replayed, estimated or simulated | todo |
| UXV-05 | Honest limitations section | P0 | M10 | Member 3 | EVL-06 | limitations, failed cases and assumptions documented for the presentation | todo |
