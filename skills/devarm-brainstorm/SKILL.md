---
name: "devarm-brainstorm"
description: "Use when the user explicitly asks for devarm/brainstorm, or before consequential code/product changes: new feature, component, behavior change, persistence/contract change, or non-trivial refactor. Do not use for ordinary Q&A, repo exploration, explanations, summaries, simple docs, diagrams, or visualization artifacts unless the user asks for devarm or the work changes runtime behavior, architecture, or the devarm method itself. Turns an idea into an approved, code-grounded design through collaborative dialogue, then runs devarm-ground BEFORE approval. By default, halt after approval and ask whether to run devarm-spec; continue automatically only when the user explicitly requested end-to-end execution."
metadata:
  phase: 1
  produces: "docs/design/YYYY-MM-DD-<topic>-design.md (draft)"
  next: "devarm-ground (before approval), then halt and ask about devarm-spec unless end-to-end was explicitly requested"
---

## Announce

"I'm using devarm-brainstorm to turn this idea into a grounded, approved design."

## Hard gate

Do NOT write code, scaffold, or invoke any implementation skill for consequential code/product
changes until a design has been presented, **grounded** (devarm-ground), and approved by the
user. This applies regardless of perceived simplicity — "too simple to design" is where
unexamined assumptions cause the most wasted work.

This skill is intentionally not the default for every helpful task. Do not invoke it for ordinary
Q&A, repo exploration, summaries, explanations, simple README/docs edits, diagrams, or
visualization artifacts unless the user explicitly asks for devarm or the work changes runtime
behavior, architecture, or the devarm method itself. If applicability is ambiguous, ask whether
to use devarm instead of invoking it by default.

## Checklist (create a task per item, complete in order)

1. **Explore project context.** Read the relevant files, docs, and recent commits. In an
   existing codebase, learn the current patterns before proposing changes. Where existing code
   has problems that directly affect this work (an overgrown file you must touch, tangled
   boundaries), include targeted improvements in the design — but never propose unrelated
   refactoring; stay on what serves the goal.
2. **Scope check.** If the idea spans multiple independent subsystems, stop and help decompose
   it into sub-projects first — each gets its own design → spec → plan → implement cycle. Don't
   refine details of something that should be split.
2b. **Scale gate.** Classify the work and recommend a track (user confirms):
   - **Quick track** — bug fix or single-story change with a small blast radius (roughly ≤3
     files, no new persistence, no contract changes). The GATES stay, the ARTIFACTS collapse:
     one short doc holds a few-sentence design, a scoped grounding pass (the touched seams +
     whichever of the 10 categories apply), and a mini task list; skip separate spec/plan/
     analyze docs. Before implement, run the scoped analyze equivalent in that same doc:
     re-verify the touched seams against current code, then a mini Pass 3 — play back the
     control flow and batch the open decisions with recommendations (see `devarm-analyze`
     Pass 3). Then go to implement (TDD + verification unchanged). If quick-track work
     reveals new persistence, a contract change, or a widening blast radius — STOP and
     upgrade to the standard track; that discovery is the signal, not an obstacle.
   - **Standard track** — everything else: the full pipeline below.
   Never skip grounding, user approval, the pre-implementation decision batch, TDD, or
   verification on any track — scale trims paperwork, not gates.
3. **Ask clarifying questions — one at a time.** Prefer multiple-choice with a recommended
   option first. One question per message; break big topics into several. Work through the
   Question Coverage Map below — every area answered or explicitly marked N/A/deferred before
   the design is presented.
4. **Propose 2-3 approaches** with trade-offs. Lead with your recommendation and why.
5. **Present the design in sections** scaled to complexity (a few sentences for simple parts,
   up to ~250 words for nuanced ones). Cover: architecture, components, data flow, error
   handling, testing. Ask after each section whether it looks right. Revise as needed.
