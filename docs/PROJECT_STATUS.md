# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** `main`
- **Latest merged work:** PR #33 separated database settings from bot credentials; merge commit [ec6ad18](https://github.com/iprotx/Telegram-activb/commit/ec6ad18c7477508f3854ff32308dc897f3c94658).
- **Current product shape:** aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates.
- **Current engineering task:** issue #32 transaction-boundary investigation. Findings are recorded on branch `investigation/transaction-boundaries`; no production transaction changes are recommended.

## Architecture and constraints

- Preserve `handlers → services → repositories → database infrastructure`.
- Keep activity/XP policy in services and persistence in repositories.
- Preserve update-level atomicity for registration + activity unless a tested transaction API replaces it.
- Keep product behavior deterministic; no AI/LLM/model calls or external AI services.
- Do not add infrastructure without measured need.

## Reliability and verification

- **Registration concurrency and nullable profile fields:** unit and PostgreSQL integration coverage.
- **Activity policy dependency direction:** corrected in PR #21.
- **Configuration/Alembic URL:** PR #24 and PR #33; `BOT_TOKEN` remains required by the app while Alembic can load DB settings independently.
- **Safe error logging:** PR #28.
- **Startup/import safety:** PR #29.
- **Docker runtime smoke and migration validation:** PR #30.
- **Transaction boundaries:** existing unit tests cover commit/rollback, and a PostgreSQL integration test confirms rollback when a handler fails. Investigation found one external Telegram call inside a transaction (`/start` response); current evidence does not justify changing the transaction contract.

## Current backlog

- [ ] **Product features:** implement deterministic `/rank`, then `/top`, each in a separate branch with unit and PostgreSQL coverage.
- [ ] **Operational evidence:** if transaction duration or lock contention becomes a measured issue, revisit the decision in `docs/DECISIONS.md`.

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
- [Issue #32](https://github.com/iprotx/Telegram-activb/issues/32)
