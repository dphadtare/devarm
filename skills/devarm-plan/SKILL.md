---
name: "devarm-plan"
description: "Use after devarm-spec to produce an implementation plan an engineer with zero context could execute. Maps the file structure (what each file is responsible for), then breaks work into bite-sized TDD steps with exact paths and real code — no placeholders. Reuses spec-kit plan/data-model/contracts templates if .specify/ exists. By default, halt after the plan gate and ask whether to run devarm-tasks; continue automatically only when the user explicitly requested end-to-end execution."
metadata:
  phase: 5
  produces: "plan.md (+ data-model.md, contracts/ if applicable) with a file-structure map"
  next: "halt and ask about devarm-tasks unless end-to-end was explicitly requested"
---

## Announce

"I'm using devarm-plan to create the implementation plan from the spec and grounded design."

## Artifact and rule handoff contract

Before acting, record the active repository and branch in the artifact metadata. Discover
applicable target-repository instructions and link the canonical rule inventory; the
target-repository rule wins over a devarm default, and material conflicts require a visible
disposition. Run the optional validator; if it is unavailable, record the limitation and keep
the manual checklist authoritative. The optional validator is not required for the native method.
A deterministic blocking error stops the handoff; warnings remain visible and do not imply
approval. Preserve explicit approval gates and mark an unanswered decision `assumed — awaiting confirmation`.
If a settled decision is superseded, ripple-check dependent artifacts and re-check the affected
evidence before continuing.

When `.specify/` is absent, use `templates/plan-doc.md`. The plan's file-structure map and every
integration seam contract must be concrete before tasks are generated.

## Mindset

Write the plan assuming the engineer is skilled but knows almost nothing about this codebase or
problem domain, and doesn't know good test design. Document everything: which files to touch per
task, the actual code, how to test it, what to check. DRY, YAGNI, TDD, frequent commit-ready
checkpoints. Actual commits require explicit developer confirmation.

**Delta-first handoff:** treat the grounded design and spec as the source of settled architecture
and intent. Reference Decision Ledger IDs and requirement IDs; do not copy unchanged architecture,
problem, or lifecycle prose into `plan.md`. Spend plan space on file ownership, integration seams,
tests, commands, and implementation deltas. If the plan must contradict a settled decision, stop
and record a superseding decision before rewriting dependent sections.

## Steps

1. **Load context.** Read the approved+grounded design (especially its Detailed Design +
   Decision Ledger), the spec, and the repo's constitution/rules. The Decision Ledger already
   fixed the hard choices — the plan **implements** them, it does not re-litigate them.
2. **Map the file structure BEFORE tasks.** List every file to create or modify and its single
   responsibility. Lock decomposition here: one clear responsibility per file; files that change
   together live together; prefer small focused files. Honor the repo's file-size budgets (from
   grounding) with **hard numbers, not soft language**: state the max lines a touched god-file
   may gain (e.g. "≤ 40 lines of thin binding") and **name the new module** the logic goes into
   up front (e.g. `feature_binding.py`) — "watch item / extract if it grows" gets rationalized
   away (a real god-file grew 500+ lines that way).
3. **Fill technical context** (language, dependencies, storage, testing, constraints). Mark true
   unknowns `NEEDS CLARIFICATION` and resolve them (research) before finalizing.
4. **If `.specify/` exists**, generate `data-model.md`, `contracts/`, and `quickstart.md` per its
   plan template. Otherwise inline the equivalent (entities, interfaces) in `plan.md`.
