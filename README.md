# Telegram-activb

Production-oriented Telegram bot foundation using aiogram 3.31 and SQLAlchemy 2.

## Project status and planning

- [Current status, priorities and backlog](docs/PROJECT_STATUS.md)
- [Work log](docs/WORKLOG.md)
- [Decision log](docs/DECISIONS.md)
- [Detailed production-hardening plan](docs/superpowers/plans/2026-10-29-production-hardening.md)

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

## Requirements

The project supports Python `3.12` and `3.13` (`>=3.12,<3.14`).

You need:

- a Telegram bot token created through [@BotFather](https://t.me/BotFather);
- Git;
- Python 3.12 or 3.13 for a native/WSL installation, or Docker Desktop for a Docker installation.

For local development, SQLite can be used without installing PostgreSQL. Docker Compose uses PostgreSQL 17 automatically.

## Configuration

Copy `.env.example` to `.env` and set at least `BOT_TOKEN`.

### Native/WSL development with SQLite

Use SQLite when you want the simplest local setup:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

`POSTGRES_*` variables are not needed for this mode.

### PostgreSQL / Docker Compose

For Docker Compose, keep the PostgreSQL settings from `.env.example` and replace the placeholder password and bot token:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=postgresql+asyncpg://telegram_activb:your-url-safe-password@postgres:5432/telegram_activb
POSTGRES_DB=telegram_activb
POSTGRES_USER=telegram_activb
POSTGRES_PASSWORD=your-url-safe-password
LOG_LEVEL=INFO
```

The database host is `postgres` because the bot and PostgreSQL run in the same Compose network. Do not change it to `localhost` inside the Compose configuration.

## Installation by environment

### Windows 10/11 — PowerShell

This is the simplest native Windows development setup. It runs the bot directly on Windows and uses SQLite.

1. Install Python 3.12 or 3.13 and make sure `python` is available in PowerShell.
2. Clone the repository and enter it:

```powershell
git clone https://github.com/iprotx/Telegram-activb.git
cd Telegram-activb
```

3. Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use the current PowerShell session with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

4. Install the project and development tools:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

5. Create `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and set:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

6. Apply migrations and start the bot:

```powershell
alembic upgrade head
python -m bot.main
```

Stop the bot with `Ctrl+C`.

### Ubuntu — native Linux

1. Install Git, Python and the virtual-environment package:

```bash
sudo apt update
sudo apt install -y git python3.12 python3.12-venv
```

If your Ubuntu release provides Python 3.13 instead, use `python3.13` in the commands below.

2. Clone the repository:

```bash
git clone https://github.com/iprotx/Telegram-activb.git
cd Telegram-activb
```

3. Create and activate the virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

4. Install the project and development tools:

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

5. Create `.env` and configure SQLite:

```bash
cp .env.example .env
nano .env
```

Set:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

6. Run migrations and start:

```bash
alembic upgrade head
python -m bot.main
```

### WSL 2 — Ubuntu

WSL uses the same Linux setup as Ubuntu. Keep the repository inside the WSL filesystem (for example `~/src/Telegram-activb`) for better performance.

1. Install WSL 2 with Ubuntu from an elevated PowerShell:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if requested, then open Ubuntu.

2. Inside Ubuntu, follow the native Ubuntu instructions above. In short:

```bash
sudo apt update
sudo apt install -y git python3.12 python3.12-venv
git clone https://github.com/iprotx/Telegram-activb.git
cd Telegram-activb
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env
```

3. Configure `.env` for SQLite:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

4. Start the bot:

```bash
alembic upgrade head
python -m bot.main
```

Do not use Windows `.venv` files from `/mnt/c/...` inside WSL. Create the virtual environment from Linux in the WSL checkout.

### Windows + Docker Desktop

Use this mode when you want the application and PostgreSQL to run in containers. This is the recommended way to reproduce the production-style database topology on Windows.

1. Install Docker Desktop for Windows with the WSL 2 backend enabled.
2. Clone the repository in PowerShell:

```powershell
git clone https://github.com/iprotx/Telegram-activb.git
cd Telegram-activb
```

3. Create `.env`:

```powershell
Copy-Item .env.example .env
```

4. Edit `.env` and set the real token and a URL-safe PostgreSQL password:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=postgresql+asyncpg://telegram_activb:your-url-safe-password@postgres:5432/telegram_activb
POSTGRES_DB=telegram_activb
POSTGRES_USER=telegram_activb
POSTGRES_PASSWORD=your-url-safe-password
LOG_LEVEL=INFO
```

5. Build and start both services:

```powershell
docker compose up --build -d
```

The Compose configuration starts PostgreSQL 17, waits for its health check, runs the bot image, and uses a named Docker volume for PostgreSQL data.

6. Check the containers and logs:

```powershell
docker compose ps
docker compose logs -f bot
```

7. Stop the stack without deleting database data:

```powershell
docker compose down
```

To remove the PostgreSQL volume as well (this deletes the local database data):

```powershell
docker compose down -v
```

## First start checklist

After the bot starts successfully:

1. Add the bot to a Telegram group.
2. Grant only the permissions the current bot features require.
3. Send `/start` in the chat.
4. Check the container/process logs for startup errors.

For group activity tracking, remember that Telegram bot privacy settings affect which group messages a bot receives. If a feature depends on ordinary group messages, review the bot's privacy mode in BotFather and the permissions of the bot in the target group.

## Useful commands

### Native Windows / Ubuntu / WSL

```bash
# Activate the environment first.
python -m bot.main

# Database migrations
alembic upgrade head

# Formatting and linting
ruff format --check .
ruff check .

# Type checking
mypy src

# Tests
pytest -q

# Check migration consistency
alembic check
```

On PowerShell, the commands are the same after `.venv` activation.

### Docker Compose

```bash
# Build and start
docker compose up --build -d

# Follow bot logs
docker compose logs -f bot

# Follow all service logs
docker compose logs -f

# Restart the bot
docker compose restart bot

# Stop containers, keep PostgreSQL volume
docker compose down

# Stop containers and delete PostgreSQL data
docker compose down -v
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

The repository contains a `Dockerfile` and `docker-compose.yml` for a PostgreSQL-backed deployment. Docker Compose provides PostgreSQL 17 and persists its data in the `postgres-data` named volume.

```bash
cp .env.example .env
# edit .env

docker compose up --build -d
```

## Troubleshooting

### `BOT_TOKEN` is missing or rejected

Check `.env` and make sure the token is copied exactly from BotFather. Do not commit `.env` to Git.

### The bot starts but does not receive ordinary group messages

Check the bot's Telegram privacy mode and its group permissions. Telegram may intentionally hide ordinary group messages from bots when privacy mode is enabled.

### Docker bot cannot connect to PostgreSQL

Inside Docker Compose, use:

```dotenv
DATABASE_URL=postgresql+asyncpg://telegram_activb:your-url-safe-password@postgres:5432/telegram_activb
```

Do not use `localhost` as the database host from the `bot` container. Also verify that the PostgreSQL service is healthy with `docker compose ps`.

### Port conflicts on Windows

The current Compose file does not publish PostgreSQL to the Windows host, so a host PostgreSQL installation normally does not conflict with it. The bot also does not publish an HTTP port.

### Reset a broken local Docker database

If the local PostgreSQL data is disposable, recreate the volume:

```powershell
docker compose down -v
docker compose up --build -d
```

## Project rules

See `AGENTS.md` for contribution and architecture rules.

Project-local engineering skills are kept under `skills/`:

- `skills/ub-mode/SKILL.md` — disciplined TDD, architecture, review and debugging workflow.
- `skills/python-aiogram-coder/SKILL.md` — aiogram-specific project conventions.
