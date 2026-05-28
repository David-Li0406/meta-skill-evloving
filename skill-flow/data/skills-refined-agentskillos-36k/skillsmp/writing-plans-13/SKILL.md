---
name: writing-plans
description: Creates Tasks with dependencies, exact file paths, complete code, and verification commands. Use when requirements are clear for multi-step tasks.
user_invokable: true
---

# Writing Plans

## Overview

Create comprehensive implementation plans as native Claude Code Tasks. Assume the engineer has zero codebase context and questionable taste. Document everything: exact file paths, complete code, verification commands, expected output.

**Core principle:** No placeholders. No assumptions. Verify with codebase-investigator, then write definitive steps.

**Announce at start:** "I'm using gambit:write-plan to create the implementation plan."

## Rigidity Level

MEDIUM FREEDOM — Follow task structure and verification pattern strictly. Adapt implementation details to actual codebase state.

## Quick Reference

| Step | Action | Critical Rule |
|------|--------|---------------|
| **Create Epic** | `TaskCreate` with requirements + success criteria | Requirements are IMMUTABLE |
| **Verify Codebase** | Use codebase-investigator agent | NEVER verify yourself |
| **Create Subtasks** | `TaskCreate` for each, then `TaskUpdate` with `addBlockedBy` | Bite-sized (2-5 min each) |
| **Present to User** | Show COMPLETE plan FIRST | Then ask for approval |
| **Continue** | Move to next subtask automatically | NO asking permission between |

**FORBIDDEN:** Placeholders like `[implementation details go here]`
**REQUIRED:** Complete code, exact paths, real commands

## Task Tool Reference

### TaskCreate

Creates a new task. Returns the task ID.

```
TaskCreate
  subject: "Brief imperative title (e.g., 'Add login endpoint')"
  description: "Full markdown description with steps, code, commands"
  activeForm: "Present participle for spinner (e.g., 'Adding login endpoint')"
```

### TaskUpdate

Updates an existing task. Use for setting dependencies and status.

```
TaskUpdate
  taskId: "the-task-id"
  status: "pending" | "in_progress" | "completed"
  addBlockedBy: ["task-id-that-must-complete-first"]
  addBlocks: ["task-id-that-waits-for-this"]
```

### TaskGet

Retrieves full task details.

```
TaskGet
  taskId: "the-task-id"
```

### TaskList

Lists all tasks with status, owner, and blockers.

```
TaskList
```

## When to Use

After `gambit:brainstorm` produces approved requirements, or when user provides clear spec.

Symptoms:
- Have requirements, need implementation plan
- Need to break work into trackable pieces
- Want explicit file paths and code examples
- Multiple engineers or sessions will execute

## The Process

### 1. Create Epic Task

The epic contains immutable requirements — these don't change during implementation.

```
TaskCreate
  subject: "Feature: User Authentication"
  description: |
    ## Goal
    Add JWT-based authentication to the API.

    ## Requirements (IMMUTABLE)
    - Users can register with email/password
    - Users can login and receive JWT token
    - Protected routes validate JWT

    ## Success Criteria
    - [ ] POST /auth/register creates user with hashed password
    - [ ] POST /auth/login returns valid JWT
    - [ ] Protected routes reject invalid/missing tokens
    - [ ] All endpoints have integration tests

    ## Architecture
    Use bcrypt for password hashing, jsonwebtoken for JWT.
    Middleware pattern for route protection.

    ## Anti-patterns (FORBIDDEN)
    - Do NOT store plaintext passwords
    - Do NOT use symmetric JWT signing in production
    - Do NOT mock database in integration tests
  activeForm: "Planning user authentication"
```

Note the epic task ID returned — you'll reference it when creating subtasks.

### 2. Verify Codebase State

**CRITICAL: Use codebase-investigator agent. Never verify yourself.**

Dispatch Task tool with Explore agent:

```
Task
  subagent_type: "Explore"
  prompt: |
    Verify these assumptions for the auth feature:
    - Where should auth routes go? Check existing route patterns.
    - Is there an existing User model? What fields does it have?
    - What test patterns are used? Where do integration tests live?
    - Is bcrypt or another hashing library already installed?

    Report:
    1. What exists vs what we expect
    2. Exact file paths for new code
    3. Dependency versions already installed
```

