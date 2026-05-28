---
name: spec-writer
description: Use this skill when the user asks to "create a spec", "write a specification", "create a feature specification", "build a requirements document", "gather requirements", "develop user stories", "start discovery process", or mentions needing help with requirements analysis or product specification. Guides users through a structured discovery process where stories emerge from problem understanding rather than being predefined.
---

# Spec Writer

## Purpose

Guide users through creating complete, unambiguous feature specifications using a discovery-driven process. Unlike traditional requirements gathering that starts with predefined user stories, this skill helps stories emerge naturally from deep problem understanding. The resulting specification is comprehensive enough for implementation without further clarification.

## Core Philosophy

**Stories emerge from discovery, they don't precede it.**

Begin by understanding the problem space. Stories crystallize as understanding deepens through iterative exploration. Stories may split, merge, be added, or be revised as learning progresses—even after being written into the specification.

## When to Use This Skill

Use this skill when the user needs to:

- Transform a feature idea into a detailed specification
- Understand and document a problem before designing solutions
- Develop user stories through structured discovery
- Create implementation-ready requirements documentation
- Guide stakeholders through requirements clarification

## State Management Architecture

### The Compaction Mechanism

SPEC.md serves as the compaction mechanism. As user stories reach full clarity, they graduate from working state into the deliverable specification. STATE.md holds only in-flight work. SPEC.md is a living document—graduated stories can be revised when new information warrants it.

### Discovery Directory Structure

```
discovery/
├── SPEC.md            # Progressive deliverable (mutable)
├── STATE.md           # Working memory (current work)
├── OPEN_QUESTIONS.md  # Current blockers
└── archive/
    ├── DECISIONS.md   # Decision history
    ├── RESEARCH.md    # Research log
    ├── ITERATIONS.md  # Iteration summaries
    └── REVISIONS.md   # Changes to graduated stories
```

## Discovery Process Overview

### Phase 1: Problem Space Exploration

**Goal**: Understand the problem before proposing solutions.

**Activities**:
- Ask open-ended questions about the problem domain
- Research similar solutions and industry patterns
- Identify stakeholders and personas
- Map current state vs. desired state

**Outputs to STATE.md**:
- Problem statement (draft, iteratively refined)
- Identified personas
- Current vs. desired state comparison
- Emerging themes (proto-stories)

**Exit Criteria**:
- Core problem articulated in one paragraph
- Primary personas identified
- At least 2-3 proto-stories emerging from themes

### Phase 2: Story Crystallization

**Goal**: Transform themes into concrete, prioritized user stories.

Proto-stories become real stories when they have:
- A clear actor (persona)
- A clear goal
- A clear value proposition ("so that...")
- Sufficient shape to enable specific questions

**Activities**:
- Propose story candidates from emerged themes
- Collaborate with user to prioritize (P1, P2, P3...)
- Identify dependencies between stories
- Validate stories are independently valuable

**Outputs to STATE.md**:
- Story backlog with priorities
- Story dependency map
- Initial confidence assessment per story

**Exit Criteria**:
- User has agreed on initial story set and priorities
- Each story passes "independently testable" validation
- Ready to deep-dive on P1 story

### Phase 3: Story Development (Iterative)

**Goal**: Develop each story to graduation-ready clarity.

Work through stories by priority while remaining alert to:
- New stories emerging from questions
- Existing stories needing to split
- Stories that should merge
- Cross-cutting concerns affecting multiple stories

**Activities**:
- Deep-dive questions on focused story
- Story-specific research
- Draft acceptance scenarios
- Identify edge cases and requirements
- Validate with user

**Graduation Criteria** (per story):
- 100% confidence on story scope
- All blocking questions resolved
- Acceptance scenarios specific and testable
- Edge cases identified with defined handling
- Requirements extractable
- Success criteria measurable

**Graduation Protocol**:
1. Confirm with user: "Story [X] feels complete. Here's the summary: [brief]. Ready to graduate to SPEC.md?"
2. If yes: Write full story to SPEC.md, update STATE.md
3. Move to next priority story

### Phase 4: Continuous Refinement

**Reality**: Discovery doesn't end when a story graduates.

Later stories may reveal:
- Gaps in earlier stories
- Conflicting requirements
- Shared concerns not previously visible
- Edge cases spanning stories

**Process**:
- Flag when new information affects graduated stories
- Propose revisions to SPEC.md when warranted
- Log all revisions to archive/REVISIONS.md
- Re-confirm with user before modifying graduated work

**Revision Types**:
- **Additive**: New acceptance scenario, edge case, requirement
- **Modificative**: Changing existing scenario or requirement
- **Structural**: Story splits or merges

**All revisions require**:
- User confirmation before changing SPEC.md
- Entry in archive/REVISIONS.md
- Update to affected decision/research references

## Session Start Protocol

### Fresh Start (No existing discovery/)

