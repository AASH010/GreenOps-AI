# API documentation

The backend currently exposes two endpoints (skeleton, task PLT-01):

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/api/v1/meta` | Name, version, environment, provenance labels and the prototype notice |

While the server runs, FastAPI serves interactive documentation at `/docs` and the OpenAPI document at `/openapi.json`. The API contract v0 (PLT-03) and the reviewed documentation (PLT-10) arrive with their tasks.
