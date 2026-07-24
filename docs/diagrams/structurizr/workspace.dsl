workspace "Tech Catalyst Internal Method Map" "C4 and flow views for the Tech Catalyst / devarm development method." {
    !identifiers hierarchical

    model {
        developer = person "Developer" "The person asking an agent to change a target repository and approving consequential decisions."
        maintainer = person "Method Maintainer" "The person improving this method kit after sessions reveal drift, missing gates, or weak instructions."

        agentTools = softwareSystem "Agent Tools" "Cursor, OpenAI Codex, GitHub Copilot, Claude Code, or another agents.md-compatible coding agent." {
            tags "External"
        }

        targetRepo = softwareSystem "Target Repository" "The application or library being changed with Tech Catalyst/devarm." {
            tags "External"
        }

        gitHost = softwareSystem "Git Remote / PR Host" "GitHub or another remote used for branches, pull requests, and review." {
            tags "External"
        }

        method = softwareSystem "Tech Catalyst / devarm Method Kit" "Portable skills, templates, and rules that turn an idea into shipped code while keeping decisions explicit." {
            instructions = container "AGENTS.md" "Cross-tool operating instructions: invocation policy, phase order, decision ownership, and principles." "Markdown / agents.md" {
                tags "Instruction Contract"
            }

            installer = container "Installer" "Symlinks skills into global or per-project agent skill directories." "Shell" {
                tags "Distribution"
            }

            skillCatalog = container "Skill Catalog" "One SKILL.md per phase; these are the executable method contracts consumed by agent tools." "Agent Skills / Markdown" {
                brainstorm = component "devarm-brainstorm" "Explores the idea, asks focused questions, proposes approaches, writes the draft design, and invokes grounding before approval." "SKILL.md"
                ground = component "devarm-ground" "Verifies reuse claims against real files, resolves implementation-decision categories, and appends Detailed Design + Decision Ledger." "SKILL.md"
                spec = component "devarm-spec" "Turns the grounded design into testable WHAT/WHY requirements and scenarios." "SKILL.md"
                plan = component "devarm-plan" "Maps file responsibilities, integration seams, contracts, and step-by-step implementation work." "SKILL.md"
                tasks = component "devarm-tasks" "Creates dependency-ordered, tests-first tasks with decision-to-test traceability." "SKILL.md"
                analyze = component "devarm-analyze" "Runs the mandatory pre-implementation gate: artifact consistency, current-code verification, and an interactive implementation-decision brainstorm that batch-decides remaining decisions with the developer." "SKILL.md"
                implement = component "devarm-implement" "Executes tasks with red-green-refactor, fresh verification, and decision-drift handling." "SKILL.md"
                review = component "devarm-review" "Reviews implementation through architecture and QA lenses against the grounded design and Decision Ledger." "SKILL.md"
                finish = component "devarm-finish" "Verifies the full suite fresh, then offers merge, PR, keep, or discard." "SKILL.md"
                retro = component "devarm-retro" "Turns shipped or painful sessions into proposed improvements to the method kit." "SKILL.md"
                debug = component "devarm-debug" "On-demand root-cause workflow for bugs, test failures, and unexpected behavior." "SKILL.md"
                tdd = component "devarm-tdd" "Shared discipline for failing-test-first implementation and bug fixes." "SKILL.md"
            }

            templates = container "Templates" "Reusable artifact structures for design docs, decision ledgers, config decisions, findings ledgers, code standards, and constitutions." "Markdown"

            artifacts = container "Planning Artifacts" "Feature-specific files produced inside the target repo: design.md, spec.md, plan.md, tasks.md, findings.md, and Decision Ledger." "Markdown"

            gates = container "Phase Gates" "Procedural stop points that decide whether the workflow may advance." "Process Rules" {
                tags "Gate"
            }

            changelog = container "CHANGELOG.md" "Durable record of method changes and the failure or lesson that motivated each one." "Markdown"
        }

        developer -> agentTools "Requests feature work, bug fixes, reviews, diagrams, or phase execution"
        maintainer -> method "Edits and commits method improvements"
        agentTools -> method.instructions "Reads portable instructions"
        agentTools -> method.skillCatalog "Discovers and invokes skills"
        agentTools -> targetRepo "Reads code, writes artifacts, edits code, runs tests"
        method.installer -> agentTools "Publishes skills via symlinks"
        method.installer -> method.skillCatalog "Links source skills"
        method.skillCatalog -> method.templates "Uses artifact templates"
        method.skillCatalog -> method.artifacts "Creates and updates planning artifacts"
        method.artifacts -> targetRepo "Live beside the code they govern"
        method.skillCatalog -> targetRepo "Grounds claims, implements tasks, verifies current code"
        method.skillCatalog -> method.gates "Stops or advances at phase gates"
        method.gates -> developer "Requests approval, decisions, or next phase confirmation"
        method.review -> method.artifacts "Writes findings ledger and checks Decision Ledger fidelity"
        method.retro -> method.changelog "Records method lessons"
        method.finish -> gitHost "Pushes branch or opens pull request when selected"
        targetRepo -> gitHost "Stores branch, commits, and PR discussion"

        method.brainstorm -> method.ground "Invokes grounding before design approval"
        method.ground -> method.artifacts "Appends Detailed Design and Decision Ledger"
        method.ground -> targetRepo "Verifies reuse claims with file:line evidence"
        method.spec -> method.artifacts "Creates spec.md"
        method.plan -> method.artifacts "Creates plan.md and file map"
        method.tasks -> method.artifacts "Creates tests-first tasks.md"
        method.analyze -> method.artifacts "Checks design, spec, plan, tasks, and Decision Ledger"
        method.analyze -> targetRepo "Re-verifies seams and reuse against current code"
        method.implement -> method.tdd "Uses failing-test-first discipline"
        method.implement -> targetRepo "Writes tests and code, runs verification"
        method.implement -> method.debug "Invokes when a bug or unexpected failure appears"
        method.debug -> method.tdd "Requires reproducing failing test before fix"
        method.debug -> targetRepo "Traces root cause and verifies one fix"
        method.review -> targetRepo "Inspects diff and runtime paths"
        method.finish -> targetRepo "Runs full suite and handles branch outcome"
        method.retro -> method.skillCatalog "Proposes skill changes"
        method.retro -> method.templates "Proposes template changes"
    }

    views {
        systemContext method "SystemContext" "Who uses the method kit, what external systems it touches, and where target code lives." {
            include *
            autoLayout lr
        }

        container method "Containers" "Internal parts of the method kit and their connections to agent tools and target repositories." {
            include *
            autoLayout lr
        }

        component method.skillCatalog "SkillComponents" "The phase skills and how they chain together." {
            include *
            autoLayout lr
        }

        dynamic method "StandardPipelineFlow" "Sequence-style flow from idea to shipped code." {
            developer -> agentTools "Ask to use Tech Catalyst/devarm"
            agentTools -> method.instructions "Check invocation policy and phase order"
            agentTools -> method.brainstorm "Explore scope and write draft design"
            method.brainstorm -> method.ground "Ground design before approval"
            method.ground -> targetRepo "Verify reuse, seams, boundaries, and runtime contracts"
            method.ground -> method.artifacts "Append Detailed Design + Decision Ledger"
            method.gates -> developer "Request design approval"
            agentTools -> method.spec "Write testable spec after approval"
            agentTools -> method.plan "Create implementation plan and file map"
            agentTools -> method.tasks "Create tests-first task list"
            agentTools -> method.analyze "Run mandatory pre-implementation gate"
            method.analyze -> targetRepo "Re-check current code and flagship story"
            agentTools -> method.implement "Execute tasks with TDD after analyze is clean"
            method.implement -> targetRepo "Write tests/code and verify"
            agentTools -> method.review "Review diff against design, ledger, and rules"
            agentTools -> method.finish "Run fresh suite and select branch outcome"
            method.finish -> gitHost "Merge, push PR, keep branch, or discard if confirmed"
            agentTools -> method.retro "Improve method after ship or painful session"
            method.retro -> method.changelog "Record lesson and method diff"
            autoLayout lr
        }

        dynamic method "GroundingFlow" "How a draft design becomes code-grounded before it can be approved." {
            method.brainstorm -> method.artifacts "Create draft design.md"
            method.ground -> method.artifacts "Extract every reuse/wrap/extend/import/call claim"
            method.ground -> targetRepo "Open cited files and verify shape, wiring, legality, size, and duplication"
            method.ground -> method.artifacts "Resolve the ten implementation-decision categories"
            method.ground -> method.artifacts "Write Detailed Design and Decision Ledger rows"
            method.gates -> method.artifacts "Check all grounding boxes"
            method.gates -> developer "Surface owner:user decisions and approval request"
            developer -> agentTools "Approve, revise, or answer open decisions"
            autoLayout lr
        }

        dynamic method "AnalyzeGateFlow" "How the method blocks implementation until artifacts and current code agree." {
            method.analyze -> method.artifacts "Load design, spec, plan, tasks, Decision Ledger"
            method.analyze -> method.artifacts "Pass 1: check coverage, ambiguity, terminology, contradictions, and ledger status"
            method.analyze -> targetRepo "Pass 2: re-open current code seams and reuse targets"
            method.analyze -> targetRepo "Trace flagship user story end-to-end with real data shapes"
            method.analyze -> method.artifacts "Write severity-ranked findings"
            method.gates -> agentTools "Block implementation on unresolved CRITICAL/HIGH findings"
            method.gates -> developer "Ask for owner:user resolutions when needed"
            method.gates -> developer "Pass 3: walk control flows and present the implementation-decision batch"
            developer -> agentTools "Confirm flows and answer the decision batch"
            method.analyze -> method.artifacts "Record batch decisions as Decision Ledger rows"
            method.gates -> method.implement "Allow implementation only when analyze is clean and Pass 3 decisions are recorded"
            autoLayout lr
        }

        dynamic method "DecisionOwnershipFlow" "How decisions are made, recorded, tested, and protected from drift." {
            developer -> agentTools "Provides goal, constraints, or answers"
            agentTools -> method.brainstorm "Elicit purpose, scope, semantics, limits, compatibility, UX, dependencies, success criteria"
            method.ground -> method.artifacts "Record load-bearing choices as Decision Ledger rows"
            method.gates -> developer "Ask for design-level owner:user decisions"
            method.plan -> method.artifacts "Implement ledger rows in file map and seam contracts"
            method.tasks -> method.artifacts "Create enforcing test tasks for each locked decision"
            method.analyze -> method.artifacts "Reject missing tests, assumptions, or drift"
            method.implement -> method.artifacts "Update ledger when implementation trade-offs arise"
            method.implement -> developer "Stop for design-level drift or changed semantics"
            method.review -> method.artifacts "Treat ledger-approved choices as by-design unless reopened"
            method.retro -> method.skillCatalog "Tighten skills when late decisions escaped earlier gates"
            autoLayout lr
        }

        dynamic method "ImplementationTddLoop" "Per-task red-green-refactor loop and decision drift handling." {
            method.implement -> method.analyze "Confirm clean analyze precondition"
            method.implement -> method.artifacts "Read next tests-first task"
            method.implement -> method.tdd "Write failing test first"
            method.tdd -> targetRepo "Run test and confirm expected RED"
            method.implement -> targetRepo "Write minimum production code"
            method.tdd -> targetRepo "Run test and confirm GREEN"
            method.implement -> targetRepo "Refactor with tests green"
            method.implement -> targetRepo "Run relevant verification"
            method.implement -> method.artifacts "Flag any implementation trade-off in ledger"
            method.implement -> developer "Stop if reality contradicts design-level decision"
            method.implement -> method.debug "Invoke root-cause workflow on failures"
            autoLayout lr
        }

        dynamic method "DebugLoop" "On-demand root-cause flow used whenever bugs or unexpected behavior appear." {
            method.implement -> method.debug "Failure or unexpected behavior appears"
            method.debug -> targetRepo "Read full error, reproduce reliably, check diff and recent changes"
            method.debug -> targetRepo "Instrument boundaries and trace bad values backward"
            method.debug -> targetRepo "Compare against working examples"
            method.debug -> targetRepo "Test one hypothesis with the smallest possible change"
            method.debug -> method.tdd "Write reproducing failing test"
            method.debug -> targetRepo "Apply one root-cause fix"
            method.debug -> targetRepo "Verify test, suite, and original symptom"
            method.debug -> method.implement "Return to current phase after verified fix"
            method.debug -> developer "After three failed fixes, ask architecture/design question"
            autoLayout lr
        }

        dynamic method "FinishFlow" "How completed work is integrated or intentionally preserved." {
            method.finish -> targetRepo "Run full suite and lint/type gates fresh"
            method.finish -> method.artifacts "Confirm no open blocking findings or assumed ledger rows"
            method.finish -> targetRepo "Determine base branch"
            method.gates -> developer "Offer exactly four options: merge, PR, keep, discard"
            developer -> agentTools "Choose finish action"
            agentTools -> method.finish "Execute selected action"
            method.finish -> gitHost "Merge locally or push PR when selected"
            method.finish -> targetRepo "Keep branch or discard only after typed confirmation"
            method.finish -> method.retro "Recommend retro after merge or PR"
            autoLayout lr
        }

        styles {
            element "Person" {
                shape person
                background #0B5CAD
                color #FFFFFF
            }

            element "Software System" {
                background #116466
                color #FFFFFF
            }

            element "External" {
                background #606C76
                color #FFFFFF
            }

            element "Container" {
                background #2F855A
                color #FFFFFF
            }

            element "Component" {
                background #F6AD55
                color #1A202C
            }

            element "Instruction Contract" {
                background #805AD5
                color #FFFFFF
            }

            element "Distribution" {
                background #3182CE
                color #FFFFFF
            }

            element "Gate" {
                shape hexagon
                background #C53030
                color #FFFFFF
            }
        }
    }
}
