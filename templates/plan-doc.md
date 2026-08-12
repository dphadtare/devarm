# <Feature> — Implementation Plan

This native fallback is a repository-local artifact. It uses no front matter and no database.
The plan is implementation-ready only when every reuse claim and requirement has a concrete
file, seam, test, and verification path.

## Implementation objective

<Outcome to implement.>

## Scope and requirement coverage

| Specification requirements | Plan coverage |
|---|---|
| FR-001 | T001 |

## File-structure map

| File | Single responsibility | Budget |
|---|---|---:|
| `<path>` | <one responsibility> | <limit> |

## Technical context

<Current code, rules, data shapes, and source-of-truth decisions.>

## Integration seams and contracts

For each seam record call site, input, output, replay/idempotency, failure posture, shared
context, and test target.

## Status transitions

<Include when the change has resumable or multi-actor state.>

## Implementation tasks

Tasks are grouped here for requirement mapping only. `tasks.md` is the sole executable task source.

## Verification

<Exact test, lint, build, and current-evidence commands.>

## Self-review

- [ ] Every requirement maps to a task.
- [ ] Every task has a RED test or characterization check before implementation.
- [ ] No placeholder, unowned decision, or unverified reuse claim remains.
