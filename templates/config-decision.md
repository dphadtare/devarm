# Config / Numeric Decision — <name>

A numeric or config value is NOT "locked" until all four sub-answers exist. Locking only the
number (e.g. "cap = 2") is what forces post-design rewrites. Fill this, then record it as a
Decision Ledger row.

| Sub-answer | Value |
|------------|-------|
| **(a) What it bounds** | <the exact thing limited — e.g. "number of PRs generated per run", NOT "number of repos considered"> |
| **(b) Where it's enforced** | <the module/function + `file:line` that applies it> |
| **(c) Configurability granularity** | <hard-coded / global setting / per-app / per-run; and WHO may override + how it's recorded> |
| **(d) Behavior at the limit** | <what happens on overflow/violation — dropped? reported? escalated? at what threshold?> |

**Default:** <value> — **Rationale:** <why this default>

## Example (from a real feature)

| Sub-answer | Value |
|------------|-------|
| What it bounds | PR/fix generation only; diagnosis breadth is uncapped |
| Where enforced | `fix_scope_gate.select_fix_set()` |
| Granularity | global `config.multi_repo_fix_cap` (default 2), per-run human override recorded on the ticket |
| Behavior at limit | overflow repos reported in the single conclusion (not dropped); escalate when `overflow ≥ cap` |
