# Aiogram Production Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the empty Telegram bot repository into a tested, maintainable aiogram 3.31 + SQLAlchemy 2 production foundation and document the corresponding `python-aiogram-coder` rules.

**Architecture:** Use a strict dependency direction of handlers -> services -> repositories -> database infrastructure, with configuration and application wiring at the composition root. Keep Telegram-specific concerns in handlers/middlewares and business logic independent of aiogram where practical.

**Tech Stack:** Python 3.12+, aiogram 3.31, SQLAlchemy 2.x async, Alembic, Pydantic Settings, pytest, Ruff, mypy, Docker Compose, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-29-aiogram-production-foundation-design.md`

## Global Constraints

- aiogram must be pinned to the 3.31 minor release line.
- SQLAlchemy must use the 2.x API and async sessions.
- Business logic must not depend on Telegram handlers or Bot API objects.
- Persistence access must be isolated behind repositories.
- Tests follow TDD and must cover configuration, service behavior, and repository boundaries.
- Secrets must be supplied through environment variables; no tokens or credentials are committed.
- Formatting/linting uses Ruff; static typing uses mypy.
- Database schema changes use Alembic migrations.

## Review Focus

- Missing or malformed environment variables must fail with a useful configuration error.
- Database sessions must be closed/rolled back correctly after repository failures.
- Handlers must not contain business or persistence logic.
- Service behavior must remain testable without Telegram or a live database.
- Docker/CI configuration must not require secrets merely to run static checks.

---

### Task 1: Repository policy and project specification

**Files:**
- Modify: `AGENTS.MD`
- Create: `docs/superpowers/specs/2026-10-29-aiogram-production-foundation-design.md`

**Interfaces:**
- Produces the project rules and architecture contract used by every later task.

- [ ] **Step 1: Write the design/spec document**
- [ ] **Step 2: Update `AGENTS.MD` with architecture, testing, quality and secret-handling rules**
- [ ] **Step 3: Review both documents for consistency**
- [ ] **Step 4: Commit** — `docs: define bot architecture and engineering rules`

### Task 2: Python package, configuration and composition root

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `src/bot/__init__.py`
- Create: `src/bot/config.py`
- Create: `src/bot/main.py`
- Test: `tests/unit/test_config.py`

**Interfaces:**
- `Settings` loads validated environment configuration.
- `create_bot()`/`create_dispatcher()` compose the application without starting polling during import.

- [ ] **Step 1: Write failing configuration tests**
- [ ] **Step 2: Run `pytest tests/unit/test_config.py -q` and verify failure**
- [ ] **Step 3: Implement validated settings and package metadata**
- [ ] **Step 4: Run the configuration tests and verify pass**
- [ ] **Step 5: Commit** — `feat: add typed application configuration`

### Task 3: Database infrastructure, models and repository boundary

**Files:**
- Create: `src/bot/db/__init__.py`
- Create: `src/bot/db/base.py`
- Create: `src/bot/db/session.py`
- Create: `src/bot/db/models/__init__.py`
- Create: `src/bot/db/models/user.py`
- Create: `src/bot/repositories/__init__.py`
- Create: `src/bot/repositories/users.py`
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/versions/0001_initial.py`
- Test: `tests/unit/test_user_repository.py`

**Interfaces:**
- `get_session_factory(settings)` returns an async SQLAlchemy session factory.
- `UserRepository` owns persistence operations for the user aggregate and does not expose SQLAlchemy details to services.

- [ ] **Step 1: Write repository contract tests with an isolated async database fixture**
- [ ] **Step 2: Run the repository tests and verify failure**
- [ ] **Step 3: Implement async engine/session and model metadata**
- [ ] **Step 4: Implement repository methods and initial migration**
- [ ] **Step 5: Run repository tests and verify pass**
- [ ] **Step 6: Commit** — `feat: add async database and repository layer`

### Task 4: Service layer, Telegram handlers and error boundary

**Files:**
- Create: `src/bot/services/__init__.py`
- Create: `src/bot/services/users.py`
- Create: `src/bot/handlers/__init__.py`
- Create: `src/bot/handlers/start.py`
- Create: `src/bot/middlewares/__init__.py`
- Create: `src/bot/middlewares/errors.py`
- Create: `src/bot/routers.py`
- Test: `tests/unit/test_user_service.py`

**Interfaces:**
- `UserService` contains user-facing business behavior and depends on repository abstractions.
- `/start` handler delegates to `UserService`; it does not query the database directly.

- [ ] **Step 1: Write failing service tests using a fake repository**
- [ ] **Step 2: Run service tests and verify failure**
- [ ] **Step 3: Implement service behavior**
- [ ] **Step 4: Implement handler/router wiring and centralized error middleware**
- [ ] **Step 5: Run service tests and verify pass**
- [ ] **Step 6: Commit** — `feat: add service and telegram handler layers`

### Task 5: Docker, CI, README and skill rules

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `.dockerignore`
- Create: `.github/workflows/ci.yml`
- Create: `README.md`
- Create: `docs/skills/python-aiogram-coder.md`

**Interfaces:**
- CI runs formatting/linting, typing and tests without Telegram credentials.
- The skill document defines the reusable `python-aiogram-coder` behavior: TDD, aiogram 3.31, SQLAlchemy 2, strict layering, migrations, quality gates and safe refactoring.

- [ ] **Step 1: Write the skill rules and README usage contract**
- [ ] **Step 2: Add Docker and CI configuration**
- [ ] **Step 3: Run a repository-wide static validation pass**
- [ ] **Step 4: Commit** — `chore: add containerization ci and developer documentation`

### Task 6: Final verification and delivery

**Files:**
- Modify: files only where verification finds defects.

- [ ] **Step 1: Run the complete test suite**
- [ ] **Step 2: Run Ruff format/check and mypy**
- [ ] **Step 3: Validate Alembic configuration**
- [ ] **Step 4: Inspect the final tree and dependency direction**
- [ ] **Step 5: Create a reviewable pull request from `feat/aiogram-production-foundation` to `main`**
- [ ] **Step 6: Report verification results and the skill document location**
