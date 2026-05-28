---
name: super-dev
description: Coordinator-driven development workflow with parallel agent execution for implementing features, fixing bugs, improving performance, or refactoring code. Central Coordinator Agent orchestrates all phases and assigns tasks to specialized sub-agents.
---

# Super Dev Workflow

A coordinator-driven development system with parallel agent execution for all development tasks including bug fixes, new features, performance improvements, and refactoring.

**Announce at start:** "I'm using the super-dev skill to systematically implement this task with coordinator-driven orchestration."

## Integrated Ecosystem

This skill is enhanced with complementary tools from the everything-claude-code collection:

| Component | Purpose | When Used |
|-----------|---------|-----------|
| **Skills** | | |
| `tdd-workflow` | Test-driven development methodology | Phase 8 (Implementation) |
| `security-review` | Security checklist and validation | Phase 9 (Code Review) |
| `continuous-learning` | Auto-extract patterns from sessions | Session end |
| `strategic-compact` | Manual compaction suggestions | Large contexts |
| `backend-patterns` | API, database, caching patterns | Phase 5 (Assessment) |
| `frontend-patterns` | React, Next.js patterns | Phase 5 (Assessment) |
| `coding-standards` | Language best practices | Phase 8 (Implementation) |
| **Rules** | | |
| `security.md` | Mandatory security checks | Phase 9 (Code Review) |
| `testing.md` | TDD, 80% coverage requirement | Phase 8 (Implementation) |
| `coding-style.md` | Immutability, file organization | Phase 8 (Implementation) |
| `patterns.md` | Common code patterns | Phase 5 (Assessment) |
| `performance.md` | Model selection, context management | Phase 8 (Implementation) |
| **Contexts** | | |
| `dev.md` | Development mode context | Phase 8 (Implementation) |
| `review.md` | Code review mode context | Phase 9 (Code Review) |
| `research.md` | Research mode context | Phase 3 (Research) |
| **Additional Agents** | | |
| `planner` | Implementation planning | Alternative to Phase 6 |
| `tdd-guide` | Test-driven development guide | Phase 8 guidance |
| `security-reviewer` | Security vulnerability analysis | Phase 9 enhancement |
| `build-error-resolver` | Fix build errors | Build failures |
| `refactor-cleaner` | Dead code cleanup | Phase 11 (Cleanup) |
| **Additional Commands** | | |
| `/plan` | Quick planning | Small tasks |
| `/tdd` | Test-driven development | Testing focus |
| `/e2e` | E2E test generation | UI testing |
| `/learn` | Extract patterns mid-session | Knowledge capture |

## Context Mode Switching

Different phases of development benefit from different operational contexts. Switch contexts to optimize behavior:

| Context | When to Use | Behavior |
|---------|------------|----------|
| **research** | Phase 3 (Research), Phase 5 (Assessment) | Gather information, explore options, document findings. Prioritize breadth over depth. |
| **dev** | Phase 8 (Implementation), Phase 11 (Cleanup) | Write code first, explain after. Prefer working solutions over perfect. Run tests after changes. |
| **review** | Phase 7 (Spec Review), Phase 9 (Code Review) | Critical analysis, specification validation. Identify issues, verify against requirements. |

**How to switch contexts:**
- The Coordinator agent automatically applies appropriate context per phase
- Manual override: Load the relevant `contexts/{mode}.md` file when needed
- Context affects: response style, tool prioritization, verification approach

## Architecture Overview

```
                    ┌─────────────────┐
                    │   super-dev     │
                    │     Skill       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Coordinator   │ ◄── Central Authority
                    │     Agent       │
                    └────────┬────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
    ▼                        ▼                        ▼
┌─────────┐            ┌─────────┐            ┌─────────┐
│Planning │            │Analysis │            │Execution│
│ Agents  │            │ Agents  │            │ Agents  │
└─────────┘            └─────────┘            └─────────┘
```

## When to Use

