# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** `main`
- **Current main HEAD:** `1c5bb9f7ac936fd999e741d38cfd07366a7ac405` — merge of PR #25.
- **Latest merged work:** PostgreSQL integration verification for user uniqueness, nullable profile fields, and concurrent registration.
- **Current product shape:** production-oriented aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose and CI quality gates.

## Reconciled hardening status

| Iteration | Status | Evidence / result |
| --- | --- | --- |
| 0. Baseline and documentation consistency | Done | PR #17 established the maintained project-management documentation and reconciled README/local skill references. |
| 1. User profile synchronization | Done | Implemented and covered by tests; repeated registration preserves identity and updates Telegram profile fields. |
| 2. `/start` behavior | Done | Dedicated handler tests cover normal users and missing optional profile fields. |
| 3. Middleware transaction boundaries | Done | Commit/rollback behavior is covered, including PostgreSQL rollback integration coverage. |
| 4. User schema/migrations | Done | PR #25 verifies PostgreSQL uniqueness and nullable profile fields; Alembic checks are part of CI. |
| 5. Error boundary and safe logging | In review | PR #28 adds tests for re-raise, diagnostic context/traceback, and exclusion of token/update sentinels from logs; CI run `40868768340` passed. Merge pending. |
| 6. Configuration and startup validation | In progress | Configuration validation is covered; a dedicated import/startup test is still missing. See #14. |
| 7. User repository concurrency/idempotence | Done | PR #25 adds dedicated PostgreSQL concurrency coverage for `get_or_create`. |
| 8. Docker runtime smoke path | Not started | CI builds the image, but there is no verified container startup smoke test. See #16. |
| 9. CI quality gate hardening | Done | Current CI covers formatting, lint, mypy, migrations, tests, PostgreSQL integration tests, Alembic drift, dependency audit and Docker build. |
| 10. Whole-branch architecture review | In progress | PR #21 fixed the known activity repository → service dependency violation. A final whole-branch review after the latest database/CI changes is still required. |
| 11. Final verification and merge readiness | Not started | Requires the remaining gaps and final architecture review to be resolved first. |

## Confirmed remaining backlog

### P1 — Production-hardening gaps

- [ ] **#13 — Error boundary and safe logging.** Add focused tests for exception re-raise, useful diagnostic context, and absence of bot tokens/full Telegram payloads in logs.
- [ ] **#14 — Configuration/startup verification.** Add startup/import-side-effect coverage and confirm safe failure behavior for invalid configuration.
- [ ] **#16 — Docker runtime smoke.** Verify the documented container path actually starts with declared environment/configuration rather than only building successfully.
- [ ] **#18 — Architecture refactor.** The implementation is already merged in PR #21; the issue itself is now stale and should be closed/updated after this reconciliation.

### P2 — Release readiness

- [ ] Define the intended first release scope and operator acceptance criteria.
- [ ] Verify clean deployment from documented setup with required environment variables and a fresh database.
- [ ] Record remaining operational limitations before calling the bot production-ready.

## Evidence rules

1. A task is **Done** only when the repository contains concrete evidence: tests, CI, a merged commit, or an explicit architectural decision.
2. `PROJECT_STATUS.md` is the current human-readable snapshot; the detailed implementation plan remains the execution protocol and must not be treated as evidence by itself.
3. CI green means the configured checks passed; it does not by itself prove deployment or production readiness.
4. Merge and deployment remain explicit human decisions.

## Working agreements

1. Start each substantial task with a written mini-plan: goal, scope, assumptions, risks/dependencies, and acceptance criteria.
2. Work in bounded steps. Before starting a new step, report the prior step's result and unresolved items.
3. Never mark an item done without concrete evidence (tests, CI link, diff, or explicit decision).
4. Prefer GitHub issues for actionable backlog items; keep this document as the human-readable overview.
5. Update this status file and the work log at the end of each meaningful task/PR.
6. Do not merge PRs or perform destructive/release actions without explicit user approval.
7. Final reports must separate changed, verified, not verified, risks/blockers, and next step.

## Links

- [Engineering rules](../AGENTS.md)
- [Production-hardening implementation plan](superpowers/plans/2026-10-29-production-hardening.md)
- [Decision log](DECISIONS.md)
- [Worklog](WORKLOG.md)
