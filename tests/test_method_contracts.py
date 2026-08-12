import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MethodContractTests(unittest.TestCase):
    def test_standard_library_test_harness_is_available(self):
        self.assertTrue(True)

    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_artifact_metadata_template_locks_fields_and_statuses(self):
        text = self.read("templates/artifact-metadata.md")
        for field in (
            "Document type",
            "Date",
            "Status",
            "Phase",
            "Feature/change",
            "Track",
            "Pipeline",
            "Target repository",
            "Target branch",
            "Last session note",
            "Last verification",
            "Open assumptions / risks",
            "Next gate",
            "Related artifacts",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)
        for status in (
            "draft",
            "awaiting approval",
            "in progress",
            "blocked",
            "partially completed",
            "failed",
            "complete",
        ):
            with self.subTest(status=status):
                self.assertIn(status, text)

    def test_artifact_metadata_template_locks_phase_verification_risks_next_gate_and_related_artifacts(self):
        text = self.read("templates/artifact-metadata.md")
        self.assertIn("Last verification", text)
        self.assertIn("Open assumptions / risks", text)
        self.assertIn("Next gate", text)
        self.assertIn("Related artifacts", text)

    def test_rule_inventory_template_locks_columns_and_precedence(self):
        text = self.read("templates/rule-inventory.md")
        for column in (
            "ID",
            "Source",
            "Scope",
            "Applies",
            "Precedence",
            "Enforcement phase",
            "Evidence",
            "Conflict/disposition",
        ):
            with self.subTest(column=column):
                self.assertIn(column, text)
        self.assertIn("target-repository rule wins", text.lower())

    def test_design_template_links_rule_inventory_and_preserves_ledger(self):
        text = self.read("templates/design-doc.md")
        self.assertIn("Repository Rule Inventory", text)
        self.assertIn("Decision Ledger", text)
        self.assertIn("Target repository", text)

    def test_native_spec_plan_tasks_and_analysis_templates_have_required_sections(self):
        expected = {
            "templates/spec-doc.md": ("Overview", "Functional requirements", "Clarifications", "Quality gate"),
            "templates/plan-doc.md": ("File-structure map", "Integration seams", "Implementation tasks", "Verification"),
            "templates/tasks-doc.md": ("Setup", "Foundational work", "tests-first", "Self-check"),
            "templates/analysis-doc.md": ("Pass 1", "Pass 2", "Pass 3", "Findings", "Analyze gate"),
        }
        for path, headings in expected.items():
            text = self.read(path).lower()
            for heading in headings:
                with self.subTest(path=path, heading=heading):
                    self.assertIn(heading.lower(), text)

    def test_templates_keep_repository_local_artifacts_as_source_of_truth(self):
        for path in (
            "templates/artifact-metadata.md",
            "templates/rule-inventory.md",
            "templates/spec-doc.md",
            "templates/plan-doc.md",
            "templates/tasks-doc.md",
            "templates/analysis-doc.md",
        ):
            with self.subTest(path=path):
                self.assertIn("repository-local", self.read(path).lower())

    def test_templates_do_not_require_front_matter_or_a_database(self):
        for path in (
            "templates/artifact-metadata.md",
            "templates/rule-inventory.md",
            "templates/spec-doc.md",
            "templates/plan-doc.md",
            "templates/tasks-doc.md",
            "templates/analysis-doc.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("no database", text)
                self.assertIn("no front matter", text)

    def test_current_design_spec_plan_tasks_and_analysis_have_metadata_and_rule_inventory_links(self):
        design = self.read("docs/design/2026-08-12-devarm-purpose-and-evolution-design.md")
        spec = self.read("docs/specs/devarm-purpose-and-evolution/spec.md")
        plan = self.read("docs/specs/devarm-purpose-and-evolution/plan.md")
        tasks = self.read("docs/specs/devarm-purpose-and-evolution/tasks.md")
        analysis = self.read("docs/specs/devarm-purpose-and-evolution/analysis.md")

        for text in (design, spec, plan, tasks, analysis):
            self.assertIn("**Target repository:** `/Users/dphadatare/vhosts/devarm`", text)
            self.assertIn("**Target branch:** `001-devarm-purpose-evolution`", text)
            self.assertIn("**Last verification:**", text)
            self.assertIn("**Open assumptions / risks:**", text)
            self.assertIn("**Next gate:**", text)
            self.assertIn("**Related artifacts:**", text)
            self.assertIn("**Analysis:**", text)

        for rule_id in ("R1", "R2", "R3", "R4", "R5", "R6", "R7"):
            self.assertIn(f"| {rule_id} |", design)
        self.assertIn("#repository-rule-inventory", spec)
        self.assertIn("#repository-rule-inventory", plan)
        self.assertIn("#repository-rule-inventory", tasks)
        self.assertIn("#repository-rule-inventory", analysis)
        for decision in ("D21", "D26", "D27", "D28", "D29", "D30", "D31", "D32", "D33", "D34"):
            self.assertIn(f"| {decision} |", design)
        self.assertIn("Pass 3 is **complete**", analysis)
        self.assertNotIn("assumed — awaiting confirmation", design)

    def test_brainstorm_requires_active_repo_branch_rule_inventory_and_track(self):
        text = self.read("skills/devarm-brainstorm/SKILL.md")
        self.assertIn("active repository and branch in the artifact metadata", text)
        self.assertIn("canonical rule inventory", text)
        self.assertIn("recommended track", text)

    def test_ground_requires_current_rule_inventory_and_grounded_handoff(self):
        text = self.read("skills/devarm-ground/SKILL.md")
        self.assertIn("active repository and branch in the artifact metadata", text)
        self.assertIn("canonical rule inventory", text)
        self.assertIn("optional validator", text)
        self.assertIn("blocking error stops the handoff", text)

    def test_clarify_requires_native_spec_handoff_and_optional_adapter_boundary(self):
        text = self.read("skills/devarm-clarify/SKILL.md")
        self.assertIn("active repository and branch in the artifact metadata", text)
        self.assertIn("native ambiguity gate", text)
        self.assertIn("optional validator", text)
        self.assertIn("clarifications into `spec.md`", text)

    def test_target_rule_conflict_requires_visible_disposition(self):
        for path in (
            "skills/devarm-brainstorm/SKILL.md",
            "skills/devarm-ground/SKILL.md",
            "skills/devarm-spec/SKILL.md",
            "skills/devarm-clarify/SKILL.md",
            "skills/devarm-plan/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path)
                self.assertIn("target-repository rule wins", text)
                self.assertIn("conflict", text.lower())

    def test_ground_requires_boundary_consumer_and_runtime_contract_audit(self):
        text = self.read("skills/devarm-ground/SKILL.md").lower()
        self.assertIn("consumer", text)
        self.assertIn("runtime contract", text)
        self.assertIn("boundary", text)

    def test_spec_requires_native_fallback_template_and_quality_gate(self):
        text = self.read("skills/devarm-spec/SKILL.md")
        self.assertIn("templates/spec-doc.md", text)
        self.assertIn("quality gate", text.lower())
        self.assertIn("optional validator", text)

    def test_plan_requires_file_map_seams_and_validator_handoff(self):
        text = self.read("skills/devarm-plan/SKILL.md")
        self.assertIn("templates/plan-doc.md", text)
        self.assertIn("file-structure map", text)
        self.assertIn("integration seam", text.lower())
        self.assertIn("optional validator", text)

    def test_early_phase_rules_preserve_approval_and_unanswered_decision_blocks(self):
        for path in (
            "skills/devarm-brainstorm/SKILL.md",
            "skills/devarm-ground/SKILL.md",
            "skills/devarm-spec/SKILL.md",
            "skills/devarm-clarify/SKILL.md",
            "skills/devarm-plan/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("approval", text)
                self.assertIn("unanswered", text)
                self.assertIn("awaiting confirmation", text)

    def test_quick_track_upgrade_condition_is_locked(self):
        text = self.read("skills/devarm-brainstorm/SKILL.md")
        self.assertIn("at most 3 changed files", text)
        self.assertIn("any persistence change", text)
        self.assertIn("any contract change", text)
        self.assertIn("upgrade to the standard track", text)

    def test_quick_track_is_exactly_three_changed_files_or_fewer(self):
        text = self.read("skills/devarm-brainstorm/SKILL.md")
        self.assertIn("at most 3 changed files", text)
        self.assertNotIn("roughly ≤3", text)
        self.assertNotIn("approximately ≤3", text)

    def test_decision_protocol_requires_recommendation_and_one_question(self):
        text = self.read("skills/devarm-brainstorm/SKILL.md").lower()
        self.assertIn("recommendation", text)
        self.assertIn("one question per message", text)
        self.assertIn("assumed — awaiting confirmation", text)

    def test_superseded_decision_requires_dependent_artifact_recheck(self):
        for path in (
            "skills/devarm-brainstorm/SKILL.md",
            "skills/devarm-spec/SKILL.md",
            "skills/devarm-plan/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("supersed", text)
                self.assertIn("dependent", text)
                self.assertIn("re-check", text)

    def test_target_rules_precede_devarm_defaults(self):
        text = self.read("skills/devarm-ground/SKILL.md").lower()
        self.assertIn("target-repository rule wins", text)
        self.assertIn("devarm default", text)

    def test_no_required_external_framework_or_validator_installation_is_stated(self):
        for path in (
            "skills/devarm-brainstorm/SKILL.md",
            "skills/devarm-ground/SKILL.md",
            "skills/devarm-spec/SKILL.md",
            "skills/devarm-clarify/SKILL.md",
            "skills/devarm-plan/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("optional validator", text)
                self.assertIn("not required", text)

    def test_source_rule_adoption_matrix_preserves_target_specific_rules(self):
        text = self.read("docs/design/2026-08-12-devarm-purpose-and-evolution-design.md")
        for rule in (
            "architecture-boundaries.mdc",
            "backend-conventions.mdc",
            "design-patterns.mdc",
            "design-principles.mdc",
            "frontend-conventions.mdc",
            "no-half-finished-refactors.mdc",
            "specify-rules.mdc",
        ):
            self.assertIn(rule, text)
        self.assertIn("Target-only adapter", text)
        self.assertIn("Adopt + adapt", text)

    def test_tasks_requires_decision_to_test_and_requirement_mapping(self):
        text = self.read("skills/devarm-tasks/SKILL.md").lower()
        self.assertIn("requirement/ledger-to-task traceability", text)
        self.assertIn("optional validator", text)
        self.assertIn("safety invariant", text)

    def test_analyze_requires_artifact_validation_before_passes(self):
        text = self.read("skills/devarm-analyze/SKILL.md").lower()
        self.assertIn("validate all loaded artifacts before pass 1", text)
        self.assertIn("validator output", text)
        self.assertIn("analysis.md", text)

    def test_implement_requires_clean_analyze_and_current_artifact_revalidation(self):
        text = self.read("skills/devarm-implement/SKILL.md").lower()
        self.assertIn("clean analyze", text)
        self.assertIn("re-validate the governing artifacts", text)
        self.assertIn("current repository rules", text)

    def test_review_requires_rule_inventory_and_real_seam_limitations(self):
        text = self.read("skills/devarm-review/SKILL.md").lower()
        self.assertIn("rule inventory", text)
        self.assertIn("real seam", text)
        self.assertIn("limitation", text)
        self.assertIn("validator output", text)

    def test_finish_requires_fresh_evidence_and_artifact_validation(self):
        text = self.read("skills/devarm-finish/SKILL.md").lower()
        self.assertIn("fresh full-suite evidence", text)
        self.assertIn("current artifact validation", text)
        self.assertIn("typed discard confirmation", text)

    def test_retro_requires_motivating_evidence_and_method_inventory(self):
        text = self.read("skills/devarm-retro/SKILL.md").lower()
        self.assertIn("motivating evidence", text)
        self.assertIn("method inventory", text)
        self.assertIn("verification evidence", text)

    def test_resume_revalidates_current_repo_rules_artifacts_and_diff(self):
        for path in (
            "skills/devarm-tasks/SKILL.md",
            "skills/devarm-analyze/SKILL.md",
            "skills/devarm-implement/SKILL.md",
            "skills/devarm-review/SKILL.md",
            "skills/devarm-finish/SKILL.md",
            "skills/devarm-retro/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("current repository rules", text)
                self.assertIn("revalidate artifacts", text)
                self.assertIn("diff", text)

    def test_current_evidence_precedes_stale_summary(self):
        for path in (
            "skills/devarm-tasks/SKILL.md",
            "skills/devarm-analyze/SKILL.md",
            "skills/devarm-implement/SKILL.md",
            "skills/devarm-review/SKILL.md",
            "skills/devarm-finish/SKILL.md",
            "skills/devarm-retro/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("current evidence", text)
                self.assertIn("stale summary", text)

    def test_mocked_seams_require_explicit_limitation(self):
        for path in ("skills/devarm-implement/SKILL.md", "skills/devarm-review/SKILL.md"):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("mocked seam", text)
                self.assertIn("limitation", text)

    def test_partial_failed_and_blocked_statuses_cannot_be_described_as_complete(self):
        text = self.read("skills/devarm-implement/SKILL.md").lower()
        self.assertIn("partial, failed, or blocked", text)
        self.assertIn("not eligible for a complete handoff", text)
        self.assertIn("complete is terminal", text)
        self.assertIn("drift becomes blocked", text)

    def test_dirty_worktree_and_unrelated_change_preservation_are_required(self):
        text = self.read("skills/devarm-implement/SKILL.md").lower()
        self.assertIn("dirty worktree", text)
        self.assertIn("unrelated changes", text)
        self.assertIn("preserve", text)

    def test_commit_push_merge_delete_reset_and_discard_remain_explicit(self):
        text = self.read("skills/devarm-finish/SKILL.md").lower()
        for operation in ("commit", "push", "merge", "delete", "reset", "discard"):
            with self.subTest(operation=operation):
                self.assertIn(operation, text)
        self.assertIn("explicit lifecycle authority", text)

    def test_adapter_use_cannot_bypass_native_gates(self):
        for path in (
            "skills/devarm-tasks/SKILL.md",
            "skills/devarm-analyze/SKILL.md",
            "skills/devarm-implement/SKILL.md",
            "skills/devarm-review/SKILL.md",
            "skills/devarm-finish/SKILL.md",
            "skills/devarm-retro/SKILL.md",
        ):
            with self.subTest(path=path):
                text = self.read(path).lower()
                self.assertIn("adapter", text)
                self.assertIn("native gates", text)

    def test_risk_based_quality_coverage_is_preserved(self):
        for path in ("skills/devarm-tasks/SKILL.md", "skills/devarm-review/SKILL.md"):
            with self.subTest(path=path):
                self.assertIn("risk-based quality coverage", self.read(path).lower())

    def test_status_transition_draft_to_in_progress_preserves_artifact(self):
        self.assertIn("draft -> in progress preserves artifact", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_draft_to_awaiting_approval_blocks_implementation(self):
        self.assertIn("draft -> awaiting approval blocks implementation", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_awaiting_approval_requires_explicit_approval(self):
        self.assertIn("awaiting approval requires explicit approval", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_awaiting_approval_change_returns_to_draft_preserves_feedback(self):
        self.assertIn("awaiting approval change returns to draft preserves feedback", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_in_progress_complete_requires_evidence(self):
        self.assertIn("in progress -> complete requires evidence", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_in_progress_partial_failed_blocked_preserves_side_effects(self):
        self.assertIn("in progress -> partial, failed, blocked preserves side effects", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_partial_failed_blocked_resume_returns_in_progress_after_revalidation(self):
        self.assertIn("partial, failed, blocked resume returns in progress after revalidation", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_complete_is_terminal_without_event(self):
        self.assertIn("complete is terminal without event", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_status_transition_complete_drift_becomes_blocked(self):
        self.assertIn("complete drift becomes blocked", self.read("skills/devarm-implement/SKILL.md").lower())

    def test_agents_documents_metadata_rules_validator_authority_and_resume(self):
        text = self.read("AGENTS.md").lower()
        for phrase in (
            "common artifact metadata",
            "canonical rule inventory",
            "target-repository rule wins",
            "optional validator",
            "human judgment",
            "partial",
            "resume",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_readme_documents_native_pipeline_fallback_and_validator_optionality(self):
        text = self.read("README.md").lower()
        self.assertIn("native pipeline", text)
        self.assertIn("fallback templates", text)
        self.assertIn("optional validator", text)
        self.assertIn("no required cli, service, or database", text)
        self.assertIn("target-project-specific rules", text)

    def test_user_guide_documents_clarify_analysis_and_resume_contract(self):
        text = self.read("USER_GUIDE.md").lower()
        for phrase in (
            "clarify",
            "analysis.md",
            "optional validator",
            "native gates",
            "partial",
            "resume",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_adapter_present_inventory_records_output_and_reuse(self):
        for path in ("README.md", "USER_GUIDE.md", "AGENTS.md"):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertIn("method inventory", text)
                self.assertIn("adapter", text)
                self.assertIn("output", text)
                self.assertIn("reuse", text)

    def test_adapter_absent_keeps_native_gates(self):
        for path in ("README.md", "USER_GUIDE.md", "AGENTS.md"):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertIn("adapter-absent", text)
                self.assertIn("native gates", text)

    def test_retro_proposal_requires_motivating_evidence_and_verification(self):
        for path in ("README.md", "USER_GUIDE.md", "AGENTS.md"):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertIn("motivating evidence", text)
                self.assertIn("verification evidence", text)

    def test_retro_requires_generalized_category_and_promotion_boundary(self):
        text = self.read("skills/devarm-retro/SKILL.md").lower()
        for phrase in (
            "failure category",
            "domain-neutral invariant",
            "applicability boundary",
            "generalization check",
            "two repository/domain",
            "shapes",
            "portable core",
            "category-scoped",
            "target-only",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_normative_skills_do_not_contain_incident_provenance_markers(self):
        import re

        markers = (
            re.compile(r"session evidence", re.IGNORECASE),
            re.compile(r"\bspec\s+\d{3}\b", re.IGNORECASE),
            re.compile(r"\bDEV-\d+\b", re.IGNORECASE),
            re.compile(r"\bPR\s+#\d+\b", re.IGNORECASE),
        )
        for path in sorted((REPO_ROOT / "skills").glob("devarm-*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(path=path, marker=marker.pattern):
                    self.assertIsNone(marker.search(text))

    def test_installation_contract_does_not_require_validator_distribution(self):
        text = self.read("README.md").lower()
        self.assertIn("validator is not installed", text)
        self.assertIn("standard-library", text)

    def test_source_rule_dispositions_are_documented_as_adopt_adapt_or_target_only(self):
        for path in ("README.md", "USER_GUIDE.md", "AGENTS.md"):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertIn("adopt", text)
                self.assertIn("adapt", text)
                self.assertIn("target-only", text)

    def test_native_phase_skills_have_common_artifact_rule_validator_handoff(self):
        skills = (
            "brainstorm",
            "ground",
            "spec",
            "clarify",
            "plan",
            "tasks",
            "analyze",
            "implement",
            "review",
            "finish",
            "retro",
        )
        for name in skills:
            text = self.read(f"skills/devarm-{name}/SKILL.md").lower()
            with self.subTest(skill=name):
                for phrase in ("artifact", "rule", "validator", "handoff"):
                    self.assertIn(phrase, text)

    def test_validator_output_is_never_described_as_human_approval(self):
        for path in (
            "skills/devarm-brainstorm/SKILL.md",
            "skills/devarm-ground/SKILL.md",
            "skills/devarm-spec/SKILL.md",
            "skills/devarm-clarify/SKILL.md",
            "skills/devarm-plan/SKILL.md",
            "skills/devarm-tasks/SKILL.md",
            "skills/devarm-analyze/SKILL.md",
            "skills/devarm-implement/SKILL.md",
            "skills/devarm-review/SKILL.md",
            "skills/devarm-finish/SKILL.md",
            "skills/devarm-retro/SKILL.md",
        ):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertNotIn("validator output is approval", text)
                self.assertNotIn("validator output marks approval", text)

    def test_method_inventory_records_native_external_output_and_reuse_columns(self):
        text = self.read("docs/design/2026-08-12-devarm-purpose-and-evolution-design.md")
        for column in ("Item", "Native/external", "Used?", "Artifact/output", "Reuse next time"):
            self.assertIn(column, text)
        self.assertIn("External adapter", text)
        self.assertIn("Spec Kit", text)

    def test_source_rule_matrix_keeps_all_seven_target_specific_rules_external(self):
        text = self.read("docs/design/2026-08-12-devarm-purpose-and-evolution-design.md")
        rules = (
            "architecture-boundaries.mdc",
            "backend-conventions.mdc",
            "design-patterns.mdc",
            "design-principles.mdc",
            "frontend-conventions.mdc",
            "no-half-finished-refactors.mdc",
            "specify-rules.mdc",
        )
        for rule in rules:
            self.assertIn(rule, text)
        self.assertIn("Target-only adapter", text)
        self.assertIn("target-repository rules", text.lower())

    def test_adapter_present_and_absent_paths_preserve_identical_native_gate_requirements(self):
        for path in ("AGENTS.md", "README.md", "USER_GUIDE.md"):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertTrue("adapter-present" in text or "adapter is present" in text)
                self.assertIn("adapter-absent", text)
                self.assertIn("native gates", text)
        retro = self.read("skills/devarm-retro/SKILL.md").lower()
        self.assertIn("cannot bypass native gates", retro)

    def test_retro_proposal_names_evidence_affected_method_surface_and_verification(self):
        text = self.read("skills/devarm-retro/SKILL.md").lower()
        self.assertIn("motivating evidence", text)
        self.assertIn("affected", text)
        self.assertIn("skill", text)
        self.assertIn("template", text)
        self.assertIn("validator", text)
        self.assertIn("verification evidence", text)

    def test_no_adapter_can_mark_native_gates_complete(self):
        for path in (
            "AGENTS.md",
            "README.md",
            "USER_GUIDE.md",
            "skills/devarm-retro/SKILL.md",
        ):
            text = self.read(path).lower()
            with self.subTest(path=path):
                self.assertIn("native gates", text)
                self.assertTrue("cannot bypass native gates" in text or "same native gates" in text)


if __name__ == "__main__":
    unittest.main()
