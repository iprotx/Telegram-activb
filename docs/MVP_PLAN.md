# KEYDROP MVP Plan

_Last updated: 2026-10-29_

## Goal

Deliver a testable Telegram Mini App where a real Telegram user can open KEYDROP, authenticate, browse the catalog, inspect a product, create a cart, complete a server-confirmed purchase through LittleFox, see the resulting order and receive the delivered digital goods. The MVP must also establish the foundation for owned customer relationships and referrals.

## Current implementation status

- Stage 0 — documentation and architecture: **implemented in PR #38; not merged**.
- Stage 1 — React + TypeScript + Vite Mini App foundation: **implemented in PR #38; CI verification pending**.
- Stage 2+ — backend API, catalog integration, checkout, orders, notifications, referrals and deployment: **not started**.

## MVP definition

### Must work

1. Telegram Mini App opens from the bot.
2. Telegram identity is validated server-side.
3. Customer is created/synchronized in PostgreSQL.
4. Catalog is available through KEYDROP API, with server-side availability and price data.
5. Product details are shown clearly.
6. Cart is created and revalidated by the server.
7. Checkout creates a KEYDROP order and a LittleFox purchase with idempotency protection.
8. Unknown/processing LittleFox responses can be reconciled without creating a duplicate purchase.
9. Delivery is shown only after the backend confirms `delivered`.
10. Customer can view their own order history and order details.
11. Customer can save/remove favorites.
12. Customer can control essential notification preferences.
13. A referral link can attribute a new Telegram customer to an existing customer.
14. A basic notification can be sent to eligible customers through the bot.
15. Test deployment is available for controlled Telegram testing.

### Explicitly not required for MVP

- full loyalty/bonus economy;
- quests, achievements and daily check-ins;
- advanced CRM segmentation UI;
- recommendation engine;
- complex campaign builder;
- multi-provider fulfillment;
- public SEO website;
- AI/LLM features;
- native mobile apps.

These remain post-MVP capabilities unless a later product decision promotes one into scope.

## Delivery stages

### Stage 0 — Documentation and architecture

**Status:** implemented in PR #38; not merged.

- align repository documentation with KEYDROP product model;
- define one-repository layout;
- document React + TypeScript + Vite frontend boundary;
- document Python API boundary;
- document LittleFox integration and security rules;
- define MVP acceptance criteria.

**Exit:** architecture and MVP plan are explicit and approved.

### Stage 1 — Frontend foundation

**Status:** implemented in PR #38; CI verification pending.

- create `frontend/` React + TypeScript + Vite application;
- add Telegram Mini App SDK integration using current supported versions;
- implement AppShell, theme handling, safe-area/viewport behavior and navigation shell;
- create typed API client boundary;
- establish loading/error/empty-state foundations.

**Exit:** Mini App shell exists, initializes the Telegram SDK, supports browser mocking, and has frontend typecheck/test/build checks in CI.

### Stage 2 — Backend API foundation

- add HTTP API transport without breaking existing aiogram handlers;
- validate Telegram Mini App `initData` server-side;
- expose authenticated customer endpoint;
- add catalog/product endpoints;
- establish API error format and authorization rules;
- add database models and Alembic migrations for MVP domains.

**Exit:** authenticated Mini App can read customer and catalog data from KEYDROP API.

### Stage 3 — Catalog and customer UX

- Home/catalog/search/filter basics;
- product detail page;
- favorites;
- customer profile / My KEYDROP;
- order-history shell;
- responsive Telegram UI states.

**Exit:** user can browse, inspect and save products end-to-end against real backend data.

### Stage 4 — Cart and checkout

- cart persistence;
- server-side cart revalidation;
- price/stock validation at checkout;
- explicit checkout states;
- create internal order before external purchase;
- LittleFox idempotency key generation and persistence;
- retry/reconciliation handling;
- delivery visibility only after confirmed fulfillment.

**Exit:** a test product can be purchased without duplicate charging and its delivery can be displayed to the owner.

### Stage 5 — Orders and notifications

- order timeline/status mapping;
- order detail and delivery display;
- bot notification for successful delivery;
- notification preferences;
- notification delivery audit record;
- safe failure messages and retry behavior.

**Exit:** customer can follow a purchase from checkout to delivered order and receive the expected Telegram notification.

### Stage 6 — Referral foundation

- `startapp` referral attribution;
- referral relationship persistence;
- protection against self-referral and duplicate attribution;
- basic reward/event model, without a complex loyalty economy;
- referral visibility in My KEYDROP.

**Exit:** A invites B, B opens KEYDROP through the referral link, attribution is persisted, and the relationship remains visible to backend tests/admin inspection.

### Stage 7 — MVP hardening and test deployment

- full backend unit/integration tests;
- frontend build/type/lint checks;
- migration consistency checks;
- LittleFox test-product flow;
- Telegram Mini App manual QA;
- mobile viewport/theme QA;
- error/retry/idempotency scenarios;
- deployment to a non-production test environment;
- test bot configured to launch the Mini App.

**Exit:** all MVP acceptance criteria are evidenced by tests or manual QA and the test environment is reachable from Telegram.

## MVP acceptance checklist

- [ ] Mini App launches from Telegram.
- [ ] `initData` is validated server-side.
- [ ] Customer identity is persisted.
- [ ] Catalog loads from KEYDROP API.
- [ ] Product detail loads.
- [ ] Favorites work.
- [ ] Cart works.
- [ ] Server revalidates price/stock before purchase.
- [ ] LittleFox test purchase succeeds.
- [ ] Duplicate/retry purchase does not double-charge.
- [ ] Processing order can be reconciled.
- [ ] Delivery is withheld until `delivered`.
- [ ] Order history/detail works.
- [ ] Telegram delivery notification works when permitted.
- [ ] Notification preferences are respected.
- [ ] Referral attribution works.
- [ ] Backend tests pass.
- [ ] Frontend checks pass.
- [ ] Alembic checks pass.
- [ ] Test deployment works.
- [ ] Manual Telegram QA passes on the target mobile clients.

## MVP READY gate

MVP is **not** considered ready merely because the code builds. The project is MVP READY only when the acceptance checklist has evidence and the deployed test environment has completed the critical purchase flow.

When this gate is reached, report explicitly:

> **MVP READY — можно тестировать.**

The report must include the test environment, test bot/Mini App entry point, what was verified, known limitations and the exact test scenarios to run.

## After MVP

Priority order:

1. customer segmentation and targeted campaigns;
2. richer referral rewards;
3. loyalty / KEYDROP CLUB;
4. product subscriptions and availability notifications;
5. personalization and recommendations;
6. quests, achievements and other gamification.
