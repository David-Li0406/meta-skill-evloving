---
name: flight-prd
description: Transform rough product ideas into atomic task queues. Use when starting a new project from a vague concept or feature request.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-prd

Transform a rough product idea into atomic tasks that can be executed one at a time through the Flight loop.

## Usage

```
/flight-prd <rough product idea> [--no-research]
```

## Arguments

- `$ARGUMENTS` - Rough product description, feature request, or problem statement

## Flags

| Flag | Behavior |
|------|----------|
| (none) | Full workflow including temporal research |
| `--no-research` | Skip dependency research (for experts or fast iteration) |

---

## The Problem This Solves

AI coding agents excel at **atomic, well-defined tasks** (1-2 hours). They struggle with:
- Large, interconnected systems
- Multi-day projects with many files
- Maintaining consistency across long sessions

A monolithic PRD like "Build an SMS document system" will fail. The agent will lose context, make inconsistent decisions, over-engineer, and produce code that doesn't fit together.

## The Solution: Atomic Task Decomposition

Instead of one big PRD, output a **task queue** that feeds the Flight loop:

```
/flight-prd "rough idea"
    ↓
[Step 2B: Temporal Research - automatic]
    ↓
PRD.md              # Vision (human reference)
MILESTONES.md       # Phases (human planning)
known-landmines.md  # Temporal issues discovered
tasks/
  001-project-setup.md  # Version pins from research
  002-database-schema.md
  003-auth-system.md
  ...
    ↓
/flight-prime tasks/001-project-setup.md
    ↓
/flight-compile
    ↓
PROMPT.md
    ↓
[Agent executes atomic task]
    ↓
npm run preflight          # Local CI (validate + lint)
    ↓
/flight-validate           # Full Flight validation
    ↓
[Human reviews, approves]
    ↓
/flight-prime tasks/002-database-schema.md
    ↓
... loop continues
```

---

## Process

### 0. Load Flight Context (MANDATORY FIRST)

**⚠️ CRITICAL: Do this FIRST, before any external research.**

Flight domain files contain project-specific rules that override external documentation.

1. **Read `.flight/FLIGHT.md`** - understand methodology and domain quick reference
2. **Scan available domains**:
   ```bash
   ls .flight/domains/*.md
   ```
3. **Match domains to planned tech stack**:
   - `code-hygiene.md` - ALWAYS (every task)
   - `scaffold.md` - if project setup uses create-vite, create-next-app, npm init, etc.
   - `react.md` - if React components
   - `typescript.md` - if TypeScript
   - `nextjs.md` - if Next.js
   - `python.md` - if Python
   - etc.
4. **Read matched domain files** to understand constraints BEFORE external research

**Why this order matters:**
- Priority: Domain files > Codebase patterns > External docs
- Domain MUST/NEVER rules are non-negotiable
- External research may contradict domain rules; domains win

### 1. Understand the Request

Parse the rough idea into:
- **Core problem**: What pain point?
- **Target users**: Who needs this?
- **Key capabilities**: What must it do (high level)?

### 2. Research Phase

Use available tools to ground the PRD in reality:

#### Web Search
- Competitor solutions
- Problem space articles
- Technology options
- **Queries**: `"{problem} solutions"`, `"best {category} tools"`, `"{competitor} alternatives"`

#### MCP Tools (if available)
Check your tool list for:
- `context7_*` → Use for framework/library documentation
- `firecrawl_*` → Use for competitor deep-dives

**If tools are missing but would help:**
```
NOTE: Better results with [Context7/Firecrawl]. Install from:
- Context7: https://github.com/upstash/context7
- Firecrawl: https://github.com/mendableai/firecrawl

Proceed with available tools, or install first?
```

### 2B. Dependency Temporal Research (AUTOMATIC)

**Skip this step only if `--no-research` flag was provided.**

Run `/flight-research` with the tech stack identified in Step 2. Pass dependencies explicitly - no files exist yet for auto-detection.

```
/flight-research {dep1} {dep2} {dep3} ...
```

**Example** (for a Next.js + Prisma + Auth.js project):
```
/flight-research next react prisma tailwindcss auth-js
```

Wait for research to complete. The output will include:
- Version recommendations with reasons
- `.flight/known-landmines.md` updates (if issues found)
- Research summary with date anchor

**Use the recommended versions when creating task files in Step 4.**

See `/flight-research` skill for the full research process (date anchoring, search queries, landmine management).

**Then continue with Step 3.**

### 3. Competitive Analysis

| Competitor | What They Do Well | Where They Fall Short |
|------------|-------------------|----------------------|
| ... | ... | ... |

### 4. Generate Outputs

Create THREE outputs:

#### A. `PRD.md` - The Vision

