# Retro: General Review-request repair handoff

**Date:** 2026-08-15  
**Target repository:** `/Users/dphadatare/vhosts/tech-catalyst-v2`  
**Target branch:** `039-general-review-request-repair-handoff`  
**Method repository:** `/Users/dphadatare/vhosts/devarm`  
**Pipeline:** brainstorm → ground → spec → plan → tasks → analyze → implement → review → finish  
**Outcome:** implementation and focused verification completed; PR not opened because the branch had zero commits ahead of `main`, and the full suite stalled in an external model-backed test.

## Evidence and current-state handoff

The current target-repository artifacts and diff were re-read before this retro. The existing
feature worktree contains unrelated tracked and untracked changes; the feature implementation
files were staged by an explicit allowlist, while unrelated changes remained unstaged.

The artifact validator was run from the canonical devarm repository:

| Artifact | Validator result |
|---|---|
| `spec.md` | `valid: true`, `issues: []` |
| `plan.md` | `valid: true`, `issues: []` |
| `tasks.md` | `valid: true`, `issues: []` |
| `analysis.md` | `valid: true`, `issues: []` |

Feature verification evidence:

- Focused repair-handoff/action-loop suite: 59 passed.
- Ruff: passed.
- mypy: passed with no issues in 415 source files.
- Fresh full backend run: progressed to 53% without an assertion failure, then stalled for
  several minutes in a subprocess running a live OpenCode/model path. It was interrupted and is
  therefore incomplete, not green.
- `git diff --cached --check`: passed after removing trailing whitespace from the staged plan.
- Current branch state at finish: `git rev-list --left-right --count origin/main...HEAD` was
  `0 0`; no PR existed for the branch.

## 1. Session arc

1. **Brainstorm:** The user and agent converged on a bounded runtime repair handoff. Review owns
   the final semantic decision; Code Fix validates every request and returns a disposition; no
   deterministic response gate or new persistence service is added.
2. **Ground/spec/plan/tasks/analyze:** The design, contract, lifecycle, and decision-to-test
   traceability were recorded. The artifacts covered exact request IDs, unmatched responses,
   fresh-session isolation, publication boundaries, and removal of the specialized revalidation
   category.
3. **Implement:** The handoff memory, prompt wiring, normalization, publication boundaries,
   skills, and tests were implemented through the existing retry path.
4. **Review/findgap/challenge:** Review identified three concrete defects: stale response memory
   was injected into Code Fix, invalid expectation IDs survived an empty finalized set, and the
   Review renderer omitted stored request evidence. Additional malformed-payload cases were
   found while repairing the same boundary.
5. **Repair:** The fixes added focused RED/GREEN coverage and preserved the approved rule that
   Review—not a deterministic validator—decides whether Code Fix satisfied a concern.
6. **Finish/PR preparation:** Focused checks and static gates passed. The fresh full suite could
   not complete because an external model-backed test had no bounded timeout. The branch also had
   no commit ahead of `main`, so a PR could not be opened under the explicit commit policy.

## 2. What held

- The user-owned semantic boundary held: Review remained the final authority, and no new
  deterministic response validator was introduced.
- The bounded-memory lifecycle held after repair: Code Fix receives the active request packet,
  Review receives the immediate response snapshot, fresh sessions do not inherit old repair
  context, and the handoff is discarded at the Review-to-PR transition.
- Exact code-owned request IDs and expectation associations remained internal; human-facing
  outputs continued to omit them.
- The existing ordinary bug/security publication blockers remained intact after removing the old
  specialized revalidation blocker.
- The existing devarm gates ran in order, and the target artifacts had no unresolved blocking
  findings or `assumed — awaiting confirmation` rows at the finish attempt.
- The dirty-worktree rule held: unrelated changes were not staged or overwritten.

## 3. Late decisions and where they belonged

| Late issue | Where it surfaced | Gate that should have locked it earlier |
|---|---|---|
| Exact behavior for malformed, singleton, duplicate, invalid, and incomplete Code Fix response shapes | Review repair and focused test additions | `devarm-plan` structured handoff seam contract and `devarm-tasks` shape-matrix tests |
| Which stored request fields must be rendered in the next Review prompt | Review finding R-003 | `devarm-plan` handoff field-to-renderer matrix |
| The practical distinction between a user-selected PR outcome and a branch with no commit to push | Finish/PR preparation | `devarm-finish` PR-head preflight |
| How long an external model-backed verification may block the lifecycle decision | Finish/PR preparation | `devarm-finish` bounded external verification |

These were implementation/verification decisions, not reopened product decisions. The user’s
semantic choice—Review decides—was already locked and was not changed.

## 4. Bugs by layer

The defects were primarily binding-seam defects, not isolated pure-function defects:

