# Aiogram Production Foundation Design

## Goal

Establish a small but production-oriented foundation for a Telegram bot. The repository is intentionally empty today, so this design prioritizes clear boundaries, testability and low operational surprise over feature breadth.

## Architecture

The application is composed at `src/bot/main.py` and flows inward:

`Telegram update -> handler -> service -> repository -> SQLAlchemy session`

Handlers know aiogram. Services contain business rules and depend on repository interfaces/protocols. Repositories own persistence details. Database models and sessions remain infrastructure concerns. Configuration is validated at startup and secrets come only from the environment.

## Technology

- Python 3.12+
- aiogram 3.31
- SQLAlchemy 2.x async API
- Alembic
- pydantic-settings
- pytest + pytest-asyncio
- Ruff
- mypy
- Docker Compose
- GitHub Actions

## Package layout

```text
src/bot/
  config.py
  main.py
  routers.py
  handlers/
  middlewares/
  services/
  repositories/
  db/
    base.py
    session.py
    models/

tests/
  unit/

alembic/
docs/
```

## Dependency rules

1. `handlers` may depend on `services` and aiogram, but not directly on repositories or SQLAlchemy.
2. `services` may depend on repository abstractions and domain data, but not aiogram or Bot API objects.
3. `repositories` may depend on SQLAlchemy and database models.
4. `db` contains persistence infrastructure and models only.
5. `main.py` is the composition root and may connect all layers.
6. No import-time polling, database connections, or secret loading with side effects.

## Persistence

Use one async engine and session factory configured from `Settings`. Repository methods receive a session and perform explicit transactions. Failed writes must roll back; sessions must be closed by the owning context manager.

The initial model is intentionally small: a Telegram user identified by `telegram_id`, with basic display metadata and timestamps. This is infrastructure for future features, not a domain feature in itself.

## Testing

Tests are written before implementation for each layer. Service tests use fakes/mocks rather than Telegram or a live network. Repository tests use an isolated database fixture. The CI gate is Ruff, mypy and pytest.

## Configuration

Required environment values are validated at startup. `BOT_TOKEN` is required for real execution but must not be required by static checks or unit tests that do not start polling. `DATABASE_URL` defaults to a local SQLite async URL for development/tests and can be replaced with PostgreSQL in deployment.

## Operational baseline

Docker runs the application from a non-development image. CI never needs Telegram credentials. Logs go to stdout/stderr so the hosting platform can collect them. Alembic owns schema changes.

## Skill alignment

`docs/skills/python-aiogram-coder.md` is the repository-local canonical version of the reusable coding rules discussed in the task. It emphasizes TDD, aiogram 3.31, SQLAlchemy 2, strict layering, safe refactoring and verification before completion.