Activate this skill when user asks to:
- Fix a bug or issue
- Fix build warnings or errors
- Implement a new feature
- Improve an existing feature
- Improve performance
- Resolve deprecation warnings
- Refactor code

## Workflow Phases

The Coordinator Agent orchestrates these phases automatically:

```
Development Workflow Progress:
- [ ] Phase 0: Apply Dev Rules (establish coding standards)
- [ ] Phase 1: Specification Setup (identify/create spec directory)
- [ ] Phase 2: Requirements Clarification (gather requirements)
- [ ] Phase 3: Research (best practices, docs, patterns) [Time MCP + Option Presentation]
- [ ] Phase 4: Debug Analysis (for bugs only) [grep/ast-grep]
- [ ] Phase 5: Code Assessment (architecture, style, frameworks) [grep/ast-grep]
- [ ] Phase 5.3: Architecture Design (for complex features - optional) [Option Presentation]
- [ ] Phase 5.5: UI/UX Design (for features with UI - optional) [Option Presentation]
- [ ] Phase 6: Specification Writing (tech spec, plan, tasks)
- [ ] Phase 7: Specification Review (validate against requirements)
- [ ] Phase 8: Execution & QA (PARALLEL: dev + qa executors)
- [ ] Phase 9: Code Review (spec-aware review using super-dev:code-reviewer)
- [ ] Iteration Rule: Loop Phase 8 and Phase 9 until no blocking issues remain (no Critical/High/Medium findings; all acceptance criteria met)
- [ ] Phase 10: Documentation Update (docs-executor sequential)
- [ ] Phase 11: Cleanup (remove temp files, unused code)
- [ ] Phase 12: Commit & Push (descriptive message)
- [ ] Phase 13: Final Verification (Coordinator verifies all complete)
```

## Option Presentation Rule (MANDATORY)

**CRITICAL WORKFLOW RULE:** The super-dev workflow MUST present 3-5 options with detailed comparisons at key decision points. This is NOT optional - it is the DEFAULT and EXPECTED behavior.

### Phases Requiring Option Presentation

The following phases MUST present options to the user for selection:

| Phase | Agent | What Requires Options |
|-------|-------|---------------------|
| Phase 3 | `super-dev:research-agent` | Technology choices, libraries, frameworks, implementation approaches |
| Phase 5.3 | `super-dev:architecture-agent` | Architecture patterns, module decomposition, data access, communication patterns |
| Phase 5.5 | `super-dev:ui-ux-designer` | Layout patterns, navigation, components, interactions, visual design |

### Option Presentation Workflow

```
User Request
     │
     ▼
┌─────────────────┐
│   Coordinator   │
│     Agent       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Research/Architecture/Design     │
│         Agent Generates              │
│           3-5 Options                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Present Options to User:          │
│   - Detailed descriptions            │
│   - Comparison matrix                │
│   - Strengths/Weaknesses             │
│   - Recommendation                   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     User Selects Option             │
│   (or requests modifications)        │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Coordinator Proceeds with         │
│      Selected Option                │
└─────────────────────────────────────┘
```

### Coordinator Responsibilities

The Coordinator Agent MUST:
1. **Ensure options are generated** - Verify that the relevant agent (research/architecture/design) has presented 3-5 options
2. **Wait for user selection** - Do NOT proceed to next phase until user has selected an option
3. **Document the decision** - Record the selected option in the specification
4. **Handle edge cases** - If user requests modifications, work with the agent to refine options

### Exception Handling

**Single answer is acceptable ONLY when:**
- Looking up specific API documentation
- Finding exact configuration values
- Retrieving specific error messages
- User explicitly requests "just give me the best option"
- Following established patterns without variation

**All other cases MUST present options.**

**CHECKPOINT RULE:** Coordinator ensures commits at each phase boundary.

Two indices are used throughout this workflow to organize specifications and their associated artifacts:

- Spec Index (spec-index): A numeric sequence that identifies each specification within the `specification/` directory. Naming convention: `[spec-index]-[spec-name]/`. Example: `01-user-auth/`, `02-payment-processing/`.

