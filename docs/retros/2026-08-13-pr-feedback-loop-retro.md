# PR Feedback Loop — Devarm Retro

**Document type:** Retro report  
**Date:** 2026-08-13  
**Status:** complete; method edits uncommitted  
**Phase:** retro  
**Feature/change:** Tech Catalyst PR-feedback redesign and follow-up runtime contract review  
**Track:** standard  
**Pipeline:** brainstorm ▶ ground ▶ spec ▶ clarify ▶ plan ▶ tasks ▶ analyze ▶ implement ▶ review ▶ finish ▶ retro  
**Target repository:** `/Users/dphadatare/vhosts/tech-catalyst-v2`  
**Target branch:** `task/dev-0/pr-review-feedback-loop`  
**Method repository:** `/Users/dphadatare/vhosts/devarm`  
**Method branch:** `001-devarm-purpose-evolution`  
**Next gate:** developer review of this retro, then an explicit commit decision  
**Related artifacts:** `docs/design/2026-07-22-pr-review-feedback-response-loop-design.md`, `specs/021-pr-review-feedback-loop/`, `skills/devarm-analyze/SKILL.md`, `skills/devarm-tasks/SKILL.md`

## 1. Scope and evidence

This retro covers the design, implementation, review, and local runtime reasoning for the PR
feedback loop. It includes the later questions about phase-specific prompt injection, completed
tickets with open PRs, Jira/manual reruns occurring with an unaddressed PR comment, and active-job
watermark behavior.

The feature artifacts and current code were treated as authoritative over earlier conversation
summaries. The useful evidence was:

- The design ledger locked the poller as detection/requeue only, fresh PR reads in remediation,
  early source-repository routing, normal remediation outcomes, marker-based completion, open-PR
  polling, and preservation of pending feedback while a job is active.
- The implementation and tests preserved the existing diagnosis/action loop and its
  `works_as_designed` / no-change path. A sibling or primary repository that needs no change is
  therefore not, by itself, an escalation.
- Prompt-routing verification showed that PR-feedback context belongs at intake, repository
  analysis, synthesis, and code-fix boundaries, not in every OpenCode session. The production
  routing and its characterization tests were added late in the session.
- The completed-ticket question exposed a missing lifecycle cross-product test. Existing
  behavior continued to consider an open tracked PR even when the ticket was completed; the
  characterization was clarified without requiring a production change.
- The Jira/manual-rerun plus PR-comment question exposed a missing cross-channel timing contract.
  The intended behavior is independent triggers serialized by the active-job guard: a PR comment
  remains pending while a manual run is active, and a later PR-feedback poll performs the fresh
  read when no active job remains.

The prior devarm generalization gate was applied. The proposed rule is category-scoped because
the evidence is strong for re-entrant multi-actor workflows but does not justify adding a matrix
to every single-trigger feature.

## 2. Session arc

1. The design moved from a special PR-feedback workflow toward a normal remediation rerun with
   fresh GitHub context. The source PR became trigger/routing evidence rather than a hard write
   boundary.
2. Grounding established reuse of early repository routing, existing diagnosis/synthesis, the
   existing partial/no-change behavior, and marker-based PR completion. The design explicitly
   rejected a new feedback-specific repair cap and legacy runtime support.
3. Specification, plan, tasks, and analyze artifacts captured the core PR state machine: open PRs
   can wake work; active jobs leave feedback pending; queued work is not canceled merely because
   the source PR later closes; and normal remediation decides whether a change, no-op, reply, or
   escalation is appropriate.
4. Implementation and review found a prompt-context scope issue: the feedback wording had leaked
   into every OpenCode session. The fix narrowed injection to the phases that consume it and added
   routing tests.
5. A status-policy question surfaced a silently made decision: whether a closed PR should remain
   eligible for feedback polling. The eventual contract became “only live-open PRs wake the
   poller; a queued run is not canceled if the source later closes,” but that source-eligibility
   choice should have been presented as an explicit user-owned decision before implementation.
6. Runtime-oriented follow-up questions then exercised lifecycle and trigger combinations that
   were not explicit in the original planning artifacts. Those questions are the main method
   improvement from this retro.

## 3. What held

These decisions survived the session and should remain unchanged:

| Decision | Why it held | Method action |
|---|---|---|
| Poller detects and requeues; remediation decides | Keeps GitHub polling thin and preserves existing diagnosis ownership | Preserve current gate |
| Fresh PR read at remediation intake | Avoids stale comments and lets the current PR state guide the run | Preserve current gate |
| Source PR is evidence, not a hard target | Allows existing primary/sibling diagnosis to determine actual scope | Preserve current gate |
| Existing no-change / already-satisfied outcomes remain valid | Prevents a sibling or primary no-op from being mistaken for escalation | Preserve current gate |
| No new feedback-specific repair cap | The existing diagnosis/action loop already controls repair iteration | Preserve current gate |
| TC-authored activity is completed by the existing marker contract | Avoids a second durable feedback state machine in TC | Preserve current gate |
| Open PR polling is independent of ticket completion | A completed ticket can still have a live PR needing review follow-up | Preserve current gate; add explicit coverage |

## 4. Late decisions and missing contracts

