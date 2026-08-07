---
name: "devarm-spec"
description: "Use after a design is grounded (devarm-ground) and approved, to produce a testable specification. Turns the WHAT/WHY of the design into unambiguous, testable functional requirements, user scenarios, and measurable, technology-agnostic success criteria. Reuses spec-kit templates if a .specify/ directory exists; otherwise uses devarm/templates. By default, halt after the spec gate and ask whether to run devarm-plan; continue automatically only when the user explicitly requested end-to-end execution."
metadata:
  phase: 3
  produces: "spec.md + a spec quality checklist"
  next: "devarm-clarify (recommended), then halt and ask about devarm-plan unless end-to-end was explicitly requested"
---

## Announce

"I'm using devarm-spec to write the testable specification from the grounded design."

## Where the spec lives

- If the target repo has a `.specify/` (spec-kit) directory: create the feature via its flow
  (`specs/<NNN-or-timestamp>-<short-name>/spec.md`) and reuse `.specify/templates/spec-template.md`
  and `.specify/memory/constitution.md`.
- Otherwise: create `docs/specs/<short-name>/spec.md` from `devarm/templates/` (or inline a
  minimal spec section into the design doc for tiny features).

## Rules for the spec

- Focus on **WHAT** users need and **WHY**. Avoid HOW (no tech stack, APIs, code structure) —
  the HOW already lives in the grounded design's Detailed Design + Decision Ledger; reference it,
  don't repeat it.
- Every functional requirement must be **testable and unambiguous**. If a requirement could be
  read two ways, pick one and make it explicit.
- Success criteria must be **measurable and technology-agnostic** (e.g. "users complete checkout
  in under 3 minutes", not "API responds in 200ms").
- **User stories are prioritized (P1, P2, …) and independently testable.** Each story is a
  standalone slice that could be implemented, tested, and demonstrated on its own; name its
  "Independent Test" explicitly and write acceptance scenarios as Given/When/Then. P1 stories
  alone must form a viable MVP — this is what lets tasks be organized story-by-story and lets
  implementation stop at a working increment.
- Cover user scenarios / primary flows, edge cases, scope boundaries, dependencies, assumptions.
  Scenario classes to check explicitly: primary, alternate, exception/error, recovery, and
  non-functional — mark any class intentionally excluded rather than leaving it silently absent.
- Make informed guesses using context and industry standards; record them in an Assumptions
  section. Use at most **3** `[NEEDS CLARIFICATION]` markers, only for choices that materially
  affect scope, security/privacy, or UX with no reasonable default.

## Quality gate (run before handing off)

The gate tests the REQUIREMENTS, not the implementation ("unit tests for English"): each check
asks whether what's *written* is complete, clear, consistent, measurable, and covered — e.g.
"is 'fast' quantified?", "do §FR-4 and §FR-10 conflict?", "is the zero-state defined?". For a
complex or risky domain (security, migration, UX-heavy), optionally generate a short
domain-specific checklist of such questions, each tagged [Completeness/Clarity/Consistency/
Coverage/Measurability] and tied to a spec section or [Gap].

Validate the spec against this checklist; iterate (max 3 passes) until it passes:

- [ ] No implementation details leak in (languages, frameworks, APIs).
- [ ] Requirements are testable and unambiguous.
- [ ] Success criteria are measurable and technology-agnostic.
- [ ] All acceptance scenarios defined; edge cases identified.
- [ ] Scope is clearly bounded; dependencies and assumptions listed.
- [ ] No unresolved `[NEEDS CLARIFICATION]` beyond the 3-max, and each has been surfaced.

## Hand off

Report the spec path, checklist result, and recommended next phase (**`devarm-clarify`**, then
`devarm-plan`). By default, STOP and ask the user whether to run **`devarm-clarify`**. If the
user explicitly skips clarify, log the risk in the spec (Assumptions or Clarifications) and ask
about `devarm-plan`. Invoke `devarm-clarify` or `devarm-plan` only if the user explicitly
requested end-to-end execution for this work or has just told you to continue. Do not treat
silence as approval to continue.
