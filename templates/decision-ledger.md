# Decision Ledger

The single, reviewable home for every load-bearing implementation decision. Filled by
`devarm-ground` before the design is approved, and kept true through implementation
(`devarm-implement` / `devarm-review` flag any drift).

## Rules

- One row per decision that would otherwise be re-litigated at implementation time.
- **Evidence is mandatory** — a `file:line` citation or a named rule. A row without evidence is
  an ungrounded assumption and blocks approval.
- **Owner:**
  - `user` — a genuine trade-off with no dominant option, or a scope/product/behavior choice.
    Surface these explicitly for a decision; do not default them.
  - `agent` — a choice the code or rules force (e.g. an illegal import rules out the alternative).
    State it; no need to ask.
- **Tier** (how a decision is handled when it arises, esp. during implementation):
  - `design` — drops/replaces a designed component, changes semantics or user-visible behavior →
    **STOP and ask the user.**
  - `impl` — real trade-off, no change to intent (module placement, error strategy, shim) →
    **proceed with the recommended option, log the row, flag it in the turn summary.**
  - `mechanical` — naming, test layout → just do it (usually not worth a row).
- **Unanswered ≠ approval.** A question with no answer becomes a row with status
  `assumed — awaiting confirmation`, surfaced to the user — never treated as a silent yes.
- **Supersede, don't edit.** When a settled decision is reopened, the old row's status becomes
  `superseded (→ D<new>)` and a new row records the new choice + evidence. Then ripple-check:
  every row and design section that depended on the old answer is re-confirmed or revised —
  never leave a dependent row citing a superseded decision.

## Ledger

| # | Decision | Alternatives rejected | Evidence (file:line / rule) | Owner | Tier | Enforcing test | Status |
|---|----------|-----------------------|------------------------------|-------|------|----------------|--------|
| D1 | <the choice> | <what was considered and dropped> | `path/to/file.py:123` / `<rule name>` | user \| agent | design \| impl \| mechanical | `test_x::case` (or N/A) | approved \| assumed — awaiting confirmation \| superseded |
| D2 | | | | | | | |

> A behavioral decision with an empty **Enforcing test** will be silently violated. `devarm-tasks`
> must create that test task before any code that could break it; `devarm-analyze` flags rows that
> still lack one; `assumed — awaiting confirmation` rows are re-surfaced at every gate.

## The eight categories every design must resolve

Use this as a prompt list — each should appear as a ledger row or be explicitly N/A.

1. Layer / boundary legality
2. Idempotency / replay
3. Persistence shape
4. Canonical identity / keys
5. Exact seams / call sites
6. Determinism / ordering
7. Back-compat / migration
8. Failure / degradation posture
