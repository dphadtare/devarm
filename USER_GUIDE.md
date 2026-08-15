# devarm user guide

This guide is for developers who want to use devarm in a real project, not just understand the
method. devarm is a set of agent skills: you install them once, then ask your coding agent to use
the method while it works in your repository.

## 1. Install devarm

From this repository:

```bash
./install.sh
```

That installs devarm globally by symlinking each skill into:

- `~/.agents/skills`
- `~/.claude/skills`
- `~/.codex/skills`

For one project only:

```bash
./install.sh --project /path/to/your/repo
```

Restart or reopen your agent tool after installing so it scans the skill directories.

## 2. Start from the target repo

Open the project you want to change in your agent tool. The working directory should be the
target repo, not this devarm repo.

Then describe the work normally:

```text
Use devarm to add bulk invoice export to this app.
```

or:

```text
I want to change how retry failures are reported. Use the devarm method.
```

You can also invoke a phase by name if your tool supports direct skill invocation:

```text
Run devarm-brainstorm for this feature.
```

When you request devarm for a new feature, behavior change, component, or non-trivial refactor,
the agent should begin with `devarm-brainstorm`. It should not jump straight to code.

devarm should not be invoked for every chat. For ordinary Q&A, repo exploration, summaries,
simple documentation edits, diagrams, or visualization artifacts, the agent should just help
directly unless you explicitly ask it to use devarm or the work changes runtime behavior,
architecture, or the devarm method itself. If it is unclear whether devarm applies, the agent
should ask before invoking it.

## 3. What the agent should do

For standard work, expect this flow. By default, the agent stops after each phase gate, reports
the artifact or result, and asks whether to continue.

| Step | What happens | Your role |
|------|--------------|-----------|
| Brainstorm | The agent asks focused questions and proposes approaches. | Answer trade-off and scope questions. |
| Ground | The agent verifies reuse claims against real files with `file:line` evidence. | Approve or reject the grounded design. |
| Spec | The agent writes testable WHAT/WHY requirements. | Check that the behavior is right. |
| Clarify | The agent asks up to five material ambiguity questions and records the answers in `spec.md`. | Resolve or explicitly defer remaining ambiguity. |
| Plan | The agent maps files, seams, and implementation steps. | Check for obvious wrong assumptions. |
| Tasks | The agent creates ordered, tests-first tasks. | Confirm scope still matches. |
| Analyze | The agent re-checks artifacts against current code, persists `analysis.md`, then walks the control flow with you and batch-presents every remaining implementation decision with recommendations. | Resolve blocking findings, confirm the flows, and answer the decision batch (a plain "yes" accepts the recommendations). |
| Implement | The agent works task by task with TDD and verification; trade-offs it logs are batched at checkpoints. | Answer design-level decisions only. |
| Review | The agent reviews against the design and repo principles. | Decide whether findings must be fixed. |
| Finish | The agent verifies fresh and offers merge, PR, keep branch, or discard. | Pick the finish action. |
| Retro | After shipping or pain, the agent proposes improvements to devarm. | Decide which method changes to keep. |

