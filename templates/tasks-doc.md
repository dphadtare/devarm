# <Feature> — Tests-first Tasks

This native fallback is a repository-local artifact. It uses no front matter and no database.
Each behavior is locked by a failing test before production implementation.

## Execution contract

Follow RED → GREEN → refactor → verify. Do not commit without explicit developer authorization.

## Setup

<Baseline commands and environment checks.>

## Foundational work

<Shared harness and contract tasks.>

## Story groups

### T001 [RED] <behavior>

**Files:** `<exact paths>`
**Requirements/decisions:** FR-001; D1.

Write the failing test and record the expected failure.

### T002 [GREEN] <implementation>

Implement only the behavior locked by T001, then run the focused and regression suites.

## Polish and verification

<Refactoring, integration, performance, and full-suite commands.>

## Self-check

- [ ] Every implementation task has a preceding tests-first task.
- [ ] Every requirement and Decision Ledger row has enforcement coverage.
- [ ] Actual command output is recorded before completion is claimed.
