---
name: "devarm-implement"
description: "Use to execute a tasks.md produced by devarm-tasks. Runs tasks one at a time with strict TDD (red → green → refactor), verifies with real command output before claiming anything is done, and commits frequently. Optionally dispatches a fresh subagent per task with review between tasks. Ends by offering devarm-review."
metadata:
  phase: 7
  produces: "working code with green tests, committed incrementally"
  next: "devarm-review"
---

## Announce

"I'm using devarm-implement to execute the plan task-by-task with TDD and verification."

## Precondition

`devarm-analyze` must report clean (no unresolved CRITICAL/HIGH) before coding starts. If it
hasn't run since the last artifact/code change, run it first.

## Execution loop (per task)

1. **Red** — write the failing test that defines the behavior. Run it; confirm it FAILS for the
   expected reason. A test that passes before implementation is not testing what you think.
2. **Green** — write the minimum code to make it pass. Run the test; confirm it PASSES.
3. **Refactor** — improve while keeping tests green.
4. **Verify** — run the relevant test/lint/type commands and read the ACTUAL output. Do not
   claim "done", "fixed", or "passing" without command output confirming it.
5. **Commit** — small, focused commit. Only commit when the user has asked you to commit, per
   the repo's git rules; otherwise stage and report.

## Commit and checkpoint discipline

- **Commit at phase/task boundaries on the feature branch** (once the user has authorized
  committing). Long uncommitted runs make fixes untrackable, cause duplicate "fix the issues"
  loops, and leave no bisectable history — a real cost in a past session where ~6 hours stayed
  uncommitted through 10+ fix rounds. A "don't commit to main" preference is not a reason to
  leave the feature branch uncommitted. If the user forbids all commits, say explicitly what
  risk that carries and keep a running staged-state summary instead.
- **Checkpoint before entering a god-file or high-coupling zone.** Pause, confirm the seam and
  the line budget with the user, then proceed. Pure/foundational modules first; risky binding
  layers last, behind a checkpoint.

## Verification before completion (non-negotiable)

Before saying a task or the feature is complete, you MUST have run the verification and seen it
pass. Evidence before assertions, always. If you cannot run it, say so explicitly rather than
implying success.

## Decision ownership at implementation time (the taxonomy)

Implementation always surfaces decisions the plan didn't fully settle. The user owns the
consequential ones. When a decision point arises, classify it and act accordingly:

- **Design-level** — drops/replaces a designed component, changes semantics, or alters
  user-visible behavior (e.g. "wrap service X" turns out illegal, so drop it; change
  partial-failure semantics). → **STOP and ask the user.** Do not proceed on assumption. Record
  the answer as a Decision Ledger row.
- **Implementation trade-off** — real choice with no dominant option but no change to intent
  (module placement, error-handling strategy, a back-compat shim). → **Proceed with the
  recommended option, but log it as a ledger row AND flag it in the turn summary** so the user
  can veto.
- **Mechanical** — naming, test layout, formatting, obvious-correct choices. → **Just do it.**

**Unanswered question ≠ silent approval.** If you asked the user something and got no answer, do
NOT treat silence as a yes. Record an explicit ledger row marked `assumed — awaiting
confirmation` and surface it. (This is the exact failure mode that silently locked a cap-override
decision in a past session.)

**Drift rule:** if reality contradicts the plan or a Decision Ledger row, STOP — do not silently
diverge. Update the design/ledger with the new evidence (a design-level decision → ask), then
continue.

## Two execution modes

- **Inline** — execute tasks in this session in small batches with checkpoints for review.
- **Subagent-driven (recommended for larger plans)** — dispatch a fresh subagent per task, then
  review its work in two stages (does it meet the task? does it meet the code standards?) before
  moving on. Keeps each unit of work in a clean context.

## Discipline

- Follow the plan's file structure — put logic where the plan/Decision Ledger says, not where
  it's momentarily convenient. If reality contradicts the plan, STOP, note the conflict, and
  update the design/ledger (the drift you're preventing) rather than silently diverging.
- Fix lints you introduce. Don't leave dead code or half-finished refactors.

## Hand off

When tasks are green and verified, offer `devarm-review` before merge.
