import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_devarm_artifacts.py"


def artifact_text(kind="spec"):
    phase = {
        "design": "design",
        "spec": "specification",
        "plan": "plan",
        "tasks": "tasks",
        "analysis": "analyze",
    }[kind]
    sections = {
        "design": """
## Problem statement

A grounded method change is needed.

## Detailed Design (grounded)

The design is grounded with current evidence.

## Repository Rule Inventory

| ID | Source | Scope | Applies | Precedence | Enforcement phase | Evidence | Conflict/disposition |
|---|---|---|---|---|---|---|---|
| R1 | AGENTS.md | method | Yes | target | all | AGENTS.md:1-10 | adopt |

## Decision Ledger

| # | Decision | Alternatives rejected | Evidence | Owner | Tier | Status |
|---|---|---|---|---|---|---|
| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |
""",
        "spec": """
## Overview

The method validates grounded artifacts.

## Functional requirements

- FR-001: The validator reports deterministic artifact issues.

## Scenario coverage matrix

| Requirement | Scenario | Verification |
|---|---|---|
| FR-001 | valid artifact | validator test |

## Success criteria

- SC-001: A valid artifact returns a valid result.

## Clarifications

No material clarification is required.

## Decision Ledger

| # | Decision | Alternatives rejected | Evidence | Owner | Tier | Status |
|---|---|---|---|---|---|---|
| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |
""",
        "plan": """
## Implementation objective

Implement deterministic artifact validation.

## Scope and requirement coverage

| Requirement | Plan coverage |
|---|---|
| FR-001 | T001 |

## File-structure map

| File | Responsibility |
|---|---|
| scripts/validate.py | validation |

## Technical context

The validator is standard-library-only.

## Integration seams and contracts

The validator receives an artifact path and kind.

## Implementation tasks

### T001

Write the failing validator test first.

## Verification

Run the standard-library test suite.

## Decision Ledger

| # | Decision | Alternatives rejected | Evidence | Owner | Tier | Status |
|---|---|---|---|---|---|---|
| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |
""",
        "tasks": """
## Execution contract

Tests precede implementation.

## Setup and baseline

Run the baseline test command.

## Foundational validator behavior

Write the validator behavior test first.

## Self-check

- Every behavior has a preceding RED task.

## Decision Ledger

| # | Decision | Alternatives rejected | Evidence | Owner | Tier | Status |
|---|---|---|---|---|---|---|
| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |
""",
        "analysis": """
## Scope and evidence

The current artifacts and code were rechecked.

## Findings

| ID | Severity | Summary |
|---|---|---|
| A-001 | LOW | No blocking finding |

## Pass 1 result

Pass 1 is clean.

## Pass 2 result

Pass 2 is clean.

## Pass 3 status

Pass 3 is complete.

## Pass 3 result

The implementation batch is recorded.

## Decision Ledger

| # | Decision | Alternatives rejected | Evidence | Owner | Tier | Status |
|---|---|---|---|---|---|---|
| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |
""",
    }[kind]
    return f"""# Fixture {kind.title()}

**Document type:** {kind} artifact
**Date:** 2026-08-13
**Status:** complete
**Phase:** {phase}
**Feature/change:** validator fixture
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☑ clarify ☑ plan ☑ tasks ☑ analyze ☑ implement ☐ review ☐ finish ☐
**Target repository:** /tmp/repo
**Target branch:** fixture
**Last session note:** fixture is ready for validation
**Last verification:** 2026-08-13 — python3 -m unittest
**Open assumptions / risks:** none
**Next gate:** devarm-implement
**Related artifacts:** design.md, spec.md, plan.md, tasks.md, analysis.md
**Design:** design.md
**Rule inventory:** design.md#repository-rule-inventory
**Analysis:** analysis.md
{sections}
"""


