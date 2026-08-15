# devarm

**Your own, portable development method** — brainstorm → ground → spec → clarify → plan → tasks →
implement → review — expressed as [Agent Skills](https://agents.md) that run unchanged in
**Cursor, OpenAI Codex, GitHub Copilot, and Claude Code**.

devarm exists to close one gap: specs and plans stay high-level, so real decisions leak into
implementation time. devarm forces those decisions — *what does what, when, and how* — into a
**code-grounded design** with a **Decision Ledger**, before any code is written. You own it; you
improve it by editing markdown. Agents never create git commits unless you explicitly ask.

## Why it's portable (no code, no lock-in)

- **Skills** (`SKILL.md`) are an open standard. Cursor auto-discovers skills from
  `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, and `.codex/skills/`; Codex and Claude
  Code read them too. `.agents/skills/` is the emerging cross-client convention.
- **`AGENTS.md`** is the cross-tool instruction standard (Linux Foundation AAIF), read natively
  by Codex, Cursor, Copilot, and more. Claude Code reads it via a `@AGENTS.md` import.
- Codex has deprecated custom slash commands in favor of skills — so devarm is skills-only and
  future-proof.

## Install

```bash
# Global — available in all your projects (recommended)
./install.sh

# Or per-project
./install.sh --project /path/to/your/repo

# Remove
./install.sh --uninstall
```

The installer **symlinks** the skills, so editing a skill in this repo updates it everywhere
instantly. It links into `.agents/skills`, `.claude/skills`, and `.codex/skills` so every tool
sees them. Restart / reopen your agent tool afterward so it re-scans skill directories.

## The pipeline

| # | Phase | Skill | Produces | Gate |
|---|-------|-------|----------|------|
| 1 | Brainstorm | `devarm-brainstorm` | draft `design.md` | sections approved |
| 2 | **Ground** | `devarm-ground` | Detailed Design + Decision Ledger | every reuse verified with `file:line` |
| 3 | Specify | `devarm-spec` | `spec.md` | quality checklist passes |
| 4 | Clarify | `devarm-clarify` | `spec.md` Clarifications | material ambiguities resolved or risk logged |
| 5 | Plan | `devarm-plan` | `plan.md` + file map | every requirement → a task, no placeholders |
| 6 | Tasks | `devarm-tasks` | `tasks.md` | failing-test task before each impl |
| 7 | **Analyze** | `devarm-analyze` | `analysis.md` + batch-decided implementation decisions | artifacts consistent AND re-verified vs current code; flagship traced; implementation decisions batch-decided |
| 8 | Implement | `devarm-implement` | code + green tests | verified before "done" |
| 9 | Review | `devarm-review` | review notes + findings ledger | architecture + QA lens |
| 10 | Finish | `devarm-finish` | merge / PR / keep / discard | fresh suite green; typed confirm to discard |
| 11 | Retro | `devarm-retro` | proposed edits + suggested commit summary (+ `CHANGELOG.md`) | method improved from the session |
| — | Debug | `devarm-debug` (on-demand, any phase) | root cause + failing test + one fix | no fix without root cause |
| — | TDD | `devarm-tdd` (core discipline) | test seen to fail first | code-before-test gets deleted |

Three phases make devarm more than a spec/plan flow:

- **Ground** (step 2) runs *inside* brainstorming, before approval, and blocks it until no
  "reuse/wrap/extend existing X" claim survives unverified. See `skills/devarm-ground/SKILL.md`.
- **Clarify** (step 4) resolves up to five material ambiguities in `spec.md` before planning. See
  `skills/devarm-clarify/SKILL.md`.
- **Analyze** (step 7) ends with an interactive implementation-decision brainstorm: the control
  flow is walked with you and every foreseeable implementation decision is batch-decided before
  any code. See `skills/devarm-analyze/SKILL.md`.
- **Retro** (step 10) turns each session's lessons into proposed edits to devarm itself — the
  engine that makes the method compound your judgment over time. It suggests a commit summary,
  but does not commit unless you explicitly ask. See `skills/devarm-retro/SKILL.md`.

## Owning decisions

devarm treats every load-bearing choice as a **Decision Ledger** row with an owner and a tier:

- **design** (changes intent) → the agent STOPS and asks you.
- **impl** (trade-off, no intent change) → the agent proceeds with a recommendation but logs it
  and flags it so you can veto. Foreseeable trade-offs are batch-decided with you in
  `devarm-analyze` before coding starts; leftovers are batched at checkpoints, not asked
  one-by-one mid-flow.
- **mechanical** → just done.
- An unanswered question is never a silent yes — it becomes `assumed — awaiting confirmation`.

This is enforced procedurally in `devarm-implement` and `AGENTS.md`, not left as advice.

## How to use it

For the full developer workflow, see [`USER_GUIDE.md`](USER_GUIDE.md).

The short version:

1. Install devarm with `./install.sh`, then restart / reopen your agent tool.
2. Open the project you want to change.
3. Ask explicitly: `Use devarm to add <feature>` or invoke a phase directly, such as
   `devarm-brainstorm`.
4. By default, the agent stops after each phase gate and asks what to run next.

devarm is for consequential code/product changes, not every chat. Agents should not invoke it for
ordinary Q&A, repo exploration, summaries, simple docs, diagrams, or visualization artifacts
unless you ask for devarm or the work changes runtime behavior, architecture, or the devarm
method itself. If it is unclear whether devarm applies, the agent should ask before invoking it.
For bugs or failing tests, invoke `devarm-debug`. For merge readiness, invoke `devarm-review`
and then `devarm-finish`.

To run the whole flow without stopping at every mechanical gate, ask explicitly for end-to-end
execution, for example: `Use devarm end-to-end for <feature>`. Even then, devarm still stops for
user approval, design-level decisions, unresolved ledger assumptions, and a failing
`devarm-analyze` gate.

## Relationship to spec-kit / other frameworks

devarm is **additive** — it doesn't replace your other tools. If a target repo has a `.specify/`
(spec-kit) directory, `devarm-spec/plan/tasks` reuse its templates and `constitution.md`.
Otherwise they use the fallback templates in `templates/`. devarm supplies the *method*; the project supplies the
*rules* — a project's own constitution / `.cursor/rules` / `AGENTS.md` always wins.

## Artifact, rule, and adapter contract

The native pipeline writes repository-local Markdown artifacts with common artifact metadata:
repository, branch, status, phase, pipeline, last verification, risks, next gate, and related
artifacts. The design owns one canonical rule inventory. The target-repository rule wins over a
devarm default; conflicts receive a visible disposition. An optional validator is a read-only
standard-library check: validator errors block a handoff, warnings remain visible, and human judgment plus
approval gates stay authoritative. The installer does not distribute or require a validator — the
validator is not installed as a skill, service, database, or required CLI. No required CLI, service, or database is needed for the native method.

Adapter-present work records the adapter, its output, and reuse value in the method inventory.
Adapter-absent work keeps the same native gates. Source rules are explicitly classified as Adopt,
Adapt, or Target-only; target-project-specific rules remain with the target repository. Partial,
failed, and blocked artifacts remain resumable only after current evidence and the diff are
revalidated. Retro proposals require motivating evidence and verification evidence.

## Layout

```
devarm/
├── AGENTS.md              # the portable brain: pipeline, when to invoke each skill, principles
├── USER_GUIDE.md          # practical developer workflow and prompts
├── install.sh            # symlink skills into .agents/.claude/.codex skill dirs (idempotent)
├── skills/               # the source of truth — one folder per phase
│   ├── devarm-brainstorm/SKILL.md
│   ├── devarm-ground/SKILL.md
│   ├── devarm-spec/SKILL.md
│   ├── devarm-clarify/SKILL.md
│   ├── devarm-plan/SKILL.md
│   ├── devarm-tasks/SKILL.md
│   ├── devarm-analyze/SKILL.md
│   ├── devarm-implement/SKILL.md
│   ├── devarm-review/SKILL.md
│   └── devarm-retro/SKILL.md
├── templates/            # artifact metadata, rule inventory, phase docs, and decision/findings templates
└── CHANGELOG.md          # every method change + the failure that motivated it (kept by devarm-retro)
```

## Improving it

Edit a `SKILL.md`; commit only when you choose to. Because installs are symlinks, the change is
live everywhere. Treat recurring review feedback and mistakes as prompts to tighten a skill —
that's how the method compounds over time.
