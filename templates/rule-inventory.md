# Repository Rule Inventory

The rule inventory is a repository-local record of the instructions that govern a change. It
uses no front matter and no database. The target-repository rule wins over a devarm default; a
material conflict is visible in the final column and is not silently resolved.

| ID | Source | Scope | Applies | Precedence | Enforcement phase | Evidence | Conflict/disposition |
|---|---|---|---|---|---|---|---|
| R1 | `<path>` | `<scope>` | Yes/No | target/devarm | `<phase>` | `<file:line>` | adopt/adapt/exclude/escalate |

Grounding adds one row per discovered instruction source. Downstream repository-local artifacts
link to this canonical inventory instead of copying it and creating a second source of truth.
