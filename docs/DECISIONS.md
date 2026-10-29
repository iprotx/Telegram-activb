# Decision Log

## 2026-10-29 — Keep transaction ownership at the update boundary for now

**Context:** Issue #32 asked whether `ServicesMiddleware` should stop wrapping the full handler in `session.begin()`. Current middleware injects `UserService` and `ActivityService`, then executes the handler inside one transaction.

**Evidence reviewed:**
- The current registered handlers are `start_handler` and `activity_message_handler`.
- `activity_message_handler` performs registration and activity recording, both database operations, inside the same transaction; it has no Telegram API call.
- `start_handler` registers/synchronizes the user and then calls `message.answer()`, so a Telegram API request occurs before the middleware transaction commits.
- Unit tests verify commit on success and rollback/re-raise on handler failure. The PostgreSQL integration test verifies that a user inserted by a handler is rolled back if the handler raises.
- The user repository and activity repository use nested transactions/savepoints to recover from uniqueness races; these do not replace the outer transaction that makes the full update atomic.

**Decision:** Do not change production transaction boundaries in this investigation. The only identified external call inside the transaction is the `/start` reply. No evidence currently shows that this short-lived path causes a material operational problem. Moving commits into individual services would weaken the existing update-level rollback guarantee: for example, registration could commit even if activity recording later failed. A safer split would require an explicit use-case/transaction API and regression tests, which is not justified by the current evidence.

**Consequences:**
- Preserve atomic registration + activity recording for each group-message update.
- Keep the existing rollback behavior and current middleware implementation.
- Revisit only if production measurements show materially long transactions or lock contention, or if a concrete use case requires external I/O between DB operations.
- If revisited, prefer moving the `/start` Telegram response after a clearly defined commit boundary without splitting registration/activity atomicity.

## 2026-10-29 — Keep chat features deterministic and non-AI

**Context:** The product direction is to study existing Telegram group bots for activity, moderation, and admin utilities without adding AI behavior to this bot.

**Decision:** Product features must use explicit rules, thresholds, configured templates, and auditable commands. Do not add LLM/model calls, embeddings, AI classifiers, prompt-based decisions, or third-party AI services.

**Consequences:** Candidate features must be explainable and testable with deterministic unit/integration tests. The research plan may cite products that also offer AI, but only their documented non-AI capabilities are in scope.

Record durable decisions that affect architecture, delivery, or operational behavior. Add new entries at the top with date, context, decision, and consequences.

## 2026-10-29 — Keep project status separate from detailed implementation plan

**Context:** The repository has a detailed production-hardening plan, but its unchecked task boxes do not provide a trustworthy snapshot of what has actually shipped.

**Decision:** Maintain `docs/PROJECT_STATUS.md` as the concise current snapshot and prioritized backlog, while keeping detailed implementation plans as execution checklists. Reconcile plans against source/tests/CI before changing task states.

**Consequences:** The overview remains readable between sessions; detailed work stays traceable. A checkbox is not evidence by itself—completed work should point to a commit, test, or CI run.

## 2026-10-29 — Keep merge and release decisions explicit

**Context:** Code can pass CI without being approved for merge or deployment.

**Decision:** Do not merge PRs, deploy, or perform destructive actions unless the user explicitly asks. Report CI readiness separately from approval.

**Consequences:** “CI green” means the configured checks passed, not that production readiness or product acceptance has been established.
