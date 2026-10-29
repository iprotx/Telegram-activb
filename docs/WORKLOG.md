# Work Log

## 2026-10-29 — PostgreSQL user repository verification

- **Goal:** verify the `users` uniqueness constraint, nullable profile fields, and concurrent registration on the same PostgreSQL engine used by CI.
- **Changed:** added dedicated PostgreSQL integration tests and an explicit CI step; the PostgreSQL tests require the CI PostgreSQL service and are excluded from the generic test step to make execution visible.
- **Verification:** pending CI on the dedicated test branch.
- **Next:** review the PostgreSQL integration CI result and merge only after all quality checks pass.

## 2026-10-29 — Alembic database URL alignment

- **Goal:** ensure the application and Alembic use the same validated database settings.
- **Changed:** Alembic now reuses application `Settings`, preserving environment-over-`.env` precedence and SQLite fallback; added configuration tests.
- **Merged:** PR #24, merge commit `f6704e14233174707df543e511f462659d4b27a0`.
- **Verification:** CI run `40863643491` completed successfully; migration, tests, Alembic check, dependency audit, and Docker build all passed.

## 2026-10-29 — Activity policy service-layer refactor

- **Goal:** keep activity business decisions in the service layer and persistence operations in the repository.
- **Merged:** PR #21, merge commit `cd96964358d79903b946225325d2c5d33f9e925a`.
- **Verification:** CI run `40862644131` completed successfully with formatting, lint, mypy, migrations, tests, Alembic check, dependency audit, and Docker build passing.

## 2026-10-29 — Project management baseline

- **Goal:** make project status, priorities, decisions, and progress traceable across tasks.
- **Changed:** added the status/roadmap page, decision log, work log, README links, and explicit stage-reporting rules in AGENTS.md.
- **Backlog:** opened [issue #11](https://github.com/iprotx/Telegram-activb/issues/11) to reconcile the detailed production-hardening plan against source/tests/CI and create evidence-backed follow-up tasks.
- **Verification:** reviewed the current main commit, PR #10 merge state, CI result, README, AGENTS.md, and detailed hardening plan. Documentation-only change; full CI will be evaluated on this PR.
- **Not verified:** all detailed hardening plan items are not yet reconciled; candidate items remain marked unverified in PROJECT_STATUS.md.
- **Next:** review this documentation PR and CI, then handle issue #11 as a separate bounded task.

Append a short entry after every meaningful task or PR. Newest entries go first. Record facts and links, not assumptions.

## 2026-10-29 — Activity timestamp and concurrency hardening

- **Goal:** remove timezone comparison failures and protect concurrent first-message activity updates.
- **Changed:** added UTC normalization in activity policy; made `ChatMember.last_xp_at` timezone-aware; added migration `0004_activity_timestamp_timezone.py`; serialized the concurrent insert-race recovery path; added repository integration tests.
- **Merged:** [PR #10](https://github.com/iprotx/Telegram-activb/pull/10), merge commit `ad20f34c46db52e8d1da9b5a5eba8d83d33cf008`.
- **Verification:** [CI run 40845554427](https://github.com/iprotx/Telegram-activb/actions/runs/40845554427) completed with success.
- **Not established by this check:** full production readiness, real deployment health, or completion of every item in the broader hardening plan.
- **Next:** reconcile the detailed implementation plan against current code/tests and convert confirmed gaps into actionable backlog items.

## 2026-10-29 — Activity levels feature

- **Goal:** resolve migration/model conflicts and deliver activity-level functionality.
- **Merged:** [PR #8](https://github.com/iprotx/Telegram-activb/pull/8) into `main`.
- **Verification:** main CI was reported green after merge.
- **Next:** continue reliability review with evidence-based, bounded changes.
