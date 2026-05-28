---
name: prd-task
description: Use this skill to convert markdown PRDs into executable JSON format for autonomous task completion after creating a PRD with the prd skill.
---

# PRD Task Skill

Convert markdown PRDs to executable JSON format for autonomous task completion. The PRD defines the **end state** via tasks with verification steps, and the agent decides HOW to get there.

Based on [Anthropic's research on long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## Workflow

1. User requests: "Load the prd-task skill and convert prd-<name>.md"
2. Read the markdown PRD.
3. Extract tasks with verification steps.
4. Create `.opencode/state/<prd-name>/` directory.
5. Move markdown PRD to `.opencode/state/<prd-name>/prd.md`.
6. Output JSON to `.opencode/state/<prd-name>/prd.json`.
7. Create empty `.opencode/state/<prd-name>/progress.txt`.

### State Folder Structure

```
.opencode/state/<prd-name>/
├── prd.md       # Original markdown PRD (moved from project root)
├── prd.json     # Converted JSON for task execution
└── progress.txt # Empty file to track progress
```

## Input Format

Expects markdown PRD with end-state focus:

```markdown
# PRD: <Feature Name>

## End State

- [ ] Users can register
- [ ] Users can log in
- [ ] Auth is secure

## Tasks

### User Registration [functional]
User can register with email and password.

**Verification:**

- POST /api/auth/register with valid email/password
- Verify 201 response with user object
- Verify password not in response
- Attempt duplicate email, verify 409

### User Login [functional]
User can log in and receive JWT token.

**Verification:**

- POST /api/auth/login with valid credentials
- Verify 200 response with token
- Attempt invalid credentials, verify 401

## Context

### Patterns

- API routes: `src/routes/items.ts`

### Key Files

- `src/db/schema.ts`

### Non-Goals

- OAuth/social login
- Password reset
```

## Output Format

Move PRD and generate JSON in `.opencode/state/<prd-name>/`:

- `prd.md` - Original markdown (moved from source location)
- `prd.json` - Converted JSON:

```json
{
  "prdName": "<prd-name>",
  "tasks": [
    {
      "id": "functional-1",
      "category": "functional",
      "description": "User can register with email and password",
      "steps": [
        "POST /api/auth/register with valid email/password",
        "Verify 201 response with user object",
        "Verify password not in response",
        "Attempt duplicate email, verify 409"
      ]
    },
    {
      "id": "functional-2",
      "category": "functional",
      "description": "User can log in and receive JWT token",
      "steps": [
        "POST /api/auth/login with valid credentials",
        "Verify 200 response with token",
        "Attempt invalid credentials, verify 401"
      ]
    }
  ]
}
```