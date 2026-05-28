---
name: brainstorming
description: Refines rough ideas into epic Tasks with immutable requirements through Socratic questioning. Use before any creative work.
user_invokable: true
---

# Brainstorming Ideas Into Designs

## Overview

Turn rough ideas into validated designs stored as epic Tasks with immutable requirements. Tasks are created iteratively as you learn, not upfront.

**Core principle:** Ask questions to understand, research before proposing, document decisions for future reference.

**Announce at start:** "I'm using gambit:brainstorming to refine your idea into a design."

## Rigidity Level

HIGH FREEDOM - Adapt Socratic questioning to context. But always:
- Create immutable epic before code
- Create only first task (not full tree)
- Use AskUserQuestion tool for questions
- Run task refinement before handoff

## Quick Reference

| Step | Action | Deliverable |
|------|--------|-------------|
| 1 | Ask questions (one at a time) | Understanding of requirements |
| 2 | Research (Explore agent for codebase) | Existing patterns and approaches |
| 3 | Propose 2-3 approaches with trade-offs | Recommended option |
| 4 | Present design in sections (200-300 words) | Validated architecture |
| 5 | Create epic Task with IMMUTABLE requirements | Epic with anti-patterns |
| 6 | Create ONLY first subtask | Ready for executing-plans |
| 7 | Apply task refinement | Corner cases covered |
| 8 | Hand off to executing-plans | Iterative implementation begins |

**Key:** Epic = contract (immutable), Tasks = adaptive (created as you learn)

## When to Use

- User describes new feature to implement
- User has rough idea that needs refinement
- About to write code without clear requirements
- Need to explore approaches before committing
- Requirements exist but architecture unclear

**Don't use for:**
- Executing existing plans (use `gambit:execute-plan`)
- Fixing bugs (use `gambit:debug` when available)
- Refactoring (use `gambit:refactor` when available)
- Requirements already crystal clear and epic exists

## The Process

### 1. Understanding the Idea

**Check current state:**
- Recent commits, existing docs, codebase structure
- Use Explore agent for existing patterns

```
Task
  subagent_type: "Explore"
  prompt: "Find existing auth implementation patterns in this codebase"
```

**REQUIRED: Use AskUserQuestion tool with scannable format**

**Question Format Guidelines:**

