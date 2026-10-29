# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** `main`
- **Latest merged work:** PR #34 recorded the transaction-boundary investigation; merge commit [42ca52a](https://github.com/iprotx/Telegram-activb/commit/42ca52a4855b71eb08f1282ed0ac35ae5500a064).
- **Current product shape:** aiogram bot with user registration, per-chat activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates.
- **Latest product feature:** `/rank` merged in PR #35 ([merge commit](https://github.com/iprotx/Telegram-activb/commit/1a29867759a338c15dfddcce075d87bbc09bd4c6)); implementation CI run [#215](https://github.com/iprotx/Telegram-activb/actions/runs/40892928139) passed all configured checks.

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
- **Transaction boundaries:** PR #34 documented why the existing update-level transaction is retained; issue #32 investigation completed.
- **Rank command:** merged in PR #35; CI run #215 passed Ruff format/lint, mypy, migrations, unit tests, PostgreSQL integration tests, Alembic check, dependency audit, Docker build and runtime smoke.
- **Top command:** in progress on branch `feat/top-command`; bounded query, deterministic ordering and chat isolation are covered by new unit/SQLite integration tests. CI pending.

## Current backlog

- [ ] **`/top`:** finish implementation, verify CI and review PR before merge.
- [ ] **Operational evidence:** if transaction duration or lock contention becomes a measured issue, revisit the decision in `docs/DECISIONS.md`.

## Evidence rules

1. A task is **Done** only with concrete evidence: tests, CI, a merged commit, or an explicit architectural decision.
2. CI green means configured checks passed; it does not by itself prove production readiness.
3. Merge and deployment remain explicit human decisions.
4. Keep this page concise and reconcile it after meaningful work.

## Links

- [Engineering rules](../AGENTS.md)
- [Architecture cleanup plan](superpowers/plans/2026-10-29-architecture-cleanup.md)
- [Feature research plan](superpowers/plans/2026-10-29-chat-bot-feature-research.md)
- [Decision log](DECISIONS.md)
- [Worklog](WORKLOG.md)
