# Retro: Speeding up long design and planning sessions

**Date:** 2026-08-15  
**Target repository:** `/Users/dphadatare/vhosts/tech-catalyst-v2`  
**Target branch:** `039-general-review-request-repair-handoff`  
**Method repository:** `/Users/dphadatare/vhosts/devarm`  
**Focus:** reduce design/planning interaction cost without weakening grounding, user ownership,
TDD, analyze, review, or verification gates.

## Evidence and measurement limits

The full captured conversation transcript is:

`/Users/dphadatare/.codex/sessions/2026/08/15/rollout-2026-08-15T15-38-06-01a004e4-9d12-7202-a654-357fffa4d23e.jsonl`

The transcript contains:

- 116 user message records;
- 718 `exec` orchestration calls;
- 81 explicit wait calls;
- at least seven consecutive routine `recommended` acceptances during the design decision loop;
- repeated manual phase invocations for ground, spec, plan, analyze, implement, review, findgap,
  and challenge.

The imported transcript normalizes the message timestamps to one session-import timestamp, so the
claimed seven-to-eight-hour wall-clock duration cannot be independently measured from those
timestamps. The interaction volume and repeated decision/phase patterns do corroborate that the
dominant cost was conversational design/planning overhead rather than implementation runtime.

The target artifacts were already validated in the preceding retro:

| Artifact | Validator result |
|---|---|
| `spec.md` | `valid: true`, `issues: []` |
| `plan.md` | `valid: true`, `issues: []` |
| `tasks.md` | `valid: true`, `issues: []` |
| `analysis.md` | `valid: true`, `issues: []` |

The native devarm test suite was rerun after these speed edits: 93 tests passed. `git diff --check`
also passed. The artifact validator has no `retro` kind; the retro report therefore remains under
the native human-review contract, with its method-contract tests providing deterministic coverage
for the normative edits.

## 1. Session arc and time sinks

### A. Problem understanding was valuable but not front-loaded

The session began with a useful investigation of the existing review/retry behavior. The user
then repeatedly tested the distinction between:

- a Review request versus a special `revalidation_request` category;
- workflow/audit state versus runtime handoff memory;
- exact request IDs versus expectation IDs;
- Code Fix validation versus Review’s final decision;
- preserving unmatched responses versus discarding them;
- fresh Code Fix sessions versus active Review repair retries.

These were important product decisions. The avoidable cost was that the current-path inventory was
not presented as a compact producer/consumer/gap table early enough. Existing capabilities were
rediscovered through dialogue instead of being used as the starting delta.

### B. Routine decisions were serialized

After the user accepted the recommended direction, the transcript contains a long run of routine
`recommended`, `yes`, and `agree` responses. The existing brainstorm rule batched three or more
dispositions, but it did not trigger when the user was accepting ordinary design choices one after
another. Each small choice therefore consumed another turn and another full-context response.

### C. The phase pipeline was manually re-entered

The user separately invoked ground, spec, plan, analyze, implement, review, findgap, and
challenge. The gates themselves were useful, but the transition overhead was avoidable after the
user had made clear they wanted to continue. A batch-approved execution mode would preserve the
same gates while removing repeated “run the next phase?” turns.

### D. The same design was restated across artifacts

The design, spec, plan, tasks, and analysis all needed separate artifacts, but much of the same
architecture and lifecycle was explained repeatedly. The repeated prose increased review surface
and made it harder to see the few true deltas. The artifacts should reference settled design and
Decision Ledger IDs, then spend their space on their own responsibility: requirements, file
ownership, tests, current-code findings, or implementation decisions.

### E. Implementation and finish were not the main design-time bottleneck

Once the design stabilized, implementation was comparatively direct. The later review fixes were
real seam defects and deserved focused TDD. The finish stall was a separate verification problem,
already addressed by the previous retro with bounded external verification and PR-head checks.

## 2. What held and must not be optimized away

- The user retained ownership of semantic decisions instead of accepting a hidden deterministic
  response gate.
- Grounding and current-code inspection prevented the runtime-memory design from becoming a new
  persistence service or phase.
- The analyze decision batch and TDD/review gates caught and repaired real wiring, normalization,
  and rendering issues.
- The user’s requests for elaboration were honored; speeding up must not turn conceptual
  confusion into an automatic acceptance.
- The explicit phase gates, artifact validators, and dirty-worktree protections remain valuable.

The target is fewer turns per decision, not fewer decisions or less evidence.

## 3. Findings mapped to devarm gates

| Finding | Failure category | Existing gate | Speed change |
|---|---|---|---|
| Existing workflow capabilities were rediscovered during design | Existing-system delta discovery too late | `devarm-brainstorm` Step 1 / `devarm-ground` | Add a five-surface current-path delta checkpoint before alternatives. |
| Seven-plus routine recommendation accepts became separate turns | Serialized routine decision loop | `devarm-brainstorm` questioning rules | Trigger a full remaining decision batch after two consecutive routine accepts. |
| Ground/spec/plan/analyze transitions were manually repeated | Phase orchestration overhead | `AGENTS.md` phase-transition policy and `devarm-brainstorm` handoff | Offer explicit guided versus batch-approved pipeline mode once. |
| Settled architecture was restated across artifacts | Artifact duplication and review-surface growth | `devarm-spec` and `devarm-plan` artifact handoff | Reference design/ledger/requirement IDs and write deltas only. |
| The existing producer/consumer/gate relationships were explained only in prose | Missing visual system model | `devarm-brainstorm` current-path checkpoint and `devarm-ground` | Require an evidence-backed as-is map plus a to-be delta flow for three-or-more-surface or cross-phase changes. |

