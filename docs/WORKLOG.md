# Work Log

## 2026-10-29 — Stage 3: catalog persistence and storefront data flow

- **Goal:** move the Mini App from an empty shell to server-controlled catalog data while keeping LittleFox behind the Python boundary.
- **Changed:** added the `products` model and migration, product repository, LittleFox catalog client, authenticated `/api/v1/products` and `/api/v1/products/{id}` endpoints, typed frontend catalog client and product-card states.
- **Provider boundary:** LittleFox credentials remain server-side. The frontend receives KEYDROP product data only; it never calls LittleFox directly.
- **Data rule:** provider price/availability are stored in KEYDROP and refreshed from the provider when the catalog endpoint is used. The backend remains authoritative for what the frontend can display.
- **Tests:** added backend catalog endpoint coverage and frontend catalog client coverage.
- **Verification status:** implementation is committed to the PR branch; GitHub CI verification is still required. Local dependency execution is unavailable in the current environment.
- **Next:** complete catalog/product UX, then move to favorites and cart foundations before checkout.

## 2026-10-29 — Stage 2: Python HTTP API + Telegram authentication foundation

- **Goal:** establish the trusted server-side identity boundary between the KEYDROP Mini App and the existing Python/PostgreSQL backend.
- **Changed:** added FastAPI/Uvicorn dependencies, API settings, Telegram `initData` HMAC validation, authenticated `GET /api/v1/me`, health endpoint and API entrypoint.
- **Persistence:** authenticated Telegram users are resolved through the existing `UserRepository`, preserving the current user table and repository layer.
- **Tests:** added TDD coverage for valid signatures, invalid signatures, expired data, invalid user payloads and authenticated customer bootstrap.
- **Security:** the API accepts raw Telegram init data through `Authorization: tma <initData>`, validates it server-side, and only then resolves/updates the customer. LittleFox and database access remain server-side.
- **Verification status:** implementation is committed to the PR branch; GitHub CI verification is still required before declaring the stage complete.
- **Next:** finish CI verification, then implement catalog/product endpoints and storefront data flow.

## 2026-10-29 — Stage 1: React + TypeScript + Vite Mini App foundation

- **Goal:** establish the first runnable KEYDROP Mini App foundation without coupling the frontend to PostgreSQL or LittleFox.
- **Changed:** added the `frontend/` Vite + React + TypeScript application shell, Telegram SDK initialization with browser mocking, Telegram theme/viewport CSS variable binding, responsive AppShell/navigation, and a typed API boundary helper.
- **Tests:** added the first frontend unit contract for forwarding raw Telegram init data to the future KEYDROP API.
- **CI:** added frontend typecheck, unit-test and production-build checks to GitHub Actions.
- **Security boundary:** the frontend does not contain LittleFox credentials and does not access PostgreSQL directly. Raw Telegram init data is treated as an authentication input for the backend, not as trusted client identity.
- **Verification status:** implementation is present in this PR, but CI has not yet been observed passing for the new frontend job; no local npm execution was possible in the current environment.
- **Next:** after CI verification, proceed to Stage 2 — Python HTTP API and server-side Telegram init-data validation.

## 2026-10-29 — KEYDROP storefront and MVP foundation

- **Goal:** align the project documentation with the agreed KEYDROP product direction and define the path from the existing bot foundation to a testable Telegram Mini App MVP.
- **Decision:** use one repository with `frontend/` for React + TypeScript + Vite; keep Python/aiogram as the backend/bot; use PostgreSQL as the source of truth; use LittleFox only as fulfillment.
- **Changed:** added `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/INTEGRATIONS.md`, `docs/integrations/littlefox.md` and `docs/MVP_PLAN.md`; reconciled `README.md`, `docs/PROJECT_STATUS.md` and `docs/DECISIONS.md`.
- **Product scope:** MVP prioritizes catalog, product detail, favorites, cart, server-confirmed/idempotent purchase, fulfillment, orders, notifications and referral attribution. Loyalty/gamification remains post-MVP.
- **Acceptance:** `docs/MVP_PLAN.md` defines the explicit **MVP READY — можно тестировать** gate and requires a deployed Telegram test environment plus evidence for the critical purchase flow.
- **Verification:** documentation changes were written to the `docs/keydrop-mvp-foundation` branch. No application code was changed in this stage; runtime checks were therefore not applicable.
- **Next:** implement and verify Stage 1 — React + TypeScript + Vite Mini App foundation.

## Historical project work

Earlier bot reliability and feature work remains represented by the existing git history and merged commits. The current product status in `docs/PROJECT_STATUS.md` is the source of truth for the new KEYDROP roadmap.

Append a short entry after every meaningful task or PR. Newest entries go first. Record facts and links, not assumptions.