1. **Enter Plan Mode** to design the discovery approach:
   - Use `EnterPlanMode` to plan the specification strategy
   - In plan mode, explore the problem space to understand scope
   - Design the discovery approach based on problem complexity
   - Exit plan mode with a structured approach ready

2. **Gather Initial Context** using AskUserQuestion:
   - Use AskUserQuestion to understand the problem domain
   - Ask about problem type, stakeholders, and constraints
   - Structured questions help identify the right discovery path

3. **Initialize Discovery Environment**:
   - Once you understand the problem and have identified an appropriate feature name, use `scripts/init-spec.sh <feature-name>` (Tier 1 Essential)
   - Navigate to the created discovery/ directory
   - Use TodoWrite to track Phase 1 objectives and next steps

4. **Continue with structured discovery** using the enhanced process below

### Resuming (Existing discovery/)

1. Read SPEC.md header + completed story count
2. Read STATE.md (in-flight work)
3. Read OPEN_QUESTIONS.md
4. **Use TodoWrite** to track current state:
   - Current phase and active story
   - Blocking questions requiring resolution
   - Stories ready for graduation
   - Watching items (revision risks)
5. Report current state:

"We're in Phase [X]. [N] stories completed, working on [Story Y]. [M] blocking questions. Any graduated stories at revision risk: [list]"

**Field Update Rules**: For exhaustive guidance on when to update each field and section, see `references/file-operations.md`.

## Question Management

### Question Categories

Track questions in OPEN_QUESTIONS.md by type using `add-question.py` (Tier 1 Essential):

- **🔴 Blocking**: Prevents progress on current story
- **🟡 Clarifying**: Needed for completeness, not blocking
- **🔵 Research Pending**: Requires investigation
- **🟠 Watching**: May affect graduated stories

Use `resolve-question.py` (Tier 2 Automation) to remove questions when answered.

### TodoWrite Integration

**CRITICAL**: Use TodoWrite at every major step to maintain visibility and track progress.

**Always track:**
- Current phase and phase objectives
- Active story being developed
- Blocking questions requiring user input
- Research tasks in progress
- Stories ready for graduation review
- Watching items (graduated story revision risks)
- Script executions in progress

**Update frequency:**
- Mark tasks in_progress before starting work
- Mark completed immediately after finishing
- Add new tasks as they emerge from discovery
- Keep exactly ONE task in_progress at a time

**Example todo structure:**
```
1. [in_progress] Deep-dive questions for Story 2 payment validation
2. [pending] Research industry payment validation patterns
3. [pending] Graduate Story 1 (authentication) after user confirmation
4. [pending] Review Story 3 for potential revision based on Story 2 findings
```

## System Tool Usage Patterns

### AskUserQuestion Patterns

**Use AskUserQuestion instead of free-text questions for:**

1. **Phase Transitions** - When moving between discovery phases:
   ```
   Question: "We've completed problem exploration. Ready to identify user stories?"
   Options:
   - "Yes, let's identify stories" (Recommended)
   - "Need more problem exploration"
   - "Want to review findings first"
   ```

2. **Story Prioritization** - Instead of listing all stories:
   ```
   Question: "Which story should we develop first?"
   Options:
   - "Story 1: User authentication (foundational)"
   - "Story 2: Payment processing (high value)"
   - "Story 3: Reporting dashboard (can wait)"
   ```

3. **Graduation Decisions** - Confirming story is ready:
   ```
   Question: "Story 2 appears complete. Ready to graduate to SPEC.md?"
   Options:
   - "Yes, graduate it" (Recommended)
   - "Need to review first"
   - "Missing something (explain what)"
   ```

4. **Revision Approval** - When graduated stories need changes:
   ```
   Question: "Story 1 needs revision based on Story 3 findings. Proceed?"
   Options:
   - "Yes, revise Story 1"
   - "Explain the conflict first"
   - "Handle it differently"
   ```

5. **Question Category Selection** - When adding questions:
   ```
   Question: "How should we categorize this question?"
   Options:
   - "🔴 Blocking - prevents progress"
   - "🟡 Clarifying - needed for completeness"
   - "🔵 Research Pending - requires investigation"
   - "🟠 Watching - may affect graduated stories"
   ```

6. **Problem Domain Exploration** - At session start:
   ```
   Question: "What type of problem are we solving?"
   Options:
   - "New feature for existing product"
   - "Replacing existing functionality"
   - "Entirely new product"
   - "Integration with external system"
   ```

**Benefits of AskUserQuestion:**
- Faster user response (click vs. type)
- Clear, structured choices
- Prevents ambiguous answers
- Easier to track decisions
- Better conversation flow

### Plan Mode Usage

**Use EnterPlanMode for:**

1. **Session Start Planning**:
   - Enter plan mode at the beginning of a new spec
   - Research similar features and industry patterns
   - Design the discovery approach
   - Identify likely story candidates early
   - Exit with structured plan for Phase 1