- **Phase wiring seam:** the response snapshot reached Code Fix through a prompt path that should
  have carried only the active Review packet.
- **Normalization seam:** expectation validation behaved differently when the finalized set was
  empty.
- **Renderer seam:** the memory object preserved evidence that the Review prompt did not expose.
- **Contract-shape seam:** malformed top-level and item-level response forms were not fully
  characterized before implementation.
- **Lifecycle/verification seam:** finish treated a long-lived external subprocess as ordinary
  suite progress and discovered the zero-commit PR condition only after expensive verification.

The pure memory builder and renderer tests were useful, but the first three defects show why a
passing pure test is insufficient for a cross-phase handoff without a caller-path and rendering
matrix.

## 5. Gate audit

| Gate | Held? | Evidence / gap |
|---|---|---|
| Brainstorm / Ground | Yes | Runtime memory, Review authority, no new validator, and lifecycle boundaries were decided and grounded. |
| Spec / Plan / Tasks | Mostly | Artifact validators passed and decision-to-test traceability existed, but the structured payload/cardinality matrix was not explicit enough. |
| Analyze | Yes | Current-code seam checks, implementation decision batch, and flagship flow were completed. |
| Implement / TDD | Yes for the repair batch | Each late repair received focused failing coverage before the fix; the first implementation still exposed an under-specified seam. |
| Review / findgap / challenge | Yes | Review found R-001–R-003; challenge prevented blindly adding a deterministic validator. |
| Finish | Partial | Fresh focused/static verification passed, but the full suite was interrupted by an unbounded external test. PR readiness also lacked a zero-commit preflight. |
| Retro | In progress | This report and the method diffs are the output of this phase. |

## 6. Method promotion decisions

### Promotion A — category-scoped structured-handoff matrix

- **Failure category:** Cross-phase structured-output contract under-specification.
- **Domain-neutral invariant:** Every structured handoff must define behavior for shape,
  cardinality, identity, completeness, unmatched values, and rendering; every stored value that
  matters to the receiving phase must have a caller-path/rendering assertion.
- **Enforcement point:** `skills/devarm-plan/SKILL.md`, with a required failing-test row in the
  generated task plan. `tests/test_method_contracts.py` protects the method wording.
- **Applicability boundary:** Applies to structured agent/model output passed between phases or
  services. It does not apply to ordinary local function arguments.
- **Generalization check:** The same seam exists in review/fix handoffs, intake/synthesis
  envelopes, webhook/event payloads, and persisted API DTOs. The rule is therefore reusable in a
  named cross-phase structured-handoff category, but does not need to become a universal parser
  policy.

### Promotion B — bounded external verification and PR-head preflight

- **Failure category:** Finish verification and lifecycle action attempted without bounded
  external execution or a publishable commit graph.
- **Domain-neutral invariant:** A lifecycle choice is available only after verification has a
  bounded, known result and the requested publish target contains a commit ahead of its base.
- **Enforcement point:** `skills/devarm-finish/SKILL.md`, before lifecycle options or push/PR
  execution. `tests/test_method_contracts.py` protects the timeout, incomplete-result, and
  zero-commit language.
- **Applicability boundary:** The timeout rule applies when tests spawn model, browser, network,
  Docker, or other external processes; the commit-graph rule applies to PR/push outcomes. Neither
  changes product runtime behavior or adds a deterministic product gate.
- **Generalization check:** Any repository can have external integration tests and any VCS-based
  PR flow can have uncommitted work. The exact timeout may be overridden by a repository CI limit,
  but it must remain explicit; the 15-minute fallback is the native default.

## 7. Back-and-forth drivers

- The discussion correctly explored whether to add `revalidation_request`, but many turns were
  spent re-evaluating the same semantic boundary before the decision ledger was fully used as the
  single source of truth.
- Review feedback was initially interpreted through the old specialized category, then
  revalidated against the approved general-request design. The findings ledger prevented the
  final repair from adding a second deterministic gate.
- Focused tests and static checks completed quickly, while the unbounded model-backed full suite
  consumed the finish tail without producing a usable verification result.
- Staging was carefully isolated, but the branch-head/commit preflight happened after staging and
  verification rather than before the PR finish path.

## 8. Proposed logical commit

Changed files in `/Users/dphadatare/vhosts/devarm`:

- `skills/devarm-plan/SKILL.md`
- `skills/devarm-finish/SKILL.md`
- `tests/test_method_contracts.py`
- `CHANGELOG.md`
- `docs/retros/2026-08-15-general-review-request-repair-handoff-retro.md`

Suggested commit message:

`retro: require structured handoff matrices and bounded finish verification`

No commit was created. Existing uncommitted devarm changes from the earlier multi-channel retro
were preserved.
