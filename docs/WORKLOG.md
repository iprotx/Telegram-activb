# Work Log

## 2026-10-29 — KEYDROP storefront and MVP foundation

- **Goal:** align the project documentation with the agreed KEYDROP product direction and define the path from the existing bot foundation to a testable Telegram Mini App MVP.
- **Decision:** use one repository with `frontend/` for React + TypeScript + Vite; keep Python/aiogram as the backend/bot; use PostgreSQL as the source of truth; use LittleFox only as fulfillment.
- **Changed:** added `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/INTEGRATIONS.md`, `docs/integrations/littlefox.md` and `docs/MVP_PLAN.md`; reconciled `README.md`, `docs/PROJECT_STATUS.md` and `docs/DECISIONS.md`.
- **Product scope:** MVP prioritizes catalog, product detail, favorites, cart, server-confirmed/idempotent purchase, fulfillment, orders, notifications and referral attribution. Loyalty/gamification remains post-MVP.
- **Acceptance:** `docs/MVP_PLAN.md` defines the explicit **MVP READY — можно тестировать** gate and requires a deployed Telegram test environment plus evidence for the critical purchase flow.
- **Verification:** documentation changes were written to the `docs/keydrop-mvp-foundation` branch. No application code was changed in this stage; runtime checks are therefore not yet applicable.
- **Next:** implement Stage 1 — React + TypeScript + Vite Mini App foundation.

## Historical project work

Earlier bot reliability and feature work remains represented by the existing git history and merged commits. The current product status in `docs/PROJECT_STATUS.md` is the source of truth for the new KEYDROP roadmap.

Append a short entry after every meaningful task or PR. Newest entries go first. Record facts and links, not assumptions.
