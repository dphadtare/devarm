---
name: "devarm-finish"
description: "Use when implementation is complete, review findings are closed, and the work needs to be integrated. Verifies the full test suite fresh, then presents exactly four options (merge locally / push + PR / keep branch / discard) and executes the choice, including worktree cleanup. Never merges on failing tests; never discards without typed confirmation."
metadata:
  phase: 10
  produces: "merged branch, opened PR, preserved branch, or (confirmed) discarded work"
  next: "devarm-retro (recommended after ship)"
---

## Announce

"I'm using devarm-finish to close out this branch."

## Artifact and evidence handoff contract

Before acting or resuming, read the current repository rules, current artifacts, and the diff;
current evidence takes precedence over any stale summary. Revalidate artifacts, require fresh full-suite evidence, and
current artifact validation before presenting lifecycle choices, and record the validator output.
Optional adapters may provide lifecycle metadata, but adapter use cannot bypass native gates.

Explicit lifecycle authority remains: commit, push, merge, delete, reset, and discard are separate
operations and require the applicable user choice. Discard requires typed discard confirmation.
If the validator is unavailable, record that limitation and keep the human checklist authoritative.

## Step 1 — Verify fresh, before offering anything

Run the project's FULL test suite (and lint/type gates) now, in this turn. If anything fails,
stop and report the failures — there are no integration options until green. A pass from an
earlier turn does not count.

**Env bleed sanity check:** if failures involve `Settings()` defaults, integration status flags,
or dry-run toggles with no feature-code change, inspect developer `backend/.env` (or equivalent)
leaking into tests before blaming the branch — fix or document `conftest` isolation first. **Fixture-
path bleed:** when a mass of unrelated unit
tests fail together (publish/action/git scope) while feature-targeted tests pass, check whether
a hardcoded mock repository path (e.g. `/tmp/repo`) **exists on disk** as an empty or stale
directory — path sanitizers that require files to exist in the worktree will strip mocked
allowlists and produce false reds. Confirm by reproducing on `main` or removing the stray path
before chasing branch regressions. *Failure-class rationale (a prior failure): empty `/tmp/repo` caused 35
failures across publish/action tests; all green after removal + conftest cleanup fixture.* If
optional deps block part of the suite (e.g.
`tree_sitter_python`), state the exclusion explicitly in the verification report; do not treat
"full suite" as green while silently skipping paths.

Also confirm the findings ledger has no `open` blocking rows and the Decision Ledger has no
`assumed — awaiting confirmation` rows.

**Pre-PR / pre-push integrity (when the user asks for a PR):** before `git push` or
`gh pr create`, confirm (1) `git status` shows **no untracked files imported by staged code**
(new modules referenced by modified files must be staged), (2) ruff/lint was run on **new test
files** with the same scope CI uses (local IDE-only checks miss SIM115-style rules), (3) for
git/worktree features, at least one real-git fixture test exists if the plan required it, and
(4) backend unit tests were run with the **same command CI uses** (e.g. `pytest tests/unit -q`
from `backend/`) — a feature-targeted subset is not sufficient for PR/merge, (5) **staging
parity:** no feature wiring remains unstaged while new modules are staged — run
`git diff --name-only` and `git diff --cached --name-only`; every importer of a staged module
(`unified.py`, workflow glue, skill cross-refs, `conftest` fixes) must appear in the index.
*Failure-class rationale (a prior failure): `nr_link_intake.py` staged but `unified.py` /
`remediation_workflow.py` unstaged at finish; a prior failure: core modules untracked at PR time.*

For a PR, also confirm that `git rev-list --count <base>..HEAD` is greater than zero before
attempting `git push` or `gh pr create`. If it is zero while the worktree or index contains the
feature, stop and report that a commit is required; do not spend the remaining finish steps on an
unopenable PR. The commit remains a separate lifecycle operation governed by the explicit commit
policy.

**Bounded external verification:** if the full suite can spawn a model, browser, network service,
Docker job, or other external subprocess, give that command an explicit wall-clock timeout. When
the repository can separate deterministic tests from external smoke tests, run the deterministic
suite first and run the external subset separately with a **15-minute maximum per command**. If
the suite cannot be separated, apply the timeout to the full command. A timeout, keyboard
interruption, or orphaned subprocess is **verification incomplete**, not green: capture the last
test node/process, clean up the child process, and do not present lifecycle options until the
required verification is rerun or the user explicitly accepts the limitation as a deferred
deployment check. This is a category-scoped rule for external-runtime verification, not a reason
to add a deterministic response gate to the product.

## Step 2 — Determine the base branch

`git merge-base HEAD main || git merge-base HEAD master`, or ask ("this split from main —
correct?").

## Step 3 — Present exactly four options (no essay)

```
Implementation complete, suite green. What would you like to do?
1. Merge back to <base> locally
2. Push and create a Pull Request
3. Keep the branch as-is (you'll handle it)
4. Discard this work
```

## Step 4 — Execute

- **1 Merge locally:** checkout base → pull → merge → re-run tests ON THE MERGED RESULT →
  delete feature branch only after green.
- **2 PR:** push with `-u`, `gh pr create` with a Summary + Test-plan body. Link the design
  doc and spec in the body.
- **3 Keep:** report branch name and worktree path; touch nothing.
- **4 Discard:** destructive — list exactly what will be deleted (branch, commits, worktree)
  and require the user to type `discard` before `git branch -D`.

## Step 5 — Worktree cleanup

If the work happened in a worktree: remove it for options 1 and 4; keep it for 2 and 3.

## Red flags

Never merge or open a PR on failing tests; never force-push unrequested; never delete work
without the typed confirmation; never end with an open-ended "what next?" — the four options
ARE the question.

## Hand off

After 1 or 2, recommend `devarm-retro` on the session — that's when lessons are freshest.
