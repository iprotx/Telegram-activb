# Production Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` (or `superpowers:subagent-driven-development` when independent review workers are available) to implement this plan task-by-task. Every task is a single iteration. Every iteration ends with verification, review, and exactly one commit.

**Goal:** Evolve the existing aiogram 3.31 foundation into a small, production-ready Telegram bot without breaking the strict `handlers -> services -> repositories -> database` dependency direction.

**Architecture:** Keep Telegram-specific behavior at the handler/middleware boundary, business decisions in services, and SQLAlchemy details in repositories/database infrastructure. Prefer the smallest explicit design; do not introduce abstractions until a concrete boundary or test requires them.

**Tech Stack:** Python 3.12+, aiogram 3.31, SQLAlchemy 2.x async, Alembic, pydantic-settings, pytest/pytest-asyncio, Ruff, mypy, Docker Compose, GitHub Actions.

**Spec:** `AGENTS.md`, `skills/ub-mode/SKILL.md`, `skills/python-aiogram-coder/SKILL.md`, and the approved production-foundation design. The repository already has the foundation and an open PR; this plan hardens that foundation rather than replacing it.

## Global Constraints

- One coherent iteration produces one independently reviewable result.
- One iteration produces exactly one commit; tests and implementation for that behavior belong in that commit.
- TDD is the default: write the behavior test, observe the intended failure when practical, implement minimally, then refactor.
- `/ub-mode` is mandatory for every code-changing iteration: First Make it Work -> Then Make it Right -> Practice.
- Dependency direction remains `handlers -> services -> repositories -> database infrastructure`.
- Handlers must not contain SQLAlchemy queries or business rules.
- Repositories must not secretly own application-level transactions.
- Telegram input is validated at the boundary and business logic remains transport-independent.
- Operations that can be retried by Telegram/polling must be safe to repeat.
- No secrets, bot tokens, or sensitive Telegram payloads are committed or unnecessarily logged.
- Quality gates are `ruff format --check .`, `ruff check .`, `mypy src`, and `pytest -q`; database work additionally requires `alembic upgrade head` and `alembic check`.
- `crapper`, `dryer`, and `mutator` are optional. If an executable is absent, skip that gate and report it; never fabricate a result.
- Do not mix unrelated cleanup, dependency upgrades, feature work, and schema changes in the same iteration.
- Do not merge the PR automatically; merge remains an explicit human decision.

## Review Focus

1. **Repeated Telegram registration:** the same Telegram user must not create duplicate rows and profile fields must converge to the latest Telegram values. Test owned by the user lifecycle task.
2. **Partial Telegram profile:** missing username/last name must remain valid and must not erase unrelated fields accidentally. Test owned by the user profile task.
3. **Transaction failure:** a handler exception must roll back repository writes and must not leave a partially committed unit of work. Test owned by the middleware transaction task.
4. **Telegram boundary failures:** malformed/absent event data and Telegram API failures must not leak database or secret details. Tests owned by the handler/error-boundary tasks.
5. **Configuration/operational failure:** missing secrets, invalid database configuration, and startup failures must fail clearly without logging secret values. Tests owned by the configuration/startup task.

## Iteration Protocol

Every iteration follows this exact sequence:

1. Read `AGENTS.md`, the relevant local skill, and the target code/tests.
2. Invoke/apply `/ub-mode`.
3. State the smallest behavior change.
4. Add or update the behavior test.
5. Run the focused test and confirm the expected failure when practical.
6. Implement the minimum production change.
7. Run the focused tests.
8. Refactor only if behavior is already pinned.
9. Run the full applicable quality gates.
10. Perform a focused self-review of the diff: correctness, architecture, security, unnecessary complexity, and regression risk.
11. If verification fails, debug root cause before committing. A debug fix still belongs to the current iteration; do not create a second opportunistic change.
12. Commit exactly once with a concise conventional-style message.
13. Record the commit and verification evidence before moving to the next iteration.

---

### Iteration 0: Baseline and repository documentation consistency

**Files:**
- Modify: `README.md`
- Test/verification: repository-level checks only; no production code change.

**Purpose:** Establish a trustworthy baseline before further code changes. The current README references the old `AGENTS.MD` and deleted `docs/skills/python-aiogram-coder.md`; these references must match the current project-local skills layout.

- [ ] Inspect the current branch head, PR state, README, `AGENTS.md`, `skills/README.md`, and CI status.
- [ ] Update README references to `AGENTS.md` and the current local skills.
- [ ] Verify no obsolete project-rule paths remain.
- [ ] Run the existing quality checks as a baseline; no code behavior should change.
- [ ] Self-review for documentation-only scope.
- [ ] Commit exactly once: `docs: align project documentation with local skills`.

**Exit condition:** README and project guidance point to files that actually exist, with existing quality checks still passing.

