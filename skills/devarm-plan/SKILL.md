---
name: "devarm-plan"
description: "Use after devarm-spec to produce an implementation plan an engineer with zero context could execute. Maps the file structure (what each file is responsible for), then breaks work into bite-sized TDD steps with exact paths and real code — no placeholders. Reuses spec-kit plan/data-model/contracts templates if .specify/ exists. Hands off to devarm-tasks."
metadata:
  phase: 4
  produces: "plan.md (+ data-model.md, contracts/ if applicable) with a file-structure map"
  next: "devarm-tasks"
---

## Announce

"I'm using devarm-plan to create the implementation plan from the spec and grounded design."

## Mindset

Write the plan assuming the engineer is skilled but knows almost nothing about this codebase or
problem domain, and doesn't know good test design. Document everything: which files to touch per
task, the actual code, how to test it, what to check. DRY, YAGNI, TDD, frequent commits.

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
   post-implementation bug was in the seam left as "confirm during coding"). For each seam
   (where new code hooks into existing flow, crosses a process/worktree boundary, or persists
   shared state) specify: exact call site, inputs/outputs, idempotency/replay behavior, and
   failure posture. If a seam genuinely cannot be specified yet, add an explicit **spike task**
   to resolve it BEFORE the implementation task that depends on it — never defer it into the
   impl task itself.
6. **Decompose into bite-sized tasks.** Each step is ONE action (2-5 min): write the failing
   test → run it (expect fail) → minimal implementation → run test (expect pass) → commit. Show
   the ACTUAL code and the ACTUAL command + expected output in each step.

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

Report the plan path and self-review result, then invoke `devarm-tasks`.
