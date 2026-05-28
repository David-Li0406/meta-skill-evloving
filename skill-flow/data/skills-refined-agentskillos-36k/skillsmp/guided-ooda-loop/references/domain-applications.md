# Domain Applications of OODA Loop

This document provides specific guidance for applying the OODA pattern across different domains. Each section includes domain-specific workflows, artifacts, and best practices.

---

## Section 1: Software Development

### Overview

Software development was the original context for Prompt-Driven Development (PDD), which became the foundation for the generalized OODA pattern. This section details the complete 8-step process for applying OODA to building software features and systems.

### When to Use for Software

**Trigger scenarios:**
- Building new features or systems
- Designing technical architectures
- Planning major refactors
- Prototyping ideas for validation
- Creating implementation roadmaps

**Do NOT use for:**
- Quick bug fixes
- Simple code changes
- Well-understood patterns (just implement)
- Emergency hotfixes

### Software-Specific OODA Mapping

| OODA Phase | Software Activities | Key Artifacts |
|------------|-------------------|---------------|
| **Observe** | Codebase analysis, API research, existing solutions, technology landscape | research.md with architecture diagrams |
| **Orient** | Requirements clarification, technical constraints, user needs, edge cases | idea-honing.md with Q&A |
| **Decide** | Technology selection, architecture patterns, component boundaries, data models | high-level-design.md with mermaid diagrams |
| **Act** | Implementation plan, test strategy, integration approach, deployment plan | detailed-design.md + implementation-plan.md |

### The 8-Step PDD Process

The original PDD SOP defines 8 steps, with Steps 3-7 forming the essential OODA core:

**Pre-OODA Steps:**
1. **Create Project Structure** - Initialize directory and files
2. **Initial Process Planning** - Determine starting approach

**OODA Core (Steps 3-7):**
3. **Requirements Clarification** (Orient)
4. **Research Relevant Information** (Observe/Orient)
5. **Iteration Checkpoint** (Orient/Decide transition)
6. **Create Detailed Design** (Decide/Act)
7. **Develop Implementation Plan** (Act)

**Post-OODA Steps:**
8. **Summarize and Present Results** - Final handoff

### Step 1: Create Project Structure

**Purpose:** Set up organized directory for all artifacts.

**Process:**
1. Create `ooda-loop-{unique-name}-{DDMMMYY.HHMMSS}/` directory
2. Create initial files:
   - `rough-idea.md` (from user input)
   - `observe/idea-honing.md` (empty, ready for Q&A)
   - `observe/research/` subdirectory
   - `decide/` subdirectory
   - `act/` subdirectory
   - `summary.md` (with YAML frontmatter)

**Critical Constraints:**
- MUST NOT overwrite existing project directory (data loss risk)
- MUST ask for project_dir if default `.sop/planning` exists with contents
- MUST prompt user to add files to context: `/context add {project_dir}/**/*.md`
- MUST explain that this ensures files remain in context throughout

**Outputs:**
- Complete directory structure
- `rough-idea.md` with user's initial concept
- `summary.md` initialized (status: in-progress, phase: observe)

### Step 2: Initial Process Planning

**Purpose:** Determine approach and sequence before starting.

**Process:**
1. Ask user preference:
   - Start with requirements clarification (default)
   - Start with preliminary research on specific topics
   - Provide additional context first
2. Explain the process is iterative
3. Wait for explicit user direction

**Critical Constraints:**
- MUST NOT automatically proceed without user confirmation
- MUST adapt subsequent process based on user preference
- MUST explain iteration is allowed between phases

**Outputs:**
- User's chosen starting approach
- Updated `summary.md` with selected path

### Step 3: Requirements Clarification (Orient Phase)

**Purpose:** Refine initial idea through structured Q&A.

**Process:**
1. Create `observe/idea-honing.md` if not exists
2. Ask ONE question at a time
3. Append question to idea-honing.md
4. Present question to user
5. Wait for complete user response (may require multiple turns)
6. Append user's answer to idea-honing.md
7. Formulate next question
8. Repeat until sufficient detail gathered

**Questions to Ask:**
- Core functionality and features
- User experience and workflows
- Technical constraints and dependencies
- Success criteria and metrics
- Edge cases and error scenarios
- Performance requirements
- Security considerations
- Integration points

**Critical Constraints:**
- MUST ask only ONE question at a time (prevents overwhelm)
- MUST NOT pre-populate answers (assumes user preferences)
- MUST NOT write multiple Q&A pairs at once (skips interaction)
- MUST wait for complete response before next question
- MAY suggest options but MUST wait for actual choice
- MUST explicitly ask if clarification is complete before proceeding
- MUST offer to conduct research if questions arise needing more info
- MUST be prepared to return to clarification after research

