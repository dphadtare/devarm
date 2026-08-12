# devarm changelog

Every entry records a method change and the session/failure that motivated it. Maintained by
`devarm-retro` — a lesson is only "done" when it's a gate in the method, not just a note.

## 2026-08-13 — portable retro promotion and normative-skill audit

Motivated by the review of TC-derived devarm evolution: incident evidence was repeatedly embedded
in normative skills as `Session evidence`, ticket/spec references, and product-specific narratives.
The method change adds a retro generalization gate requiring a failure category, domain-neutral
invariant, enforcement point, applicability boundary, and a two-shape generalization check. New
promotions must be classified as portable core, category-scoped, or target-only.

The normative `skills/devarm-*/SKILL.md` files were audited and their incident provenance was
removed or generalized while historical changelog evidence was preserved. Contract tests now
reject incident markers in normative skills. No runtime, persistence, or external-service behavior
changed.

## 2026-08-08 — spec 033 fix-loop worktree merge seed retro (DEV-323494 / PR #124)

Motivated by DEV-323494 postmortem → brainstorm → ground → spec/plan/tasks/analyze →
implement → findgap → challenge → split-brain re-wire → findgap → challenge →
`code_fix_attempts` / coverage-loop fix → push (commits `0667d3d`, `b4d6af5` on
`032-nr-link-intake`). Core ledger (D4′ worktree seed, D5 full re-declare prompt, D6 stray
dirt accepted) held. Expensive tail: (1) helpers + tests landed without `unified.py`
wiring — findgap said green, challenge found split-brain; (2) D1 used `retry_count` but
infra `action_prep` and pre-validation **coverage `continue`** paths skipped the repair
counter increment — same DEV-323494 failure mode on second code-fix; (3) merge gated on
`code_fix_attempts`, prompts on `retry_count` — coverage feedback never shown; (4) source
grep wiring test insufficient until behavioral `run_action_phases` test added; (5) user
"fix required / ignore rest" + challenge-findings before second fix batch worked well.

Four existing gates tightened (no new skills):

- **devarm-plan** — **Fix-loop retry-counter seam**: enumerate all loop counters + every
  `continue` between success and iteration end; one repair-retry signal for merge + prompt
  + discard; routing characterization test per non-obvious loop path.
- **devarm-analyze** — Pass 2 **Continue-path side-effect audit** for re-entrant loops.
- **devarm-tasks** — God-file-only helper wiring requires behavioral orchestrator test;
  source grep alone insufficient.
- **devarm-implement** — **Wiring completeness sweep** before task-done (grep call sites,
  run wiring test, detect split-brain).

**Not changed:** native findgap/challenge already covered by `devarm-review` challenge-before-fix-all
and required/defer state split; doc drift (`retry_count` vs `code_fix_attempts`) deferred as
hygiene; D6 / god-file growth accepted per ledger.

## 2026-08-07 — spec 032 human NR link intake retro (PR #124) — native method pass

Motivated by the DEV-323859 postmortem → brainstorm → ground → spec/plan/tasks/analyze →
implement → findgap/review tail → devarm-finish → PR #124 session, plus explicit user direction
to **adopt external patterns natively in devarm** (Superpowers skill-check, speckit-clarify,
preserve-existing-tool grounding) instead of depending on those tools.

Core Decision Ledger held through ship. Expensive patterns: (1) findgap on ~10 design Q&A turns;
(2) user "confirm ground reality" on existing NR MCP tools → **PRESERVE** inventory; (3) session
inventory + superpowers adoption intent; (4) post-implement clarify on `one.newrelic.com`
(prerequisites pointed at spec 019 not 032); (5) R3 optional-input branch seam; (6) partial git
staging at finish; (7) 35 false-red tests from empty `/tmp/repo`; (8) SC-001 mock-heavy (existing
review gate).

**One new skill + gate tightenings:**

- **devarm-clarify** (NEW, phase 4) — native ≤5-question ambiguity gate + code-grounded reconcile;
  optional Spec Kit delegate after feature-dir sanity.
- **AGENTS.md** — clarify in pipeline; invocation preamble; native-over-external policy.
- **devarm-brainstorm** — Preserve trigger; method inventory; findgap → native review.
- **devarm-ground** — `preserve` verb; parallel-capability (cat 1); optional-input branch (cat 3).
- **devarm-spec** — hand off to clarify before plan.
- **devarm-review** — code-grounded spec reconcile.
- **devarm-finish** — fixture-path bleed + staging parity.
- **devarm-retro** — method adoption bullet.
- Phases renumbered: plan=5 … retro=11.

**Not changed:** domain skills (tc-postmortem) stay project-specific; SC-001 mock audit unchanged.

## 2026-08-05 — spec 026 GitHub App auth hardening retro (PR #86)

Motivated by the GitHub App auth hardening session on PR #86: findgap → challenge → alignment
notes → one-by-one disposition lock → ground (revised R5) → spec → plan → tasks → analyze →
implement (TDD) → review approve → findgap/challenge tail → push `00ee2e70`. Core ledger (R1
path refresh, R5 share-when-`config is None`, R7 must-have tests, R3/R2 deferred) held; code
shipped clean. Expensive or near-miss patterns: (1) plan’s test patched a non-existent
`github_app_auth.settings` while production locally imports `backend.config.settings` — analyze
caught as HIGH A5 before implement; (2) post-implement findgap re-ranked ledger-deferred
residuals (Git 401 remint, R2 URL-inject, Helm `b64dec`) as High merge urgency until challenge
restored the defer split (same class as 030); (3) seven “recommended” turns locking dispositions
one-by-one before “Accept all”; (4) user needed a separate explainer that R3/FG-03 blocks
**cutover**, not code merge.

