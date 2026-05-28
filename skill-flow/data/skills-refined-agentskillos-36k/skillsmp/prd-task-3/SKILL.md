---
name: prd-task
description: Convert markdown PRDs to executable JSON format. Use after creating a PRD with the prd skill to generate the prd.json for autonomous task completion.
---

# PRD Task Skill

Convert markdown PRDs to executable JSON format for autonomous task completion.

The PRD defines the **end state** via tasks with verification steps. The agent decides HOW to get there.

Based on [Anthropic's research on long-running agents](https://www.anthropic.com/engineering/effective-harnesses-long-running-agents).

## Workflow

1. User requests: "Load the prd-task skill and convert prd-<name>.md"
2. Read the markdown PRD
3. **Exhaustively analyze the current project** (see Project Analysis below)
4. Extract tasks with verification steps, informed by project analysis
5. Create `.opencode/state/<prd-name>/` directory
6. Move markdown PRD to `.opencode/state/<prd-name>/prd.md`
7. Output JSON to `.opencode/state/<prd-name>/prd.json`
8. Create empty `.opencode/state/<prd-name>/progress.txt`

## Project Analysis (CRITICAL)

Before converting PRD tasks, **exhaustively analyze the current project**. This ensures tasks account for existing state, patterns, and constraints.

### What to Check

#### 1. Project Documentation
- `AGENTS.md` (root and subdirectories) - coding standards, patterns, constraints
- `specs/` directory - detailed specifications, best practices, conventions (e.g., testing strategy, data access patterns, framework-specific guides)
- `README.md` - project overview, setup, architecture
- `CONTRIBUTING.md` - contribution guidelines
- `docs/` directory - additional documentation

#### 2. Project Status
- Existing implementation of related features
- Database schema state (migrations, existing tables)
- API routes already defined
- Components/modules that overlap with PRD scope
- Tests that already exist for related functionality

#### 3. Codebase Patterns
- File/folder naming conventions
- Code organization patterns (barrel exports, co-location)
- Error handling patterns
- Validation patterns (zod, io-ts, etc.)
- State management patterns
- Testing patterns (unit, integration, e2e)

#### 4. Technical Constraints
- Dependencies and their versions
- Framework-specific patterns (Next.js App Router vs Pages, etc.)
- Type definitions and shared types
- Environment configuration patterns

### How to Apply

1. **Mark tasks as already passing** if implementation already exists and meets verification steps
2. **Adjust verification steps** to align with existing patterns (e.g., if project uses zod, verification should expect zod validation)
3. **Add project-specific context** to `context.patterns` based on discovered patterns
4. **Flag conflicts** - if PRD conflicts with existing patterns/constraints, note in output
5. **Reference existing code** - include specific file paths in `context.keyFiles` that are relevant

### Output Enrichment

After analysis, the `context` object should include:

```json
{
  "context": {
    "patterns": ["discovered patterns from codebase analysis"],
    "keyFiles": ["files relevant to PRD tasks"],
    "nonGoals": ["from PRD"],
    "projectConstraints": ["constraints from AGENTS.md, README, etc."],
    "existingImplementation": ["what already exists that relates to PRD"]
  }
}
```

State folder structure:
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
      ],
      "passes": false
    }
  ],
  "context": {
    "patterns": ["API routes: src/routes/items.ts"],
    "keyFiles": ["src/db/schema.ts"],
    "nonGoals": ["OAuth/social login", "Password reset"],
    "projectConstraints": ["from AGENTS.md and project docs"],
    "existingImplementation": ["what already exists relevant to tasks"]
  }
}
```

## Schema Details

### Task Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier, e.g. "db-1", "api-auth", "setup-deps" |
| `category` | string | Grouping: "functional", "ui", "api", "security", "testing", etc. |
| `description` | string | What the task does when complete |
| `steps` | string[] | **Verification steps** - how to test it works |
| `passes` | boolean | Set to `true` when ALL steps verified |

### Key Points

- **Steps are verification, not implementation** - They describe HOW TO TEST, not how to build
- **Category is flexible** - Use what fits your codebase
- **ID format**: `<category>-<number>` or descriptive like `"api-auth"`, `"db-schema"`
- **Context helps agent explore** - Patterns and key files guide initial exploration

## Conversion Rules

### Task Sizing

Keep tasks small and focused:

- One logical change per task
- If a PRD section feels too large, break it into multiple tasks
- Prefer many small tasks over few large ones
- Each task should be completable in one commit

Quality over speed. Small steps compound into big progress.

### Tasks from Markdown
- Each `### Title [category]` becomes a task
- Generate `id` as `<category>-<number>` (e.g., "db-1", "api-2") or descriptive slug
- Text after title is the `description`
- Items under `**Verification:**` become `steps`
- `passes` always starts as `false`
- **Split large sections** into multiple focused tasks

