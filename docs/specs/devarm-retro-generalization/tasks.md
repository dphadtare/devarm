# Retro Generalization Gate — Tests-first Tasks

**Document type:** Tests-first task list
**Date:** 2026-08-13
**Status:** complete
**Phase:** tasks
**Feature/change:** Portable retro promotion and normative-skill audit
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☐ clarify ☐ plan ☑ tasks ☑ analyze ☐ implement ☐ review ☐ finish ☐
**Last session note:** Standalone specification skipped by explicit user decision; approved design and plan govern.
**Last verification:** RED to be run before implementation
**Open assumptions / risks:** Generic technical examples remain allowed; only incident/product provenance is prohibited in normative skills.
**Next gate:** devarm-analyze
**Target repository:** /Users/dphadatare/vhosts/devarm
**Related artifacts:** `docs/design/2026-08-13-retro-generalization-gate-design.md`, `docs/specs/devarm-retro-generalization/plan.md`
**Target branch:** 001-devarm-purpose-evolution
**Rule inventory:** `docs/design/2026-08-13-retro-generalization-gate-design.md` Section 7
**Analysis:** `docs/specs/devarm-retro-generalization/analysis.md`

## Execution contract

Follow RED → GREEN → refactor → verify. Do not commit without explicit developer authorization.

## Setup

### Setup and baseline

Confirm `git status --short` and preserve all existing modifications. Run the focused contract
test before editing production skill text.

## Foundational work

### Foundational validator behavior

The contract tests are the deterministic validator for the documentation-only change. They scan
the canonical skill paths and do not inspect historical changelog or design evidence.

## Story groups

### T001 [RED] Lock the retro generalization contract

**Files:** `tests/test_method_contracts.py`
**Requirements/decisions:** G1–G5; D1–D4.

Add assertions that `skills/devarm-retro/SKILL.md` requires a failure category, domain-neutral
invariant, applicability boundary, generalization check across two shapes, and portable,
category-scoped, and target-only outcomes. Run:

```bash
python3 -m unittest tests.test_method_contracts.MethodContractTests
```

Expected RED: the new contract phrases are absent.

### T002 [RED] Lock the normative-skill provenance prohibition

**Files:** `tests/test_method_contracts.py`
**Requirements/decisions:** G6; D5.

Add a test that scans every `skills/devarm-*/SKILL.md` and rejects incident provenance markers:
`Session evidence`, `spec NNN`, `DEV-NNNNNN`, and `PR #N`. Keep the allowlist limited to generic
technical examples; do not scan `CHANGELOG.md` or design/retro artifacts.

Run the focused suite and record RED because current skills contain those markers.

### T003 [GREEN] Generalize retro promotion instructions and audit normative skills

**Files:** `skills/devarm-retro/SKILL.md`, `skills/devarm-brainstorm/SKILL.md`,
`skills/devarm-ground/SKILL.md`, `skills/devarm-plan/SKILL.md`, `skills/devarm-tasks/SKILL.md`,
`skills/devarm-analyze/SKILL.md`, `skills/devarm-implement/SKILL.md`,
`skills/devarm-review/SKILL.md`, `skills/devarm-finish/SKILL.md`, `skills/devarm-debug/SKILL.md`,
`skills/devarm-clarify/SKILL.md`
**Requirements/decisions:** G1–G4, G6; D1–D3, D5.

Add the retro generalization gate. Rewrite or remove case-specific provenance annotations and
postmortem narratives in normative skills. Preserve the underlying generic controls, replacing
product/module/ticket names with neutral terms such as `orchestrator`, `serializer`, `migration
graph`, `retry signal`, and `operator-facing output` where needed. Do not alter historical
`CHANGELOG.md` evidence.

Run the focused suite and confirm GREEN.

### T004 [GREEN] Record the portable method change

**Files:** `CHANGELOG.md`
**Requirements/decisions:** G2, G6; D2, D4, D5.

Add one dated entry describing the generalization gate and the normative-skill audit. Name the
Tech Catalyst-derived incidents only as motivating evidence, not as devarm behavior. Run the
focused suite again.

## Polish and verification

### T005 [VERIFY] Audit and full contract suite

**Files:** all `skills/devarm-*/SKILL.md`, `tests/test_method_contracts.py`
**Requirements/decisions:** G5–G6; D4–D5.

Run the marker audit, focused contract suite, and full test discovery. Confirm no skill file grows
because of the change and review the diff to ensure generic rules were not accidentally removed.

Commands:

```bash
rg -n -i 'session evidence|spec [0-9]{3}|DEV-[0-9]+|PR #[0-9]+' skills/devarm-*/SKILL.md
python3 -m unittest tests.test_method_contracts.MethodContractTests
python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected result: the marker search returns no matches; all tests pass.

## Self-check

- [x] Every implementation task has a preceding tests-first task.
- [x] Every design goal and Decision Ledger row has enforcement coverage.
- [x] Negative contract coverage rejects forbidden normative-skill provenance.
- [ ] Actual GREEN and full-suite output must be recorded during implementation.