Four existing gates tightened (no new skills):

- **devarm-plan** — Step 5 **Settings/config patch seam**: patch the binding site
  (`backend.config.settings.<attr>` when that is the import); never invent
  `feature_module.settings` for a local import.
- **devarm-analyze** — Pass 2: verify planned settings patch strings against real imports
  (HIGH if no-op); Pass 3: `owner: user` deploy-gates get an explicit “blocks cutover, not
  merge” sentence.
- **devarm-review** — ledger status language (`deferred for this PR` / deploy-gate /
  out-of-scope / follow-up) cannot become **Required for merge** after findgap re-labeling.
- **devarm-brainstorm** — **Disposition batch (≥3 Recommended remedies)**: present full batch +
  accept-all; sequential deep-dives optional after, not instead of the batch.

**Not changed (deliberate):** grounding’s R5 revision (share only when `config is None`) worked
and needed no new gate; TDD red→green and god-file net≤0 held; R3 remaining as ops evidence
(secrets owner) is correct process, not a method hole; parallel findgap transcript evaluation
was covered by existing challenge-before-fix-all.

## 2026-08-05 — spec 030 multi-pod worker concurrency retro (PR #108)

Motivated by the multi-pod concurrency session: brainstorm→ground→spec→plan→tasks→analyze→
implement→review→long findgap/challenge/fix tail→finish→PR #108. Core ledger (enqueue + lease +
Redis leader) held; the expensive tail was (1) soft-delete API/tests stripped from shared
`routes.py` / `ticket_job.py` while #107 landed on the same surfaces, (2) Alembic dual-head when
lease migration reused revision `0026`, (3) cutover orphans when nullable lease columns replaced
heartbeat stale without a NULL-row path, (4) D2 `waiting_signal` reuse shipping a stuck-requeue
UX until mid-flight supersede, (5) findgap re-ranking by-design residuals as top-5 until
challenge + "fix required only", (6) user had to *ask* for architecture/as-built diagrams
and for elaboration mid-Q loop ("I'm not getting…", "help me decide/understand").

Seven existing gates tightened (no new skills):

- **devarm-implement** — precondition **Shared-surface collateral check** on god-file edits vs
  `main`; Verify **Alembic graph** single-head / no reused revision ids; post-implement
  **as-built diagram** before offering review when topology changed.
- **devarm-plan** — Step 5 **Migration graph seam**: parent = current `alembic heads`; unique
  revision id; polish re-check.
- **devarm-ground** — category 7 **Cutover-null variant** for nullable ownership/lease columns.
- **devarm-analyze** — Pass 3 **Shared policy matrix** (status × channel) when centralizing
  enqueue/claim.
- **devarm-review** — end-of-turn split adds **Required for merge** vs **Defer / optional**;
  bare "fix the findings" must not expand Defer.
- **devarm-brainstorm** — **Architecture diagram gate** before concluding multi-component
  sections / approval; **Confusion / decide stop** before the next Recommended question;
  diagrams persisted into the design doc.

**Not changed (deliberate):** challenge-findings correctly deferred zombie task-cancel and
D25 renew-loop (spec out-of-scope / by-design); finish CI-command gate from 029 held (caught
ruff I001 on new tests); claim-before-`create_task` and Redis fail-closed needed no new gates.

## 2026-08-05 — spec 029 fix verification policy retro (DEV-319678 → skills-only policy)

Motivated by the DEV-319678 postmortem → design → spec/plan/tasks/analyze/implement/review →
findgap/challenge → PR #106 CI tail: targeted feature tests were green but CI failed on repo-wide
`test_skill_content_requirements` (new skill missing untrusted guard + reference-only classification)
and on main-branch triage dedup tests (identical error messages collapsed by issue signature).
Cross-section Phase 1 vs Phase 1b contradiction escaped analyze wording-lock until findgap; user
skipped `devarm-finish` and opened PR directly.

Five existing gates tightened (no new skills):

- **devarm-plan** — Step 5 **OpenCode skill contract seam**: producing vs reference-only,
  untrusted-input guard, skill-content test module named, full backend unit CI command in polish.
- **devarm-tasks** — decision→test: new OpenCode skill dirs require skill-content contract task
  (untrusted guard + producing/reference-only allowlist).
- **devarm-analyze** — Pass 2: **workflow-order pairs** in cross-section sweep; **New OpenCode
  skill contract** checklist when plan adds a skill directory.
- **devarm-implement** — Verify: run skill-content tests or full `pytest tests/unit -q` when
  touching `backend/opencode/skills/**` — targeted subset insufficient.
- **devarm-finish** — Pre-PR integrity item (4): same backend unit command CI uses, not subset only.

**Not changed (deliberate):** challenge-findings downgrade of G2/N1 (accepted D7 Python residual)
worked; triage test fix was main-branch dedup alignment, not a new devarm gate; context-overburden
question answered by thin skill design (D8) — no new context budget rule.

## 2026-07-31 — spec 028 reuse-branch reconciliation retro (inert feature behind green tests)

Motivated by the reuse-branch reconciliation session: design→ground→spec→plan→tasks→implement all
completed with **52 tasks and a green suite**, and `devarm-review` **approved** — yet the feature was
**completely inert**. `challenge-findings` + live E2E exposed the truth in a long, expensive tail:
`prior_change_reconciliation` was silently dropped crossing `DiagnosticPayload` (Pydantic
`extra=ignore`) and was never rendered into the code_fix prompt; the reconciliation `revert` (a file
**deletion**) was then stripped by `sanitize_publish_paths` at 4 call sites + 2 discard sites. The
flagship integration test **mocked `run_action_phases`**, hiding every one of these. The deletion bug
was point-patched one call site per live-E2E cycle (L1→L1b→L1c = 3 rebuild+run+log cycles).

