# backend/

Python + FastAPI **modular monolith** (see ADR 0001). Each module becomes a package under `app/` when its task starts.

| Module | State | Tasks |
|---|---|---|
| `app/main.py`, `app/config.py` | Skeleton: `/health`, `/api/v1/meta`, settings from the environment | PLT-01 |
| `app/provenance.py` | The four provenance labels | DAT-04 |
| `app/ingestion/validation.py` | First draft: validates one telemetry record (fields, provenance, timestamp, metric and unit, percent range, missing values) | DAT-03, DAT-05 |
| `app/safety/guard.py` | First draft: deterministic, deny-by-default action guard with no network or model access | SAF-02 |
| `detection`, `forecasting`, `optimization` | Planned | DET-*, FOR-*, OPT-* |
| `researcher` | Planned: one deterministic orchestrator with stages | RES-* |
| `twin` | Planned: simulator, replay, experiment runner | TWN-* |
| `governance` | Planned: Decision Certificate, review states, audit | DEC-*, PLT-08 |

Drafts are not marked done in `TRACKING.md` until they are reviewed and fully tested. Run the tests from the repository root (`python -m pytest backend/tests`); see `setup.md`.