- doc Index (doc-index): A auto-incrementalnumeric sequence used to order and label files produced within a specific spec across workflow phases, not same with the phase index. These files are stored under the corresponding spec directory and use the doc index in their filenames. Naming convention: `[doc-index]-[document-type].md`. Example within `01-research-report.md`: `02-requirements.md`, `03-specification.md`.

Summary:
- Spec Index organizes specs at the directory level (which spec).
- Phase Index organizes documents within a spec by workflow phase (what was produced when).


## Entry Point: Coordinator Agent

**AGENT:** Invoke `super-dev:coordinator`

The Coordinator Agent is the CENTRAL AUTHORITY that:
1. Orchestrates ALL workflow phases
2. Assigns tasks to specialized sub-agents
3. Monitors execution - no unauthorized stops
4. Enforces quality gates
5. Manages build queue (Rust/Go serialization)
6. Performs final verification

```
Task(
  prompt: "Implement: [task description]",
  context: {
    task_type: "feature|bug|refactor|improvement",
    spec_directory: "[path to spec]"
  },
  subagent_type: "super-dev:coordinator"
)
```

---

## Individual Phase Commands

For granular control, you can invoke individual phases using slash commands:

| Phase | Command | Purpose |
|-------|---------|---------|
| 3 | `/super-dev:research [topic]` | Research - find best practices with Time MCP |
| 4 | `/super-dev:debug-analysis [bug details]` | Debug Analysis - root cause analysis (bugs only) |
| 5 | `/super-dev:code-assessment [feature]` | Code Assessment - evaluate existing codebase |
| 5.3 | `/super-dev:architecture-design [requirements]` | Architecture Design - create ADRs (complex features) |
| 5.5 | `/super-dev:ui-ux-design [UI requirements]` | UI/UX Design - design specifications (UI features) |
| 8 | `/super-dev:execute [spec path]` | Execution & QA - implement code with parallel testing |
| 9 | `/super-dev:code-review [changes]` | Code Review - spec-aware review using super-dev:code-reviewer |
| 10 | `/super-dev:documentation [spec path]` | Documentation Update - update all documentation |

**When to use individual phases:**
- When you need granular control over the workflow
- To re-run a specific phase after making corrections
- For learning or debugging the development process
- When working on very small tasks that don't need the full workflow

---

## Documentation Update Rules (CRITICAL - MANDATORY)

**At every milestone/phase boundary, update these documents:**

### 1. Task List Updates (`[doc-index]-task-list.md`)
- [ ] Mark completed tasks with `[x]`
- [ ] Add any new tasks discovered during implementation
- [ ] Note any blocked or deferred tasks with reasons

### 2. Implementation Summary Updates (`[doc-index]-implementation-summary.md`)
- [ ] Add completed work to "Code Changes" section
- [ ] Document any technical decisions made
- [ ] Record challenges encountered and solutions found

### 3. Specification Updates (`[doc-index]-specification.md`)
- [ ] Update affected sections with `[UPDATED: date]` marker
- [ ] Document why the change was necessary

**FORBIDDEN:**
- ❌ Completing a milestone without updating task list
- ❌ Moving to next phase with outdated implementation summary
- ❌ Changing implementation without updating specification

---

## Phase 0: Apply Dev Rules

**SKILL:** Invoke `super-dev:dev-rules`

Establishes coding standards, git practices, and quality standards.

---

## Phase 1: Specification Setup

Analyze information and identify/create spec directory under `specification/` with [spec-index(number)]-[spec name]

---

## Phase 2: Requirements Clarification

**AGENT:** Invoke `super-dev:requirements-clarifier`

**Output:** `[doc-index]-requirements.md`

---

## Phase 3: Research Phase (Time MCP Enhanced)

**AGENT:** Invoke `super-dev:research-agent`

**CONTEXT:** Apply `research` mode for information gathering and exploration

The research-agent:
- Gets current timestamp via Time MCP
- Adds year context to queries
- Filters by recency
- Flags deprecated information