1. **1-5 questions maximum** per round (don't overwhelm)
2. **Multiple choice preferred** with clear options
3. **Include suggested default** marked with "(Recommended)"
4. **Numbered for easy reference**
5. **Separate critical from nice-to-have**

**Question Structure:**
```
Question: [Clear question ending with ?]
Options:
  A. [Option] (Recommended) - [Why this is default]
  B. [Option] - [Trade-off]
  C. [Option] - [Trade-off]
  D. Other (please specify)

Priority: [CRITICAL | IMPORTANT | NICE_TO_HAVE]
```

**Priority Definitions:**
- **CRITICAL**: Must answer before proceeding (security, core functionality)
- **IMPORTANT**: Affects design significantly but has reasonable default
- **NICE_TO_HAVE**: Can defer to implementation phase

**Example using AskUserQuestion:**

```
AskUserQuestion
  questions:
    - question: "Where should OAuth tokens be stored?"
      header: "Token storage"
      options:
        - label: "httpOnly cookies (Recommended)"
          description: "Prevents XSS token theft, industry standard"
        - label: "sessionStorage"
          description: "Cleared on tab close, less persistent"
        - label: "localStorage"
          description: "Persists across sessions, XSS vulnerable"
      multiSelect: false
```

**Fast-Path Option:**
For IMPORTANT/NICE_TO_HAVE questions with good defaults, offer:
"Reply 'defaults' to accept all recommended options"

**Do NOT just print questions and wait for "yes"** - use the AskUserQuestion tool.

---

### 2. Exploring Approaches

**Research first:**
- Similar feature exists → Use Explore agent
- New integration → Use WebSearch or WebFetch
- Review findings before proposing

```
Task
  subagent_type: "Explore"
  prompt: "Find how authentication is currently implemented and what patterns are used"
```

**Propose 2-3 approaches with trade-offs:**

```
Based on [research findings], I recommend:

1. **[Approach A]** (recommended)
   - Pros: [benefits, especially "matches existing pattern"]
   - Cons: [drawbacks]

2. **[Approach B]**
   - Pros: [benefits]
   - Cons: [drawbacks]

3. **[Approach C]**
   - Pros: [benefits]
   - Cons: [drawbacks]

I recommend option 1 because [specific reason, especially codebase consistency].
```

**Lead with recommended option and explain why.**

---

### 3. Presenting the Design

**Once approach is chosen, present design in sections:**
- Break into 200-300 word chunks
- Ask after each: "Does this look right so far?"
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify

**Show research findings:**
- "Based on codebase investigation: auth/ uses passport.js..."
- "API docs show OAuth flow requires..."

---

### 4. Creating the Epic Task

**After design validated, create epic as immutable contract:**

```
TaskCreate
  subject: "Epic: [Feature Name]"
  description: |
    ## Requirements (IMMUTABLE)
    [What MUST be true when complete - specific, testable]
    - Requirement 1: [concrete requirement]
    - Requirement 2: [concrete requirement]
    - Requirement 3: [concrete requirement]

    ## Success Criteria (MUST ALL BE TRUE)
    - [ ] Criterion 1 (objective, testable - e.g., 'Integration tests pass')
    - [ ] Criterion 2 (objective, testable - e.g., 'Works with existing User model')
    - [ ] All tests passing
    - [ ] Pre-commit hooks passing

    ## Anti-Patterns (FORBIDDEN)
    - NO [Pattern 1] (reason: [why forbidden])
    - NO [Pattern 2] (reason: [why forbidden])

    ## Approach
    [2-3 paragraph summary of chosen approach]

    ## Architecture
    [Key components, data flow, integration points]

    ## Design Rationale

    ### Problem
    [1-2 sentences: what problem this solves, why status quo insufficient]

    ### Research Findings
    **Codebase:**
    - [file.ts:line] - [what it does, why relevant]
    - [pattern discovered, implications]

    **External:**
    - [API/library] - [key capability, constraint discovered]
    - [doc URL] - [relevant guidance found]

    ### Approaches Considered

    #### 1. [Chosen Approach] - CHOSEN
    **What it is:** [2-3 sentence description]
    **Investigation:** [What was researched]
    **Pros:** [benefits]
    **Cons:** [drawbacks]
    **Chosen because:** [specific reasoning]

    #### 2. [Rejected Approach] - REJECTED
    **What it is:** [2-3 sentence description]
    **Why explored:** [What made it seem viable]
    **Investigation:** [What was researched]
    **Pros:** [benefits]
    **Cons:** [fatal flaw]
    **REJECTED BECAUSE:** [specific reason]
    **DO NOT REVISIT UNLESS:** [condition that would change decision]

    ### Scope Boundaries
    **In scope:**
    - [explicit inclusions]

    **Out of scope:**
    - [explicit exclusions with reasoning]

    ### Open Questions
    - [uncertainties to resolve during implementation]
    - [decisions deferred to execution phase]

    ## Design Discovery (Optional - for complex features)
    Key decisions: [question] → [answer] → [implication]
    Dead-ends: [path] → [why abandoned]
    Concerns raised: [concern] → [resolution]
  activeForm: "Planning [feature name]"
```

**Critical:** Anti-patterns section prevents watering down requirements when blockers occur. Always include reasoning.

**Example anti-patterns:**
- NO localStorage tokens (reason: httpOnly prevents XSS token theft)
- NO new user model (reason: must integrate with existing db/models/user.ts)
- NO mocking OAuth in integration tests (reason: defeats purpose of testing real flow)

---

### 5. Creating ONLY First Task

**Create one task, not full tree:**

```
TaskCreate
  subject: "Add [specific deliverable]"
  description: |
    ## Goal
    [What this task delivers - one clear outcome]

    ## Implementation

    1. Study existing code
       [Point to 2-3 similar implementations: file.ts:line]

    2. Write tests first (TDD)
       [Specific test cases for this task]

    3. Implementation checklist
       - [ ] file.ts:line - function_name() - [what it does]
       - [ ] test.ts:line - test_name() - [what it tests]

    ## Success Criteria
    - [ ] [Specific, measurable outcome]
    - [ ] Tests passing
    - [ ] Pre-commit hooks passing
  activeForm: "Adding [deliverable]"
```

**Link task to epic using metadata or description reference.**

The subtask is part of the epic. Epic stays in_progress while subtasks execute.

**Why only one task?**
- Subsequent tasks created iteratively by executing-plans
- Each task reflects learnings from previous
- Avoids brittle task trees that break when assumptions change

---

### 6. Apply Task Refinement

**REQUIRED: Before handoff, verify first task passes these criteria:**

1. **Is it 2-5 minutes of work?** (If longer, break down)
2. **Can it be executed without asking questions?** (All info present)
3. **Are all file paths explicit?** (No searching required)
4. **Are success criteria specific and testable?** (At least 3 criteria)

**Corner-case analysis checklist:**
- [ ] What happens if the happy path fails?
- [ ] What are the edge cases for inputs?
- [ ] What happens on network/IO failures?
- [ ] What happens on concurrent access?
- [ ] What happens with empty/null/missing data?
- [ ] What are the security implications?
- [ ] What happens at boundaries (max size, timeout)?

If task fails any check, update it with missing details before proceeding.

---

### 7. Documentation (Optional but Recommended)

**Write validated design to docs:**

```bash
# Create design document
# File: docs/plans/YYYY-MM-DD-<topic>-design.md
```

Include:
- Problem statement
- Chosen approach with rationale
- Architecture overview
- Key decisions made
- Anti-patterns to avoid

**Commit the design document** before starting implementation.

---

### 8. Handoff

**After refinement complete, present handoff:**

```
Epic Task created with immutable requirements and success criteria.
First task is ready to execute and has been refined.

Ready to start implementation? I'll use gambit:execute-plan to work through this iteratively.

The executing-plans skill will:
1. Execute the current task
2. Review what was learned against epic requirements
3. Create next task based on current reality
4. Repeat until all epic success criteria met

This approach avoids brittle upfront planning - each task adapts to what we learn.
```

## Research Protocol

1. Codebase pattern exists → Use it (Explore agent)
2. No codebase pattern → Research external patterns (WebSearch)
3. Research yields nothing → Ask user for direction

## Examples

### Bad: Creating Full Task Tree Upfront

```
TaskCreate subject: "Epic: Add OAuth"
TaskCreate subject: "Task 1: Configure OAuth"
TaskCreate subject: "Task 2: Implement token exchange"
TaskCreate subject: "Task 3: Add refresh logic"
TaskCreate subject: "Task 4: Create middleware"
TaskCreate subject: "Task 5: Add UI components"
TaskCreate subject: "Task 6: Write tests"

# Starts Task 1
# Discovers library handles refresh automatically
# Now Task 3 is wrong
# Discovers middleware exists
# Now Task 4 is wrong
# Task tree brittle to reality
```

**Why it fails:**
- Assumptions prove wrong as you learn
- Task tree becomes incorrect
- Wastes time updating/deleting wrong tasks

### Good: Iterative Task Creation

```
TaskCreate subject: "Epic: Add OAuth" [with immutable requirements]
TaskCreate subject: "Task 1: Configure OAuth provider"

# Execute Task 1
# Learn: library handles refresh, middleware exists

TaskCreate subject: "Task 2: Integrate with existing middleware"
# Created AFTER learning from Task 1

# Execute Task 2
# Learn: UI needs OAuth button

TaskCreate subject: "Task 3: Add OAuth button to login"
# Created AFTER learning from Task 2
```

**Why it works:**
- Tasks reflect current reality
- No wasted time fixing wrong plans
- Epic requirements stay immutable

### Bad: Epic Without Anti-Patterns

```
TaskCreate
  subject: "Epic: OAuth Authentication"
  description: |
    ## Requirements
    - Users authenticate via Google OAuth2
    - Tokens stored securely

    ## Success Criteria
    - [ ] Login flow works
    - [ ] Tokens secured
```

**Why it fails:**
- No explicit forbidden patterns
- Agent rationalizes shortcuts when blocked
- "Tokens stored securely" too vague
- Mocking defeats the purpose of integration tests

### Good: Follow the Template in Section 4

See the epic template in "Creating the Epic Task" above. Key elements that make it work:
- Requirements are concrete and specific
- Forbidden patterns explicit with reasoning
- Rejected approaches documented with "DO NOT REVISIT UNLESS"
- Design Discovery preserves context for obstacle handling

## Critical Rules

1. **Use AskUserQuestion tool** → Don't just print questions and wait
2. **Research BEFORE proposing** → Use Explore agent to understand context
3. **Propose 2-3 approaches** → Don't jump to single solution
4. **Epic requirements IMMUTABLE** → Tasks adapt, requirements don't
5. **Include anti-patterns section** → Prevents watering down requirements
6. **Create ONLY first task** → Subsequent tasks created iteratively
7. **Apply task refinement** → Before handoff to executing-plans

**Common rationalizations (all mean STOP, follow the process):**
- "Requirements obvious" → Questions reveal hidden complexity
- "I know this pattern" → Research might show better way
- "Can plan all tasks upfront" → Plans become brittle as you learn

## Verification Checklist

Before handing off to executing-plans:

- [ ] Used AskUserQuestion tool for clarifying questions
- [ ] Researched codebase patterns (Explore agent)
- [ ] Proposed 2-3 approaches with trade-offs
- [ ] Presented design in sections, validated each
- [ ] Created epic Task with all sections
- [ ] Requirements are IMMUTABLE and specific
- [ ] Anti-patterns include reasoning
- [ ] Approaches Considered shows rejected options with DO NOT REVISIT
- [ ] Design Discovery section captures Q&A, research, dead-ends
- [ ] Created ONLY first task (not full tree)
- [ ] First task has detailed implementation checklist
- [ ] Applied task refinement (2-5 min, explicit paths, testable criteria)

## Integration

**Calls:** Explore agent, then hands off to `gambit:executing-plans`
