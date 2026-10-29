# KEYDROP MVP Execution Plan

## Objective

Turn the existing Telegram bot repository into a testable Telegram-first digital-goods storefront without destabilizing the current bot foundation.

## Stage 1 — Frontend foundation

### Deliverables
- `frontend/` React + TypeScript + Vite project;
- Telegram Mini App SDK/UI integration;
- AppShell, navigation, theme and viewport handling;
- typed API client;
- basic screens and shared loading/error/empty states.

### Acceptance
- frontend builds;
- TypeScript checks pass;
- Mini App can open in Telegram test configuration;
- frontend has no provider secrets.

## Stage 2 — API and identity

### Deliverables
- HTTP API transport;
- Telegram `initData` validation;
- authenticated customer lookup/create;
- product list/detail endpoints;
- API error contract;
- MVP migrations/models.

### Acceptance
- invalid/expired Telegram auth is rejected;
- authenticated user is resolved deterministically;
- catalog is readable from the Mini App;
- ownership checks are covered by tests.

## Stage 3 — Storefront

### Deliverables
- Home/catalog;
- search/filter basics;
- product detail;
- favorites;
- My KEYDROP/order-history shell.

### Acceptance
- real backend data is displayed;
- loading, empty and error states are usable;
- mobile Telegram viewport behavior is acceptable.

## Stage 4 — Purchase and fulfillment

### Deliverables
- cart;
- server-side cart revalidation;
- internal order model;
- LittleFox adapter;
- idempotency persistence;
- retry/reconciliation state machine;
- delivery protection.

### Acceptance
- test product purchase succeeds;
- repeated request does not create a second provider order;
- processing/unknown result can be reconciled;
- delivery is not exposed before confirmed delivery;
- delivery data is not logged.

## Stage 5 — Orders and communication

### Deliverables
- order detail/timeline;
- successful-delivery notification;
- notification preferences;
- notification delivery records.

### Acceptance
- customer sees the same authoritative order state in Mini App and notification;
- opt-in/opt-out behavior is respected for optional communications.

## Stage 6 — Referral foundation

### Deliverables
- `startapp` referral code format;
- attribution endpoint/flow;
- referral persistence;
- self-referral/duplicate protection;
- minimal referral visibility.

### Acceptance
- A -> referral link -> B -> Mini App produces one stable attribution;
- repeated app opens do not duplicate the relationship;
- invalid/self referral is rejected.

## Stage 7 — Hardening and deployment

### Deliverables
- backend unit/integration tests;
- frontend lint/type/build checks;
- migration checks;
- LittleFox test flow;
- Telegram manual QA;
- test deployment;
- test bot/Mini App configuration.

### Acceptance
- all MVP checklist items in `docs/MVP_PLAN.md` have evidence;
- critical purchase flow works in deployed Telegram environment;
- known limitations are documented.

## Guardrails

- No direct browser -> LittleFox calls.
- No direct browser -> PostgreSQL calls.
- No provider credentials in frontend code.
- No AI/LLM features.
- No loyalty/gamification expansion before the transaction loop is validated.
- No merge/deployment without explicit user approval.

## Verification commands

Backend baseline:

```bash
ruff format --check .
ruff check .
mypy src
pytest -q
alembic upgrade head
alembic check
```

Frontend commands will be added with the Stage 1 project configuration and must include at least build/type/lint verification appropriate to the selected toolchain.
