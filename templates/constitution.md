# Project Constitution (devarm starter)

A short, enforceable set of principles every devarm phase checks against. Copy into a target
project (e.g. `.specify/memory/constitution.md` or a `.cursor/rules/` file) and adapt. If the
project already has one, THAT wins — devarm supplies the method, the project supplies the rules.

## I. Single responsibility & cohesion
- One module = one reason to change. Many small, well-named units over one multi-purpose file.

## II. File-size budgets (guardrails)
- Set explicit budgets per language (e.g. Python module < 500 lines; UI component < 300 lines).
- Maintain a list of known god-files: do not grow them; extract when touched.

## III. Dependency direction
- Define the allowed import direction (e.g. `routes → workflows → services → repositories → db`).
- Never import "upward". No circular imports.

## IV. No half-finished refactors
- When you add a new way, remove the old way in the same change. One home per concept
  (enum, status, type, constant). No orphaned or "staged for later" modules.

## V. Testing standards
- TDD: failing test before implementation. Integration tests where behavior crosses boundaries.

## VI. Verification before completion
- No "done"/"fixed"/"passing" claim without command output confirming it.

## VII. Own the decisions
- Every load-bearing choice is recorded in the Decision Ledger with evidence and an owner,
  before implementation.

## VIII. Design patterns & anti-patterns
- Follow the project's pattern catalog (repository for persistence, DTOs at boundaries,
  composition over inheritance, caller-owns-transaction, one settings home, one source of
  truth per type). If the project has none, use `devarm/templates/code-standards.md`.
- Every pattern rule carries a BAD/GOOD example pair so violations are recognizable in review.
