# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** main
- **Latest merged change:** PR #10, `fix: harden activity timestamp and concurrency handling`
- **Latest merged commit:** `ad20f34c46db52e8d1da9b5a5eba8d83d33cf008`
- **CI evidence for PR #10:** [run 40845554427](https://github.com/iprotx/Telegram-activb/actions/runs/40845554427) — success.
- **Current product shape:** production-oriented aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose and CI quality gates.

## Recently completed

- [x] Merge PR #8: activity levels and database migration conflict resolution.
- [x] Merge PR #10: normalize activity timestamps to UTC, use timezone-aware `last_xp_at`, handle concurrent first-message creation, and add activity repository integration tests.
- [x] Verify PR #10 CI passed: Ruff format/lint, mypy, tests, Alembic checks, dependency audit and Docker build were green in the completed workflow.
- [x] Preserve architecture boundaries documented in `AGENTS.md`: handlers → services → repositories → database infrastructure.

## In progress

- [ ] Establish a maintained project-management layer: status, roadmap, decision log, and work log. This PR creates the initial baseline; review it against the existing implementation plan before treating all roadmap entries as current truth.

## Prioritized backlog

These are engineering follow-ups drawn from the existing production-hardening plan in `docs/superpowers/plans/2026-10-29-production-hardening.md`. The plan has older unchecked boxes and must be reconciled against current code before work is claimed complete.

### P0 — Reconcile the implementation plan

- [ ] Audit each plan iteration against current source, tests, migrations, and CI evidence.
- [ ] Update stale checkboxes and obsolete descriptions; do not infer completion from a file merely existing.
- [ ] Convert confirmed remaining work into bounded GitHub issues or explicit roadmap tasks with acceptance criteria.

**Acceptance:** every plan iteration has one of: Done (with evidence), In progress, Blocked (with reason), or Not started.

### P1 — Close remaining production-hardening gaps

Candidate work items from the existing plan; status intentionally remains unverified until the P0 audit:

- [ ] User profile synchronization on repeated registration.
- [ ] Explicit `/start` behavior coverage, including missing optional profile fields.
- [ ] Middleware transaction commit/rollback tests.
- [ ] User schema/constraint integration coverage and clean-database migration verification.
- [ ] Error-boundary tests and safe logging review.
- [ ] Configuration/startup validation and import-side-effect tests.
- [ ] User repository duplicate-registration concurrency test.
- [ ] Docker runtime smoke test, beyond image build.
- [ ] Verify CI gates match contributor documentation.
- [ ] Whole-branch architecture/security review.

### P2 — Release readiness

- [ ] Define the intended first release scope and operator acceptance criteria.
- [ ] Verify clean deployment from documented setup with required environment variables and a fresh database.
- [ ] Record any remaining operational limitations before calling the bot production-ready.

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
- [Work log](WORKLOG.md)