### Iteration 1: Complete Telegram user profile synchronization

**Files:** `src/bot/repositories/users.py`, `src/bot/services/users.py`, `tests/unit/test_user_repository.py`, `tests/unit/test_user_service.py`

- [ ] Add behavior tests proving repeated registration updates owned profile fields while preserving the same database identity.
- [ ] Run focused tests and observe the intended failure when fields are not synchronized.
- [ ] Extend the repository/service interface minimally and explicitly for the profile data.
- [ ] Implement only the required update behavior; do not add generic CRUD abstractions.
- [ ] Run focused tests and all applicable quality gates.
- [ ] Review idempotence, SQLAlchemy semantics, and dependency direction.
- [ ] Commit exactly once: `fix: synchronize Telegram user profile`.

**Exit condition:** repeated registration converges stored profile data to current Telegram values and is idempotent.

### Iteration 2: Make `/start` behavior explicit and testable

**Files:** `src/bot/handlers/start.py`, `tests/unit/test_start_handler.py`

- [ ] Define handler tests for a normal user and users with missing optional profile fields.
- [ ] Assert the service receives the Telegram identity/profile and the expected response is sent.
- [ ] Run focused tests and observe the intended failure.
- [ ] Implement the smallest handler change.
- [ ] Run handler tests and full quality gates.
- [ ] Review that the handler stays transport-only.
- [ ] Commit exactly once: `test: cover start handler behavior` or the equivalent `fix:` commit if production code changes are required.

**Exit condition:** `/start` behavior is pinned by tests and the handler remains thin.

### Iteration 3: Prove middleware transaction boundaries

**Files:** `src/bot/middlewares/services.py`, `tests/unit/test_services_middleware.py`, `src/bot/db/session.py` only if required.

- [ ] Test successful handler execution followed by commit.
- [ ] Test failing handler execution followed by rollback and re-raise.
- [ ] Prefer fakes for the middleware unit tests; avoid coupling to SQLAlchemy internals.
- [ ] Run focused tests, then make the minimum transaction-boundary change.
- [ ] Verify the failure path cannot leave a partially committed unit of work.
- [ ] Run full quality gates and review transaction ownership.
- [ ] Commit exactly once: `test: pin middleware transaction semantics` or `fix: harden middleware transaction boundary`.

**Exit condition:** success commits once, exceptions roll back once, and ownership is obvious.

### Iteration 4: Database model and migration correctness

**Files:** `src/bot/db/models/user.py`, `alembic/versions/*`, `tests/integration/test_user_schema.py` if needed.

- [ ] Add integration-level assertions for unique `telegram_id` and nullable profile fields.
- [ ] Run the migration/schema test before changing schema.
- [ ] Make only schema changes justified by the tests/spec.
- [ ] Run `alembic upgrade head` and `alembic check` from a clean database.
- [ ] Review migration determinism and constraint safety.
- [ ] Commit exactly once: `test: cover user database constraints` or a justified `fix:` commit.

**Exit condition:** model and migration agree, database invariants are enforced, and Alembic reports no drift.

### Iteration 5: Error boundary and safe logging

**Files:** `src/bot/middlewares/errors.py`, `tests/unit/test_error_middleware.py`

- [ ] Test unexpected exceptions are logged and re-raised.
- [ ] Test logging does not interpolate bot tokens or full Telegram payloads.
- [ ] Run focused tests and observe failure.
- [ ] Implement minimal diagnostic context without sensitive payloads.
- [ ] Run full quality gates.
- [ ] Review logging for secret/PII exposure and unnecessary serialization.
- [ ] Commit exactly once: `fix: harden Telegram error logging`.

**Exit condition:** failures remain observable without leaking credentials or unnecessary Telegram data.

### Iteration 6: Configuration and startup validation

**Files:** `src/bot/config.py`, `src/bot/main.py` only if needed, `tests/unit/test_config.py`, `tests/unit/test_main.py`.

- [ ] Test required secrets, valid database configuration, and safe failure messages.
- [ ] Test importing the application does not start polling.
- [ ] Run focused tests and observe intended failures.
- [ ] Implement minimal validation/startup behavior.
- [ ] Run full quality gates.
- [ ] Review configuration for secret exposure and unnecessary global state.
- [ ] Commit exactly once: `fix: harden application configuration`.

**Exit condition:** invalid configuration fails early and clearly; secrets do not appear in normal logs/errors; imports are side-effect free.

### Iteration 7: Repository concurrency and idempotence

**Files:** `src/bot/repositories/users.py`, `tests/integration/test_user_repository.py`

