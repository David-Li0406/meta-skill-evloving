---
name: interview
description: Comprehensive feature development workflow that gathers requirements, creates specs, plans, and tasks, then implements incrementally while maintaining living documentation. This skill should be used when the user asks to "interview me", "ask me questions about", mentions "spec interview", "interview about spec", or wants to be interviewed in detail about a specification, feature, or implementation.
---

# Interview - Requirements Gathering & Specification

This skill guides you through gathering requirements to create a complete feature specification with PRD, technical plan, and actionable tasks.

## Overview

Use `/interview` when starting a new feature. This skill will:
1. Ask questions to understand the "what" and "why" (for the spec)
2. Ask technical questions inferred from the spec (for the plan)
3. Generate three living documents in `specs/<feature-name>/`

## Instructions

### Phase 1: Product Interview (spec.md)

Use `AskUserQuestion` to understand the feature. Start with core questions, then follow up based on answers.

**Start with these core questions:**
- "What feature do you want to build?" (header: "Feature")
- "What problem does this solve and why is it needed?" (header: "Problem")
- "Who are the users and what's their goal?" (header: "Users")
- "What does success look like?" (header: "Success")

**Then infer follow-up questions based on answers:**

Analyze responses and ask about anything unclear or important:
- Scope boundaries - what's in vs out?
- Priority - must-have vs nice-to-have requirements?
- User flows - key scenarios to support?
- Constraints - time, budget, technical limitations?
- Integration - existing features this touches?
- Edge cases from a user perspective?

**Clarify ambiguities immediately:**

When a user's response is unclear, vague, or could be interpreted multiple ways, ask clarifying questions before moving on:
- If a term is ambiguous: "When you say 'users', do you mean all users or just authenticated users?"
- If scope is unclear: "You mentioned 'notifications' - do you mean in-app notifications, email, push, or all of them?"
- If a flow has gaps: "You described step A and step C, but what happens in between? What if the user cancels?"
- If requirements conflict: "Earlier you said X, but this seems to contradict Y. Which takes priority?"
- If assumptions are implicit: "You mentioned 'the usual flow' - can you describe what that looks like specifically?"

**Do NOT assume or fill in gaps yourself.** If something could go multiple ways, ask. It's better to ask one extra question than to build the wrong thing.

Ask up to 4 questions at a time. Continue until you have enough context.

**Suggest better UX when you see obvious improvements:**
- If the user describes a flow with unnecessary steps, friction, or poor patterns, propose a better alternative
- Frame it as: "Based on what you've described, have you considered [alternative]? It would [benefit] because [reason]."
- Examples of improvements to suggest:
  - Multi-step wizards → single-page with sections (when steps are short)
  - Confirmation dialogs for every action → undo functionality (less intrusive)
  - Full-page reloads → optimistic updates (feels instant)
  - Manual refresh to see updates → real-time sync (better UX)
  - Complex settings pages → smart defaults with advanced options (simpler start)
- Always present as an option, not a mandate - the user may have context you don't

### Phase 2: Technical Interview (plan.md)

**Do NOT use hardcoded questions.** Analyze the spec context and infer what technical decisions need user input.

**How to infer technical questions:**

Read through the gathered requirements and identify:

1. **Architecture decisions** - If multiple approaches exist, ask which one:
   - "Should we use REST or GraphQL for this API?"
   - "Client-side or server-side rendering for this page?"
   - "Monolith or microservice for this functionality?"

2. **Database/Data** - If data storage is involved:
   - "What's the data model? What fields are needed?"
   - "Use existing tables or new ones?"
   - "What are the relationships between entities?"

3. **Security** - If auth/sensitive data is involved:
   - "What authorization rules apply?"
   - "What data needs protection?"
   - "Any compliance requirements?"

4. **External services** - If integrations are needed:
   - "Which third-party service to use?"
   - "How to handle failures/retries?"
   - "Caching strategy?"

5. **User experience** - If UI is involved:
   - "What should happen on error?"
   - "Loading states needed?"
   - "Mobile considerations?"

6. **Suggest better UX flows** - When you identify obvious improvements:
   - If the described flow has friction points, propose smoother alternatives
   - Present the user's original approach alongside your recommended improvement
   - Example: "You mentioned a 3-step form. Have you considered a single-page form with inline validation? It reduces drop-off and feels faster."
   - Always explain WHY your suggestion is better (fewer clicks, faster feedback, less cognitive load, etc.)

7. **Edge cases** - Technical edge cases:
   - "What if X fails?"
   - "How to handle concurrent edits?"
   - "Rate limiting needed?"

