# KEYDROP

Production-oriented Telegram bot foundation evolving into a Telegram-first digital-goods storefront.

## Product

KEYDROP will provide a first-party Telegram Mini App where customers can browse digital goods, purchase them, receive fulfillment, view order history, manage favorites, use referrals and control relevant notifications.

The customer relationship belongs to KEYDROP. LittleFox is used as an external fulfillment provider.

## Architecture

```text
Telegram
├── Bot / aiogram
│      └── commands + notifications
│
└── KEYDROP Mini App
       └── React + TypeScript + Vite
                 │
                 ▼
            Python HTTP API
                 │
          ┌──────┴──────┐
          ▼             ▼
     PostgreSQL      LittleFox
```

The MVP keeps all components in this repository:

```text
Telegram-activb/
├── src/                 # Python bot + API
├── frontend/            # React + TypeScript + Vite Mini App
├── alembic/             # migrations
├── docs/                # architecture, API, integrations and MVP plan
└── tests/
```

React is never allowed to connect directly to PostgreSQL or LittleFox. Telegram Mini App identity is validated by the backend.

## Documentation

- [Project status](docs/PROJECT_STATUS.md)
- [MVP plan](docs/MVP_PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API contract](docs/API.md)
- [Integrations](docs/INTEGRATIONS.md)
- [LittleFox integration](docs/integrations/littlefox.md)
- [Decision log](docs/DECISIONS.md)
- [Work log](docs/WORKLOG.md)

## Current backend stack

- Python 3.12+
- aiogram 3.31
- SQLAlchemy 2.x async
- Alembic
- PostgreSQL / SQLite for development
- pydantic-settings
- pytest / pytest-asyncio
- Ruff
- mypy
- Docker Compose

## Current status

The existing bot foundation is working and has registration, group activity/XP, `/rank`, `/top` and group-join welcome behavior. The Mini App/API/MVP implementation is the next product stage.

See `docs/MVP_PLAN.md` for the staged delivery plan and the explicit **MVP READY** gate.

## Development

The existing bot can still be run using the environment documented below. The Mini App setup will be added as Stage 1 of the MVP plan rather than mixing unimplemented frontend instructions into the current setup.

### Configuration

Copy `.env.example` to `.env` and set at least `BOT_TOKEN`.

For native development with SQLite:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

For Docker Compose/PostgreSQL:

```dotenv
BOT_TOKEN=123456789:your-real-token
DATABASE_URL=postgresql+asyncpg://telegram_activb:your-url-safe-password@postgres:5432/telegram_activb
POSTGRES_DB=telegram_activb
POSTGRES_USER=telegram_activb
POSTGRES_PASSWORD=your-url-safe-password
LOG_LEVEL=INFO
```

Never commit `.env` or secrets.

## Quality checks

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
alembic upgrade head
alembic check
```

For Docker:

```bash
docker compose up --build -d
docker compose logs -f bot
docker compose down
```

## Product principles

- transaction integrity before gamification;
- server-side authority for identity, price, stock and order state;
- idempotent/recoverable purchases;
- own customer relationship and notification preferences;
- deterministic, testable behavior; no AI/LLM features;
- small explicit architecture before premature infrastructure.