Four existing gates tightened (no new skills):

- **devarm-ground** — Step 3 category 3 **Carrier-field variant**: for a new field consumed by a
  later phase, trace every serialization hop (typed model → dict → typed model → prompt → scope
  filter), name each model's Pydantic `extra` policy, and confirm the consumer renders it — a
  dropped/unrendered carrier ships the feature inert though tests are green.
- **devarm-plan** — Step 5 **Change-set pipeline seam**: a new *change type* (deletion / rename /
  mode-change) must be traced through EVERY change-set filter (apply → merge → sanitize → discard →
  commit → publish); an existence-based filter silently drops a deletion.
- **devarm-review** — QA lens **Mock-boundary / inert-feature audit**: per behavioral SC, state
  whether its test hits the real seam or mocks it; a mocked-seam SC is not covered — require one
  unmocked/live test or mark completion provisional.
- **devarm-debug** — **Shared-helper bugs**: when the root cause is a shared filter/sanitizer/
  serializer, grep all call sites and fix at the source *before* the first fix — one-per-cycle
  patching is fix-stacking across (expensive live) runs.

**Not changed (deliberate):** the git-layout gates from the 027 retro **held** (diagnose-on-base,
mirror fixtures, god-file budgets all survived to the end); the L2 `revert_file` MCP-tool-adherence
gap is low-value and self-healing (the publish path now handles the deletion regardless of mechanism).

## 2026-07-30 — spec 027 ticket PR reuse retro (mirror git + PR/CI tail)

Motivated by the ticket PR reuse session: design→implement was sound on DB reuse (D1–D6), but
**P0 mirror/worktree git layout bugs** escaped mocked tests until local Docker E2E; a long tail of
findgap → challenge → fix cycles re-litigated god-file and applied-files severity; PR almost
shipped with **untracked core modules**; CI failed on ruff SIM115 + checkout test after
diagnostic added subprocess `rev-parse`.

Five existing gates tightened (no new skills):

- **devarm-ground** — Step 2 item **5 (Git/worktree layout)**: mandatory mirror/refspec/`origin/*`
  check when reusing existing remote branches.
- **devarm-plan** — Step 5 **Git layout seam**: real-git mirror/worktree fixture required in plan;
  mock-only `_run_git` insufficient for merge gate.
- **devarm-tasks** — decision→test: git reuse/checkout ledger rows require real-git fixture test.
- **devarm-implement** — Verify: **subprocess patch sweep** when extending checkout/diagnostic flows.
- **devarm-finish** — Pre-PR integrity: no untracked imported modules; ruff on new test files.

