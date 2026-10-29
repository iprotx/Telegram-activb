# Non-AI Telegram Group Bot Feature Research Plan

> **For agentic workers:** This is a research and product-planning plan, not authorization to implement every candidate feature. Execute it in bounded stages; use the repository's TDD and review workflow for any later code change.

**Goal:** Produce an evidence-backed, prioritized roadmap for adding useful activity, moderation, and admin utilities to this Telegram group bot, using deterministic rules only and no AI functionality.

**Architecture:** Build on the existing aiogram/SQLAlchemy foundation and preserve `handlers → services → repositories → database infrastructure`. Keep Telegram permissions and update parsing at the boundary, policy in services, and persistence in repositories. Select features only after comparing user value, technical fit, privacy, and operational risk.

**Tech Stack:** Existing Python 3.12+, aiogram 3.31, SQLAlchemy 2.x async, Alembic, pydantic-settings, pytest, Ruff, mypy, Docker Compose, and GitHub Actions. Do not add AI/model dependencies.

**Spec:** `AGENTS.md`, `docs/PROJECT_STATUS.md`, `docs/DECISIONS.md`, `docs/WORKLOG.md`, `docs/superpowers/plans/2026-10-29-production-hardening.md`, and the official references linked below.

## Scope and global constraints

- **No AI:** no LLM/model calls, embeddings, AI classifiers, prompt-based decisions, or external AI services. The bot's shipped behavior must be rule-based and deterministic.
- Do not add new functionality while carrying out this research plan. This document records research steps and candidate ideas; candidates are not product commitments.
- Do not delay the existing reliability backlog: #13 safe error logging, #14 startup/import safety, #16 Docker runtime smoke, then the final architecture/release-readiness review remain ahead of a production feature expansion unless the user explicitly changes priorities.
- Preserve `handlers → services → repositories → database infrastructure`.
- Keep moderation settings chat-scoped; validate commands and IDs at the Telegram boundary; check admin role and required rights before taking an action.
- Make actions with external effects explicit, auditable, and reversible where possible. Avoid broad automatic bans/deletions in the first iteration.
- Store only data needed for a declared feature. Never log tokens or full sensitive update payloads.
- Treat official bot documentation as the source of truth for Telegram update visibility and permission requirements; competitor behavior is evidence of product patterns, not an instruction to copy their implementation.

## Current baseline

The maintained project status describes a production-oriented bot foundation with user registration, activity/XP tracking, SQLAlchemy persistence, Alembic migrations, Docker Compose, and CI quality gates. `/start` registration and the core activity service are present. The current release-readiness gaps are #13, #14, #16, whole-branch architecture review, and final operational verification.

During the inventory step, verify which user-facing activity commands and admin features exist in the current code before marking any candidate as missing. Do not infer a feature from a database model or service alone.

## Initial comparison set (official documentation only)

| Bot/reference | Non-AI capabilities to inspect | Why it is relevant | Source |
| --- | --- | --- | --- |
| Combot | Group analytics, top users, XP/ranks, leaderboards, captcha, moderation, configurable automations | Closest comparison for activity/engagement and admin visibility. Ignore Combot's separately marketed AI feature entirely. | https://combot.org/ |
| MissRose / Rose | Welcome messages, captcha, warnings, mute/ban/kick, anti-flood, content locks, filters and allowlists | Useful reference for transparent, rules-based moderation and permission-aware commands. | https://missrose.org/docs/getting-started/ |
| Group Help | Join protection/captcha, spam and repeated-message controls, banned words, night mode | Useful reference for onboarding and baseline anti-spam controls. | https://grouphelp.me/en |
| Telegram Bot Platform | Privacy mode, update delivery, bot administrator rights and method requirements | Defines feasibility and safety constraints for any group-wide feature. | https://core.telegram.org/bots/faq and https://core.telegram.org/bots/api |

This set is deliberately small. Add another comparable bot only when it contributes a distinct feature category or has better first-party documentation.

## Research workflow

### Stage 1 — Inventory this repository

- [ ] Review `README.md`, `AGENTS.md`, `docs/PROJECT_STATUS.md`, `docs/DECISIONS.md`, and the production-hardening plan.
- [ ] Map current commands, handlers/routers, services, repositories, models, migrations, and tests by capability: onboarding, activity/XP, admin utilities, moderation, configuration, operations.
- [ ] Mark every capability as **implemented and tested**, **partially present**, **not present**, or **unknown**. Link each claim to a file/test/issue.
- [ ] Record Telegram update types and permissions needed for each current/future capability.

**Deliverable:** a concise current-capability inventory that does not confuse infrastructure with user-facing functionality.

### Stage 2 — Compare similar bots

For Combot, Rose, and Group Help, record only documented non-AI functionality. For each relevant feature capture:

- user/admin problem solved;
- trigger and interaction style (command, event, time window, configuration);
- behavior on normal and edge cases;
- required Telegram permissions and message visibility;
- state required, retention concerns, and audit expectations;
- failure modes, false-positive risk, and escape hatch/undo operation;
- evidence URL and the date checked.