**Integrated Tools:**
- **continuous-learning skill**: Auto-extracts reusable patterns from research sessions
- **backend-patterns/frontend-patterns**: Reference for architectural patterns
- **coding-standards**: Language-specific best practices lookup

**Output:** `[doc-index]-research-report.md` with freshness scores

---

## Phase 4: Debug Analysis (grep/ast-grep Enhanced)

**AGENT:** Invoke `super-dev:debug-analyzer`

The debug-analyzer:
- Uses Grep for text pattern search
- Uses ast-grep for structural analysis
- Tracks file coverage for debugging scope

**Output:** `[doc-index]-debug-analysis.md`

---

## Phase 5: Code Assessment (grep/ast-grep Enhanced)

**AGENT:** Invoke `super-dev:code-assessor`

The code-assessor:
- Uses Grep for pattern matching
- Uses ast-grep for structural analysis
- Tracks file coverage percentage

**Output:** `[doc-index]-assessment.md`

---

## Phase 5.3: Architecture Design (Complex Features)

**AGENT:** Invoke `super-dev:architecture-agent`

**Output:** `[doc-index]-architecture.md` and ADRs

---

## Phase 5.5: UI/UX Design (Features with UI)

**AGENT:** Invoke `super-dev:ui-ux-designer`

**Output:** `[doc-index]-design-spec.md`

---

## Phase 6: Specification Writing

**AGENT:** Invoke `super-dev:spec-writer`

**Output:** Three files (or sub-specifications for large features)
- `[doc-index]-specification.md` - Technical specification
- `[doc-index]-implementation-plan.md` - Implementation plan
- `[doc-index]-task-list.md` - Task list
(Or sub-specifications for large features)

---

## Phase 7: Specification Review (VALIDATION GATES)

Coordinator reviews all documents for alignment and completeness.

**CRITICAL VALIDATION GATES - Spec Review MUST verify:**

### Naming Convention Requirements (MANDATORY)
- [ ] **No generic variable names** - All variables use feature-specific prefixes
  - Prohibited: `data`, `item`, `value`, `result`, `temp`, `obj`, `val`
  - Required: `[feature][entity][property]` (e.g., `userAuthState`, `orderTotal`)
- [ ] **No single-letter names** - Except loop indices (i, j, k)
- [ ] **No abbreviations** - Except well-known ones (id, url, api, http)
- [ ] **Function names use verb-noun pattern** - `[feature][Action]` or `[verb][Noun]`
- [ ] **Constants use UPPER_CASE** - `[FEATURE_NAME]_[CONSTANT]`
- [ ] **Booleans use is/has/should prefix** - `isAuthenticated`, `hasPermission`

### No Ambiguity Requirements (MANDATORY)
- [ ] **Single Implementation Guarantee** - Spec must result in exactly ONE valid implementation
- [ ] **All function names are specified** - No room for interpretation
- [ ] **All parameter names are specified** - No generic names allowed
- [ ] **All file paths are specified** - No ambiguity about where code goes
- [ ] **All conditional behaviors are documented** - No "if needed, do X"
- [ ] **All error cases are listed** - No "handle errors appropriately"
- [ ] **No pronouns** - Replace "it", "they", "this" with specific nouns
- [ ] **No "etc." or "and so on"** - List everything explicitly
- [ ] **No "appropriate" or "suitable"** - Specify exact values
- [ ] **No "handle" or "process"** - Specify exact actions
- [ ] **No optional behaviors** - Everything is required or explicitly conditional

### File Inventory Requirements (MANDATORY)
- [ ] **Files to be Created** - Complete list with specific file names
- [ ] **Files to be Modified** - Complete list with specific changes required
- [ ] **Files to be Deleted** - Complete list with reasons
- [ ] **File Summary** - Total counts for created/modified/deleted
- [ ] **Each milestone includes Files Affected section** - Created/Modified/Deleted

**REJECT SPEC IF ANY GATE FAILS** - Return to spec-writer for corrections

