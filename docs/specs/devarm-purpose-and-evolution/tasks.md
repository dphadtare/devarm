# Devarm Purpose and Evolution — Tasks

**Document type:** Tests-first implementation tasks
**Date:** 2026-08-12
**Status:** complete
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☑ clarify ☑ plan ☑ tasks ☑ analyze ☑ implement ▶ review ☐ finish ☐
**Phase:** tasks
**Feature/change:** Devarm purpose and evolution
**Design:** [`docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md)
**Specification:** [`docs/specs/devarm-purpose-and-evolution/spec.md`](spec.md)
**Plan:** [`docs/specs/devarm-purpose-and-evolution/plan.md`](plan.md)
**Rule inventory:** [`docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md#repository-rule-inventory)
**Analysis:** [`analysis.md`](analysis.md)
**Target repository:** `/Users/dphadatare/vhosts/devarm`
**Target branch:** `001-devarm-purpose-evolution`
**Last session note:** T001–T016 and the devarm-analyze re-gate are complete on the feature branch; the next phase is review.
**Last verification:** 2026-08-13 — 85 tests passed; design/spec/plan/tasks/analysis validator checks returned `valid: true`; `git diff --check` passed.
**Open assumptions / risks:** No unresolved task-level assumptions; review findings F1–F3 and F5 require remediation before finish.
**Next gate:** `devarm-implement` to address review findings.
**Related artifacts:** `design.md`, `spec.md`, `plan.md`, `analysis.md`, and `findings.md`.

## 1. Execution contract

### TDD rule

For every implementation task below:

1. Complete its preceding RED task.
2. Run the named test command and observe the expected behavioral failure.
3. Make only the implementation change needed for that task.
4. Re-run the focused test until GREEN.
5. Run the listed regression command and report the actual output.
6. Stop at the checkpoint; do not commit unless explicitly authorized.

A test that fails with an import error, syntax error, missing fixture, or bad command is not a RED
test. Repair the test until it fails because the intended behavior is absent.

### MVP slice

The MVP is the deterministic validator plus the common artifact/rule contracts and native gate
wiring: T001–T012 and T015. It must validate the current design, specification, and plan, reject
incomplete artifacts, preserve human approval gates, and remain usable without network access or
an installed external framework. T013–T014 complete the adapter/retro documentation and final
cross-phase proof but are still required before implementation is considered complete.

### Parallelism

`[P]` is used only where tasks touch different files and have no incomplete dependency. Tasks
touching `tests/test_method_contracts.py` are deliberately sequential.

## 2. Setup and baseline

### T001 [Setup] Establish the standard-library test harness — `tests/__init__.py`

**Requirements/decisions:** FR-029, FR-028; D1, D8, D17.

Create `tests/__init__.py` and a minimal test-discovery smoke test in
`tests/test_method_contracts.py` that executes without third-party dependencies. Confirm the
repository baseline before adding behavior:

```bash
python3 --version
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

**Expected result:** Python is available, discovery runs, and the new smoke test passes. If the
environment lacks Python, stop and record the environment blocker; do not replace the planned
standard-library test strategy.

**Checkpoint:** report the Python version, baseline test result, and unchanged unrelated worktree
state.

## 3. Foundational validator behavior — P2 Validate deterministic safety conditions

### T002 [P] [P2] Write RED validator contract tests — `tests/test_validate_devarm_artifacts.py`

**Requirements/decisions:** FR-026–FR-029; D1, D8, D17, D23, D24.

Add subprocess-based tests using `tempfile.TemporaryDirectory` and only the standard library.
The tests must invoke the planned command rather than import the not-yet-created module. Add
named tests for:

- `test_missing_entrypoint_fails_as_behavioral_assertion`.
- `test_valid_design_spec_plan_tasks_and_analysis_return_zero_json`.
- `test_missing_metadata_returns_error_with_line`.
- `test_invalid_status_and_pipeline_return_distinct_errors`.
- `test_empty_ledger_owner_evidence_tier_and_status_are_blocking`.
- `test_missing_rule_inventory_or_link_is_blocking`.
- `test_missing_requirement_traceability_is_blocking_for_spec_and_plan`.
- `test_completed_artifact_with_placeholder_or_missing_verification_is_blocking`.
- `test_partial_blocked_and_failed_artifacts_cannot_pass_as_complete`.
- `test_validator_errors_block_and_warnings_are_visible`.
- `test_validator_does_not_replace_human_judgment`.
- `test_invalid_kind_or_missing_file_returns_invocation_failure`.
- `test_analysis_kind_uses_path_and_kind_without_expected_phase_argument`.
- `test_json_issue_order_is_stable_across_repeated_runs`.
- `test_validator_does_not_require_network_or_optional_packages`.

Use fixture text that includes the exact metadata, required headings, rule-inventory link, ledger,
requirements, scenarios, findings, Pass 3 status, and verification sections specified in `plan.md`.
Normalize only the
temporary artifact path before comparing repeated JSON output.

Run:

```bash
python3 -m unittest tests.test_validate_devarm_artifacts -v
```

**Expected RED:** the first failure is the missing validator entrypoint assertion; after a stub
entrypoint exists, behavior tests fail with the named missing validation codes, not import errors.

### T003 [P] [P2] Implement the deterministic validator — `scripts/validate_devarm_artifacts.py`

**Depends on:** T002 RED evidence.
**Requirements/decisions:** FR-026–FR-029; D1, D8, D17, D23, D24.

Implement the planned standard-library-only CLI and pure function:

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

Required behavior:

- Parse `--artifact`, `--kind {design,spec,plan,tasks,analysis,review}`, and `--format {text,json}`.
- Return exit `0` only when no blocking errors exist; return `1` for validation errors; return `2`
  for invalid invocation or unreadable input.
- Parse and validate the common metadata fields and allowed statuses.
- Validate per-kind required headings and expected pipeline handoff markers.
- Validate non-empty Decision Ledger owner, evidence, tier, and status cells.
- Validate the rule-inventory table or a valid downstream inventory link.
- Validate requirement-to-scenario and requirement-to-verification traceability for specs/plans.
- Reject placeholders and missing verification evidence when an artifact claims completion.
- Emit issues with `code`, `severity`, `line`, and `message` in stable sort order.
- Never mutate the artifact, access the network, import optional packages, or infer developer
  approval from silence.

Run:

```bash
python3 -m unittest tests.test_validate_devarm_artifacts -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

**Expected GREEN:** all T002 tests pass; repeated JSON output is identical after path
normalization; no external dependency is imported.

**Checkpoint:** report the validator interface, exit-code behavior, focused tests, and full test
discovery output.

## 4. Common artifact contracts — P1 Complete a grounded repository change

### T004 [P] [P1] Write RED wording-lock tests for templates — `tests/test_method_contracts.py`

**Depends on:** T001.
**Requirements/decisions:** FR-010–FR-015, FR-022, FR-025; D4, D9, D12, D19, D20, D21, D22.

Add tests that read the template files as text and fail until the common contract exists:

- `test_artifact_metadata_template_locks_fields_and_statuses`.
- `test_artifact_metadata_template_locks_phase_verification_risks_next_gate_and_related_artifacts`.
- `test_rule_inventory_template_locks_columns_and_precedence`.
- `test_design_template_links_rule_inventory_and_preserves_ledger`.
- `test_native_spec_plan_tasks_and_analysis_templates_have_required_sections`.
- `test_templates_keep_repository_local_artifacts_as_source_of_truth`.
- `test_templates_do_not_require_front_matter_or_a_database`.

Assert exact labels for repository, branch, status, pipeline, last verification, assumptions,
next gate, related artifacts, rule inventory, and the allowed status values. Assert the canonical
rule-inventory columns: `ID`, `Source`, `Scope`, `Applies`, `Precedence`, `Enforcement phase`,
`Evidence`, and `Conflict/disposition`.

Run:

```bash
python3 -m unittest tests.test_method_contracts.MethodContractTests.test_artifact_metadata_template_locks_fields_and_statuses -v
```

**Expected RED:** assertions fail because the new templates/sections are not yet present.

### T005 [P] [P1] Implement common artifact templates — `templates/artifact-metadata.md`

**Depends on:** T004 RED evidence.
**Requirements/decisions:** FR-010–FR-015, FR-022, FR-025; D4, D9, D19, D20, D21, D22.

Create:

- `templates/artifact-metadata.md` with the exact common metadata contract and allowed status
  values.
- `templates/rule-inventory.md` with the canonical row format and target-rule precedence.
- `templates/spec-doc.md` with the native fallback specification sections.
- `templates/plan-doc.md` with file map, technical context, contracts, seams, status transitions,
  tasks, verification, and self-review.
- `templates/tasks-doc.md` with setup, foundational work, story groups, polish, and tests-first
  self-checks.
- `templates/analysis-doc.md` with findings, Pass 1/2 evidence, Pass 3 decisions, and the analyze
  gate result.

Update `templates/design-doc.md` to include the common metadata and rule-inventory link/section
without removing the existing grounding or Decision Ledger sections. Keep each new template under
its plan budget.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
git diff --check
```

**Expected GREEN:** all T004 wording-lock tests pass and no formatting errors are reported.

### T006 [P1] Reconcile current artifacts with the common contract — exact current artifacts

**Depends on:** T003 and T005 GREEN.
**Files:** `docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`,
`docs/specs/devarm-purpose-and-evolution/spec.md`,
`docs/specs/devarm-purpose-and-evolution/plan.md`,
`docs/specs/devarm-purpose-and-evolution/tasks.md`,
`docs/specs/devarm-purpose-and-evolution/analysis.md`.
**Requirements/decisions:** FR-004–FR-015, FR-022, FR-025; D4, D5, D9, D19–D22, D26, D28.

Add a fixture/characterization test in `tests/test_method_contracts.py` named
`test_current_design_spec_and_plan_have_metadata_and_rule_inventory_links`. It must validate:

- Repository `/Users/dphadatare/vhosts/devarm` and branch `main` are present.
- The design has the canonical `## Repository Rule Inventory` section with R1–R7.
- The spec and plan link to the design inventory.
- The design contains D21–D34 and the grounded evidence remains intact.
- The four artifacts identify their next phase and do not claim an unearned implementation
  completion state.
- The analysis artifact exists, links the governing artifacts, and preserves the blocked-to-clean
  analyze handoff without being mistaken for implementation completion.

Run the test before any artifact correction and record whether it is a characterization pass or a
RED failure. If it fails, make the narrowest correction to the four current artifacts; do not
rewrite historical artifacts or duplicate the inventory downstream. Then run:

```bash
python3 -m unittest tests.test_method_contracts -v
python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md --kind design --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/spec.md --kind spec --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
```

**Expected GREEN:** all four current artifacts validate successfully and the existing grounding
evidence/decision records remain present.

## 5. P1 gate wiring — Complete a grounded repository change

### T007 [P1] Write RED tests for early-phase handoffs — `tests/test_method_contracts.py`

**Depends on:** T005.
**Requirements/decisions:** FR-001–FR-016, FR-022, FR-025; D1–D13, D19–D22, D26–D29.

Add wording-lock tests before editing the early phase skills:

- `test_brainstorm_classifies_consequential_existing_repo_workflow`.
- `test_brainstorm_requires_active_repo_branch_rule_inventory_and_track`.
- `test_ground_requires_current_rule_inventory_and_grounded_handoff`.
- `test_clarify_requires_native_spec_handoff_and_optional_adapter_boundary`.
- `test_target_rule_conflict_requires_visible_disposition`.
- `test_ground_requires_boundary_consumer_and_runtime_contract_audit`.
- `test_spec_requires_native_fallback_template_and_quality_gate`.
- `test_plan_requires_file_map_seams_and_validator_handoff`.
- `test_early_phase_rules_preserve_approval_and_unanswered_decision_blocks`.
- `test_quick_track_upgrade_condition_is_locked`.
- `test_quick_track_is_exactly_three_changed_files_or_fewer`.
- `test_decision_protocol_requires_recommendation_and_one_question`.
- `test_superseded_decision_requires_dependent_artifact_recheck`.
- `test_target_rules_precede_devarm_defaults`.
- `test_no_required_external_framework_or_validator_installation_is_stated`.
- `test_source_rule_adoption_matrix_preserves_target_specific_rules`.

Each test must assert the complete instruction sentence or stable required phrase, not merely that
the skill file contains the word `validator`. Run:

```bash
python3 -m unittest tests.test_method_contracts -v
```

**Expected RED:** the new assertions fail against the current early-phase skill text.

### T008 [P1] Wire early-phase artifact and rule gates — exact skill files

**Depends on:** T007 RED evidence.
**Files:** `skills/devarm-brainstorm/SKILL.md`, `skills/devarm-ground/SKILL.md`,
`skills/devarm-spec/SKILL.md`, `skills/devarm-clarify/SKILL.md`, `skills/devarm-plan/SKILL.md`.
**Requirements/decisions:** FR-001–FR-016, FR-022, FR-025; D1–D13, D19–D22.

Update the skills to require:

- Active repository and branch in the artifact metadata.
- Target-rule discovery and the canonical rule-inventory link/table.
- Target-rule precedence and visible conflict disposition.
- Optional validator invocation or a recorded unavailable-tool limitation.
- Blocking deterministic errors before handoff, while retaining human judgment gates.
- Native fallback templates when `.specify/` is absent.
- Clarify's native ambiguity gate and clarified-spec handoff, without requiring Spec Kit.
- Existing design approval, grounding, clarification, and no-silent-approval semantics.

Preserve the existing quick/standard track boundary, grounding-before-approval order, and
one-question recommendation protocol. Do not make the validator an installed skill or a required
runtime dependency.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
```

**Expected GREEN:** T007 passes, the plan validates, and existing gate wording remains intact.

### T009 [P1] Write RED tests for late-phase safety handoffs — `tests/test_method_contracts.py`

**Depends on:** T008 GREEN.
**Requirements/decisions:** FR-016–FR-025, FR-030–FR-032; D3, D6, D10–D18, D23–D29.

Add tests before editing the late-phase skills:

- `test_tasks_requires_decision_to_test_and_requirement_mapping`.
- `test_analyze_requires_artifact_validation_before_passes`.
- `test_implement_requires_clean_analyze_and_current_artifact_revalidation`.
- `test_review_requires_rule_inventory_and_real_seam_limitations`.
- `test_finish_requires_fresh_evidence_and_artifact_validation`.
- `test_retro_requires_motivating_evidence_and_method_inventory`.
- `test_resume_revalidates_current_repo_rules_artifacts_and_diff`.
- `test_current_evidence_precedes_stale_summary`.
- `test_mocked_seams_require_explicit_limitation`.
- `test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete`.
- `test_dirty_worktree_and_unrelated_change_preservation_are_required`.
- `test_commit_push_merge_delete_reset_and_discard_remain_explicit`.
- `test_adapter_use_cannot_bypass_native_gates`.
- `test_risk_based_quality_coverage_is_preserved`.

The status test must assert the forbidden outcome: a partial, failed, or blocked predecessor is
not eligible for a complete handoff. It must also cover the preserving terminal `complete` state
and the drift-to-`blocked` rule from the plan transition table.

The transition coverage must include named negative/preservation tests for every table path:

- `test_status_transition_draft_to_in_progress_preserves_artifact`.
- `test_status_transition_draft_to_awaiting_approval_blocks_implementation`.
- `test_status_transition_awaiting_approval_requires_explicit_approval`.
- `test_status_transition_awaiting_approval_change_returns_to_draft_preserves_feedback`.
- `test_status_transition_in_progress_complete_requires_evidence`.
- `test_status_transition_in_progress_partial_failed_blocked_preserves_side_effects`.
- `test_status_transition_partial_failed_blocked_resume_returns_in_progress_after_revalidation`.
- `test_status_transition_complete_is_terminal_without_event`.
- `test_status_transition_complete_drift_becomes_blocked`.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
```

**Expected RED:** late-phase contract assertions fail before the skill edits.

### T010 [P1] Wire late-phase safety and evidence gates — exact skill files

**Depends on:** T009 RED evidence.
**Files:** `skills/devarm-tasks/SKILL.md`, `skills/devarm-analyze/SKILL.md`,
`skills/devarm-implement/SKILL.md`, `skills/devarm-review/SKILL.md`,
`skills/devarm-finish/SKILL.md`, `skills/devarm-retro/SKILL.md`.
**Requirements/decisions:** FR-016–FR-025, FR-030–FR-032; D3, D6, D10–D18, D23–D25.

Update the skills so that:

- `devarm-tasks` validates metadata and requirement/ledger-to-task traceability while retaining
  tests-first and safety-invariant rules.
- `devarm-analyze` validates all loaded artifacts before Pass 1 and records validator output.
- `devarm-analyze` persists its findings and Pass 3 decisions in `analysis.md`.
- `devarm-implement` validates the governing artifacts before coding and after course correction,
  while retaining TDD, branch, dirty-worktree, and fresh-evidence rules.
- `devarm-review` records rule inventory, validator output, real-seam limitations, and findings
  status in its durable ledger.
- `devarm-finish` requires current artifact validation in addition to fresh full-suite evidence;
  it retains exactly four lifecycle options and typed discard confirmation.
- `devarm-retro` connects proposed method changes to motivating evidence and method inventory.

Keep validator errors blocking, warnings visible as limitations, and optional-validator absence
explicit. Do not turn a validator result into autonomous approval or lifecycle action.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

**Expected GREEN:** T009 passes; all existing safety and authority wording remains present.

## 6. P2 rule, recovery, and deterministic validation coverage

### T011 [P2] Write RED tests for portable documentation and adapter semantics — `tests/test_method_contracts.py`

**Depends on:** T010 GREEN.
D11, D12, D14–D18, D25–D27.

Add wording-lock tests for:

- `AGENTS.md` artifact metadata, rule precedence, optional validator, authority, and resume model.
- `README.md` method purpose, native pipeline including clarify, fallback templates, validator optionality, and
  portability boundary.
- `USER_GUIDE.md` phase inventory including clarify and analysis artifact behavior.
- Adapter-present and adapter-absent method inventory semantics.
- No required CLI/service/database and no target-project-specific rule leakage.
- Retro evidence and verification requirements.
- Source-rule adoption matrix wording and Adopt/Adapt/Target-only dispositions.
- `test_adapter_present_inventory_records_output_and_reuse`.
- `test_adapter_absent_keeps_native_gates`.
- `test_retro_proposal_requires_motivating_evidence_and_verification`.
- `test_installation_contract_does_not_require_validator_distribution`.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
```

**Expected RED:** documentation and adapter contract assertions fail before documentation edits.

### T012 [P2] Update portable documentation and adapter contract — `AGENTS.md`, `README.md`, `USER_GUIDE.md`

**Depends on:** T011 RED evidence.
D8, D11, D12, D14–D18, D25–D27.

Add concise guidance for:

- Common artifact metadata and canonical rule-inventory precedence.
- Repository-local state and resumable/partial statuses.
- Optional read-only standard-library validator and its blocking-error/warning distinction.
- Human judgment versus deterministic checks.
- Native core versus optional adapters.
- The seven source-rule dispositions and the exact three-file quick-track boundary.
- Evidence requirements and explicit lifecycle authority.

Keep `AGENTS.md` within its plan budget of at most 40 added lines and keep detailed validator
behavior in `scripts/validate_devarm_artifacts.py` and templates. Update `README.md` without
duplicating the full skill instructions.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
git diff --check
```

**Expected GREEN:** T011 passes, documentation remains concise, and no unrelated instructions
are removed.

### T013 [P2] Add final deterministic validator and artifact fixtures — exact test files

**Depends on:** T003, T006, T008, T010, and T012 GREEN.
**Files:** `tests/test_validate_devarm_artifacts.py`, `tests/test_method_contracts.py`.
**Requirements/decisions:** FR-022–FR-028; D1, D9, D10, D14, D16, D17, D18, D21–D24, D28, D29.

Add final integration tests that:

- `test_current_artifact_set_passes_all_native_handoff_checks`.
- `test_incomplete_fixture_blocks_handoff`.
- `test_complete_fixture_requires_verification_record`.
- `test_validator_output_is_not_human_approval`.
- `test_status_fixture_preserves_partial_failed_and_blocked_states`.
- `test_current_analysis_artifact_preserves_findings_until_pass3`.

The tests must also:

- Validate the current design, spec, plan, and analysis artifacts with the actual CLI.
- Confirm every native phase skill named in the design has the common artifact/rule/validator
  handoff wording.
- Confirm no skill describes validator installation as mandatory or validator output as approval.
- Confirm repeated JSON validation is identical after normalizing only the artifact path.
- Confirm a deliberately incomplete fixture returns exit `1` and identifies the blocking issue.
- Confirm partial/failed/blocked status fixtures never pass as completed.
- Confirm a complete fixture requires a verification record.
- Confirm 20 representative phase documents validate within the 10-second SC-008 target.

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md --kind design --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/spec.md --kind spec --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
git diff --check
```

**Expected GREEN:** all tests pass; current artifacts return `valid: true`; incomplete fixtures
return exit `1`; no network or external service is used.

### T014 [P3] Add retro, optional-adapter, and source-rule regression fixtures — `tests/test_method_contracts.py`

**Depends on:** T012.
**Requirements/decisions:** FR-030–FR-032; D11, D17, D18, D26.

Add tests showing that:

- A method inventory records native and external items with `Used?`, artifact/output, and reuse
  columns.
- The source-rule matrix records all seven cited rules and keeps stack-specific rules external.
- An adapter-present path and an adapter-absent path preserve identical native gate requirements.
- A retro proposal names motivating evidence, affected skill/template/validator, and verification.
- No adapter can mark grounding, approval, analyze, verification, or finish complete by itself.

Run:

```bash
python3 -m unittest tests.test_method_contracts -v
```

**Expected GREEN:** the adapter/retro contract is locked without adding a real external adapter.

## 7. Cross-cutting verification and handoff

### T015 [P1] Run the complete task acceptance matrix — exact repository commands

**Depends on:** T013 and T014 GREEN.
**Requirements/decisions:** FR-001–FR-032; D1–D34.

Run the complete evidence set in a clean current turn:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_devarm_artifacts.py --artifact docs/design/2026-08-12-devarm-purpose-and-evolution-design.md --kind design --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/spec.md --kind spec --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/plan.md --kind plan --format json
python3 scripts/validate_devarm_artifacts.py --artifact docs/specs/devarm-purpose-and-evolution/analysis.md --kind analysis --format json
git diff --check
```

Confirm manually from the actual diff:

- No planned file is missing or replaced by a duplicate concept.
- No existing skill name, pipeline order, install destination, or explicit-commit rule regressed.
- `AGENTS.md` gained no more than 40 lines of method guidance.
- Every validator error blocks the appropriate handoff, while warnings and unavailable optional
  tooling remain visible limitations.
- The current design/spec/plan/analysis artifacts are valid and the tasks artifact itself contains no placeholder.
- No commit, push, merge, reset, delete, or discard action was run.

**Expected acceptance:** all tests pass, all four current artifacts validate with `valid: true`,
`git diff --check` passes, and the implementation checkpoint reports changed files and evidence.

### T016 [P1] Record the task checkpoint and prepare analyze handoff — artifact metadata

**Files:** `docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`,
`docs/specs/devarm-purpose-and-evolution/spec.md`,
`docs/specs/devarm-purpose-and-evolution/plan.md`,
`docs/specs/devarm-purpose-and-evolution/tasks.md`,
`docs/specs/devarm-purpose-and-evolution/analysis.md`.
**Requirements/decisions:** FR-010–FR-016, FR-018–FR-023; D3, D9, D10, D14, D16, D18, D28.

After T015, update only phase metadata and checkpoint evidence:

- Mark tasks complete only with the actual task command output.
- Record the exact test and validator commands, result, date, and any limitations.
- Record changed files and any open warnings; do not claim implementation complete.
- Set the next gate to `devarm-analyze` and preserve the mandatory pre-implementation block.
- Keep the Decision Ledger and rule inventory linked; do not add a second planning system.
- Preserve the completed analysis findings and Pass 3 decisions as the implementation handoff.

Run:

```bash
git diff --check
git status --short
```

**Expected result:** the task artifact is ready for analyze, with no unresolved task-level
placeholder or silent assumption.

## 8. Requirement-to-test coverage

Every individual functional requirement has a named acceptance test or explicit verification
task before the implementation task that can violate it.

| Requirement | Named acceptance task/test | Implementation or final verification |
|---|---|---|
| FR-001 | T007 — `test_brainstorm_classifies_consequential_existing_repo_workflow` | T008 |
| FR-002 | T007 — `test_quick_track_upgrade_condition_is_locked` | T008 |
| FR-003 | T007 — `test_quick_track_upgrade_condition_is_locked` | T008 |
| FR-004 | T006 — `test_current_design_spec_and_plan_have_metadata_and_rule_inventory_links` | T006 |
| FR-005 | T007 — `test_brainstorm_requires_active_repo_branch_rule_inventory_and_track` | T008 |
| FR-006 | T007 — `test_target_rules_precede_devarm_defaults` | T008 |
| FR-007 | T007 — `test_target_rule_conflict_requires_visible_disposition` | T008 |
| FR-008 | T007 — `test_ground_requires_current_rule_inventory_and_grounded_handoff` | T008 |
| FR-009 | T007 — `test_ground_requires_boundary_consumer_and_runtime_contract_audit` | T008 |
| FR-010 | T004 — `test_templates_keep_repository_local_artifacts_as_source_of_truth` | T005 |
| FR-011 | T004 — `test_design_template_links_rule_inventory_and_preserves_ledger` | T005 |
| FR-012 | T007 — `test_early_phase_rules_preserve_approval_and_unanswered_decision_blocks` | T008 |
| FR-013 | T007 — `test_early_phase_rules_preserve_approval_and_unanswered_decision_blocks` | T008 |
| FR-014 | T004 — `test_artifact_metadata_template_locks_fields_and_statuses` and phase/verification metadata lock | T005 |
| FR-015 | T007 — `test_superseded_decision_requires_dependent_artifact_recheck` | T008 |
| FR-016 | T009 — `test_analyze_requires_artifact_validation_before_passes` | T010 |
| FR-017 | T009 — `test_dirty_worktree_and_unrelated_change_preservation_are_required` | T010 |
| FR-018 | T009 — `test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete` | T010 |
| FR-019 | T009 — `test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete` | T010 |
| FR-020 | T009 — `test_resume_revalidates_current_repo_rules_artifacts_and_diff` | T010 |
| FR-021 | T009 — `test_commit_push_merge_delete_reset_and_discard_remain_explicit` | T010 |
| FR-022 | T009 — `test_tasks_requires_decision_to_test_and_requirement_mapping` | T010 |
| FR-023 | T009 — `test_finish_requires_fresh_evidence_and_artifact_validation` | T010, T015 |
| FR-024 | T009 — `test_mocked_seams_require_explicit_limitation` | T010 |
| FR-025 | T009 — `test_risk_based_quality_coverage_is_preserved` | T010 |
| FR-026 | T002 — `test_missing_metadata_returns_error_with_line`, `test_missing_rule_inventory_or_link_is_blocking`, and related defect tests | T003, T013 |
| FR-027 | T002 — `test_validator_does_not_replace_human_judgment` | T003 |
| FR-028 | T002 — `test_json_issue_order_is_stable_across_repeated_runs` | T003, T013 |
| FR-029 | T001 — standard-library discovery smoke test | T015 |
| FR-030 | T011 — `test_adapter_present_inventory_records_output_and_reuse` and `test_adapter_absent_keeps_native_gates` | T012, T014 |
| FR-031 | T011 — `test_retro_proposal_requires_motivating_evidence_and_verification` | T012, T014 |
| FR-032 | T011 — `test_retro_proposal_requires_motivating_evidence_and_verification` | T012, T014, T015 |
| SC-008 | T013 — 20-document validation performance fixture | T015 |

## 9. Decision-to-test coverage

Every locked Decision Ledger row has a named acceptance test task before the implementation that
could violate it. Safety decisions include negative assertions, not only happy-path checks.

| Ledger decision | Named acceptance task/test | Guard type |
|---|---|---|
| D1 | T002 — `test_validator_does_not_require_network_or_optional_packages` | Method-first, optional-check boundary |
| D2 | T007 — `test_brainstorm_classifies_consequential_existing_repo_workflow` | Flagship workflow classification |
| D3 | T009 — `test_resume_revalidates_current_repo_rules_artifacts_and_diff` | Preserve and resume after interruption |
| D4 | T004 — `test_templates_keep_repository_local_artifacts_as_source_of_truth` | Repository-local source of truth |
| D5 | T007 — `test_target_rules_precede_devarm_defaults` | Target-rule precedence |
| D6 | T009 — `test_commit_push_merge_delete_reset_and_discard_remain_explicit` | Explicit lifecycle authority |
| D7 | T007 — `test_quick_track_upgrade_condition_is_locked` | Adaptive track boundary |
| D8 | T002 — `test_validator_does_not_require_network_or_optional_packages` | No required runtime dependency |
| D9 | T004 — `test_design_template_links_rule_inventory_and_preserves_ledger` | Durable phase artifact and ledger |
| D10 | T009 — `test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete` | Hard gate and negative status guard |
| D11 | T011 — `test_adapter_present_inventory_records_output_and_reuse` and `test_adapter_absent_keeps_native_gates` | Native core with optional adapters |
| D12 | T009 — `test_risk_based_quality_coverage_is_preserved` | Risk-based quality coverage |
| D13 | T007 — `test_decision_protocol_requires_recommendation_and_one_question` | Recommendation-first decision protocol |
| D14 | T009 — `test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete` | Partial output is preserved and not complete |
| D15 | T009 — `test_dirty_worktree_and_unrelated_change_preservation_are_required` | Dirty-worktree protection |
| D16 | T009 — `test_current_evidence_precedes_stale_summary` | Current evidence hierarchy |
| D17 | T002 — `test_validator_does_not_replace_human_judgment` | Skills own judgment; validator owns deterministic checks |
| D18 | T013 — `test_current_artifact_set_passes_all_native_handoff_checks` | Grounded, testable, resumable, portable success |
| D19 | T004 — `test_artifact_metadata_template_locks_fields_and_statuses` | Design path and repo/branch identity |
| D20 | T006 — `test_current_design_spec_and_plan_have_metadata_and_rule_inventory_links` | Preserve names and phase relationships |
| D21 | T004 — `test_templates_do_not_require_front_matter_or_a_database` | Structured Markdown contract |
| D22 | T004 — `test_rule_inventory_template_locks_columns_and_precedence` | Canonical inventory with downstream links |
| D23 | T002 — `test_validator_does_not_require_network_or_optional_packages` | Standard-library validator contract |
| D24 | T002 — `test_validator_errors_block_and_warnings_are_visible` | Error/warning enforcement split |
| D25 | T011 — `test_installation_contract_does_not_require_validator_distribution` | Installation compatibility |
| D26 | T011/T014 — `test_source_rule_adoption_matrix_preserves_target_specific_rules` | Portable source-rule adoption boundary |
| D27 | T007 — `test_quick_track_is_exactly_three_changed_files_or_fewer` | Hard quick-track threshold |
| D28 | T006/T013 — analysis artifact characterization and preservation tests | Durable analyze output |
| D29 | T002/T003 — `test_analysis_kind_uses_path_and_kind_without_expected_phase_argument` | Validator seam contract |
| D30 | T011/T015 — canonical task-source wording and final artifact review | One executable task source |
| D31 | T001–T003/T015 — ordered RED/GREEN/full-suite checkpoints | Sequential TDD execution |
| D32 | T001–T003/T013/T015 — standard-library subprocess and performance fixtures | Dependency-free verification |
| D33 | T016 — feature-branch and baseline precondition verification | No implementation on `main` |
| D34 | T014/T016 — retro handoff and changelog ownership wording | Method-change history ownership |

## 10. Self-check

- [x] Every individual specification requirement FR-001–FR-032 maps to a named acceptance test
  or explicit verification task.
- [x] Every Decision Ledger row D1–D34 has a named acceptance test task or explicit implementation
  verification before violating implementation.
  implementation.
- [x] Safety invariants use negative assertions: incomplete predecessor blocks handoff, partial/
  failed/blocked cannot pass as complete, no silent approval, no adapter bypass, and no missing
  verification completion claim.
- [x] Every implementation task has a preceding RED task or a documented characterization test
  where the artifact already contains the planned phase output.
- [x] Integration seams S1–S3 have subprocess/contract tests and no unplanned external seams.
- [x] No Git mirror, change-set, retry-counter, migration, or settings-binding task is needed;
  the plan explicitly marks each as out of scope.
- [x] `[P]` markers are limited to T002/T004 and T003/T005, which can run in parallel within
  their dependency wave and touch different files; tasks sharing a test file remain serial.
- [x] Every task has exact file paths, a focused command, and expected RED/GREEN evidence.
- [x] No task instructs an automatic commit, push, merge, reset, delete, or discard.

**Task gate result:** PASS. The recorded analyze findings and Pass 3 decisions are preserved. The
fresh `devarm-analyze` re-gate is now complete on the feature branch; the next phase is review.

### T001–T016 execution checkpoint — 2026-08-13

- [x] T001 — standard-library `unittest` harness established.
- [x] T002–T003 — validator RED/GREEN tests and `scripts/validate_devarm_artifacts.py` implemented.
- [x] T004–T005 — common metadata, rule-inventory, and native fallback templates implemented.
- [x] T006 — current design/spec/plan/tasks/analysis artifacts reconciled and characterized.
- [x] T007–T008 — early-phase skill handoff contracts wired with RED/GREEN wording locks.
- [x] T009–T010 — late-phase safety/evidence handoffs and status-transition contracts wired.
- [x] T011–T012 — portable documentation and adapter boundaries wired.
- [x] T013–T014 — final fixtures, 20-document performance check, retro, and source-rule regressions wired.
- [x] T015–T016 — complete acceptance matrix and this checkpoint recorded.

Evidence: `python3 -m unittest discover -s tests -p 'test_*.py' -q` → 85 tests passed;
the design, spec, plan, tasks, and analysis validator invocations each returned `valid: true`
with `issues: []`; `git diff --check` returned no output. No commit, push, merge, reset, delete,
or discard action was run. The analyze re-gate then completed cleanly; review has recorded
findings in `findings.md`, and the next gate is `devarm-implement`.
