# Work Log

## 2026-10-29 — Production-hardening plan audit

- **Goal:** replace stale unchecked plan boxes with an evidence-backed view of shipped work and real remaining gaps.
- **Reviewed:** current main tree; user repository/service, /start handler, transaction/error middleware, config/startup wiring, user model and migration, integration/unit tests, Docker files, CI workflow, project skills, and latest main CI.
- **Verified complete:** user profile synchronization; /start behavior; middleware commit/rollback coverage; current CI quality gates. Main CI run [40846550635](https://github.com/iprotx/Telegram-activb/actions/runs/40846550635) passed.
- **Partial gaps confirmed:** dedicated user schema test; error middleware safe-logging tests; main import/startup tests; PostgreSQL-backed concurrent user registration test; Docker runtime smoke/clean deployment test.
- **Issues created:** [#13 error middleware](https://github.com/iprotx/Telegram-activb/issues/13), [#14 startup safety](https://github.com/iprotx/Telegram-activb/issues/14), [#15 schema and PostgreSQL concurrency](https://github.com/iprotx/Telegram-activb/issues/15), [#16 Docker runtime smoke/release review](https://github.com/iprotx/Telegram-activb/issues/16).
- **Changed in this stage:** added an evidence-backed iteration status table to the detailed plan and refreshed the project status page on branch `docs/reconcile-hardening-plan`.
- **Not verified:** no live Telegram bot or deployed environment was exercised; a green CI run is not a production-readiness sign-off. Full whole-branch architecture review is still pending.
- **Next:** open a documentation-only PR, verify its CI, then continue with the whole-branch architecture review as a separate stage.

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
