# Code Standards (devarm starter)

A portable catalog of patterns to prefer and anti-patterns to reject, checked by
`devarm-ground` (reuse legality), `devarm-implement` (while coding), and `devarm-review`
(architecture lens). Copy into a target project (e.g. `.cursor/rules/design-patterns.mdc` or
`AGENTS.md`) and adapt to its stack. If the project already has its own standards, THOSE win.

**Convention: every rule ships a BAD/GOOD pair.** A rule without a concrete counter-example
gets rationalized away; the pair makes violations recognizable at review time.

## Prefer

- **Repository/Store for persistence** — DB access lives behind a repository that takes the
  session/connection. Business code never builds queries inline.
- **Ports & Adapters for orchestration** — each phase/step exposes a small interface; the
  orchestrator wires phases, it does not embed their internals.
- **Composition over inheritance** — build behavior from small pieces, not deep hierarchies.
- **DTOs at boundaries** — convert persistence entities to typed DTOs before they cross the
  API/serialization boundary.
- **Dependency injection** — pass sessions/clients/services in; avoid module-level singletons.
- **Caller owns the transaction** — repositories/services `flush()`; the outermost caller
  (route/worker/workflow) commits exactly once. No commits buried in helpers.
- **One settings home** — config lives in one typed settings module read via one accessor;
  no `os.getenv`/`process.env` scattered through modules.
- **One source of truth for types** — a domain type has exactly one declaration; extend it,
  never shadow it with a local near-copy.
- **Push aggregation to the datastore** — `SUM`/`GROUP BY` in SQL, not loops over fetched rows.

## Avoid (anti-patterns)

- **God object / god orchestrator** — one class or file that imports everything and does every
  phase. Split by responsibility; god-files get hard line budgets (see constitution II).
- **Fat controller** — route/page handlers that orchestrate + query + serialize inline. Keep
  handlers thin; delegate to services/hooks.
- **Anemic or leaky model** — business logic embedded in ORM models, or ORM objects returned
  raw to callers. Persistence and domain concerns stay separate.
- **Mixed persistence styles** — don't add a new `*Store` beside an existing `*Repository`
  (or vice versa) for the same layer; pick the established convention.
- **View-local data fetching** — UI views calling the backend directly instead of the
  project's data layer (query hooks / services).
- **Suppression creep** — no new `any`/`@ts-ignore`/`# type: ignore`/lint-disable without a
  recorded reason; fixing the type is the default.

## Example pair format

```python
# BAD: query built inside a service
rows = (await session.execute(select(Job).where(...))).scalars().all()
# GOOD: go through the repository
rows = await job_repo.list_active()
```

```ts
// BAD: page-local fetching
useEffect(() => { apiClient.get('/errors').then(setErrors); }, []);
// GOOD: typed query hook from the data layer
const { data: errors } = useErrors();
```
