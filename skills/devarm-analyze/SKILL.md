---
name: "devarm-analyze"
description: "Use after devarm-tasks and BEFORE devarm-implement — a mandatory read-only gate with two passes: (1) cross-artifact consistency (design ↔ spec ↔ plan ↔ tasks ↔ Decision Ledger), and (2) architecture-vs-codebase verification that re-checks every integration claim against the CURRENT code, since the repo may have moved since grounding. Also traces the flagship user story end-to-end on paper. Blocks implementation until CRITICAL/HIGH findings are resolved. Also usable as a re-gate after large fix batches."
metadata:
  phase: 6
  produces: "analysis report (severity-ranked findings); implementation blocked until CRITICAL/HIGH resolved"
  next: "devarm-implement (once clean)"
---

## Why this skill exists

Artifact self-consistency and artifact-vs-code truth are different checks. A spec/plan/tasks set
can be perfectly internally consistent and still be wrong about the code — an assumed-sync service
that is async, an assumed-wired component that is dead scaffolding, an evidence rule that rejects
the flagship use case. Those are the failures that surface as mid-implementation flip-flops. And
because grounding happened at design time, the repo may have moved since. This gate catches both
classes right before any code is written.

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
- **Ledger status:** no row still `assumed — awaiting confirmation` — resolve with the user now.

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

## Output

A severity-ranked findings table: `ID | Category | Severity (CRITICAL/HIGH/MEDIUM/LOW) |
Location(s) | Summary | Recommendation`. Then:

- CRITICAL/HIGH → fix the artifacts (with the user for `owner: user` items) and re-run the
  failing pass.
- MEDIUM/LOW → fix or explicitly accept with a note.
- Update the Decision Ledger for anything Pass 2 changed (new evidence, superseded rows).

## Gate

Do not hand to `devarm-implement` until Pass 1 and Pass 2 report zero unresolved CRITICAL/HIGH
findings. State the final result explicitly ("analyze clean" or the accepted residuals).
