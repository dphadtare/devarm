---
name: "devarm-review"
description: "Use when a major step completes or before merge, to review the work against the grounded design, the Decision Ledger, and the repo's principles. Applies an architecture lens and a QA lens (the useful, transferable part of persona-based methods) without a heavyweight persona framework. Produces prioritized, actionable review notes."
metadata:
  phase: 8
  produces: "prioritized review notes (blocking / should-fix / nit)"
  next: "devarm-implement (to address) or devarm-finish (to integrate)"
---

## Announce

"I'm using devarm-review to review this work against the grounded design and the repo's rules."

## Inputs

- The diff / changed files, the spec, and the grounded design (Detailed Design + Decision
  Ledger), plus the repo's constitution / architecture / design-principles rules.

## Two lenses

### Architecture lens
- **Boundaries:** are all imports legal per the dependency direction? Any cycles?
- **File-size / god-files:** did any listed god-file grow with business logic instead of a thin
  seam? Should anything be extracted?
- **Single conventions / no duplication:** any concept (enum, status, constant, type) declared a
  second time instead of reusing its one home? Any half-finished refactor (new way added, old way
  left)?
- **Patterns / anti-patterns:** does the change follow the project's pattern catalog (or
  `devarm/templates/code-standards.md` as fallback)? Watch for the classics: fat controller,
  query built inside a service, ORM objects leaking across the API boundary, commit inside a
  helper instead of the transaction owner, view-local data fetching, a second persistence
  style beside the established one, new type/lint suppressions.
- **Ledger fidelity:** does the implementation match each Decision Ledger row? Flag every drift —
  if the code chose differently than the ledger, either the code is wrong or the ledger must be
  updated with new evidence.
- **Runtime prompt/directive sweep:** if the change adds or edits a prompt-injected instruction
  gated on a runtime value, confirm it holds (or is suppressed) in EVERY context that builds that
  prompt — primary vs expansion/variant. A directive true on one path can contradict an
  authoritative block in the same prompt on another (a real bug in a past session: a "single
  linked repository" directive fired on a pinned expansion pass that carried a multi-repo plan).
- **Cross-section pairing (skill/prompt-only):** when the diff touches multiple sections of the
  same runtime artifact, list every **section pair** checked (e.g. Finding Severity ↔ Phase 1e,
  new Phase 1c item ↔ existing Phase 1b item) and record pass/fail in the findings ledger or
  polish task — a read scoped to "the sections we added" misses contradictions in sections we
  only referenced. *Session evidence: T026 read Hard Rules + Phase 1c 7-10 only; G1 (floor vs
  Phase 1e) escaped until findgap.*

### QA lens
- **Test coverage of behavior** (not just lines): does each spec requirement have a test? Are
  failure modes, edge cases, empty/single/disabled paths, and idempotency/replay tested?
- **Mock-boundary / inert-feature audit:** for each behavioral success criterion, state whether its
  covering test exercises the **real seam** or mocks it out. An SC whose only test mocks the exact
  seam it asserts is **not covered** — green there is false confidence. Require at least one test per
  behavioral SC that runs the unmocked path (real-git fixture, in-process wiring, or a live smoke),
  or mark completion **provisional pending a live run**. *Session evidence: spec 028's flagship test
  mocked `run_action_phases`, so a completely unwired reconciliation (dropped field, unrendered
  prompt, scope-stripped deletion) passed green and was approved — only live E2E exposed it; spec 027
  repeated the shape (74 mocked `_run_git` tests green, live E2E failed).*
- **Determinism:** are ordering/tiebreak rules actually enforced and tested?
- **Verification evidence:** were tests/lints/types actually run green? Ask for the output if not
  shown. Re-derive "done" from the repo itself (grep for the named test / read the file), never
  from a prior session summary or an implementer's claim — in a past session a compaction summary
  asserted wording-lock tests that were absent from the codebase.
- **UX / contract consistency:** does observable behavior match the spec's success criteria?

## Output

Group findings by severity and make each one actionable with a file:line reference:

- **Blocking** — must fix before merge (broken behavior, boundary/ledger violation, missing test
  for a requirement).
- **Should-fix** — real issues that aren't merge-blockers.
- **Nit** — style/readability.

Be technically rigorous, not performative: verify claims, don't rubber-stamp, and don't invent
problems. If it's solid, say so and approve.

## Findings ledger (one home for all review findings)

Write findings to a single durable file (`findings.md` beside the spec/plan) with one row each:
`ID | claim | severity | verdict + code evidence (file:line) | status (fixed / deferred /
rejected)`. Multiple/parallel review passes **append to this one file**; the implementer works
it top-to-bottom. This replaces re-feeding raw review transcripts — which in a past session
triggered full re-verification loops, some of invalid findings, and re-asking of already-pending
items.

**Verify verdicts in both directions.** Trace the actual runtime path before accepting *any*
verdict — a reviewer's finding can be wrong, and so can an implementer's rebuttal (in a past
session each was wrong once about the same `SKILL.md` issue). Evidence, not authority.

**Challenge before fix-all.** When the findings ledger has multiple HIGH/Should-fix items — or
after an external `/findgap` pass — pressure-test each against grounded design, Decision Ledger
rows, and real consumers before implementing all of them. Overreach (spec 022: SC-005 "missing
render" while `possible_causes` + `best_repo_evidence` already surfaced) wastes a fix cycle;
defer or downgrade items that contradict locked decisions or grounded design.

**Check every finding against the Decision Ledger first.** A finding that contradicts a recorded
`owner: user` decision is `by-design`, not a bug, unless the user explicitly reopens it — this
stops reviews from re-litigating settled decisions (a real source of churn in a past session).

## Receiving feedback (when you are the implementer working the ledger)

- **No performative agreement.** Never "You're absolutely right!" / "Great point!" / thanks.
  Restate the technical requirement, or just fix it — the diff is the acknowledgment.
- **Clarify ALL items before implementing ANY.** For multi-item feedback where some items are
  unclear: stop and ask about the unclear ones first — items may be related, and partial
  understanding produces wrong implementations of the clear ones too.
- **Order of execution:** blocking → simple → complex; test each fix individually.
- **YAGNI-check "implement it properly" suggestions:** grep for actual usage first. If nothing
  calls it, propose removal instead of building it out.
- **Push back with technical reasoning** when a suggestion breaks existing behavior, ignores
  context, or contradicts a ledger decision — and if your pushback turns out wrong, state the
  correction factually ("verified — you're correct because X; fixing") and move on. No
  apologies, no defending.
- **Design-deviation guard (fires at fix time, not review time).** Before applying a finding whose
  fix would *change* an agreed design decision or a locked Decision Ledger row — not merely
  implement it — STOP and consult the user first; that remediation is itself a design-level
  decision. Supersede the ledger row explicitly (with a ripple-check of its consumers); never
  smuggle a redesign into a "fix". This is distinct from the reviewer-side "check findings against
  the ledger" rule above — that screens findings; this screens the *fixes* you apply to them.

## End every review turn with an explicit state split

Close each turn with two labeled lists so "fix the issues found" is never ambiguous:

- **Already fixed this turn** — with the commit if explicitly authorized, otherwise with the
  diff/checkpoint evidence.
- **Awaiting your decision** — findings that need the user's call before action.

(Ambiguity here caused duplicate "fix it" turns on already-applied fixes in a past session.)
