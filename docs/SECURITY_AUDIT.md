# Security Audit — Telegram-activb

**Date:** 2026-10-29  
**Repository:** `iprotx/Telegram-activb`  
**Scope:** source code, configuration, Docker/Compose, GitHub Actions, database access patterns, tests and dependency configuration on the default branch.  
**Method:** three independent specialist tracks coordinated by the orchestrator: AppSec/OWASP, GitHub/CI supply-chain, and defensive red-team review.  
**Safety:** no deployment, no Telegram Bot API calls, no credential use, no secret exfiltration and no attacks against external systems were performed.

## Executive summary

**Overall risk: LOW–MODERATE.** No confirmed critical or high-severity remote-code-execution, authentication-bypass, SQL-injection, or hard-coded-secret finding was identified in the reviewed code. The strongest risks are operational/supply-chain hardening items rather than an immediately exploitable application vulnerability.

The repository already has several good controls: secrets are represented by environment variables and `SecretStr`; CI has `contents: read`; CI runs dependency auditing; the Docker image drops root; SQL access uses SQLAlchemy expressions rather than interpolated SQL; activity events have a uniqueness constraint; and tests explicitly exercise log-redaction sentinels.

## Findings

### S1 — GitHub Actions dependencies are mutable tags

**Severity:** Medium  
**Category:** Supply-chain / CI security  
**Evidence:** `.github/workflows/ci.yml` uses `actions/checkout@v5` and `actions/setup-python@v6`.  

**Risk:** A mutable major tag can move to a different upstream commit. A compromised or malicious upstream release could therefore affect the CI execution environment. The workflow has only `contents: read`, which limits blast radius, but the workflow still executes repository code and builds a Docker image.

**Recommendation:** Pin third-party GitHub Actions to full commit SHAs and update them through a controlled dependency-update process. Keep `permissions: contents: read` and add explicit job-level permissions if a future step needs more access.

**Status:** Remediation documented; code change intentionally not made because the requested output location was `docs/`.

### S2 — Base images and runtime dependencies are version ranges rather than immutable artifacts

**Severity:** Low–Medium  
**Category:** Supply-chain / reproducibility  
**Evidence:** `Dockerfile` uses `python:3.12-slim`; `pyproject.toml` allows ranges such as `alembic>=1.16,<2.0`, `asyncpg>=0.30,<1.0`, and `pydantic-settings>=2.7,<3.0`.

**Risk:** Rebuilds can resolve newer artifacts without a source change. CI mitigates part of this with `pip-audit`, but reproducibility and change attribution are weaker than with lockfiles/digests.

**Recommendation:** Use a lock/constraints strategy for production builds and pin the Docker base image by digest. Continue `pip-audit` in CI.

**Status:** Remediation documented.

### S3 — Error logging deliberately records full exception tracebacks

**Severity:** Low  
**Category:** Information disclosure / observability  
**Evidence:** `src/bot/middlewares/errors.py` calls `logger.exception("Unhandled Telegram update error")`.

**Risk:** Python exception tracebacks can contain sensitive runtime values if a future exception includes a token, private update field, database URL, or other secret-bearing object. Existing tests indicate an explicit effort to prevent secret/update leakage, which is positive, but this control should remain regression-tested as code grows.

**Recommendation:** Keep generic operator-facing error messages, avoid logging raw update objects, add structured redaction for known secret fields, and ensure log sinks are access-controlled and retention-limited.

**Status:** No confirmed leakage in the reviewed implementation; remediation is preventive.

### S4 — SQLite is allowed as the default runtime database

**Severity:** Low  
**Category:** Deployment safety / data integrity  
**Evidence:** `src/bot/config.py` defaults to `sqlite+aiosqlite:///./bot.db`; the production Compose path requires `DATABASE_URL`.

**Risk:** SQLite is convenient for development but is not the intended concurrent production database. The repository's locking strategy uses `with_for_update()` for member rows, which is meaningful for PostgreSQL but does not provide equivalent row-lock semantics on SQLite.

