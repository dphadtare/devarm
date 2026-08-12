# Retro Generalization Gate — Implementation Plan

**Document type:** Implementation plan
**Date:** 2026-08-13
**Status:** complete
**Phase:** plan
**Feature/change:** Portable retro promotion and normative-skill audit
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☐ clarify ☐ plan ☑ tasks ☐ analyze ☐ implement ☐ review ☐ finish ☐
**Last session note:** Standalone specification intentionally skipped by user; approved design is the source of truth.
**Last verification:** `python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-13-retro-generalization-gate-design.md --kind design` — validator reports draft/approved status limitation; manual grounding complete.
**Open assumptions / risks:** Existing uncommitted method-evolution changes are preserved; audit must not remove generic technical guidance.
**Next gate:** tasks, then analyze
**Target repository:** /Users/dphadatare/vhosts/devarm
**Target branch:** 001-devarm-purpose-evolution
**Related artifacts:** `docs/design/2026-08-13-retro-generalization-gate-design.md`
**Rule inventory:** `docs/design/2026-08-13-retro-generalization-gate-design.md` Section 7
**Analysis:** `docs/specs/devarm-retro-generalization/analysis.md`

## Implementation objective

Make retro promotions explicitly category-based and keep normative devarm skills free of
incident-specific provenance. Preserve historical evidence in `CHANGELOG.md` and preserve
generic technical examples that explain reusable rules.

## Scope and requirement coverage

| Design goal / decision | Plan coverage |
|---|---|
| G1–G4, D1–D3: category, invariant, boundary, generalization, and promotion outcomes | T001–T003 |
| G5, D4: contract tests with no runtime taxonomy | T001–T004 |
| G6, D5: audit all normative skills; preserve history | T001, T003, T004 |

Acceptance coverage and verification are provided by T001–T005 and the commands in Verification.

## File-structure map

| File | Single responsibility | Budget |
|---|---|---:|
| `skills/devarm-retro/SKILL.md` | Define retro evidence, abstraction, and promotion contract | ≤30 net added lines |
| `skills/devarm-*/SKILL.md` | Hold only domain-neutral normative instructions and generic examples | No file grows; audit may remove/rewrite case prose |
| `tests/test_method_contracts.py` | Lock documentation contracts and forbidden case markers | ≤45 net added lines |
| `CHANGELOG.md` | Record this method change and its motivating evidence | One dated entry |
| `docs/design/2026-08-13-retro-generalization-gate-design.md` | Approved source of truth and ledger | No further design expansion |

## Technical context

The repository is a Markdown-defined method kit with standard-library contract tests. There is no
application runtime seam, persistence change, external dependency, or `.specify/` directory. The
existing retro skill already requires motivating evidence, verification evidence, recurrence or
severity, and a diff in the canonical devarm repository. The implementation adds human-checkable
fields and a textual regression guard; it does not classify domains automatically.

## Integration seams and contracts

There are no runtime integration seams. The documentation seam is:

- Input: a retro report or current session evidence.
- Transformation: classify failure category → state invariant → define boundary → test across two
  repository/domain shapes → choose portable/category-scoped/target-only outcome.
- Output: a method diff only when the abstraction check passes; otherwise target-only/deferred
  evidence remains in the retro record.
- Test target: `MethodContractTests` reads `skills/devarm-retro/SKILL.md` and every
  `skills/devarm-*/SKILL.md`.
- Failure posture: missing fields or forbidden provenance markers fail the contract test; no
  historical artifact is deleted.

## Implementation tasks

`docs/specs/devarm-retro-generalization/tasks.md` is the sole executable task source.

## Verification

- RED/GREEN focused command: `python3 -m unittest tests.test_method_contracts.MethodContractTests`
- Full repository contract suite: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Artifact validation where supported: `python3 scripts/validate_devarm_artifacts.py --artifact <path> --kind <kind>`
- Final audit: `rg -n -i 'session evidence|spec [0-9]{3}|DEV-[0-9]+|PR #[0-9]+' skills/devarm-*/SKILL.md`

## Self-review

- [x] Every design goal and ledger row maps to a task.
- [x] Every implementation task has a preceding RED task.
- [x] No application seam, persistence shape, or runtime dependency is introduced.
- [x] Historical changelog evidence is explicitly out of scope for cleanup.

## Repository Rule Inventory

The canonical inventory is the approved design's Section 7. This plan preserves its target-rule
precedence, evidence-before-assertion, no-destructive-worktree, and retro ownership rules.
