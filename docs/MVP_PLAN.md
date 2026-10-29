# KEYDROP MVP Plan

_Last updated: 2026-10-29_

## Goal

Deliver a testable Telegram Mini App where a real Telegram user can open KEYDROP, authenticate, browse the catalog, inspect a product, create a cart, complete a server-confirmed purchase through LittleFox, see the resulting order and receive the delivered digital goods. The MVP must also establish the foundation for owned customer relationships and referrals.

## Current implementation status

- Stage 0 — documentation and architecture: **implemented in PR #38; not merged**.
- Stage 1 — React + TypeScript + Vite Mini App foundation: **implemented in PR #38; CI verification pending**.
- Stage 2 — Telegram authentication + `/api/v1/me`: **implemented in PR #38; CI verification pending**.
- Stage 3 — catalog persistence, LittleFox catalog client, product endpoints and basic product cards: **implemented in PR #38; CI verification pending**.
- Stage 3 remaining — richer catalog UX, favorites and cart.
- Stage 4+ — checkout, orders, notifications, referrals and deployment remain ahead.

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

**Status:** authentication foundation implemented; CI verification pending.

- add HTTP API transport without breaking existing aiogram handlers;
- validate Telegram Mini App `initData` server-side;
- expose authenticated customer endpoint;
- persist/synchronize Telegram customer identity through the existing repository layer;
- define stable API authentication errors;
- add API tests for valid, invalid and expired Telegram auth.

**Exit:** a valid Telegram Mini App request resolves exactly one KEYDROP customer, invalid/expired init data is rejected, and the API auth contract is covered by tests.

### Stage 3 — Catalog and storefront

**Status:** catalog data foundation implemented; richer storefront work remains.

- add product/category persistence and LittleFox catalog synchronization boundary;
- expose catalog list/detail endpoints;
- implement Home, Catalog, search/filter basics and Product Detail;
- add favorites;
- add authenticated customer/order-history shell.

**Exit:** Mini App displays real server-controlled product data with usable loading, empty and error states.

### Stage 4 — Cart, checkout and fulfillment

- add cart persistence and server revalidation;
- add internal order model;
- implement LittleFox adapter;
- persist idempotency key and operation parameters before provider purchase;
- implement processing/recovery reconciliation;
- expose delivery only after confirmed provider delivery.

**Exit:** test purchase succeeds, duplicate requests do not create duplicate provider purchases, processing/unknown results reconcile, and delivery data is protected.

### Stage 5 — Orders and communication

- add order detail/timeline;
- add successful-delivery notification;
- add notification preferences;
- add notification delivery records.

**Exit:** Mini App and bot notifications show the same authoritative order state and optional communications respect preferences.

### Stage 6 — Referral foundation

- define `startapp` referral code format;
- attribute referrals server-side;
- persist referral relationship/events;
- protect against self-referral and duplicate/conflicting attribution;
- expose minimal referral status.

**Exit:** A → referral link → B produces one stable attribution and repeated opens do not duplicate it.

### Stage 7 — Hardening and test deployment

- backend unit/integration coverage;
- frontend typecheck/test/build checks;
- migration consistency checks;
- LittleFox test purchase flow;
- Telegram manual QA;
- deploy frontend and backend to a controlled test environment;
- configure test bot/Mini App entry point;
- document known limitations.

**Exit:** every MVP checklist item has evidence and the critical purchase flow works in the deployed Telegram environment.

## MVP READY gate

Do not call the project ready because the code merely builds.

The explicit release statement is:

> **MVP READY — можно тестировать.**

It may be reported only after:

1. frontend is deployed;
2. backend API is deployed;
3. Telegram Mini App opens from the test bot;
4. Telegram authentication is server-validated;
5. catalog/product data is real and server-controlled;
6. test purchase reaches LittleFox;
7. duplicate/retry behavior has been verified;
8. processing/reconciliation behavior has been verified;
9. delivery is withheld until `delivered`;
10. order history is visible to the correct customer;
11. notifications/referral smoke tests pass;
12. known limitations are documented.

At that point report the test entry point, verified scenarios and exact deployment environment. Deployment remains an explicit user approval gate.