**Based on report:**
- ✓ Confirmed → Use in plan
- ✗ Incorrect → Adjust plan to reality
- + Found additional → Incorporate

**NEVER write conditional steps:**
- ❌ "Update `index.js` if exists"
- ❌ "Modify `config.py` (if present)"

**ALWAYS write definitive steps:**
- ✅ "Create `src/routes/auth.ts`" (investigator confirmed doesn't exist)
- ✅ "Modify `src/routes/index.ts:12-15`" (investigator confirmed location)

### 3. Create Subtasks with Dependencies

Each subtask is bite-sized (2-5 minutes) and follows TDD.

**First subtask (no dependencies):**

```
TaskCreate
  subject: "Add User model with password hashing"
  description: |
    **Files:**
    - Create: `src/models/user.ts`
    - Test: `tests/models/user.test.ts`

    **Step 1: Write failing test**
    ```typescript
    // tests/models/user.test.ts
    import { createUser, verifyPassword } from '../src/models/user';

    describe('User model', () => {
      it('hashes password on creation', async () => {
        const user = await createUser('test@example.com', 'plaintext123');
        expect(user.password).not.toBe('plaintext123');
        expect(user.password).toMatch(/^\$2[ayb]\$.{56}$/);
      });

      it('verifies correct password', async () => {
        const user = await createUser('test@example.com', 'mypassword');
        expect(await verifyPassword(user, 'mypassword')).toBe(true);
        expect(await verifyPassword(user, 'wrongpassword')).toBe(false);
      });
    });
    ```

    **Step 2: Run test (expect fail)**
    ```bash
    npm test -- tests/models/user.test.ts
    ```
    Expected: `Cannot find module '../src/models/user'`

    **Step 3: Implement minimal code**
    ```typescript
    // src/models/user.ts
    import bcrypt from 'bcrypt';

    export interface User {
      id: string;
      email: string;
      password: string;
    }

    export async function createUser(email: string, plainPassword: string): Promise<User> {
      const password = await bcrypt.hash(plainPassword, 10);
      return { id: crypto.randomUUID(), email, password };
    }

    export async function verifyPassword(user: User, plainPassword: string): Promise<boolean> {
      return bcrypt.compare(plainPassword, user.password);
    }
    ```

    **Step 4: Run test (expect pass)**
    ```bash
    npm test -- tests/models/user.test.ts
    ```
    Expected: `PASS`

    **Step 5: Commit**
    ```bash
    git add src/models/user.ts tests/models/user.test.ts
    git commit -m "feat(auth): add User model with bcrypt password hashing"
    ```
  activeForm: "Adding User model"
```

Save the returned task ID (e.g., `task-user-model`).

**Second subtask (depends on first):**

```
TaskCreate
  subject: "Add login endpoint"
  description: |
    **Files:**
    - Create: `src/routes/auth.ts`
    - Modify: `src/routes/index.ts:12-15`
    - Test: `tests/routes/auth.test.ts`

    **Step 1: Write failing test**
    ```typescript
    // tests/routes/auth.test.ts
    import request from 'supertest';
    import { app } from '../src/app';
    import { createUser } from '../src/models/user';

    describe('POST /auth/login', () => {
      it('returns JWT for valid credentials', async () => {
        await createUser('test@example.com', 'password123');

        const response = await request(app)
          .post('/auth/login')
          .send({ email: 'test@example.com', password: 'password123' });

        expect(response.status).toBe(200);
        expect(response.body.token).toBeDefined();
        expect(response.body.token).toMatch(/^eyJ/); // JWT format
      });

      it('returns 401 for invalid password', async () => {
        await createUser('test@example.com', 'password123');

        const response = await request(app)
          .post('/auth/login')
          .send({ email: 'test@example.com', password: 'wrongpassword' });

        expect(response.status).toBe(401);
      });
    });
    ```

    **Step 2: Run test (expect fail)**
    ```bash
    npm test -- tests/routes/auth.test.ts
    ```
    Expected: `404` (route doesn't exist yet)

    **Step 3: Implement login route**
    ```typescript
    // src/routes/auth.ts
    import { Router } from 'express';
    import jwt from 'jsonwebtoken';
    import { findUserByEmail, verifyPassword } from '../models/user';

    const router = Router();

    router.post('/login', async (req, res) => {
      const { email, password } = req.body;

      const user = await findUserByEmail(email);
      if (!user || !await verifyPassword(user, password)) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }

      const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!, { expiresIn: '24h' });
      res.json({ token });
    });

    export default router;
    ```

    **Step 4: Register route in index**
    ```typescript
    // src/routes/index.ts - add at line 12
    import authRoutes from './auth';
    router.use('/auth', authRoutes);
    ```

    **Step 5: Run test (expect pass)**
    ```bash
    npm test -- tests/routes/auth.test.ts
    ```
    Expected: `PASS`

    **Step 6: Commit**
    ```bash
    git add src/routes/auth.ts src/routes/index.ts tests/routes/auth.test.ts
    git commit -m "feat(auth): add POST /auth/login endpoint"
    ```
  activeForm: "Adding login endpoint"
```

