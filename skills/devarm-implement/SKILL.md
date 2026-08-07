---
name: "devarm-implement"
description: "Use to execute a tasks.md produced by devarm-tasks. Runs tasks one at a time with strict TDD (red → green → refactor), verifies with real command output before claiming anything is done, and reports commit-ready checkpoints. Never run git commit unless the developer explicitly asks for that commit. Optionally dispatches a fresh subagent per task with review between tasks. Ends by offering devarm-review."
metadata:
  phase: 8
  produces: "working code with green tests + commit-ready checkpoint summaries"
  next: "devarm-review"
---

## Announce

"I'm using devarm-implement to execute the plan task-by-task with TDD and verification."

## Preconditions

1. `devarm-analyze` must report clean (no unresolved CRITICAL/HIGH, Pass 3 decisions recorded)
   before coding starts — or, on the brainstorm quick track, its scoped equivalent recorded in
   the quick-track doc (touched seams re-verified + mini Pass 3 decision batch). If neither has
   run since the last artifact/code change, run the appropriate one first.
2. **Feature branch before task 1.** Create or checkout `NNN-short-name` (or project convention)
   before the first implementation edit — do not accumulate the full feature uncommitted on
   `main` (spec 022: entire feature landed on `main`, branch/commit only at finish).
3. **Design anchor — run before task 1, and again whenever resuming in a new session.** Locate
   the governing design doc + Decision Ledger for this work and play back, in 3-5 bullets, the
   constraints that bind implementation (architecture, boundaries, key ledger decisions). The
   written design and ledger govern over session memory: what the current conversation drifted
   toward NEVER overrides what the approved doc says. If landed code or new instructions
   contradict the doc, that is the drift rule / course-correction protocol below — not a silent
   re-design from session context.
4. **Base-branch drift check before task 1 (and after any `git pull` / merge during the feature).**
   Re-verify plan anchors against the **current checkout**: file baselines (`wc -l`, grep anchor
   strings), cited `file:line` seams, and branch identity vs where planning happened. If the
   baseline moved, stop, record a PF-N note in tasks, and re-verify anchors by content — not
   stale line numbers. *Session evidence: planning on a branch 2 commits behind `main` changed
   SKILL.md from 382 to 351 lines; every edit anchor was still correct but the line budget was
   wrong.*
5. **Shared-surface collateral check (when editing a high-traffic module already on `main`).**
   Before the first edit to a god-file / shared route/repo/worker module (e.g. `routes.py`,
   `repositories/ticket_job.py`, `worker.py`), diff that path against `main` (or the merge-base)
   and list sibling behaviors already present on the file (soft-delete, list filters, aggregates,
   auth guards). After your edits, keep or restore at least one contract/unit test that would
   fail if those sibling behaviors were deleted — do not "win" your feature by silently removing
   another. *Session evidence (spec 030): concurrent soft-delete (#107) on the same files was
   stripped during multi-pod edits; DELETE returned 405 and list-filter asserts broke.*

## Execution loop (per task)

Follow `devarm-tdd` for steps 1–3 — it carries the full discipline (the delete rule for code
written before its test, RED must FAIL not error, test-quality rules, anti-patterns).

1. **Red** — write the failing test that defines the behavior. Run it; confirm it FAILS for the
   expected reason (a failure, not an error). A test that passes before implementation is not
   testing what you think. Code written before its test gets deleted, not "kept as reference".
2. **Green** — write the minimum code to make it pass. Run the test; confirm it PASSES and the
   rest of the suite stays green.
3. **Refactor** — improve while keeping tests green. No new behavior.
4. **Verify** — run the relevant test/lint/type commands and read the ACTUAL output. Do not
   claim "done", "fixed", or "passing" without command output confirming it. **Mirror CI, not
   the IDE:** run the SAME gate commands CI runs (discover them from the CI config — e.g.
   `mypy .`, `ruff check .`), because editor/IDE diagnostics (ReadLints) do NOT invoke the CI
   type-checker. Code that passes tests + IDE lints but fails `mypy .` still breaks the build.
   **Subprocess patch sweep:** when adding a new git/subprocess call to an existing flow
   (checkout, publish, diagnostic), grep tests that exercise that flow and confirm mocks patch
   the **import site the caller uses** (e.g. function-local `from repo_publish import _run_git`
   → patch `backend.services.git.repo_publish._run_git`, not the caller module attribute).
   *Session evidence (spec 027): diagnostic head-commit `rev-parse` broke CI because checkout
   cleanup tests did not mock the new subprocess call.*
   **OpenCode skill repo contract:** when adding or modifying
   `backend/opencode/skills/**/SKILL.md`, run the repo's skill-content test module (e.g.
   `pytest tests/unit/test_skill_content_requirements.py -q` from `backend/`) **or** the same
   full backend unit command CI uses (`pytest tests/unit -q`) — a feature-targeted subset alone
   is not sufficient. *Session evidence (spec 029): targeted 029 tests passed; CI failed on
   missing untrusted-input guard + reference-only classification for a new skill.*
   **Alembic graph:** when adding or editing `**/alembic/versions/**`, run `alembic heads` and
   require a **single** head whose `down_revision` is the previous tip — never reuse a revision
   id already on `main`. *Session evidence (spec 030): lease migration reused `0026` already
   taken by soft-delete → dual heads / broken migrate graph.*
5. **Checkpoint** — report the changed files, verification evidence, any trade-off ledger rows
   logged since the last checkpoint (batched for veto, per the batching rule below), and a
   suggested commit message. Never run `git commit` unless the developer explicitly asks for
   that commit. Do not treat task completion, phase completion, or end-to-end mode as commit
   permission.

