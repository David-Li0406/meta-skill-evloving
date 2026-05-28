# Module 3: Specification-Driven Development

This is the core workflow. Master this before exploring optional add-ons.

## Before You Start

**This workflow works well for:**
- New features with clear requirements
- API endpoints, utilities, CRUD operations
- Bug fixes where you can describe expected behavior

**Use traditional coding instead for:**
- Security-critical code (auth, payments, encryption)
- Performance-critical code requiring optimization
- Legacy code without tests
- Exploratory/research work

See [Limitations](../../LIMITATIONS.md) for details.

---

## Learning Objectives

By the end of this module, you will:
- Write a spec that Claude can work from
- Guide Claude through context gathering
- Review generated tests and code
- Approve the final implementation

## The New Workflow

### Old Way (Manual)
```
Developer writes code → Developer writes tests → Debug → Repeat
```

### Agentic Way
```
Specify → Context → Plan → Generate Tests → Generate Code → Review → Validate
  [You]   [Claude]  [Interactive]  [Claude]    [Claude]      [AI]    [Claude+You]
```

**Your job**: Define WHAT you want, approve at checkpoints
**Claude's job**: Figure out HOW, run tests, iterate until passing

### Common Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Vague specs → wrong code | Be specific. Include examples. |
| Rubber-stamping approvals | Actually read the diff. You own the code. |
| Tests pass but code is wrong | Tests are samples, not proofs. Review logic. |
| Claude hallucinates APIs | Verify imports and library calls exist. |
| Infinite iteration loop | If stuck after 3 attempts, debug manually. |

## The Specification-Driven Cycle

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  1. SPECIFY    2. CONTEXT     3. PLAN       4. GENERATE    5. REVIEW      │
│     (You)        (Claude)       (Interactive)  (Claude)       (AI)        │
│                                                                           │
│  "I need user   "What auth?   "Here's my    Tests first,   AI-assisted   │
│   registration" Where do      plan..."      then code      code review   │
│                 users live?"  [You approve]                              │
│                                                                           │
│         │            │              │              │              │       │
│         └────────────┴──────────────┴──────────────┴──────────────┘       │
│                                      ▼                                    │
│                               6. VALIDATE                                 │
│                            (Claude runs tests)                            │
│                                                                           │
│                    Run tests → Fix failures → Repeat                      │
│                    until all tests pass, then you approve                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Step 1: Write a Specification

A good spec answers: **What do I want to exist that doesn't exist yet?**

### Spec Formats (Pick One)

**User Story Format:**
```markdown
As a [user type]
I want to [action]
So that [benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

**Feature Brief Format:**
```markdown
## Feature: [Name]

### Problem
What problem does this solve?

### Solution
What should happen?

### Requirements
- Requirement 1
- Requirement 2

### Out of Scope
- What this does NOT include
```

**Simple Format:**
```markdown
## [Feature Name]

Build a function/endpoint/component that:
- Does X
- Handles Y
- Returns Z

Constraints:
- Must work with existing [system]
- Should not break [thing]
```

### Example Spec

```markdown
## Feature: User Registration API

### Problem
Users can't create accounts in our system.

### Solution
Create a POST /api/users endpoint that registers new users.

### Requirements
- Accept email and password
- Validate email format
- Require password minimum 8 characters
- Hash password before storing
- Return user object (without password)
- Return 400 for validation errors
- Return 409 if email already exists

### Out of Scope
- Email verification (separate feature)
- OAuth/social login
```

## Step 2: Context Gathering

After you provide a spec, Claude should ask clarifying questions. **Answer honestly** - this is where tribal knowledge gets captured.

### Questions Claude Should Ask

```
Based on your spec, I have some questions:

1. Architecture: Where does this fit?
   - Which directory/module?
   - Any existing patterns to follow?

2. Dependencies: What already exists?
   - Database/ORM you're using?
   - Existing auth/validation utilities?
   - Error handling conventions?

3. Constraints: What should I avoid?
   - Protected files?
   - Deprecated patterns?

4. Testing: How do you test?
   - Test framework?
   - Where do tests live?
   - Any test utilities?
```

### Example Context Exchange

**You**: [paste spec from above]

**Claude**: "I have some questions:
1. What database/ORM do you use for users?
2. Where should this endpoint live?
3. What's your password hashing approach?
4. What does your error response format look like?"

**You**: "We use Prisma with PostgreSQL. Put it in src/routes/users.ts. Use bcrypt for passwords. Errors are { error: string, code: number }."

Now Claude has real context, not assumptions.

## Step 3: Execution Planning

After gathering context, Claude enters **plan mode** to create a detailed execution plan. This is an interactive checkpoint where you refine the approach before any code is written.

### What Claude Presents

```
Based on your spec and context, here's my execution plan:

