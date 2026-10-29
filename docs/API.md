# KEYDROP HTTP API

_Last updated: 2026-10-29_

This document defines the internal API boundary between the React Mini App and the Python backend. It is an MVP contract, not a promise to expose the API publicly.

## Principles

- Telegram Mini App `initData` is sent to the backend and validated server-side.
- The frontend never receives LittleFox credentials.
- The frontend never writes directly to PostgreSQL.
- Authorization is based on the authenticated Telegram customer.
- Purchase state is owned by KEYDROP, not by the client.
- Responses expose KEYDROP concepts rather than LittleFox-specific internals where practical.

## Authentication

The Mini App sends raw Telegram initialization data in the `Authorization` header:

```text
Authorization: tma <raw Telegram initData>
```

The backend validates the signature with the bot token, validates `auth_date`, parses the Telegram user payload and only then resolves the KEYDROP customer. The client must not use `initDataUnsafe` as an authentication source.

The current API accepts initialization data for up to one hour by default. This value is configurable server-side with `TELEGRAM_INIT_DATA_MAX_AGE`.

## MVP endpoints

### Health

`GET /api/v1/health`

Returns a minimal process health response and does not require Telegram authentication.

### Customer

`GET /api/v1/me`

Returns the authenticated KEYDROP customer and essential notification preferences.

The first authenticated request creates the local customer if the Telegram account is not already present. Subsequent requests synchronize the Telegram profile fields through the existing user repository.

### Catalog

`GET /api/v1/products`

Supported MVP query parameters may include `page`, `limit`, `category`, `search` and `available`.

`GET /api/v1/products/{product_id}`

Returns product facts, price, availability and delivery-related description data that is safe to display before purchase.

### Favorites

`GET /api/v1/favorites`

`PUT /api/v1/favorites/{product_id}`

`DELETE /api/v1/favorites/{product_id}`

All operations are scoped to the authenticated customer.

### Cart

`GET /api/v1/cart`

`PUT /api/v1/cart`

`POST /api/v1/cart/validate`

The server is authoritative for current price and availability. The client must not assume that a previously displayed price remains valid at checkout.

### Orders

`GET /api/v1/orders`

`GET /api/v1/orders/{order_id}`

`POST /api/v1/orders`

The create-order request contains product/quantity intent. The backend calculates and validates the payable amount and manages the LittleFox operation key.

The frontend must never submit a trusted final amount as an instruction to charge.

### Notifications

`GET /api/v1/notification-preferences`

`PUT /api/v1/notification-preferences`

Only communication categories that the product actually supports should be exposed. Transactional order updates are distinct from optional marketing/product notifications.

### Referrals

`GET /api/v1/referral`

`POST /api/v1/referral/attribute`

Referral attribution is created from a Telegram `startapp` value after server-side validation. The backend must reject self-referral and conflicting attribution according to the referral policy.

## Error model

Use a stable JSON shape with a machine-readable `code` and human-readable message. Suggested categories:

- `unauthorized`
- `forbidden`
- `not_found`
- `validation_error`
- `product_unavailable`
- `price_changed`
- `order_in_progress`
- `purchase_processing`
- `purchase_failed`
- `rate_limited`
- `internal_error`

The frontend maps these to predictable UI states; it must not parse provider-specific error strings.

## Purchase contract

A purchase is a state machine, not a synchronous button action:

`checkout -> order created -> provider processing -> delivered | failed | recovering`

The backend persists the LittleFox idempotency key and operation parameters before making the provider request. If the response is unknown or processing, the same operation is reconciled rather than creating a new purchase with a new key.

Delivery data is returned only for the authenticated owner after the provider confirms delivery.

## Versioning

Start with `/api/v1`. Breaking changes require a deliberate API version decision rather than silently changing existing response semantics.
