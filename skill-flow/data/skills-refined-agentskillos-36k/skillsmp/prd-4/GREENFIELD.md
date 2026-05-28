---
name: prd-greenfield
description: "Generate a PRD for a new greenfield project (building from scratch). Use when starting a completely new project with no existing codebase."
---

# PRD Generator - Greenfield Projects

Create detailed Product Requirements Documents for **new projects** built from scratch, including architecture decisions and technology selection.

---

## The Job

1. Receive a feature/project description from the user
2. Ask 3-5 essential clarifying questions (with lettered options) focused on **architecture and technology choices**
3. Generate a structured PRD with technology recommendations
4. Save to `tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 1: Clarifying Questions (Greenfield-Specific)

For greenfield projects, focus on foundational decisions:

### Architecture Questions:
```
1. What type of application is this?
   A. Web application (full-stack)
   B. API/Backend service only
   C. CLI tool
   D. Mobile app (React Native/Flutter)
   E. Desktop app (Electron/Tauri)

2. What is your preferred tech stack?
   A. TypeScript + Node.js (Express/Fastify)
   B. TypeScript + Next.js (React)
   C. Python + FastAPI/Django
   D. Go
   E. Rust
   F. Let me recommend based on requirements

3. What database approach?
   A. PostgreSQL (relational)
   B. MongoDB (document)
   C. SQLite (simple/embedded)
   D. No database needed
   E. Let me recommend based on requirements

4. What is the deployment target?
   A. Serverless (Vercel/AWS Lambda)
   B. Containers (Docker/Kubernetes)
   C. Traditional server (VPS)
   D. Local only (development tool)

5. What is the scope for v1?
   A. Minimal viable product (core features only)
   B. Feature-complete first version
   C. Proof of concept / prototype
```

This lets users respond with "1A, 2B, 3A, 4A, 5A" for quick iteration.

---

## Step 2: PRD Structure (Greenfield)

Generate the PRD with these sections:

### 1. Introduction/Overview
Brief description of the project and the problem it solves.

### 2. Goals
Specific, measurable objectives (bullet list).

### 3. Technology Stack (Greenfield-Specific)
Document the chosen technologies:
- **Runtime:** Node.js 20+ / Python 3.12+ / etc.
- **Framework:** Next.js 14 / FastAPI / etc.
- **Database:** PostgreSQL + Prisma / etc.
- **Authentication:** NextAuth / Clerk / etc.
- **Deployment:** Vercel / Docker / etc.

**Rationale:** Brief explanation of why these choices fit the project.

### 4. Project Structure (Greenfield-Specific)
Recommended directory structure:
```
project-name/
├── src/
│   ├── app/           # Routes/pages
│   ├── components/    # UI components
│   ├── lib/           # Utilities
│   └── server/        # Server-side code
├── prisma/            # Database schema
├── tests/             # Test files
└── package.json
```

### 5. User Stories
Each story needs:
- **Title:** Short descriptive name
- **Description:** "As a [user], I want [feature] so that [benefit]"
- **Acceptance Criteria:** Verifiable checklist

**Important for Greenfield:** Include setup/scaffolding stories first:

```markdown
### US-001: Project Setup
**Description:** As a developer, I need the project scaffolded with the chosen tech stack.

**Acceptance Criteria:**
- [ ] Initialize project with package.json/requirements.txt
- [ ] Configure TypeScript/linting (if applicable)
- [ ] Set up basic project structure
- [ ] Add development scripts (dev, build, test)
- [ ] Typecheck passes

### US-002: Database Schema Setup
**Description:** As a developer, I need the initial database schema configured.

**Acceptance Criteria:**
- [ ] Install and configure ORM (Prisma/Drizzle/etc.)
- [ ] Create initial schema with core models
- [ ] Generate and run initial migration
- [ ] Typecheck passes
```

### 6. Functional Requirements
Numbered list of specific functionalities (FR-1, FR-2, etc.).

### 7. Non-Goals (Out of Scope)
What this v1 will NOT include. Critical for greenfield to prevent scope creep.

### 8. Technical Considerations
- Performance requirements
- Security considerations
- Scalability expectations
- Testing strategy

### 9. Success Metrics
How will success be measured?

### 10. Open Questions
Remaining questions or areas needing clarification.

---

## Story Ordering for Greenfield

**Always order stories in this sequence:**

1. **Setup stories** - Project scaffolding, tooling
2. **Schema stories** - Database models, migrations
3. **Core backend** - Essential APIs/services
4. **Basic UI** - Minimal working interface
5. **Feature completion** - Additional functionality
6. **Polish** - Error handling, edge cases

---

## Writing for Greenfield Implementation

Since there's no existing code:

- Be explicit about file locations and naming conventions
- Specify exact package versions when critical
- Include setup commands in acceptance criteria
- Reference official documentation for complex setups
- Keep initial stories focused on "walking skeleton" - get something working end-to-end first

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)

---

## Example PRD (Greenfield)

```markdown
# PRD: Task Management API

