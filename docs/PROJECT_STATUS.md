# Project Status

_Last reconciled: 2026-10-29_

## Current product direction

KEYDROP is evolving from the current aiogram bot foundation into a Telegram-first digital-goods storefront with its own customer base.

The target product consists of:

- React + TypeScript + Vite Telegram Mini App;
- Python backend and aiogram bot;
- PostgreSQL as the source of truth;
- LittleFox as external digital-goods fulfillment;
- customer preferences, notifications and referrals owned by KEYDROP.

The frontend lives in this repository under `frontend/`.

## Current repository state

- **Default branch:** `main`
- **Current foundation:** aiogram 3.31, SQLAlchemy 2.x async, Alembic, PostgreSQL/SQLite development support, Docker Compose and CI quality gates.
- **Existing bot features:** registration/profile synchronization, group activity/XP, `/rank`, `/top`, and group-join welcome behavior.
- **Mini App:** Stage 1 foundation is implemented in PR #38; it is not merged into `main` yet.
- **Backend API:** not implemented yet.

## Architecture decisions

- Keep one repository for MVP.
- Keep the existing backend dependency direction: `handlers -> services -> repositories -> database infrastructure`.
- Add the HTTP API as a transport boundary; do not move business logic into React.
- React must never access PostgreSQL or LittleFox directly.
- Telegram Mini App identity is validated server-side.
- LittleFox credentials remain server-side.
- Purchase operations are idempotent and recoverable.
- KEYDROP owns the customer relationship; LittleFox is a fulfillment provider.
- MVP prioritizes transaction integrity and repeatable customer journeys over gamification.

## MVP roadmap

See `docs/MVP_PLAN.md` for the detailed staged plan.

1. Documentation/architecture foundation — **implemented in PR #38; not merged**
2. React/Vite Mini App foundation — **implemented in PR #38; CI verification pending**
3. Python API + authenticated customer/catalog endpoints — **not started**
4. Catalog/customer UX — **not started**
5. Cart/checkout/LittleFox fulfillment — **not started**
6. Orders/notifications — **not started**
7. Referral foundation — **not started**
8. MVP hardening + test deployment — **not started**

## MVP gate

MVP is ready only when the critical Telegram purchase flow is working in a deployed test environment and the acceptance checklist in `docs/MVP_PLAN.md` has evidence.

At that point the project report must explicitly say **MVP READY — можно тестировать** and provide the test entry point, verified scenarios and known limitations.

## Out of MVP scope

Full loyalty economy, KEYDROP CLUB, quests, achievements, advanced segmentation/campaign UI, recommendations, multi-provider fulfillment, public SEO site and AI features remain post-MVP unless explicitly promoted into scope.

## Reliability rules

- Done requires evidence from tests, CI, a merged commit, deployment verification or an explicit architectural decision.
- CI green does not by itself prove product readiness.
- Merge and deployment remain explicit human decisions.
- Keep production secrets out of the repository and logs.

## Documentation map

- `docs/ARCHITECTURE.md` — target system boundaries and responsibilities.
- `docs/API.md` — Mini App ↔ Python API contract.
- `docs/INTEGRATIONS.md` — external integration boundaries.
- `docs/integrations/littlefox.md` — LittleFox adapter and purchase rules.
- `docs/MVP_PLAN.md` — staged delivery plan and MVP READY gate.
- `docs/DECISIONS.md` — durable architecture/product decisions.
- `docs/WORKLOG.md` — chronological execution evidence.
