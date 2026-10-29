# Integrations

_Last updated: 2026-10-29_

## Telegram

Telegram is the identity, launch and communication platform.

KEYDROP uses:

- Telegram Bot API through aiogram for bot interactions and notifications;
- Telegram Mini Apps for the customer storefront;
- Mini App `initData` for server-side authentication;
- `startapp` parameters for referral attribution.

Telegram-specific code stays at the transport edge. Product rules belong to services/domain code.

Official documentation: https://core.telegram.org/bots/webapps

## LittleFox

LittleFox supplies digital goods and fulfillment. KEYDROP owns the customer relationship and internal order model.

The integration is documented separately in `docs/integrations/littlefox.md`.

## Integration security

- secrets are server-side only;
- provider credentials are never embedded in the React bundle;
- outbound provider errors are translated into KEYDROP error states;
- sensitive delivery data is not written to normal logs;
- external calls must have explicit timeout/retry/reconciliation behavior.

## Future integrations

CRM/campaign tooling, analytics, payment providers and additional fulfillment providers are intentionally not required for MVP. Add an integration only after its business boundary and operational need are documented.
