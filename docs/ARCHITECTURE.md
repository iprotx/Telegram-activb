# KEYDROP Architecture

_Last updated: 2026-10-29_

## Product model

KEYDROP is a Telegram-first digital-goods storefront and customer relationship platform. The Mini App is the customer-facing store; the bot is the communication and notification channel; PostgreSQL is the source of truth for customer, catalog, order, referral and communication state; LittleFox is an external fulfillment provider.

The product is not a white-label client. KEYDROP owns the customer relationship and the data required to operate it.

## Repository shape

```text
Telegram-activb/
├── src/                 # Python application: bot + HTTP API
├── frontend/            # React + TypeScript + Vite Mini App
├── alembic/             # Database migrations
├── docs/                # Product and engineering documentation
└── tests/               # Backend tests
```

The first implementation stage keeps the frontend in the same repository. A separate frontend repository is not required for MVP.

## Runtime boundaries

```text
Telegram
├── Bot / aiogram
│      └── notifications, commands, support entry points
│
└── KEYDROP Mini App
       └── React + TypeScript + Vite
                 │
                 ▼
            KEYDROP HTTP API
                 │
          ┌──────┴──────┐
          ▼             ▼
     PostgreSQL      LittleFox API
          │             │
          └──── order / fulfillment
```

### Frontend

React is the presentation layer. It must not connect directly to PostgreSQL, LittleFox, or private Telegram bot credentials.

Responsibilities:

- render catalog, product, cart, checkout, orders, favorites and customer profile;
- consume KEYDROP API responses;
- pass Telegram Mini App `initData` to the backend for validation/authentication;
- remain responsive to Telegram theme and viewport behavior;
- never contain LittleFox API keys or server secrets.

### Python application

Python remains the backend source of truth. The existing bot architecture stays `handlers -> services -> repositories -> database infrastructure`; the HTTP API is another transport boundary and must not move business rules into the frontend.

Backend responsibilities:

- validate Telegram Mini App identity and request boundaries;
- expose the customer/catalog/order API;
- enforce authorization and ownership;
- calculate order totals and validate product availability;
- create and reconcile LittleFox purchases with idempotency;
- persist delivery and order state safely;
- manage referrals, preferences and notification eligibility;
- send Telegram notifications through aiogram.

## Core data domains

MVP should establish these domains without implementing every future feature:

- `users` — Telegram customer identity and profile;
- `products` / categories — KEYDROP catalog representation;
- `orders` / `order_items` — customer purchase state;
- `favorites` — saved products;
- `user_preferences` / notification preferences — communication controls;
- `referrals` — attribution and referral relationship;
- notification delivery records — auditability of outbound messages.

Future domains such as loyalty ledger, quests, achievements and advanced segmentation are explicitly post-MVP unless a concrete MVP acceptance test requires them.

## Provider boundary

LittleFox is an integration, not a domain model exposed to the frontend. The backend should translate LittleFox products/orders into KEYDROP concepts.

This keeps the customer experience independent of the fulfillment vendor and allows a future provider to be introduced without redesigning the Mini App.

## Customer relationship

The customer lifecycle is:

`Telegram user -> KEYDROP customer -> browse -> purchase -> fulfillment -> notification -> repeat purchase`

Referral attribution and notification preferences belong to KEYDROP. They must not depend on LittleFox's customer model.

## Security boundaries

- Validate Telegram `initData` on the server; do not trust `initDataUnsafe`.
- Keep LittleFox API keys server-side.
- Do not log delivery data, payment secrets, Telegram credentials or API keys.
- A customer can read only their own orders, delivery data and private profile state.
- Order completion is server-confirmed; the frontend cannot mark an order as paid or delivered.
- Financial operations must be idempotent and recoverable after timeouts or unknown responses.

## MVP architecture principle

Prefer a small number of explicit boundaries over premature microservices. One repository, one Python backend, one PostgreSQL database, one React Mini App and one LittleFox integration are sufficient for MVP.