8. **Alternatives & Improvements** - When you see multiple valid options OR better approaches:
   - Present the options with trade-offs
   - Ask which approach the user prefers
   - If one option is clearly better, add "(Recommended)" to its label
   - **Proactively suggest improvements**: If the user's proposed approach has known pitfalls or there's a clearly superior pattern, present it as an alternative
   - Example: "You mentioned polling for updates. Consider WebSockets instead - they provide real-time updates without the latency and server load of polling. (Recommended)"
   - Example: "For this data structure, you could use a flat list, but a normalized structure with IDs would make updates O(1) instead of O(n). (Recommended)"

**Clarify technical ambiguities:**

When technical details are unclear or could be interpreted multiple ways:
- If implementation is ambiguous: "You mentioned 'real-time updates' - do you mean WebSocket-based live updates, or polling every few seconds?"
- If data structure is unclear: "What exactly goes in a 'user profile'? Just name and email, or more fields?"
- If error handling is vague: "When you say 'handle errors gracefully', what should the user see? A toast, a modal, inline error?"
- If scale is unknown: "How many concurrent users do you expect? This affects caching and database decisions."
- If existing patterns are unclear: "Is there an existing way similar features handle this in the codebase?"

**Summarize understanding before proceeding:**
After gathering technical context, briefly summarize your understanding: "So to confirm: we'll use X for Y, store data in Z, and handle errors by W. Is that right?" This catches misunderstandings early.

**Key principles:**
- Surface decisions the user needs to make. Don't assume - ask.
- **Clarify before assuming**: If something could be interpreted multiple ways, ask which interpretation is correct.
- **Be a proactive advisor**: If you see a better way, say so. Your experience across many projects is valuable - share patterns that work well and warn about common pitfalls.
- When suggesting improvements, always explain the trade-off (what they gain vs. what it costs in complexity/time).

### Phase 3: Create Specification Documents

After gathering all context, create three files:

#### 1. `specs/<feature-name>/spec.md`

```markdown
# <Feature Name> Specification

## Overview
Brief description of the feature

## Problem Statement
Why this feature is needed (from interview)

## Target Users
Who will use this and their goals

## Success Criteria
How we measure success

## Requirements

### Must Have
- Requirement 1
- Requirement 2

### Nice to Have
- Optional requirement 1

## User Flows
Key scenarios from the interview

## Constraints
Limitations and boundaries

## Out of Scope
What we're explicitly NOT building
```

#### 2. `specs/<feature-name>/plan.md`

**Structure is dynamic** - only include sections relevant to this feature based on the technical interview.

```markdown
# <Feature Name> Technical Plan

## Overview
High-level technical approach

## Implementation Approach
Step-by-step technical strategy

<!-- Only include relevant sections below -->

## Architecture
<!-- If architecture was discussed -->

## Data Model
<!-- If database/schema was discussed -->

## API Design
<!-- If APIs were discussed -->

## Security
<!-- If security was discussed -->

## Integrations
<!-- If external services were discussed -->

## Error Handling
<!-- If error scenarios were discussed -->

## Edge Cases
Specific edge cases from the interview

## Testing Strategy
<!-- ALWAYS include - not optional -->
- Unit tests for: <business logic, utilities, helpers>
- Integration tests for: <API endpoints, database operations>
- Test command: <e.g., npm test, pytest, go test>

## Linting & Type Checking
<!-- ALWAYS include - not optional -->
- Lint command: <e.g., npm run lint>
- Type check command: <e.g., npm run typecheck, tsc>

## Open Questions
Any unresolved decisions
```

## Guidelines

1. **Ask clarifying questions** - When something is unclear, vague, or ambiguous, ask before proceeding. Never assume or guess the user's intent. One extra question is always better than building the wrong thing.

2. **Be thorough** - Continue asking questions until you have a complete understanding of:
   - All technical requirements
   - All user experience requirements
   - All constraints and tradeoffs
   - All edge cases and error scenarios

**Required sections:** Testing Strategy and Linting & Type Checking must ALWAYS be included in every plan - these are not optional.

#### 3. `specs/<feature-name>/tasks.json`

**Critical: Tasks must be self-contained, testable in isolation, and have clear success criteria.**

Each task should:
- Be independently implementable
- Not depend on uncommitted work from other tasks
- Not modify the same files as concurrent tasks
- Include all context needed to execute it
- Be testable in isolation - user can pause, verify it works, then continue
- Have clear success criteria that can be verified (tests pass, endpoint returns X, UI shows Y)

