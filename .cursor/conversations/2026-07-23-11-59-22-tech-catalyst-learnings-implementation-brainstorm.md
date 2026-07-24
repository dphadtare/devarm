# Tech Catalyst learnings → implementation-decision brainstorm + design anchoring

**Date:** 2026-07-23 11:59:22
**Topic:** Method improvements to devarm from Tech Catalyst project learnings

## User request (summary)

Four learnings from the Tech Catalyst project:

1. Every dev session should start with brainstorming and end with a reviewed design doc before
   specs/tickets.
2. Design brainstorming misses implementation details; decisions surface at implementation time.
   Wanted a dedicated "implementation brainstorming" session (functional/control flow + the
   decisions implementation will need) so they can be pulled earlier and decided up front.
3. Vibe-coding / long sessions anchor to current-session context and skip designs approved in
   earlier sessions — the agent should be forced to follow the previously decided design.
4. Decision triage: small choices can proceed on the recommendation; control-flow/design changes
   are too hard to decide mid-implementation and belong in the design/implementation brainstorm.

## Gap analysis

- Learning 1: already enforced (devarm-brainstorm hard gate + section-by-section approval).
- Learning 2: devarm-ground resolves the 10 decision categories and devarm-analyze traces the
  flagship story, but both are agent-driven verification — no interactive control-flow
  walkthrough or batched decision session with the user. Genuine gap.
- Learning 3: no rule forced a coding session to reload the governing design doc. Genuine gap.
- Learning 4: taxonomy existed (design-level / trade-off / mechanical) but no batching —
  questions still arrived one at a time mid-flow.

## User decisions

- Implementation brainstorming lives as the **closing pass (Pass 3) of devarm-analyze** (chose
  over a new dedicated skill or step 0 of devarm-implement).
- Design-anchor rule applies to **devarm pipeline sessions only** (devarm-implement), not all
  ad-hoc coding sessions.

## Changes made

- `skills/devarm-analyze/SKILL.md`: new Pass 3 — interactive implementation-decision brainstorm
  (control-flow walkthrough of flagship + failure paths, enumerate foreseeable decisions,
  batch-present with recommendations, exit criterion: implement asks near-zero questions).
  Gate extended to require Pass 3 completion; Pass 1 ledger check now defers resolution to
  Pass 3; description/metadata updated.
- `skills/devarm-implement/SKILL.md`: design-anchor precondition (reload governing design doc +
  ledger before task 1 and on session resume; written design governs over session memory);
  batching rule (mid-flow trade-offs proceed on recommendation, presented together at next
  checkpoint; foreseeable trade-off mid-task = Pass-3 miss logged for retro); checkpoint step
  now includes accumulated trade-off rows.
- `AGENTS.md`: pipeline table row 6 + devarm-analyze bullet updated.
- `README.md`: pipeline table row 6 + owning-decisions section updated.
- `CHANGELOG.md`: new 2026-07-23 entry recording the learnings and changes.

## Suggested commit message

Add implementation-decision brainstorm (analyze Pass 3) and design anchoring in implement, from
Tech Catalyst learnings: batch implementation decisions before coding; written design governs
over session memory.

---

## Follow-up (12:39): findgap review + fixes

A findgap review of the full uncommitted change set found and fixed:

1. Quick track vs implement precondition contradiction → quick track now includes a scoped
   analyze equivalent (touched seams + mini Pass 3 batch); implement precondition accepts it;
   never-skip list includes the pre-implementation decision batch. (USER_GUIDE aligned.)
2. Phase-number drift → retro frontmatter 9→10, finish 10→9, README "Retro (step 8)"→10.
3. Pass 3 re-run scope defined (only touched flows/decisions re-walked); "scoped re-gate"
   restored to the analyze description; design-level items listed first in the batch.
4. USER_GUIDE analyze/implement rows updated for Pass 3.
5. structurizr: analyze component no longer "read-only"; AnalyzeGateFlow gained Pass 3 steps.
6. AGENTS.md decision-ownership trade-off bullet aligned with the batching rule.
7. Cosmetic: implement long line rewrapped; README "Two phases"→"Three phases" incl. Analyze.

CHANGELOG 2026-07-23 entry extended with these rows. No commits made.
