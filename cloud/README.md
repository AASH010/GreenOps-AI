# cloud/

Deployment scripts and environment notes for Huawei Cloud (area A12). **Nothing is provisioned yet.**

## Readiness checklist (task CLD-01 — complete before any provisioning)
- [ ] Account access confirmed
- [ ] Region chosen; availability of ECS, RDS for PostgreSQL and OBS confirmed there
- [ ] Instance specifications and quotas confirmed
- [ ] Credits or budget and competition eligibility of the services confirmed
- [ ] One person owns provisioning at a time

## Service status (update as work proceeds; each service is labelled in the final presentation)
| Service | Planned role | Status |
|---|---|---|
| ECS | Host the backend and cockpit | planned |
| RDS for PostgreSQL | Primary structured data store | planned |
| OBS | Traces, simulation outputs, model artifacts, reports | planned |
| IAM / CTS | Access control and audit for supported cloud operations | planned |
| AOM / Cloud Eye, VPC | Monitoring and networking, only the exact supported features used | planned |
| ModelArts | Forecasting or anomaly models, only if justified | optional |
| MaaS / Pangu models | Hypothesis drafting and explanations, only after compatibility is tested | optional |
| CCE / DCS | Orchestration or cache, only if deployment complexity requires it | optional |
| CodeArts Agent | Team development productivity, not the product runtime | optional |

A local container fallback is kept so the demo can run without optional services.

## Rules
- Do not expose database ports publicly; restrict inbound traffic; apply least privilege.
- Credentials never go into the repository; supply them through the environment or a secret store.
- Deployment commands are added here only after they have been run successfully.
