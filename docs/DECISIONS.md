# Decision Log

## 2026-10-29 — Build KEYDROP as an owned customer storefront

**Context:** The product direction is a Telegram Mini App for digital goods, but the business requirement is to own the customer relationship rather than depend on a third-party storefront client.

**Decision:** KEYDROP will own the customer-facing Mini App, customer data, notification preferences, referrals and repeat-purchase experience. LittleFox is a fulfillment provider only.

**Consequences:** Product architecture must preserve a first-party customer model, server-side order state and a direct Telegram communication channel. Provider APIs are hidden behind the backend.

## 2026-10-29 — Use one repository for MVP

**Context:** The existing repository is the backend/bot foundation and the product now needs a React Mini App.

**Decision:** Add `frontend/` for React + TypeScript + Vite in the same repository for MVP.

**Consequences:** Bot, API, database and frontend documentation/versioning remain coordinated. Splitting repositories can be reconsidered after MVP if operational needs justify it.

## 2026-10-29 — Keep React as a transport client, not the business authority

**Context:** The Mini App needs catalog, cart, checkout, orders, referrals and customer data.

**Decision:** React renders the experience and calls a Python HTTP API. PostgreSQL and LittleFox are never accessed directly by the browser.

**Consequences:** Authorization, pricing, stock, order state, referral attribution and fulfillment remain server-controlled.

## 2026-10-29 — Treat purchase as an idempotent recoverable workflow

**Context:** LittleFox purchase requests can return delivered, repeated, processing, rate-limited or transient failure outcomes.

**Decision:** Persist the operation parameters and idempotency key before the provider request. Unknown outcomes are reconciled using the same key and parameters. Delivery is exposed only after confirmed fulfillment.

**Consequences:** Checkout cannot be implemented as a simple synchronous button-to-success action. Order state, retries and reconciliation are MVP-critical.

## 2026-10-29 — MVP before loyalty/gamification

**Context:** The design direction includes personalization, KEYDROP CLUB, check-ins, quests and achievements.

**Decision:** MVP prioritizes storefront clarity, transaction integrity, fulfillment, order history, notifications and the referral foundation. Loyalty economy and gamification remain post-MVP.

**Consequences:** We can validate the actual purchase and retention loop before adding engagement mechanics.

## 2026-10-29 — Keep transaction ownership at the update boundary for now

**Context:** Issue #32 asked whether `ServicesMiddleware` should stop wrapping the full handler in `session.begin()`.

**Decision:** Do not change the existing transaction boundary without evidence of a material operational problem or a concrete use case requiring a different boundary.

**Consequences:** Preserve current update-level atomicity for the existing bot while the Mini App/API is introduced as a separate transport concern.

## 2026-10-29 — Keep chat features deterministic and non-AI

**Context:** The existing bot product constraint excludes AI behavior.

**Decision:** Product features use explicit rules and auditable behavior. Do not add LLM/model calls, embeddings, AI classifiers or external AI services.

## 2026-10-29 — Keep merge and release decisions explicit

**Context:** Code can pass CI without being approved for merge or deployment.

**Decision:** Do not merge PRs, deploy, or perform destructive actions unless the user explicitly asks.

**Consequences:** CI readiness and product acceptance remain separate decisions.

Record durable decisions that affect architecture, delivery, or operational behavior. Add new entries at the top with date, context, decision and consequences.
