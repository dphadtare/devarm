# devarm

**Your own, portable development method** — brainstorm → ground → spec → plan → tasks →
implement → review — expressed as [Agent Skills](https://agents.md) that run unchanged in
**Cursor, OpenAI Codex, GitHub Copilot, and Claude Code**.

devarm exists to close one gap: specs and plans stay high-level, so real decisions leak into
implementation time. devarm forces those decisions — *what does what, when, and how* — into a
**code-grounded design** with a **Decision Ledger**, before any code is written. You own it; you
improve it by editing markdown and committing.

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
| 4 | Plan | `devarm-plan` | `plan.md` + file map | every requirement → a task, no placeholders |
| 5 | Tasks | `devarm-tasks` | `tasks.md` | failing-test task before each impl |
| 6 | **Analyze** | `devarm-analyze` | findings report | artifacts consistent AND re-verified vs current code; flagship traced |
| 7 | Implement | `devarm-implement` | code + green tests | verified before "done" |
| 8 | Review | `devarm-review` | review notes + findings ledger | architecture + QA lens |
| 9 | Retro | `devarm-retro` | proposed commits to this kit (+ `CHANGELOG.md`) | method improved from the session |

Two phases make devarm more than a spec/plan flow:

- **Ground** (step 2) runs *inside* brainstorming, before approval, and blocks it until no
  "reuse/wrap/extend existing X" claim survives unverified. See `skills/devarm-ground/SKILL.md`.
- **Retro** (step 8) turns each session's lessons into commits to devarm itself — the engine that
  makes the method compound your judgment over time. See `skills/devarm-retro/SKILL.md`.

## Owning decisions

devarm treats every load-bearing choice as a **Decision Ledger** row with an owner and a tier:

- **design** (changes intent) → the agent STOPS and asks you.
- **impl** (trade-off, no intent change) → the agent proceeds with a recommendation but logs it
  and flags it so you can veto.
- **mechanical** → just done.
- An unanswered question is never a silent yes — it becomes `assumed — awaiting confirmation`.

This is enforced procedurally in `devarm-implement` and `AGENTS.md`, not left as advice.

## How to use it

In any tool, once installed, just start creative work — the agent will pick up `devarm-brainstorm`
from the skill `description`, or you can invoke a phase explicitly (e.g. `/devarm-brainstorm`).
The skills chain to the next phase automatically.

## Relationship to spec-kit / other frameworks

devarm is **additive** — it doesn't replace your other tools. If a target repo has a `.specify/`
(spec-kit) directory, `devarm-spec/plan/tasks` reuse its templates and `constitution.md`.
Otherwise they fall back to `templates/`. devarm supplies the *method*; the project supplies the
*rules* — a project's own constitution / `.cursor/rules` / `AGENTS.md` always wins.

## Layout

```
devarm/
├── AGENTS.md              # the portable brain: pipeline, when to invoke each skill, principles
├── install.sh            # symlink skills into .agents/.claude/.codex skill dirs (idempotent)
├── skills/               # the source of truth — one folder per phase
│   ├── devarm-brainstorm/SKILL.md
│   ├── devarm-ground/SKILL.md
│   ├── devarm-spec/SKILL.md
│   ├── devarm-plan/SKILL.md
│   ├── devarm-tasks/SKILL.md
│   ├── devarm-analyze/SKILL.md
│   ├── devarm-implement/SKILL.md
│   ├── devarm-review/SKILL.md
│   └── devarm-retro/SKILL.md
├── templates/            # design-doc, decision-ledger, config-decision, findings-ledger, constitution
└── CHANGELOG.md          # every method change + the failure that motivated it (kept by devarm-retro)
```

## Improving it

Edit a `SKILL.md`, commit. Because installs are symlinks, the change is live everywhere. Treat
recurring review feedback and mistakes as prompts to tighten a skill — that's how the method
compounds over time.