Save the returned task ID (e.g., `task-login`).

**Set dependency:**

```
TaskUpdate
  taskId: "task-login"
  addBlockedBy: ["task-user-model"]
```

### 4. Present Complete Plan

Show the FULL plan before asking for approval:

```markdown
## Epic: User Authentication

**Task 1: Add User model with password hashing**
- Creates `src/models/user.ts` with bcrypt hashing
- Tests in `tests/models/user.test.ts`
- No dependencies (ready to start)

**Task 2: Add login endpoint** (blocked by Task 1)
- Creates `src/routes/auth.ts`
- Modifies `src/routes/index.ts`
- Tests in `tests/routes/auth.test.ts`

**Task 3: Add JWT middleware** (blocked by Task 2)
- Creates `src/middleware/auth.ts`
- Tests in `tests/middleware/auth.test.ts`

---

**Codebase verification findings:**
- ✓ Confirmed: Express app at `src/app.ts`, routes at `src/routes/`
- ✓ Confirmed: bcrypt@5.1.0 already installed
- + Discovered: Existing test helper at `tests/helpers/db.ts` for test DB setup
```

**THEN ask:**
"Is this plan approved? I can begin execution with `/gambit:execute-plan`."

### 5. After Approval

All Tasks are now created with proper dependencies.

```
TaskList
```

Shows:
- Task 1: pending, blockedBy: [] (ready)
- Task 2: pending, blockedBy: [task-1]
- Task 3: pending, blockedBy: [task-2]

Report: "Plan created. 3 tasks ready for execution. Run `/gambit:execute-plan` to begin."

## Task Granularity

**Each step is ONE action (2-5 minutes):**

1. "Write the failing test" — one step
2. "Run it to verify it fails" — one step
3. "Implement minimal code to pass" — one step
4. "Run tests to verify they pass" — one step
5. "Commit" — one step

**NOT:**
- "Implement authentication" (too big)
- "Add tests" (too vague)
- "Update the code" (meaningless)

## Anti-patterns

**Don't:**
- Write placeholders ("details above", "see requirements")
- Verify codebase yourself (use Explore agent)
- Write conditional steps ("if exists")
- Ask permission between subtasks
- Create vague tasks ("implement feature")

**Do:**
- Write complete code in every step
- Use Explore agent to verify assumptions
- Write definitive steps based on verification
- Continue automatically after approval
- Create bite-sized tasks (2-5 min each)

## Verification Checklist

Before presenting plan:
- [ ] Used Explore agent (not manual verification)
- [ ] All steps have complete code (no placeholders)
- [ ] All steps have exact file paths
- [ ] All steps have exact commands with expected output
- [ ] Dependencies set correctly with `TaskUpdate addBlockedBy`
- [ ] Each task is 2-5 minutes of work

## Integration

**This skill is called by:**
- `gambit:brainstorm` (after design approval)
- User via `/gambit:write-plan`

**This skill calls:**
- Explore agent (verify assumptions)
- `gambit:execute-plan` (offered after plan approval)

**Task tools used:**
- `TaskCreate` — Create epic and subtasks
- `TaskUpdate` — Set dependencies via `addBlockedBy`
- `TaskList` — Verify task structure
- `TaskGet` — Read task details
