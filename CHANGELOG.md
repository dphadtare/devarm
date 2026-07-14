# devarm changelog

Every entry records a method change and the session/failure that motivated it. Maintained by
`devarm-retro` — a lesson is only "done" when it's a gate in the method, not just a note.

## 2026-07-14 — adopt from BMad Method (v6)

Reviewed BMad v6 (no local install — reviewed via its docs: 4-phase model, scale-adaptive
tracks, 12 agent personas, story-by-story implementation loop, party mode, web bundles).
BMad's persona layer duplicates what devarm's review lenses already do, but three ideas were
genuinely missing:

| Change | Source / rationale |
|--------|--------------------|
| Scale gate in brainstorm (quick vs standard track): bug-fix/single-story work collapses spec/plan/analyze into one short doc; gates (grounding, approval, TDD, verification) never collapse; auto-upgrade to standard when quick work reveals persistence/contract/blast-radius growth | BMad's scale-adaptive levels 0-4 / quick-spec track — devarm previously ran full ceremony on everything, which invites skipping the method for small work |
| Course-correction protocol in implement: mid-stream scope change → list affected requirements/ledger rows/tasks, update artifacts, scoped re-analyze, explicit rework tasks | BMad's `correct-course` workflow — devarm's drift rule covered code-vs-plan conflicts but not requirements changing underneath the work |
| Pipeline status line + last-session note in the design-doc header, updated at every gate | BMad's `workflow-status` / sprint-status tracking — devarm had no durable "where are we" marker, so a fresh session (or tool switch) had to reconstruct state from artifacts |

