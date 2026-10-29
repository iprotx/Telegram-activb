# Decision Log

## 2026-10-29 — Keep chat features deterministic and non-AI

**Context:** The product direction is to study existing Telegram group bots for activity, moderation, and admin utilities without adding AI behavior to this bot.

**Decision:** Product features must use explicit rules, thresholds, configured templates, and auditable commands. Do not add LLM/model calls, embeddings, AI classifiers, prompt-based decisions, or third-party AI services.

**Consequences:** Candidate features must be explainable and testable with deterministic unit/integration tests. The research plan may cite products that also offer AI, but only their documented non-AI capabilities are in scope.

Record durable decisions that affect architecture, delivery, or operational behavior. Add new entries at the top with date, context, decision, and consequences.

## 2026-10-29 — Keep project status separate from detailed implementation plan

**Context:** The repository has a detailed production-hardening plan, but its unchecked task boxes do not provide a trustworthy snapshot of what has actually shipped.

**Decision:** Maintain `docs/PROJECT_STATUS.md` as the concise current snapshot and prioritized backlog, while keeping `docs/superpowers/plans/2026-10-29-production-hardening.md` as the detailed execution checklist. Reconcile the detailed plan against source/tests/CI before changing task states.

**Consequences:** The overview remains readable between sessions; detailed work stays traceable. A checkbox is not evidence by itself—completed work should point to a commit, test, or CI run.

## 2026-10-29 — Keep merge and release decisions explicit

**Context:** Code can pass CI without being approved for merge or deployment.

**Decision:** Do not merge PRs, deploy, or perform destructive actions unless the user explicitly asks. Report CI readiness separately from approval.

**Consequences:** “CI green” means the configured checks passed, not that production readiness or product acceptance has been established.
