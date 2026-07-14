# devarm — an owned, portable development method

`devarm` is a single, tool-agnostic methodology for taking an idea from brainstorm to
shipped code with **no rethinking left for implementation time**. It is expressed entirely as
[Agent Skills](https://agents.md) (`SKILL.md`) plus this `AGENTS.md`, so the same source of
truth runs in **Cursor, OpenAI Codex, GitHub Copilot, and Claude Code** without duplication.

You own it. You improve it by editing markdown and committing — no code, no vendor lock-in.

## The pipeline

Each phase is a skill. Each skill produces one artifact and ends at a gate before the next
phase. **The order is load-bearing** — in particular, grounding happens *before* the design is
approved, which is what keeps decisions out of implementation.

| # | Phase | Skill | Produces | Gate before advancing |
|---|-------|-------|----------|-----------------------|
| 1 | Brainstorm | `devarm-brainstorm` | `design.md` (draft) | Design presented, sections approved section-by-section |
| 2 | **Ground** | `devarm-ground` | `Detailed Design` + `Decision Ledger` appended to `design.md` | Every reuse claim verified with `file:line`; no ungrounded assumption |
| 3 | Specify | `devarm-spec` | `spec.md` (WHAT/WHY, testable) | Spec quality checklist passes |
| 4 | Plan | `devarm-plan` | `plan.md` + file-structure map | Every requirement maps to a task; no placeholders |
| 5 | Tasks | `devarm-tasks` | `tasks.md` (tests-first, ordered) | Each behavior has a failing test task before impl |
| 6 | **Analyze** | `devarm-analyze` | severity-ranked findings report | Artifacts consistent AND re-verified vs current code; flagship story traced end-to-end |
| 7 | Implement | `devarm-implement` | code + green tests | Verification run and confirmed before "done" |
| 8 | Review | `devarm-review` | review notes + findings ledger | Architecture + QA lens against principles + ledger |
| 9 | Finish | `devarm-finish` | merged branch / PR / kept / discarded | Fresh full-suite green; four structured options; typed confirm to discard |
| 10 | Retro | `devarm-retro` | proposed edits (commits) to this kit | Session analyzed; method improved |
| — | Debug (on-demand) | `devarm-debug` | root cause + failing test + one verified fix | No fix without root cause; 3 failed fixes → question the architecture |

## When to invoke each skill

- Any creative work (new feature, component, behavior change) **starts** with
  `devarm-brainstorm`. Do not write code before a design exists and is approved.
- `devarm-ground` runs **inside** brainstorming, after the design is presented and **before**
  the user approves it. It is the difference between this method and a plain spec/plan flow.
- `devarm-analyze` is the **mandatory gate between tasks and implement** — artifact
  self-consistency is not the same as artifact-vs-code truth; both passes must be clean, and the
  flagship user story must trace end-to-end without a gate rejecting it.
- `devarm-spec` → `devarm-plan` → `devarm-tasks` turn the grounded design into executable work.
  If a `.specify/` (spec-kit) directory exists in the target repo, these skills reuse its
  templates and `constitution.md`; otherwise they fall back to `devarm/templates/`.
- `devarm-implement` executes tasks one at a time (red → green → refactor → verify → commit).
- `devarm-review` runs before merge, or whenever a major step completes.
- `devarm-debug` is invoked **on demand from any phase** the moment a bug, test failure, or
  unexpected behavior appears — before proposing any fix. Root cause first, always.
- `devarm-finish` closes the branch once review findings are resolved: fresh full-suite
  verification, then merge / PR / keep / discard (discard needs typed confirmation).
- `devarm-retro` runs after a feature ships (or after a painful session) to feed lessons back
  into this kit — it is how devarm improves over time.

## Decision ownership (applies in every phase, especially implementation)

The user owns consequential decisions. When a decision point arises at any time — including
ad-hoc fix loops outside the pipeline — classify and act:

- **Design-level** (drop/replace a designed component, change semantics or user-visible
  behavior) → **STOP and ask the user**; record in the Decision Ledger.
- **Implementation trade-off** (module placement, error strategy, back-compat shim) → **proceed
  with the recommended option, but log it in the ledger and flag it in the turn summary** so it
  can be vetoed.
- **Mechanical** (naming, test layout) → just do it.
- **Unanswered ≠ approval.** Silence on a question becomes a ledger row `assumed — awaiting
  confirmation`, surfaced — never a silent yes.

## Principles (apply to every phase)

- **Evidence before assertion.** A claim about existing code is a hypothesis until the file is
  open with the line cited. Never write a requirement on an unread file. **Dead scaffolding is
  not reuse — "exists" ≠ "wired".**
- **A number is not a decision.** Every config/limit value needs: what it bounds, where enforced,
  configurability granularity, and at-limit behavior.
- **Follow the data.** A changed persistence shape is not done until every existing consumer
  (sync jobs, APIs, dashboards, resume paths, notifications) is audited in/out of scope.
- **Prompts and SKILL files are runtime contracts.** A contract change without its paired
  prompt/skill update ships conflicting guidance to the model.
- **Decisions become tests.** A behavioral decision without an enforcing test will be silently
  violated; wire the test before the code that could break it.
- **Boundary-first, and prose gets rationalized away.** Check import direction and
  file-size/god-file budgets before anything else — the most expensive surprises — and turn every
  guardrail into a gate with a hard number, not advisory prose.
- **Own the decisions.** Every load-bearing choice goes in the Decision Ledger with an owner
  (`user` for real trade-offs, `agent` for choices the code/rules force). Pull them out of
  prose and decide them consciously, up front.
- **YAGNI / DRY / TDD.** Only build what the design touches. One home per concept. Tests first.
- **Respect the target repo.** If the project has its own `constitution.md`, `.cursor/rules/`,
  or `AGENTS.md`, those win. `devarm` supplies the *method*; the project supplies the *rules*.
- **Procedural over advisory.** Gates that *run* (skill steps) beat rules that merely *advise* —
  advisory rules get rationalized away in long sessions (a real god-file rule was violated by
  500+ lines despite being always-on). Every devarm guardrail is a checklist step in a skill,
  with a hard number wherever possible, not soft prose.

## Session hygiene

- **One feature per thread.** Long threads that carry multiple features compound context loss
  and re-derivation. Start each feature fresh, linking the prior design doc if related.
- **One canonical planning system per feature.** If both a devarm plan and a spec-kit plan
  exist, declare which is the source of truth and generate the other from it — never maintain
  two hand-edited plans (they drift, as MR-### vs FR-### drift did in a past session).

## Portability notes

- Skills live in `devarm/skills/` and install to `.agents/skills/` (the cross-client
  convention read by Cursor, Codex, and Claude Code). Run `./install.sh` — see `README.md`.
- Claude Code reads `AGENTS.md` via import: add `@AGENTS.md` to a `CLAUDE.md`, or symlink
  `CLAUDE.md -> AGENTS.md`. `install.sh` sets this up.
- Codex has deprecated custom slash commands in favor of skills, so `devarm` is built on
  skills only — future-proof across tools.
