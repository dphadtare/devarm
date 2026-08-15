#!/usr/bin/env python3
"""Validate the portable, repository-local structure of a devarm artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


KINDS = ("design", "spec", "plan", "tasks", "analysis", "review")
ALLOWED_STATUSES = {
    "draft",
    "awaiting approval",
    "in progress",
    "blocked",
    "partially completed",
    "failed",
    "complete",
}
REQUIRED_METADATA = (
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
)
EXPECTED_PHASES = {
    "design": ("design",),
    "spec": ("spec", "clarif"),
    "plan": ("plan",),
    "tasks": ("tasks",),
    "analysis": ("analy", "analysis"),
    "review": ("review",),
}
REQUIRED_HEADINGS = {
    "design": ("problem statement", "detailed design", "decision ledger"),
    "spec": (
        "overview",
        "functional requirements",
        "scenario coverage matrix",
        "success criteria",
        "clarifications",
    ),
    "plan": (
        "implementation objective",
        "scope and requirement coverage",
        "file-structure map",
        "technical context",
        "integration seams and contracts",
        "implementation tasks",
    ),
    "tasks": (
        "execution contract",
        "setup and baseline",
        "foundational validator behavior",
        "self-check",
    ),
    "analysis": (
        "scope and evidence",
        "findings",
        "pass 1 result",
        "pass 2 result",
        "pass 3 status",
        "pass 3 result",
    ),
    "review": ("findings",),
}
PIPELINE_PHASES = (
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
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"<\s*TODO\s*>", re.IGNORECASE),
    re.compile(r"\bTODO\s*:", re.IGNORECASE),
    re.compile(r"<\s*TBD\s*>", re.IGNORECASE),
    re.compile(r"\bTBD\s*:", re.IGNORECASE),
    re.compile(r"\[NEEDS CLARIFICATION\]", re.IGNORECASE),
    re.compile(r"<TODO>", re.IGNORECASE),
)
RANGE_RE = re.compile(r"\b(FR-\d+)\s*[–—-]\s*(FR-\d+)\b")
FR_RE = re.compile(r"\bFR-(\d+)\b")
METADATA_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")


@dataclass(frozen=True)
class Issue:
    code: str
    severity: str
    line: Optional[int]
    message: str


def _issue(code: str, severity: str, line: Optional[int], message: str) -> Issue:
    return Issue(code=code, severity=severity, line=line, message=message)


def _metadata(lines: list[str]) -> tuple[dict[str, str], dict[str, int]]:
    values: dict[str, str] = {}
    locations: dict[str, int] = {}
    for number, line in enumerate(lines, start=1):
        match = METADATA_RE.match(line)
        if match:
            key, value = match.groups()
            values[key.strip()] = value.strip()
            locations[key.strip()] = number
    return values, locations


def _heading_text(line: str) -> str:
    return re.sub(r"^#+\s*", "", line).strip().lower()


def _has_heading(lines: Iterable[str], phrase: str) -> bool:
    return any(phrase.lower() in _heading_text(line) for line in lines if line.startswith("#"))


def _heading_line(lines: list[str], phrase: str) -> Optional[int]:
    for number, line in enumerate(lines, start=1):
        if line.startswith("#") and phrase.lower() in _heading_text(line):
            return number
    return None


def _section(lines: list[str], phrase: str) -> tuple[list[str], Optional[int]]:
    start = _heading_line(lines, phrase)
    if start is None:
        return [], None
    content: list[str] = []
    for line in lines[start:]:
        if content and line.startswith("## "):
            break
        content.append(line)
    return content, start


def _expand_requirement_ids(text: str) -> set[str]:
    ids = {f"FR-{int(number):03d}" for number in FR_RE.findall(text)}
    for first, last in RANGE_RE.findall(text):
        first_number = int(first.split("-")[1])
        last_number = int(last.split("-")[1])
        ids.update(f"FR-{number:03d}" for number in range(first_number, last_number + 1))
    return ids


def _check_metadata(lines: list[str], kind: str) -> list[Issue]:
    values, locations = _metadata(lines)
    issues: list[Issue] = []
    for field in REQUIRED_METADATA:
        if not values.get(field):
            issues.append(
                _issue(
                    "MISSING_METADATA",
                    "error",
                    locations.get(field, 1),
                    f"required metadata field is missing or empty: {field}",
                )
            )

    status = values.get("Status", "").lower()
    status_line = locations.get("Status", 1)
    if status and status not in ALLOWED_STATUSES:
        issues.append(_issue("INVALID_STATUS", "error", status_line, f"unsupported status: {status}"))
    elif status and status != "complete":
        issues.append(
            _issue(
                "INCOMPLETE_STATUS",
                "error",
                status_line,
                f"artifact status {status!r} cannot pass a phase handoff as complete",
            )
        )

    phase = values.get("Phase", "").lower()
    expected = EXPECTED_PHASES[kind]
    if phase and not any(token in phase for token in expected):
        issues.append(
            _issue(
                "INVALID_PHASE",
                "error",
                locations.get("Phase", 1),
                f"phase {phase!r} does not match artifact kind {kind}",
            )
        )

    pipeline = values.get("Pipeline", "")
    if pipeline:
        missing = [name for name in PIPELINE_PHASES if name not in pipeline.lower()]
        if missing or not any(marker in pipeline for marker in ("☐", "☑", "▶")):
            detail = f"; missing phases: {', '.join(missing)}" if missing else ""
            issues.append(
                _issue(
                    "INVALID_PIPELINE",
                    "error",
                    locations.get("Pipeline", 1),
                    f"pipeline must list the native phases and a gate marker{detail}",
                )
            )

    rule_inventory = values.get("Rule inventory", "")
    if not rule_inventory and not _has_heading(lines, "repository rule inventory"):
        issues.append(
            _issue(
                "MISSING_RULE_INVENTORY",
                "error",
                locations.get("Rule inventory", 1),
                "artifact must link the canonical rule inventory or contain the repository rule inventory",
            )
        )
    if kind == "design" and not _has_heading(lines, "repository rule inventory"):
        issues.append(
            _issue(
                "MISSING_RULE_INVENTORY",
                "error",
                locations.get("Rule inventory", 1),
                "the design must contain the canonical Repository Rule Inventory section",
            )
        )

    if not values.get("Analysis"):
        issues.append(
            _issue(
                "MISSING_ANALYSIS_LINK",
                "error",
                locations.get("Analysis", 1),
                "artifact must link the durable analysis/findings artifact",
            )
        )
    return issues


def _check_pipeline_and_sections(lines: list[str], kind: str) -> list[Issue]:
    issues: list[Issue] = []
    for phrase in REQUIRED_HEADINGS[kind]:
        if not _has_heading(lines, phrase):
            issues.append(
                _issue(
                    "MISSING_SECTION",
                    "error",
                    1,
                    f"required {kind} section is missing: {phrase}",
                )
            )
    return issues


def _check_ledger(lines: list[str], kind: str) -> list[Issue]:
    ledger_line = _heading_line(lines, "decision ledger")
    if ledger_line is None:
        return [] if kind != "design" else [
            _issue("MISSING_LEDGER", "error", 1, "design must contain a Decision Ledger")
        ]

    rows: list[tuple[int, list[str]]] = []
    for number, line in enumerate(lines[ledger_line:], start=ledger_line):
        if number > ledger_line and line.startswith("## "):
            break
        if not line.lstrip().startswith("|") or set(line.replace("|", "").strip()) <= {"-", ":", " "}:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] not in {"#", "ID"} and "Decision" not in cells:
            rows.append((number, cells))

    if not rows:
        return [_issue("EMPTY_LEDGER", "error", ledger_line, "Decision Ledger has no decision rows")]

    issues: list[Issue] = []
    for number, cells in rows:
        if len(cells) < 7:
            issues.append(_issue("MALFORMED_LEDGER_ROW", "error", number, "Decision Ledger row has too few columns"))
            continue
        checks = (
            (3, "EMPTY_LEDGER_EVIDENCE", "evidence"),
            (4, "EMPTY_LEDGER_OWNER", "owner"),
            (5, "EMPTY_LEDGER_TIER", "tier"),
            (6, "EMPTY_LEDGER_STATUS", "status"),
        )
        for index, code, label in checks:
            if not cells[index]:
                issues.append(_issue(code, "error", number, f"Decision Ledger {label} must not be empty"))
    return issues


def _check_traceability(lines: list[str], kind: str) -> list[Issue]:
    if kind not in {"spec", "plan"}:
        return []
    if kind == "spec":
        requirement_section, requirement_line = _section(lines, "functional requirements")
        coverage_section, coverage_line = _section(lines, "requirement traceability")
        if not coverage_section:
            coverage_section, coverage_line = _section(lines, "scenario coverage matrix")
    else:
        requirement_section, requirement_line = _section(lines, "scope and requirement coverage")
        coverage_section, coverage_line = requirement_section, requirement_line

    required = _expand_requirement_ids("\n".join(requirement_section))
    covered = _expand_requirement_ids("\n".join(coverage_section))
    if not required or not coverage_section:
        return [
            _issue(
                "MISSING_REQUIREMENT_TRACE",
                "error",
                coverage_line or requirement_line or 1,
                f"{kind} must map requirements to acceptance coverage and verification",
            )
        ]
    missing = sorted(required - covered)
    if missing:
        return [
            _issue(
                "MISSING_REQUIREMENT_TRACE",
                "error",
                coverage_line or 1,
                f"requirements missing from traceability coverage: {', '.join(missing)}",
            )
        ]
    return []


def _check_completion(lines: list[str], metadata: dict[str, str], locations: dict[str, int]) -> list[Issue]:
    if metadata.get("Status", "").lower() != "complete":
        return []
    issues: list[Issue] = []
    for number, line in enumerate(lines, start=1):
        normalized = line.lower()
        marker_is_explanatory = "no unresolved" in normalized or "without unresolved" in normalized
        if not marker_is_explanatory and any(pattern.search(line) for pattern in PLACEHOLDER_PATTERNS):
            issues.append(
                _issue(
                    "COMPLETION_PLACEHOLDER",
                    "error",
                    number,
                    "completed artifact contains an unresolved placeholder",
                )
            )
    verification = metadata.get("Last verification", "")
    if not verification:
        issues.append(
            _issue(
                "MISSING_VERIFICATION",
                "error",
                locations.get("Last verification", 1),
                "completed artifact must include a Last verification record",
            )
        )
    return issues


def _check_warnings(metadata: dict[str, str], locations: dict[str, int]) -> list[Issue]:
    assumptions = metadata.get("Open assumptions / risks", "")
    if re.search(r"\b(?:warning|risk):", assumptions, re.IGNORECASE):
        return [
            _issue(
                "OPEN_RISK",
                "warning",
                locations.get("Open assumptions / risks", 1),
                "open assumptions or risks are recorded and remain visible to the phase gate",
            )
        ]
    return []


def validate_artifact(path: Path, kind: str) -> list[Issue]:
    """Read one artifact without mutation and return sorted validation issues."""
    if kind not in KINDS:
        raise ValueError(f"unsupported artifact kind: {kind}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    metadata, locations = _metadata(lines)
    issues = []
    issues.extend(_check_metadata(lines, kind))
    issues.extend(_check_pipeline_and_sections(lines, kind))
    issues.extend(_check_ledger(lines, kind))
    issues.extend(_check_traceability(lines, kind))
    issues.extend(_check_completion(lines, metadata, locations))
    issues.extend(_check_warnings(metadata, locations))
    return sorted(issues, key=lambda item: (item.line is None, item.line or 0, item.code, item.severity, item.message))


def _payload(artifact: str, kind: str, issues: list[Issue]) -> dict[str, object]:
    return {
        "artifact": artifact,
        "kind": kind,
        "valid": not any(issue.severity == "error" for issue in issues),
        "issues": [asdict(issue) for issue in issues],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", required=True, help="path to one Markdown artifact")
    parser.add_argument("--kind", required=True, choices=KINDS, help="artifact kind")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = _parser().parse_args(argv)
    path = Path(args.artifact)
    try:
        issues = validate_artifact(path, args.kind)
    except (OSError, UnicodeError, ValueError) as exc:
        issue = _issue("INVOCATION_FAILURE", "error", None, str(exc))
        payload = _payload(str(path), args.kind, [issue])
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, sort_keys=False))
        else:
            print(f"invalid invocation: {exc}")
        return 2

    payload = _payload(str(path), args.kind, issues)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, sort_keys=False))
    else:
        print(f"artifact: {path}")
        print(f"kind: {args.kind}")
        print(f"valid: {payload['valid']}")
        for issue in issues:
            location = f"line {issue.line}" if issue.line else "no line"
            print(f"{issue.severity}: {issue.code} ({location}) — {issue.message}")
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
