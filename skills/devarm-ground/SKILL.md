---
name: "devarm-ground"
description: "Use DURING brainstorming, after a design is presented and BEFORE the user approves it. Grounds every 'reuse/wrap/extend/import/call existing X' claim against the real code and repo rules with file:line evidence, resolves the ten implementation-decision categories that otherwise leak into implementation (including config semantics, data-consumer audit, and runtime contract surfaces), and appends a Detailed Design + Decision Ledger to the design doc. Blocks design approval until no ungrounded assumption remains."
metadata:
  phase: 2
  produces: "Detailed Design (grounded) + Decision Ledger sections appended to the design doc"
  next: "return to devarm-brainstorm approval gate; halt unless end-to-end was explicitly requested"
---

## Why this skill exists

Specs and plans stay high-level. The expensive decisions — the "what does what, when, and
how" — live at the **boundary between the new code and the code that already exists**, and those
are usually only discovered when an engineer opens the existing file during implementation. That
is the drift this kills.

**The rule this skill enforces:**
> Every "reuse / wrap / extend / import / call existing X" claim is FORBIDDEN from becoming a
> requirement until you have opened X and confirmed the dependency is legal under the project's
> architecture/boundary rules and file-size budgets, with the `file:line` recorded.
> Dead scaffolding is not reuse — "exists" ≠ "wired into the live path".

## Announce

"I'm using devarm-ground to verify this design against the real code before we lock it."

## Artifact and rule handoff contract

Before acting, record the active repository and branch in the artifact metadata. Discover
applicable target-repository instructions and link the canonical rule inventory; the
target-repository rule wins over a devarm default, and material conflicts require a visible
disposition. Run the optional validator; if it is unavailable, record the limitation and keep
the manual checklist authoritative. The optional validator is not required for the native method.
A deterministic blocking error stops the handoff; warnings remain visible and do not imply
approval. Preserve explicit approval gates and mark an unanswered decision `assumed — awaiting
confirmation`. If a settled decision is superseded, ripple-check dependent artifacts and re-check
the affected evidence before continuing.

## Inputs

- The draft design doc from `devarm-brainstorm`.
- The target repo's rules: any architecture-boundary rule, design-principles / file-size rule,
  no-duplicate-concept rule, and pattern/anti-pattern catalog (check `.cursor/rules/`,
  `.specify/memory/`, `AGENTS.md`, `CONTRIBUTING.md`). If none exist, apply the devarm
  defaults in `AGENTS.md` and `devarm/templates/code-standards.md`.

## Process (create a task per step, complete in order)

**Visual grounding for multi-surface changes:** when the brainstorm delta checkpoint produced an
as-is/to-be visual, re-open both diagrams during grounding. Annotate every existing-system node
and edge with current-code `file:line` evidence, mark any unverified relationship explicitly, and
confirm that the to-be flow changes only the grounded delta. A diagram is an evidence aid, not a
replacement for the ten decision categories or the Decision Ledger. If the change is a single
local surface and the design records `diagram: N/A` with a reason, no visual is required.

### Step 1 — Build the Reuse Inventory

Extract EVERY reference in the draft to something that already exists, tagged with the verb:
`reuse | wrap | extend | import | call | subclass | persist-to | hook-into | **preserve**`. These
are the claims that must be grounded. New-only components are grounded in Step 3.

**`preserve`** — user or design explicitly requires an existing tool/service/wiring to stay
untouched ("confirm ground reality", "don't change existing provider wiring"). Record live path +
what the new feature must **not** replace.

### Step 2 — Ground each item against real code (file:line evidence)

Open the actual files. A claim is grounded only when you can cite `path:line`. For each item:

1. **Shape** — does it exist with the assumed signature / sync-vs-async / return type / state
   model? Is it actually wired into the live path (not dead scaffolding)? Cite the definition line.
2. **Legality** — is the dependency direction legal under the repo's boundary rules? (e.g. a
   lower layer importing an upper one is illegal). If the reuse requires an illegal import, it is
   REJECTED — record the alternative (own the policy locally, read shared config, move the
   contract to a neutral module, etc.).
3. **God-file** — does it add logic to a file already over the repo's size budget? If so, the
   design MUST place logic in a **named** new module and leave only a thin seam, with a **hard
   line budget** for what the existing file may gain (not "watch item"). Record the module name
   and the number.
