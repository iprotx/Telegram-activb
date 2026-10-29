# Work Log

## 2026-10-29 — Initial `/top` leaderboard

- **Goal:** show the top 10 active users in the current group.
- **Changed:** added `/top` handler and a chat-scoped repository query ordered by XP, message count, then user ID; service validates limits between 1 and 50. Empty/private-chat cases return explicit messages.
- **Architecture:** handler → activity service → activity repository; no schema or migration changes.
- **Tests added:** service limit validation, handler output/empty/private cases, and SQLite integration coverage for chat isolation, ordering and limit.
- **Verification:** CI pending for this branch; local execution is unavailable through the connected GitHub tools.
- **Branch:** `feat/top-command`.
- **Next:** inspect CI and fix failures before opening/recommending merge.


## 2026-10-29 — Initial `/rank` command

- **Goal:** expose existing per-chat XP, level, message count, rank position, and progress to the next level.
- **Changed:** added `/rank` for the caller and `/rank @username` for an existing activity member in the current group; ranking is deterministic (XP descending, message count descending, user ID ascending).
- **Architecture:** handler handles command parsing and response only; service delegates lookup; repository calculates chat-scoped position with a SQL window function. No model/schema/migration changes.
- **Tests added:** unit tests for service lookup and command responses; SQLite integration test for chat isolation, username matching, unknown users, and stable tie ordering.
- **Verification:** CI run [#215](https://github.com/iprotx/Telegram-activb/actions/runs/40892928139) passed Ruff format/lint, mypy, Alembic migrations/check, unit tests, PostgreSQL integration tests, pip-audit, Docker build and runtime smoke. The first CI run caught a mypy inference issue in the SQL result; explicit casts fixed it, and the subsequent full run passed.
- **Branch:** `feat/rank-command`.
- **Next:** review PR #35; merge remains an explicit user decision.


## 2026-10-29 — Transaction boundary investigation (issue #32)

- **Question:** should `ServicesMiddleware` stop wrapping the entire handler in `session.begin()`?
- **Inspected:** all registered handlers, middleware, user/activity services and repositories, middleware unit tests, and PostgreSQL rollback integration test.
- **Finding:** only `start_handler` makes a Telegram API call inside the transaction (`message.answer` after user registration). `activity_message_handler` is DB-only and uses the same transaction for user registration plus activity recording.
- **Existing contract:** unit tests verify commit on success and rollback/re-raise on failure; PostgreSQL integration verifies a newly registered user is rolled back when a handler fails. Repository savepoints handle uniqueness races but do not replace the outer transaction.
- **Decision:** no production change. There is no evidence of a material transaction-duration problem, while moving commits into services could leave a registered user without corresponding activity if the latter fails. Preserve current update-level atomicity; revisit with measurements or a concrete use case.
- **Changed:** documented the decision in `docs/DECISIONS.md`, reconciled the architecture plan and project status.
- **Verification:** source and existing test contracts were inspected from GitHub. No production code, dependencies, or tests were changed; CI is not required to validate runtime behavior changes because none were made. Documentation PR CI remains to be checked.
- **Branch:** `investigation/transaction-boundaries`.
- **Next:** merge the documentation PR; then proceed to `/rank` as a separate feature.

## 2026-10-29 — Configuration boundary refactor

- **Goal:** simplify database URL loading without weakening the application's required `BOT_TOKEN` validation.
- **Changed:** introduced `DatabaseSettings` for database URL configuration and validation; `Settings` extends it and still requires `bot_token`. `get_database_url()` no longer constructs application settings with a synthetic empty secret. Existing environment-over-`.env` precedence is retained.
- **Tests:** updated configuration characterization tests to explicitly remove `BOT_TOKEN` while testing Alembic's database URL loading.
- **Architecture:** no handler, service, repository, transaction, XP, migration, or schema behavior changed.
- **Verification:** CI run [40888401905](https://github.com/iprotx/Telegram-activb/actions/runs/40888401905) passed Ruff format/lint, mypy, Alembic migrations/check, unit tests, PostgreSQL integration tests, pip-audit, Docker build, and Docker runtime smoke. Files were read back from the feature branch; local execution was not available through the connected GitHub file tools.
- **Branch:** `refactor/config-settings-boundary`, based on `main` at `fe25dba738f8201646772f6f8409c9d77c088705`.
- **PR:** [#33](https://github.com/iprotx/Telegram-activb/pull/33) is open for review; not merged.

## 2026-10-29 — Startup/import-safety regression tests

- **Goal:** cover issue #14's import safety, dispatcher wiring, and startup failure cleanup contracts.
- **Changed:** added `tests/unit/test_main.py`: an isolated subprocess imports `bot.main` without a token and asserts that no runtime resources/polling start; the dispatcher test verifies custom middleware and root-router registration; a failure-path test verifies database disposal if polling raises.
- **Production code:** unchanged; all three tests pass against the current implementation.
- **Verification:** CI run [40869999942](https://github.com/iprotx/Telegram-activb/actions/runs/40869999942) passed Ruff format/lint, mypy, Alembic migrations/check, both general and PostgreSQL pytest suites, dependency audit, and Docker build.
- **Review state:** PR #29 is open; issue #14 remains open until the change is reviewed and merged.
- **Next:** after PR #29 is integrated, continue with issue #16 (Docker runtime smoke).

## 2026-10-29 — Non-AI chat bot feature research plan

- **Goal:** define an evidence-backed process for studying comparable Telegram group bots and selecting deterministic activity, moderation, and admin features.
- **Scope:** documentation/research plan only; no runtime behavior or dependencies changed.
- **Compared official references:** Combot's non-AI analytics/XP/moderation capabilities, Rose's rules-based moderation docs, Group Help's group-protection overview, and Telegram's Bot API/FAQ for message visibility and permissions.
- **No-AI constraint:** exclude AI/LLM/model calls, AI classifiers, and external AI services from product candidates.
- **Changed:** added `docs/superpowers/plans/2026-10-29-chat-bot-feature-research.md`; linked it from `docs/PROJECT_STATUS.md`; recorded the durable product constraint in `docs/DECISIONS.md`.
- **Verification:** repository docs/source and open hardening issues were inspected; official reference pages were reviewed. No application code or tests changed, so code quality checks were not run for this documentation-only change.
- **Next:** finish the remaining reliability gaps (#14 and #16), then perform the architecture/release-readiness review before expanding runtime scope.

## 2026-10-29 — Production-hardening status reconciliation

- **Goal:** reconcile the detailed hardening plan with the current `main` after PR #25 and replace the stale pre-PR status snapshot with evidence-backed states.
- **Current main:** `1c5bb9f7ac936fd999e741d38cfd07366a7ac405`, merge of PR #25.
- **Confirmed complete:** user profile synchronization, `/start` coverage, middleware transaction boundaries, user schema/constraints, PostgreSQL registration concurrency, and current CI quality gates.
- **Confirmed remaining:** #13 error-boundary tests/safe logging, #14 startup/import-side-effect coverage, #16 Docker runtime smoke, final whole-branch architecture review, and final release-readiness verification.
- **Stale backlog:** #18 describes the dependency violation already fixed by merged PR #21; the issue should be closed/updated as part of backlog cleanup.
- **Changed:** updated `docs/PROJECT_STATUS.md` with the reconciled snapshot and evidence-backed backlog.
- **Verification:** repository state and historical PR/CI evidence were checked before assigning statuses; no production code changed.
- **Next:** finish the documentation reconciliation, verify its CI, then take the first remaining engineering gap (#13) as a bounded code-changing iteration.

## 2026-10-29 — Error middleware safe-logging regression tests

- **Goal:** cover issue #13's observable error middleware contract without changing production behavior.
- **Changed:** added `tests/unit/test_error_middleware.py` with two tests: one checks the original exception is re-raised and logged with the expected message/traceback; the other checks a synthetic token and serialized update payload passed through the event/context are not logged.
- **Production code:** unchanged; the current middleware satisfies these behaviors in the regression tests.
- **Verification:** CI run [40868768340](https://github.com/iprotx/Telegram-activb/actions/runs/40868768340) passed Ruff format/lint, mypy, Alembic migration/check, both general and PostgreSQL pytest suites, dependency audit, and Docker build.
- **Merged:** PR #28, merge commit `5eb3b3d02453bf98af3c8c3aa2d95c6c4e9ddcad`; issue #13 was closed by the PR.
- **Verification:** CI run [40868768340](https://github.com/iprotx/Telegram-activb/actions/runs/40868768340) passed all configured quality gates for the regression tests; production code was unchanged.
- **Next:** proceed with issue #14 (startup/import-side-effect coverage).

## 2026-10-29 — PostgreSQL user repository verification

- **Goal:** verify the `users` uniqueness constraint, nullable profile fields, and concurrent registration on the same PostgreSQL engine used by CI.
- **Changed:** added dedicated PostgreSQL integration tests and an explicit CI step; the PostgreSQL tests require the CI PostgreSQL service and are excluded from the generic test step to make execution visible.
- **Merged:** PR #25, merge commit `1c5bb9f7ac936fd999e741d38cfd07366a7ac405`.
- **Verification:** PR #25 CI run `40865798961` completed successfully, including PostgreSQL integration tests, Alembic checks, dependency audit and Docker build.

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
- **Backlog:** opened issue #11 to reconcile the detailed production-hardening plan against source/tests/CI and create evidence-backed follow-up tasks.
- **Verification:** the reconciliation task is now being completed against the post-PR #25 `main` state.

Append a short entry after every meaningful task or PR. Newest entries go first. Record facts and links, not assumptions.

## 2026-10-29 — Activity timestamp and concurrency hardening

- **Goal:** remove timezone comparison failures and protect concurrent first-message activity updates.
- **Changed:** added UTC normalization in activity policy; made `ChatMember.last_xp_at` timezone-aware; added migration `0004_activity_timestamp_timezone.py`; serialized the concurrent insert-race recovery path; added repository integration tests.
- **Merged:** PR #10, merge commit `ad20f34c46db52e8d1da9b5a5eba8d83d33cf008`.
- **Verification:** CI run `40845554427` completed with success.
- **Not established by this check:** full production readiness, real deployment health, or completion of every item in the broader hardening plan.
- **Next:** reconcile the detailed implementation plan against current code/tests and convert confirmed gaps into actionable backlog items.

## 2026-10-29 — Activity levels feature

- **Goal:** resolve migration/model conflicts and deliver activity-level functionality.
- **Merged:** PR #8 into `main`.
- **Verification:** main CI was reported green after merge.
- **Next:** continue reliability review with evidence-based, bounded changes.