**Formatting in idea-honing.md:**
```markdown
## Question 1: Core Functionality

**Q:** What is the primary function of this feature?

**Options considered:**
- Template creation system
- Document generation engine
- Both creation and generation

**Final Answer:**
Users need both - ability to create reusable templates and then generate documents from those templates with custom field values.

**Rationale:**
This provides the most value and matches existing workflow patterns.
```

**Outputs:**
- Complete `observe/idea-honing.md` with all Q&A
- Updated `summary.md` (phase: orient)

**Troubleshooting - Clarification Stalls:**
- Suggest moving to different aspect
- Provide examples or options
- Summarize what's established, identify gaps
- Suggest research to inform decisions

### Step 4: Research Relevant Information (Observe/Orient)

**Purpose:** Gather information on technologies, patterns, existing solutions.

**Process:**
1. Identify research areas based on requirements
2. Propose research plan to user:
   - Topics to investigate
   - Suggested resources
   - Available search tools
3. Ask for user input:
   - Additional topics
   - Specific resources they recommend
   - Their existing knowledge to contribute
4. Incorporate user suggestions
5. Conduct research with appropriate tools
6. Document in `observe/research/*.md` files
7. Include mermaid diagrams for architectures
8. Include links to sources
9. Periodically check in with user
10. Summarize key findings
11. Ask if research is sufficient

**Research Topics for Software:**
- Existing code patterns in codebase
- Relevant libraries and frameworks
- API documentation
- Similar features in other systems
- Technology trade-offs
- Security best practices
- Performance patterns
- Testing approaches

**Tool Usage:**
- `search_internal_code` - Find relevant code in codebase
- `read_internal_website` - Access internal docs/wikis
- MCP tools like 'peccy web search' - External research
- MUST ask user about using additional search tools

**Documentation Structure:**
```
observe/research/
├── existing-code.md      # Current codebase patterns
├── technologies.md       # Framework/library options
├── architecture.md       # System design patterns
└── external-solutions.md # How others solved this
```