### Additional Review Criteria
- [ ] Requirements addressed in specification
- [ ] Research findings incorporated
- [ ] Architecture decisions documented (if applicable)
- [ ] Design specifications included (if UI feature)
- [ ] Implementation plan is feasible
- [ ] Task list is complete and actionable
- [ ] All acceptance criteria are testable

---

## Phase 8: Execution & QA (PARALLEL Agents)

**CONTEXT:** Apply `dev` mode for implementation focus

**CRITICAL CHANGE:** The Coordinator invokes TWO agents in PARALLEL, with CodeRabbit running proactively:

```
┌─────────────────────────────────────────────────────────────┐
│                PARALLEL EXECUTION & QA                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │dev-executor │  │   qa-agent  │  │   CodeRabbit     │    │
│  │             │  │             │  │   (Background)   │    │
│  │ Implements  │  │ Plans & runs│  │   Reviews code   │    │
│  │ code        │  │ tests       │  │   proactively    │    │
│  │             │  │             │  │                   │    │
│  │             │  │             │  │  → Report issues │    │
│  │             │  │             │  │     to dev       │    │
│  │             │  │             │  │  → Verify fixes  │    │
│  │             │  │             │  │                   │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
│                          │                                   │
│                   BUILD QUEUE                                │
│              (Rust/Go: one at a time)                       │
└─────────────────────────────────────────────────────────────┘
```

**Agents:**
- `super-dev:dev-executor` - Implements code, invokes specialist developers
- `super-dev:qa-agent` - Modality-specific testing and verification (merged planning + execution)
- **CodeRabbit CLI (Background)** - Proactive code review starting immediately when dev begins implementation

**Integrated Skills & Rules:**
- **tdd-workflow skill**: Test-first methodology with 80%+ coverage requirement
- **testing rules**: Enforces TDD, unit/integration/E2E test coverage
- **coding-style rules**: Immutability, file organization (200-400 lines typical), error handling
- **performance rules**: Model selection guidance (Haiku for lightweight, Sonnet for development)
- **patterns reference**: Common patterns for API responses, custom hooks, repository pattern

### Code Quality Standards (MANDATORY - Enforced During Implementation)

**The dev-executor MUST adhere to these standards during Phase 8:**

#### Naming Convention Requirements (MANDATORY)
- [ ] **No generic variable names** - All variables use feature-specific prefixes
  - Prohibited: `data`, `item`, `value`, `result`, `temp`, `obj`, `val`
  - Required: `[feature][entity][property]` (e.g., `userAuthState`, `orderTotal`)
- [ ] **No single-letter names** - Except loop indices (i, j, k)
- [ ] **No abbreviations** - Except well-known ones (id, url, api, http)
- [ ] **Function names use verb-noun pattern** - `[feature][Action]` or `[verb][Noun]`
- [ ] **Constants use UPPER_CASE** - `[FEATURE_NAME]_[CONSTANT]`
- [ ] **Booleans use is/has/should prefix** - `isAuthenticated`, `hasPermission`

#### No Ambiguity Requirements (MANDATORY)
- [ ] **Follow spec exactly** - Implementation must match specification unambiguously
- [ ] **Use specified names** - No deviation from spec-defined variable/function names
- [ ] **No generic names in code** - Even if spec allows, use descriptive names
- [ ] **Explicit error handling** - No "handle errors", specify exact error handling
- [ ] **No optional behaviors** - Everything is explicit or explicitly conditional

**CodeRabbit will flag violations of these standards.**

### CodeRabbit Proactive Execution

- Starts: As soon as dev agent signals implementation begins
- Mode: Background process with `--prompt-only` flag
- Purpose: Find issues early during implementation, not after completion
- Workflow:
  1. QA agent starts `coderabbit --prompt-only > coderabbit-output.log 2>&1 &`
  2. Monitors output for issues in real-time
  3. Reports issues to dev agent as they are found
  4. Dev agent fixes issues during implementation
  5. QA agent re-runs CodeRabbit to verify fixes
  6. Final CodeRabbit review before marking QA complete