## Introduction

A RESTful API for managing tasks and projects, built as a backend service for multiple client applications. Focuses on simplicity and clean API design.

## Goals

- Provide CRUD operations for tasks and projects
- Support user authentication via API keys
- Enable filtering and sorting of tasks
- Maintain sub-100ms response times

## Technology Stack

- **Runtime:** Node.js 20 LTS
- **Framework:** Fastify (performance-focused)
- **Database:** PostgreSQL 15 + Prisma ORM
- **Validation:** Zod
- **Testing:** Vitest
- **Deployment:** Docker container

**Rationale:** Fastify chosen for its speed and TypeScript support. Prisma provides type-safe database access. Zod ensures runtime validation matches TypeScript types.

## Project Structure

```
task-api/
├── src/
│   ├── routes/        # API route handlers
│   ├── services/      # Business logic
│   ├── schemas/       # Zod validation schemas
│   └── index.ts       # App entry point
├── prisma/
│   └── schema.prisma  # Database schema
├── tests/
└── package.json
```

## User Stories

### US-001: Project Scaffolding
**Description:** As a developer, I need the project initialized with Fastify and TypeScript.

**Acceptance Criteria:**
- [ ] Initialize npm project with TypeScript
- [ ] Install Fastify, @fastify/type-provider-zod
- [ ] Configure tsconfig.json for strict mode
- [ ] Add scripts: dev, build, start, test
- [ ] Create src/index.ts with basic server
- [ ] Server starts on port 3000
- [ ] Typecheck passes

### US-002: Database Setup
**Description:** As a developer, I need PostgreSQL configured with Prisma.

**Acceptance Criteria:**
- [ ] Install Prisma and initialize
- [ ] Create schema with Task model (id, title, description, status, createdAt, updatedAt)
- [ ] Generate Prisma client
- [ ] Run initial migration
- [ ] Typecheck passes

### US-003: Create Task Endpoint
**Description:** As an API consumer, I want to create new tasks via POST /tasks.

**Acceptance Criteria:**
- [ ] POST /tasks accepts { title, description? }
- [ ] Returns 201 with created task
- [ ] Returns 400 for invalid input
- [ ] Task persisted to database
- [ ] Typecheck passes
- [ ] Tests pass

### US-004: List Tasks Endpoint
**Description:** As an API consumer, I want to list all tasks via GET /tasks.

**Acceptance Criteria:**
- [ ] GET /tasks returns array of tasks
- [ ] Supports ?status= filter
- [ ] Supports ?sort=createdAt query param
- [ ] Returns empty array when no tasks
- [ ] Typecheck passes
- [ ] Tests pass

## Functional Requirements

- FR-1: All endpoints return JSON with consistent error format
- FR-2: Task status enum: 'pending' | 'in_progress' | 'done'
- FR-3: All timestamps in ISO 8601 format
- FR-4: Request validation via Zod schemas

## Non-Goals (v1)

- User authentication (use API keys in v2)
- Real-time updates (WebSocket in v2)
- File attachments
- Task assignments

## Technical Considerations

- Use connection pooling for database
- Implement request logging
- Add health check endpoint
- Configure CORS for development

## Success Metrics

- All CRUD operations work correctly
- Response times under 100ms
- Zero TypeScript errors
- 80%+ test coverage

## Open Questions

- Should we add rate limiting in v1?
- What's the maximum title length?
```

---

## Security: No Hardcoded Secrets

If the user's description mentions specific passwords, API keys, tokens, or credentials:

1. **NEVER put literal credentials in the PRD or acceptance criteria**
2. **Convert to environment variables:** e.g. "password 12345678" → "use `ADMIN_PASSWORD` from environment"
3. **Use `.env.example` pattern:** Document required env vars with placeholder values
4. **Seed data:** For initial users/admin accounts, reference env vars: `ADMIN_EMAIL`, `ADMIN_PASSWORD`

**Example transformation:**
- User says: "make user admin@foo.com with password secret123"
- PRD says: "Create admin seed using `ADMIN_EMAIL` and `ADMIN_PASSWORD` env vars, documented in `.env.example`"

---

## Checklist

Before saving the PRD:

- [ ] Asked architecture/tech stack questions
- [ ] Incorporated user's technology preferences
- [ ] Included Technology Stack section
- [ ] Included Project Structure section
- [ ] First stories are setup/scaffolding
- [ ] User stories are small and specific
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear v1 boundaries
- [ ] **No hardcoded secrets** - credentials use env vars
- [ ] Saved to `tasks/prd-[feature-name].md`