4. **Duplication** — does it re-declare a concept (enum, status, constant, config) that already
   has a home? Cite the home and reuse it; do not create a second.
5. **Git / worktree layout** — when the design touches checkout, fetch, push, or publish on an
   **existing remote branch** (reuse, append, rebase, force-with-lease), open the worktree
   clone path (`worktree_service`, mirror cache setup) and cite: clone mode (`--mirror` vs
   standard), `remote.origin.fetch` refspec, and whether code assumes `origin/<branch>` vs
   `refs/heads/<branch>`. A design that assumes standard-clone layout against a mirror-backed
   worktree is **REJECTED** until a real-git fixture or spike proves the incantation.

If any item fails 1-5, revise the design NOW (before approval), then re-ground.

### Step 3 — Resolve the ten implementation-decision categories

Every category must have an explicit, evidence-backed answer before approval. Mark N/A explicitly
if it doesn't apply.

| # | Category | Question to answer with evidence |
|---|----------|----------------------------------|
| 1 | Layer / boundary legality | Which layer does each new module live in? All imports legal? Which reuse claims were rejected as illegal, and what replaced them? **Parallel-capability variant:** when adding automation adjacent to an existing agent/tool path, document both paths in the ledger — preserved path, new path, overlap rule, and a test or grep guard that new code does not illegally import or replace the preserved path. |
| 2 | Idempotency / replay | For durable/retryable work: step granularity + key? What makes a re-run produce no duplicates (naming, "already exists" path, unique constraint)? |
| 3 | Persistence shape + consumer audit | Scalar vs blob vs new table? If new: exact columns, keys, unique constraint, migration id. Then enumerate EVERY existing reader/writer of the old shape (sync/poll jobs, list/detail APIs, dashboards/counts, resume/replay paths, notifications) and mark each in-scope or explicitly out-of-scope. An unlisted consumer is a latent P0. **New-producer variant:** this audit ALSO fires when new code starts *producing* an existing cross-layer/persisted field (a Result/Output flag, list, or status) from a new path — not just when the shape changes. Enumerate the invariants existing consumers already assume about that field (status mapping, persistence filters that silently drop malformed rows, notification routing) and confirm the new producer honors every one; a new producer that violates an implicit invariant (e.g. sets a "partial success" flag with no published artifact) is the same latent P0. **Render-path variant:** when a new/changed field is meant for operator-facing copy (escalation/issue tracker/operator chat messages, handoff `user_message`), name the render function (`build_*_user_message`, `_append_*_sections`, template) and confirm the field is actually rendered — not only attached to `final_output` or notification context. Dict populated + message silent is a latent P0 (a prior failure: `partial findings` vs `message renderer`). **Carrier-field variant:** when a new field must be *consumed by a later phase/process* (not just persisted), trace EVERY serialization hop between producer and consumer — typed model → dict → typed model → prompt string → scope/allowlist filter — and confirm no hop silently drops it. Name the typed model `extra` policy of each model it crosses (`extra='ignore'`, the default, silently discards an undeclared field) and any explicit field allow-list or scope filter on the path, and confirm the consumer actually *reads/renders* it. A field the producer emits but a mid-path model doesn't declare, or the consumer's prompt never renders, ships the feature **inert** while all unit tests stay green (a prior failure: `prior-context reconciliation` dropped by `downstream payload model(extra=ignore)` AND never rendered into the repair prompt prompt — the entire reconciliation feature was a no-op). **Optional-input branch variant:** when new context is attached only under a conditional (e.g. "when attachments exist", "when URLs found"), enumerate EVERY persist/cache/copy path — including cached early-return branches — and confirm the new field syncs wherever sibling intake fields sync. A field wired only inside the "happy" branch is missing on the no-attachment / no-URL path (a prior failure: `link insights` + stack promotion persisted only inside the attachment block until R3 fix). |
| 4 | Canonical identity / keys | The ONE identifier used across modules; where any other id is mapped to/from it, at which edge only. |
| 5 | Exact seams / call sites | The precise `file:line` (or function) where new code hooks into existing flow, per hook. |
| 6 | Determinism / ordering | Any ordering/selection/tiebreak rule so the same input always yields the same output. |
| 7 | Back-compat / migration | What must stay byte-identical? Rollout story? The single-item / empty / disabled path? **Cutover-null variant (required when adding nullable ownership / lease / claim columns):** state what happens to *existing* in-flight rows with NULL after migrate (reaper? claim? heartbeat? ops SQL?). "New code only writes the columns" is not a plan — orphaned RUNNING/NULL rows are a P0 cutover bug. |
| 8 | Failure / degradation | Per failure mode: raise, retry, best-effort-degrade, pause, or escalate? The safe fallback? |
| 9 | Config / limit semantics | For every numeric or configurable value: (a) what exactly it bounds, (b) where it is enforced, (c) configurability granularity (global / per-entity / per-run + who may override), (d) behavior at the limit (drop / report / escalate + threshold). A bare number is not a decision. Use `devarm/templates/config-decision.md`. |
| 10 | Runtime contract surfaces | Which prompts, output contracts, and SKILL/instruction files consumed at runtime are affected? Four sub-checks: **(a) Pairing** — every contract change lists its paired prompt/skill update (skill files ARE runtime artifacts; unpaired changes ship conflicting guidance). **(b) Value grounding** — every runtime value a prompt/skill/contract *states* (enum member, threshold, constant, id format) is cited to its source symbol `file:line`; a stated number/enum that isn't grounded against code is drift waiting to happen. **(c) Directive context sweep** — for any prompt-injected instruction gated on a runtime value, enumerate EVERY context that builds that prompt and confirm the instruction stays true (or is suppressed) in each; a directive correct on the primary path can contradict an authoritative block on an expansion/variant path (e.g. a count that means "single-repo app" on one path but "pinned to one repo" mid-coordinated-fix on another). **(d) LLM-output realism** — when a control signal or downstream predicate is derived from **LLM free-text output** (change-detection over a generated summary, an intent/classification branch, a "did it comply?" check), validate it will actually fire as intended given *realistic, non-verbatim* model output — or key it on a stable structured field instead. And when LLM text is rendered to a specific surface (operator chat mrkdwn, HTML, a card), specify the presentation/normalization contract. A control signal that almost never (or always) fires is a dead predicate; unnormalized LLM text ships malformed to the surface. (Failure-class rationale: `changed` keyed on free-text `understanding` the model rarely reproduces → the no-change short-circuit almost never fires, L2, the core cost goal; run-on `1) … 2) …` lists shipped unreadable to operator chat until reported.) |

