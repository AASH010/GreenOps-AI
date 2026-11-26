# Contributing

Two standards apply to every change: the **commit convention** and the **pull request template**. Work happens through forks; branches are prefixed by area (`backend/…`, `frontend/…`, `contracts/…`, `docs/…`).

## Commit convention

Format: `type(scope): short imperative summary`, with an optional body and footer.

```
feat(backend): validate telemetry units on ingestion
fix(frontend): show the provenance label on every KPI

Refs: DAT-03
```

**Types:** `feat` new capability · `fix` bug fix · `docs` documentation · `style` formatting only · `refactor` no behaviour change · `test` tests only · `perf` performance · `build` build or dependencies · `ci` workflows · `chore` maintenance.

**Scopes:** `backend`, `frontend`, `contracts`, `experiments`, `data`, `cloud`, `docker`, `docs`, `tracking`, `ops`.

**Rules**
- Imperative mood; summary up to about 72 characters.
- Explain *why* in the body when it is not obvious.
- One logical change per commit.
- Mention task IDs in a `Refs:` footer.
- Mark breaking contract changes with `!` (for example `feat(contracts)!: rename a field`) and a `BREAKING CHANGE:` footer.
- A task is finished by editing its status in `TRACKING.md` in the same pull request (`docs(tracking): mark DAT-01 done`), not by the commit message alone.
- `chore(status): …` commits are reserved for the automation (see `workflows.md`).

| Correct | Incorrect |
|---|---|
| `fix(backend): reject percent values above 100` | `fixed stuff` |
| `feat(frontend): add the case detail view` | `Added the feature of cases.` |
| `docs(tracking): mark SEC-01 done` | `update` |
| `test(contracts): cover the certificate invariants` | `tests and some refactoring and docs` |

## Pull request template

The template lives in [`.github/pull_request_template.md`](../.github/pull_request_template.md) and is applied automatically. It covers: title, description, purpose, related tasks, implemented changes, testing, documentation updates, potential breaking changes, integration considerations and the completion checklist.