## Execution Plan: User Registration API

### Files to Create/Modify
1. `src/routes/users.ts` - New file for user registration endpoint
2. `src/routes/users.test.ts` - Test file
3. `src/routes/index.ts` - Add route import

### Implementation Steps
1. Create Prisma schema update for User model (if needed)
2. Write test cases covering all requirements
3. Implement POST /api/users endpoint
4. Add email validation using existing validator
5. Integrate bcrypt for password hashing
6. Add error handling following your { error, code } pattern

### Dependencies
- Using existing: `bcrypt`, `prisma`, email validator from `src/utils/validators`
- No new dependencies needed

### Questions Before Proceeding
1. Should I run `prisma migrate` after schema changes?
2. Do you want integration tests with a real DB or mocked?

Does this plan look right? Any adjustments?
```

### Your Review Checkpoint

At this stage, you can:
- **Approve**: "Looks good, proceed"
- **Adjust scope**: "Skip the Prisma migration, schema already exists"
- **Add constraints**: "Use the test database for integration tests"
- **Request changes**: "Also add rate limiting to the endpoint"

### Example Plan Interaction

**Claude**: "Here's my plan: [shows plan above]. Does this look right?"

**You**: "Two changes: 1) Schema already exists, skip that step. 2) Add a test for rate limiting - max 5 requests per minute per IP."

**Claude**: "Got it. Updated plan:
- Removed Prisma schema step
- Added rate limiting test case
- Will use existing `rateLimiter` middleware from `src/middleware/`

Ready to generate tests?"

**You**: "Yes, proceed."

### Why Plan Mode Matters

- **Catches misunderstandings early** - Before code is written
- **Surfaces hidden dependencies** - Claude might reference files you forgot about
- **Gives you control** - You approve the approach, not just the output
- **Saves iteration cycles** - Better plan = fewer rewrites

## Step 4: Test Generation

Claude proposes tests based on your spec. **Review them before implementation.**

### What Claude Should Generate

```typescript
// Claude generates tests from your requirements:

describe('POST /api/users', () => {
  it('creates user with valid email and password', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'password123' });

    expect(res.status).toBe(201);
    expect(res.body.email).toBe('test@example.com');
    expect(res.body.password).toBeUndefined(); // Not exposed
  });

  it('returns 400 for invalid email', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', password: 'password123' });

    expect(res.status).toBe(400);
  });

  it('returns 400 for short password', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: '123' });

    expect(res.status).toBe(400);
  });

  it('returns 409 for duplicate email', async () => {
    // Create user first, then try again
    await createUser({ email: 'test@example.com' });

    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'password123' });

    expect(res.status).toBe(409);
  });
});
```

### Your Review Checkpoint

Before Claude implements, review the tests:
- Do they cover all requirements?
- Are edge cases handled?
- Do they match your testing patterns?

Say "yes" to proceed, or "add test for X" to expand.

## Step 5: Code Generation

Claude implements code based on the approved tests.

```
Claude: "Generating implementation based on the test cases..."
Claude: "Here's the code: [shows diff]"
```

At this point, the code is written but not yet validated.

## Step 6: Code Review (Optional)

You can add an AI review step before running tests. **This is optional**—skip it for simple features.

### Quick Review (Default)

Just ask Claude:
```
"Review this code for obvious issues before we run tests."
```

### Third-Party Tools (Optional Add-on)

For teams wanting additional review layers:

| Tool | Use Case | Setup |
|------|----------|-------|
| Snyk | Security vulnerabilities | `snyk code test` |
| SonarQube | Code quality | Requires server setup |
| CodeRabbit | PR review automation | GitHub integration |

See your team's existing tooling. Don't add complexity you don't need.

### Your Checkpoint

- **Proceed**: "Run the tests"
- **Fix first**: "Address X before testing"
- **Skip review**: Move directly to validation

## Step 7: Validation (Test-Fix Loop)

Claude runs tests and **iterates until all pass**. You don't need to manually debug.

### The Automated Loop

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Claude: "Running tests..."                                 │
│                                                             │
│  Test Results: 3/4 passing                                  │
│  ✓ creates user with valid email and password              │
│  ✓ returns 400 for invalid email                           │
│  ✓ returns 400 for short password                          │
│  ✗ returns 409 for duplicate email                         │
│                                                             │
│  Error: Expected 409, got 500                               │
│  Cause: Missing unique constraint handler                   │
│                                                             │
│  Claude: "Fixing the duplicate email handling..."           │
│  [Makes targeted fix]                                       │
│                                                             │
│  Claude: "Running tests again..."                           │
│  Test Results: 4/4 passing ✓                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### What Claude Does Automatically

1. **Runs the test suite** (or specific tests for the feature)
2. **Analyzes failures** - reads error messages, stack traces
3. **Makes targeted fixes** - only changes what's needed
4. **Re-runs tests** - verifies the fix worked
5. **Repeats** until all tests pass (or asks for help if stuck)

### When Claude Asks for Help

```
Claude: "I've tried 3 approaches to fix this test but it's still failing.
The issue seems to be with the database connection in tests.