## 4. Generalization and promotion decisions

### Promotion A — portable current-path delta checkpoint

- **Failure category:** New design begins before existing producers, consumers, and contracts are
  summarized.
- **Domain-neutral invariant:** For an existing-system change, the design must distinguish what
  already works from the smallest missing behavior before proposing new components.
- **Enforcement point:** `skills/devarm-brainstorm/SKILL.md`, capped at five high-value surfaces
  with a required `existing behavior | actual gap | proposed delta | out of scope` table.
- **Applicability boundary:** Existing repositories and behavior/contract changes. Net-new
  projects without an existing path may state “no current path” and proceed.
- **Generalization check:** This applies equally to agent handoffs, API endpoints, event consumers,
  and UI workflows. The five-surface cap prevents the inventory from becoming a new analysis
  project; deeper discovery remains available when the feature proves it is needed.

### Promotion B — portable batch-approved execution mode

- **Failure category:** Repeated phase-transition turns after the user has clearly opted to
  continue.
- **Domain-neutral invariant:** A user may authorize automatic progression through non-approval
  gates while design approval, owner-user decisions, failures, and verification remain blocking.
- **Enforcement point:** `skills/devarm-brainstorm/SKILL.md`; the mode is selected once and is
  explicit, so it does not weaken the global “silence is not approval” rule.
- **Applicability boundary:** Multi-phase devarm work. Guided mode remains the default when the
  user has not selected batch-approved execution.
- **Generalization check:** The same mode works for backend features, data migrations, and
  workflow changes because it changes orchestration cadence, not the gates’ content.

### Promotion C — portable repeated-accept batch trigger

- **Failure category:** Routine implementation choices serialized into one question per turn.
- **Domain-neutral invariant:** Repeated acceptance of recommended routine choices is evidence
  that the user prefers a batch, unless the user is expressing confusion or opening a new fork.
- **Enforcement point:** `devarm-brainstorm` questioning rules and method-contract tests.
- **Applicability boundary:** Routine choices only; conceptual misunderstandings, design-level
  forks, and explicit one-by-one requests remain interactive.
- **Generalization check:** This is independent of product domain and applies to architecture,
  testing, lifecycle, and operational decisions. The two-accept trigger is a conversation-control
  heuristic, not an approval shortcut.

### Promotion D — portable delta-first artifacts

- **Failure category:** Repeated settled design prose across phase artifacts.
- **Domain-neutral invariant:** Each artifact should add the information owned by its phase and
  reference settled decisions by ID; only superseded decisions require repeated explanation.
- **Enforcement point:** `devarm-spec` and `devarm-plan` artifact handoff instructions and their
  method-contract tests.
- **Applicability boundary:** Features with an approved grounded design. New or superseding design
  decisions still require explicit ripple checks and updated artifact context.
- **Generalization check:** The rule applies to any artifact chain with shared design/spec/plan
  context and reduces prose drift without removing traceability.

### Promotion E — portable as-is/to-be visual grounding

- **Failure category:** Multi-surface system behavior explained without a shared visual model.
- **Domain-neutral invariant:** Before changing a cross-phase or multi-surface flow, participants
  must be able to see the existing producer/consumer/state/gate relationships and the proposed
  delta; existing edges must be grounded in current code.
- **Enforcement point:** `devarm-brainstorm` current-path delta checkpoint creates the visuals;
  `devarm-ground` reopens and annotates every node and edge with `file:line` evidence.
- **Applicability boundary:** Changes crossing a phase/process boundary or touching at least three
  high-value surfaces. A one-surface local change records `diagram: N/A` with a reason.
- **Generalization check:** The same visual helps explain agent pipelines, event-driven workers,
  API request flows, and UI state transitions. The rule requires a small flow/map, not a decorative
  architecture diagram or a visualization for every trivial edit.

## 5. Proposed method edits

The following edits are applied in the canonical devarm repository:

- `skills/devarm-brainstorm/SKILL.md`
  - five-surface current-path delta checkpoint;
  - guided versus batch-approved pipeline mode;
  - repeated-acceptance trigger for batching routine decisions;
  - evidence-backed as-is and to-be visuals for multi-surface changes.
- `skills/devarm-spec/SKILL.md`
  - delta-first writing rule.
- `skills/devarm-plan/SKILL.md`
  - delta-first handoff rule.
- `skills/devarm-ground/SKILL.md`
  - current-code validation of diagram nodes and edges.
- `tests/test_method_contracts.py`
  - contract coverage for all new speed controls.
- `CHANGELOG.md`
  - dated method-inventory entry.

This report is the durable evidence and rationale. The normative skill files contain no ticket
identifier or product-specific postmortem details.

## 6. Expected speed improvement

For a similar existing-system feature, the intended reduction is:

- one early current-path table instead of repeated capability rediscovery;
- one pipeline-mode choice instead of repeated manual phase invocations;
- one batch response for routine decisions instead of one turn per recommendation;
- delta-focused spec/plan review instead of re-reading settled architecture.
- one shared as-is/to-be visual instead of repeatedly reconstructing the existing flow in prose.

The method still requires design approval, grounding, artifact validation, analyze Pass 3,
tests-first implementation, review, and fresh verification. The likely result is a materially
shorter design/planning conversation while preserving the decisions that prevented incorrect
implementation.

## 7. Verification and suggested commit

Verification completed:

```text
python3 -m unittest discover -s tests -q
Ran 95 tests in 2.000s
OK

git diff --check
passed
```

Suggested commit message:

`retro: batch decisions and require evidence-backed system maps`

No commit was created. Existing uncommitted devarm changes from earlier retros were preserved.