## Commit and checkpoint discipline

- **Prepare commit-ready checkpoints at phase/task boundaries.** A checkpoint includes changed
  files, verification evidence, and a suggested commit message. It is advisory until the
  developer confirms. Long uncommitted runs make fixes harder to audit, so surface that risk,
  but never solve it by committing without permission.
- **Explicit commit confirmation required.** Acceptable confirmations are direct instructions
  such as "commit this", "commit after each task", or "create the checkpoint commit now". If the
  user only says "continue", "done", "looks good", or asks for end-to-end execution, do not
  commit; continue with uncommitted changes and keep reporting checkpoint summaries.
- **Checkpoint before entering a god-file or high-coupling zone.** Pause, confirm the seam and
  the line budget with the user, then proceed. Pure/foundational modules first; risky binding
  layers last, behind a checkpoint.

## Verification before completion (non-negotiable)

> NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE — run the proving command in THIS
> turn, read the full output, then claim. "Should work", confidence, and previous runs are not
> evidence. This covers paraphrases too: any wording implying success counts as a claim.

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | fresh test run: 0 failures | earlier run, "should pass" |
| Lint/types clean | fresh CI-gate output (e.g. `mypy .`, `ruff check .`): 0 errors | IDE/editor diagnostics; skipping the CI type-checker |
| Build succeeds | build exit 0 | lint passing |
| Bug fixed | original symptom re-tested | code changed, assumed fixed |
| Regression test works | red-green verified (fails without fix, passes with) | test passed once |
| Subagent completed | inspect the actual diff | subagent's "success" report |

If you cannot run the verification, say so explicitly rather than implying success.

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

**Batching rule (question fatigue is a drift vector).** Foreseeable trade-offs were already
batch-decided in `devarm-analyze` Pass 3 (or the quick-track mini batch). Mid-implementation,
do NOT interrupt with trade-off
questions one at a time: proceed with the recommended option, log the ledger row, and present
all accumulated trade-offs together at the next checkpoint for veto. Only design-level
decisions interrupt immediately. A foreseeable trade-off that still surfaces mid-task is a
Pass-3 miss — note it explicitly so `devarm-retro` can tighten the method.

**Unanswered question ≠ silent approval.** If you asked the user something and got no answer, do
NOT treat silence as a yes. Record an explicit ledger row marked `assumed — awaiting
confirmation` and surface it. (This is the exact failure mode that silently locked a cap-override
decision in a past session.)

**Drift rule:** if reality contradicts the plan or a Decision Ledger row, STOP — do not silently
diverge. Update the design/ledger with the new evidence (a design-level decision → ask), then
continue.

**Course correction (requirements changed underneath you):** when the user changes scope
mid-implementation or a new external constraint lands, do not absorb it ad hoc. Stop and run
a mini correct-course pass: (1) list which spec requirements, ledger rows, and remaining tasks
the change touches; (2) update those artifacts (new/superseded ledger rows, with the user for
design-level ones); (3) re-run `devarm-analyze` scoped to the affected areas; (4) resume.
Completed, unaffected work stays; affected completed work gets an explicit rework task.

## Two execution modes

- **Inline** — execute tasks in this session in small batches with checkpoints for review.
- **Subagent-driven (recommended for larger plans)** — dispatch a fresh subagent per task.
  Protocol:
  - **Provide the full task text + curated context in the prompt** — never "read the plan
    file"; the controller extracts what each task needs, including where it fits.
  - **Two-stage review per task, in order:** spec compliance first (does it do exactly what
    the task says — nothing missing, nothing extra), THEN code quality (standards, patterns,
    tests). Issues found → same subagent fixes → re-review. Never start quality review before
    spec compliance passes; never move on with open issues.
  - **Size the model to the task:** cheap/fast model for mechanical 1–2-file tasks with a
    complete spec; standard for multi-file integration; most capable for design/review.
  - **Handle subagent status:** NEEDS_CONTEXT → supply it and re-dispatch; BLOCKED → change
    something (context, model, task split) or escalate to the user — never retry unchanged;
    never dispatch two implementers in parallel on overlapping files.
  - **Verify independently** — check the actual diff; a subagent's "success" is not evidence.
- **Debugging during either mode:** any test failure or unexpected behavior → invoke
  `devarm-debug` (root cause first); do not patch symptoms inline. If multiple independent
  failures appear, `devarm-debug` covers parallel per-domain subagents.
- **Isolation (optional):** for work that must not disturb the main checkout, use a git
  worktree — create it under an ignored dir (`git check-ignore` it first), run setup, and
  confirm a green baseline before task 1; a dirty baseline makes new failures unattributable.

## Discipline

- Follow the plan's file structure — put logic where the plan/Decision Ledger says, not where
  it's momentarily convenient. If reality contradicts the plan, STOP, note the conflict, and
  update the design/ledger (the drift you're preventing) rather than silently diverging.
- Fix lints you introduce. Don't leave dead code or half-finished refactors.

## Hand off

When tasks are green and verified, **before offering `devarm-review`**, if the feature changed
multi-pod / multi-process / ownership topology (or the user asked for an implementation
diagram), show one mermaid of what was *actually implemented* (components + claim/lease/
schedule paths) so the operator mental model matches the code — not only the design doc.
*Session evidence (spec 030): user asked "show me implementations in diagram format so I can
understand what we implemented" after the coding pass.*

When tasks are green and verified, offer `devarm-review`; after findings are closed,
`devarm-finish` handles merge/PR/cleanup.
