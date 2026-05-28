---
name: Development Workflow
description: |
  Use this skill when the user asks to implement/build/create a feature, or asks about development process, git workflow, or planning. Triggers on: "implement feature", "build feature", "add feature", "create feature", "how do I implement", "git workflow", "branching strategy", "commit conventions".
version: 1.0.0
---

# Development Workflow

## Feature Implementation Flow (REQUIRED)

**When user requests a feature, ALWAYS follow this flow:**

```
1. Story    → Create user story in .claude/project/features/
2. Plan     → Create plan in .claude/project/plans/
3. Approve  → Get user approval before coding
4. Build    → Implement following the plan
5. Complete → Update tracking files, commit
```

**If no story exists:** Create one first, update high-level-user-stories.md
**If no plan exists:** Create one, validate, get approval
**Never start coding without approved plan**

### File Naming Conventions

| Type  | Path                                      | Example                |
| ----- | ----------------------------------------- | ---------------------- |
| Story | `.claude/project/features/us-XXX-name.md` | `us-001-user-login.md` |
| Plan  | `.claude/project/plans/us-XXX-plan.md`    | `us-001-plan.md`       |

- **Filenames:** lowercase (`us-001`)
- **Display:** UPPERCASE (`US-001`)

### Auto-Increment User Story IDs

When creating a new user story:

1. Read `high-level-user-stories.md` to find the highest US-XXX number
2. Use the next number (e.g., if US-003 exists, use US-004)
3. If user specifies a number, use that instead

### After Creating Files

**After creating a user story:**

1. Update `high-level-user-stories.md` table with new entry
2. Update Overview counts
3. Set initial status to 'Planned'

**After creating a plan:**

1. Link plan in `high-level-user-stories.md` Plan column
2. Update Overview counts if needed

**After completing a feature:**

1. Update story status in `high-level-user-stories.md`
2. Add commit hash to the story
3. Update `roadmap.md` phase progress

---

## Workflow Commands

| Command                  | Phase         |
| ------------------------ | ------------- |
| `/implement`             | Full workflow |
| `/discovery`             | Requirements  |
| `/plan-and-validate`     | Planning      |
| `/start-implementation`  | Building      |
| `/review-implementation` | Code review   |
| `/next`                  | Continue      |

---

## Quick Process (10 Steps)

1. **Standards** - Read skills for domain patterns
2. **Requirements** - Write user story with acceptance criteria
3. **Discovery** - Explore codebase, find patterns
4. **Plan** - Create validated implementation plan
5. **Design** - Component hierarchy, data models
6. **Database** - Migrations, API endpoints
7. **Build** - Implement following patterns
8. **States** - Handle loading/error/empty/success
9. **Test** - Write tests, verify edge cases
10. **Commit** - Follow git conventions

---

## Git Conventions

**Branches:**

- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `hotfix/<name>` - Urgent fixes
- `chore/<name>` - Maintenance

**Commits:** Conventional Commits format

```
<type>: <subject>

<body>
```

**Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`

**Example:**

```bash
git commit -m "feat: add user authentication

- Login and register endpoints
- JWT token generation
- Tests: 90% coverage"
```

---

## Plan Structure (10 Sections)

1. Requirements Summary
2. Technical Approach
3. Database Changes
4. API Layer
5. Component Architecture
6. State Management
7. Edge Cases & Error Handling
8. Testing Strategy
9. Implementation Checklist
10. Effort & Risks

---

## Pre-Commit Checklist

- [ ] Lint passes
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Edge cases handled
- [ ] Story status updated
- [ ] high-level-user-stories.md updated