**Mermaid Diagram Requirements:**
```markdown
## Current System Architecture

<function_calls>
graph TB
    Frontend[React Frontend]
    API[REST API]
    DB[(PostgreSQL)]

    Frontend -->|HTTP| API
    API -->|SQL| DB
```markdown
```

**Critical Constraints:**
- MUST organize research by topic in separate files
- MUST include mermaid diagrams for system architectures
- MUST include links to references and sources
- MUST periodically check with user during research
- MUST ask if research is sufficient before proceeding
- MUST offer to return to requirements if research uncovers questions
- MUST NOT automatically return without user direction
- MUST wait for user to decide next step

**Outputs:**
- Multiple `observe/research/*.md` files organized by topic
- Updated `summary.md` with research findings summary

**Troubleshooting - Research Limitations:**
- Document what information is missing
- Suggest alternative approaches
- Ask user for additional context
- Continue with available information

### Step 5: Iteration Checkpoint (Orient/Decide Transition)

**Purpose:** Ensure readiness before proceeding to design.

**Process:**
1. Summarize current state:
   - Requirements captured
   - Research findings
   - Open questions
2. Explicitly ask user if they want to:
   - Proceed to detailed design
   - Return to requirements clarification
   - Conduct additional research
3. Support iterating as many times as needed
4. Ensure both requirements and research are sufficient
5. Wait for explicit confirmation to proceed

**Critical Constraints:**
- MUST summarize to help user make informed decision
- MUST NOT proceed without explicit confirmation
- MUST support iteration between clarification and research

**Outputs:**
- User's decision on next step
- Updated `summary.md` (phase: decide if proceeding)

### Step 6: Create Detailed Design (Decide Phase)

**Purpose:** Develop comprehensive design document.

**Process:**
1. Create `decide/high-level-design.md` first (architecture overview)
2. Create `act/detailed-design.md` (complete specification)
3. Include required sections (see below)
4. Generate mermaid diagrams for key concepts
5. Consolidate all requirements from idea-honing.md
6. Include research findings appendix
7. Review with user
8. Iterate based on feedback
9. Explicitly ask if ready for implementation plan

**High-Level Design Structure:**
```markdown
# High-Level Design: [Feature Name]

## Architecture Overview
[Mermaid diagram showing major components]

## Major Components
- Component 1: Purpose and responsibilities
- Component 2: Purpose and responsibilities

## Key Decisions
1. Technology: [Choice] - Rationale: [Why]
2. Architecture: [Pattern] - Rationale: [Why]

## Data Flow
[Mermaid sequence diagram]

## Integration Points
- Existing System A
- Existing System B
```

**Detailed Design Structure:**
```markdown
# Detailed Design: [Feature Name]

## 1. Overview
[Standalone description - can be read without other files]

## 2. Detailed Requirements
[Consolidated from idea-honing.md]
- Functional Requirements
- Non-Functional Requirements
- Constraints

## 3. Architecture Overview
[Mermaid diagram with detailed components]

## 4. Components and Interfaces
### Component A
- Responsibilities
- Public Interface
- Dependencies
- Implementation Notes

## 5. Data Models
[Entity relationships, schemas, mermaid ER diagrams]

## 6. Error Handling
- Error types
- Recovery strategies
- User-facing messaging

## 7. Testing Strategy
- Unit testing approach
- Integration testing approach
- E2E testing approach
- Test coverage goals

## 8. Appendices

### A. Technology Choices
| Technology | Alternatives | Decision Rationale |
|------------|--------------|-------------------|
| React | Angular, Vue | Team expertise, ecosystem |

### B. Research Findings Summary
[Key insights from research phase]

### C. Alternative Approaches Considered
[Other options and why they were rejected]

### D. Constraints and Limitations
[Technical, time, resource constraints]
```

**Critical Constraints:**
- MUST write as standalone document (understandable without reading other files)
- MUST include all required sections
- MUST consolidate requirements from idea-honing.md
- MUST include research findings appendix
- MUST include mermaid diagrams for architectures and data flows
- MUST review with user and iterate
- MUST NOT proceed to implementation plan without confirmation
- MUST offer to return to requirements/research if gaps identified

**Outputs:**
- `decide/high-level-design.md`
- `act/detailed-design.md`
- Updated `summary.md` (phase: decide)

### Step 7: Develop Implementation Plan (Act Phase)

**Purpose:** Create actionable, step-by-step implementation guide.

**Process:**
1. Create `decide/to-do.md` with implementation checklist
2. Create `act/implementation-plan.md` with detailed steps
3. Follow specific instructions for step creation (see below)
4. Ensure each step is demoable
5. Sequence for core functionality early
6. Review with user

**Specific Instructions for Plan Creation:**

Convert the design into a series of implementation steps that build each component in a test-driven manner following agile best practices. Each step must result in working, demoable increment of functionality. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Each step builds on previous steps and ends with wiring things together. No hanging or orphaned code that isn't integrated.

**Implementation Plan Structure:**
```markdown
# Implementation Plan: [Feature Name]

## Implementation Checklist

- [ ] Step 1: [Brief description]
- [ ] Step 2: [Brief description]
- [ ] Step 3: [Brief description]
...

---

## Step 1: [Clear Objective Title]

**Objective:** [What this step accomplishes]

**Implementation Guidance:**
- Set up [infrastructure/component]
- Create [files/modules]
- Implement [specific functionality]

**Test Requirements:**
- Unit tests for [component]
- Integration test for [interaction]

**Integration:**
- Builds on: Initial setup
- Wires together: [Components]

**Demo:**
After this step, you should be able to:
- [Specific demoable functionality 1]
- [Specific demoable functionality 2]
Example: "Run the server and see 'Hello World' at http://localhost:3000"

---

## Step 2: [Next Objective]

[Same structure as Step 1]
```

**Step Requirements:**
- **Clear objective:** Each step begins with "Step N:" and clear title
- **Implementation guidance:** General approach (not excessive detail)
- **Test requirements:** What to test at this stage
- **Integration:** How it connects to previous work
- **Demo:** Explicit description of working functionality

**Sequencing Principles:**
- Core end-to-end functionality early (Step 1-3 should show basic flow)
- Incremental feature additions
- Test at each step
- No orphaned code (everything integrated)

**Critical Constraints:**
- MUST include checklist at top of plan.md
- MUST format as numbered steps ("Step N:")
- MUST ensure each step results in working, demoable functionality
- MUST sequence for core end-to-end functionality early
- MUST NOT include excessive detail (that's in design doc)
- MUST assume all context documents available during implementation
- MUST ensure checklist items correspond to steps

**Outputs:**
- `decide/to-do.md` with checklist
- `act/implementation-plan.md` with numbered steps
- Updated `summary.md` (phase: act, status: complete)

**Troubleshooting - Complexity Overload:**
- Break down into smaller components
- Focus on core functionality first
- Suggest phased approach
- Return to clarification to prioritize

### Step 8: Summarize and Present Results

**Purpose:** Provide complete overview and suggest next steps.

**Process:**
1. Create `summary.md` (if not already complete)
2. List all artifacts created
3. Provide brief design overview
4. Summarize implementation approach
5. Suggest next steps
6. Highlight areas needing refinement
7. Present to user

**Summary Structure:**
```markdown
---
status: complete
phase: act
domain: software
started: 2026-01-03T15:00:45Z
updated: 2026-01-03T18:45:23Z
---

# OODA Loop Summary: [Feature Name]

## Current Status
✅ **Complete** - Ready for implementation

## Artifacts Created

### Observation Phase
- `rough-idea.md` - Initial concept
- `observe/research/existing-code.md` - Current patterns
- `observe/research/technologies.md` - Framework options
- `observe/idea-honing.md` - Requirements Q&A (12 questions)

### Orientation Phase
- `observe/idea-honing.md` - Completed clarification

### Decision Phase
- `decide/to-do.md` - Implementation checklist
- `decide/high-level-design.md` - Architecture overview

### Action Phase
- `act/detailed-design.md` - Complete specifications
- `act/implementation-plan.md` - 15-step implementation guide

## Key Design Elements
- Template management CRUD operations
- Role-based access control
- Version control for templates
- Custom field validation
- Document generation engine

## Implementation Approach
15 incremental steps, test-driven development:
- Steps 1-3: Core data models and API endpoints
- Steps 4-7: Template CRUD operations
- Steps 8-11: Document generation
- Steps 12-15: Advanced features and deployment

## Next Steps
1. Review detailed design: `act/detailed-design.md`
2. Review implementation plan: `act/implementation-plan.md`
3. Begin implementation following checklist in `decide/to-do.md`
4. Demo working functionality after each step

## Areas for Further Refinement
- Performance testing strategy needs more detail
- Security audit should be scheduled after Step 10
- Consider additional error scenarios for custom fields
```

**Critical Constraints:**
- MUST list all artifacts
- MUST provide design overview
- MUST suggest next steps
- SHOULD highlight refinement areas

**Outputs:**
- Complete `summary.md`
- User ready to begin implementation

### Software-Specific Best Practices

**For Code Research (Observe):**
- Use `search_internal_code` to find existing patterns
- Document current architecture with mermaid diagrams
- Identify reusable components vs. new development
- Note technical debt that impacts design

**For Requirements (Orient):**
- Ask about edge cases early
- Clarify performance requirements
- Understand existing user workflows
- Identify integration touchpoints

**For Architecture (Decide):**
- Start with high-level components
- Define clear interfaces early
- Consider testing strategy upfront
- Document trade-offs explicitly

**For Implementation Planning (Act):**
- First step should validate core flow
- Test at every step
- Demo early and often
- No big-bang integrations

### Common Software Pitfalls

**Pitfall 1: Skipping Research**
```
❌ Assumption: "I'll just use React"
✅ Research: Compare React, Vue, Angular based on:
   - Team expertise
   - Ecosystem maturity
   - Performance needs
   - Build tooling
```

**Pitfall 2: Vague Requirements**
```
❌ Requirement: "It should be fast"
✅ Requirement: "API response time < 200ms for 95th percentile
                Template generation < 1s for 10-page documents"
```

**Pitfall 3: Over-Designing**
```
❌ Design: 50-page document with every possible feature
✅ Design: Core functionality MVP, future enhancements appendix
```

**Pitfall 4: Big-Bang Implementation**
```
❌ Plan: "Step 1: Build entire backend (2 weeks)"
✅ Plan: "Step 1: Single endpoint with database (2 hours, demoable)"
```

### Integration with Existing Development Practices

**With Agile:**
- OODA creates the "epic" planning
- Each implementation step becomes user stories
- Demos align with sprint reviews

**With TDD:**
- Implementation plan includes test requirements per step
- Red-Green-Refactor cycle within each step
- Tests validate integration, not just units

**With CI/CD:**
- Each step results in deployable increment
- Automated tests run on every integration
- Demo environments auto-update per step

**With Code Review:**
- Design doc reviewed before implementation starts
- Implementation plan reviewed for sequencing
- Code reviewed at each step completion

---

## Universal Principles Across Domains

### Consistent Patterns

**All domains follow:**
1. **Phased progression:** Observe → Orient → Decide → Act
2. **Artifact creation:** Externalize thinking into files
3. **Structured interaction:** One question at a time during Orient
4. **Checkpoint system:** summary.md tracks progress
5. **Iteration support:** Move between phases as needed

### Domain-Specific Adaptations

**What varies by domain:**
- Research topics and sources
- Clarification questions
- Design artifacts and formats
- Implementation/execution plans
- Success metrics and demos

### Choosing Your Domain

When OODA loop activates, determine domain by:
1. User's language and terminology
2. Rough idea content
3. Explicit user statement
4. Context of conversation

Update `summary.md` with domain field for context.

---

# Appendix: Domain Templates for Future Expansion

**Status:** The templates below provide frameworks for applying OODA to non-software domains. Section 1 (Software Development) is complete and production-ready. The templates below outline the structure for future detailed expansions.

---

## Template A: Strategy & Planning

### Overview

Apply OODA to business strategy, product planning, organizational design, and other strategic initiatives.

### When to Use for Strategy

**Trigger scenarios:**
- Developing business strategies
- Planning product roadmaps
- Designing organizational structures
- Creating go-to-market plans
- Strategic pivots or initiatives

### Strategy-Specific OODA Mapping

| OODA Phase | Strategy Activities | Key Artifacts |
|------------|-------------------|---------------|
| **Observe** | Market research, competitive analysis, customer insights, internal capabilities | research.md with market maps |
| **Orient** | SWOT analysis, stakeholder interviews, constraint identification, opportunity framing | idea-honing.md with strategic questions |
| **Decide** | Strategic options, trade-off analysis, resource allocation, success metrics | high-level-strategy.md with options |
| **Act** | Execution roadmap, milestones, responsibilities, measurement plan | strategy-plan.md with timeline |

### Key Differences from Software

**Focus:**
- Software: Technical implementation
- Strategy: Business outcomes

**Artifacts:**
- Software: Code, APIs, data models
- Strategy: Frameworks, roadmaps, OKRs

**Timeline:**
- Software: Weeks to months
- Strategy: Quarters to years

### Strategy Research Topics

- Market size and growth trends
- Competitive landscape and positioning
- Customer segments and needs
- Internal capabilities and gaps
- Resource availability
- Regulatory environment
- Technology trends impacting industry
- Partnership opportunities

### Strategy Clarification Questions

- What business outcomes are we trying to achieve?
- What are our competitive advantages?
- What constraints limit our options?
- How do we measure success?
- What stakeholders must be aligned?
- What risks are acceptable?
- What's our timeline?
- What resources are available?

### Strategy Design Outputs

- Strategic options analysis
- Recommended approach with rationale
- Resource requirements
- Risk assessment and mitigation
- Success metrics and KPIs
- Stakeholder alignment plan

*[Additional strategy-specific guidance would continue here]*

---

## Template B: Writing & Documentation

### Overview

Apply OODA to technical writing, content creation, documentation systems, and knowledge management.

### When to Use for Writing

**Trigger scenarios:**
- Creating comprehensive documentation
- Designing content strategies
- Building knowledge bases
- Writing technical specifications
- Planning content calendars

### Writing-Specific OODA Mapping

| OODA Phase | Writing Activities | Key Artifacts |
|------------|-------------------|---------------|
| **Observe** | Audience research, existing content audit, style guide review, competitor analysis | research.md with content inventory |
| **Orient** | Content structure, tone requirements, key messages, audience needs | idea-honing.md with content questions |
| **Decide** | Outline, section organization, examples to include, delivery format | content-outline.md with structure |
| **Act** | Writing plan, sections breakdown, review checkpoints, publication steps | writing-plan.md with schedule |

*[Additional writing-specific guidance would continue here]*

---

## Template C: Research & Analysis

### Overview

Apply OODA to academic research, market analysis, data investigation, and analytical projects.

### When to Use for Research

**Trigger scenarios:**
- Conducting academic research
- Performing market analysis
- Investigating data patterns
- Creating research reports
- Building analytical frameworks

### Research-Specific OODA Mapping

| OODA Phase | Research Activities | Key Artifacts |
|------------|-------------------|---------------|
| **Observe** | Literature review, data collection, expert interviews, source gathering | research.md with bibliography |
| **Orient** | Pattern identification, hypothesis formation, methodology selection | idea-honing.md with research questions |
| **Decide** | Research approach, analysis methods, validation criteria | research-design.md with methodology |
| **Act** | Research execution plan, analysis steps, reporting structure | analysis-plan.md with timeline |

*[Additional research-specific guidance would continue here]*

---

**End of Appendix**

Templates A-C provide the structural framework for future domain expansions. Each template would follow the detailed 8-step pattern established in Section 1 (Software Development), adapted for domain-specific needs, research topics, clarification questions, and success metrics.