class ValidatorContractTests(unittest.TestCase):
    def invoke(self, text, kind="spec", extra_args=()):
        self.assertTrue(
            VALIDATOR.exists(),
            "validator entrypoint is missing: scripts/validate_devarm_artifacts.py",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            artifact = Path(temp_dir) / f"artifact-{kind}.md"
            artifact.write_text(text, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    "--artifact",
                    str(artifact),
                    "--kind",
                    kind,
                    "--format",
                    "json",
                    *extra_args,
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    def result(self, completed):
        return json.loads(completed.stdout)

    def invoke_current(self, relative_path, kind):
        return subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--artifact",
                str(REPO_ROOT / relative_path),
                "--kind",
                kind,
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_missing_entrypoint_fails_as_behavioral_assertion(self):
        self.assertTrue(VALIDATOR.exists(), "validator entrypoint is missing")

    def test_valid_design_spec_plan_tasks_and_analysis_return_zero_json(self):
        for kind in ("design", "spec", "plan", "tasks", "analysis"):
            with self.subTest(kind=kind):
                completed = self.invoke(artifact_text(kind), kind)
                self.assertEqual(completed.returncode, 0)
                self.assertTrue(self.result(completed)["valid"])

    def test_missing_metadata_returns_error_with_line(self):
        completed = self.invoke(artifact_text().replace("**Status:** complete\n", ""))
        payload = self.result(completed)
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(
            any(issue["code"] == "MISSING_METADATA" and issue["line"] for issue in payload["issues"])
        )

    def test_invalid_status_and_pipeline_return_distinct_errors(self):
        text = artifact_text().replace("**Status:** complete", "**Status:** finished").replace(
            "**Pipeline:** brainstorm", "**Pipeline:** invalid"
        )
        completed = self.invoke(text)
        codes = {issue["code"] for issue in self.result(completed)["issues"]}
        self.assertEqual(completed.returncode, 1)
        self.assertIn("INVALID_STATUS", codes)
        self.assertIn("INVALID_PIPELINE", codes)

    def test_empty_ledger_owner_evidence_tier_and_status_are_blocking(self):
        text = artifact_text("design").replace(
            "| D1 | Keep artifacts local | hosted state | fixture:1 | user | design | approved |",
            "| D1 | Keep artifacts local | hosted state |  |  |  |  |",
        )
        completed = self.invoke(text, "design")
        codes = {issue["code"] for issue in self.result(completed)["issues"]}
        self.assertEqual(completed.returncode, 1)
        self.assertTrue({"EMPTY_LEDGER_EVIDENCE", "EMPTY_LEDGER_OWNER", "EMPTY_LEDGER_TIER", "EMPTY_LEDGER_STATUS"} <= codes)

    def test_missing_rule_inventory_or_link_is_blocking(self):
        text = artifact_text().replace("**Rule inventory:** design.md#repository-rule-inventory\n", "")
        completed = self.invoke(text)
        codes = {issue["code"] for issue in self.result(completed)["issues"]}
        self.assertEqual(completed.returncode, 1)
        self.assertIn("MISSING_RULE_INVENTORY", codes)

    def test_missing_requirement_traceability_is_blocking_for_spec_and_plan(self):
        for kind in ("spec", "plan"):
            with self.subTest(kind=kind):
                if kind == "spec":
                    text = artifact_text(kind).replace("FR-001", "FR-999", 1)
                else:
                    text = artifact_text(kind).replace("FR-001", "NO-REQ")
                completed = self.invoke(text, kind)
                codes = {issue["code"] for issue in self.result(completed)["issues"]}
                self.assertEqual(completed.returncode, 1)
                self.assertIn("MISSING_REQUIREMENT_TRACE", codes)

    def test_completed_artifact_with_placeholder_or_missing_verification_is_blocking(self):
        text = artifact_text().replace("The method validates grounded artifacts.", "<TODO>").replace(
            "**Last verification:** 2026-08-13 — python3 -m unittest\n", ""
        )
        completed = self.invoke(text)
        codes = {issue["code"] for issue in self.result(completed)["issues"]}
        self.assertEqual(completed.returncode, 1)
        self.assertIn("COMPLETION_PLACEHOLDER", codes)
        self.assertIn("MISSING_VERIFICATION", codes)

    def test_partial_blocked_and_failed_artifacts_cannot_pass_as_complete(self):
        for status in ("partially completed", "blocked", "failed"):
            with self.subTest(status=status):
                completed = self.invoke(artifact_text().replace("**Status:** complete", f"**Status:** {status}"))
                self.assertNotEqual(completed.returncode, 0)
                self.assertFalse(self.result(completed)["valid"])

    def test_validator_errors_block_and_warnings_are_visible(self):
        error = self.invoke(artifact_text().replace("**Status:** complete", "**Status:** invalid"))
        warning = self.invoke(
            artifact_text().replace("**Open assumptions / risks:** none", "**Open assumptions / risks:** warning: legacy fixture")
        )
        self.assertEqual(error.returncode, 1)
        self.assertEqual(warning.returncode, 0)
        self.assertTrue(any(issue["severity"] == "warning" for issue in self.result(warning)["issues"]))

    def test_validator_does_not_replace_human_judgment(self):
        completed = self.invoke(artifact_text())
        payload = self.result(completed)
        self.assertNotIn("APPROVAL_INFERRED", {issue["code"] for issue in payload["issues"]})
        self.assertNotIn("human approval", completed.stdout.lower())

    def test_invalid_kind_or_missing_file_returns_invocation_failure(self):
        self.assertTrue(VALIDATOR.exists(), "validator entrypoint is missing")
        invalid_kind = subprocess.run(
            [sys.executable, str(VALIDATOR), "--artifact", "missing.md", "--kind", "unknown", "--format", "json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(invalid_kind.returncode, 2)

    def test_analysis_kind_uses_path_and_kind_without_expected_phase_argument(self):
        completed = self.invoke(artifact_text("analysis"), "analysis")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(self.result(completed)["kind"], "analysis")

    def test_json_issue_order_is_stable_across_repeated_runs(self):
        text = artifact_text().replace("**Status:** complete", "**Status:** invalid")
        first = self.invoke(text)
        second = self.invoke(text)
        self.assertEqual(first.returncode, 1)
        first_payload = self.result(first)
        second_payload = self.result(second)
        first_payload["artifact"] = "<temporary-artifact>"
        second_payload["artifact"] = "<temporary-artifact>"
        self.assertEqual(first_payload, second_payload)

    def test_validator_does_not_require_network_or_optional_packages(self):
        completed = self.invoke(artifact_text())
        self.assertEqual(completed.returncode, 0)

    def test_current_artifact_set_passes_all_native_handoff_checks(self):
        artifacts = (
            ("docs/design/2026-08-12-devarm-purpose-and-evolution-design.md", "design"),
            ("docs/specs/devarm-purpose-and-evolution/spec.md", "spec"),
            ("docs/specs/devarm-purpose-and-evolution/plan.md", "plan"),
            ("docs/specs/devarm-purpose-and-evolution/tasks.md", "tasks"),
            ("docs/specs/devarm-purpose-and-evolution/analysis.md", "analysis"),
        )
        for path, kind in artifacts:
            with self.subTest(path=path):
                completed = self.invoke_current(path, kind)
                self.assertEqual(completed.returncode, 0, completed.stdout)
                self.assertTrue(self.result(completed)["valid"])

    def test_incomplete_fixture_blocks_handoff(self):
        completed = self.invoke(artifact_text().replace("**Last verification:**", "**Last verification:**" ).replace(
            "**Rule inventory:** design.md#repository-rule-inventory\n", ""
        ))
        self.assertEqual(completed.returncode, 1)
        payload = self.result(completed)
        self.assertFalse(payload["valid"])
        self.assertIn("MISSING_RULE_INVENTORY", {issue["code"] for issue in payload["issues"]})

    def test_complete_fixture_requires_verification_record(self):
        completed = self.invoke(artifact_text().replace("**Last verification:** 2026-08-13 — python3 -m unittest\n", ""))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("MISSING_VERIFICATION", {issue["code"] for issue in self.result(completed)["issues"]})

    def test_validator_output_is_not_human_approval(self):
        completed = self.invoke(artifact_text())
        payload = self.result(completed)
        self.assertTrue(payload["valid"])
        self.assertNotIn("approval", json.dumps(payload).lower())

    def test_status_fixture_preserves_partial_failed_and_blocked_states(self):
        for status in ("partially completed", "failed", "blocked"):
            with self.subTest(status=status):
                completed = self.invoke(artifact_text().replace("**Status:** complete", f"**Status:** {status}"))
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(self.result(completed)["valid"])

    def test_current_analysis_artifact_preserves_findings_until_pass3(self):
        text = (REPO_ROOT / "docs/specs/devarm-purpose-and-evolution/analysis.md").read_text(encoding="utf-8")
        for marker in ("## Initial findings", "## Remediation and recheck", "## Pass 1 result", "## Pass 2 result", "## Pass 3 result", "Pass 3 is **complete**"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_repeated_current_json_validation_is_stable_after_path_normalization(self):
        first = self.invoke_current("docs/specs/devarm-purpose-and-evolution/plan.md", "plan")
        second = self.invoke_current("docs/specs/devarm-purpose-and-evolution/plan.md", "plan")
        self.assertEqual(first.returncode, second.returncode)
        first_payload = self.result(first)
        second_payload = self.result(second)
        first_payload["artifact"] = "<artifact>"
        second_payload["artifact"] = "<artifact>"
        self.assertEqual(first_payload, second_payload)

    def test_twenty_representative_phase_documents_validate_within_ten_seconds(self):
        documents = [(kind, artifact_text(kind)) for kind in ("design", "spec", "plan", "tasks", "analysis")]
        start = time.perf_counter()
        for index in range(4):
            for kind, text in documents:
                path = Path(tempfile.gettempdir()) / f"devarm-fixture-{index}-{kind}.md"
                path.write_text(text, encoding="utf-8")
                try:
                    self.assertEqual([], __import__("scripts.validate_devarm_artifacts", fromlist=["validate_artifact"]).validate_artifact(path, kind))
                finally:
                    path.unlink()
        self.assertLess(time.perf_counter() - start, 10.0)


if __name__ == "__main__":
    unittest.main()