5. **Give integration seams the same contract treatment as modules.** Pure modules are rarely
   where bugs live — **binding/integration seams are** (in a past session, nearly every
   post-implementation bug was in the seam left as "confirm during coding"; a prior failure repeated
   this: `gathered_info` alias drift, workflow-level import for mocks). For each seam
   (where new code hooks into existing flow, crosses a process/worktree boundary, or persists
   shared state) specify: exact call site, inputs/outputs, idempotency/replay behavior,
   failure posture, **shared mutable context sync** (which objects must hold the same dict
   reference — e.g. `diagnostic_context.gathered_info` ↔ `rem_context.gathered_info`), and
   **integration-test patch target** (patch where the caller imports — e.g.
   `backend.workflows.remediation_workflow.apply_*` — not only the defining module). **Git
   layout seam (required when checkout/publish touches an existing remote branch):** cite
   worktree clone mode + refspec from grounding; plan MUST include a **real-git mirror/worktree
   fixture test** (not mock-only `_run_git`) before the merge gate — mock tests alone cannot
   catch mirror `origin/*` absence or `mirror=true` fetch refusal. *Failure-class rationale (a prior failure):
   74 mocked tests green; live Docker E2E blocked until mirror refspec was fixed.* **Change-set
   pipeline seam (required when a feature introduces a new *change type* — deletion / rename /
   mode-change — or a new source of worktree changes):** enumerate EVERY stage that derives or
   filters the change set from production to publish (apply → merge/scope-select → sanitize →
   discard-outside-allowlist → commit → publish/scope-assert) and confirm the new type survives each
   stage; a deletion is not a file that `exists()` on disk, so any existence-based filter silently
   drops it. *Failure-class rationale (a prior failure): a reconciliation `revert` (a deletion) was stripped at 4
   `change-set sanitizer` sites + 2 discard sites; because each stage was found one at a time, it
   took 3 full live-E2E cycles (L1→L1b→L1c) to converge.* **Fix-loop retry-counter
   seam (required when a feature changes behavior on "repair retry" inside an existing
   re-entrant loop — fix loop, coverage loop, context-window retry, infra prep retry):**
   enumerate **every counter** that can mean "this is a repair retry" (`retry_count`,
   `repair prompt_attempts`, `coverage_retry_count`, etc.) and **every `continue` / early exit**
   between "code fix succeeded" and "loop iteration ends". For each path, state which counter
   increments **before** the next iteration and which gate (merge seed, prompt, discard
   allowlist) reads which counter. If merge and prompt use different counters, that is a
   **HIGH** plan defect — name one canonical `repair_retry` signal or document why they
   diverge. Add at least one **routing characterization test** per non-obvious loop
   (`coverage continue`, `action_prep sync continue`, context-window retry) that asserts
   the widen/narrow decision. *Failure-class rationale (a prior failure): D1 locked
   `retry_count > 0`; infra `retry_count` bump on `action_prep` widened merge before first
   code fix; pre-validation `coverage_retry_count continue` skipped `repair prompt_attempts +=
   1`, so the second code-fix run behaved like a first attempt and dropped multi-file
   patches; prompt gated on `retry_count` while merge used `repair prompt_attempts` — coverage
   feedback never reached the agent.* **repository-local skill contract seam
   (required when adding `backend/repository-local/skills/<name>/`):** specify producing vs
   reference-only (overlay loaded by another phase), require the standard untrusted-input
   guard, name the repo skill-content test module in the plan, and add a polish-task to run CI's
   full backend unit command — not only feature-targeted tests. *Failure-class rationale (a prior failure):
   targeted tests passed; CI failed on `test_skill_content_requirements`.* **Migration graph
   seam (required when adding an migration/DB revision):** cite the current single `migration heads`
   revision as `down_revision`; assign a **new** revision id that does not collide with any
   revision already on `main` or another in-flight branch; add a polish/verify step that re-runs
   `migration heads` and fails the plan if more than one head appears. *Failure-class rationale (a prior failure):
   lease columns and soft-delete both claimed `0026` → migrate graph broken until renumbered to
   `0027`.* **Settings/config patch seam (required when planned tests patch application
   settings or process-global config):** resolve the *binding site*, not a guess. If production
   code does `from backend.config import settings` (module-level **or** function-local), the plan's
   test patch MUST target `backend.config.settings.<attr>` (or the module that actually holds the
   bound name). Do **not** invent `feature_module.settings` unless that attribute exists at module
   scope — a local import ignores it and the patch is a silent no-op. Cite the import form
   (`module` vs `local`) next to the patch string. *Failure-class rationale (026 external-service authentication hardening):
   plan/tests first patched `application settings binding`; `get_service authenticator` locally
   imports `backend.config.settings` → analyze A5 HIGH before implement.* If a seam
   genuinely cannot be specified yet, add an explicit **spike task**
   to resolve it BEFORE the implementation task that depends on it — never defer it into the
   impl task itself.
   **Structured handoff seam (required when a feature passes structured agent/model output between
   phases or services):** add a shape-and-cardinality matrix before implementation. At minimum cover
   an absent, null, wrong-type, empty, singleton, and list-valued payload; missing, unknown, duplicate,
   and invalid identifiers; incomplete required fields; omitted current responses; and unmatched
   supplemental entries. For each case specify whether the caller rejects, normalizes, preserves, or
   exposes the value for a later phase, and state the exact prompt/renderer surface that must show it.
   If a field is stored in a handoff, require a rendering assertion for that field; if no
   deterministic semantic gate is allowed, record which phase owns the final decision. Add a failing
   test task for every non-obvious row, including the real caller seam rather than only the pure
   parser/renderer. This is category-scoped to cross-phase structured handoffs, not ordinary local
   function arguments.
5b. **State-transition table (required when the feature adds/changes a re-entrant or multi-actor
   state machine** — re-mention, retry, mid-flight arrival, resume, reopen, cancel, or any flow
   where the same entity is re-processed). A narrative walkthrough is not enough here and is
   silently skippable; a **table** makes a missing cell obvious. Enumerate every
   `(current_state × incoming_event)` cell and, for each, state: the **resulting state**, the
   **side-effects** (posts, reactions, `ui_generation`/card invalidation, metric), and **which
   module owns the write** (so cross-module ownership of the same field is explicit). Call out
   every cell whose resulting state must be **non-schedulable / preserving** (must not loop, must
   not downgrade, must not close/reset). *General rationale: ~6 same-class bugs — F1 ASSESSING
   loop, F3 dropped card, F6 two-mention downgrade, L1 unsupported closed an active investigation,
   R2→R3 re-queue signal — were all unenumerated `(state,event)→wrong terminal state` cells spread
   across the worker↔coordinator↔session_service seam.*
6. **Decompose into bite-sized tasks.** Each step is ONE action (2-5 min): write the failing
   test → run it (expect fail) → minimal implementation → run test (expect pass) → report a
   commit-ready checkpoint. Show the ACTUAL code and the ACTUAL command + expected output in
   each step. Do not instruct the implementer to run `git commit` unless the developer has
   explicitly authorized commits.

## No placeholders (these are plan failures — never write them)

- "TBD", "implement later", "add appropriate error handling / validation / edge cases".
- "Write tests for the above" without the test code.
- "Similar to Task N" — repeat the code; the engineer may read tasks out of order.
- References to types/functions/methods not defined in any task.

## Self-review (run yourself after writing the plan)

- **Spec coverage:** every spec requirement maps to a task — list gaps and add tasks.
- **Placeholder scan:** search for the red flags above; fix them.
- **Type consistency:** signatures/names used in later tasks match earlier definitions.
- **Ledger consistency:** the plan implements each Decision Ledger row (no drift from grounding).

## Hand off

Report the plan path, self-review result, and recommended next phase (`devarm-tasks`). By
default, STOP and ask the user whether to run `devarm-tasks`. Invoke `devarm-tasks` only if the
user explicitly requested end-to-end execution for this work or has just told you to continue. Do
not treat silence as approval to continue.
