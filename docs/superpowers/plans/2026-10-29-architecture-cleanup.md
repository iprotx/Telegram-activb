# Architecture Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Упростить архитектуру без большого переписывания и сохранить текущую надёжность.

**Architecture:** Сохраняем текущую границу `handlers → services → repositories → database`. Убираем только безопасную избыточность; границы транзакций и модель активности не меняем без отдельного тестового доказательства.

**Tech Stack:** Python 3.12+, aiogram 3, SQLAlchemy async, Alembic, pytest, Ruff, mypy.

**Spec:** `docs/PROJECT_STATUS.md` и текущая архитектура `src/bot/`.

## Global Constraints

- Не добавлять Redis, очереди, микросервисы или другой инфраструктурный слой без измеренной необходимости.
- Не смешивать `/rank`, `/top`, welcome или moderation с этим cleanup.
- Не менять публичное поведение бота.
- Все изменения должны проходить существующий CI.
- Commit messages — на английском, Conventional Commits.

## Review Focus

- Конфигурация: `BOT_TOKEN` остаётся обязательным, `DATABASE_URL` сохраняет env-over-`.env` precedence.
- Alembic: URL продолжает браться из тех же настроек, что и приложение.
- Транзакции: атомарность регистрации пользователя и activity не должна быть случайно потеряна.
- Activity: repository не должен зависеть от service layer.
- PostgreSQL/SQLite: существующие integration tests должны оставаться зелёными.

### Task 1: Baseline and safe cleanup

**Files:**
- Modify: только файлы, где cleanup подтверждён тестами и не меняет поведение.
- Test: существующие unit/integration suites.

**Interfaces:**
- Consumes: текущие `Settings`, services, repositories и middleware.
- Produces: тот же внешний API и те же runtime semantics.

- [x] Проверить baseline: текущий `main` включает PR #31, а конфигурационные тесты покрывают обязательность токена и env-over-`.env` precedence.
- [x] Не найден подтверждённый мёртвый код, который стоило бы удалять в рамках этой узкой задачи.
- [x] Не менять transaction scope в рамках этого cleanup.
- [x] Уточнить конфигурационную границу тестами: helper загрузки DB URL должен работать без `BOT_TOKEN`.
- [ ] Запустить локально доступные проверки.
- [ ] Проверить GitHub Actions для ветки.
- [ ] Сделать атомарный commit.

### Task 2: Configuration simplification review

**Files:**
- `src/bot/config.py`
- `alembic/env.py`
- `tests/unit/test_config.py`

- [x] Убрать искусственное создание `Settings(bot_token=SecretStr(""))`: выделить общие database settings, сохранив обязательность `BOT_TOKEN` в приложении.
- [x] Сохранить одну реализацию URL validation и env-over-`.env` precedence через наследование настроек; Alembic продолжает вызывать `get_database_url()`.
- [x] Обновить characterization tests, явно проверяющие работу `get_database_url()` без `BOT_TOKEN`.
- [ ] Подтвердить отсутствие drift/регрессий полным набором проверок.

### Task 3: Scalability follow-up

**Files:**
- `src/bot/middlewares/services.py`
- `src/bot/services/`
- `src/bot/repositories/`
- соответствующие tests

- [ ] Отдельно исследовать короткие transaction boundaries.
- [x] Не менять их в этом cleanup без отдельного failing test, доказывающего требуемую семантику.
- [ ] Продолжать отдельной задачей только если появится измеримая проблема.

### Task 4: Verification

- [ ] Ruff format check.
- [ ] Ruff lint.
- [ ] mypy.
- [ ] Alembic migrations/check.
- [ ] Unit tests.
- [ ] PostgreSQL integration tests.
- [ ] pip-audit.
- [ ] Docker build/runtime smoke.
- [ ] Проверить итоговый diff и отсутствие лишнего рефакторинга.
