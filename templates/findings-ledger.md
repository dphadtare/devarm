# Findings Ledger — <feature>

One durable home for all review findings across every review pass (including parallel/independent
review sessions). Reviewers **append**; the implementer works it top-to-bottom. Do not re-feed
raw review transcripts — add rows here instead.

## Rules

- Every finding gets a stable ID and a **code-evidence** verdict (`file:line`), not an opinion.
- Verify in both directions: a reviewer's finding can be wrong, and so can an implementer's
  rebuttal. Trace the actual runtime path before setting a verdict.
- **Check against the Decision Ledger first:** a finding that contradicts a recorded `owner: user`
  decision is not a bug — mark it `by-design (D<n>)` unless the user reopens the decision.
- `status` moves through: `open → fixed | deferred | rejected | by-design`. Never delete a row;
  supersede it. Status strictness:
  - **fixed** — only after verification output is seen (test/lint run); cite the commit if one
    was explicitly authorized, otherwise cite the diff/checkpoint.
  - **deferred** — real but consciously postponed; MUST carry a tracked task id.
  - **rejected / by-design** — evidence recorded so it is never re-litigated.

## Ledger

| ID | Source | Claim | Severity | Verdict + evidence (file:line) | Status | Owner |
|----|--------|-------|----------|-------------------------------|--------|-------|
| F1 | <review pass / session> | <what the reviewer claims is wrong> | blocking \| should-fix \| nit | <confirmed/refuted + `path:line`> | open \| fixed (<commit or diff/checkpoint>) \| deferred (<task id>) \| rejected \| by-design (D<n>) | user \| agent |

## Turn close (every review/fix turn)

- **Already fixed this turn:** <ids + commit if authorized, otherwise diff/checkpoint>
- **Awaiting your decision:** <ids needing the user's call>
