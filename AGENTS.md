# AGENTS.md

## Mission

This repository is a production-oriented Telegram bot. Prefer simple, explicit designs that are easy to test, review, and operate.

## Stack

- Python 3.12+
- aiogram 3.31
- SQLAlchemy 2.x async
- Alembic
- pydantic-settings
- pytest / pytest-asyncio
- Ruff
- mypy

## Instruction precedence

1. User requirements and explicit task constraints.
2. This `AGENTS.md`.
3. Project-local skills under `skills/`.
4. General engineering conventions.

When a local skill is invoked explicitly (for example `/ub-mode`), follow it unless it conflicts with a higher-priority instruction.

## Required workflow for code changes

### 1. Understand before editing

- Inspect the relevant code, tests, configuration, and existing architecture first.
- State the smallest coherent change that satisfies the requirement.
- Do not introduce abstractions until their boundary is justified.

### 2. TDD / behavior first

- Write or update a behavior-level test before implementation when practical.
- Run the test and confirm it fails for the intended reason.
- Make the smallest implementation change that makes it pass.
- Refactor only after the behavior is pinned by tests.

### 3. Architecture

Dependency direction is strict:

`handlers -> services -> repositories -> database infrastructure`

- `handlers/`: Telegram transport only. Parse updates, perform edge validation, call services, render responses.
- `services/`: business rules and orchestration. Keep them testable without aiogram or a live database where practical.
- `repositories/`: persistence boundary. SQLAlchemy queries and persistence details stay here.
- `db/`: engine, sessions, models, and migration infrastructure.
- `main.py`: composition root. Dependency wiring is allowed here.

Never put SQL queries, persistence details, or business rules directly in handlers.

### 4. Boundaries and types

- Validate external input at the boundary; trust validated values inside the domain.
- Keep business decisions independent of Telegram transport.
- Prefer typed interfaces and explicit dependencies over global mutable state.
- Do not silence mypy to hide a design problem.
- Make illegal states difficult or impossible to represent.
- Design operations to be idempotent where retries or crashes are possible.

### 5. Database

- Use SQLAlchemy 2.x typed mappings and async sessions.
- Repositories should not secretly own transactions unless the boundary explicitly requires it.
- Use Alembic for schema changes; never edit production schema manually.
- Test transaction and failure paths when they matter to the behavior.

### 6. Preventing Alembic drift

A migration must always match the ORM model. Do not let them diverge in intent, naming, or constraint semantics.

- Treat the ORM model and Alembic migration as one synchronized change set.
- After changing a model, generate the migration with `alembic revision --autogenerate -m "..."` instead of editing the migration by hand.
- Review the generated migration before committing. Confirm the exact table, column, unique constraint, index, and foreign key names match the model.
- Prefer explicit names for constraints and indexes to avoid Alembic seeing the same logical thing as two different objects.
- Do not mix equivalent definitions in different forms, for example:
  - `telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)`
  - and a separate migration that creates `ix_chats_telegram_id` as a unique index with a different implied constraint shape
- If a unique field is intended to be unique, define it explicitly and consistently:

```python
class Chat(Base):
    __tablename__ = "chats"
    __table_args__ = (UniqueConstraint("telegram_id", name="uq_chats_telegram_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
```

and in the migration:

```python
op.create_unique_constraint("uq_chats_telegram_id", "chats", ["telegram_id"])
```

or, if using an index, make the naming and semantics match exactly.

- Never commit a schema change where the generated migration differs from the model in a way that `alembic check` would flag.
- Before pushing, run both:

```bash
alembic upgrade head
alembic check
```

- If `alembic check` fails, do not suppress it; fix the root cause by aligning the migration with the model, not by weakening the check.

### 7. Telegram safety

- Target aiogram 3.31 APIs; do not introduce aiogram 2-style patterns.
- Do not start polling during import.
- Never commit tokens, passwords, or other secrets.
- Do not log secrets or unnecessarily sensitive Telegram payloads.
- Keep Telegram-specific code at the edge.

## Local skills

Project-local skills live in `skills/<skill-name>/SKILL.md`.

- `skills/ub-mode/SKILL.md` — disciplined change workflow: make it work, make it right, then practice.
- `skills/python-aiogram-coder/SKILL.md` — project-specific aiogram architecture and quality rules.

When `/ub-mode` is requested or used, apply it to the next code change. If `crapper`, `dryer`, or `mutator` are not installed, skip those individual gates and explicitly report that they were unavailable.

## Quality gates

For every meaningful code change, run the applicable checks:

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
```

For database changes also run:

```bash
alembic upgrade head
alembic check
```

If a check cannot run locally, state why and give the exact CI command instead. Never claim a check passed without evidence.

If `/ub-mode` is active, additionally run `crapper`, `dryer`, and `mutator` when those executables are actually installed. Skip only missing tools.

## Refactoring rules

- Pin observable behavior with tests before risky structural changes.
- Fix root causes rather than adding guards that merely hide failures.
- Prefer subtraction before introducing new abstractions.
- Make one coherent change at a time and verify it.
- Remove dead code only after replacement behavior is covered.
- Keep dependency direction intact.

## Completion checklist

Before declaring work complete:

- [ ] Requirements are satisfied.
- [ ] Relevant behavior is covered by tests.
- [ ] Architecture boundaries remain intact.
- [ ] Ruff format and lint pass.
- [ ] mypy passes.
- [ ] pytest passes.
- [ ] Alembic checks pass when relevant.
- [ ] ub-mode quality tools were run when installed, or explicitly skipped when absent.
- [ ] No secrets or unrelated changes were introduced.
- [ ] The final response reports what changed and what was verified.

## Git discipline

- Keep commits small and ordered by intent.
- Use concise conventional-style messages: `feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `chore:`.
- Each meaningful commit should make it clear why the change exists and how it was verified.
- Do not rewrite or discard unrelated user work.
