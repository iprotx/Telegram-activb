---
name: ub-mode
description: >
  Follow disciplined software engineering principles when writing or changing
  code. Every change follows First Make it Work, then Then Make it Right,
  then Follow Practice. Use when the user runs /ub-mode or asks for the
  reduced principles.
---

# ub-mode

Every code change follows three phases:

1. **First Make it Work**
2. **Then Make it Right**
3. **Follow Practice**

## First Make it Work

### Laziness Protocol

- One decision lives in one place.
- Ship the smallest edit that solves the problem.

### Foundational Thinking

- Get the data shape right before writing logic.
- Do first whatever helps every later phase.
- If a concurrent writer would matter, do not share mutable state.

### TDD

- Write the failing test before changing code.
- See it fail for the expected reason.
- Make the smallest change that makes it pass.
- If an honest test is impractical, do not write a bad test.

### Redesign From First Principles

- Do not bolt a new requirement onto a broken design.
- Ask what you would have built if the requirement had existed from the start, then deliver it in verifiable pieces.

### Attack the Premise

- When repeated fixes sharing one premise fail the same gate, state that premise explicitly before attempting another fix.
- Remove the faulty assignment rather than stacking another workaround on it.

### Subtract Before You Add

- Remove complexity before adding abstractions, branches, or dependencies.

### Outcome-Oriented Execution

- Aim at an end state that can be checked.
- Intermediate breakage is acceptable only when planned and reversible.

### Build the Lever

- If work is not obvious at a glance, build a small tool or check that makes it repeatable.
- Do one unit by hand first, then automate that unit.

### Architecture

#### Model the Domain

- Structure the domain so illegal states are difficult or impossible to represent.
- Keep domain terminology explicit and consistent.
- If code is already clear and local, leave it alone.

#### Boundary Discipline

- Validate data where it enters.
- Inside the boundary, trust validated values.
- Keep business logic independent from transport and infrastructure.

#### Type System Discipline

- Make invalid values hard to construct.
- Parse external data once at the boundary.
- Never silence the type checker to hide a design problem.

#### Make Operations Idempotent

- Repeating an operation, or resuming after a crash, should converge on the same state whenever the domain permits it.

#### Separate Before Serializing Shared State

- If components do not need the same mutable state, give each its own.
- If shared state is required, enforce a single-writer boundary.

## Then Make it Right

### Fix Root Causes

- Reproduce the failure.
- Fix its cause.
- A guard that only hides the crash is not a fix.

### Sequence Work Into Verifiable Units

- Finish one small unit and check it.
- Then start the next unit.

### Test Behavior, Not Implementation

- Test the code through the boundary its user actually uses.
- Assert observable results, not private implementation details.
- If a test would pass even when the behavior returned nothing useful, throw it out.

### Crapper

- Use `crapper` when installed.
- Reduce each function below CRAP 10 by simplifying it, testing it, or both.
- Consider whether large case statements should be redesigned.

### Dryer

- Use `dryer` when installed.
- Eliminate structural duplication at or above the 0.8 similarity threshold.

### Mutator

- Use `mutator` when installed.
- Cover uncovered behavior.
- Kill surviving mutants.
- Delete dead code.

### Refactoring

- Pin observable behavior with tests.
- Change structure without changing behavior.
- Prove behavior is unchanged with the tests and quality gates.

## Practice

### Keep a Log

- Keep a concise log of actions and why they were taken.
- Report the relevant log at completion.

### Guard the Context Window

- Keep the main thread focused.
- Summarize completed work and preserve only information needed for the next step.

### Worktree Cleanup

- Remove only artifacts confirmed safe to delete.
- Never discard uncommitted user work without explicit approval.

### Commit and Push

- Commit often in small ordered commits.
- Each commit should explain why, what changed, and how it was proved.
- Push only when the requested workflow calls for it.

## Project integration

This repository also has project-specific rules in `AGENTS.md`. Those rules remain authoritative for the Python/aiogram stack and complement this skill. When both apply, satisfy both; if they conflict, follow the higher-priority project/user instruction.

If `crapper`, `dryer`, or `mutator` are unavailable, skip only that gate and report it. Never invent a result.