Options:
1. Check if test database is running
2. Review the test setup in jest.setup.ts
3. I can show you the error details

What would you like to do?"
```

### Your Final Review

Once all tests pass:

```
Claude: "All 4 tests passing. Here's the final diff:"

[Shows complete diff with all changes]

You: Review the implementation
  - Does it match the spec?
  - Any concerns with the approach?
  - Ready to merge?

You: "Approved" or "One change: [specific request]"
```

## Exercise: Your First Spec-Driven Feature

### Step 1: Write Your Spec

Pick something real for your project, or use this:

```markdown
## Feature: Slug Generator Utility

### Problem
Need to convert titles to URL-friendly slugs.

### Requirements
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Handle empty strings

### Example
"Hello World!" → "hello-world"
```

### Step 2: Give Spec to Claude

```
Here's my feature spec:

[paste spec]

Ask me any clarifying questions about my codebase, then:
1. Create an execution plan for my approval
2. Propose tests based on the requirements
3. Wait for my approval
4. Implement code to pass the tests
```

### Step 3: Answer Context Questions

Claude asks, you answer with real details about your project.

### Step 4: Review Execution Plan

Claude presents a plan. You approve, adjust, or add constraints.

### Step 5: Review Generated Tests

Claude shows tests. You approve or adjust.

### Step 6: Review AI-Generated Code

Claude generates code, runs AI review. You approve or request fixes.

### Step 7: Validate Implementation

Claude runs tests, fixes failures automatically, and presents final diff for your approval.

## When This Works Best

| Good Fit | Less Ideal |
|----------|------------|
| New features with clear requirements | Exploratory/research work |
| Bug fixes (spec = "this should work") | Performance optimization |
| API endpoints | Complex refactoring |
| Utility functions | |
| Business logic | |
| Frontend components (with Figma MCP) | |

> **Frontend Developers**: Use the Figma MCP integration (see Module 2) to let Claude reference your designs directly. Your spec becomes: "Implement the component from this Figma frame."

## Checkpoint

Module 3 is complete when:
- [ ] You've written a spec for a feature
- [ ] Claude asked context questions and you answered
- [ ] Claude presented an execution plan and you approved it
- [ ] Claude generated tests from your spec
- [ ] Code passed AI review (Claude or third-party tools)
- [ ] Claude iterated until all tests passed
- [ ] You approved the final implementation

## Key Takeaway

**You are the architect. You define what should exist.**

Claude handles:
- Asking the right questions
- Creating detailed execution plans
- Writing tests from requirements
- Implementing code
- Running AI-assisted code review
- Iterating on test failures until all pass

Your job is specification, plan approval, and final validation—not debugging or manual iteration.

---

## Cost Awareness

Each iteration costs API tokens. Rough estimates:

| Feature Complexity | Iterations | Estimated Cost |
|--------------------|------------|----------------|
| Simple (utility function) | 1-2 | $0.50-1.00 |
| Medium (API endpoint) | 2-4 | $1.00-3.00 |
| Complex (multi-file feature) | 4-8 | $3.00-10.00 |

**Tips to reduce cost:**
- Write clear specs (fewer misunderstandings = fewer iterations)
- Add context to CLAUDE.md (Claude asks fewer questions)
- Break large features into smaller specs
- Set token budgets in Anthropic Console

---

## Next Steps

- **Add-ons**: [MCP integrations](02-mcp-mastery.md), [Git hooks](04-governance.md)
- **Limitations**: [When not to use this workflow](../../LIMITATIONS.md)
- **Enterprise**: [Compliance and security controls](../../ENTERPRISE.md)
