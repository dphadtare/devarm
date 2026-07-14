---
name: "devarm-tdd"
description: "The test-driven development discipline used by devarm-implement (every task) and devarm-debug (every fix). Use whenever writing production code or fixing a bug, before the implementation code exists. Enforces the failing-test-first law with the delete rule, RED/GREEN verification specifics, test-quality rules, and defenses against the standard rationalizations."
metadata:
  phase: "core discipline (used by implement and debug)"
  produces: "behavior locked by a test that was seen to fail first"
  next: "return to the calling skill"
---

## The Iron Law

> NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

Wrote code before the test? **Delete it and start over.** Not "keep as reference", not "adapt
it while writing tests" — you'll bias the tests to what you built. Delete means delete;
implement fresh from the tests. (Sunk cost is not a reason: keeping unverified code is debt.)

Exceptions (throwaway prototypes, generated code, pure config) require the user's explicit OK.

## RED — write one failing test, and WATCH it fail

- One behavior per test, named as a specification (`retries failed operations 3 times`, not
  `test1`; an "and" in the name means split it).
- Test real code; mock only what is unavoidable (external boundaries).
- **Run it. Confirm it FAILS — not errors.** An error (typo, missing import) is not a failing
  test; fix and re-run until it fails for the expected reason: the behavior is missing.
- **Test passes immediately?** It's testing existing behavior or nothing — fix the test, not
  your confidence.

## GREEN — minimal code, and watch it pass

Simplest code that passes. No extra options, flags, or generality the test didn't demand
(YAGNI). Run it: this test passes, the rest of the suite stays green, output pristine (no new
warnings). Fails? Fix the code, never loosen the test.

## REFACTOR — only on green

Remove duplication, improve names, extract helpers. No new behavior. Suite stays green.

## Why order matters (the one-line version)

Tests written after answer "what does this code do?"; tests written first answer "what SHOULD
it do?" — and only a test you watched fail is proven to test anything.

## When stuck

| Problem | It means |
|---------|----------|
| Don't know how to test it | Write the wished-for API and the assertion first; ask the user if still stuck |
| Test is too complicated | The design is too complicated — simplify the interface |
| Must mock everything | The code is too coupled — inject dependencies |
| Test setup is huge | Extract helpers; still huge? simplify the design |

## Anti-patterns

- Asserting on the mock instead of the behavior (you tested the mock).
- Test-only methods or hooks added to production classes.
- Bug fixed without a reproducing test first (see `devarm-debug` — the failing repro test IS
  Phase 4 step 1).

## Red flags — stop and restart with TDD

"Too simple to test" · "I'll test after" · "already manually tested it" · "keep it as
reference" · "tests-after achieve the same goals" · "it's about spirit not ritual" ·
"deleting X hours is wasteful" · a test you can't explain the failure of · "just this once".
