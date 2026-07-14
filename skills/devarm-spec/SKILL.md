---
name: "devarm-spec"
description: "Use after a design is grounded (devarm-ground) and approved, to produce a testable specification. Turns the WHAT/WHY of the design into unambiguous, testable functional requirements, user scenarios, and measurable, technology-agnostic success criteria. Reuses spec-kit templates if a .specify/ directory exists; otherwise uses devarm/templates. Hands off to devarm-plan."
metadata:
  phase: 3
  produces: "spec.md + a spec quality checklist"
  next: "devarm-plan"
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
- Cover user scenarios / primary flows, edge cases, scope boundaries, dependencies, assumptions.
- Make informed guesses using context and industry standards; record them in an Assumptions
  section. Use at most **3** `[NEEDS CLARIFICATION]` markers, only for choices that materially
  affect scope, security/privacy, or UX with no reasonable default.

## Quality gate (run before handing off)

Validate the spec against this checklist; iterate (max 3 passes) until it passes:

- [ ] No implementation details leak in (languages, frameworks, APIs).
- [ ] Requirements are testable and unambiguous.
- [ ] Success criteria are measurable and technology-agnostic.
- [ ] All acceptance scenarios defined; edge cases identified.
- [ ] Scope is clearly bounded; dependencies and assumptions listed.
- [ ] No unresolved `[NEEDS CLARIFICATION]` beyond the 3-max, and each has been surfaced.

## Hand off

Report the spec path and checklist result, then invoke `devarm-plan`.