| Finding | Layer | Should have been caught | Assessment |
|---|---|---|---|
| PR-feedback prompt context must be phase-scoped | Binding/prompt routing seam | Ground consumer audit, then plan/spec/tasks wording-lock and routing test | Late implementation decision; fixed in the target repo |
| Completed ticket plus open tracked PR remains pollable | Lifecycle/poller seam | Spec scenario and tasks state-table cell | No production defect confirmed; contract/test coverage was missing |
| Jira/manual rerun and PR comment can coexist | Orchestration/re-entrancy seam | Analyze Pass 3 timing matrix and tasks negative tests | No new production defect confirmed; behavior was reconstructed late |
| PR update while an active run exists must not consume feedback | Poller watermark/claim seam | Analyze state table and tasks side-effect assertions | Core design had the active-job rule, but not the full trigger-channel cross-product |
| Closed PR feedback eligibility was inferred before being explicitly locked | Source-eligibility policy seam | Brainstorm/Analyze `owner: user` decision with an open-versus-closed source matrix | Process defect: the final D25 policy is explicit now, but the decision was surfaced late |

No locked Decision Ledger row was shown to be violated. The primary gap was that several
cross-channel decisions were implicit or answered during follow-up instead of being represented
as a single artifact contract with a test for each meaningful cell.

## 5. Back-and-forth drivers

The repeated clarification was not primarily caused by the core design changing. It was driven by
three missing views:

- a phase-consumer map for prompt/context injection;
- a lifecycle cross-product for ticket status versus live PR status; and
- a timing matrix for independent PR-poll and Jira/manual triggers around an active run.

The existing artifacts had narrative flows and a partial state table, but they did not force those
three views to be walked together. That allowed implementation and runtime questions to surface
otherwise foreseeable decisions late.

The closed-PR question adds a fourth driver: status-based eligibility was treated as an existing
behavior detail instead of a product decision. The correct method response is to make the
alternatives visible (continue polling, stop polling, or poll only while open), recommend one,
and record the answer before implementation.

## 6. Generalization and promotion decision

### Failure category

Cross-channel/re-entrant workflow state ambiguity: multiple actors can submit work for the same
entity while an execution attempt is idle, active, completed, or nominally terminal.

### Domain-neutral invariant

For every trigger source × entity lifecycle state × event timing combination, the workflow must
name its owner, terminal outcome, and side effects for pending work, acknowledgement,
watermark/cursor, claim/lease, duplicate prevention, and terminal-state handling. A terminal
status must not suppress live external work unless that suppression is an explicit decision.

### Enforcement point

- `skills/devarm-analyze/SKILL.md`: a required cross-channel trigger/timing matrix in Pass 2 when
  two or more trigger channels or an external requeue source exists; status-based source
  eligibility is explicitly an `owner: user` Pass 3 decision.
- `skills/devarm-tasks/SKILL.md`: acceptance tests for the timing cells and negative assertions
  for lost work, duplicate scheduling, suppressed live work, and terminal-state downgrade.
- `tests/test_method_contracts.py`: a wording-lock contract for the two native gates.

### Applicability boundary

This applies to multi-actor/re-entrant workflows with two or more intake/trigger channels, or an
external poller/webhook that can wake or requeue work also rerunnable by an operator. It does not
apply to a single-trigger, non-reentrant feature merely because it has lifecycle states.

### Generalization check

The rule holds for the evidence-backed shape of GitHub review polling combined with Jira/manual
reruns, and for the broader shape of an external reconciliation/webhook source combined with an
operator retry queue. The second shape is a category check rather than a claim about a current
Tech Catalyst implementation. That boundary supports the **category-scoped** promotion outcome,
not a universal portable-core rule.

### Method inventory entry

Native devarm gate. Input: multi-channel/re-entrant workflow evidence. Output: analyze timing
matrix plus decision-to-test tasks. Reuse: any external poller/webhook paired with manual or
operator rerun. No adapter, runtime dependency, persistence change, or product-specific rule was
added to devarm.

## 7. Edits applied

Uncommitted edits in `/Users/dphadatare/vhosts/devarm`:

- Added the category-scoped timing-matrix requirement to `skills/devarm-analyze/SKILL.md`.
- Added the explicit `owner: user` rule for status-based source eligibility.
- Added the corresponding decision-to-test and negative-side-effect requirement to
  `skills/devarm-tasks/SKILL.md`.
- Added a contract regression test to `tests/test_method_contracts.py`.
- Added this retro report.
- Added the dated provenance entry to `CHANGELOG.md`.

The existing `devarm-retro` generalization gate was retained and reused; it did not need another
normative edit.

## 8. Verification

The feature-repository implementation had already been verified during the session with focused
PR-feedback/prompt-routing tests, compilation, and targeted diff checks. This retro does not alter
the feature repository.

For this method change, the current verification is:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v  # 88 tests, OK
git diff --check                                      # clean
```

The validator has no `retro` artifact kind; attempting `--kind retro` is rejected by its CLI.
The current devarm artifact validation was also run. The purpose-evolution design/spec/plan/tasks/
analysis/findings set returned `valid: true` with no issues. Two pre-existing artifacts in the
separate retro-generalization work were not clean: its design has the unsupported status
`approved`, its plan lacks requirement traceability, and its analysis lacks the required Pass 1,
Pass 2, Pass 3, Pass 3 status, and scope/evidence sections. Those unrelated artifact defects are
recorded here and left untouched to preserve the existing devarm work.

This report is therefore checked by the native method contract tests and `git diff --check`; the
validator limitation and pre-existing artifact findings are visible rather than treated as an
approval.

## 9. Suggested commit

```text
retro: require cross-channel trigger timing coverage
```

No commit was created. The developer must review the report and explicitly choose whether to
commit these devarm changes.
