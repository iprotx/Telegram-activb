---
name: python-aiogram-coder
description: >
  Build and refactor production Telegram bots with Python, aiogram 3.31,
  SQLAlchemy 2.x, strict layered architecture, TDD, and explicit quality gates.
---

# python-aiogram-coder

Use this skill for Telegram bot implementation and refactoring in this repository.

## Stack

- Python 3.12+
- aiogram 3.31
- SQLAlchemy 2.x async
- Alembic
- pydantic-settings
- pytest / pytest-asyncio
- Ruff
- mypy

## Workflow

1. Inspect the relevant code, tests, and architecture.
2. Define the smallest coherent change.
3. Write a behavior-level failing test when practical.
4. Implement the smallest change that passes.
5. Refactor while preserving behavior.
6. Run the relevant quality gates.
7. Report evidence rather than assumptions.

## Architecture

Keep dependency direction strict:

`handlers -> services -> repositories -> database infrastructure`

### Handlers

- Telegram transport adapters only.
- Validate transport input at the boundary.
- Call services; do not query SQLAlchemy directly.
- Do not contain business rules.

### Services

- Own business decisions and orchestration.
- Prefer explicit protocols/abstractions where they improve testability.
- Must be testable without aiogram or a live network where practical.

### Repositories

- Encapsulate SQLAlchemy queries and persistence details.
- Keep transaction ownership explicit.
- Prefer `flush()` over hidden commits when the caller owns the transaction.

### Database

- Use SQLAlchemy 2.x typed mappings and async sessions.
- Use Alembic for all schema changes.
- Keep migration configuration deterministic.

## Telegram-specific rules

- Use aiogram 3.31 APIs only; no aiogram 2 patterns.
- Do not start polling during import.
- Keep Telegram-specific code at the architectural edge.
- Never log bot tokens, passwords, or unnecessarily sensitive update payloads.
- Prefer explicit router registration.

## Quality

Before completion, run the applicable checks:

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
```

For database changes:

```bash
alembic upgrade head
alembic check
```

When `/ub-mode` is active, run `crapper`, `dryer`, and `mutator` if installed. If any are missing, skip only that tool and say so explicitly.

## Refactoring

- Characterize existing behavior before risky changes.
- Separate transport, business, and persistence concerns.
- Move one responsibility at a time.
- Fix root causes instead of masking failures.
- Delete obsolete paths only after replacement behavior is covered.

## Completion rule

A task is complete only when implementation, tests, documentation, architecture, and verification evidence agree.
