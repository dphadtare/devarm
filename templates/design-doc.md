# <Feature Name> — Design

**Document type:** Design spec (devarm-brainstorm output)
**Date:** YYYY-MM-DD
**Status:** Draft — pending grounding (devarm-ground) and user approval

**Builds on / related:** <links to prior designs, specs, or landed work this must respect>

---

## 1. Problem statement

<What problem, for whom, why now. The current behavior and its structural limits.>

## 2. Goals and non-goals

### Goals
| ID | Goal |
|----|------|
| G1 | |

### Non-goals
- <Explicitly out of scope — protects against scope creep.>

## 3. Approach

<The chosen approach in a few sentences.>

**Rejected alternatives:**
- **<Alternative A>** — why rejected.
- **<Alternative B>** — why rejected.

## 4. Architecture

### 4.1 Flow
<Diagram or step list of the end-to-end flow.>

### 4.2 Components
| Component | Location | Responsibility |
|-----------|----------|----------------|

### 4.3 Data
<Entities, shapes, persistence. Where state lives.>

## 5. Error handling & completion semantics

<Per failure mode: raise / retry / degrade / pause / escalate. The safe fallback.>

## 6. Testing

<Unit / integration / regression strategy. What each level proves.>

## 7. Open items

<Anything deferred to spec/plan. Resolve or mark clearly.>

---

<!-- The two sections below are filled by devarm-ground BEFORE approval. -->

## Detailed Design (grounded)

<Per touched area, the resolved implementation-decision categories, each backed by file:line:
layer/boundary legality, idempotency/replay, persistence shape, canonical identity, exact seams,
determinism, back-compat, failure posture. Mark N/A where a category doesn't apply.>

## Decision Ledger

See `devarm/templates/decision-ledger.md` for the tier/owner rules.

| # | Decision | Alternatives rejected | Evidence (file:line / rule) | Owner | Tier | Status |
|---|----------|-----------------------|------------------------------|-------|------|--------|
| D1 | | | | user | design | approved |