### Step 4 — Write Detailed Design + Decision Ledger into the design doc

Append two sections (use `devarm/templates/decision-ledger.md` for the table):

- **`## Detailed Design (grounded)`** — a short subsection per touched area answering the
  relevant Step-3 categories, each backed by a `path:line` citation.
- **`## Decision Ledger`** — one row per load-bearing decision: `Decision | Alternatives rejected
  | Evidence (file:line / rule) | Owner | Tier | Enforcing test | Status`. `owner: user` for
  genuine trade-offs (surface these for an explicit decision); `owner: agent` for choices the
  code/rules force. Every row MUST have non-empty Evidence. If the user does not answer an
  `owner: user` question, mark the row `assumed — awaiting confirmation` and **re-surface it at
  every later gate** — silence is never approval.

### Step 5 — Approval gate

Report the checklist. The design is approval-ready only when all hold:

- [ ] Every Reuse Inventory item grounded with `file:line`, confirmed legal, and confirmed wired
      (not dead scaffolding).
- [ ] No reuse requires an illegal import; rejected ones have a recorded alternative.
- [ ] No new logic grows a god-file; each lands in a named module with a hard line budget.
- [ ] All ten decision categories answered or explicitly N/A.
- [ ] Every config/limit value has its four sub-answers (bounds what / enforced where /
      granularity / at-limit behavior).
- [ ] Every changed data shape — and every existing cross-layer field a new path starts
      producing — has a consumer audit; every changed contract has its paired
      prompt/skill update listed; every runtime value a prompt/skill states is grounded to its
      source `file:line`; every runtime-gated prompt directive is swept across all
      prompt-building contexts.
- [ ] Detailed Design + Decision Ledger written to the design doc.
- [ ] Every ledger row has evidence; every `owner: user` row surfaced; no row silently defaulted
      from an unanswered question.

If any box is unchecked, revise and re-run the failing step. Then return to the
`devarm-brainstorm` approval gate.
