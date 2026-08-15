---
name: "devarm-retro"
description: "Use after a feature ships, or after a painful/back-and-forth session, to turn the session into improvements to the devarm method itself. Analyzes a session transcript, compares what happened against the pipeline, identifies decisions made late / bugs that a gate should have caught / avoidable back-and-forth, and proposes concrete edits plus a suggested commit summary for the devarm repo. Never run git commit unless the developer explicitly asks for that commit. This is how devarm compounds your judgment over time."
metadata:
  phase: 11
  produces: "a retro report + proposed edits + suggested commit summary"
  next: "wait for developer confirmation before any git commit"
---

## Announce

"I'm using devarm-retro to turn this session into improvements to the method."

## Artifact and evidence handoff contract

Before acting or resuming, read the current repository rules, current artifacts, and the diff;
current evidence takes precedence over any stale summary. Revalidate artifacts and record the
validator output and verification evidence in the retro report. Every proposed method change must
name its motivating evidence, affected skill/template/validator surface, and its method inventory entry. Optional adapters may be recorded,
but adapter use cannot bypass native gates. If the validator is unavailable, record that limitation
and keep the human checklist authoritative.

## Generalize before promoting a method change

For every proposed method change, separate incident evidence from the portable rule before
editing the kit. Record:

1. **Failure category** — the reusable class of problem, not the product or ticket name.
2. **Domain-neutral invariant** — what must be true across implementations.
3. **Enforcement point** — the devarm skill, template, validator, or target-repository rule that
   will enforce it.
4. **Applicability boundary** — when the rule applies and when it remains target-only.
5. **Generalization check** — explain how the rule holds across at least two repository/domain
   shapes, or record why the evidence supports only a narrower category.

Choose one promotion outcome:

- **Portable core** — applies across repository and domain shapes; add it to native devarm.
- **Category-scoped** — reusable within a named class; add it to an existing gate with the
  boundary stated explicitly.
- **Target-only** — specific to a product, repository, framework, or workflow; keep it in the
  target repository or domain skill.

Incident identifiers, product names, and postmortem narratives are motivating evidence only. They
must not appear in normative `skills/devarm-*/SKILL.md` instructions. Preserve that provenance in
the changelog or retro report.

## Inputs

- A session transcript (e.g. a `.jsonl` under the agent-transcripts dir) OR the current session.
- The devarm kit (skills + templates + AGENTS.md) — this is what you propose changes to.
- If it exists, the feature's Decision Ledger and findings ledger.

## Process (create a task per step)

### Step 1 — Reconstruct the session arc

For a large transcript, condense first (extract user messages + tool-call summaries) rather than
reading raw. Map the phases: brainstorm → ground → spec → plan → tasks → implement → review, and
note where time actually went (usually a long review/fix tail).

### Step 2 — Classify what happened against the pipeline

- **What held** — decisions locked early that survived to the end (evidence the method worked;
  don't touch those parts).
- **Late decisions** — anything decided during implementation that could have been decided at
  design/plan time. For each, name the phase it *should* have been caught in.
- **Bugs by layer** — were bugs in pure modules or in binding/integration seams? (Seam bugs
  usually mean the plan under-specified the seam.)
- **Decisions violated** — any locked decision the implementation broke. If so, it lacked an
  acceptance test (decision→test traceability gap).
- **Back-and-forth drivers** — re-fed review transcripts, duplicate "fix it" turns, re-litigated
  settled decisions, two planning systems, uncommitted long runs.
- **Method adoption** — when the user says they will adopt an external pattern into devarm
  (Superpowers skill-check, Spec Kit clarify, findgap behavior), record it as a **native gate
  proposal** in Step 4 — absorb the behavior into `devarm-*` skills / `AGENTS.md`, do not leave
  the repo depending on the external tool. Domain skills (ticket postmortem, etc.) stay external
  but belong in the session method inventory.

### Step 3 — Map each finding to a devarm gate

For every finding, answer: **which existing gate should have caught this, or what new gate is
needed?** Examples of the mapping:

| Symptom | devarm response |
|---|---|
| Reuse of a component that didn't fit | strengthen `devarm-ground` Step 2 (code read) |
| Bug in an integration seam | `devarm-plan` seam-contract / spike requirement |
| Changed persistence broke a downstream reader | `devarm-ground` follow-the-data audit |
| A prompt/skill gave stale runtime guidance | `devarm-ground`/`plan` runtime-contract rule |
| A locked decision was silently broken | `devarm-tasks` decision→test traceability |
| A decision was made without asking | `devarm-implement` decision taxonomy |
| God-file grew despite the rule | hard-number budget + named module upfront |
| Review loops re-litigated fixed items | `devarm-review` findings ledger + turn state-split |

### Step 3.5 — Check the method held its own gates

Did each skill's gate actually run, or was one skipped/rationalized? A gate that can be skipped
silently is a gate that must become structural (a checklist item / template section with a hard
number) rather than advisory prose. Note any gate that existed but didn't fire.

### Step 4 — Propose concrete edits to the devarm kit

Do NOT just write advice. Produce actual diffs/edits to specific `SKILL.md` / template /
`AGENTS.md` files — a new checklist step, a template section, a taxonomy tweak — each with a
one-line rationale tied to the finding. Prefer procedural checklist steps with hard numbers over
soft prose. **Only recurring (≥2 occurrences) or one severe failure earns a method change** —
resist adding a rule for every one-off.

**Canonical home (`vhosts/devarm`):** apply all skill edits under `skills/devarm-*/SKILL.md` in the
devarm repo (`~/vhosts/devarm` or your clone). `install.sh` symlinks those dirs into
`~/.agents/skills`, `~/.claude/skills`, and `~/.codex/skills` — **do not copy skills into feature
repos** (e.g. `target-repo/.cursor/skills/devarm-*`); Spec Kit and project pulls will diverge
or overwrite. Editing the symlink target updates every tool instantly. See devarm `README.md`.

### Step 5 — Record and propose a commit

- Append a dated entry to `CHANGELOG.md` at the **devarm repo root** (what changed, which
  session/failure motivated it). Each retro should identify one logical commit boundary, but the
  skill must not create the commit by default.
- Changed files must live in the devarm repo (`skills/devarm-*`, `CHANGELOG.md`, templates,
  `AGENTS.md` as needed). Never treat symlink destinations (`~/.claude/skills/`, feature-repo
  `.cursor/skills/`) as the commit target — they are views of `vhosts/devarm`.
- Present the proposed edits, changed files, verification evidence, and a suggested commit
  message. Wait for explicit developer confirmation before running `git commit` in **vhosts/devarm**
  (editing the method is itself a design-level decision — the user owns it).

## Anti-patterns

- Retro notes that end as a document instead of a diff to this repo — the lesson isn't learned
  until it's a gate. The diff may remain uncommitted until the developer confirms.
- Copying devarm skills into a feature repo or editing only a symlink path without committing
  **vhosts/devarm** — changes won't reach teammates or survive reinstall; always diff `skills/` in
  the devarm repo.
- Adding a new rule for every one-off — only recurring or severe failures earn a method change.
- Growing skills past the point where they get read — prefer tightening an existing gate over
  adding a new one.

## Principle

The retro is the flywheel: bugs and back-and-forth are not just fixed in the feature, they are
converted into a gate so the *class* of problem cannot recur. Over time, devarm becomes the
accumulated record of your engineering judgment.
