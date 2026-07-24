---
name: "devarm-finish"
description: "Use when implementation is complete, review findings are closed, and the work needs to be integrated. Verifies the full test suite fresh, then presents exactly four options (merge locally / push + PR / keep branch / discard) and executes the choice, including worktree cleanup. Never merges on failing tests; never discards without typed confirmation."
metadata:
  phase: 9
  produces: "merged branch, opened PR, preserved branch, or (confirmed) discarded work"
  next: "devarm-retro (recommended after ship)"
---

## Announce

"I'm using devarm-finish to close out this branch."

## Step 1 — Verify fresh, before offering anything

Run the project's FULL test suite (and lint/type gates) now, in this turn. If anything fails,
stop and report the failures — there are no integration options until green. A pass from an
earlier turn does not count.

**Env bleed sanity check:** if failures involve `Settings()` defaults, integration status flags,
or dry-run toggles with no feature-code change, inspect developer `backend/.env` (or equivalent)
leaking into tests before blaming the branch — fix or document `conftest` isolation first (spec
022: `PR_CREATION_DRY_RUN` / Guru creds). If optional deps block part of the suite (e.g.
`tree_sitter_python`), state the exclusion explicitly in the verification report; do not treat
"full suite" as green while silently skipping paths.

Also confirm the findings ledger has no `open` blocking rows and the Decision Ledger has no
`assumed — awaiting confirmation` rows.

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
