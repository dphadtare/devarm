---
name: "devarm-clarify"
description: "Use after devarm-spec (pre-plan) or during devarm-review (code-grounded) to resolve spec ambiguities with up to 5 targeted questions and write answers back into spec.md. Native devarm gate — does not require Spec Kit; may delegate to /speckit-clarify only when .specify/ exists AND feature-dir sanity passes."
metadata:
  phase: 4
  produces: "spec.md with Clarifications section + resolved FR/edge-case updates"
  next: "devarm-plan (pre-plan mode) or return to devarm-review (code-grounded mode)"
---

## Announce

"I'm using devarm-clarify to resolve spec ambiguities and record answers in the spec."

## Artifact and rule handoff contract

Before acting, record the active repository and branch in the artifact metadata. Discover
applicable target-repository instructions and link the canonical rule inventory; the
target-repository rule wins over a devarm default, and material conflicts require a visible
disposition. Run the optional validator; if it is unavailable, record the limitation and keep
the manual checklist authoritative. The optional validator is not required for the native method.
A deterministic blocking error stops the handoff; warnings remain visible and do not imply
approval. Preserve explicit approval gates and mark an unanswered decision `assumed — awaiting confirmation`.
If a settled decision is superseded, ripple-check dependent artifacts and re-check the affected
evidence before continuing. The native ambiguity gate records accepted clarifications into `spec.md`.

## Why this skill exists (native, not external)

Spec Kit's `/speckit-clarify` and similar tools encode a useful behavior: structured ambiguity
reduction before planning. **devarm owns that behavior** so the method does not depend on
Superpowers, Spec Kit, or Cursor commands. When `.specify/` exists, this skill may *delegate* to
`/speckit-clarify` — but the gate, output shape, and feature-dir sanity checks live here.

## Invocation preamble

Before clarifying:

1. Read this skill fully.
2. Resolve the **active feature spec path** (see Feature-dir sanity below) — never edit a spec
   returned by prerequisites if it does not match the branch/feature you are working on.
3. Load the grounded design Decision Ledger — clarifications must not contradict locked rows
   without an explicit superseding ledger entry.

## Modes

| Mode | When | Input | Output |
|------|------|-------|--------|
| **Pre-plan** | After `devarm-spec` quality gate, before `devarm-plan` | Draft `spec.md` + design ledger | Up to 5 questions → spec updates |
| **Code-grounded** | During `devarm-review` or user verification mid/late pipeline | Question + **implementation** | Answer from code first → reconcile spec to match reality |

**Pre-plan** resolves requirements ambiguity. **Code-grounded** resolves "does the built system
match the spec?" — answer from `file:line` evidence, then update spec Clarifications + FRs.

## Feature-dir sanity (required)

Before reading or writing any spec:

1. Identify the active feature from branch name (`NNN-short-name`), user statement, or
   `specs/NNN-*/spec.md` path already in use this session.
2. If using Spec Kit prerequisites (`check-prerequisites.sh --json --paths-only`), compare
   returned `FEATURE_SPEC` to the active feature. **If mismatch** (e.g. prerequisites say
   `019-*` but work is `032-*`), use the active feature path — do not edit the wrong spec.
3. Record which spec path was used in the completion report.

*Failure-class rationale (a prior failure): prerequisites resolved to a prior failure; agent correctly edited 032.*

## Pre-plan process

1. **Load spec** from the active feature path (`specs/<NNN-*/spec.md` or devarm fallback).
2. **Ambiguity scan** — mark each category Clear / Partial / Missing:
   - Functional scope & behavior, domain/data model, interaction flows, non-functional attributes,
     integrations, edge cases, constraints/tradeoffs, terminology, completion signals.
3. **Question queue** — max **5** questions total; one at a time; each must materially affect
   architecture, tests, or acceptance criteria. Prefer multiple-choice with a recommended option.
4. **After each accepted answer:**
   - Append to `## Clarifications` → `### Session YYYY-MM-DD` → `- Q: … → A: …`
   - Update the relevant FR / edge case / entity section immediately (no contradictory prose left).
   - Save spec after each integration.
5. **Stop when:** critical ambiguities resolved, user says done, or 5 questions asked.

## Code-grounded process

1. User asks a verification question (e.g. "will host X be supported?").
2. **Open the implementation** — grep/read the real code path; cite `file:line`.
3. If code matches an implicit spec gap, update spec Clarifications + FR/edge cases to match
   verified behavior (or flag a defect if code contradicts a locked ledger row).
4. Do **not** ask speculative clarifying questions when code already answers — report evidence.

## Spec Kit adapter (optional)

When `.specify/` exists **and** feature-dir sanity passes:

- You MAY run `/speckit-clarify` instead of reimplementing the question loop — **if** the user
  prefers Spec Kit UX or hooks are required.
- Regardless of delegate path, completion must include: questions count, spec path, sections
  touched, coverage summary, suggested next phase (`devarm-plan` or back to review).

If `.specify/` is absent, run the native process above using devarm spec locations.

## Quality gate (before hand off)

- [ ] Clarifications session has one bullet per accepted answer (no duplicates).
- [ ] Total asked (accepted) questions ≤ 5 (pre-plan mode).
- [ ] No contradictory FR/edge-case prose remains after updates.
- [ ] Feature-dir sanity documented in completion report.
- [ ] No clarification contradicts Decision Ledger without superseding row.

## Hand off

**Pre-plan:** report spec path, questions answered, sections touched → recommend `devarm-plan`.
By default STOP and ask unless end-to-end was explicitly requested.

**Code-grounded:** report evidence cited, spec deltas (if any) → return to review/fix loop.

## Red flags

- Never run pre-plan clarify *after* plan/tasks without re-running `devarm-analyze` on affected
  artifacts.
- Never treat `/findgap` as a substitute for clarify — findgap reviews diffs; clarify resolves
  spec ambiguity.
- Skipping clarify when `[NEEDS CLARIFICATION]` markers remain → warn downstream rework risk.
