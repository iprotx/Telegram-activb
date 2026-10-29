# Project skills

Project-local agent skills are kept under this directory so the rules used by coding agents are versioned with the project.

## Skills

- `ub-mode/` — disciplined TDD, root-cause debugging, refactoring, and quality-gate workflow.
- `python-aiogram-coder/` — project-specific Python/aiogram 3.31 architecture and testing rules.

## Usage

Invoke `ub-mode` explicitly with `/ub-mode` when requested. For code changes in this repository, combine it with the project rules in `AGENTS.md` and the stack-specific `python-aiogram-coder` skill.

Quality tools mentioned by `ub-mode` are optional. If `crapper`, `dryer`, or `mutator` are not installed, skip only those checks and report the omission rather than fabricating results.
