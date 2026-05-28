# Phase 2: Parallel Quality Checks

## Goal

Run independent quality checks simultaneously for speed.

## Pre-check: Load Pattern Files

Before launching agents, load relevant pattern files based on file types:

- Service files → `service-refactoring-patterns.md`
- SQL files → `sql-testing-patterns.md`
- Components → `react-typescript-antipatterns.md`

Use Read tool to load patterns from `claude-patterns/`. Pass pattern content to agents.

## Agents (Launch in Parallel)

Launch all 6 agents in a single message with multiple Task calls:

### 1. duplicate-code-detector Agent

Checks for duplications of existing utilities, services, hooks, components, or validation schemas.

**Reports each duplication with**:

- Location
- The existing code it duplicates
- Why to use the existing code
- Refactoring steps

### 2. jenny Agent (User Voice / Completeness Verification)

**Role**: Speak for the user. Verify the implementation matches the request and ask "what did we miss?"

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are jenny - the voice of the user. Your job is to verify we actually built what was requested and challenge what we might have missed.

FILES CHANGED: {file_list}

ORIGINAL REQUEST CONTEXT: {conversation_context}

Check these 5 areas:

1. **Feature Completeness** (reactive)
   - Did we implement EVERYTHING the user asked?
   - Are there TODO comments or unfinished parts?
   - Did we skip any requirements mentioned in the conversation?

2. **Missing Requirements** (proactive)
   - What did we forget to ask about?
   - "Spec says always on - would user ever want to turn it off?"
   - "We built create - what about edit/delete?"
   - "This saves to DB - what about undo?"
   - What's the obvious next question a user would have?

3. **User Expectations**
   - Would a user trying this feature get what they expect?
   - Are there obvious use cases we didn't handle?
   - Does the happy path work?

4. **Integration**
   - Is the feature accessible from the UI?
   - Are there missing routes, buttons, or entry points?
   - Is it wired up to the backend correctly?

5. **Edge Cases a User Would Hit**
   - Empty states handled?
   - Error messages user-friendly?
   - Loading states present?

For each issue found, report:
- Category (completeness/missing-req/expectations/integration/edge-case)
- What's missing or wrong
- Why a user would care
- Suggested addition or fix
```

**NOT jenny's job** (handled elsewhere):

- Pattern compliance (pattern-enforcer in check-your-code)
- Bug hunting (deep-bug-hunter)
- Security (Security Reviewer)

### 3. deep-bug-hunter Agent

Performs initial bug detection focusing on:

- Logic errors
- Null/undefined handling
- Race conditions
- Async/await issues
- Edge cases (empty arrays, boundary conditions)
- Type coercion bugs
- Error handling gaps

**Reports each potential bug with**:

- Severity classification
- Impact analysis
- Fix recommendation

### 4. Security & Multi-tenant Reviewer

**Uses**: `general-purpose` agent

Focuses on:

- SQL injection vulnerabilities
- Missing organization_id filtering (multi-tenant isolation)
- PII in localStorage/sessionStorage
- XSS vulnerabilities
- Authentication/authorization gaps

### 5. Performance & Bug-Causing Antipattern Reviewer

**Uses**: `general-purpose` agent

Focuses on **bug-causing issues only** (style/quality issues go to check-your-code):

- Memory leaks (missing useEffect cleanup)
- useState for derived values → causes stale data bugs
- Missing effect dependencies → causes stale closure bugs
- Direct service calls in components → causes infinite re-render loops
- Handwritten interfaces (should use Zod inference) → causes type bugs
- Inefficient algorithms causing performance degradation

### 6. Bug & Correctness Reviewer

**Uses**: `general-purpose` agent

Focuses on:

- Logic errors
- Unhandled edge cases (null/undefined, empty arrays)
- Async/await issues (missing error handling, race conditions)
- Type errors and type coercion bugs
- Error handling gaps

## Severity Classification Guidelines

All reviewers follow these:

**P0 requires actual impact evidence**, not just pattern violation:

- Good: "P0 because query returns data from all orgs" (evidence)
- Bad: "P0 because missing org_id filter" (pattern only - might be admin code)

**Consider context**:

- Is this admin-only?
- Utility function?
- Test code?

**When uncertain**: Mark as "P0 (needs validation)" with reasoning for Phase 3 to verify.

## After Completion

Wait for all 6 agents to complete, then collect their reports.

Proceed to Phase 3 with P0/P1/P2 findings for validation.
