# Common Artifact Metadata

Every devarm phase artifact is repository-local and remains the source of truth for its phase.
Use structured Markdown headings and bold fields; use no front matter and no database.

```text
Document type
Date
Status
Phase
Feature/change
Track
Pipeline
Target repository
Target branch
Last session note
Last verification
Open assumptions / risks
Next gate
Related artifacts
Design or governing artifact link
Rule inventory link
Analysis/findings artifact link
```

Allowed statuses are: `draft`, `awaiting approval`, `in progress`, `blocked`, `partially completed`,
`failed`, and `complete`. A non-`complete` status cannot satisfy a phase handoff.
The phase owns status updates; deterministic validators only report findings.