For small bug fixes or single-story changes, `devarm-brainstorm` may recommend the quick track.
Quick track collapses the paperwork into one short doc, but it does not skip grounding, approval,
the pre-implementation decision batch (a scoped mini version of analyze's walkthrough), TDD, or
verification.

## 4. Phase-by-phase by default

devarm is phase-by-phase by default: one phase runs, reaches its gate, then stops for your next
instruction.

Use prompts like:

```text
Run devarm-brainstorm only. Stop after the grounded design is ready for my approval.
```

```text
The design is approved. Run devarm-spec next.
```

```text
The spec is approved. Run devarm-plan next, but do not create tasks yet.
```

```text
The plan looks good. Run devarm-tasks and stop before implementation.
```

```text
Run devarm-analyze. If it is clean, stop and wait for me before implementation.
```

```text
Analyze is clean. Run devarm-implement for the first task only.
```

This works best when you name the artifact path as you resume:

```text
Resume with devarm-plan using docs/design/2026-07-14-bulk-export-design.md and
docs/specs/bulk-export/spec.md.
```

To opt into automatic phase transitions, say so explicitly:

```text
Use devarm end-to-end for this feature. Stop only for user approval gates, design-level
decisions, unresolved ledger assumptions, failed verification, or a failing analyze gate.
```

Later phases should not invent missing earlier work. If you invoke `devarm-implement` before
there is an approved design, spec, plan, tasks file, and clean analyze result, the agent should
stop and ask to run the missing gate first.

## 5. What files to expect

devarm creates planning artifacts in the target repo. Common paths are:

- `docs/design/YYYY-MM-DD-<topic>-design.md`
- `docs/specs/<topic>/spec.md`
- `docs/specs/<topic>/plan.md`
- `docs/specs/<topic>/tasks.md`
- `docs/specs/<topic>/analysis.md`
- a findings ledger or review notes during review

If the target repo has `.specify/`, devarm reuses that repo's spec-kit templates and layout
instead.

## Portable artifact and adapter rules

Each repository-local artifact records common metadata (repository, branch, status, phase, pipeline,
verification, risks, next gate, and related artifacts) and links the design's canonical rule
inventory. The target-repository rule wins over a devarm default. The optional validator is a
standard-library check that reports blocking errors or visible warnings; it does not replace human judgment or an
approval gate. Partial, failed, and blocked work is preserved and must be revalidated before resume.

For the adapter-present path, record the adapter in the method inventory with its output and reuse
value. For the adapter-absent path, the same native gates still run. Source rules use Adopt, Adapt, or Target-only
dispositions, so target-project-specific guidance does not leak into the portable core. Retro
proposals cite motivating evidence and verification evidence.

## 6. How to work with it

Use normal language. Good requests include the outcome and any important boundary:

```text
Use devarm to add CSV import for contacts. Keep the first version admin-only and do not change
the public API.
```

```text
Use devarm-debug. The checkout retry test is failing after the last change.
```

```text
Resume the devarm plan in docs/design/2026-07-14-bulk-export-design.md.
```

```text
Run devarm-review before we merge this branch.
```

If the agent asks a decision question, answer it explicitly. Silence is not approval in devarm;
unanswered decisions are recorded as `assumed — awaiting confirmation` and should be surfaced
again at later gates.

Git commits are developer-controlled. By default, devarm should leave changes uncommitted and
report commit-ready checkpoints with changed files, verification evidence, and a suggested commit
message. It may run `git commit` only after you explicitly ask for that commit, for example
`commit this checkpoint` or `commit after each task`.

## 7. When to invoke specific phases

- Use `devarm-brainstorm` for new features, behavior changes, components, and non-trivial
  refactors, or when you explicitly want devarm's design gate.
- Use `devarm-debug` as soon as a bug, failing test, or unexpected behavior appears.
- Use `devarm-review` after implementation or before merge.
- Use `devarm-finish` only when review findings are closed and you are ready to integrate or
  keep the branch.
- Use `devarm-retro` after shipping, or after a painful session, to improve the method itself.

Do not invoke devarm for simple questions, explanations, summaries, lightweight docs, diagrams,
or exploratory reading unless the user asks for it.

Do not start at `devarm-implement` unless `devarm-analyze` has already passed for the current
artifacts and current code.

## 8. Using devarm across tools

The same skill files work across tools, but discovery differs slightly:

- Codex and Cursor should discover installed skills from `.agents/skills` or their tool-specific
  skill directories.
- Claude Code can use the skills and should read project instructions through `AGENTS.md` or a
  `CLAUDE.md` that imports it.
- If a tool does not auto-trigger a skill, name the phase directly in your prompt, for example
  `Use devarm-brainstorm`.

The source of truth stays in this repository. Because installs are symlinks, editing a skill here
updates every installed copy.

## 9. Maintaining devarm itself

Use devarm on devarm. For method changes, update the relevant `skills/*/SKILL.md`, templates, or
`AGENTS.md`, then record the lesson in `CHANGELOG.md` when the method itself changed. Commit only
when the developer explicitly confirms.

For simple documentation fixes, update the docs directly and keep the change small.
