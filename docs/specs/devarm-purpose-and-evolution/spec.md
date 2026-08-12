# Devarm Purpose and Evolution — Specification

**Document type:** Functional specification
**Date:** 2026-08-12
**Status:** complete
**Track:** standard
**Pipeline:** brainstorm ☑ ground ☑ spec ☑ clarify ☑ plan ☑ tasks ☑ analyze ☑ implement ▶ review ☐ finish ☐
**Phase:** specification and clarification
**Feature/change:** Devarm purpose and evolution
**Design:** [`docs/design/2026-08-12-devarm-purpose-and-evolution-design.md`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md)
**Rule inventory:** [`design.md#repository-rule-inventory`](../../design/2026-08-12-devarm-purpose-and-evolution-design.md#repository-rule-inventory)
**Tasks:** [`tasks.md`](tasks.md)
**Analysis:** [`analysis.md`](analysis.md)
**Target repository:** `/Users/dphadatare/vhosts/devarm`
**Target branch:** `001-devarm-purpose-evolution`
**Last session note:** T001–T016 and the devarm-analyze re-gate are complete on the feature branch; the next phase is review.
**Last verification:** 2026-08-13 — 85 tests passed; design/spec/plan/tasks/analysis validator checks returned `valid: true`; `git diff --check` passed.
**Open assumptions / risks:** No unresolved clarification or ledger assumptions; source-rule boundary is recorded in the design. Review findings F1–F3 and F5 require remediation before finish.
**Next gate:** `devarm-implement` to address review findings.
**Related artifacts:** `design.md`, `plan.md`, `tasks.md`, `analysis.md`, and `findings.md`.

## 1. Overview

Devarm helps a developer and an AI agent make consequential changes in an existing software
repository without silently inventing design decisions, missing repository constraints, or
claiming completion without evidence.

Devarm must remain a portable development method. Its native behavior is expressed through phase
guidance and repository-local artifacts. It may use lightweight deterministic checks and optional
adapters, but it must not require a hosted service, database, command-line runtime, or particular
agent platform.

## 2. Scope

### In scope

- A flagship workflow for consequential changes in existing repositories.
- Request classification and adaptive quick/standard process depth.
- Repository-rule discovery, applicability, precedence, and recording.
- Grounded design, testable specification, planning, tests-first tasks, analysis, implementation,
  review, finish, and retro gates.
- Durable phase state, Decision Ledger entries, assumptions, evidence, and handoffs.
- Failure, interruption, partial-completion, dirty-worktree, and resume semantics.
- Lightweight deterministic validation of artifact and gate conditions.
- Optional external adapters that cannot bypass native devarm gates.

### Out of scope

- A hosted workflow service or required state database.
- Replacing a target repository’s architecture, security, CI, product, or contribution rules.
- Replacing Git hosting, issue tracking, CI, Spec Kit, or domain-specific skills.
- Applying the standard process to trivial questions, simple documentation edits, or ordinary
  exploration unless explicitly requested.
- Autonomous commit, push, merge, delete, reset, discard, or other consequential external action.
- Language-, framework-, database-, or deployment-specific application conventions in devarm core.

## 3. Terminology and states

- **Consequential change:** a feature, behavior change, meaningful bug fix, refactor, persistence
  change, contract change, architecture change, or devarm method change.
- **Quick track:** a small, low-risk change whose scope remains within the approved quick-track
  boundary; it retains safety gates while using compact artifacts.
- **Standard track:** the full gated workflow for all other consequential changes.
- **Target rule:** an instruction supplied by the repository being changed, including repository
  guidance, constitutions, rule files, contribution rules, and local workflow instructions.
- **Decision Ledger:** the durable record of load-bearing choices, alternatives, owners, evidence,
  and status.
- **Evidence:** current source/configuration, command output, tests, runtime/CI results, or other
  directly supporting material; stale summaries and prose are context, not confirmation.
- **Phase status:** `draft`, `awaiting approval`, `in progress`, `blocked`, `partially completed`,
  `failed`, or `complete`.

## 4. User stories

### P1 — Complete a grounded repository change

**As a developer, I want an AI agent to take a consequential change from request to verified
completion through explicit gates, so that important decisions are made before implementation
and the result is reviewable.**

**Independent Test:** Give devarm a representative change in an existing repository and verify
that it classifies the work, discovers applicable rules, produces a grounded design and testable
specification, creates an executable plan and tests-first tasks, blocks implementation until the
pre-implementation gate passes, and produces verification evidence before completion.

#### Acceptance scenarios

```gherkin
Scenario: Standard-track change reaches implementation only after its gates pass
  Given a consequential change in an existing repository
  When the developer approves the grounded design and the specification, plan, tasks, and analysis gates pass
  Then implementation is permitted
  And the phase artifacts identify the decisions, constraints, expected tests, and next handoff

Scenario: Unresolved design intent blocks implementation
  Given a consequential change with an unanswered design-level decision
  When the agent reaches the implementation gate
  Then implementation is blocked
  And the unresolved decision is surfaced to the developer

Scenario: Completion requires current verification evidence
  Given implementation is finished but the proving checks have not run in the current turn
  When the agent evaluates completion
  Then it does not claim the change is complete
  And it records the missing verification as an open condition
```

### P2 — Apply repository rules without losing portability

**As a developer, I want devarm to discover and apply my repository’s own rules, so that project
constraints govern the work without being hard-coded into devarm.**

**Independent Test:** Run a change against a repository with applicable rule files and another
repository without them; verify the first records and applies its rules while the second uses
devarm defaults only where no repository rule exists.

#### Acceptance scenarios

```gherkin
Scenario: Target rules take precedence
  Given the target repository defines a rule for a concern that devarm also addresses
  When the agent plans or reviews the change
  Then the target rule governs
  And the artifact records the rule source, applicability, enforcement phase, and evidence

Scenario: Rule conflict is visible
  Given two applicable instruction sources conflict
  When the agent discovers the conflict
  Then it does not silently choose a rule
  And it records the precedence decision and asks the developer when intent is affected

Scenario: Project-specific rules remain outside devarm core
  Given a target repository has framework- or path-specific conventions
  When devarm runs in that repository
  Then it consumes those conventions through the target-rule inventory
  And devarm core does not require those conventions in another repository
```

### P2 — Resume safely after interruption or partial completion

**As a developer, I want interrupted work to preserve progress and resume from a verified
checkpoint, so that I do not have to reconstruct decisions and do not lose unrelated changes.**

**Independent Test:** Interrupt a run after a phase has produced partial output, alter or inspect
the repository state, and resume; verify that the agent revalidates the state, preserves completed
work, and does not treat partial output as final.

#### Acceptance scenarios

```gherkin
Scenario: Partial phase output remains recoverable
  Given a phase has produced some artifacts but has not passed its gate
  When the phase stops
  Then the artifacts and evidence remain available
  And the phase is marked partially completed, blocked, or failed as appropriate
  And later phases cannot treat it as complete

Scenario: Resume revalidates current state
  Given a prior run stopped before a phase gate
  When the developer resumes the work
  Then the agent checks the current branch, worktree, rules, artifacts, and changed files
  And it reports any drift before continuing

Scenario: Unrelated dirty-worktree changes are preserved
  Given the active checkout contains changes unrelated to the requested work
  When the agent prepares consequential changes
  Then it preserves those changes
  And it uses an isolated workspace or obtains explicit direction before mixing the changes
```

### P2 — Validate deterministic safety conditions

**As a developer, I want lightweight checks to catch incomplete artifacts and unsafe handoffs, so
that deterministic gates are not left to memory or prose alone.**

**Independent Test:** Give a validator complete and deliberately incomplete artifacts; verify it
accepts the complete set, identifies each deterministic defect in the incomplete set, and does not
pretend to resolve judgment-based design questions.

#### Acceptance scenarios

```gherkin
Scenario: Complete artifacts pass deterministic checks
  Given phase artifacts contain required sections, status, ownership, evidence, mappings, and handoff data
  When the deterministic checks run
  Then they pass
  And the result identifies the validated artifact set and rule set

Scenario: Missing deterministic evidence blocks the handoff
  Given an artifact lacks a required decision owner, requirement mapping, or verification record
  When the deterministic checks run
  Then they fail with the missing condition identified
  And the next phase is not presented as ready

Scenario: Validators do not replace human judgment
  Given an artifact contains two plausible design alternatives
  When the deterministic checks run
  Then they report the decision as requiring ownership or approval
  And they do not select an alternative automatically

Scenario: Repeated validation is deterministic
  Given the same artifact set and repository state
  When the validation is repeated without other changes
  Then it produces the same result
```

### P3 — Extend the method without bypassing its core

**As a method maintainer, I want proven external practices and project-specific workflows to be
usable as adapters, so that devarm can improve without becoming dependent on any one ecosystem.**

**Independent Test:** Run a change with an optional adapter present and absent; verify native gates
still run in both cases and adapter use is recorded.

#### Acceptance scenarios

```gherkin
Scenario: Optional adapter is recorded
  Given an external template, tool integration, or project skill is used
  When the phase completes
  Then the method inventory records the adapter, its output, and its reuse value

Scenario: Native gates remain authoritative
  Given an adapter supplies templates or workflow guidance
  When the adapter completes
  Then devarm still performs its required grounding, approval, verification, and handoff checks
  And the adapter cannot silently mark a native gate complete

Scenario: Devarm works without an adapter
  Given no optional adapter is available
  When the same change is run
  Then the native devarm workflow remains usable
```

## 5. Functional requirements

### Request, scope, and process depth

- **FR-001:** Devarm SHALL classify each requested action as ordinary work, quick-track work,
  standard-track work, or a request to improve the method before applying consequential-change
  gates.
- **FR-002:** Devarm SHALL use the standard track for consequential work unless the change meets
  the quick-track boundary and no later discovery widens its scope.
- **FR-003:** If a quick-track change introduces persistence, a contract change, or a wider blast
  radius, devarm SHALL stop the quick track, record the discovery, and upgrade the work to the
  standard track.
- **FR-004:** Devarm SHALL identify the active repository and branch before planning or changing
  a repository.

### Rules and grounding

- **FR-005:** Before a phase acts, devarm SHALL discover applicable repository instructions and
  record the relevant sources, including their applicability and enforcement phase.
- **FR-006:** When a target-repository rule conflicts with a devarm default, the target rule SHALL
  take precedence.
- **FR-007:** When instruction sources conflict in a way that changes scope, behavior, or safety,
  devarm SHALL surface the conflict for a developer decision rather than silently resolving it.
- **FR-008:** Before a design is approved, devarm SHALL verify reuse and integration claims against
  current code, current rules, and live wiring, with directly supporting evidence.
- **FR-009:** Grounding SHALL identify affected boundaries, consumers, compatibility obligations,
  failure posture, and runtime instruction contracts, or explicitly mark them not applicable.

### Decisions and artifacts

- **FR-010:** Each consequential change SHALL have one canonical chain of repository-local phase
  artifacts; devarm SHALL not maintain parallel hand-edited planning systems for the same change.
- **FR-011:** The governing design artifact SHALL record load-bearing decisions, alternatives,
  owner, evidence, tier, and status in a Decision Ledger.
- **FR-012:** A design-level decision SHALL require explicit developer approval before the workflow
  advances past the relevant gate.
- **FR-013:** An unanswered decision SHALL be marked as awaiting confirmation and SHALL not be
  treated as approval.
- **FR-014:** Each phase artifact SHALL record its phase, status, repository and branch context,
  last verification, open assumptions or risks, next gate, and related artifacts.
- **FR-015:** When a settled decision changes, devarm SHALL supersede the old decision, record the
  new decision, and check dependent design and planning content for required updates.

### Execution and safety

- **FR-016:** Devarm SHALL block implementation until the grounded design is approved, the
  requirements are testable, tests-first tasks exist, and the pre-implementation analysis gate
  is clean.
- **FR-017:** Implementation work SHALL preserve unrelated tracked and untracked changes and
  SHALL use isolation or obtain explicit direction when the active checkout is unsafe.
- **FR-018:** Devarm SHALL preserve artifacts, evidence, and authorized code changes when a phase
  fails, is interrupted, or partially completes.
- **FR-019:** A failed or partial phase SHALL be distinguishable from a completed phase, and later
  gates SHALL reject incomplete predecessor output.
- **FR-020:** Devarm SHALL revalidate the current repository state before resuming work after an
  interruption or session gap.
- **FR-021:** Devarm SHALL allow local inspection, artifact work, tests, and verification without
  requiring approval for each command, while requiring explicit approval for commits, pushes,
  merges, deletion, reset, discard, and other consequential external actions.

### Verification and quality

- **FR-022:** Every requirement SHALL map to at least one acceptance scenario and one test or
  explicit verification step before implementation begins.
- **FR-023:** Devarm SHALL require real verification evidence before claiming that work is done,
  fixed, passing, or complete.
- **FR-024:** When a test mocks the seam needed to prove a behavior, devarm SHALL identify the
  limitation and require a real seam check, integration test, or live smoke before treating the
  behavior as fully verified.
- **FR-025:** Each change SHALL classify relevant security, performance, reliability,
  accessibility, observability, and compatibility concerns as required, deferred with risk, or
  not applicable with a reason.
- **FR-026:** Deterministic checks SHALL identify missing required sections, unresolved
  placeholders, missing decision ownership or evidence, unmapped requirements, missing handoff
  status, and completion claims without verification evidence.
- **FR-027:** Deterministic checks SHALL not select among competing design choices or replace
  developer judgment.
- **FR-028:** For an unchanged artifact set and repository state, deterministic checks SHALL
  produce the same result on repeated runs.

### Portability and improvement

- **FR-029:** Devarm SHALL remain usable without a hosted service, state database, mandatory CLI,
  or specific agent platform.
- **FR-030:** Optional adapters SHALL be recorded in a method inventory and SHALL not bypass native
  devarm gates.
- **FR-031:** Retro output SHALL connect recurring failures or late decisions to proposed changes
  in skills, templates, validators, documentation, or adapter contracts.
- **FR-032:** A devarm method improvement SHALL include its motivating evidence and a verification
  approach before it is considered complete.

## 6. Scenario coverage matrix

| Scenario class | Covered by | Status |
|---|---|---|
| Primary flow | P1, FR-001–FR-004, FR-010–FR-016 | Included |
| Alternate flow | P2 rules, P3 adapters, FR-002–FR-003, FR-005–FR-007, FR-029–FR-030 | Included |
| Exception/error | P1 unresolved decision, P2 conflict, validator failure, FR-018–FR-021, FR-026–FR-027 | Included |
| Recovery/resume | P2 interruption and dirty-worktree scenarios, FR-018–FR-020 | Included |
| Non-functional | P2 portability and deterministic validation, FR-023–FR-029 | Included |
| User-experience surface | Phase statuses, explicit handoffs, surfaced conflicts and risks | Included |

### Requirement traceability

| Requirement group | Acceptance coverage | Success criteria |
|---|---|---|
| FR-001–FR-004 | P1 standard-track, quick-track, and active-repository scenarios | SC-001, SC-002 |
| FR-005–FR-009 | P2 target-rule, conflict, and project-specific-rule scenarios | SC-003 |
| FR-010–FR-015 | P1 gate and unresolved-decision scenarios | SC-001, SC-002, SC-004 |
| FR-016–FR-021 | P1 implementation gate plus P2 interruption, resume, and dirty-worktree scenarios | SC-002, SC-004, SC-005 |
| FR-022–FR-025 | P1 completion scenario and risk-based quality coverage | SC-001, SC-006, SC-010 |
| FR-026–FR-028 | P2 deterministic-validator scenarios | SC-006, SC-007, SC-008 |
| FR-029–FR-032 | P3 adapter-present, adapter-absent, and retro scenarios | SC-009, SC-010 |

## 7. Success criteria

- **SC-001:** In a representative standard-track run, 100% of required phase handoffs identify
  their predecessor artifact, current status, next gate, open decisions, and verification state.
- **SC-002:** In validation tests, no implementation run proceeds when the grounded-design
  approval, required predecessor artifact, or clean pre-implementation analysis gate is missing.
- **SC-003:** In a repository-rule fixture, every applicable rule used by the change appears in the
  rule inventory with source, applicability, enforcement phase, and supporting evidence.
- **SC-004:** In interruption-and-resume tests, 100% of accepted decisions remain available after
  interruption, partial output is not treated as complete, and repository drift is reported before
  continuation.
- **SC-005:** In dirty-worktree tests, 100% of unrelated tracked and untracked changes remain
  unchanged after devarm prepares or executes the requested isolated work.
- **SC-006:** In artifact validation tests, each deliberately introduced deterministic defect is
  reported, and the complete fixture passes without requiring network access or a hosted service.
- **SC-007:** Repeating validation against an unchanged artifact set produces identical findings
  and status in 100% of repeated runs.
- **SC-008:** For a local artifact set of up to 20 phase documents, the deterministic validation
  completes within 10 seconds on a supported developer workstation.
- **SC-009:** In adapter-present and adapter-absent tests, the same native safety gates execute and
  no adapter alone can mark a native gate complete.
- **SC-010:** Every shipped devarm method improvement links its changed guidance or validator
  behavior to motivating evidence and a passing verification result.

## 8. Dependencies

- A target repository with an identifiable working tree and branch when repository work is in
  scope.
- Access to the target repository’s applicable instructions and current source/configuration for
  grounding.
- A way to run the target repository’s relevant verification commands when implementation is in
  scope.
- Developer participation for design-level decisions, approvals, and consequential lifecycle
  actions.
- Optional adapters only when a target repository or tool explicitly provides them.

## 9. Assumptions

- Repository-local artifacts are reviewable and persist through the normal repository workflow.
- The developer can approve or reject design-level decisions and can provide direction when
  repository rules conflict.
- “Current evidence” means evidence gathered during the active phase or resumed validation, not
  a prior session’s unverified claim.
- A ten-second validation target is appropriate for the first deterministic validator set and is
  measured on a local developer workstation, not a remote service.
- Existing historical artifacts may lack the common metadata contract; migration is required when
  they are resumed, not as a bulk rewrite.

## 10. Clarifications

No material clarification is currently required. The implementation-level choices are resolved
in the design Decision Ledger D21–D34 and recorded in the completed analyze artifact.

## 11. Quality gate checklist

- [x] No implementation details leak into the requirements; behavior is described at the method
  and developer-outcome level.
- [x] Requirements use testable, unambiguous language with explicit blocking and completion
  semantics.
- [x] Success criteria are measurable and do not depend on a particular programming language,
  framework, API, or hosted service.
- [x] Primary, alternate, exception/error, recovery, non-functional, and user-experience scenario
  classes are explicitly covered.
- [x] Scope, dependencies, assumptions, and non-goals are listed.
- [x] There are no unresolved `[NEEDS CLARIFICATION]` markers.
- [x] P1 is independently testable and forms a viable MVP workflow.
- [x] Each functional-requirement group maps to acceptance scenarios and success criteria.

**Checklist result:** PASS after two self-review passes, including requirement traceability.
