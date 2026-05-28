---
name: development-methodology
description: >
  Milestone-anchored development methodology. Use when planning milestones,
  starting sessions, creating implementation guides, or reviewing process.
  Triggers: milestone planning, session workflow, implementation guide,
  session summary, milestone review, maintenance session, PROJECT.md,
  session closeout, development session, planning phase, post session review.
  File patterns: _context/milestones/*.md, _context/sessions/*.md, PROJECT.md
---

# Development Methodology

## When This Skill Applies

- Starting a new milestone or session
- Creating implementation guides
- Conducting milestone planning or review
- Session closeout activities
- Understanding the development workflow

## Milestone Planning Session

Before starting a milestone, conduct a planning session to align on scope, dependencies, and session breakdown.

### 1. Explore Current State
- Launch explore agents to understand codebase, architecture, dependencies
- Identify patterns established in previous milestones
- Review what infrastructure exists to build on

### 2. Analyze Roadmap Alignment
- Review milestone deliverables and success criteria from PROJECT.md
- Check for missing dependencies (go.mod, external tools, libraries)
- Evaluate milestone ordering - surface concerns if dependencies seem misaligned
- Identify any deliverables that could be simplified by existing patterns

### 3. Discuss Strategic Questions
- Surface ordering concerns or alternatives collaboratively
- Resolve through discussion, not assumptions
- Document decisions with rationale

### 4. Explore External Dependencies
- For milestones using external libraries, explore their APIs
- Identify built-in capabilities that simplify scope
- Understand configuration patterns and integration points

### 5. Define Session Breakdown
- Break milestone into focused 2-3 hour sessions
- Identify key files and validation criteria per session
- Leverage existing patterns from previous milestones
- Ensure dependency order (sessions build on previous work)

### 6. Resolve Design Questions
- Address implementation decisions incrementally with context
- Document decisions with rationale in PROJECT.md

### 7. Finalize and Document
- Update PROJECT.md with session breakdown and design decisions
- Create milestone architecture document at `_context/milestones/m##-[title].md`
- Capture process improvements if workflow evolved

## Milestone Architecture Documents

For milestones with multiple sessions, create an architecture document that preserves technical context across sessions.

**Location**: `_context/milestones/m##-[title].md`

**Contents**:
- **Key Decisions**: Architectural choices and rationale
- **Schema Design**: Database tables with field descriptions
- **API Design**: Endpoints with request/response formats
- **Integration Patterns**: How this milestone connects to existing domains
- **Interface Definitions**: Key types and contracts
- **Session Breakdown**: Overview of what each session delivers

**Lifecycle**:
- Created during milestone planning
- Referenced by implementation guides for each session
- Updated if sessions reveal new patterns or decisions
- Archived to `_context/milestones/.archive/` after milestone completion

## Development Session Workflow

Each development session follows a structured workflow:

### 1. Planning Phase
**Collaborative exploration** of implementation approaches:
- Discuss architectural decisions and trade-offs
- Explore multiple implementation strategies
- Ask clarifying questions as needed
- Reach alignment on approach before proceeding

**Not** a one-shot plan presentation - iterate until aligned.

### 2. Plan Presentation
Present **outline of implementation guide** for approval:
- Summarize agreed approach
- Show high-level structure
- Confirm scope and phases
- Get explicit approval before detailed guide

**Plan Mode Note**: If using plan mode, the plan file (`.claude/plans/`) serves as this outline. After plan mode approval, proceed to step 3 to create the full implementation guide - do NOT begin implementation.

### 3. Implementation Guide Creation
Create comprehensive step-by-step guide:
- Stored in `_context/[session-id]-[session-title].md`
- Session ID format: `01a`, `01b`, `02a`, etc. (milestone + letter)
- Structure: Problem context, architecture approach, detailed implementation steps
- **Dependency Order**: Structure steps from lowest to highest dependency level

**Code Block Conventions:**
- Code blocks have NO comments (minimize tokens, avoid maintenance)
- NO testing infrastructure (AI's responsibility after implementation)
- NO documentation (godoc comments added by AI after validation)
- NO OpenAPI `openapi.go` file contents (AI creates these in Step 4)
  - DO include route definitions with `OpenAPI: Spec.*` references
  - DO include schema registration in routes.go (`components.AddSchemas(...)`)

**File Change Conventions:**
- **Existing files**: Show incremental changes only (what's being added/modified)
- **New files**: Provide complete implementation
- Never replace entire existing files - preserve original architecture integrity

### 4. OpenAPI Maintenance
Prepare API specification infrastructure before implementation:
- Create/update domain `openapi.go` with operations and schemas
- Ensure schema types align with OpenAPI 3.1
- Verify helper functions produce valid references

### 5. Developer Execution
Developer implements following the guide:
- Developer executes implementation as code base maintainer
- AI on standby for mentorship and adjustments
- Focus on code structure, not comments or tests

### 6. Validation Phase
AI reviews and validates implementation:
- Review for accuracy and completeness
- Add and revise testing infrastructure
- Execute tests until passing
- Verify critical paths are covered
- Black-box testing: `package <name>_test`, test only public API

### 7. Documentation Phase
AI adds code documentation:
- Add godoc comments to exported types, functions, methods
- Document non-obvious behavior

### 8. Session Closeout
Session closeout ensures documentation stays aligned and captures patterns.

**8.1 Generate Session Summary**:
- Create `_context/sessions/[session-id]-[session-title].md`
- Document what was implemented, key decisions, and patterns established

**8.2 Archive Implementation Guide**:
- Move guide to `_context/sessions/.archive/[session-id]-[session-title].md`

**8.3 Update Documentation** (evaluate each):

| Document | Update Criteria |
|----------|-----------------|
| **README.md** | Only critical user-facing changes |
| **Context architecture** | Update rules/skills if patterns evolved |
| **Milestone architecture doc** | Update if session revealed new patterns |
| **PROJECT.md** | Update session status, evaluate remaining sessions |

## Maintenance Session Workflow

Maintenance sessions focus on cleanup, refactoring, or cross-repository coordination.

**When to Use**:
- Migrating functionality between repositories
- Refactoring patterns across multiple domains
- Pre-milestone cleanup to reduce technical debt
- Cross-repository version coordination

**Session ID Format**: `mt##` (e.g., `mt01`, `mt02`)

**Workflow**:
1. **Planning Phase** - Review scope and dependencies across repositories
2. **Implementation Guide** - Create guide at `_context/mt##-[title].md`
3. **Developer Execution** - Follow guide, coordinating releases if needed
4. **AI Validation** - Validate changes and adjust tests
5. **Session Closeout**:
   - Archive guide to `_context/sessions/.archive/mt##-[title].md`
   - Create summary at `_context/sessions/mt##-[title].md`
   - Update PROJECT.md with maintenance session status

**Key Differences from Development Sessions**:
- May span multiple repositories
- Library releases may be required between phases
- Focus on consolidation rather than new capability
- Tests may need adjustment rather than creation

## Post Session Milestone Review

After completing a development session (especially mid-milestone), conduct a review to ensure the roadmap stays aligned.

**When to Trigger:**
- After sessions where friction points or improvement opportunities were identified
- When architectural patterns evolved during implementation
- When scope adjustments are needed for remaining sessions

**Workflow:**
1. **Reflect on Current State** - What was implemented vs. planned? What patterns emerged?
2. **Identify Improvement Areas** - Friction points, patterns that could be abstracted
3. **Determine Approach** - Address now vs. defer? Which session handles it?
4. **Update Roadmap** - Adjust remaining session scopes in PROJECT.md

**Note:** This is a planning-only activity. No code changes.

## Milestone Review

After completing all sessions in a milestone:
1. **Validate Success Criteria** - Confirm all milestone objectives met
2. **Integration Testing** - Test milestone as cohesive unit
3. **Identify Adjustments** - Document any final changes needed
4. **Execute Adjustments** - Make necessary refinements
5. **Final Validation** - Confirm milestone complete
6. **Documentation Update** - Update PROJECT.md milestone status

## Milestone Completion

Mark milestone complete only after:
- All development sessions completed
- Milestone review passed
- All success criteria validated
- Integration tests passing
- Documentation updated

## Testing Conventions

**Organization:**
- Tests in `tests/` directory mirroring `internal/` structure
- File naming: `<file>_test.go`

**Black-Box Testing:**
- All tests use `package <name>_test`
- Import package being tested
- Test only exported types/functions/methods

**Coverage Success Criteria:**

Testing success is measured by coverage of critical paths:

- Happy paths - Normal operation flows work correctly
- Security paths - Input validation, path traversal prevention
- Error types - Domain errors are defined and distinguishable
- Integration points - Lifecycle hooks, system boundaries

Uncovered code is acceptable when it consists of:
- Defensive error handling for OS-level failures
- Edge cases requiring special conditions
- Error wrapping paths that don't affect behavior

## Directory Reference

```
_context/
├── [session-id]-[title].md      # Active implementation guides
├── milestones/
│   ├── m##-[title].md           # Active milestone architecture docs
│   └── .archive/                # Completed milestone docs
├── sessions/
│   ├── [session-id]-[title].md  # Session summaries
│   └── .archive/                # Archived implementation guides
└── prompts/                     # Session start prompts
```