**Build Policy (Rust/Go):**
- Only ONE build at a time
- Coordinator manages build queue
- Prevents resource conflicts

**Output:** Code, tests, and progress tracking

---

## Phase 9: Code Review

**CONTEXT:** Apply `review` mode for critical analysis

**AGENT:** Invoke `super-dev:code-reviewer`

**Integrated Skills & Rules:**
- **security-review skill**: Comprehensive security checklist validation
- **security rules**: Mandatory security checks (no hardcoded secrets, input validation, XSS/CSRF protection)
- **coding-style rules**: Code quality verification (immutability, no deep nesting, proper error handling)

Run specification-aware code review focused on correctness, security, performance, and maintainability. Scope to changed files and implementation summary; reference acceptance criteria from the spec.

**Iteration Rule (Coordinator-Enforced):**
- If verdict is Blocked or Changes Requested, or any Critical/High/Medium findings exist, or any acceptance criteria are Not Met/Partial → RE-ENTER Phase 8
- Create remediation tasks mapped from findings, run Execution & QA in parallel, then re-run Code Review
- Only proceed beyond Phase 9 when verdict is Approved or Approved with Comments (Low/Info only) and all acceptance criteria are met

**Output:** Code review report with severity, evidence, and verdict
- `[doc-index]-code-review.md`

---

## Phase 10: Documentation Update (Sequential)

**AGENT:** Invoke `super-dev:docs-executor`

After code review is complete and approved, update all documentation:
- Task list completion status
- Implementation summary with all changes
- Specification updates for any deviations
- Review findings integration

**Execution Model:** Sequential batch processing
- Runs after Phase 9 approval
- Processes all accumulated changes from Phases 8-9
- Single pass to update all documents
- Coordinates commit with code changes

**Output:** Updated
- `[doc-index]-task-list.md`
- `[doc-index]-implementation-summary.md`
- `[doc-index]-specification.md`

---

## Phase 11-12: Cleanup & Commit

Coordinator ensures:
1. No temp files remain
2. All changes committed
3. Descriptive commit messages

---

## Phase 13: Final Verification

Coordinator verifies:
- [ ] All specification documents created
- [ ] Implementation summary complete
- [ ] No missing code or files
- [ ] All changes committed
- [ ] All changes pushed to remote
- [ ] Git status clean (working tree clean)

### MANDATORY: Commit and Push on Completion

**CRITICAL REQUIREMENT:** When ALL tasks are complete, you MUST:

1. **Stage all changes**: `git add [files]` (only files modified in this session)
2. **Commit with descriptive message**: Follow project commit conventions
3. **Push to remote**: `git push` to ensure changes are not lost
4. **Verify clean state**: `git status` must show "working tree clean"

**NEVER** mark workflow as complete without committing and pushing all changes.

---

## Agents Reference

### Coordinator Agent (NEW - Central Authority)

| Agent | Purpose | Invoke Via |
|-------|---------|------------|
| `coordinator` | Central orchestrator for all phases | `super-dev:coordinator` |

### Executor Agents (NEW - Parallel & Sequential Execution)

| Agent | Purpose | Execution Mode | Invoke Via |
|-------|---------|----------------|------------|
| `super-dev:dev-executor` | Development implementation | Parallel (Phase 8) | `super-dev:dev-executor` |
| `super-dev:qa-agent` | Testing and verification (merged) | Parallel (Phase 8) | `super-dev:qa-agent` |
| `super-dev:docs-executor` | Documentation updates | Sequential (Phase 10) | `super-dev:docs-executor` |

### Workflow Agents

