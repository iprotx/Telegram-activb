# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** `main`
- **Current main HEAD:** `5eb3b3d02453bf98af3c8c3aa2d95c6c4e9ddcad` — merge of PR #28.
- **Latest merged work:** PR #28 adds error middleware regression coverage; PR #27 adds the research plan for deterministic, non-AI chat features.
- **Current product shape:** production-oriented aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose and CI quality gates.

## Product feature research

- **Direction:** evaluate activity/XP, chat moderation, and admin utilities using deterministic rules only; no AI/LLM/model integration or external AI service.
- **Plan:** [Non-AI chat bot feature research](superpowers/plans/2026-10-29-chat-bot-feature-research.md).
- **Status:** comparison research and prioritization are planned; no candidate feature has been approved or implemented by this research.
- **Engineering order:** finish the remaining reliability backlog (#14, #16), then whole-branch architecture review and release-readiness verification before expanding runtime scope.

## Reconciled hardening status

| Iteration | Status | Evidence / result |
| --- | --- | --- |
| 0. Baseline and documentation consistency | Done | PR #17 established the maintained project-management documentation and reconciled README/local skill references. |
| 1. User profile synchronization | Done | Implemented and covered by tests; repeated registration preserves identity and updates Telegram profile fields. |
| 2. `/start` behavior | Done | Dedicated handler tests cover normal users and missing optional profile fields. |
| 3. Middleware transaction boundaries | Done | Commit/rollback behavior is covered, including PostgreSQL rollback integration coverage. |
| 4. User schema/migrations | Done | PR #25 verifies PostgreSQL uniqueness and nullable profile fields; Alembic checks are part of CI. |
| 5. Error boundary and safe logging | Done | PR #28 merged as `5eb3b3d02453bf98af3c8c3aa2d95c6c4e9ddcad`; issue #13 closed. CI run `40868768340` passed all configured gates for the regression tests. |
| 6. Configuration and startup validation | In review | PR #29 adds import-side-effect, dispatcher wiring, and cleanup tests; CI run `40869999942` passed all configured quality gates. Merge pending. |
| 7. User repository concurrency/idempotence | Done | PR #25 adds dedicated PostgreSQL concurrency coverage for `get_or_create`. |
| 8. Docker runtime smoke path | Not started | CI builds the image, but there is no verified container startup smoke test. See #16. |
| 9. CI quality gate hardening | Done | Current CI covers formatting, lint, mypy, migrations, tests, PostgreSQL integration tests, Alembic drift, dependency audit and Docker build. |
| 10. Whole-branch architecture review | In progress | PR #21 fixed the known activity repository → service dependency violation. A final whole-branch review after the latest database/CI changes is still required. |
| 11. Final verification and merge readiness | Not started | Requires the remaining gaps and final architecture review to be resolved first. |

## Confirmed remaining backlog

### P1 — Production-hardening gaps

- [ ] **#14 — Configuration/startup verification.** PR #29 adds startup/import-side-effect, dispatcher wiring, and polling-failure cleanup tests; CI run `40869999942` passed all configured gates. Awaiting review/merge.
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
