# Development Setup

This file covers everything needed to work on the repository **as it exists today**: the backend skeleton, the frontend skeleton, the contracts and the tracking scripts. Nothing is deployed to the cloud yet, and the container files have not been run (see sections 9 and 10).

Commands below were run on Linux unless stated otherwise. Values marked **(owner)** must be supplied by the project owner. Never commit real secrets, tokens or passwords.

## 1. Prerequisites
- A GitHub account and a fork of the upstream repository (work happens through forks).
- A terminal with Bash (Linux or macOS; Windows users can use WSL).

## 2. Required Software
| Software | Used for |
|---|---|
| Git | Version control |
| Python | Backend, tracking scripts, tests |
| Node.js and npm | Frontend |
| Docker with the Compose plugin | Optional: local container stack. **Not run in the validation environment** |
| Huawei Cloud account | Not needed yet; required from the deployment tasks (see section 9) |

## 3. Required Versions
| Software | Version used for validation |
|---|---|
| Python | 3.12 (tested with 3.12.3) |
| Node.js | 22 (tested with v22.23.5) |
| npm | 10 (tested with 10.9.9) |
| Git | any recent version (tested with 2.43.0) |
| Docker | any recent version; **untested** |

Dependency versions are pinned in `requirements-dev.txt`, `backend/requirements.txt` and `frontend/package-lock.json`.

## 4. Repository Setup
```bash
git clone <your-fork-url> GreenOpsAI                 # your fork
cd GreenOpsAI
git remote add upstream <upstream-repository-url>    # (owner) the URL of the main repository
git checkout -b backend/my-change                    # branch prefixes: backend/, frontend/, contracts/, docs/
```

## 5. Installation
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

cd frontend
npm ci
cd ..
```
Use the virtual environment: installing into the system Python can fail with an "externally-managed-environment" error.

## 6. Environment Variables
The backend reads the **process environment**. The variables are defined in `.env.example`:

| Variable | Default | Meaning |
|---|---|---|
| `GREENOPS_ENV` | `development` | `development` or `production` |
| `GREENOPS_API_HOST` | `127.0.0.1` | Address to bind when you pass it to `uvicorn` (section 10) |
| `GREENOPS_API_PORT` | `8000` | Port to bind (integer, 1–65535) |
| `GREENOPS_CORS_ORIGINS` | `http://localhost:5173` | Comma-separated origins allowed to call the API |
| `GREENOPS_DATABASE_URL` | *(empty)* | PostgreSQL URL — **(owner)** supplies it once the database exists (tasks PLT-04, CLD-03). Empty is fine for the skeleton |
| `POSTGRES_USER`, `POSTGRES_DB` | `greenops` | Used only by `docker-compose.yml` |
| `POSTGRES_PASSWORD` | *(none)* | Used only by `docker-compose.yml`; **choose your own local-only value** |

## 7. `.env.example` Configuration
```bash
cp .env.example .env          # .env is git-ignored
set -a; source .env; set +a   # load the variables into the current shell
```

## 8. Database Setup
The backend skeleton needs no database. The schema and migrations arrive with task PLT-04 and the managed database (RDS for PostgreSQL) with CLD-03. For a local database, `docker-compose.yml` defines a PostgreSQL service (section 10) — **generated but not run here**.

## 9. External Services Configuration
Nothing external is required to run what exists today. Later, the **(owner)** supplies:

- **Huawei Cloud:** account access, region, quotas and credits, competition eligibility of the services, and confirmation that ECS, RDS for PostgreSQL and OBS are available in the region. Complete the readiness checklist in `cloud/README.md` first. Credentials come from the environment or a secret store, never from the repository.
- **Optional services** (ModelArts, MaaS / Pangu, CCE, DCS, CodeArts Agent) are only configured if their optional tasks are taken on.

## 10. Running the Project Locally
Backend (from the repository root, virtual environment active, variables loaded):
```bash
cd backend
uvicorn app.main:app --host "${GREENOPS_API_HOST:-127.0.0.1}" --port "${GREENOPS_API_PORT:-8000}"
```
Check it from another terminal:
```bash
curl http://127.0.0.1:8000/health          # {"status":"ok"}
curl http://127.0.0.1:8000/api/v1/meta
```
Interactive API documentation is served at `http://127.0.0.1:8000/docs`.

Frontend:
```bash
cd frontend
npm run dev                                 # http://localhost:5173
```

Containers (optional; **not tested in the validation environment**) — set `POSTGRES_PASSWORD` in `.env` first:
```bash
docker compose up --build
```

## 11. Running Tests
From the repository root with the virtual environment active:
```bash
python -m pytest                            # tracking scripts, backend, contracts
ruff check .
ruff format --check .
python scripts/update_status.py --validate  # TRACKING.md tracking contract
cd frontend && npm run build                # type-check and build the frontend
```

## 12. Development Commands
| Command | Purpose |
|---|---|
| `python scripts/update_status.py --validate` | Check `TRACKING.md` against the tracking contract |
| `python scripts/update_status.py --dry-run` | Print computed progress, milestones and commit activity as JSON; writes nothing |
| `python scripts/update_status.py --write` | Regenerate `assets/status/*.svg` and the README progress and milestone sections |
| `ruff format .` | Format Python code |
| `python -m pytest contracts/tests` | Run only the contract tests |

The README progress and milestone sections are refreshed automatically on `main` (see `docs/workflows.md`). Run `--write` locally only to preview, and do not commit its output on feature branches. When you finish a task, set its status to `done` in `TRACKING.md` in the same pull request. Commit and pull request standards are in `docs/contributing.md`.

## 13. Troubleshooting
| Symptom | Likely cause and fix |
|---|---|
| `externally-managed-environment` when running `pip install` | Install inside the virtual environment (section 5) |
| `ModuleNotFoundError: No module named 'app'` | Run `pytest` from the repository root (`pytest.ini` sets the path), or run `uvicorn` from `backend/` |
| `GREENOPS_API_PORT must be an integer` | Fix the value in `.env` and reload it (section 7) |
| Port already in use | Change `GREENOPS_API_PORT`, or stop the other process |
| `update_status.py` fails with `line N: …` | `TRACKING.md` violates the tracking contract; fix the cited row (IDs, dependencies, owners, statuses, column count) |
| `README markers for PROGRESS not found` | Restore the `<!-- PROGRESS:START -->` and `<!-- PROGRESS:END -->` comments in `README.md` |
| `npm ci` fails because the lock file is out of sync | Run `npm install` in `frontend` and commit the updated `package-lock.json` |
| `docker compose` complains that `POSTGRES_PASSWORD` is not set | Set it in `.env` and load the file (section 7) |

## 14. Common Setup Problems
- **The cockpit cannot reach the API:** make sure the backend is running and `GREENOPS_CORS_ORIGINS` includes the frontend origin (`http://localhost:5173` by default).
- **Tests pass locally but a pull request fails:** the pull request checks also run `ruff check .` and `ruff format --check .`; run both before pushing.
- **The container stack fails to start:** the container files are untested; check `docker compose config`, then open an issue or fix them and record the result in `docs/workflows.md`.
