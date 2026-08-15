---
name: "devarm-debug"
description: "Use for ANY bug, test failure, or unexpected behavior, BEFORE proposing fixes — including mid-implement and during review/fix loops. Enforces root-cause-first debugging in four phases (investigate, pattern-match, hypothesize, fix), forbids symptom patches and fix-stacking, and escalates to an architecture question after 3 failed fixes. On-demand: not a pipeline phase; invoke whenever something breaks."
metadata:
  phase: "on-demand"
  produces: "root-cause diagnosis + a failing test + a single verified fix"
  next: "return to whatever phase you were in"
---

## The Iron Law

> NO FIXES WITHOUT ROOT-CAUSE INVESTIGATION FIRST. A symptom fix is a failure.

Applies to every technical issue — test failures, production bugs, build breaks, flaky
behavior. ESPECIALLY under time pressure: systematic is faster than guess-and-check thrashing.

## Announce

"I'm using devarm-debug to find the root cause before touching a fix."

## Phase 1 — Root-cause investigation (before ANY fix)

1. **Read the error completely** — full stack trace, line numbers, exit codes. The answer is
   often in text you were about to skip.
2. **Reproduce reliably** — exact steps; if not reproducible, gather more data, don't guess.
3. **Check what changed** — `git diff`, recent commits, deps, config, environment.
4. **Multi-component systems: instrument the boundaries** — log what enters/exits each layer,
   run once, and let the evidence show WHICH layer breaks before investigating it.
5. **Trace bad values backward** — to where they originate; fix at the source, not where the
   error surfaced.

## Phase 2 — Pattern analysis

Find working examples of the same pattern in this codebase; read reference implementations
completely (not skimmed); list EVERY difference between working and broken — don't assume
"that can't matter".

## Phase 3 — Hypothesis, minimally tested

State one specific hypothesis ("X is the root cause because Y"). Test it with the SMALLEST
possible change — one variable at a time. Wrong? Form a new hypothesis; do NOT stack another
fix on top. If you don't understand something, say so instead of pretending.

## Phase 4 — Fix

1. Write the failing test that reproduces it — before the fix (per `devarm-tdd`; confirm it
   fails for the bug's reason, not an error). Never fix a bug without a reproducing test.
2. One fix, addressing the root cause. No "while I'm here" refactoring.
3. Verify: the test passes, the suite is green, the original symptom is gone.

## Shared-helper bugs: fix the class, enumerate all call sites first

When the root cause is a **shared helper's behavior** (a filter, sanitizer, scope/allowlist
function, serializer), `grep` for **every** call site BEFORE the first fix and fix it at the source.
Patching only the call site the symptom surfaced at leaves the same bug latent at the others — and
if the feedback loop is a slow live E2E, each missed site costs another full cycle. This is
fix-stacking spread across runs; the 3-strikes tell ("each fix reveals the same problem elsewhere")
applies here too. *Failure-class rationale (a prior failure): `sanitize_publish_paths` dropped deletions at 4 call
sites; fixed one-per-live-run (L1→L1b→L1c) = 3 expensive cycles, when one
`git grep sanitize_publish_paths` at strike 1 would have shown all 4 and pointed the fix at the
shared function itself.*

## The 3-strikes architecture rule

If **3 fixes have failed**, STOP. This is no longer a bug — it's a wrong pattern/architecture
(each fix revealing a new problem elsewhere is the tell). Question the design with the user
(this is a design-level decision — ledger row) instead of attempting fix #4.

## Independent failures → parallel subagents

If multiple failures are genuinely independent (different subsystems, no shared state),
dispatch one focused subagent per problem domain — each with a specific scope, pasted error
text, constraints ("do NOT just raise timeouts"), and a required summary. Verify their fixes
together against the full suite. Related failures are investigated together, not split.

## Red flags — stop and return to Phase 1

"Quick fix for now, investigate later" · "just try X and see" · multiple changes at once ·
"it's probably X" · proposing fixes before tracing data flow · "one more attempt" after 2+
failures. Simple bugs have root causes too, and emergencies don't exempt you.
