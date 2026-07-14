---
name: "devarm-brainstorm"
description: "Use before ANY creative work — new feature, component, behavior change, or non-trivial refactor. Turns an idea into an approved, code-grounded design through collaborative dialogue: explore context, ask one question at a time, propose 2-3 approaches, present the design in scaled sections, then run devarm-ground BEFORE approval. Terminal state hands to devarm-spec. Do not write code until the design is grounded and approved."
metadata:
  phase: 1
  produces: "docs/design/YYYY-MM-DD-<topic>-design.md (draft)"
  next: "devarm-ground (before approval), then devarm-spec"
---

## Announce

"I'm using devarm-brainstorm to turn this idea into a grounded, approved design."

## Hard gate

Do NOT write code, scaffold, or invoke any implementation skill until a design has been
presented, **grounded** (devarm-ground), and approved by the user. This applies to every
project regardless of perceived simplicity — "too simple to design" is where unexamined
assumptions cause the most wasted work.

## Checklist (create a task per item, complete in order)

1. **Explore project context.** Read the relevant files, docs, and recent commits. In an
   existing codebase, learn the current patterns before proposing changes.
2. **Scope check.** If the idea spans multiple independent subsystems, stop and help decompose
   it into sub-projects first — each gets its own design → spec → plan → implement cycle. Don't
   refine details of something that should be split.
3. **Ask clarifying questions — one at a time.** Prefer multiple-choice. Focus on purpose,
   constraints, and success criteria. One question per message; break big topics into several.
4. **Propose 2-3 approaches** with trade-offs. Lead with your recommendation and why.
5. **Present the design in sections** scaled to complexity (a few sentences for simple parts,
   up to ~250 words for nuanced ones). Cover: architecture, components, data flow, error
   handling, testing. Ask after each section whether it looks right. Revise as needed.
6. **Write the draft design doc** to `docs/design/YYYY-MM-DD-<topic>-design.md` (or the target
   repo's configured design location, e.g. `docs/superpowers/specs/`). Use
   `devarm/templates/design-doc.md` as the structure.
7. **Spec self-review** (inline): scan for placeholders/TBDs, internal contradictions, scope
   creep, and requirements that could be read two ways. Fix inline.
8. **Run devarm-ground** on the draft — BEFORE asking for approval. Grounding may send you back
   to revise sections 4-6; that is expected and is the point.
9. **User approval gate.** Only after grounding passes, ask the user to approve the written,
   grounded design. If they request changes, revise and re-ground.
10. **Hand off to devarm-spec.** That is the only skill you invoke next.

## Design for isolation and clarity

Break the system into small units that each have one clear purpose, communicate through
well-defined interfaces, and can be tested independently. For each unit you must be able to
answer: what does it do, how do you use it, what does it depend on? If you can't change a unit's
internals without breaking consumers, the boundaries need work. When a file grows large, that's
a signal it's doing too much.

## Key principles

- One question at a time; multiple choice preferred.
- YAGNI ruthlessly — remove unnecessary features from every design.
- Always explore alternatives before settling.
- Incremental validation — approval per section, not all-at-once.
- Be flexible — go back and clarify when something doesn't fit.