**Recommendation:** Make PostgreSQL mandatory for production deployments through an explicit production configuration/profile, and reserve SQLite for local development/tests.

**Status:** Remediation documented.

## Positive controls verified

- `BOT_TOKEN` is loaded from configuration and represented as `SecretStr`; `.env.example` contains placeholders rather than a real token.
- The bot token is passed to `aiogram.Bot` only at runtime.
- CI explicitly sets `permissions: contents: read`.
- CI runs Ruff, mypy, migrations, tests, PostgreSQL integration tests, `alembic check`, `pip-audit`, Docker build and a runtime smoke test.
- The Dockerfile creates a non-root `bot` user and runs the application as that user.
- SQL queries are built through SQLAlchemy `select()` expressions; no string-interpolated SQL sink was found in the reviewed paths.
- Activity event uniqueness is enforced by `UniqueConstraint("chat_member_id", "telegram_message_id")`, reducing duplicate-event replay/double-award risk.
- Activity member lookup uses row locking under transactional middleware, which is appropriate for PostgreSQL concurrency.
- The reviewed CI job does not expose repository secrets to pull-request code and has read-only repository permissions.

## Defensive red-team scenarios performed as code review

1. **Secret exposure:** searched for token/environment use and logging paths. No hard-coded production token was identified; configuration uses `SecretStr`.
2. **SQL injection:** reviewed repository queries and searched for common dynamic execution constructs. No raw SQL interpolation or obvious SQL execution sink was identified.
3. **IDOR / cross-chat mix-up:** traced `chat_telegram_id -> Chat -> ChatMember -> ActivityEvent`. Membership is keyed by both chat and user, and events are keyed by the resulting member, so the reviewed activity path does not expose an obvious cross-chat object reference flaw.
4. **Replay/double-award:** traced the message uniqueness constraint plus transactional member locking. The design prevents the common duplicate-message path from awarding XP twice.
5. **CI compromise:** reviewed workflow permissions and third-party actions. No write token permission was granted; the remaining concern is mutable action tags.
6. **Container escape / privilege:** reviewed Dockerfile. The application runs as UID 10001 rather than root; no privileged mode or host mount was found in Compose.

## Limitations

This was a repository-level defensive audit, not a production penetration test. The GitHub connector used for this review does not expose secret values and no live bot/database deployment was used. Therefore this report does not certify GitHub organization settings, branch protection, secret rotation history, external infrastructure, or runtime Telegram permissions.

## Priority order

1. Pin GitHub Actions to commit SHAs.
2. Pin/lock production Python dependencies and the Docker base image.
3. Make PostgreSQL explicit for production and keep SQLite development-only.
4. Maintain log-redaction tests and review every new error/log statement for secret-bearing data.
5. Periodically rerun `pip-audit`, static security review, and the defensive red-team scenarios above.

## Evidence references

- `.github/workflows/ci.yml`: CI permissions, tests, dependency audit and Docker checks.
- `src/bot/config.py`: secret handling and database URL validation.
- `src/bot/main.py`: bot construction and dispatcher lifecycle.
- `src/bot/handlers/activity.py`: Telegram update to activity flow.
- `src/bot/services/activity_tracking.py`: XP/event processing.
- `src/bot/repositories/activity.py`: chat/member/event lookup and concurrency handling.
- `src/bot/repositories/users.py`: Telegram user registration/profile synchronization.
- `src/bot/middlewares/errors.py`: exception logging.
- `Dockerfile`: non-root container execution.
- `docker-compose.yml`: production-style PostgreSQL dependency and required database configuration.
- `pyproject.toml`: dependency ranges and security tooling.

## Conclusion

No confirmed critical/high exploit was found in the reviewed default-branch implementation. The repository is in a reasonably strong baseline state for a small Telegram bot, with the main remaining security work concentrated on supply-chain immutability, production database guarantees, and continued log-redaction discipline.