```markdown
# PRD: [Product Name]

## Problem Statement
[Specific problem. Who has it. Why current solutions fail.]

## Target Users
- Primary: [specific persona]
- Secondary: [specific persona]

## Core Value Proposition
[One sentence: what makes this different]

## Success Metrics
- [Measurable metric]: [Target]

## Competitive Landscape
[Brief summary of research findings]

## Technical Constraints
- [Constraint]: [Reason]

## Out of Scope (V1)
- [What this is NOT building]

## Research Sources
- [URL]: [Key finding]
```

#### B. `MILESTONES.md` - The Phases

```markdown
# Milestones

## M1: Foundation (Tasks 001-003)
Project setup, database schema, basic auth.
**Exit Criteria**: Can log in and see empty dashboard.
**Validation**: `.flight/validate-all.sh` should pass after each task.

## M2: Core Feature (Tasks 004-007)
[The main thing the product does]
**Exit Criteria**: [Specific testable outcome]
**Validation**: `.flight/validate-all.sh` should pass after each task.

## M3: Polish (Tasks 008-010)
Error handling, edge cases, UX improvements.
**Exit Criteria**: Ready for beta users.
**Validation**: `.flight/validate-all.sh` should pass after each task.
```

#### C. `tasks/` - Atomic Task Files

Create 8-15 task files, each following this structure:

```markdown
# Task [NNN]: [Short Name]

## Depends On
- [Task numbers that must complete first]
- OR "None (first task)"

## Delivers
- [Specific, concrete output 1]
- [Specific, concrete output 2]
- [Specific, concrete output 3]

## NOT In Scope (Critical)
- [Thing that seems related but is a different task]
- [Thing user might expect but we're deferring]
- [Adjacent feature that's Task XXX]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]
- [ ] Flight validation passes for files created/modified in this task

## Domain Constraints
Load these before starting:
- code-hygiene.md (always)
- [relevant-domain].md
- [relevant-domain].md

## Context
[Minimal context the agent needs for THIS task only.
Don't repeat the whole PRD. Just what's relevant.]

## Technical Notes
[Any specific technical decisions or patterns to follow.
Reference prior tasks if building on them.]

## Validation
Run after implementing:
```bash
# Validate specific files created in this task
.flight/domains/[domain].validate.sh path/to/created/files

# Or validate all (may show pre-existing issues in other files)
.flight/validate-all.sh
```
```

---

## Task Decomposition Rules

### Size Constraints

| Constraint | Limit |
|------------|-------|
| Maximum time | 2 hours of agent work |
| Maximum files | 5-7 files created/modified |
| If bigger | Split into multiple tasks |

### Dependency Rules
- Tasks should be **sequential** where possible
- Minimize parallel dependencies (harder to coordinate)
- Each task should work even if future tasks never happen

### Scope Rules
- **"NOT In Scope" is the most important section**
- Be explicit about what's adjacent but excluded
- Reference which task WILL handle deferred items

### Domain Constraints Discovery

For each task, the "Domain Constraints" section MUST:
1. Always include `code-hygiene.md`
2. Include domains matching the task's tech (from FLIGHT.md Domain Quick Reference)
3. Include `scaffold.md` for ANY task that creates/initializes project structure
4. Be based on actual `.flight/domains/` contents, not assumptions

**Anti-pattern:** Guessing domains based on keywords
**Correct:** Reading FLIGHT.md table + scanning `.flight/domains/`

### Key Domain Mappings

| Task Type | Required Domains |
|-----------|------------------|
| Project setup (create-vite, npm init, etc.) | `code-hygiene.md`, `scaffold.md` |
| React components | `code-hygiene.md`, `react.md` |
| TypeScript files | `code-hygiene.md`, `typescript.md` |
| Next.js routes/pages | `code-hygiene.md`, `nextjs.md`, `react.md` |
| Database/SQL | `code-hygiene.md`, `sql.md` |
| API endpoints | `code-hygiene.md`, `api.md` (if exists) |
| Python code | `code-hygiene.md`, `python.md` |

Always verify against actual `.flight/domains/` contents.

### Flight Local CI Setup (Task 001 MUST include)

Every `001-project-setup` task MUST configure Flight as local CI:

1. **Use scaffolding tools with linting enabled**:
   ```bash
   # Next.js - include --eslint flag
   npx create-next-app my-app --typescript --tailwind --app --eslint

   # Vite - add ESLint after
   npm create vite@latest my-app -- --template react-ts
   npm install -D eslint @eslint/js typescript-eslint
   npx eslint --init
   ```

2. **Add scripts to package.json**:
   ```json
   {
     "scripts": {
       "lint": "eslint .",
       "validate": ".flight/validate-all.sh",
       "preflight": "npm run validate && npm run lint"
     }
   }
   ```
   Note: `lint` script may already exist from scaffolding. Verify it works.