Do not copy proprietary internals or assume that a marketing page documents every edge case. If behavior is unclear, mark it **unverified**.

**Deliverable:** a comparison matrix with source links and explicit unknowns.

### Stage 3 — Evaluate candidate features

Start with these hypotheses; keep, reorder, or reject them based on the inventory and comparison matrix.

| Candidate | Deterministic implementation idea | Main dependency/risk | Initial view |
| --- | --- | --- | --- |
| `/rank` and `/top` | Query existing XP/level data; stable ordering and pagination/limit; exclude inappropriate account types if applicable | Confirm current commands and efficient per-chat queries | Strong first product candidate if not already implemented |
| Welcome message and `/rules` | Admin-configured text templates with a small, allowlisted set of substitutions | Service-message handling, template escaping and chat settings | Good low-complexity candidate |
| Warnings and timed restrictions | Persist warning count/reason/actor; configured threshold maps to a fixed action; check admin rights before acting | Schema/migrations, race safety, rights, audit history and undo | Valuable, but medium/high risk |
| Anti-flood | Count messages per user/chat in a bounded time window and apply an explicit configured response | Must receive ordinary group messages; false positives; window and cleanup policy | Rules-based, but requires a clear privacy-mode setup guide |
| Link/keyword filters | Normalize text, match configured patterns, support allowlists and admin exemptions | False positives, Unicode/case handling, delete-message rights | Later moderation slice after audit/config patterns exist |
| Admin utilities (`/help`, `/id`, chat status) | Deterministic responses from the current update and stored settings | Keep sensitive identifiers scoped and avoid unnecessary storage | Small, easy-to-review additions |
| Scheduled notices | Persist schedule and send at defined times | A reliable scheduler/worker, timezone semantics, retries and idempotency | Defer until runtime behavior is verified |

No candidate is approved by this table. First confirm the current command surface and estimate the change based on the real code.

### Stage 4 — Rank features and define an MVP

Score each candidate from 1–5 for:
1. member/admin value;
2. fit with current architecture and stored data;
3. implementation effort (lower effort scores higher);
4. operational/security risk (lower risk scores higher);
5. testability and reversibility.

Write down the evidence and trade-offs, rather than treating the numerical total as a decision by itself. Choose no more than three first-wave features, with one capability per implementation iteration. Prefer a value that reuses existing data and needs no new background worker or destructive moderation action.

**Deliverable:** a prioritized shortlist with dependencies, explicit exclusions, acceptance criteria, and verification commands.

### Stage 5 — Turn approved choices into engineering tasks

- [ ] After the research matrix and shortlist have been reviewed, create one GitHub issue per independently testable feature.
- [ ] Each issue must name the user/admin problem, command/event contract, permission needs, data changes, privacy/logging behavior, failure cases, acceptance criteria, and tests.
- [ ] For each approved implementation, add behavior tests first, observe the expected failure, then implement the smallest change.
- [ ] Apply Alembic migrations only if the data model actually needs to change; run both `alembic upgrade head` and `alembic check`.
- [ ] Run `ruff format --check .`, `ruff check .`, `mypy src`, and `pytest -q`; update project status and work log with actual evidence.
- [ ] Do not merge or deploy without explicit user approval.

## Telegram feasibility and safety gate

Before proposing any feature that processes every group message, confirm how the bot will receive updates. Telegram documents that privacy-enabled bots normally receive only relevant commands/replies and service messages; group-wide activity tracking or anti-flood may require the bot to be an administrator or have privacy mode disabled. Verify the least-privilege set of admin rights needed for each moderation action. Document setup requirements clearly instead of silently assuming full message access.

## Definition of done for this research

- [ ] The current capability inventory is linked to repository evidence.
- [ ] The comparison matrix includes at least Combot, Rose, Group Help, and Telegram's official platform documentation.
- [ ] Every competitor-derived claim has a first-party source link; unknowns are labeled rather than guessed.
- [ ] The shortlist contains no AI/LLM/model-backed features or external AI dependencies.
- [ ] Each recommended feature has an explicit value, architecture fit, risk, dependency, and test strategy.
- [ ] The next engineering step respects the existing #13 → #14 → #16 hardening sequence.
- [ ] Research does not mark implementation tasks complete and does not itself change runtime behavior.

## References (checked 2026-10-29)

- Combot feature overview: https://combot.org/
- Rose overview: https://missrose.org/docs/getting-started/
- Rose filters: https://missrose.org/docs/filters/
- Rose bans/mutes/kicks: https://missrose.org/docs/moderation/restrictions/
- Rose content locks: https://missrose.org/docs/anti-spam/locks/
- Rose anti-flood: https://missrose.org/docs/anti-spam/antiflood/
- Rose captcha: https://missrose.org/docs/anti-spam/captchas/
- Rose warnings: https://missrose.org/docs/moderation/warnings/
- Group Help feature overview: https://grouphelp.me/en
- Telegram Bots FAQ (message visibility): https://core.telegram.org/bots/faq
- Telegram Bot API (method/admin rights): https://core.telegram.org/bots/api
