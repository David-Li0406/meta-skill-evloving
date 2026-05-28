# PRD Creation Skill - Comprehensive Reference

This document is the comprehensive reference for the PRD creation skill. Read this when you need deep understanding of any aspect of PRD creation.

## Table of Contents

1. [Philosophy and Principles](#philosophy-and-principles)
2. [Interview Methodology](#interview-methodology)
3. [Category Deep Dives](#category-deep-dives)
4. [Story Structure Patterns](#story-structure-patterns)
5. [Verification Philosophy](#verification-philosophy)
6. [Agent Browser CLI Mastery](#agent-browser-cli-mastery)
7. [Decision-Making Frameworks](#decision-making-frameworks)
8. [Common Pitfalls](#common-pitfalls)
9. [Advanced Patterns](#advanced-patterns)

---

# Philosophy and Principles

## The Purpose of a PRD

A PRD is not documentation - it's an execution plan. The goal is to create a document that enables an AI agent (or human) to complete the work autonomously with minimal interruption.

A good PRD:
- Provides enough context to make informed decisions
- Breaks work into verifiable chunks
- Anticipates problems and provides guidance
- Enables autonomous execution with clear checkpoints
- Includes verification at every stage

A bad PRD:
- Lists features without explaining why
- Has vague acceptance criteria ("it should work")
- Assumes knowledge the executor doesn't have
- Batches unrelated work together
- Skips verification steps

## Thinking Independently

These guidelines are tools, not rules. You have intelligence - use it.

**When to follow guidelines closely:**
- You're unfamiliar with the task type
- The stakes are high (production systems, security)
- The user seems uncertain about what they want

**When to adapt or deviate:**
- The guidelines don't fit the specific situation
- You have relevant experience that suggests a better approach
- The user has clear preferences that differ

**Always:**
- Explain your reasoning when you deviate
- Be willing to adjust based on user feedback
- Prioritize the user's actual goals over process compliance

## Principles Over Prescriptions

We provide mental models, not scripts. Here's the difference:

**Prescription (avoid):**
"In round 1, ask about scope. In round 2, ask about user flows. In round 3, ask about data requirements."

**Principle (prefer):**
"Build a complete mental model of what needs to exist. Ask questions until you understand the spec, dependencies, and implementation path. The number of rounds depends on complexity."

The prescription tells you what to do. The principle tells you what to think about.

---

# Interview Methodology

The interview is the foundation of a good PRD. Your job is to extract enough information to create a comprehensive, executable plan.

## Mental Model for Interviewing

Think of the interview as building a mental model with four layers:

```
Layer 4: Verification - How do we know it works?
Layer 3: Implementation - How do we build it?
Layer 2: Dependencies - What do we need first?
Layer 1: Specification - What exactly are we building?
```

Start at Layer 1 and work up. Don't discuss implementation until you understand the spec. Don't discuss verification until you understand implementation.

## Information Gathering Principles

### The Brain Dump Phase

The brain dump is about removing friction. Let the user share information in whatever way is natural for them.

**Your mindset:** "Help me understand everything you know about this."

**What you're listening for:**
- The core problem or goal
- Context they assume you know
- Constraints they mention casually
- Excitement or concern in their language
- References to other systems, files, or people

**What to avoid:**
- Interrupting with clarifying questions too early
- Imposing structure on their thinking
- Showing impatience with tangential information
- Dismissing "irrelevant" details (they might be important)

**Good prompts:**
- "Tell me everything about this project"
- "What's the backstory here?"
- "Walk me through what you're imagining"
- "What else should I know?"

### The Clarifying Questions Phase

After the brain dump, you have raw material. Now you need to refine it.

**Your mindset:** "What do I still not understand? What assumptions might be wrong?"

**Types of questions:**
1. **Gap-filling** - "You mentioned X but not Y. How does Y fit in?"
2. **Assumption-challenging** - "You said users will do X. Have you validated that?"
3. **Edge-case exploring** - "What happens if X fails? What about users who..."
4. **Scope-clarifying** - "Is X in scope for this work, or a future enhancement?"
5. **Priority-establishing** - "If you had to cut something, what would it be?"

**Question Formulation Guidelines:**

One topic at a time. Don't ask:
- "What's the scope, and also how should error handling work, and what about mobile?"

Instead ask:
- "Let's nail down scope first. What's definitely in vs. definitely out?"

Use multiple choice when helpful. Don't ask:
- "How should authentication work?"

Instead ask:
- "For authentication, should we: (A) use existing auth system, (B) implement OAuth, (C) simple API keys, or (D) something else?"

Build on answers. Don't treat each question as independent. If they say "we need to support mobile," follow up with mobile-specific questions.

Challenge assumptions gently. Don't say:
- "That won't work."

Instead say:
- "Interesting. I want to make sure I understand - you're assuming X because of Y. Is that accurate? Have you considered Z?"

### Knowing When to Stop

Stop asking questions when:
- You can confidently outline the work
- Additional questions would be diminishing returns
- The user is getting fatigued
- You're asking about implementation details you can figure out yourself

Don't stop when:
- You have significant gaps in understanding
- The scope is still fuzzy
- You're making assumptions you haven't validated
- Critical decisions haven't been made

**The test:** Could you write a detailed PRD right now that wouldn't require significant revision? If yes, stop. If no, keep asking.

## Confirmation

Before generating, present your understanding in a structured way:

1. **Problem Statement** - What problem are we solving? For whom?
2. **Proposed Solution** - What will we build?
3. **Scope** - What's in? What's explicitly out?
4. **Approach** - High-level phases and key decisions
5. **Verification** - How will we know it works?

Get explicit approval. "Does this match your expectations?" is not enough. Ask:
- "Is anything missing from this understanding?"
- "Is anything here that shouldn't be?"
- "Do the phases make sense in this order?"
- "Is the verification approach sufficient?"

If they have changes, incorporate them and re-present. Don't start generating until you have clear approval.

---

# Category Deep Dives

Each task category has a different mental model and workflow emphasis. These are thinking frameworks to inform your approach.

## Feature Development

### Mental Model

Feature development is about translation: from idea → spec → code → verification.

```
Idea: "Users should be able to export data"
           ↓
Spec: What formats? What data? Where does button go? What happens during export?
           ↓
Implementation: UI component, export logic, file generation, download trigger
           ↓
Verification: Export works for all formats, handles large data, UI is intuitive
```

### Key Principles

**Start with specification:** Before implementation details, understand exactly what should exist. What screens? What components? What behaviors? What data flows?

**Map dependencies:** Features rarely exist in isolation. What needs to exist first? What might this break? What patterns should this follow?

**Implement incrementally:** Don't build the whole thing and then test. Build piece by piece, verifying each piece works.

**Verify against spec:** The final check is always "does this match what we said we'd build?" Use Agent Browser CLI to visually confirm.

### What to Extract from Users

- Complete specification of the feature
- Current state vs. desired state
- UI/UX expectations (mockups, references, descriptions)
- Data requirements and sources
- Integration points with existing systems
- Performance expectations
- Edge cases and error scenarios

### Red Flags

- Starting implementation without clear spec
- Building multiple things before testing any
- Skipping browser verification for UI work
- Assuming you know what the user wants without confirming

## Bug Fixing

### Mental Model

Bug fixing is investigation work. You're a detective, not a repairman.

```
Report: "Login doesn't work"
           ↓
Clarify: What exactly happens? Error message? Blank screen? Wrong redirect?
           ↓
Reproduce: Follow exact steps to see the bug yourself
           ↓
Investigate: Why is this happening? Find the root cause.
           ↓
Fix: Make minimal, targeted changes
           ↓
Verify: Same steps, bug is gone, nothing else broke
```

### Key Principles

**Understand expected vs. actual:** Before investigating, be crystal clear on what should happen vs. what is happening.

**Reproduce first:** You cannot fix what you cannot see. Establish exact reproduction steps before touching code.

**No speculation:** Don't guess at the cause. Investigate until you find it. Add logging, use debugger, trace the code path.

**Minimal fixes:** Change only what's necessary. Don't refactor surrounding code. Don't add "improvements."

**Verify thoroughly:** Use the same reproduction steps to confirm the fix. Run related tests. Check for regressions.

### What to Extract from Users

- Exact reproduction steps
- Expected behavior vs. actual behavior
- When it started happening (recent changes?)
- Environment details (browser, OS, user type)
- Frequency (always, sometimes, specific conditions)
- Error messages or logs
- Impact and urgency

### Red Flags

- "Let me just try this and see if it works"
- Making changes without reproducing the bug
- Can't explain why the fix should work
- Multiple unrelated changes in one fix
- Not testing with original reproduction steps

## Research & Planning

### Mental Model

Research is about reducing uncertainty. You start with unknowns and end with a plan.

```
Unknown: "How should we implement real-time features?"
           ↓
Requirements: What exactly do we need? Latency? Scale? Complexity?
           ↓
Exploration: What exists? Libraries? Patterns? Similar implementations?
           ↓
Evaluation: Which options meet our requirements? Trade-offs?
           ↓
Recommendation: This is what we should do and why
           ↓
Plan: Here's how to implement it
```

### Key Principles

**Requirements first:** Document what you need before exploring solutions. Otherwise you'll chase shiny objects.

**Assume it exists:** Whatever you're trying to build, someone has probably done it. Find their work first.

**Minimum effort:** The best solution uses existing tools, requires minimal code, and builds on proven patterns.

**Deep exploration:** Spend most of your time exploring, not deciding. Look at multiple options, read documentation, try things out.

**Document findings:** Your research is valuable. Document what you learned, not just your recommendation.

### What to Extract from Users

- Clear statement of what we're trying to learn/decide
- Constraints (budget, time, team skills, existing systems)
- How the results will be used
- Success criteria for the research itself
- Specific questions that need answers
- Known options or starting points

### Deliverables

Research tasks should produce:
1. **Requirements document** - What we need, why, constraints
2. **Research findings** - What exists, what we learned
3. **System design** - Recommended approach with architecture
4. **Implementation plan** - How to build it

### Red Flags

- Jumping to solutions without exploring options
- Not documenting findings
- Ignoring existing tools/libraries
- Over-engineering when simple solutions exist
- Analysis paralysis (research forever without deciding)

## Quality Assurance

### Mental Model

QA is about finding problems before users do. You're adversarial - try to break things.

```
Codebase: Existing code with potential issues
           ↓
Scan: Automated tools, code review, pattern analysis
           ↓
Test: Write tests, run tests, manual testing
           ↓
Review: Code quality, optimization opportunities
           ↓
Report: What was found, severity, recommendations
```

### Key Principles

**Multiple angles:** Use static analysis, automated tests, manual testing, and code review. Each catches different problems.

**Think like an attacker:** For security, ask "how would I exploit this?" Test input validation, authentication, authorization.

**Think like a confused user:** For UX, ask "what might confuse someone?" Test edge cases, error states, unexpected flows.

**Prioritize by impact:** Not all issues are equal. Critical security bugs > performance issues > code style.

**Browser verification for UI:** Use Agent Browser CLI to test actual user flows, not just code paths.

### What to Extract from Users

- What areas should be focused on (security, performance, correctness)
- Known problem areas or concerns
- Risk tolerance (how thorough should we be?)
- What tests already exist
- Success criteria (all tests pass? security audit clean?)

### QA Approaches by Focus

| Focus | Key Activities |
|-------|----------------|
| Security | Input validation, auth flows, dependency vulnerabilities, OWASP top 10 |
| Performance | Profiling, load testing, bundle analysis, render optimization |
| Correctness | Unit tests, integration tests, edge cases, regression tests |
| Code quality | Patterns, readability, maintainability, documentation |

### Red Flags

- Only testing happy paths
- Ignoring UI/UX issues because "code works"
- Not prioritizing findings
- Testing without clear criteria for "done"

## Maintenance

### Mental Model

Maintenance is about health and hygiene. Keep the codebase clean and working.

```
Codebase: Accumulated code over time
           ↓
Review: Git history, current state, documentation
           ↓
Identify: Stale code, outdated patterns, documentation gaps
           ↓
Clean: Delete unused code, update patterns, improve docs
           ↓
Verify: Nothing broke, tests pass, docs are accurate
```

### Key Principles

**Understand before changing:** Read git history. Understand why things are the way they are before changing them.

**Delete more than you add:** The best maintenance removes complexity. Delete unused code, simplify patterns.

**One change at a time:** Don't batch unrelated changes. Each change should be verifiable independently.

**Preserve behavior:** Unless explicitly changing functionality, the system should work the same after maintenance.

**Test after each change:** Verify nothing broke before moving to the next change.

### What to Extract from Users

- Goals for the maintenance work
- Areas of concern or known technical debt
- What should NOT be changed
- Testing requirements
- Documentation needs

### Red Flags

- Changing things "because they're ugly" without clear benefit
- Batching unrelated changes
- Deleting code without verifying it's unused
- Not testing after changes
- Refactoring for hypothetical future needs

## DevOps

### Mental Model

DevOps is about reliable delivery. Changes to infrastructure and deployment are high-stakes.

```
Goal: Change to deployment, CI/CD, or infrastructure
           ↓
Plan: Detailed steps, rollback plan, verification steps
           ↓
Test: Validate plan in safe environment
           ↓
Execute: Implement with monitoring
           ↓
Verify: Confirm everything works
           ↓
Document: Record what was done
```

### Key Principles

**Plan completely before executing:** DevOps changes can be hard to reverse. Plan every step.

**Always have rollback:** Every change should be reversible. Document how to roll back.

**Test before production:** If possible, test in staging or similar environment first.

**Monitor during execution:** Watch metrics and logs while making changes.

**Stop on problems:** If something goes wrong, stop immediately. Don't push through.

**Document everything:** Future you (or someone else) needs to understand what was done.

### What to Extract from Users

- Exact goal of the DevOps work
- Current state of infrastructure/deployment
- Risk tolerance and rollback requirements
- Testing environment availability
- Monitoring and alerting setup
- Human availability during execution

### Non-Negotiables

- Rollback plan exists and is tested
- Monitoring is in place
- Human can be reached if problems occur
- Changes are documented

### Red Flags

- "Let's just try it and see"
- No rollback plan
- No monitoring during execution
- Batching unrelated infrastructure changes
- Working on production without testing first

## General

For tasks that don't fit other categories, apply fundamental principles:

1. **Understand before implementing** - Don't start work until you understand the goal
2. **Break into verifiable chunks** - Each piece should be independently testable
3. **Verify as you go** - Don't batch all verification at the end
4. **Document what you did** - Enable future understanding

Adapt your approach based on what the task actually requires.

---

# Story Structure Patterns

Stories are the building blocks of a PRD. Each story should be a coherent unit of work.

## Anatomy of a Good Story

### Title
Short, descriptive, action-oriented.
- Good: "Implement user authentication flow"
- Bad: "Auth stuff"

### Description
What and why, not how. The executor should understand the purpose.
- Good: "Users need to log in to access protected features. This story implements the authentication UI and connects it to the existing auth service."
- Bad: "Add login page."

### Tasks
Step-by-step instructions. Each task should be independently completable.
- Good: "1. Read the existing auth service implementation in src/services/auth.ts"
- Good: "2. Create login form component following existing form patterns"
- Bad: "1. Build the login feature"

### Acceptance Criteria
Specific, verifiable conditions. When all are met, the story is done.
- Good: "User can enter email and password and submit the form"
- Good: "Invalid credentials display appropriate error message"
- Bad: "Login works correctly"

### Notes
File paths, patterns to follow, warnings, context.
- Good: "Follow the existing form patterns in src/components/forms/"
- Good: "WARNING: The auth service returns different error codes for invalid email vs invalid password"

## Story Types

### Context Gathering Story
First story of a phase. Establishes understanding before implementation.

**Pattern:**
```
Title: Understand [area] before implementing
Description: Before implementing, we need to understand the current state and establish our approach.
Tasks:
  - Read and understand [relevant files]
  - Document current state and patterns
  - Plan specific approach for this phase
Acceptance Criteria:
  - Understanding is documented
  - Approach is clear
  - Ready to implement
```

### Implementation Story
The actual work of building something.

**Pattern:**
```
Title: Implement [specific thing]
Description: [What we're building and why it matters]
Tasks:
  - [Specific implementation steps]
  - [Include verification within implementation]
Acceptance Criteria:
  - [Specific, verifiable conditions]
Notes: [File paths, patterns, warnings]
```

### Checkpoint Story
End of phase verification. Ensures everything works before continuing.

**Pattern:**
```
Title: Verify phase [N] completion
Description: Ensure all phase [N] work is complete and working before continuing.
Tasks:
  - Run all tests related to [area]
  - Verify [specific functionality] works
  - Document any issues or learnings
  - Commit work with descriptive message
Acceptance Criteria:
  - All tests pass
  - [Specific verification criteria]
  - Work is committed
```

### Browser Verification Story
For UI work. Visual and interactive verification.

**Pattern:**
```
Title: Verify [feature] in browser
Description: Visual and interactive verification of [feature].
Tasks:
  - Start development server
  - Use Agent Browser CLI to navigate to [page]
  - Verify [visual elements] appear correctly
  - Test [interactions]
  - Screenshot key states for documentation
Acceptance Criteria:
  - [Specific visual criteria]
  - [Specific interaction criteria]
```

### Final Validation Story
End of PRD. Comprehensive verification.

**Pattern:**
```
Title: Final validation and completion
Description: Comprehensive verification that all work is complete and working.
Tasks:
  - Run full test suite
  - Run build process
  - Verify all acceptance criteria from all stories
  - Document completion
Acceptance Criteria:
  - All tests pass
  - Build succeeds
  - All features work as specified
```

### Report Story
Document what was done.

**Pattern:**
```
Title: Document completion and findings
Description: Create summary of work completed, decisions made, and any issues encountered.
Tasks:
  - Summarize work completed
  - Document key decisions and reasoning
  - Note any issues or follow-up needed
  - Update relevant documentation
Acceptance Criteria:
  - Summary is clear and complete
  - Decisions are explained
  - Follow-up items are captured
```

## Story Dependencies

Stories can depend on other stories. Use `dependsOn` to express this.

**Principles:**
- Only depend on what you actually need
- Avoid circular dependencies
- Keep dependency chains short
- Context gathering stories have no dependencies
- Implementation stories depend on context gathering
- Checkpoint stories depend on implementation stories

---

# Verification Philosophy

Verification is not an afterthought. It's woven throughout the PRD.

## Levels of Verification

### Minimal
For low-risk work like research or documentation.
- Accuracy check
- Spelling/grammar for docs

### Light
For simple changes with low impact.
- Type checking
- Linting
- Quick manual review

### Standard
For most implementation work.
- Type checking
- Linting
- Related unit tests
- Manual verification

### Heavy
For complex or risky changes.
- All of standard, plus:
- Integration tests
- Cross-browser/platform testing
- Performance verification

### Full
For checkpoints and final validation.
- Complete test suite
- Full build process
- End-to-end verification
- Browser verification for UI

## When to Use Each Level

| Situation | Level |
|-----------|-------|
| Documentation update | Minimal |
| Config change | Light |
| Bug fix | Standard |
| New feature | Standard to Heavy |
| Phase checkpoint | Full |
| Security-related | Heavy |
| Final validation | Full |

## Browser Verification

For any UI work, browser verification is mandatory. This is not optional.

**What to verify:**
- Visual appearance matches design
- Interactive elements work
- Data displays correctly
- Error states appear when expected
- Loading states are appropriate
- Responsive behavior (if applicable)

**How to verify:**
Use Agent Browser CLI throughout development, not just at the end.

---

# Agent Browser CLI Mastery

Agent Browser CLI is your primary tool for visual and interactive verification.

## Core Philosophy

Browser verification should be continuous, not just final. Check your work as you build.

## When to Use

| Category | When to Use Agent Browser CLI |
|----------|------------------------------|
| Feature Development | During implementation, after each component, final validation |
| Bug Fixing | Reproduce bug, verify fix, check for regressions |
| Research | Explore documentation, validate approaches, see examples |
| QA | Test user flows, visual verification, interactive testing |
| Maintenance | Verify UI still works after refactoring |

## Command Reference

### Session Management
```bash
# Start a session
agent-browser open http://localhost:3000

# Navigate to page
agent-browser navigate http://localhost:3000/login

# Close session
agent-browser close
```

### Element Discovery
```bash
# Get all interactive elements with IDs
agent-browser snapshot -i

# Get full page snapshot
agent-browser snapshot
```

### Interaction
```bash
# Click element by ID
agent-browser click @e5

# Click element by selector
agent-browser click "[data-testid='submit']"

# Fill input
agent-browser fill "[name='email']" "test@example.com"

# Select from dropdown
agent-browser select "[name='country']" "US"

# Press key
agent-browser press Enter
```

### Verification
```bash
# Take screenshot
agent-browser screenshot verification.png

# Get page content
agent-browser content

# Check element exists
agent-browser exists "[data-testid='success-message']"
```

## Patterns by Task Type

### Feature Development Pattern
```bash
# 1. Start dev server and open browser
agent-browser open http://localhost:3000/feature-page

# 2. Get interactive elements
agent-browser snapshot -i

# 3. Test interaction
agent-browser click @e5
agent-browser fill "[name='input']" "test data"
agent-browser click "[type='submit']"

# 4. Verify result
agent-browser screenshot after-submit.png
agent-browser exists "[data-testid='success']"

# 5. Clean up
agent-browser close
```

### Bug Reproduction Pattern
```bash
# 1. Open the problematic page
agent-browser open http://localhost:3000/buggy-page

# 2. Follow reproduction steps
agent-browser click @e3
agent-browser fill "[name='field']" "trigger value"
agent-browser click "[type='submit']"

# 3. Screenshot the bug
agent-browser screenshot bug-state.png

# 4. After fix, same steps should work
# ... repeat steps 2-3, should see different result
```

### Research Pattern
```bash
# 1. Open documentation
agent-browser open https://docs.example.com/api

# 2. Navigate to relevant section
agent-browser click "[href='/api/authentication']"

# 3. Capture content
agent-browser content > auth-docs.txt
agent-browser screenshot auth-docs.png
```

---

# Decision-Making Frameworks

## When to Ask vs. Decide

| Situation | Action |
|-----------|--------|
| Multiple valid approaches with significant trade-offs | Ask user |
| Implementation detail with one clearly better option | Decide |
| Scope question (in or out?) | Ask user |
| Technical choice within scope | Decide |
| Unclear requirement | Ask user |
| Obvious next step | Decide |

## Scope Decisions

**Include in scope:**
- Explicitly requested features
- Necessary dependencies of requested features
- Essential error handling
- Basic verification

**Exclude from scope:**
- "Nice to have" features not requested
- Optimizations beyond requirements
- Future-proofing for hypothetical needs
- Refactoring unrelated code

## Quality vs. Speed Trade-offs

When time pressure exists, prioritize:
1. Core functionality working
2. Critical error handling
3. Basic tests for main paths
4. Documentation of known limitations

Don't sacrifice:
- Security
- Data integrity
- User-facing error handling

## Technical Choices

When choosing between options:
1. Does one have clear technical advantages?
2. Does the team/codebase have an existing pattern?
3. Is one more maintainable long-term?
4. Is one significantly simpler?

Prefer simpler solutions. Prefer existing patterns. Prefer boring technology.

---

# Common Pitfalls

## Interview Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Leading questions | You bias the answer | Ask open-ended questions first |
| Information overload | User gets overwhelmed | One topic at a time |
| Stopping too early | Incomplete understanding | Test: Can you write the PRD? |
| Asking forever | User fatigue | Know when you have enough |
| Ignoring non-answers | Gaps in requirements | Notice and probe "I don't know" |

## PRD Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Vague acceptance criteria | Can't verify completion | Make criteria specific and measurable |
| Missing dependencies | Stories can't be executed | Map dependencies before writing |
| Too many stories | Overhead exceeds value | Combine related small stories |
| Too few stories | Each story is too large | Break down into verifiable chunks |
| No verification stories | Quality issues at end | Include verification throughout |

## Implementation Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Skipping context gathering | Misunderstanding leads to rework | Always start by reading and understanding |
| Batching verification | Problems compound | Verify after each story |
| Over-engineering | Wasted effort | Build only what's needed |
| Under-testing | Bugs escape | Include verification in every story |
| Not using browser | UI issues missed | Browser verify all UI work |

---

# Advanced Patterns

## Multi-Phase PRDs

For large projects, organize into phases with clear boundaries.

**Phase structure:**
- Each phase has a clear objective
- Phases end with checkpoint stories
- Later phases can depend on earlier phases
- Each phase is independently shippable (if possible)

**Example:**
```
Phase 1: Foundation
  - Set up project structure
  - Implement core data models
  - Checkpoint: Models work with basic tests

Phase 2: Core Features
  - Implement main user flows
  - Basic UI for each flow
  - Checkpoint: Core features work

Phase 3: Polish
  - Error handling and edge cases
  - UI refinement
  - Final checkpoint
```

## Parallel Story Execution

Some stories can be executed in parallel if they don't depend on each other.

**Good candidates for parallel:**
- Independent features
- Separate components that don't interact
- Tests for different areas

**Poor candidates for parallel:**
- Features with shared state
- Sequential workflows
- Dependent components

## Iterative PRDs

For exploratory work, use iterative PRD structure.

**Pattern:**
```
Iteration 1: Discovery
  - Research and prototype
  - Validate approach
  - Decide next steps

Iteration 2: Implementation (based on iteration 1 findings)
  - Build based on validated approach
  - Verify and gather feedback
  - Adjust scope for next iteration
```

## Handling Uncertainty

When requirements are uncertain:
1. Include explicit decision points in the PRD
2. Note what information would change the approach
3. Build for the most likely case
4. Include stories for validating assumptions

**Example decision point story:**
```
Title: Validate authentication approach
Description: Before implementing auth, validate our chosen approach works.
Tasks:
  - Build minimal auth proof of concept
  - Test against actual auth service
  - Document findings
Acceptance Criteria:
  - Approach is validated or alternative identified
  - Decision is documented
Notes: If approach doesn't work, create new stories for alternative
```

---

# Output Specifications

## prd.json Schema

```json
{
  "name": "string - kebab-case identifier",
  "description": "string - context for all tasks, motivation, goals",
  "branchName": "string - git branch name (type/feature-name)",
  "userStories": [
    {
      "id": "string - unique identifier (US-001, US-002, etc.)",
      "title": "string - short descriptive title",
      "description": "string - what and why, not how. Include tasks formatted:\n\n**Tasks:**\n1. First task\n2. Second task\n3. Third task",
      "acceptanceCriteria": ["array of strings - verifiable criteria"],
      "dependsOn": ["array of story IDs this depends on"],
      "notes": "string - file paths, patterns, warnings",
      "passes": "boolean - false initially, true when complete"
    }
  ]
}
```

**Key points for Ralph TUI template compatibility:**
- `tasks` field: Embed formatted tasks in `description` (not passed separately to template)
- `acceptanceCriteria`: Use array in JSON - template engine converts to formatted string automatically
- Template uses `{{acceptanceCriteria}}` directly (no `{{#each}}` needed)

## PRD.md Structure

```markdown
# [Project Name]

## Overview
Brief description of what this project accomplishes and why it matters.

## Goals
- Specific outcome 1
- Specific outcome 2
- ...

## Non-Goals
Explicitly out of scope:
- Thing we're not doing 1
- Thing we're not doing 2

## Technical Approach
High-level description of how we'll accomplish the goals.

## Phases

### Phase 1: [Name]
**Objective:** What this phase accomplishes
**Stories:** US-001 through US-003
**Exit criteria:** How we know phase is complete

### Phase 2: [Name]
...

## Testing Strategy
How verification will happen at each level.

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact level] | [How we handle it] |

## Success Criteria
How we know the entire project is complete:
- Criterion 1
- Criterion 2
```

## File Locations

PRD files go in `docs/prds/[name]/`:
- `docs/prds/user-auth/PRD.md`
- `docs/prds/user-auth/prd.json`

---

# Completion Signals

When executing PRD tasks, use these signals to communicate status.

| Signal | When to Use |
|--------|-------------|
| `<promise>COMPLETE</promise>` | All acceptance criteria met, verification passed |
| `<promise>BLOCKED</promise>` | Cannot proceed without human input |
| `<promise>SKIP</promise>` | Non-critical task, can't complete after genuine attempts |
| `<promise>EJECT</promise>` | Critical failure, requires human intervention |

**COMPLETE:** Use when the story is fully done. All criteria met, tests pass, verified.

**BLOCKED:** Use when you need a decision or information only the user can provide. Document what you need.

**SKIP:** Use for non-critical tasks that you've genuinely tried but can't complete. Don't use this to avoid difficult work.

**EJECT:** Use for critical failures that prevent further progress. This stops execution entirely.

---

# Reference Card

## Quick Decision Reference

| I need to... | Action |
|--------------|--------|
| Understand scope | Ask user |
| Choose implementation | Decide (follow patterns) |
| Know if something is needed | Ask user |
| Handle an edge case | Decide (use judgment) |
| Verify understanding | Present and confirm |
| Verify implementation | Browser + tests |

## Quick Verification Reference

| Task Type | Minimum Verification |
|-----------|---------------------|
| Research | Accuracy check |
| Documentation | Accuracy + spelling |
| Bug fix | Reproduction steps work |
| Feature | Tests + browser |
| Refactor | All existing tests pass |
| DevOps | Rollback plan exists |

## Quick Story Reference

| Story Type | Purpose |
|------------|---------|
| Context | Understand before implementing |
| Implementation | Build the thing |
| Checkpoint | Verify before continuing |
| Browser | Visual/interactive verification |
| Final | Comprehensive verification |
| Report | Document what was done |
