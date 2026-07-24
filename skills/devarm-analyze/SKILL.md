---
name: "devarm-analyze"
description: "Use after devarm-tasks and BEFORE devarm-implement — a mandatory gate with three passes: (1) cross-artifact consistency (design ↔ spec ↔ plan ↔ tasks ↔ Decision Ledger), (2) architecture-vs-codebase verification that re-checks every integration claim against the CURRENT code, since the repo may have moved since grounding, and (3) an interactive implementation-decision brainstorm — a control-flow walkthrough with the user that batch-decides every foreseeable implementation decision before any code. Also traces the flagship user story end-to-end on paper. Blocks implementation until CRITICAL/HIGH findings are resolved and Pass 3 decisions are recorded. Also usable as a scoped re-gate after course corrections or large fix batches. By default, halt after the analyze report and ask whether to run devarm-implement; continue automatically only when the user explicitly requested end-to-end execution."
metadata:
  phase: 6
  produces: "analysis report (severity-ranked findings) + batch-decided implementation decisions in the ledger; implementation blocked until CRITICAL/HIGH resolved"
  next: "halt and ask about devarm-implement once clean unless end-to-end was explicitly requested"
---

## Why this skill exists

Artifact self-consistency and artifact-vs-code truth are different checks. A spec/plan/tasks set
can be perfectly internally consistent and still be wrong about the code — an assumed-sync service
that is async, an assumed-wired component that is dead scaffolding, an evidence rule that rejects
the flagship use case. Those are the failures that surface as mid-implementation flip-flops. And
because grounding happened at design time, the repo may have moved since. This gate catches both
classes right before any code is written.

Passes 1 and 2 are agent-driven verification. Pass 3 exists because verification alone still
leaves decisions to surface piecemeal during coding — where question fatigue makes the user
"go with the flow" and lets control-flow changes through unexamined. Pass 3 pulls those
decisions into one interactive sitting before implementation starts.

## Announce

"I'm using devarm-analyze to gate the artifacts against each other and against the current code."

## Pass 1 — Cross-artifact consistency (read-only)

Load the design (incl. Detailed Design + Decision Ledger), spec, plan, and tasks. Check:

- **Coverage:** every requirement has ≥1 task; every Decision Ledger row has its enforcing
  task/test; every task traces back to a requirement or ledger row (no orphan tasks).
- **Ambiguity:** vague adverbs ("large", "fast", "may escalate") without a threshold; any
  `[NEEDS CLARIFICATION]` left; any config value missing its four sub-answers.
- **Terminology drift:** the same concept named differently across artifacts (incl. requirement
  ID schemes) — one canonical name/ID everywhere.
- **Duplication / contradiction:** conflicting statements between artifacts; if two planning
  artifacts describe the same work, ONE is declared canonical and the other references it.
- **Ledger status:** flag every row still `assumed — awaiting confirmation` — these get resolved
  with the user in Pass 3, never carried into implementation.

## Pass 2 — Architecture-vs-codebase verification (read-only)

Grounding cited evidence at design time; the repo may have changed since. Re-verify against the
CURRENT working tree:

- **Every seam:** the cited `file:line` hooks still exist and still mean what the plan says.
- **Every reuse claim:** open the target again — confirm shape (sync/async, statefulness,
  signature), legality (import direction), and that it is actually wired into the live path (dead
  scaffolding is not reuse).
- **Flagship walkthrough:** trace the #1 user story end-to-end through the planned components on
  paper, with real data shapes. Confirm no gate/filter/threshold on the path rejects the flagship
  case itself. (This is the check that catches "the evidence rule rejects our headline use case".)
- **Runtime contracts:** every contract change in the plan has its paired prompt/SKILL update
  task, and the current runtime files match what the plan assumes they say.

## Pass 3 — Implementation-decision brainstorm (interactive, with the user)

This is a dialogue, not a report. Run it after Passes 1–2 are clean (or their findings are
resolved), in this order:

1. **Control-flow walkthrough.** Narrate the functional/control flow of the flagship scenario
   AND each major failure/edge path through the planned components, as short numbered flows the
   user can read and object to ("A receives X → validates via B → on failure does C…"). Pause
   after each flow for confirmation. An objection is a reopened decision → handle via
   `devarm-brainstorm`'s back-and-forth protocol (supersede + ripple-check), not an inline patch.
2. **Enumerate the foreseeable implementation decisions.** Collect into one list: (a) every
   ledger row still `assumed — awaiting confirmation` or `owner: user` and undecided; (b) every
   implementation trade-off visible from the plan/tasks (module placement, error-handling
   strategy, retry/timeout choices, back-compat shims, library selection); (c) every fork the
   walkthrough surfaced.
3. **Batch-present with recommendations.** One list, each item carrying
   `**Recommended:** <option> — <1-2 line reason>`; tell the user a plain "yes" accepts all
   recommendations, or they can override per item. List `owner: user` design-level items FIRST
   and under their own heading, separate from routine trade-offs, so a batch "yes" never buries
   an intent-level decision. Record every answer as a Decision Ledger row.
4. **Exit criterion.** The target is that `devarm-implement` asks the user near-zero questions:
   only genuine design-level surprises may interrupt coding. A foreseeable trade-off that still
   surfaces mid-implementation is a Pass-3 miss — `devarm-implement` logs it for `devarm-retro`.

**Scoped re-runs.** When analyze is re-run scoped (after a course correction, drift, or a large
fix batch), Pass 3 covers ONLY the flows and decisions the change touched; previously confirmed
flows and recorded ledger decisions stand unless the change superseded them. Never re-walk the
whole feature — that recreates the question fatigue this pass exists to remove.

## Output

A severity-ranked findings table: `ID | Category | Severity (CRITICAL/HIGH/MEDIUM/LOW) |
Location(s) | Summary | Recommendation`. Then:

- CRITICAL/HIGH → fix the artifacts (with the user for `owner: user` items) and re-run the
  failing pass.
- MEDIUM/LOW → fix or explicitly accept with a note.
- Update the Decision Ledger for anything Pass 2 changed (new evidence, superseded rows).

## Gate

Do not hand to `devarm-implement` until Pass 1 and Pass 2 report zero unresolved CRITICAL/HIGH
findings AND Pass 3 is complete: every walked flow confirmed, the decision batch answered and
recorded in the ledger, and no row left `assumed — awaiting confirmation`. State the final
result explicitly ("analyze clean" or the accepted residuals).

By default, STOP after the report and ask the user whether to run `devarm-implement`. Invoke
`devarm-implement` only if analyze is clean AND the user explicitly requested end-to-end
execution for this work or has just told you to continue. Do not treat silence as approval to
begin implementation.