2. **Phase Transition Planning**:
   - Before moving from Phase 1 (exploration) to Phase 2 (story crystallization)
   - Before starting Phase 3 (story development) to prioritize work
   - Plan the approach for complex cross-cutting concerns

3. **Story Graduation Planning**:
   - Before graduating stories, enter plan mode to verify completeness
   - Check all acceptance scenarios are testable
   - Ensure edge cases are covered
   - Validate requirements are specific and measurable
   - Exit with confidence or identified gaps

4. **Revision Planning**:
   - When multiple graduated stories need coordinated revisions
   - For significant structural changes (story splits/merges)
   - To assess impact of cross-cutting changes
   - Exit with revision strategy and updated REVISIONS.md entries

**Plan Mode Best Practices:**
- Use read-only tools (Read, Grep, Glob) to explore without modifying
- Create thorough analysis before proposing changes
- Exit plan mode with clear, actionable recommendations
- Present plan to user with AskUserQuestion for approval

## Rules of Engagement

- **Problem before solution** - Understand problem space before structuring stories
- **Stories emerge** - Let them crystallize from understanding, don't assign them
- **Stories are mutable** - Even graduated work can be revised with new information
- **Graduation is not forever** - Flag and revise when later discovery reveals gaps
- **Always use system tools** - AskUserQuestion for decisions, EnterPlanMode for complex planning, TodoWrite for tracking
- **Always confirm changes** - Never modify SPEC.md without user approval via AskUserQuestion
- **Track everything** - Log decisions, research, revisions, and use TodoWrite for active work
- **Quantify everything** - Replace vague terms with specific numbers ("fast" → "under 200ms", "many" → "up to 10,000")
- **Challenge assumptions** - Question both your assumptions and the user's

## Completion Criteria

The specification is complete when:

- All identified stories graduated to SPEC.md
- No proto-stories remain in STATE.md
- OPEN_QUESTIONS.md is empty (including Watching list)
- All cross-cutting concerns addressed
- User confirms: "This spec captures everything"

### Final Deliverable Check

Before marking complete, verify:
- [ ] Every story independently testable
- [ ] Every acceptance scenario specific (no ambiguity)
- [ ] Every edge case has defined handling
- [ ] Every requirement is specific and measurable
- [ ] Every success criterion has numbers, not vibes
- [ ] Glossary captures all domain terms
- [ ] Run `validate-spec.py` (Tier 1) for final validation
- [ ] User has done final review and approved

## Context Recovery

### Standard Resume

1. Read SPEC.md header + story status markers
2. Read STATE.md
3. Read OPEN_QUESTIONS.md
4. Report current state and continue

### User Asks About Completed Story

1. Read that story section from SPEC.md
2. If context needed, search archive files

### User Wants to Restart or Revise

1. Confirm: "Do you want to revise specific stories, or restart discovery entirely?"
2. If restart: Archive current files, begin fresh
3. If revise: Identify what to reconsider, move back to appropriate phase

## Additional Resources

### Reference Files

For detailed templates and formats:

- **`references/file-templates.md`** - Manual operations reference showing what sections you must write manually vs what scripts handle. Focus on Problem Understanding, In-Progress Story Detail, and manual metadata updates.
- **`references/file-operations.md`** - Exhaustive field-level update rules, sync checkpoints, and cross-file consistency invariants. Reference when updating files to ensure all required fields are updated and cross-references maintained.
- **`references/phase-guide.md`** - Comprehensive phase-by-phase guidance with questioning strategies, research approaches, and transition criteria

### Example Files

Working examples in `examples/`:

- **`examples/sample-spec/`** - Complete example specification showing the discovery process from problem exploration through graduated stories

### Helper Scripts

The spec-writer skill includes 14 automation scripts in `scripts/` organized in four tiers by functionality.

**Script Organization**:

- **Tier 1: Essential Scripts** (6 scripts) - Initialization, question management, decision logging, validation
- **Tier 2: High-Value Automation** (4 scripts) - Story graduation, status updates, research search
- **Tier 3: Enhancement Scripts** (3 scripts) - Research logging, revisions, status monitoring
- **Tier 4: Specialized Tables** (3 scripts) - Edge cases, requirements, success criteria

**Quick Start**:
```bash
# Initialize new spec
scripts/init-spec.sh payment-flow-redesign
cd discovery

# Add question
../scripts/add-question.py \
  --question "Who are the primary users?" \
  --category clarifying

# Log decision
../scripts/log-decision.py \
  --title "Use REST API" \
  --context "Need API protocol" \
  --decision "REST with JSON" \
  --stories "Story 1, Story 2"

# Find decisions
../scripts/find-decisions.py --story 1

# Validate spec
../scripts/validate-spec.py
```

**Smart Directory Discovery**: All scripts automatically locate `discovery/` directory using:
1. Explicit `--discovery-path` flag
2. Current directory if in `discovery/`
3. Auto-locate in parent directories

**Script Reference Documentation**:

Read the appropriate tier reference based on your current task:

- **`references/scripts-tier-1.md`**