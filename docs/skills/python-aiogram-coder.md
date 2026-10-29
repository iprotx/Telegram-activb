# python-aiogram-coder

Reusable engineering rules for Telegram bots built with aiogram 3.31.

## Core behavior

- Start from the user's requirements and inspect the existing repository before changing code.
- Prefer small, reversible changes with explicit boundaries.
- Use TDD: failing test -> minimal implementation -> passing test -> refactor.
- Never claim a fix or completion without running the relevant verification.

## Stack

- Python 3.12+
- aiogram 3.31
- SQLAlchemy 2.x async
- Alembic
- pydantic-settings
- pytest / pytest-asyncio
- Ruff
- mypy

## Architecture

Enforce:

`handlers -> services -> repositories -> database`

Handlers are transport adapters. Services own business behavior. Repositories own persistence. The composition root wires dependencies.

### Handlers

- Accept Telegram events and validate transport-level input.
- Call services rather than querying the database.
- Do not contain business rules.

### Services

- Depend on protocols/abstractions where useful.
- Must be testable without aiogram, Bot objects or a live network.
- Own business decisions and transaction orchestration boundaries.

### Repositories

- Encapsulate SQLAlchemy queries and persistence details.
- Prefer `flush()` over committing inside repository methods when the caller owns the transaction.
- Keep models and SQLAlchemy expressions out of handlers/services.

### Database

- Use SQLAlchemy 2.x typed mappings and async sessions.
- Schema changes are Alembic migrations.
- Roll back failed transactions.

## Quality

Every non-trivial change should have focused tests. Before completion run:

```text
ruff format --check .
ruff check .
mypy src
pytest -q
alembic upgrade head
alembic check
```

## Telegram-specific safety

- Do not log bot tokens, passwords, or sensitive update payloads.
- Do not start polling during import.
- Keep Telegram-specific code at the edge of the architecture.
- Prefer explicit router registration.

## Refactoring

When cleaning an existing bot:

1. Characterize behavior with regression tests.
2. Separate transport, business and persistence concerns.
3. Move one responsibility at a time.
4. Run tests and quality gates after each meaningful step.
5. Delete obsolete paths only after replacement behavior is covered.

## Completion rule

A task is complete only when the implementation, tests, documentation and quality checks agree. If a check cannot be executed in the current environment, say so explicitly and provide the exact command that CI will execute.
