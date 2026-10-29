# Architecture Cleanup Implementation Plan

> **For agentic workers:** Follow the relevant project skills and use tests before changing behavior.

**Goal:** Упростить архитектуру без большого переписывания и сохранить текущую надёжность.

**Architecture:** Сохраняем `handlers → services → repositories → database`. Меняем только то, для чего есть конкретная польза и тестовое доказательство.

**Tech Stack:** Python 3.12+, aiogram 3, SQLAlchemy async, Alembic, pytest, Ruff, mypy.

## Global constraints

- Не добавлять Redis, очереди, микросервисы или другую инфраструктуру без измеренной необходимости.
- Не смешивать `/rank`, `/top`, welcome или moderation с архитектурной очисткой.
- Не менять публичное поведение без regression tests.
- Commit messages — на английском, Conventional Commits.

## Completed: configuration boundary

- [x] Выделен `DatabaseSettings`, общий URL validation и env-over-`.env` precedence сохранены.
- [x] `Settings` по-прежнему требует `BOT_TOKEN`; Alembic может загрузить DB URL без него.
- [x] PR #33 merged: [ec6ad18](https://github.com/iprotx/Telegram-activb/commit/ec6ad18c7477508f3854ff32308dc897f3c94658).
- [x] CI до merge прошёл все настроенные проверки: [run #198](https://github.com/iprotx/Telegram-activb/actions/runs/40889013179).

## Completed: transaction boundary investigation (issue #32)

- [x] Проверены все текущие message handlers: `start_handler`, `activity_message_handler`; callback-query handlers не обнаружены.
- [x] Найден внешний вызов внутри транзакции: `/start` вызывает `message.answer()` после регистрации.
- [x] Подтверждено, что activity handler выполняет только DB operations.
- [x] Изучены middleware unit tests и PostgreSQL rollback integration test.
- [x] Зафиксировано решение: сохранить текущую транзакцию на update; сейчас нет измерений, оправдывающих смену контракта.
- [x] Не менять production code: переход на отдельные commits внутри сервисов ослабил бы rollback-атомарность регистрации и activity.
- [x] Решение и условия повторного рассмотрения записаны в `docs/DECISIONS.md`.

## Verification and follow-up

- [x] Source and tests reviewed from current `main`.
- [x] No production code or dependencies changed in the investigation.
- [ ] Merge the documentation PR and close issue #32.
- [ ] Next feature work: implement `/rank`, then `/top`, separately.
