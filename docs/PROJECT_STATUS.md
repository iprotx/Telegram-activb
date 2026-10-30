# Project Status

_Last reconciled: 2026-10-30_

## Current snapshot

- **Default branch:** `main`
- **Latest merged work:** PR #37 added group-join welcomes; merge commit [d74820e](https://github.com/iprotx/Telegram-activb/commit/d74820edfdd950fb4a0bb9253fb251ebe7070c25).
- **Current product shape:** aiogram bot with user registration, per-chat activity/XP tracking, `/rank`, `/top`, group-join welcomes, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates.
- **Current branch work:** `hotfix/group-command-routing` prevents the activity fallback from preempting group commands; local Ruff, mypy, and pytest gates pass, while CI, merge, rebuild, and live Telegram verification are pending.

## Architecture and constraints

- Preserve `handlers → services → repositories → database infrastructure`.
- Keep activity/XP policy in services and persistence in repositories.
- Preserve update-level atomicity for registration + activity unless a tested transaction API replaces it.
- Keep product behavior deterministic; no AI/LLM/model calls or external AI services.
- Do not add infrastructure without measured need.

## Reliability and verification

- **Command routing:** a real aiogram dispatch test reproduced `/rank` and `/top` being recorded as activity with no response; the hotfix registers command routers first and excludes slash commands from activity.
- **Registration concurrency and nullable profile fields:** unit and PostgreSQL integration coverage.
- **Activity policy dependency direction:** corrected in PR #21.
- **Configuration/Alembic URL:** PR #24 and PR #33; `BOT_TOKEN` remains required by the app while Alembic can load DB settings independently.
- **Safe error logging:** PR #28.
- **Startup/import safety:** PR #29.
- **Docker runtime smoke and migration validation:** PR #30.
- **Transaction boundaries:** PR #34 documented why the existing update-level transaction is retained; issue #32 investigation completed.
- **Rank command:** merged in PR #35; CI run #215 passed Ruff format/lint, mypy, migrations, unit tests, PostgreSQL integration tests, Alembic check, dependency audit, Docker build and runtime smoke.
- **Top command:** merged in PR #36; CI run [#242](https://github.com/iprotx/Telegram-activb/actions/runs/40894363840) passed Ruff format/lint, mypy, migrations, unit tests, PostgreSQL integration tests, Alembic check, dependency audit, Docker build and runtime smoke.

## Current backlog

- [ ] **Group command hotfix:** complete review and CI, merge, rebuild the bot image, and verify addressed commands in the test group without awarding activity.
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