```json
{
  "featureName": "<feature-name>",
  "description": "Living document. Update passes/learnings as tasks complete.",
  "tasks": [
    {
      "id": 1,
      "title": "<clear action>",
      "category": "<backend|frontend|database|config|test|docs>",
      "context": "<relevant details from spec/plan>",
      "files": ["<file1>", "<file2>"],
      "success": "<verifiable criteria - e.g., 'tests pass', 'endpoint returns 200'>",
      "steps": [
        "<step 1 - e.g., 'run npm test'>",
        "<step 2 - e.g., 'curl localhost:3000/api/users'>",
        "<step 3 - e.g., 'verify response contains user object'>"
      ],
      "passes": false,
      "learnings": []
    },
    {
      "id": 2,
      "title": "<clear action>",
      "category": "<category>",
      "context": "<relevant details>",
      "files": ["<file1>"],
      "success": "<verifiable criteria>",
      "steps": ["<verification step 1>", "<verification step 2>"],
      "passes": false,
      "learnings": []
    }
  ]
}
```

**Field descriptions:**
- `id`: Auto-incrementing task identifier (1, 2, 3...)
- `title`: Clear, actionable task name
- `category`: Type of work (backend, frontend, database, config, test, docs)
- `context`: Relevant details from spec/plan needed to complete the task
- `files`: Expected files to create or modify
- `success`: Verifiable success criteria
- `steps`: Ordered verification steps to confirm task completion
- `passes`: Boolean - false when pending, true when completed
- `learnings`: Array of strings - notes added after completion about decisions, deviations, or useful context for subsequent tasks

**Example of a completed task:**
```json
{
  "id": 3,
  "title": "Set up authentication middleware",
  "category": "backend",
  "context": "Use JWT for stateless auth per plan.md",
  "files": ["src/middleware/auth.ts"],
  "success": "Protected routes return 401 without token, 200 with valid token",
  "steps": [
    "Run npm test -- auth.test.ts",
    "curl -X GET localhost:3000/api/protected (expect 401)",
    "curl -X GET localhost:3000/api/protected -H 'Authorization: Bearer <token>' (expect 200)"
  ],
  "passes": true,
  "learnings": [
    "Used Passport.js instead of custom JWT validation for better OAuth support",
    "Existing error handler in src/middleware/error.ts already formats auth errors correctly"
  ]
}
```

**Task sizing guidelines:**
- **Ideal size:** 1-2 hours of human work equivalent
- **Small enough** to complete in one context window (~50-100 turns)
- **Big enough** to be a meaningful, testable unit
- **One commit's worth** - would you squash these changes into one commit?
- If a task touches more than 3-5 files, consider splitting it
- If it can't be tested without another uncompleted task, merge them

**Good task examples:**
- "Create user registration API endpoint with validation"
- "Add login form component with error handling"
- "Set up database schema for orders table"

**Too small** (combine with related work):
- "Create user model" → combine with related endpoint
- "Add email field validation" → part of a larger form task

**Too big** (break down further):
- "Implement full authentication system" → split into: registration, login, password reset
- "Build the entire checkout flow" → split into: cart, payment, confirmation

**Task ordering principles:**
- Foundation first (setup, config, types)
- Core logic before edge cases
- Backend before frontend (if applicable)
- Each task should include writing its own unit/integration tests
- Final task should always be "Run linting, type checking, and all tests" to verify no regressions

**Testing requirements:**
- Every task that adds functionality MUST include writing tests for that functionality
- Tests are part of the task, not a separate task (keeps tasks self-contained and verifiable)
- Integration tests for API endpoints, unit tests for business logic

### Phase 4: Review

After creating all documents:

1. Summarize what was created
2. Show the task list
3. Mention they can edit the specs manually before implementing
4. Output the available commands for next steps:

```
Ready to implement! Recommend running /clear first for a fresh context, then:

/implement <feature-name>
  → Interactive mode: asks after each task

/implement <feature-name> --all
  → Autonomous mode: completes all tasks without stopping

ralph -f <feature-name> [-n <iterations>]
  → Fully automated: no human in the loop (default: 30 iterations)
```

## File Naming

Convert feature name to kebab-case:
- "User Authentication" -> `specs/user-authentication/`
- "Shopping Cart" -> `specs/shopping-cart/`

## Example Flow

```
User: /interview

Agent: [Asks product questions using AskUserQuestion]
User: [Answers]

Agent: [Asks inferred technical questions]
User: [Answers]

Agent: [Creates specs/my-feature/spec.md, plan.md, tasks.json]
Agent: "I've created the specification documents:
  - specs/my-feature/spec.md (PRD)
  - specs/my-feature/plan.md (technical plan)
  - specs/my-feature/tasks.json (5 tasks)

Review and edit the specs if needed.

Ready to implement! Recommend running /clear first for a fresh context, then:

/implement my-feature
  → Interactive mode: asks after each task

/implement my-feature --all
  → Autonomous mode: completes all tasks without stopping

ralph -f my-feature [-n <iterations>]
  → Fully automated: no human in the loop (default: 30 iterations)"
```