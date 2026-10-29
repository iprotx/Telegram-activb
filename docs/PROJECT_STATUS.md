# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** `main`
- **Current main HEAD:** `fe25dba738f8201646772f6f8409c9d77c088705` — merge of PR #31.
- **Latest merged work:** PR #30 adds Docker runtime smoke coverage; PR #31 records the minimal architecture-cleanup plan. PR #31 itself did not change application code.
- **Current product shape:** production-oriented aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates.
- **Current engineering task:** `refactor/config-settings-boundary` separates database configuration from the required Telegram bot token while preserving validation and environment precedence.

## Architecture and constraints

- Preserve `handlers → services → repositories → database infrastructure`.
- Keep activity/XP policy in services and persistence in repositories.
- Do not change middleware transaction scope without dedicated regression tests and a clear rollback contract; see [issue #32](https://github.com/iprotx/Telegram-activb/issues/32).
- Keep product behavior deterministic; no AI/LLM/model calls or external AI services.
- Do not add infrastructure without measured need.

## Reliability and verification

- **User profile synchronization and registration concurrency:** covered by unit and PostgreSQL integration tests.
- **Activity policy dependency direction:** corrected in PR #21.
- **Configuration and Alembic URL alignment:** PR #24; environment variables continue to override `.env`.
- **PostgreSQL uniqueness/concurrency:** PR #25.
- **Safe error logging:** PR #28.
- **Startup/import safety:** PR #29.
- **Docker runtime smoke and migration validation:** PR #30; CI runs formatting, lint, mypy, migrations, unit tests, PostgreSQL integration tests, Alembic drift check, dependency audit, Docker build, and runtime smoke.
- **Architecture cleanup:** PR #31 added the plan only. The current branch makes a narrowly scoped configuration refactor; runtime transaction boundaries and activity semantics remain unchanged.

## Current backlog

- [ ] **#32 — Transaction boundary investigation.** Determine whether any transaction scope change is warranted; retain current behavior unless evidence justifies a change.
- [ ] **Configuration refactor CI/review.** Verify the current branch with all configured quality gates before considering it ready.
- [ ] **Product scope.** The research plan lists deterministic candidates such as `/rank` and `/top`; these remain separate from architecture cleanup.

## Evidence rules

1. A task is **Done** only with concrete evidence: tests, CI, a merged commit, or an explicit architectural decision.
2. CI green means configured checks passed; it does not by itself prove production readiness.
3. Merge and deployment remain explicit human decisions.
4. Keep this page concise and reconcile it after meaningful work.

## Links

- [Engineering rules](../AGENTS.md)
- [Architecture cleanup plan](superpowers/plans/2026-10-29-architecture-cleanup.md)
- [Decision log](DECISIONS.md)
- [Worklog](WORKLOG.md)