| Agent | Purpose | Invoke Via |
|-------|---------|------------|
| `super-dev:requirements-clarifier` | Gather requirements | `super-dev:requirements-clarifier` |
| `super-dev:research-agent` | Research with Time MCP | `super-dev:research-agent` |
| `super-dev:search-agent` | Multi-source search | `super-dev:search-agent` |
| `super-dev:debug-analyzer` | Root cause analysis (grep/ast-grep) | `super-dev:debug-analyzer` |
| `super-dev:code-assessor` | Assess codebase (grep/ast-grep) | `super-dev:code-assessor` |
| `super-dev:code-reviewer` | Specification-aware code review | `super-dev:code-reviewer` |
| `super-dev:architecture-agent` | Design architecture and create ADRs | `super-dev:architecture-agent` |
| `super-dev:ui-ux-designer` | Create UI/UX design specifications | `super-dev:ui-ux-designer` |
| `super-dev:spec-writer` | Write specifications | `super-dev:spec-writer` |
| `super-dev:qa-agent` | Modality-specific QA testing | `super-dev:qa-agent` |

### Developer Agents (Specialists)

| Agent | Purpose | Languages/Frameworks |
|-------|---------|---------------------|
| `super-dev:rust-developer` | Rust systems programming | Rust 1.75+, Tokio, axum |
| `super-dev:golang-developer` | Go backend development | Go 1.21+, stdlib, gin, chi |
| `super-dev:frontend-developer` | Web frontend development | React 19, Next.js 15, TypeScript, Tailwind v4 |
| `super-dev:backend-developer` | Backend/API development | Node.js/TS, Python, FastAPI, databases |
| `super-dev:android-developer` | Android app development | Kotlin, Jetpack Compose, MVVM |
| `super-dev:ios-developer` | iOS app development | Swift, SwiftUI, async/await |
| `super-dev:windows-app-developer` | Windows desktop development | C#/.NET 8+, WinUI 3, WPF |
| `super-dev:macos-app-developer` | macOS desktop development | Swift, SwiftUI, AppKit |

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `super-dev:dev-rules` | Core development rules and philosophy |
| `tdd-workflow` | Test-driven development methodology (80%+ coverage) |
| `security-review` | Security checklist and validation |
| `continuous-learning` | Auto-extract patterns from sessions |
| `strategic-compact` | Manual compaction suggestions |
| `coding-standards` | Language best practices reference |
| `backend-patterns` | API, database, caching patterns |
| `frontend-patterns` | React, Next.js patterns |

## Rules Reference

The `rules/` directory contains modular always-follow guidelines that apply throughout the workflow:

| Rule | Applies To | Key Requirements |
|------|-----------|------------------|
| `security.md` | Phase 9 (Code Review) | No hardcoded secrets, input validation, XSS/CSRF protection |
| `testing.md` | Phase 8 (Implementation) | TDD, 80% coverage, unit/integration/E2E tests |
| `coding-style.md` | Phase 8 (Implementation) | Immutability, 200-400 line files, proper error handling |
| `patterns.md` | Phase 5 (Assessment) | Common code patterns (API format, hooks, repository) |
| `performance.md` | Model Selection | Haiku (lightweight), Sonnet (development), Opus (complex) |
| `git-workflow.md` | Phase 12 (Commit) | Commit format, PR process |
| `agents.md` | Task Delegation | When to delegate to subagents |

## Key Differences from Previous Version

1. **Coordinator Agent**: Central authority orchestrates all phases
2. **Parallel Execution**: dev/qa executors run simultaneously in Phase 8
3. **Sequential Documentation**: docs-executor runs in Phase 10 after code review approval
4. **Build Queue**: Rust/Go builds serialized (one at a time)
5. **Time MCP**: Research agent uses current timestamp
6. **grep/ast-grep**: Assessment/debug agents use code search skills
7. **Final Verification**: Coordinator verifies all artifacts complete
8. **NEW: Integrated Ecosystem**: Enhanced with everything-claude-code skills, rules, and contexts
9. **NEW: Context Mode Switching**: Dynamic context injection for dev/review/research modes
10. **NEW: TDD Workflow**: Comprehensive test-driven development methodology
11. **NEW: Security Review**: Enhanced security validation and checklist

## Notes

All core agents are provided by this plugin (`super-dev:*` prefix).

The plugin is self-contained with integrated best practices including skills, rules, and contexts.
