# Security Remediation Plan — Telegram-activb

This document records the concrete fixes recommended by `docs/SECURITY_AUDIT.md`. It is intentionally stored under `docs/` as requested; it does not claim that application source code was changed.

## 1. GitHub Actions: immutable action references

**Finding:** S1

### Current

```yaml
- uses: actions/checkout@v5
- uses: actions/setup-python@v6
```

### Required fix

Resolve each action tag to its exact upstream commit SHA and use the SHA in the workflow. Keep the human-readable version in a comment, for example:

```yaml
- uses: actions/checkout@<FULL_COMMIT_SHA> # v5
- uses: actions/setup-python@<FULL_COMMIT_SHA> # v6
```

Do not copy a SHA from an untrusted third-party article; resolve it from the official action repository/release and review the change.

### Verification

- CI still starts successfully.
- `permissions` remains least-privilege (`contents: read`).
- No new write-capable token is introduced.

## 2. Dependency and image reproducibility

**Finding:** S2

### Required fix

Introduce a production dependency lock/constraints workflow and pin the Docker base image by digest. Continue running `pip-audit` on every CI run.

Recommended policy:

- application dependency versions are locked for production builds;
- security updates are reviewed as explicit dependency changes;
- `python:3.12-slim` is replaced by a reviewed digest reference;
- CI records the resolved dependency set as an auditable artifact when appropriate.

### Verification

Run:

```text
pip-audit
python -m pytest -q
alembic check
```

and build the image twice from the same commit to confirm the dependency resolution is controlled by the lock/constraints process.

## 3. Production database mode

**Finding:** S4

### Required fix

Keep SQLite available for local development/tests, but make production startup require PostgreSQL. The deployment configuration already requires an explicit `DATABASE_URL`; document and enforce that production uses `postgresql+asyncpg://...`.

Recommended deployment guard:

- development/test profile: SQLite allowed;
- production profile: PostgreSQL required;
- production startup fails closed if a SQLite URL is supplied.

This avoids relying on SQLite's weaker concurrency semantics for the activity counter/XP path.

### Verification

- Production configuration with PostgreSQL starts normally.
- Production configuration with a SQLite URL fails with a clear validation error.
- Existing SQLite unit tests remain green.
- PostgreSQL integration tests remain green.

## 4. Logging and secret redaction

**Finding:** S3

### Required fix

Keep generic exception logging, but treat Telegram updates, configuration objects, database URLs, authorization values and tokens as sensitive. Never add a log statement that serializes the complete update or settings object.

Maintain regression tests containing synthetic sentinel values and assert that those values do not appear in emitted logs.

### Verification

At minimum test that:

- a synthetic bot token is absent from error logs;
- private Telegram update fields are not serialized into logs;
- database credentials are not emitted;
- traceback logging remains useful without dumping request/update payloads.

## 5. Defensive test-hack suite

These tests are safe to run locally or in isolated CI and do not contact Telegram or attack external infrastructure.

### Test A — synthetic secret leak

Inject a fake token such as `123456:synthetic-test-token`, trigger a controlled exception, capture logs, and assert the token is absent.

### Test B — duplicate message replay

Submit the same synthetic `(chat_id, user_id, message_id)` twice inside the repository/service test harness. Assert that the second submission does not create a second activity event and does not award XP again.

### Test C — cross-chat isolation

Use the same synthetic user in two different synthetic chats. Assert that each chat has a distinct `ChatMember` record and activity events never cross the chat boundary.

### Test D — concurrent first message

For PostgreSQL integration tests, concurrently process the same first message for one member. Assert one logical activity event and one XP award.

### Test E — CI permissions regression

Review the workflow file and assert that the workflow/job does not acquire write permissions unless a documented change requires them.

## 6. Definition of done

The security remediation is complete when:

- [ ] GitHub Actions are pinned to full commit SHAs.
- [ ] Production Python dependencies are locked/controlled.
- [ ] Docker base image is pinned by digest.
- [ ] Production rejects SQLite and requires PostgreSQL.
- [ ] Secret/log-redaction regression tests pass.
- [ ] Duplicate/replay, cross-chat isolation and concurrency tests pass.
- [ ] `ruff format --check .` passes.
- [ ] `ruff check .` passes.
- [ ] `mypy src` passes.
- [ ] `pytest -q -m "not postgres"` passes.
- [ ] `pytest -q -m postgres` passes.
- [ ] `alembic check` passes.
- [ ] `pip-audit` reports no unresolved known vulnerabilities according to the project's accepted policy.
- [ ] Docker build and the existing runtime smoke test pass without network access to Telegram.

## Important note

No real credentials, production services, Telegram endpoints, or external targets were used for this audit. The remediation items above are safe engineering changes and verification procedures; they should be implemented through normal reviewed source changes rather than by testing against live infrastructure.