Not adopted: agent personas incl. party mode (devarm's review already applies the useful
lenses — architecture + QA — without persona ceremony; personas add role-play overhead, not
gates); PRD/product-brief artifact layer (devarm's design doc + spec cover it for solo work);
JIT per-epic tech-specs (devarm-analyze re-verifies against current code, which addresses the
same staleness problem); web bundles (tool-specific packaging).

## 2026-07-14 — adopt from spec-kit (speckit)

Reviewed all 14 speckit skills, its templates, scripts, and extension machinery. devarm's
pipeline was already modeled on speckit's (specify→plan→tasks→analyze→implement) and reuses
`.specify/` templates when present; adopted the concepts that survive outside that machinery:

| Change | Source / rationale |
|--------|--------------------|
| Spec: prioritized, independently-testable user stories (P1/P2/…, named Independent Test, Given/When/Then scenarios, P1 = viable MVP) | speckit spec-template — this structure is what made spec-016's tasks organizable story-by-story with a stoppable MVP slice |
| Spec: explicit scenario-class sweep (primary / alternate / exception / recovery / non-functional), absent classes marked excluded rather than silent | speckit-clarify taxonomy + checklist scenario classification |
| Spec quality gate reframed as "unit tests for English" — checks test the WRITTEN requirements (completeness/clarity/consistency/measurability/coverage), with optional domain checklist for risky areas | speckit-checklist's core concept, condensed from 367 lines to a paragraph |
| Brainstorm: recommendation-first question format ("Recommended: X — reason; reply 'yes' to accept") + impact×uncertainty prioritization of remaining questions | speckit-clarify's questioning loop — cheap accepts and never spending low-impact questions while high-impact areas are open |
| Brainstorm coverage map: non-functional qualities + integration/external-dependency areas | speckit-clarify's taxonomy had these two categories the map lacked |

Not adopted: hooks/extensions.yml machinery and check-prerequisites scripts (speckit plumbing —
devarm skills chain directly); `## Clarifications` session log in the spec (the Decision
Ledger is devarm's single home for decisions; a second Q→A log would split the record);
speckit-taskstoissues (YAGNI for a solo workflow — revisit if working with a team);
feature-numbering git scripts (reused via `.specify/` when present).

## 2026-07-14 — Question Coverage Map in brainstorm

"Ask clarifying questions" said HOW to ask (one at a time, multiple choice) but not WHAT must
be covered — so question coverage depended on where the dialogue happened to wander. In the
spec-016 session the brainstorm asked 6 good questions yet never elicited cap semantics or the
communication surface; both surfaced post-design.

| Change | Rationale |
|--------|-----------|
| 8-area Question Coverage Map (purpose, scope+flagship, behavior semantics incl. failure/partial/pause, limits & config with the four sub-answers, compatibility, communication surface, success criteria, trade-off preferences) | Questions are complete when the map is covered, not when the conversation feels done |
| Follow-the-fork rule: restate what an answer decided, ask the question it opened | User answers often contain 2-3 embedded decisions; interpreting them silently is how decisions get made without the user |
| Stop condition: all areas answered/N/A AND last answer opened no new fork; skipped questions carried as `assumed — awaiting confirmation` | Aligns brainstorm questioning with the ledger's no-silent-approval rule |

## 2026-07-14 — deep-dive on superpowers brainstorming + TDD

Line-by-line comparison of the two most important superpowers skills against devarm:

| Change | Rationale |
|--------|-----------|
| New `devarm-tdd` (core discipline, consumed by implement + debug) | devarm-implement's 3-line red/green/refactor lost the parts that make TDD hold under pressure: the **delete rule** (code before test is deleted, not "kept as reference"), **RED must FAIL not error** / test-passes-immediately means it tests nothing, test-quality rules (one behavior, spec-like names, real code over mocks), the when-stuck table (hard to test = design problem), mock/test-only-method anti-patterns, and the rationalization red-flags |
| `devarm-implement` execution loop delegates to `devarm-tdd`; `devarm-debug` Phase-4 repro test cites it | One home for the discipline instead of two paraphrases |
| `devarm-brainstorm`: targeted-improvement rule for existing codebases | From superpowers brainstorming — fix existing problems that directly affect the work as part of the design; never bundle unrelated refactoring |

Checked and already covered by devarm-brainstorm (no change): hard gate, "too simple to need
a design" anti-pattern, scope-check/decomposition, one-question-at-a-time, 2-3 approaches,
sectioned presentation, spec self-review checklist, written-spec user gate, single terminal
hand-off. Not adopted: the browser "visual companion" (tool-specific, token-heavy).

## 2026-07-14 — adopt from the superpowers plugin

Reviewed all 14 superpowers skills. Brainstorming/TDD/plan-writing/verification were already
absorbed into devarm's phases; adopted the pieces devarm lacked, condensed:

| Change | Source / rationale |
|--------|--------------------|
| New `devarm-debug` (on-demand, any phase): 4-phase root-cause-first debugging, no fix-stacking, 3-failed-fixes → question the architecture, parallel subagents for independent failures | `systematic-debugging` + `dispatching-parallel-agents`. devarm had NO debugging discipline — fix loops were its weakest phase |
| New `devarm-finish` (phase 9): fresh full-suite verification, then exactly four options (merge / PR / keep / discard), typed confirm to discard, worktree cleanup | `finishing-a-development-branch`. devarm previously ended at review with no integration protocol |
| Implement: verification claim→evidence table ("fresh run in THIS turn"; subagent report ≠ evidence; red-green for regression tests) | `verification-before-completion` — the table format makes "what proves this claim" explicit |
| Implement: subagent protocol — full task text in prompt (never "read the plan"), two-stage review (spec compliance THEN quality), model sized to task, BLOCKED/NEEDS_CONTEXT handling, never retry unchanged | `subagent-driven-development` — devarm's subagent mode was one sentence |
| Implement: optional worktree isolation (ignored dir + green baseline before task 1) | `using-git-worktrees`, trimmed to the two safety rules that matter |
| Review: receiving-feedback discipline — no performative agreement, clarify ALL items before implementing ANY, YAGNI-check reviewer suggestions, push back technically, correct pushback factually | `receiving-code-review` — complements the findings ledger with response behavior |

Not adopted: `using-superpowers` (meta-dispatch — the skills' own descriptions handle
discovery), `writing-skills` TDD-for-docs (interesting; revisit if retro edits start missing),
`executing-plans` (parallel-session variant of implement — YAGNI for a solo workflow).

## 2026-07-14 — adopt code-quality standards from tech-catalyst-v2 rules

Ported the transferable core of the project's `.cursor/rules/` code-quality set
(`design-patterns`, `architecture-boundaries`, `backend-conventions`, `frontend-conventions`)
into the kit as `templates/code-standards.md`, stripped of repo-specific paths so it works in
any stack:

| Change | Rationale |
|--------|-----------|
| New `templates/code-standards.md` — prefer/avoid pattern catalog with mandatory BAD/GOOD pairs | The tech-catalyst rules proved that pattern rules only bite when each carries a concrete counter-example |
| Constitution VIII: design patterns & anti-patterns | Makes the catalog a checked principle, not an optional doc |
| `devarm-ground` inputs now include the project's pattern catalog (fallback: code-standards) | Reuse legality and pattern conformance are checked at the same grounding read |
| `devarm-review` architecture lens gains a patterns/anti-patterns check (fat controller, inline queries, leaky ORM, buried commits, view-local fetching, suppression creep) | The review lens previously checked boundaries/duplication but not pattern conformance |

Not ported (stays project-side): repo-specific layering paths, named god-files, stack-specific
rules (React Query, pydantic-settings) — devarm supplies the method, the project supplies those.

## 2026-07-14 — final devarm2 delta port (devarm becomes the single active kit)

Side-by-side review confirmed devarm ⊇ devarm2 except two findings-ledger details, now ported:

| Change | Rationale |
|--------|-----------|
| Findings ledger gains a **Source** column | Multiple review passes/sessions append to one file; rows must say where a claim came from without re-feeding transcripts. |
| Strict status semantics: `fixed` requires verification output + commit; `deferred` requires a tracked task id | "Fixed" without seen verification and "deferred" without a task are how findings silently rot. |

devarm2 is superseded and can be discarded.

## 2026-07-14 — merge best-of from devarm2

Reviewed the parallel `devarm2` build (same source retro) and adopted what it did better:

| Change | Rationale |
|--------|-----------|
| New `devarm-analyze` gate (phase 6, between tasks and implement) | Artifact self-consistency ≠ artifact-vs-code truth; the repo can move after grounding. Adds a flagship end-to-end paper-trace — the check that catches "a gate on the path rejects the headline use case" (the US1 near-miss). |
| `devarm-ground` consolidated to **ten** numbered decision categories | Config semantics (#9) and runtime-contract surfaces (#10) were scattered notes; folding them into the numbered list makes them un-skippable. |
| Decision Ledger gains an **Enforcing test** column + "re-surface assumed rows at every gate" | Tightens decision→test traceability and the no-silent-approval rule. |
| Added this `CHANGELOG.md` | The audit trail of why the method is shaped the way it is. |
| Crisper principle one-liners in `AGENTS.md`; anti-patterns in `devarm-retro` | "A number is not a decision", "exists ≠ wired", "prose rules get rationalized away → gates with numbers"; retro must end as a diff, not a doc. |

## 2026-07-14 — founding (retro of the multi-repo fix generation session)

Source: retrospective of the spec-016 multi-repo session (Jul 10–14, tech-catalyst-v2; brainstorm
→ design → speckit → implement → 6+ review/fix loops; ~60% of wall-clock in the post-implementation
fix tail). Each gate below exists because of a specific failure in that session.

| Gate added | Motivating failure |
|------------|--------------------|
| Ground: reuse requires shape check (sync/async, statefulness, wired-vs-dead) | Design claimed "reuse MultiRepoDecisionService"; it was async, per-request, in-memory, unwired; flip-flopped 3× and was finally deleted (~760 lines) |
| Ground category 9: config/limit semantics | "Cap = 2" locked as a number; semantics (PR-only vs diagnosis, configurability, overflow) resolved in 4 post-design exchanges; design rewritten twice |
| Ground category 3: consumer audit for changed data shapes | New `ticket_pull_requests` table shipped while PR-sync loop, list API, and dashboard still read the old scalar → P0 sync gap found only in external review |
| Ground category 10: runtime contract surfaces | Synthesis SKILL.md taught `next_repo` while the injected contract demanded `cross_repo_targets[]` — conflicting model guidance; initially misclassified as "docs only" |
| Tasks: decision → enforcing-test traceability | "Intake-once" and "single consolidated comment" were explicit decisions, violated by the first implementation, caught only by findgap |
| Plan: integration seams get contracts / spike tasks | Nearly every post-implementation bug lived in seams left as "confirm during coding" |
| Implement: mid-implementation decision taxonomy + no-silent-approval | Per-app cap-override question went unanswered and was silently resolved as YAGNI; the gate dropped a designed component without asking |
| Implement: phase-boundary commits + high-coupling checkpoints | ~6h uncommitted → duplicate "fix the issues found" loops, no bisectable history; god-file grew +563 lines despite a known rule |
| Review: single findings ledger, evidence-based verdicts both ways, fixed/awaiting split | Three external review transcripts re-fed and re-litigated; two duplicate fix requests for already-applied fixes |
| AGENTS.md: one planning system per feature; one feature per thread | Superpowers plan + speckit artifacts drifted (MR-### vs FR-###); 009 brainstorm started at the tail of a 1,000-message thread |
