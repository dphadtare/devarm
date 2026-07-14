# devarm changelog

Every entry records a method change and the session/failure that motivated it. Maintained by
`devarm-retro` — a lesson is only "done" when it's a gate in the method, not just a note.

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
