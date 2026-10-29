# LittleFox Integration

_Last updated: 2026-10-29_

## Purpose

LittleFox is the external provider used by KEYDROP to source and deliver digital goods. It is a fulfillment dependency, not the customer database or storefront API.

Official API base URL:

`https://littlefox-api.ru/api/v1`

Official documentation:

`https://littlefox-api.ru/docs?lang=ru`

## Authentication

The LittleFox API key is stored only on the server as `LITTLEFOX_API_KEY`.

The React Mini App must never call LittleFox directly and must never receive this key.

## Catalog

KEYDROP reads products through LittleFox and maps them into the KEYDROP catalog model.

Relevant provider fields include product ID, name, `price_kopeks`, currency, stock, `stock_unlimited`, availability, category, descriptions and wholesale tiers.

The provider does not publish catalog change notifications, so KEYDROP must use an explicit refresh/cache strategy rather than assuming catalog data is immutable.

For money calculations, use the integer `*_kopeks` values. Do not calculate a purchase from display strings.

## Currency

For MVP, prefer RUB settlement.

When using LittleFox orders:

- send `currency=RUB`;
- do not send price/currency/exchange-rate fields as client-authoritative purchase data;
- use `max_total_kopeks` as a server-side spend guard;
- if USD is ever used, treat exchange-rate availability as a provider dependency and preserve the same operation key when retrying the same operation.

## Purchase flow

`POST /orders?currency=RUB` accepts one product and quantity 1–100.

Required provider controls:

- `Idempotency-Key`, 8–128 allowed characters;
- `product_id`;
- `quantity`;
- `max_total_kopeks`;
- optional `client_order_id`.

KEYDROP must persist the operation key and its parameters before sending the provider request.

Provider responses may be:

- `201` — delivered;
- `200` — repeated/idempotent result;
- `202` — processing.

Only a confirmed `delivered` state releases delivery data to the customer.

## Idempotency and recovery

One provider order gets one idempotency key.

If the network response is unknown, the backend retries/reconciles using the **same key and same operation parameters**. A new key must not be created merely because the first HTTP response was lost.

Changing parameters with the same key is a conflict and must not be used as a retry strategy.

Known provider orders can be polled through `GET /orders/{id}`. Do not poll more frequently than the provider's documented minimum interval.

## Provider statuses

Provider order statuses include `processing`, `recovering`, `delivered`, `failed` and `refunded`.

KEYDROP maps these to its own order state model rather than exposing provider terminology directly to the UI.

## Delivery data

`delivery_data` is returned by the provider unchanged and may contain multiline text or JSON strings.

Rules:

- store the complete value when needed for fulfillment/recovery;
- do not truncate line breaks;
- do not log it;
- expose it only to the authenticated order owner after confirmed delivery;
- treat it as sensitive digital-goods data.

## Errors and retries

Important provider classes include authentication errors, insufficient balance, not found, conflicts, rate limits, unavailable API/exchange service and temporary purchase failures.

Retry with backoff for documented transient cases such as `202`, `429` and appropriate `5xx` responses. Do not blindly retry non-retryable validation, authorization or idempotency-conflict errors.

## Test purchase

LittleFox provides a test purchase mode with `is_test=true`. The documented test product behavior uses unlimited stock and a nominal price of 100 kopeks (1 RUB) with fake delivery data.

MVP verification should use the provider's test mechanism before any real-money test is considered.

## Internal order model

KEYDROP should retain at minimum:

- internal order ID;
- Telegram customer ID;
- product ID;
- quantity;
- currency;
- amount in kopeks;
- internal status;
- LittleFox order ID;
- idempotency key;
- created/updated timestamps;
- delivery data where required for fulfillment.

The internal record is the source of truth for the Mini App.

## Provider change policy

Do not mirror the complete LittleFox API into the frontend. When the provider changes, update this integration adapter and its tests first. Keep the public KEYDROP API stable where possible.
