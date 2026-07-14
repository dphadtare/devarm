---
name: "devarm-tasks"
description: "Use after devarm-plan to generate an actionable, dependency-ordered tasks.md. Groups work so each unit has a failing test task before its implementation task (TDD-first), marks parallelizable tasks, and includes exact file paths. Reuses spec-kit tasks template if .specify/ exists. Hands off to devarm-implement."
metadata:
  phase: 5
  produces: "tasks.md (tests-first, dependency-ordered, [P] parallel markers)"
  next: "devarm-analyze (mandatory gate), then devarm-implement"
---

## Announce

"I'm using devarm-tasks to generate the dependency-ordered, tests-first task list."

## Rules

- **Tests first (TDD).** Each behavior gets a failing-test task BEFORE its implementation task.
  Verify the test fails before implementing.
- **Dependency order.** Foundational / shared building blocks come first and block the stories
  that use them. Never order an impl task before the module it depends on.
- **Organize by user story / behavior**, so each group is independently testable and shippable.
  Call out the MVP slice explicitly.
- **Exact file paths** in every task. Use `[P]` to mark tasks that can run in parallel (different
  files, no dependency on an incomplete task); sequence tasks that touch the same file.
- **Decision → test traceability (required).** Every *locked decision* in the Decision Ledger
  gets a named acceptance test task, written BEFORE the code that could violate it. A decision
  that lives only in prose gets silently broken — in a past session "intake runs exactly once"
  and "exactly one comment per run" were both locked decisions violated by the first
  implementation, because neither had a failing test guarding it. Each task cites the spec
  requirement and the ledger row (Dn) it serves.

## Format

`[ID] [P?] [Story] Description — exact/path/to/file`

## Structure

1. **Setup** — environment / dependency confirmation (no business logic).
2. **Foundational** — shared modules every story needs (blocks all stories).
3. **Per user story** — failing tests first, then implementation, then the observable end-to-end
   behavior. Mark the MVP story.
4. **Polish / cross-cutting** — guardrail checks (boundaries, god-file budgets, anti-duplication),
   lint/type gates, performance verification, docs.

## Self-check before handoff

- Every spec requirement and every Decision Ledger row has at least one task.
- Every **locked decision** has a named acceptance-test task preceding any code that could break it.
- Every implementation task has a preceding failing-test task.
- Every integration seam has either a full contract or a spike task before its dependent impl task.
- `[P]` markers are only on genuinely independent tasks.

## Hand off

Report the tasks path, then invoke `devarm-analyze` (the mandatory gate before implementation) —
not `devarm-implement` directly.