3. **Include in acceptance criteria**:
   - `npm run lint` works (ESLint configured)
   - `package.json has validate and preflight scripts`
   - `npm run validate passes`
   - `npm run preflight passes`

### Naming Convention

```
tasks/
  001-project-setup.md       # Always first
  002-database-schema.md     # Data layer early
  003-auth-basic.md          # Auth before features
  004-[core-feature-1].md
  005-[core-feature-2].md
  ...
  0XX-error-handling.md      # Polish later
  0XX-testing.md             # Near end
```

---

## Example Decomposition

**Input**: `/flight-prd Document collection via SMS - encrypted storage`

### tasks/001-project-setup.md
```markdown
# Task 001: Project Setup

## Depends On
- None (first task)

## Delivers
- Next.js 14 project with App Router (use --eslint flag)
- Supabase project connected
- Environment variables configured
- Basic layout component
- ESLint configured and working
- Flight local CI configured in package.json

## NOT In Scope
- Authentication (Task 003)
- Database tables (Task 002)
- Any business logic
- Styling beyond basic layout

## Acceptance Criteria
- [ ] `npm run dev` starts without errors
- [ ] `/` route renders "Hello World"
- [ ] `supabase status` shows connection
- [ ] .env.local has SUPABASE_URL and SUPABASE_ANON_KEY
- [ ] `npm run lint` works (ESLint configured)
- [ ] package.json has `validate` and `preflight` scripts
- [ ] `npm run validate` passes
- [ ] `npm run preflight` passes

## Domain Constraints
- code-hygiene.md (always)
- scaffold.md (project initialization)
- nextjs.md
- typescript.md

## Flight Setup (REQUIRED for Task 001)

1. Use scaffolding with ESLint:
```bash
npx create-next-app my-app --typescript --tailwind --app --eslint
```

2. Add/verify scripts in package.json:
```json
{
  "scripts": {
    "lint": "next lint",
    "validate": ".flight/validate-all.sh",
    "preflight": "npm run validate && npm run lint"
  }
}
```

## Validation
Run after implementing:
```bash
npm run preflight    # Must pass before moving to next task
```
```

### tasks/002-database-schema.md
```markdown
# Task 002: Database Schema

## Depends On
- 001-project-setup

## Delivers
- users table (id, email, created_at)
- documents table (id, user_id, filename, encrypted_url, created_at)
- upload_links table (id, user_id, token, expires_at, used_at)
- RLS policies for all tables
- Indexes on foreign keys

## NOT In Scope
- Authentication logic (Task 003)
- File upload handling (Task 005)
- SMS sending (Task 004)
- Any API routes

## Acceptance Criteria
- [ ] All tables created in Supabase
- [ ] RLS enabled on all tables
- [ ] Can insert test row via SQL editor
- [ ] Foreign key indexes exist
- [ ] `.flight/validate-all.sh` passes

## Domain Constraints
- code-hygiene.md (always)
- sql.md

## Technical Notes
Use snake_case for columns. user_id references auth.users().

## Validation
Run after implementing:
```bash
.flight/validate-all.sh    # Must pass before moving to next task
```
```

### tasks/003-auth-basic.md
```markdown
# Task 003: Basic Authentication

## Depends On
- 001-project-setup
- 002-database-schema

## Delivers
- /login page with email/password
- /signup page
- Auth middleware protecting /dashboard
- useAuth hook
- Logout functionality

## NOT In Scope
- Magic links (future enhancement)
- OAuth providers (future enhancement)
- Password reset (Task 008)
- Profile editing

## Acceptance Criteria
- [ ] Can create account at /signup
- [ ] Can log in at /login
- [ ] /dashboard redirects to /login if not authenticated
- [ ] Logout clears session
- [ ] `.flight/validate-all.sh` passes

## Domain Constraints
- code-hygiene.md (always)
- nextjs.md
- react.md
- typescript.md

## Validation
Run after implementing:
```bash
.flight/validate-all.sh    # Must pass before moving to next task
```
```

*[Continue for all tasks...]*

---

## Critical Rules

