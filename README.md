# Telegram-activb

Production-oriented Telegram bot foundation using aiogram 3.31 and SQLAlchemy 2.

## Architecture

```text
Telegram update
      |
   handlers
      |
   services
      |
 repositories
      |
 SQLAlchemy / DB
```

The composition root is `src/bot/main.py`. Business logic lives in services and persistence is isolated behind repositories.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
# edit .env and set BOT_TOKEN
alembic upgrade head
python -m bot.main
```

## Checks

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
alembic upgrade head
alembic check
```

## Docker

```bash
cp .env.example .env
# edit .env

docker compose up --build -d
```

## Project rules

See `AGENTS.MD` for contribution and architecture rules.

The reusable coding rules discussed for `python-aiogram-coder` are kept in `docs/skills/python-aiogram-coder.md`.