**Not changed (deliberate):** findgap/challenge downgrade of speculative findings worked; applied-files
review friction was polish, not merge-blocking after live append publish (DEV-321527 #8).

**Retro durability note:** devarm lives in `vhosts/devarm` and is symlinked globally via
`install.sh` — never vendor into feature repos.

## 2026-07-29 — spec 026 review semantic-minimality retro (DEV-320248 postmortem)

Two blocking defects escaped analyze, review, and all wording-lock tests: F1 (Phase 1c item 10
blocked runs with zero `ticket_expectations`) and G1 (correctness floor contradicted Phase 1e
test-file severity). Found only via runtime prompt/directive sweep (F1) and findgap with executed
ship-gate predicates (G1). Planning baseline drift (382 vs 351 SKILL lines) when implement started
on a stale branch.

Four existing gates tightened (no new skills):

- **devarm-analyze** — Pass 2: mandatory **cross-section contradiction sweep** when ≥2 sections of
  the same runtime skill/prompt change; HIGH if no carve-out or routing guard on realistic
  populations (empty list, test path, deferral path).
- **devarm-tasks** — decision→test: **routing characterization test** required when a new rule can
  flip an existing ship-gate boolean (wording-lock alone insufficient).
- **devarm-implement** — Precondition 4: **base-branch drift check** before task 1 and after any
  `git pull` / merge during the feature.
- **devarm-review** — architecture lens: **cross-section pairing checklist** for skill/prompt diffs
  (e.g. Finding Severity ↔ Phase 1e).

**Not changed (deliberate):** findgap/challenge downgrade of speculative findings worked; PR-merge
alignment was user process, not a method gap.

**Retro durability note:** devarm lives in `vhosts/devarm` and is symlinked globally via
`install.sh` — never vendor into feature repos.

## 2026-07-25 — spec 025 slack-conversational-repair retro

Motivated by the Slack conversational-repair session, whose long tail was live-testing + repeated
`/findgap` → challenge → fix cycles on a **re-entrant state machine** (a Slack thread re-processed
across re-mentions, mid-flight arrivals, no-change passes, reopen). The pure decision-log module
was clean; ~6 same-class bugs lived in the worker↔coordinator↔session_service **state-transition
seam** — F1 (ASSESSING loop), F3 (dropped card), F6 (two-mention state downgrade), L1 (unsupported
re-mention closed an active investigation), and the R2→R3 re-queue signal flip. A second class was
**LLM-output realism**: `changed` keyed on free-text `understanding` the model rarely reproduces so
the no-change short-circuit almost never fires (L2 — the feature's core cost goal), and run-on
`1) … 2) …` lists shipped unreadable to Slack until reported. A third pattern was **silent design
deviation in the fix loops**: several `/findgap` → challenge → fix iterations *changed* agreed
behavior (the conditional-reset realignment, the unsupported re-mention handling) rather than merely
implementing it, and nothing in the fix loop forced a consult — the developer had to repeatedly ask
"are we changing the design?"

Three recurring patterns cleared the ≥2/severe bar. Six existing gates tightened (no new skills):

- **devarm-plan** — new step **5b: State-Transition Table** required whenever the feature adds/
  changes a re-entrant or multi-actor state machine (re-mention, retry, mid-flight, resume, reopen,
  cancel). Enumerate every `(current_state × incoming_event)` → resulting state + side-effects +
  owning module, flagging cells that must be non-schedulable/preserving. *Why:* the fix-tail bugs
  were all unenumerated `(state,event)→wrong terminal state` cells; a narrative walkthrough is
  silently skippable, a missing table cell is visible.

- **devarm-analyze** — Pass 3 control-flow walkthrough now **walks that table cell by cell** to
  terminal state (no loop / no downgrade / no unintended close-reset), treating a missing or
  hand-waved cell as a HIGH finding. *Why:* analyze's narrative-only walkthrough (and, here, being
  skipped entirely when the feature went design→implement) let the state-transition class through.

- **devarm-tasks** — decision→test traceability extended: every non-schedulable/preserving cell of
  a State-Transition Table gets an acceptance test asserting its **terminal state + side-effects**
  and the forbidden outcomes as negatives. *Why:* L1/F6 broke "repair preserves an active
  investigation" because no test pinned those transitions' terminal states.

- **devarm-ground** — category #10 (runtime contract surfaces) gains sub-check **(d) LLM-output
  realism**: a control signal/predicate derived from LLM free-text must be validated to actually
  fire given non-verbatim output (or keyed on a stable field), and LLM text rendered to a surface
  must specify its presentation/normalization contract. *Why:* L2 dead predicate + the Slack mrkdwn
  formatting miss.

- **devarm-debug + devarm-review** — a **design-deviation guard** at fix time: a fix (root-cause
  fix or finding remediation) that would *change* an agreed design decision or a locked Decision
  Ledger row — not merely implement it — must STOP and consult the user, superseding the ledger row
  with a ripple-check, before it is applied. *Why:* `devarm-implement` already carried the drift
  rule, but the debug/review fix loops — where this session's design changes actually happened —
  only consulted design at debug's 3-strikes rule and review's reviewer-side ledger screen; neither
  guarded the fix being applied, so the developer had to police design drift by hand.

## 2026-07-23 — implementation-decision brainstorm + design anchoring (Tech Catalyst learnings)

Tech Catalyst sessions surfaced two recurring failures. (1) Even with grounding, implementation
decisions still arrived piecemeal *during* coding; question fatigue made the developer "go with
the flow", which is acceptable for mechanical choices but let control-flow and design changes
through unexamined — those needed a dedicated implementation brainstorm before coding, not
one-at-a-time questions mid-task. (2) Long or resumed coding sessions anchored to
current-session context and quietly skipped designs approved in earlier sessions — nothing
forced the agent to reload the approved design doc before writing code.

| Change | Rationale |
|--------|-----------|
| Added Pass 3 to `devarm-analyze`: an interactive implementation-decision brainstorm — control-flow walkthrough of the flagship + failure paths with the user, then ONE batch of all remaining decisions (assumed/undecided ledger rows, visible trade-offs, walkthrough forks), each with a recommendation | Pulls implementation-time decisions into one pre-coding sitting; the target is that `devarm-implement` asks near-zero questions |
| Extended the analyze gate: no handoff to implement until Pass 3 flows are confirmed, the batch is answered, and no ledger row is left `assumed — awaiting confirmation` | Makes the brainstorm a hard gate, not advisory prose |
| Added a design-anchor precondition to `devarm-implement`: before task 1 and on every session resume, locate the governing design doc + ledger and play back its binding constraints; the written design governs over session memory | Stops earlier-session designs being silently displaced by current-session context (the vibe-coding drift) |
| Added a batching rule to `devarm-implement` decision ownership: mid-flow trade-offs proceed on the recommendation and are presented together at the next checkpoint for veto; only design-level surprises interrupt immediately; a foreseeable trade-off surfacing mid-task is logged as a Pass-3 miss for `devarm-retro` | Question fatigue is a drift vector — batching keeps the developer's attention for the decisions that change intent |
| Paired updates: `AGENTS.md` pipeline table + analyze bullet + decision-ownership section, `README.md` pipeline table + owning-decisions section, `USER_GUIDE.md` flow table + quick-track note, structurizr analyze component + `AnalyzeGateFlow` | Skill files are runtime contracts; the routing surfaces must describe the same method |
| Quick track gains a scoped analyze equivalent (touched seams re-verified + mini Pass 3 decision batch inside the quick-track doc); `devarm-implement` precondition 1 accepts it; the never-skip list now includes the pre-implementation decision batch | A findgap review of this change found the quick track ("go to implement") directly contradicting implement's hardened analyze precondition |
| Pass 3 scoped re-run rule: after course corrections/drift/fix batches, re-walk only touched flows and decisions — confirmed ones stand; batch presentation lists `owner: user` design-level items first under their own heading | A full re-walk each re-gate would recreate the question fatigue Pass 3 removes; a batch "yes" must never bury an intent-level decision |
| Fixed phase-number drift: `devarm-retro` frontmatter 9→10, `devarm-finish` 10→9 (both were swapped vs the pipeline tables), README "Retro (step 8)"→step 10 | Frontmatter is a runtime contract; retro was simultaneously numbered 8, 9, and 10 across surfaces |

## 2026-07-23 — spec 022 repo-ownership-confirm retro

Motivated by the spec 022 session (DEV-319678 postmortem → brainstorm → implement → findgap →
challenge → fix → branch commit). Pure routing modules were stable; the long tail was **seam
binding**, **render-path consumer gaps**, **local `.env` test pollution**, and **findgap
overreach** before a challenge pass.

Six existing gates tightened (no new skills):

- **devarm-ground** — category #3 (consumer audit) gained a **render-path variant**: operator-
  facing fields must name the render function and confirm copy is shown, not only that a dict
  exists on `final_output`. *Why:* `partial_findings` was populated but Jira/Slack sections
  omitted key fields until a follow-up fix; dict-level tests passed SC-002 but not SC-005 message
  structure.

- **devarm-plan** — seam contract now requires **shared mutable context sync** (which objects
  share the same `gathered_info` reference) and **integration-test patch target** (patch where
  the workflow imports, not only the defining module). *Why:* spec 022 bugs in confirm binding
  alias drift and integration mocks patching the wrong import path.

- **devarm-tasks** — decision→test traceability now requires **rendered message assertions** when
  the deliverable is operator-visible escalation/notification copy. *Why:* complements the
  render-path audit with an enforceable acceptance test.

- **devarm-implement** — precondition: **feature branch before task 1** (do not accumulate on
  `main`). *Why:* entire 022 feature was uncommitted on `main` until finish.

- **devarm-finish** — Step 1 adds **env bleed sanity check** and explicit reporting when optional
  deps exclude part of the suite. *Why:* finish blocked on unrelated `PR_CREATION_DRY_RUN` /
  Guru `.env` values and optional `tree_sitter` dep.

- **devarm-review** — **Challenge before fix-all** for HIGH/Should-fix batches (especially after
  `/findgap`). *Why:* challenge pass downgraded several findgap HIGH items to defer/by-design,
  preventing a wasted fix cycle.

## 2026-07-17 — spec 017 diagnosis-gap-repair retro

Motivated by the spec 017 (diagnosis-gap-repair) development session, whose long tail was
repeated `/findgap` → fix cycles. The pure modules (`review_route_back`, policy, dispatch,
gate) were largely correct first time; almost every correctness bug lived in the **integration
seams and downstream consumers** — especially the `ActionResult → RemediationOutput → worker →
notification` data contract for US6 partial-publish.

Three existing gates tightened (no new skills added):

- **devarm-implement** — Verify step + verification table now require mirroring the CI gate
  commands (e.g. `mypy .`, `ruff check .`); IDE/editor diagnostics (ReadLints) are explicitly
  NOT a substitute. *Why:* 5 `mypy` errors survived the implement loop (which ran pytest + ruff
  + IDE lints but never `mypy .`) and were only caught by a separate review — a CI gate existed
  but the loop didn't mirror it.

- **devarm-ground** — decision category #3 (persistence + consumer audit) gained a
  "new-producer variant": the audit also fires when new code starts *producing* an existing
  cross-layer/persisted field, and must confirm the new producer honors invariants existing
  consumers assume. *Why:* US6's route-back began writing `multi_repo_partial`/`prs`, silently
  breaking invariants the worker (dropped URL-less PR rows) and `_notify_success` (claimed full
  success) already assumed.

- **devarm-tasks** — decision→test traceability now requires a **negative** acceptance test for
  any safety invariant ("never/always"), not just a happy-path test. *Why:* design §10.4 ("never
  `success:true` while no PR published") had a task (T040) that asserted only the publish-happy
  path, so the first US6 build shipped a false "partial success" with no PR.

## 2026-07-16 — runtime prompt/skill/contract artifacts as first-class gated surfaces

A review-driven session on the tech-catalyst repo fixed skills/prompts-accuracy findings, then a
self-initiated review caught two of its own defects: (1) a new prompt directive gated on
`len(repository_candidates) < 2` was correct on the single-repo primary path but contradicted the
authoritative Shared-Cross-Repository-Plan block on the pinned expansion pass (candidates are
narrowed to one there) — a self-contradicting prompt that would have shipped into the multi-repo
flow; and (2) three separate wording drifts between skill/contract text and runtime truth (a
"investigate next" vs "fix next" collision, an invalid `contract_mismatch` enum, an imprecise
`0.85`/id-format guidance). A compaction summary also *claimed* lock tests that did not exist. Root
cause: runtime prompt/skill/contract files describe runtime behavior but were gated more weakly
than code modules.

| Change | Rationale |
|--------|-----------|
| Expanded `devarm-ground` decision category #10 (Runtime contract surfaces) from pairing-only to three sub-checks: (a) pairing, (b) **value grounding** — every stated enum/threshold/constant cited to its source `file:line`, (c) **directive context sweep** — every runtime-gated prompt directive confirmed across every prompt-building context | Kills the wording-drift class (D3/D4/D5) and the context-contradiction class (B2) at design time |
| Updated the `devarm-ground` Step-5 approval checklist to require value-grounding and the directive context sweep | Makes the new sub-checks a hard gate, not advisory prose |
| Extended `devarm-tasks` decision→test traceability: a decision whose deliverable is prompt/skill/contract **wording** requires a **wording-lock test** asserting the exact string/value | The fix the session used ad hoc becomes standard; also makes "done" verifiable against the repo instead of a summary |
| Added a `devarm-review` architecture-lens **runtime prompt/directive sweep** bullet | Second line of defense before merge for the context-contradiction class |
| Extended the `devarm-review` QA-lens verification-evidence bullet to re-derive "done" from the repo, never from a session summary or implementer claim | Addresses the compaction-summary false-completion near-miss |

## 2026-07-15 — explicit developer confirmation for git commits

The implementation and retro skills still encouraged commits as an automatic phase/task outcome.
That conflicts with developer ownership of repository history: no agent should create commits
unless the developer explicitly asks for them.

| Change | Rationale |
|--------|-----------|
| Added a global git commit policy to `AGENTS.md`: never run `git commit` without explicit developer confirmation in the current context | Task completion, phase completion, and end-to-end mode are not commit permission |
| Reworked `devarm-implement` from automatic/frequent commits to commit-ready checkpoints with changed files, verification evidence, and suggested commit messages | Preserves auditability without taking control of history |
| Reworked `devarm-plan` task language and `devarm-retro` output so they propose commit boundaries/summaries instead of creating commits | Plans and retros now align with the confirmation rule |
| Updated README, USER_GUIDE, and findings ledger wording from required commits to commit-or-diff evidence | Verification remains evidence-based even when the developer keeps changes uncommitted |

## 2026-07-14 — narrower devarm invocation policy

The trigger language said "ANY creative work", which caused devarm to fire in chats where the
user wanted a diagram, explanation, or lightweight documentation help. That made the method feel
invasive instead of deliberate.

| Change | Rationale |
|--------|-----------|
| Added an invocation policy to `AGENTS.md`: use devarm when explicitly requested or for consequential code/product work; do not use it for ordinary Q&A, repo exploration, summaries, simple docs, diagrams, or visualizations | The method should protect important implementation decisions, not wrap every helpful interaction |
| Narrowed `devarm-brainstorm`'s description and hard gate from "ANY creative work" to consequential code/product changes plus explicit user request | Skill discovery now has a less trigger-happy contract |
| Updated `README.md` and `USER_GUIDE.md` with when not to invoke devarm | Developers and agents both get the same operating expectation |

## 2026-07-14 — default phase-by-phase execution

The first user-guide pass made manual phase invocation possible, but the runtime skill contracts
still said to invoke the next phase automatically (`spec → plan → tasks → analyze`). That made
"manual gates" look like an exception instead of the default operating model.

| Change | Rationale |
|--------|-----------|
| Added a global phase transition policy to `AGENTS.md`: halt after each phase gate, report the artifact/result, and ask what to run next unless the user explicitly requested end-to-end execution | The developer controls cadence; silence is not permission to continue into the next phase |
| Updated `devarm-brainstorm`, `devarm-spec`, `devarm-plan`, `devarm-tasks`, and `devarm-analyze` handoffs to stop-and-ask by default | The behavior now lives in the runtime contracts, not just the user guide |
| Documented explicit end-to-end mode in `README.md` and `USER_GUIDE.md`, while preserving stops for user approvals, design-level decisions, unresolved assumptions, failed verification, and failed analyze gates | End-to-end is opt-in and cannot bypass load-bearing gates |

## 2026-07-14 — back-and-forth protocol for brainstorming/design

devarm channeled iteration (fork-following, per-section approval, ground bounce-backs, ledger
rows) but had no protocol for the two churn patterns that actually hurt in the spec-016
session: reopening a settled decision (cap semantics — 4 post-design exchanges, design
rewritten twice) and resuming after a gap (Jul 10 → 13, landed code had invalidated design
assumptions).

| Change | Rationale |
|--------|-----------|
| Brainstorm back-and-forth protocol: open-vs-settled distinction; supersede + **ripple-check** for reopened decisions; classify mid-design arrivals (new fork vs scope change); resume-after-gap steps (status line → repo diff vs grounded evidence → play back state, never re-ask the ledger); post-approval changes go through superseding rows / course-correction | Every loop must end in an updated artifact, not a drifting conversation |
| Ledger rule: supersede-don't-edit with `superseded (→ D<new>)` back-reference; dependent rows/sections re-confirmed | A reopened decision that skips the ripple check is how designs go internally inconsistent |

## 2026-07-14 — adopt from BMad Method (v6)

Reviewed BMad v6 (no local install — reviewed via its docs: 4-phase model, scale-adaptive
tracks, 12 agent personas, story-by-story implementation loop, party mode, web bundles).
BMad's persona layer duplicates what devarm's review lenses already do, but three ideas were
genuinely missing:

| Change | Source / rationale |
|--------|--------------------|
| Scale gate in brainstorm (quick vs standard track): bug-fix/single-story work collapses spec/plan/analyze into one short doc; gates (grounding, approval, TDD, verification) never collapse; auto-upgrade to standard when quick work reveals persistence/contract/blast-radius growth | BMad's scale-adaptive levels 0-4 / quick-spec track — devarm previously ran full ceremony on everything, which invites skipping the method for small work |
| Course-correction protocol in implement: mid-stream scope change → list affected requirements/ledger rows/tasks, update artifacts, scoped re-analyze, explicit rework tasks | BMad's `correct-course` workflow — devarm's drift rule covered code-vs-plan conflicts but not requirements changing underneath the work |
| Pipeline status line + last-session note in the design-doc header, updated at every gate | BMad's `workflow-status` / sprint-status tracking — devarm had no durable "where are we" marker, so a fresh session (or tool switch) had to reconstruct state from artifacts |

Not adopted: agent personas incl. party mode (devarm's review already applies the useful
lenses — architecture + QA — without persona ceremony; personas add role-play overhead, not
gates); PRD/product-brief artifact layer (devarm's design doc + spec cover it for solo work);
JIT per-epic tech-specs (devarm-analyze re-verifies against current code, which addresses the
same staleness problem); web bundles (tool-specific packaging).

## 2026-07-14 — adopt from spec-kit (speckit)

Reviewed all 14 speckit skills, its templates, scripts, and extension machinery. devarm's
pipeline was already modeled on speckit's (specify→plan→tasks→analyze→implement) and reuses
`.specify/` templates when present; adopted the concepts that survive outside that machinery:

| Change | Source / rationale |
|--------|--------------------|
| Spec: prioritized, independently-testable user stories (P1/P2/…, named Independent Test, Given/When/Then scenarios, P1 = viable MVP) | speckit spec-template — this structure is what made spec-016's tasks organizable story-by-story with a stoppable MVP slice |
| Spec: explicit scenario-class sweep (primary / alternate / exception / recovery / non-functional), absent classes marked excluded rather than silent | speckit-clarify taxonomy + checklist scenario classification |
| Spec quality gate reframed as "unit tests for English" — checks test the WRITTEN requirements (completeness/clarity/consistency/measurability/coverage), with optional domain checklist for risky areas | speckit-checklist's core concept, condensed from 367 lines to a paragraph |
| Brainstorm: recommendation-first question format ("Recommended: X — reason; reply 'yes' to accept") + impact×uncertainty prioritization of remaining questions | speckit-clarify's questioning loop — cheap accepts and never spending low-impact questions while high-impact areas are open |
| Brainstorm coverage map: non-functional qualities + integration/external-dependency areas | speckit-clarify's taxonomy had these two categories the map lacked |

Not adopted: hooks/extensions.yml machinery and check-prerequisites scripts (speckit plumbing —
devarm skills coordinate through phase gates directly); `## Clarifications` session log in the spec (the Decision
Ledger is devarm's single home for decisions; a second Q→A log would split the record);
speckit-taskstoissues (YAGNI for a solo workflow — revisit if working with a team);
feature-numbering git scripts (reused via `.specify/` when present).

## 2026-07-14 — Question Coverage Map in brainstorm

"Ask clarifying questions" said HOW to ask (one at a time, multiple choice) but not WHAT must
be covered — so question coverage depended on where the dialogue happened to wander. In the
spec-016 session the brainstorm asked 6 good questions yet never elicited cap semantics or the
communication surface; both surfaced post-design.

| Change | Rationale |
|--------|-----------|
| 8-area Question Coverage Map (purpose, scope+flagship, behavior semantics incl. failure/partial/pause, limits & config with the four sub-answers, compatibility, communication surface, success criteria, trade-off preferences) | Questions are complete when the map is covered, not when the conversation feels done |
| Follow-the-fork rule: restate what an answer decided, ask the question it opened | User answers often contain 2-3 embedded decisions; interpreting them silently is how decisions get made without the user |
| Stop condition: all areas answered/N/A AND last answer opened no new fork; skipped questions carried as `assumed — awaiting confirmation` | Aligns brainstorm questioning with the ledger's no-silent-approval rule |

## 2026-07-14 — deep-dive on superpowers brainstorming + TDD

Line-by-line comparison of the two most important superpowers skills against devarm:

| Change | Rationale |
|--------|-----------|
| New `devarm-tdd` (core discipline, consumed by implement + debug) | devarm-implement's 3-line red/green/refactor lost the parts that make TDD hold under pressure: the **delete rule** (code before test is deleted, not "kept as reference"), **RED must FAIL not error** / test-passes-immediately means it tests nothing, test-quality rules (one behavior, spec-like names, real code over mocks), the when-stuck table (hard to test = design problem), mock/test-only-method anti-patterns, and the rationalization red-flags |
| `devarm-implement` execution loop delegates to `devarm-tdd`; `devarm-debug` Phase-4 repro test cites it | One home for the discipline instead of two paraphrases |
| `devarm-brainstorm`: targeted-improvement rule for existing codebases | From superpowers brainstorming — fix existing problems that directly affect the work as part of the design; never bundle unrelated refactoring |

Checked and already covered by devarm-brainstorm (no change): hard gate, "too simple to need
a design" anti-pattern, scope-check/decomposition, one-question-at-a-time, 2-3 approaches,
sectioned presentation, spec self-review checklist, written-spec user gate, single terminal
hand-off. Not adopted: the browser "visual companion" (tool-specific, token-heavy).

## 2026-07-14 — adopt from the superpowers plugin

Reviewed all 14 superpowers skills. Brainstorming/TDD/plan-writing/verification were already
absorbed into devarm's phases; adopted the pieces devarm lacked, condensed:

| Change | Source / rationale |
|--------|--------------------|
| New `devarm-debug` (on-demand, any phase): 4-phase root-cause-first debugging, no fix-stacking, 3-failed-fixes → question the architecture, parallel subagents for independent failures | `systematic-debugging` + `dispatching-parallel-agents`. devarm had NO debugging discipline — fix loops were its weakest phase |
| New `devarm-finish` (phase 9): fresh full-suite verification, then exactly four options (merge / PR / keep / discard), typed confirm to discard, worktree cleanup | `finishing-a-development-branch`. devarm previously ended at review with no integration protocol |
| Implement: verification claim→evidence table ("fresh run in THIS turn"; subagent report ≠ evidence; red-green for regression tests) | `verification-before-completion` — the table format makes "what proves this claim" explicit |
| Implement: subagent protocol — full task text in prompt (never "read the plan"), two-stage review (spec compliance THEN quality), model sized to task, BLOCKED/NEEDS_CONTEXT handling, never retry unchanged | `subagent-driven-development` — devarm's subagent mode was one sentence |
| Implement: optional worktree isolation (ignored dir + green baseline before task 1) | `using-git-worktrees`, trimmed to the two safety rules that matter |
| Review: receiving-feedback discipline — no performative agreement, clarify ALL items before implementing ANY, YAGNI-check reviewer suggestions, push back technically, correct pushback factually | `receiving-code-review` — complements the findings ledger with response behavior |

Not adopted: `using-superpowers` (meta-dispatch — the skills' own descriptions handle
discovery), `writing-skills` TDD-for-docs (interesting; revisit if retro edits start missing),
`executing-plans` (parallel-session variant of implement — YAGNI for a solo workflow).

## 2026-07-14 — adopt code-quality standards from tech-catalyst-v2 rules

Ported the transferable core of the project's `.cursor/rules/` code-quality set
(`design-patterns`, `architecture-boundaries`, `backend-conventions`, `frontend-conventions`)
into the kit as `templates/code-standards.md`, stripped of repo-specific paths so it works in
any stack:

| Change | Rationale |
|--------|-----------|
| New `templates/code-standards.md` — prefer/avoid pattern catalog with mandatory BAD/GOOD pairs | The tech-catalyst rules proved that pattern rules only bite when each carries a concrete counter-example |
| Constitution VIII: design patterns & anti-patterns | Makes the catalog a checked principle, not an optional doc |
| `devarm-ground` inputs now include the project's pattern catalog (fallback: code-standards) | Reuse legality and pattern conformance are checked at the same grounding read |
| `devarm-review` architecture lens gains a patterns/anti-patterns check (fat controller, inline queries, leaky ORM, buried commits, view-local fetching, suppression creep) | The review lens previously checked boundaries/duplication but not pattern conformance |

Not ported (stays project-side): repo-specific layering paths, named god-files, stack-specific
rules (React Query, pydantic-settings) — devarm supplies the method, the project supplies those.

## 2026-07-14 — final devarm2 delta port (devarm becomes the single active kit)

Side-by-side review confirmed devarm ⊇ devarm2 except two findings-ledger details, now ported:

| Change | Rationale |
|--------|-----------|
| Findings ledger gains a **Source** column | Multiple review passes/sessions append to one file; rows must say where a claim came from without re-feeding transcripts. |
| Strict status semantics: `fixed` requires verification output + commit/diff evidence; `deferred` requires a tracked task id | "Fixed" without seen verification and "deferred" without a task are how findings silently rot. |

devarm2 is superseded and can be discarded.

## 2026-07-14 — merge best-of from devarm2

Reviewed the parallel `devarm2` build (same source retro) and adopted what it did better:

| Change | Rationale |
|--------|-----------|
| New `devarm-analyze` gate (phase 6, between tasks and implement) | Artifact self-consistency ≠ artifact-vs-code truth; the repo can move after grounding. Adds a flagship end-to-end paper-trace — the check that catches "a gate on the path rejects the headline use case" (the US1 near-miss). |
| `devarm-ground` consolidated to **ten** numbered decision categories | Config semantics (#9) and runtime-contract surfaces (#10) were scattered notes; folding them into the numbered list makes them un-skippable. |
| Decision Ledger gains an **Enforcing test** column + "re-surface assumed rows at every gate" | Tightens decision→test traceability and the no-silent-approval rule. |
| Added this `CHANGELOG.md` | The audit trail of why the method is shaped the way it is. |
| Crisper principle one-liners in `AGENTS.md`; anti-patterns in `devarm-retro` | "A number is not a decision", "exists ≠ wired", "prose rules get rationalized away → gates with numbers"; retro must end as a diff, not a doc. |

## 2026-07-14 — founding (retro of the multi-repo fix generation session)

Source: retrospective of the spec-016 multi-repo session (Jul 10–14, tech-catalyst-v2; brainstorm
→ design → speckit → implement → 6+ review/fix loops; ~60% of wall-clock in the post-implementation
fix tail). Each gate below exists because of a specific failure in that session.

| Gate added | Motivating failure |
|------------|--------------------|
| Ground: reuse requires shape check (sync/async, statefulness, wired-vs-dead) | Design claimed "reuse MultiRepoDecisionService"; it was async, per-request, in-memory, unwired; flip-flopped 3× and was finally deleted (~760 lines) |
| Ground category 9: config/limit semantics | "Cap = 2" locked as a number; semantics (PR-only vs diagnosis, configurability, overflow) resolved in 4 post-design exchanges; design rewritten twice |
| Ground category 3: consumer audit for changed data shapes | New `ticket_pull_requests` table shipped while PR-sync loop, list API, and dashboard still read the old scalar → P0 sync gap found only in external review |
| Ground category 10: runtime contract surfaces | Synthesis SKILL.md taught `next_repo` while the injected contract demanded `cross_repo_targets[]` — conflicting model guidance; initially misclassified as "docs only" |
| Tasks: decision → enforcing-test traceability | "Intake-once" and "single consolidated comment" were explicit decisions, violated by the first implementation, caught only by findgap |
| Plan: integration seams get contracts / spike tasks | Nearly every post-implementation bug lived in seams left as "confirm during coding" |
| Implement: mid-implementation decision taxonomy + no-silent-approval | Per-app cap-override question went unanswered and was silently resolved as YAGNI; the gate dropped a designed component without asking |
| Implement: phase-boundary commits + high-coupling checkpoints | ~6h uncommitted → duplicate "fix the issues found" loops, no bisectable history; god-file grew +563 lines despite a known rule |
| Review: single findings ledger, evidence-based verdicts both ways, fixed/awaiting split | Three external review transcripts re-fed and re-litigated; two duplicate fix requests for already-applied fixes |
| AGENTS.md: one planning system per feature; one feature per thread | Superpowers plan + speckit artifacts drifted (MR-### vs FR-###); 009 brainstorm started at the tail of a 1,000-message thread |