### Context Preserved
- `context.patterns` - existing code patterns to follow (from PRD + discovered)
- `context.keyFiles` - files to explore first (from PRD + discovered)
- `context.nonGoals` - explicit scope boundaries
- `context.projectConstraints` - constraints from AGENTS.md, README, etc.
- `context.existingImplementation` - what already exists relevant to PRD

## Philosophy

This codebase will outlive you. Every shortcut becomes someone else's burden. Every hack compounds into technical debt that slows the whole team down.

You are not just writing code. You are shaping the future of this project. The patterns you establish will be copied. The corners you cut will be cut again.

Fight entropy. Leave the codebase better than you found it.

## Field Rules

**READ-ONLY except:**
- `passes`: Set to `true` when ALL verification steps pass

**NEVER edit or remove tasks** - This could lead to missing functionality.

## PRD Name

Derive from PRD title:
- `# PRD: User Authentication` -> `"prdName": "user-authentication"`

## After Conversion

Tell the user:

```
PRD converted and moved to .opencode/state/<prd-name>/
  - prd.md (moved from <original-path>)
  - prd.json (generated)
  - progress.txt (empty)

PRD: <prd-name>
Tasks: X total (Y already passing)
  - functional: N
  - testing: N

Project Analysis:
  - Constraints found: <count from AGENTS.md, etc.>
  - Existing implementation: <what already exists>
  - Patterns discovered: <key patterns>

Non-goals (excluded): <list>

Conflicts/Notes: <any PRD vs project conflicts>

To complete tasks:
  /complete-next-task <prd-name>

This will:
1. Get bearings (read progress, check history, verify environment)
2. Choose a task to implement
3. Implement until all verification steps pass
4. Commit and update progress
```

## Example

### Input: prd-favorites.md

```markdown
# PRD: User Favorites

## End State
- [ ] Users can favorite items
- [ ] Favorites persist
- [ ] Users can list favorites

## Tasks

### Favorites Storage [db]
Database table for storing favorites.

**Verification:**
- Favorites table exists with userId, itemId, createdAt
- Unique constraint prevents duplicates
- Foreign keys reference users and items tables

### Add Favorite [api]
User can add an item to favorites.

**Verification:**
- POST /api/favorites with itemId
- Verify 201 response
- Verify item appears in database
- Attempt duplicate, verify 409
- Attempt without auth, verify 401

### List Favorites [api]
User can retrieve their favorites.

**Verification:**
- GET /api/favorites returns array
- Results are paginated (20 per page)
- Results sorted by createdAt desc
- Only returns current user's favorites

## Context

### Patterns
- API routes: `src/routes/items.ts`
- Auth middleware: `src/middleware/auth.ts`

### Key Files
- `src/db/schema.ts`

### Non-Goals
- Favorite folders
- Sharing favorites
```

### Output: .opencode/state/user-favorites/

**prd.md** - Moved from `prd-favorites.md`

**progress.txt** - Empty file for tracking progress

**prd.json**:

```json
{
  "prdName": "user-favorites",
  "tasks": [
    {
      "id": "db-1",
      "category": "db",
      "description": "Database table for storing favorites",
      "steps": [
        "Favorites table exists with userId, itemId, createdAt",
        "Unique constraint prevents duplicates",
        "Foreign keys reference users and items tables"
      ],
      "passes": false
    },
    {
      "id": "api-1",
      "category": "api",
      "description": "User can add an item to favorites",
      "steps": [
        "POST /api/favorites with itemId",
        "Verify 201 response",
        "Verify item appears in database",
        "Attempt duplicate, verify 409",
        "Attempt without auth, verify 401"
      ],
      "passes": false
    },
    {
      "id": "api-2",
      "category": "api",
      "description": "User can retrieve their favorites",
      "steps": [
        "GET /api/favorites returns array",
        "Results are paginated (20 per page)",
        "Results sorted by createdAt desc",
        "Only returns current user's favorites"
      ],
      "passes": false
    }
  ],
  "context": {
    "patterns": [
      "API routes: src/routes/items.ts",
      "Auth middleware: src/middleware/auth.ts",
      "Zod validation on all inputs (discovered)",
      "Drizzle ORM for DB (discovered)"
    ],
    "keyFiles": [
      "src/db/schema.ts",
      "src/lib/validation.ts (discovered)",
      "src/routes/items.ts (reference pattern)"
    ],
    "nonGoals": ["Favorite folders", "Sharing favorites"],
    "projectConstraints": [
      "No any types (from AGENTS.md)",
      "All API routes require auth middleware"
    ],
    "existingImplementation": [
      "User table exists with id, email, createdAt",
      "Items table exists with id, name, userId"
    ]
  }
}
```
