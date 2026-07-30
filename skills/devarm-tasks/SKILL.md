---
name: "devarm-tasks"
description: "Use after devarm-plan to generate an actionable, dependency-ordered tasks.md. Groups work so each unit has a failing test task before its implementation task (TDD-first), marks parallelizable tasks, and includes exact file paths. Reuses spec-kit tasks template if .specify/ exists. By default, halt after the tasks gate and ask whether to run devarm-analyze; continue automatically only when the user explicitly requested end-to-end execution."
metadata:
  phase: 5
  produces: "tasks.md (tests-first, dependency-ordered, [P] parallel markers)"
  next: "halt and ask about devarm-analyze unless end-to-end was explicitly requested; implementation still requires clean analyze"
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
  When a decision is a **safety invariant** ("never X", "always Y"), the acceptance test must
  assert the FORBIDDEN state cannot occur, not just the happy path — a positive-only test lets
  the negative case ship. In a past session "never mark success while no PR is published" had a
  task, but it only checked the publish-happy path, so the first build shipped a false "partial
  success" with no PR; the missing test was the negative guard "no real PR ⇒ not success".
  When the deliverable is a **state machine** (a plan State-Transition Table), every cell required
  to be non-schedulable / preserving gets an acceptance test asserting its **terminal state and
  side-effects** — and the forbidden outcomes as negatives (does NOT loop / does NOT downgrade /
  does NOT close-or-reset an active entity). A per-transition test is the guard; a happy-path-only
  suite lets a wrong terminal state ship. *Why (this session): "repair preserves an active
  investigation" was broken by the unsupported-close path (L1) and a two-mention downgrade (F6)
  because no test pinned those transitions' terminal states.*
  When a decision's deliverable is prompt/skill/contract **wording** (an enum value, a
  threshold, an instruction string), the acceptance test is a **wording-lock test** that asserts
  the exact string/value in the artifact. Without it the wording silently drifts — and in a past
  session a compaction summary even *claimed* lock tests that were never written, so the lock
  test both prevents drift and makes "done" verifiable against the repo, not a summary.
  When a deliverable includes **operator-visible escalation or notification copy**, the
  acceptance test must assert strings appear in the rendered message (e.g.
  `build_diagnosis_escalation_user_message` output), not only that a dict exists on
  `final_output` — spec 022 SC-005 shipped dict-level coverage while Jira copy stayed thin until
  a follow-up fix.
  When a new skill/prompt rule can change a **ship-gate boolean** (an existing Python predicate
  on phase output — waiver, override, `blocks_pr`, retry routing), add a **routing
  characterization test** that executes the predicate on a constructed payload and asserts the
  measured before/after, not only a wording-lock on the instruction text. *Session evidence:
  changing finding severity from `warning` to `error` flipped
  `review_allows_test_file_deferred_review` with no test until findgap — wording locks were
  green throughout.*
  When a locked decision implements **git checkout/publish on an existing remote branch**
  (append reuse, rebase onto base, force-with-lease), the acceptance test MUST include a
  **real-git mirror + worktree fixture** exercising fetch → checkout → at least one
  post-checkout fetch — mock-only `_run_git` tests are necessary but not sufficient for merge.
  *Session evidence (spec 027): D7 git reuse mode; mocked suite passed; live E2E found P0 mirror
  layout bugs.*

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
- Every **safety invariant** ("never/always") has a negative test asserting the forbidden state cannot occur, not only a happy-path test.
- Every implementation task has a preceding failing-test task.
- Every integration seam has either a full contract or a spike task before its dependent impl task.
- `[P]` markers are only on genuinely independent tasks.

## Hand off

Report the tasks path, self-check result, and recommended next phase (`devarm-analyze`). By
default, STOP and ask the user whether to run `devarm-analyze`. Invoke `devarm-analyze` only if
the user explicitly requested end-to-end execution for this work or has just told you to
continue. Never invoke `devarm-implement` directly from tasks; implementation still requires a
clean `devarm-analyze` gate.