6. **Write the draft design doc** to `docs/design/YYYY-MM-DD-<topic>-design.md` (or the target
   repo's configured design location, e.g. `docs/superpowers/specs/`). Use
   `devarm/templates/design-doc.md` as the structure.
7. **Spec self-review** (inline): scan for placeholders/TBDs, internal contradictions, scope
   creep, and requirements that could be read two ways. Fix inline.
8. **Run devarm-ground** on the draft — BEFORE asking for approval. Grounding may send you back
   to revise sections 4-6; that is expected and is the point.
9. **User approval gate.** Only after grounding passes, ask the user to approve the written,
   grounded design. If they request changes, revise and re-ground.
10. **Phase gate / handoff.** Report the design path, grounding result, approval state, and
    recommended next phase (`devarm-spec`). By default, STOP and ask the user whether to run
    `devarm-spec`. Invoke `devarm-spec` only if the user explicitly requested end-to-end
    execution for this work or has just told you to continue. Do not treat silence as approval
    to continue.

## Question Coverage Map

The goal of questioning is that the user fills in every detail the design depends on — not
just the ones the first question happened to touch. Cover each area (or mark it N/A aloud);
each answer becomes a candidate Decision Ledger row so it can't be re-litigated later.

| Area | What to elicit from the user |
|------|------------------------------|
| Purpose | Who is this for, what problem, why now? What triggers it? |
| Scope boundary | What's explicitly IN and OUT? What's the **flagship scenario** the design must nail? |
| Behavior semantics | The happy path, then: what happens on failure? Partial success? Pause/resume? What does the user/system see in each case? |
| Limits & config | Every number or knob, with its four sub-answers up front: bounds what / enforced where / configurable at what granularity / behavior at the limit. Don't accept a bare number. |
| Compatibility | What existing behavior must remain byte-identical? Who else consumes what this touches? |
| Communication/UX surface | What messages/notifications/UI does this emit — how many, when, consolidated or per-item? |
| Non-functional qualities | Only the ones that matter here: performance/scale targets, reliability/recovery expectations, observability (what must be visible in logs/metrics), security/privacy posture, compliance. Skip aloud what doesn't apply. |
| Integration & external dependencies | Which external services/APIs are touched, their failure modes, data formats, versioning assumptions. |
| Success criteria | How will we KNOW it works — measurable, checkable after implementation. |
| Trade-off preferences | Where the user stands on speed vs safety, cost vs completeness, simple-now vs flexible-later. |

**Questioning rules:**

- **Lead with a recommendation the user can accept cheaply.** For multiple-choice, put
  `**Recommended:** <option> — <1-2 line reason>` above the options and tell the user a plain
  "yes" accepts it. Prioritize remaining questions by impact × uncertainty — never spend two
  low-impact questions while a high-impact area is unresolved.
- **Follow the fork.** If an answer opens a new decision (an answer like "sequential is fine,
  but the fallback needs expansion" contains 2-3 embedded decisions), play back your
  restatement of what they decided and ask the next question the answer created — don't move
  on with your own interpretation.
- **Unanswered ≠ answered.** If the user skips a question, it does NOT default — carry it
  forward as `assumed — awaiting confirmation` and re-surface it at the approval gate.
- **Stop condition:** questioning is done when every map area is answered/N/A **and** the last
  answer opened no new fork — not when a fixed question count is reached.

## Back-and-forth protocol (iteration is normal — churn must land somewhere)

Revision during brainstorming is expected and cheap **before approval**; the job is to make
sure every loop ends in an updated artifact, not a drifting conversation.

- **Open question revisited** → just answer it again; nothing special.
- **Settled decision reopened** (user changes an earlier answer, or new information invalidates
  it): do NOT edit the conversation's memory only. (1) Mark the old ledger row `superseded`,
  add the new row with the new evidence; (2) **ripple-check**: scan the other ledger rows and
  design sections that depended on the old answer and re-confirm or revise each one aloud;
  (3) if the change touches any reuse claim or grounded category, re-run the affected part of
  `devarm-ground`. A reopened decision that skips the ripple check is how designs go
  internally inconsistent.
- **New consideration arrives mid-design** ("let's also account for X"): first classify — is
  it a new fork in THIS design (fold it into the coverage map and continue) or a scope change
  (back to the scope/scale check; possibly a separate feature)?
- **Resuming after a gap** (hours, days, or a new session): before continuing the dialogue,
  (1) read the design doc's Pipeline line + last-session note; (2) `git log`/diff the repo
  since the design was last touched and check whether landed changes invalidate any grounded
  evidence or ledger row — re-ground what moved; (3) play back the current decision state in
  3-5 bullets and confirm before asking the next question. Never resume by re-asking what the
  ledger already answers.
- **After approval**, the bar changes: design changes go through a superseding ledger row
  (design-level → the user decides), and if implementation has started, through
  `devarm-implement`'s course-correction protocol instead of quiet design edits.

## Design for isolation and clarity

Break the system into small units that each have one clear purpose, communicate through
well-defined interfaces, and can be tested independently. For each unit you must be able to
answer: what does it do, how do you use it, what does it depend on? If you can't change a unit's
internals without breaking consumers, the boundaries need work. When a file grows large, that's
a signal it's doing too much.

## Key principles

- One question at a time; multiple choice preferred.
- YAGNI ruthlessly — remove unnecessary features from every design.
- Always explore alternatives before settling.
- Incremental validation — approval per section, not all-at-once.
- Be flexible — go back and clarify when something doesn't fit.
