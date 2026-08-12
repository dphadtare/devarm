# Devarm Purpose and Evolution — Implementation Plan

**Document type:** Implementation plan
**Date:** 2026-08-12
**Status:** complete
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☑ clarify ☑ plan ☑ tasks ☑ analyze ☑ implement ▶ review ☐ finish ☐
**Phase:** plan
**Feature/change:** Devarm purpose and evolution
**Design:** [`docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md)
**Specification:** [`docs/specs/devarm-purpose-and-evolution/spec.md`](spec.md)
**Rule inventory:** [`docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md#repository-rule-inventory)
**Tasks:** [`tasks.md`](tasks.md)
**Analysis:** [`analysis.md`](analysis.md)
**Target repository:** `/Users/dphadatare/vhosts/devarm`
**Target branch:** `001-devarm-purpose-evolution`
**Last session note:** T001–T016 and the devarm-analyze re-gate are complete on the feature branch; the next phase is review.
**Last verification:** 2026-08-13 — 85 tests passed; design/spec/plan/tasks/analysis validator checks returned `valid: true`; `git diff --check` passed.
**Open assumptions / risks:** No unresolved plan-level assumptions; validator, analysis, clarify, source-rule, and metadata contracts are recorded below. Review findings F1–F3 and F5 require remediation before finish.
**Next gate:** `devarm-implement` to address review findings.
**Related artifacts:** `design.md`, `spec.md`, `tasks.md`, `analysis.md`, and `findings.md`.

## 1. Implementation objective

Add a small, optional artifact-validation capability to devarm and wire the native phase skills
and templates to use it. The result must make the existing method's metadata, rule applicability,
Decision Ledger, handoff, and verification contracts explicit without turning devarm into a
required runtime, CLI, service, database, or framework-specific product.

The implementation is a method change in the devarm repository. It does not change a target
application's runtime behavior, add persistence, or perform Git lifecycle actions.

## 2. Scope and requirement coverage

| Specification requirements | Plan coverage |
|---|---|
| FR-001–FR-004: classification, track selection, upgrade, repository/branch identity | T006, T007, T009 |
| FR-005–FR-009: rule discovery, precedence, conflict visibility, grounding | T005, T006, T007, T009 |
| FR-010–FR-015: canonical artifacts, ledger, approvals, metadata, supersession | T004, T005, T006, T007, T009 |
| FR-016–FR-021: implementation gates, worktree safety, failure/resume, authority | T007, T009 |
| FR-022–FR-025: requirement mapping, evidence, real-seam limits, risk coverage | T004, T007, T009 |
| FR-026–FR-028: deterministic validator behavior | T001, T002, T003, T009 |
| FR-029–FR-032: portability, adapters, retro evidence | T007, T008, T009 |

Every requirement group has a failing-test or wording-lock task before the implementation task
that can violate it. `tasks.md` is the sole executable task source; the coarse groups below map to
its detailed T001–T016 sequence and must not be maintained as a second hand-edited task list.

## 3. File-structure map

### New files

| File | Single responsibility | Budget |
|---|---|---:|
| `templates/artifact-metadata.md` | Canonical metadata fields and allowed phase statuses/pipeline notation | ≤120 lines |
| `templates/rule-inventory.md` | Canonical repository-rule applicability table and conflict disposition format | ≤120 lines |
| `templates/spec-doc.md` | Native fallback specification structure used when `.specify/` is absent | ≤240 lines |
| `templates/plan-doc.md` | Native fallback implementation-plan structure, including file map and seam contracts | ≤260 lines |
| `templates/tasks-doc.md` | Native tests-first task-list structure and self-check contract | ≤220 lines |
| `templates/analysis-doc.md` | Native analyze-report structure, findings table, and Pass 3 handoff contract | ≤220 lines |
| `scripts/validate_devarm_artifacts.py` | Optional, read-only validator for artifact structure and deterministic gate conditions | ≤500 lines |
| `tests/test_validate_devarm_artifacts.py` | Behavioral tests for validator results, failure modes, output stability, and exit codes | ≤500 lines |
| `tests/test_method_contracts.py` | Wording-lock tests for templates, skills, metadata, rule inventory, and handoff references | ≤400 lines |

### Existing files to modify

| File | Single responsibility of the change | Change budget |
|---|---|---:|
| `AGENTS.md` | Describe the common artifact contract, rule-inventory precedence, and optional validator gate | ≤40 added lines |
| `README.md` | Explain the artifact contract, optional validation, and native fallback templates | ≤35 added lines |
| `templates/design-doc.md` | Add common metadata and rule-inventory sections to new designs | ≤25 added lines |
| `skills/devarm-brainstorm/SKILL.md` | Require repository/branch metadata, rule inventory, and draft validation | ≤35 added lines |
| `skills/devarm-ground/SKILL.md` | Make rule inventory structured and validate grounding handoff | ≤35 added lines |
| `skills/devarm-spec/SKILL.md` | Use the native spec template and validate specification handoff | ≤30 added lines |
| `skills/devarm-clarify/SKILL.md` | Preserve the native ambiguity gate while validating the clarified spec handoff | ≤30 added lines |
| `skills/devarm-plan/SKILL.md` | Use the native plan template, define the validator seam, and validate plan handoff | ≤35 added lines |
| `skills/devarm-tasks/SKILL.md` | Require metadata, requirement/ledger mapping, and task-artifact validation | ≤30 added lines |
| `skills/devarm-analyze/SKILL.md` | Run deterministic artifact checks before analysis passes and record results | ≤25 added lines |
| `skills/devarm-implement/SKILL.md` | Revalidate the governing artifacts before coding and at checkpoints | ≤25 added lines |
| `skills/devarm-review/SKILL.md` | Include artifact/rule/verification validator results in review evidence | ≤25 added lines |
| `skills/devarm-finish/SKILL.md` | Require the validator and current evidence before integration options | ≤20 added lines |
| `skills/devarm-retro/SKILL.md` | Require method-inventory and evidence links for method improvements | ≤20 added lines |
| `USER_GUIDE.md` | Keep the operator-facing pipeline and phase inventory aligned with the native method | ≤20 added lines |
| `docs/design/2026-08-12-devarm-purpose-and-evolution-design.md` | Add target metadata, canonical rule inventory, and plan-resolved implementation rows | ≤35 added lines |
| `docs/specs/devarm-purpose-and-evolution/spec.md` | Link the canonical rule inventory and plan artifact | ≤10 added lines |
| `docs/specs/devarm-purpose-and-evolution/analysis.md` | Persist current-code findings and Pass 3 decisions for this change | ≤260 lines |

`install.sh` is intentionally not modified. The validator is optional and repository-local; the
skills remain usable when only the symlinked `SKILL.md` files are installed.

## 4. Technical context

### Source of truth

The governing design, specification, plan, tasks, findings, and verification artifacts remain
repository-local. The design document remains the canonical home of the Decision Ledger. Downstream
artifacts link to it and record only phase-specific decisions or rule deltas.

### Artifact metadata contract

Every new or resumed artifact uses structured Markdown metadata with these fields:

```text
Document type
Date
Status
Phase
Feature/change
Track
Pipeline
Target repository
Target branch
Last session note
Last verification
Open assumptions / risks
Next gate
Related artifacts
Design or governing artifact link
Rule inventory link
Analysis/findings artifact link
```

Allowed statuses are `draft`, `awaiting approval`, `in progress`, `blocked`, `partially
completed`, `failed`, and `complete`. A phase may not claim `complete` when its predecessor is
not complete or when the artifact has an unresolved blocking issue.

### Rule inventory contract

The design carries the canonical inventory. Each row contains:

```text
ID | Source | Scope | Applies | Precedence | Enforcement phase | Evidence | Conflict/disposition
```

Downstream artifacts link to that inventory and may add a phase-specific row only when the phase
discovers a new applicable instruction or conflict. The target repository's rule wins over a
devarm default; an intent-affecting conflict is surfaced for the developer.

### Validator contract

`scripts/validate_devarm_artifacts.py` is an optional standard-library-only helper. It is not
imported by the skills and does not require network access or installation into target projects.

Invocation:

```bash
python3 scripts/validate_devarm_artifacts.py \
  --artifact docs/specs/devarm-purpose-and-evolution/spec.md \
  --kind spec \
  --format json
```

The validator reads one artifact and emits stable JSON or human-readable output. Its result shape
is:

```json
{
  "artifact": "docs/specs/devarm-purpose-and-evolution/spec.md",
  "kind": "spec",
  "valid": true,
  "issues": []
}
```

Each issue has `code`, `severity`, `line`, and `message`. `error` issues make a required gate
fail; `warning` issues are reported without pretending to be resolved. Exit code `0` means valid,
`1` means validation errors, and `2` means invalid invocation or validator failure. Issues are
sorted by source line, code, severity, and message so repeated validation is deterministic.

The first validator set checks:

1. Required metadata fields and allowed status values.
2. Pipeline marker and expected phase handoff.
3. Required headings for `design`, `spec`, `plan`, `tasks`, and `analysis` artifacts.
4. Non-empty Decision Ledger owner, evidence, tier, and status cells.
5. Rule-inventory presence or downstream inventory link.
6. Requirement-to-scenario/verification traceability in specifications and plans.
7. Findings and Pass 3 handoff fields in analysis artifacts.
8. No unresolved placeholders in artifacts claiming a completed gate.
9. No completion claim without a verification record.

The validator does not choose design alternatives, infer approval from silence, inspect application
runtime behavior, replace test execution, or mutate artifacts.

### Testing

The repository currently has no `.specify/` directory, no project test runner, and no applicable
`.cursor/rules/` directory. The validator and contract tests use the Python standard library:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Markdown-only skill/template changes are protected by wording-lock tests in
`tests/test_method_contracts.py`, while validator behavior is protected by behavioral tests in
`tests/test_validate_devarm_artifacts.py`. The implementation must also run:

```bash
python3 scripts/validate_devarm_artifacts.py \
  --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md \
  --kind design --format json
python3 scripts/validate_devarm_artifacts.py \
  --artifact docs/specs/devarm-purpose-and-evolution/spec.md \
  --kind spec --format json
python3 scripts/validate_devarm_artifacts.py \
  --artifact docs/specs/devarm-purpose-and-evolution/plan.md \
  --kind plan --format json
python3 scripts/validate_devarm_artifacts.py \
  --artifact docs/specs/devarm-purpose-and-evolution/analysis.md \
  --kind analysis --format json
git diff --check
```

No external service, database, migration, branch publish, or remote Git layout seam is involved.

## 5. Integration seams and contracts

### Seam S1 — phase skill to artifact validator

- **Call site:** Each phase skill's gate section invokes the optional helper after writing or
  updating its artifact; the exact wording is added to the skills listed in the file map.
  Implement/review/finish validate their governing artifacts rather than adding a separate runtime
  state input.
- **Input:** Artifact path and artifact kind. The expected phase is derived from the kind map;
  repository root and expected next phase are not separate interface inputs.
- **Output:** Deterministic validation result with errors/warnings and exit status.
- **Idempotency/replay:** Read-only; repeated runs over unchanged input produce identical output and
  no duplicate state.
- **Failure posture:** A validator error blocks the phase handoff; an unavailable optional helper
  is reported as a validation limitation and the skill's manual checklist remains authoritative.
- **Shared context:** None; the validator reads files and returns a value. It does not own phase
  status writes.
- **Test target:** Invoke the CLI as a subprocess from
  `tests/test_validate_devarm_artifacts.py`; no import-site patching is needed.

### Seam S2 — repository instructions to rule inventory

- **Call site:** Brainstorm discovers instructions; ground resolves applicability and records the
  canonical inventory; plan/review consume it.
- **Input:** Existing target-repository instruction files and devarm defaults.
- **Output:** Structured inventory rows and conflict dispositions in the governing design artifact.
- **Idempotency/replay:** Re-reading the same files produces the same source set; new or changed
  files create a new evidence event rather than silently rewriting a prior decision.
- **Failure posture:** Missing or unreadable rule sources are reported; the phase cannot claim a
  complete grounding gate while a material source remains unknown.
- **Shared context:** None; the artifact is the handoff carrier.
- **Test target:** `tests/test_method_contracts.py` checks the required inventory headings and
  precedence wording in the skills/templates.

### Seam S3 — artifact validator to phase gate

- **Call site:** Gate completion sections in brainstorm, ground, spec, clarify, plan, tasks,
  analyze, implement, review, and finish skills.
- **Input:** Validator result plus human judgment and required evidence.
- **Output:** A gate report that distinguishes deterministic failure from judgment-required review.
- **Idempotency/replay:** No mutation; gate status changes only when the agent updates the artifact.
- **Failure posture:** Blocking errors stop handoff; warnings and unavailable optional tooling are
  recorded as limitations.
- **Shared context:** None.
- **Test target:** `tests/test_method_contracts.py` verifies every listed skill has the same
  fail/record/handoff wording, avoiding one phase silently bypassing the contract.

### Out-of-scope seam checks

- No database or persistence consumer audit is needed beyond the Markdown artifact chain.
- No Git mirror/worktree fixture is needed because the implementation does not fetch, checkout,
  publish, merge, or reuse a remote branch.
- No change-set pipeline audit is needed because no production change type is introduced.
- No repair-retry counter or re-entrant application loop is touched.
- No application settings binding or external API client is added.

## 6. Phase-status transition table

This feature formalizes artifact status but does not create a scheduler or multi-actor runtime
state machine. The following table makes every supported resume/re-entry path explicit. Artifact
status is owned by the phase skill writing the artifact; validators only report.

| Current status | Incoming event | Resulting status | Side effects | Owner / preserving rule |
|---|---|---|---|---|
| `draft` | Phase begins work | `in progress` | Record current phase and session note | Phase skill; no artifact deletion |
| `draft` | Phase is presented for approval | `awaiting approval` | Preserve draft and open decisions | Brainstorm/spec skill; no implementation allowed |
| `awaiting approval` | Developer approves | `in progress` | Record approval and next gate | Phase skill; approval cannot be inferred |
| `awaiting approval` | Developer requests changes | `draft` | Preserve feedback and revise artifact | Phase skill; prior decision is not silently overwritten |
| `in progress` | Gate evidence passes | `complete` | Record verification, handoff, and next phase | Phase skill; predecessor is now eligible |
| `in progress` | Work stops after partial output | `partially completed` | Preserve output and record remaining work | Phase skill; later gates reject it as complete |
| `in progress` | Deterministic or runtime failure | `failed` | Preserve evidence and failure cause | Phase skill/debug; no speculative fix stacking |
| `in progress` | Material blocker or unresolved design decision | `blocked` | Record blocker and owner/action needed | Phase skill; implementation remains prohibited |
| `partially completed` | Resume after repository revalidation | `in progress` | Re-check branch, rules, artifacts, and diff | Resuming phase; preserve completed work |
| `failed` | Root cause repaired and resume authorized | `in progress` | Re-run the failing check from current state | Debug/phase skill; do not erase failure evidence |
| `blocked` | Blocker resolved and required decision recorded | `in progress` | Re-run the blocked gate | Phase skill; unresolved intent remains blocking |
| `complete` | No new event | `complete` | No mutation | Phase skill; terminal/preserving |
| `complete` | New evidence contradicts the artifact | `blocked` | Record drift and require revalidation or superseding decision | Analyze/implement; never silently diverge |

## 7. Plan-level implementation decisions

These are implementation-level choices consistent with the approved design; they do not change
the product scope or user-visible intent. They must be added to the design Decision Ledger before
implementation begins so later tasks have one durable decision home.

| ID | Decision | Alternatives rejected | Rationale/evidence | Owner | Tier |
|---|---|---|---|---|---|
| D21 | Use structured Markdown headings and bold metadata fields, not front matter | YAML front matter; separate database state | Preserves tool portability and matches existing `templates/design-doc.md:1-12`; no YAML parser is required | agent | impl |
| D22 | Keep the canonical rule inventory in the design and link downstream artifacts to it, adding only phase-specific deltas | Duplicate the full table in every artifact; global rule database | Avoids drift while satisfying the design's rule-inventory component and one-canonical-planning-system rule | agent | impl |
| D23 | Implement the optional validator as a standard-library-only Python script under `scripts/` | Mandatory CLI package; shell-only parser; hosted service | Supports deterministic parsing/tests without adding dependencies or making Python a devarm runtime requirement | agent | impl |
| D24 | Treat validator errors as blocking and warnings as reported limitations | Make all findings blocking; make all findings advisory | Separates deterministic safety failures from unavailable optional tooling and judgment-required decisions | agent | impl |
| D25 | Do not modify `install.sh` to distribute the validator | Install the helper into every target project; require global executable discovery | The design allows repository-local optional validators and `install.sh:42-75` currently installs only skills; preserving installation compatibility reduces blast radius | agent | impl |

## 8. Implementation tasks

Tasks are intentionally ordered red → green → refactor/contract wiring → verification. The task
IDs are stable references for `devarm-tasks`, findings, and later review.

### T001 — Establish the standard-library test harness `[P]`

**Files:** `tests/__init__.py`, `tests/test_validate_devarm_artifacts.py`,
`tests/test_method_contracts.py`

Create the test package and a test helper that can invoke the planned validator by subprocess
without importing a missing module. Add a first assertion that the validator entrypoint exists;
the test must fail with an assertion (not an import error) before `scripts/validate_devarm_artifacts.py`
exists. Add the test command to the plan checkpoint:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

**Expected RED:** the entrypoint-existence assertion fails. No production implementation is added
in this task.

### T002 — Define validator behavior tests before the validator `[P]`

**File:** `tests/test_validate_devarm_artifacts.py`

Add complete and invalid in-memory artifact fixtures written to `TemporaryDirectory`, then invoke
the CLI with `--artifact`, `--kind`, and `--format`. Cover:

1. Complete design/spec/plan/tasks/analysis artifacts return exit `0` and `valid: true`.
2. Missing metadata returns exit `1` with `MISSING_METADATA` and a line number.
3. Invalid status or pipeline handoff returns `INVALID_STATUS` or `INVALID_PIPELINE`.
4. Empty ledger owner/evidence/status returns distinct deterministic issues.
5. Missing rule inventory/link and missing requirement traceability are reported for the relevant
   artifact kinds.
6. A completed artifact containing an unresolved placeholder returns a blocking issue.
7. A partial/blocked artifact is not treated as complete.
8. `--format json` output is valid JSON, issue ordering is stable, and repeated calls match.
9. Invalid `--kind`/missing artifact returns exit `2` with a useful invocation error.
10. Analysis validation uses only artifact path and kind; expected phase is derived by the kind map.

The test helper must normalize temporary paths before comparing repeated output so only validator
ordering and content are under test.

**Expected RED:** after T001 the tests fail at the missing validator entrypoint assertion; once the
entrypoint exists but has no behavior, the behavior assertions fail with expected mismatches.

### T003 — Implement the deterministic validator `[P1]`

**File:** `scripts/validate_devarm_artifacts.py`

Implement the following concrete interface:

```python
@dataclass(frozen=True)
class Issue:
    code: str
    severity: str
    line: Optional[int]
    message: str

def validate_artifact(path: Path, kind: str) -> List[Issue]:
    """Read one artifact without mutation and return sorted validation issues."""
```

Implement:

- `argparse` options `--artifact`, `--kind {design,spec,plan,tasks,analysis,review}`, and
  `--format {text,json}`.
- Safe UTF-8 file reading and a clear exit `2` for invalid invocation/read failures.
- Line-aware metadata parsing for the common fields and allowed statuses.
- Per-kind required-section maps.
- Decision Ledger row checks that ignore the header/separator but reject empty required cells.
- Rule-inventory/link checks.
- Requirement-traceability checks for `spec` and `plan` artifacts.
- Completed-gate placeholder and verification-record checks.
- Stable issue sorting and JSON serialization.

Run the focused RED suite, then the full suite:

```bash
python3 -m unittest tests.test_validate_devarm_artifacts -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

**Expected GREEN:** all T002 behavior tests pass, with no third-party import or network access.

### T004 — Lock the common artifact and rule-inventory contracts `[P1]`

**Files:** `templates/artifact-metadata.md`, `templates/rule-inventory.md`,
`templates/design-doc.md`, `templates/spec-doc.md`, `templates/plan-doc.md`,
`templates/tasks-doc.md`, `templates/analysis-doc.md`

Write the reusable templates with exact headings and metadata used by T003. `spec-doc.md` must
include overview, scope, prioritized stories, Gherkin scenarios, requirements, coverage matrix,
success criteria, dependencies, assumptions, clarifications, and quality checklist. `plan-doc.md`
must include file structure, technical context, data/contracts, integration seams, status
transitions when relevant, task plan, verification, and self-review. `tasks-doc.md` must include
setup, foundational work, story groups, polish, and tests-first self-checks. `analysis-doc.md` must
include Pass 1/2 evidence, findings, Pass 3 decisions, and the analyze gate result.

Add wording-lock tests to `tests/test_method_contracts.py` before editing these templates. Assert
the exact metadata labels, allowed status list, rule-inventory columns, required template
headings, and validator invocation shape.

**Expected RED:** wording-lock tests fail against the existing templates because the new common
metadata/rule-inventory/spec/plan/tasks contracts are absent.

**Expected GREEN:** after the template edits, run:

```bash
python3 -m unittest tests.test_method_contracts -v
```

### T005 — Add rule inventory and artifact metadata to the current planning artifacts `[P1]`

**Files:** `docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`,
`docs/specs/devarm-purpose-and-evolution/spec.md`,
`docs/specs/devarm-purpose-and-evolution/plan.md`,
`docs/specs/devarm-purpose-and-evolution/tasks.md`,
`docs/specs/devarm-purpose-and-evolution/analysis.md`

Update the current design, specification, plan, tasks, and analysis artifacts to use the common
metadata, link the canonical rule inventory, and record the actual devarm rule sources discovered
during grounding. Add the source-rule adoption matrix and Decision Ledger rows D26–D29 to the
design. Do not bulk-rewrite historical artifacts outside this feature.

Add wording-lock fixture assertions that these current artifacts validate as `design`, `spec`,
`plan`, and `analysis` respectively. Run:

```bash
python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md --kind design --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/spec.md --kind spec --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/analysis.md --kind analysis --format json
```

**Expected GREEN:** all four current artifacts pass with no blocking issues.

### T006 — Wire brainstorm, grounding, specification, and planning handoffs `[P1]`

**Files:** `skills/devarm-brainstorm/SKILL.md`, `skills/devarm-ground/SKILL.md`,
`skills/devarm-spec/SKILL.md`, `skills/devarm-clarify/SKILL.md`,
`skills/devarm-plan/SKILL.md`

First extend `tests/test_method_contracts.py` with wording-lock assertions that these five skills:

- Require active repository and branch metadata.
- Discover applicable target instructions before acting.
- Use the canonical rule inventory and target-rule precedence.
- Invoke the optional validator or record why it is unavailable.
- Stop the handoff when deterministic blocking errors exist.
- Preserve user approval and unresolved-decision gates.

Then update the skills. `devarm-spec` must reference `templates/spec-doc.md` when `.specify/` is
absent; `devarm-clarify` must preserve the native five-question ambiguity gate and write its
clarifications into `spec.md`; `devarm-plan` must reference `templates/plan-doc.md` and the inline
data/contract sections.
No skill may imply that the optional script is a required runtime dependency.

**Expected RED:** the new skill-contract assertions fail before the skill edits.
**Expected GREEN:** run the contract suite and validate the current design/spec/plan/analysis
artifacts.

### T007 — Wire tasks, analyze, implement, review, finish, and retro handoffs `[P1]`

**Files:** `skills/devarm-tasks/SKILL.md`, `skills/devarm-analyze/SKILL.md`,
`skills/devarm-implement/SKILL.md`, `skills/devarm-review/SKILL.md`,
`skills/devarm-finish/SKILL.md`, `skills/devarm-retro/SKILL.md`

Add wording-lock assertions before editing. Then require:

- `devarm-tasks` to validate metadata, requirement/ledger-to-task mapping, and tests-first order.
- `devarm-analyze` to validate all loaded artifacts before Pass 1 and to record validator results.
- `devarm-implement` to validate the governing design/spec/plan/tasks before coding and after
  course correction, while retaining its existing TDD and current-evidence rules.
- `devarm-review` to include rule inventory, artifact validation, and verification limitations in
  its findings ledger.
- `devarm-finish` to require current artifact validation in addition to fresh full-suite evidence.
- `devarm-retro` to connect method improvements to evidence and record the method inventory.

The skills must retain explicit commit/lifecycle authority and must not turn validator warnings
into silent approval.

**Expected RED:** contract assertions fail before these six skills contain the new handoff rules.
**Expected GREEN:** run the contract suite and the validator against all current artifacts.

### T008 — Update the portable method documentation `[P]`

**Files:** `AGENTS.md`, `README.md`, `USER_GUIDE.md`

Add a concise artifact-contract section covering repository/branch identity, status, pipeline,
last verification, assumptions, next gate, and rule-inventory precedence. Document that the
validator is optional, read-only, standard-library-only, deterministic, and never a replacement
for human judgment or target-repository rules. Update the layout and workflow tables to include
native fallback templates and the validator test command.

Update the pipeline and phase inventories to include `devarm-clarify`, and add wording-lock tests
before the documentation edits, then run:

```bash
python3 -m unittest tests.test_method_contracts -v
git diff --check
```

Keep `AGENTS.md` within its +40-line budget; place detailed validator behavior in the script and
template rather than growing the portable brain into a second implementation manual.

### T009 — Run the full contract, validator, and phase-handoff verification `[P1]`

**Files:** `tests/test_validate_devarm_artifacts.py`, `tests/test_method_contracts.py`,
`docs/specs/devarm-purpose-and-evolution/analysis.md`

Add final integration assertions for:

- The current design, spec, plan, and analysis artifacts validating cleanly.
- Every native phase skill named in the design having the common artifact/rule/validator handoff.
- No skill describing the validator as mandatory installation or as an autonomous approval path.
- Repeated JSON validation producing identical normalized output.
- A deliberately incomplete fixture stopping the handoff with exit `1`.
- An adapter-present/adapter-absent method inventory preserving the same native gate wording.

Run the exact evidence set:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md --kind design --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/spec.md --kind spec --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
git diff --check
```

**Acceptance:** all tests pass; the four current artifacts return `valid: true`; no network or
external service is required; and the validator's output is stable.

## 9. Self-review before task generation

- **Spec coverage:** FR-001–FR-032 are mapped in Section 2; `devarm-tasks` must create named
  acceptance tasks for each individual requirement and each D1–D34 ledger decision.
- **File structure:** every planned file has one responsibility and a line budget; `AGENTS.md`
  and each skill receive only thin contract wiring.
- **Integration seams:** S1–S3 specify inputs, outputs, replay, failure, shared state, and test
  targets; the Git/change-set/retry/migration/settings seams are explicitly not applicable.
- **State semantics:** the artifact status transition table covers start, approval, revision,
  pass, partial stop, failure, blocking, resume, drift, and terminal behavior.
- **TDD:** T001/T002 precede validator implementation; T004/T006/T007/T008 wording-lock tests
  precede template, skill, and documentation edits.
- **Compatibility:** no existing skill name, artifact type, installation destination, commit rule,
  or historical artifact is removed or bulk-rewritten.
- **Placeholder scan:** this plan contains concrete paths, interfaces, commands, expected results,
  and decisions; no unresolved implementation placeholder remains.
- **Clarification status:** the specification has no material clarification markers; the remaining
  choices are resolved as D21–D34 implementation decisions and have been surfaced at the analyze
  gate before coding.

**Plan gate result:** PASS; `tasks.md` is generated and the required pre-implementation
`devarm-analyze` gate is clean; implementation starts only after its branch/baseline preconditions.
