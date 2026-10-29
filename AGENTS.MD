# AGENTS.md

## Project

This repository is a production-oriented Telegram bot built with Python, aiogram 3.31 and SQLAlchemy 2.x.

## Architecture

Use strict dependency direction:

`handlers -> services -> repositories -> database infrastructure`

- `handlers/`: Telegram transport only. Parse updates, call services, render responses.
- `services/`: business rules and orchestration. Must be testable without aiogram or a live database.
- `repositories/`: persistence boundary. SQLAlchemy details stay here.
- `db/`: engine, sessions, models and migrations.
- `main.py`: composition root; wiring is allowed here.

Do not put SQL queries, repository calls or business rules directly in handlers.

## Development rules

1. Use TDD: write a failing test, implement the smallest change, then refactor.
2. Target aiogram 3.31 APIs; do not introduce aiogram 2-style patterns.
3. Use SQLAlchemy 2.x APIs and async sessions.
4. Use Alembic for schema changes; never modify production schema manually.
5. Keep configuration typed and environment-driven. Never commit bot tokens, passwords or other secrets.
6. Prefer small focused modules and explicit dependencies over global mutable state.
7. New behavior needs tests at the appropriate boundary.
8. Refactors must preserve behavior and should be accompanied by a regression test when risk is non-trivial.

## Quality gates

Before considering a change complete, run:

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
```

For database changes also validate Alembic configuration/migrations.

## Runtime

- Do not start polling on import.
- Keep logs on stdout/stderr.
- Load secrets only from environment variables.
- CI must be runnable without Telegram credentials.

## Commits

Use concise conventional-style commit messages such as `feat:`, `fix:`, `test:`, `docs:`, and `chore:`.

## Review checklist

- Does the dependency direction remain intact?
- Is business logic independent of Telegram?
- Are persistence details isolated?
- Are failure paths and transaction boundaries tested?
- Are secrets absent from source, tests and examples?
- Do lint, type checks and tests pass?