- [ ] Add an integration test for duplicate registration attempts against a temporary real database.
- [ ] Run it and classify the failure as repository logic, DB constraint behavior, or environment limitation.
- [ ] Fix the root cause; do not use an in-memory lock as a substitute for database correctness.
- [ ] Run the test and full quality gates.
- [ ] Review transaction isolation and integrity-error handling.
- [ ] Commit exactly once: `fix: make user registration idempotent`.

**Exit condition:** duplicate registration cannot violate the database invariant and retry behavior is deterministic.

### Iteration 8: Docker runtime smoke path

**Files:** `Dockerfile`, `docker-compose.yml`, optional lightweight smoke test.

- [ ] Define the operational contract: build, environment injection, writable DB path, process startup, and signal/shutdown behavior.
- [ ] Run the existing Docker build/start path before changing it.
- [ ] Fix only observed runtime defects.
- [ ] Run application quality gates plus the Docker smoke command.
- [ ] Review image/runtime concerns and secret handling.
- [ ] Commit exactly once: `chore: harden bot container runtime`.

**Exit condition:** the documented container path is reproducible and does not depend on undeclared local state.

### Iteration 9: CI quality gate hardening

**Files:** `.github/workflows/ci.yml` and docs only if commands change.

- [ ] Compare CI commands with `AGENTS.md` and actual project commands.
- [ ] Add only missing deterministic gates; avoid speculative infrastructure.
- [ ] Validate workflow syntax and run equivalent commands where available.
- [ ] Review reproducibility, Python version alignment, and failure visibility.
- [ ] Commit exactly once: `ci: harden project quality gates`.

**Exit condition:** CI proves the documented contributor quality contract.

### Iteration 10: Whole-branch architecture review

**Files:** no production changes unless a concrete finding requires a new iteration.

- [ ] Review all commits since the production-foundation baseline.
- [ ] Trace `main.py -> routers -> handlers -> services -> repositories -> database`.
- [ ] Search for SQLAlchemy outside repositories/database infrastructure.
- [ ] Search for business decisions in handlers and Telegram-specific imports in services.
- [ ] Check global mutable state, hidden transactions, dead code, duplicate abstractions, and unnecessary wrappers.
- [ ] Review errors, logging, configuration, and secrets.
- [ ] Convert every actionable finding into a new bounded iteration rather than fixing it opportunistically.
- [ ] If clean, record the review without creating a meaningless commit.

**Exit condition:** architecture is explainable and every dependency crosses an intentional boundary.

### Iteration 11: Final verification and merge readiness

**Files:** documentation only if verification instructions are stale.

- [ ] Run `ruff format --check .`.
- [ ] Run `ruff check .`.
- [ ] Run `mypy src`.
- [ ] Run `pytest -q`.
- [ ] Run `alembic upgrade head` and `alembic check`.
- [ ] Run available `/ub-mode` auxiliary tools; explicitly record missing `crapper`, `dryer`, or `mutator`.
- [ ] Inspect final diff/history for one-intent commits and unrelated changes.
- [ ] Check PR CI and resolve failures through bounded iterations.
- [ ] Do not create a meaningless final commit when verification is already clean.

**Exit condition:** all applicable checks have evidence, unresolved failures are fixed or explicitly documented, and the PR is ready for human merge approval.

## Debugging Protocol

When any test, CI job, migration, or runtime check fails:

1. Reproduce the exact failure with the smallest command.
2. Capture the first meaningful error, not the final cascade.
3. Identify the violated invariant or contract.
4. Write a regression test before the fix when practical.
5. Fix the root cause with the smallest coherent change.
6. Re-run the focused test.
7. Re-run all applicable quality gates.
8. Review the diff for accidental scope expansion.
9. Commit the debugging fix as the single commit for that iteration.
10. Never suppress, skip, or downgrade a failing check just to make CI green.

## Review Protocol

Each iteration gets a self-review before commit. After implementation, perform a whole-branch review covering behavior, TDD evidence, architecture, async/session/transaction correctness, database invariants, Telegram boundary behavior, configuration and secrets, logging, Docker/CI reproducibility, unnecessary complexity, and regression risk.

Any review finding that requires code changes becomes a new bounded iteration and receives its own test, verification, and exactly one commit.

## Definition of Done

- `/start` and user registration behavior are covered by meaningful tests.
- Telegram profile synchronization is idempotent.
- Transaction commit/rollback semantics are tested.
- Database constraints and migrations are verified.
- Error logging is useful without leaking secrets or unnecessary Telegram data.
- Configuration fails safely and startup remains side-effect free on import.
- Docker startup is reproducible.
- CI enforces the documented quality gates.
- Ruff, mypy, pytest, and applicable Alembic checks pass with evidence.
- Missing optional `ub-mode` tools are explicitly reported rather than faked.
- Architecture remains `handlers -> services -> repositories -> database infrastructure`.
- Every meaningful change is isolated into one reviewable iteration and one commit.
- The final PR review has no unresolved correctness or security findings.
