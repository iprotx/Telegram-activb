# Project Status

_Last reconciled: 2026-10-29_

## Current snapshot

- **Default branch:** main
- **Latest merged change:** PR #12, project status, roadmap, decision log, work log, and reporting rules.
- **Latest merged commit:** 6816dd2bfab5e346f8680340fab3127d90dfe0d6.
- **Main CI:** [run 40846550635](https://github.com/iprotx/Telegram-activb/actions/runs/40846550635) — success.
- **Product shape:** aiogram bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates.
- **Release status:** not yet certified production-ready. CI is green, but container runtime smoke, full architecture review, and several focused test gaps remain.

## Recently completed

- [x] PR #8: activity levels and migration conflict resolution.
- [x] PR #10: activity timestamp normalization, timezone-aware persistence, concurrency handling, and activity repository tests. [CI](https://github.com/iprotx/Telegram-activb/actions/runs/40845554427)
- [x] PR #12: project status/roadmap, decision log, work log, README links, and stage-reporting rules. [CI](https://github.com/iprotx/Telegram-activb/actions/runs/40846301942)
- [x] Verify main CI after PR #12: [run 40846550635](https://github.com/iprotx/Telegram-activb/actions/runs/40846550635).

## In progress

- [ ] Reconcile the production-hardening plan against actual source, tests, migrations, and CI evidence. The evidence-backed audit table is being added to the detailed plan in a documentation-only PR.
- [ ] After the audit is merged, perform the whole-branch architecture review and update statuses based on that review.

## Prioritized backlog

### P0 — Evidence-backed plan and architecture review

- [ ] Complete review of all hardening iterations; see [detailed plan](superpowers/plans/2026-10-29-production-hardening.md) and [issue #11](https://github.com/iprotx/Telegram-activb/issues/11).
- [ ] Finish the full dependency-path review from main/routers through handlers, services, repositories, and database infrastructure. A confirmed dependency inversion is tracked in [#18](https://github.com/iprotx/Telegram-activb/issues/18): activity repository imports business policy from services.
- [ ] Confirm remaining tasks and keep this page aligned with issue/PR/CI state.

### P1 — Confirmed verification gaps

- [ ] [#13 Error middleware propagation and safe logging tests](https://github.com/iprotx/Telegram-activb/issues/13).
- [ ] [#14 Application startup wiring and import-safety tests](https://github.com/iprotx/Telegram-activb/issues/14).
- [ ] [#15 User schema constraints and PostgreSQL registration concurrency](https://github.com/iprotx/Telegram-activb/issues/15).
- [ ] [#16 Docker runtime smoke test and release-readiness review](https://github.com/iprotx/Telegram-activb/issues/16).
- [ ] [#18 Move activity policy decisions out of the repository layer](https://github.com/iprotx/Telegram-activb/issues/18).
- [ ] [#20 Verify SQLite Alembic migration compatibility](https://github.com/iprotx/Telegram-activb/issues/20).

### P2 — Release readiness

- [ ] Define first-release scope and operator acceptance criteria.
- [ ] Verify a clean deployment from documented setup with required environment variables and a fresh database.
- [ ] Record operational limitations before describing the bot as production-ready.

## Working agreements

1. Start substantial tasks with goal, scope, assumptions, risks/dependencies, and acceptance criteria.
2. Work in bounded stages and report each stage before moving to a separate one.
3. Mark work done only with evidence: test, CI link, diff, or explicit decision.
4. Use GitHub issues for actionable tasks and this page as the overview.
5. Update this page and the work log after each meaningful task/PR; record durable decisions in DECISIONS.md.
6. Do not merge PRs, deploy, or perform destructive/release actions without explicit user approval.
7. Reports distinguish **changed**, **verified**, **not verified**, **risks/blockers**, and **next step**.

## Links

- [Engineering rules](../AGENTS.md)
- [Production-hardening implementation plan](superpowers/plans/2026-10-29-production-hardening.md)
- [Decision log](DECISIONS.md)
- [Work log](WORKLOG.md)
