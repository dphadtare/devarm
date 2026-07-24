# Structurizr diagrams

This folder contains the C4 and sequence-style flow diagrams for the Tech Catalyst / devarm
method kit.

## Files

- `workspace.dsl` - Structurizr DSL source.

## Views

- `SystemContext` - who uses the method kit and which external systems it touches.
- `Containers` - internal parts: instructions, installer, skill catalog, templates, artifacts,
  gates, and changelog.
- `SkillComponents` - the phase skills and their dependencies.
- `StandardPipelineFlow` - idea to shipped code.
- `GroundingFlow` - how draft design decisions are grounded before approval.
- `AnalyzeGateFlow` - how implementation is blocked until artifacts and current code agree and
  remaining implementation decisions are batch-decided.
- `DecisionOwnershipFlow` - how decisions are surfaced, recorded, tested, and protected.
- `ImplementationTddLoop` - the per-task red/green/refactor cycle.
- `DebugLoop` - root-cause-first failure handling.
- `FinishFlow` - fresh verification and branch/PR outcomes.

## Render locally

With Structurizr Lite:

```bash
docker run --rm -it -p 8080:8080 -v "$PWD/docs/diagrams/structurizr:/usr/local/structurizr" structurizr/lite
```

Then open `http://localhost:8080`.

With the Structurizr CLI, from the repo root:

```bash
structurizr validate -workspace docs/diagrams/structurizr/workspace.dsl
structurizr export -workspace docs/diagrams/structurizr/workspace.dsl -format plantuml -output docs/diagrams/structurizr/out
```
