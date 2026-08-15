# Retro Generalization Gate — Analyze

**Document type:** Analysis/findings report
**Date:** 2026-08-13
**Status:** complete
**Phase:** analyze
**Feature/change:** Portable retro promotion and normative-skill audit
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☐ clarify ☐ plan ☑ tasks ☑ analyze ☑ implement ☑ review ☐ finish ☐
**Last session note:** Passes 1–3 are clean; implementation verified. Review/finish remain optional next gates.
**Last verification:** Fresh 87-test contract suite, product/framework-term audit, provenance-marker audit, and `git diff --check` — passed 2026-08-13
**Open assumptions / risks:** Standalone spec was intentionally skipped; approved design is the source of truth. Existing unrelated worktree changes remain.
**Next gate:** User confirmation of Pass 3, then final verification/review
**Target repository:** /Users/dphadatare/vhosts/devarm
**Target branch:** 001-devarm-purpose-evolution
**Related artifacts:** `docs/design/2026-08-13-retro-generalization-gate-design.md`, `docs/specs/devarm-retro-generalization/plan.md`, `docs/specs/devarm-retro-generalization/tasks.md`
**Rule inventory:** Approved design Section 7
**Analysis:** This document

## Validator limitation

The optional artifact validator was run on the design, plan, and tasks. It reports handoff-status
errors for non-`complete` draft/in-progress states and does not accept the design's `approved`
status. This is a validator-schema limitation; manual artifact and rule checks remain authoritative.

## Pass 1 — Cross-artifact consistency

**Result: clean.** The approved design goals D1–D5 map to T001–T005. The plan and tasks use the
same terms: failure category, domain-neutral invariant, applicability boundary, generalization
check, and portable/category-scoped/target-only outcomes. No persistence, configuration, or
runtime contract beyond Markdown skill instructions is introduced. The standalone spec is
explicitly skipped by user decision and recorded in all downstream artifacts.

## Pass 2 — Current-code verification

**Result: clean.** Current working-tree checks confirm:

- `skills/devarm-retro/SKILL.md` contains the new generalization and promotion contract.
- Every normative `skills/devarm-*/SKILL.md` has no `Session evidence`, `spec NNN`, `DEV-NNN`, or
  `PR #N` provenance marker.
- `tests/test_method_contracts.py` contains the RED/GREEN contract tests and the full suite passes.
- No application import, persistence shape, external service, prompt consumer, or deployment seam
  is changed by this work.
- `CHANGELOG.md` retains historical incident evidence and records the new portable boundary.
- A review sweep found and generalized remaining provider, issue-tracker, chat, migration, typed-
  model, and repository-local skill examples; no product/framework-specific terms remain in
  normative skills.

## Flagship flow

1. A retro receives incident/session evidence.
2. It classifies the reusable failure category and states the domain-neutral invariant.
3. It names the enforcement point and applicability boundary.
4. It checks the rule against at least two repository/domain shapes.
5. It promotes the result to portable core, category-scoped guidance, or target-only evidence.
6. Only the selected portable/category-scoped instruction is written to normative method files;
   provenance remains in changelog or retro artifacts.

Failure path: if the evidence cannot support generalization, the retro remains target-only or
deferred; it does not become a native devarm rule.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation | Status |
|---|---|---|---|---|---|---|
| A-001 | Artifact validator | LOW | `scripts/validate_devarm_artifacts.py` | Validator does not accept the repository's approved/phase-in-progress design states as a handoff artifact. | Preserve the limitation for this change; consider a separate validator contract change later. | accepted limitation |
| A-002 | Process timing | LOW | Current session; T001–T003 | Skill edits occurred after RED tests but before this durable analyze artifact because the user requested skipping spec and moving to implementation. | Keep this re-gate and require clean analyze evidence before final completion; no runtime risk exists. | resolved by re-gate |

No CRITICAL or HIGH findings remain.

## Review result

**Approved with no blocking findings.** The audit preserved generic category controls while removing
case provenance from normative skills. Historical evidence remains in `CHANGELOG.md`.

## Pass 3 — Implementation-decision batch

The control flow and failure path above were walked against the current skill and test surfaces.
The remaining choices are mechanical and already fixed by the approved design:

| ID | Decision | Recommended outcome | Status |
|---|---|---|---|
| P3-1 | Keep historical changelog incident evidence unchanged | Yes — it is provenance, not normative guidance. | approved |
| P3-2 | Keep generic technical examples while removing product/ticket provenance | Yes — this preserves useful category guidance without case promotion. | approved |
| P3-3 | Do not add automated taxonomy or runtime classification | Yes — human judgment remains the approval gate. | approved |

Analyze gate: Pass 1 clean; Pass 2 clean; Pass 3 complete with all three recommendations accepted.