1. **READ FLIGHT CONTEXT FIRST** - Load FLIGHT.md and scan domains before any research
2. **RESEARCH AFTER DOMAIN DISCOVERY** - External docs may conflict; domains are authoritative
3. **TASKS MUST BE ATOMIC** - If you can't do it in 2 hours, split it
4. **"NOT IN SCOPE" IS SACRED** - This prevents the agent from scope creeping
5. **DEPENDENCIES FLOW FORWARD** - Task 005 can depend on 001-004, not on 006
6. **EACH TASK IS SELF-CONTAINED** - Include enough context to execute without re-reading PRD
7. **ACCEPTANCE CRITERIA ARE TESTABLE** - "Works well" is bad. "Returns 200 on GET /api/users" is good
8. **ALWAYS INCLUDE DOMAIN CONSTRAINTS** - Based on FLIGHT.md table and actual `.flight/domains/` contents
9. **INCLUDE scaffold.md FOR PROJECT SETUP** - Prevents destructive overwrites of project infrastructure
10. **NUMBER TASKS WITH PADDING** - 001, 002... not 1, 2 (sorting matters)
11. **validate-all.sh IN ACCEPTANCE CRITERIA** - Local CI must pass before moving to next task
12. **TASK 001 CONFIGURES FLIGHT CI** - ESLint + validate/preflight scripts in package.json

---

## Checklist Before Finishing

### Flight Context
- [ ] Read `.flight/FLIGHT.md` first
- [ ] Scanned `.flight/domains/*.md` to discover available domains
- [ ] Matched domains to tech stack before external research

### Research
- [ ] At least 3 competitors analyzed
- [ ] Tech stack decisions grounded in research
- [ ] Sources cited in PRD.md

### Temporal Research (unless --no-research)
- [ ] `/flight-research` was run and completed
- [ ] Recommended versions from research used in task files

### Decomposition
- [ ] 8-15 tasks (not too few, not too many)
- [ ] No task exceeds 2-hour estimate
- [ ] Dependencies are linear where possible
- [ ] Every task has "NOT In Scope" section

### Task Quality
- [ ] Each task has 3-5 acceptance criteria
- [ ] All acceptance criteria are testable
- [ ] All tasks include `.flight/validate-all.sh` passes in acceptance criteria
- [ ] Domain constraints based on actual `.flight/domains/` contents
- [ ] `scaffold.md` included for project setup tasks
- [ ] Task 001 includes Flight CI setup (ESLint + validate/preflight scripts)
- [ ] Context section is minimal but sufficient

### Workflow Ready
- [ ] tasks/ directory created
- [ ] .flight/known-landmines.md created/updated (if issues found)
- [ ] User knows to run `/flight-prime tasks/001-*.md` next
- [ ] User knows to run `.flight/validate-all.sh` after each task
- [ ] MILESTONES.md shows the journey

---

## Output: Summary Report

After running `/flight-prd`, report:

```markdown
## Created

- **PRD.md** - Product vision (for reference)
- **MILESTONES.md** - [X] milestones, [Y] tasks total
- **.flight/known-landmines.md** - Temporal issues discovered (if any)
- **tasks/**
  - 001-project-setup.md (with version pins from research)
  - 002-database-schema.md
  - ...

## Temporal Research Summary

📅 **Research Date:** {date}

| Package | Recommended | Reason |
|---------|-------------|--------|
| next | 15.1.0 | Stable |
| prisma | 5.22.0 | v6.x has migration issues |
| auth-js | 5.x | v5 API (not v4 tutorials) |
| tailwindcss | 3.4.0 | v4 has PostCSS breaking changes |

⚠️ **Landmines:** {count} issues documented (see `.flight/known-landmines.md`)

## Workflow for Each Task

```
/flight-prime tasks/001-project-setup.md    # Research & compile
/flight-compile                             # Create atomic prompt
[implement]
npm run preflight                           # Local CI (validate + lint)
/flight-validate                            # Full Flight validation
[review and approve]
/flight-prime tasks/002-[next].md           # Next task
```

## Notes

- Temporal research was performed automatically (versions pinned in tasks)
- Task 001 will configure local CI: ESLint + Flight validation
- After Task 001: use `npm run preflight` (runs validate + lint)
- This catches issues before they hit remote CI or code review
```

---

## When to Use

| Starting Point | Use This? |
|----------------|-----------|
| Vague product idea | Yes |
| Feature request | Yes |
| "Build me a..." request | Yes |
| Clear task description | No → Use `/flight-prime` directly |
| Existing PRD document | No → Use `/flight-prime` directly |
| Have code, need validation | No → Use `/flight-validate` |

---

## Next Step

After `/flight-prd` completes (including temporal research):

**Begin the Flight loop:**

```
/flight-prime tasks/001-project-setup.md
```

**Workflow**: `/flight-prd` → `/flight-prime` → `/flight-compile` → [implement] → `/flight-validate` → repeat

| Response | Action |
|----------|--------|
| `continue` or `c` | Proceed to `/flight-prime tasks/001-*.md` |
| `review` | Display the generated task files for review |
| Task filename | Prime that specific task (e.g., `tasks/002-*.md`) |

**Note:** `/flight-research` is still available standalone for:
- Existing projects needing dependency validation
- Adding new dependencies mid-project
- Re-checking stale landmines (>3 months old)
