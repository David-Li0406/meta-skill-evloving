# Feature Issue Template (Hierarchical)

Use this template for multi-phase work requiring breakdown into subtasks.

## CRITICAL: Creating Sub-Issues with `parentId`

When creating hierarchical issues, **you MUST use the `parentId` parameter**:

```
mcp__linear-server__create_issue:
  title: "Task title"
  team: "Team Name"
  parentId: "PARENT-ISSUE-UUID"  ← Use the parent's UUID, not identifier!
```

**DO NOT use `relatedTo`** - that creates a "related" relationship, not parent-child.

| Relationship | Parameter | Result |
|--------------|-----------|--------|
| **Sub-issue (child)** | `parentId` | Appears nested under parent ✓ |
| Related issue | `relatedTo` | Appears in "Related" section |
| Blocking | `blockedBy` / `blocks` | Shows dependency |

**Workflow:**
1. Create root feature issue first → get its `id` (UUID)
2. Create phase issues with `parentId: "<root-uuid>"`
3. Create task issues with `parentId: "<phase-uuid>"`

---

## Root Feature Template

```markdown
**Title:** [Feature] {Feature Name}
**Labels:** feature
**Priority:** High

## Goal
{One sentence describing the outcome}

## Context (Auto-gathered)
**Codebase analysis:**
- Existing patterns: {what was found}
- Related code: {file paths}
- Dependencies: {external services, packages}

## Success Criteria
- [ ] {Measurable criterion}
- [ ] {Measurable criterion}

## Phases
1. {Phase name} - {brief description}
2. {Phase name} - {brief description}
3. Verification - {how to verify complete}

## Architecture
{Based on codebase patterns - data flow, component structure, etc.}
```

## Phase Template

```markdown
**Title:** [Phase N] {Phase Name}
**Labels:** phase
**Parent:** {Feature ID}

## Objective
{What this phase accomplishes}

## Tasks
{List of atomic tasks - created as sub-issues}

## Dependencies
{What must be complete before this phase}

## Deliverable
{What's produced at end of this phase}
```

## Atomic Task Template

Every leaf task must be immediately executable:

```markdown
**Title:** {Action verb} {component}
**Labels:** task
**Parent:** {Phase ID}

## Action
{Exactly what to do - single unit of work}

## File
`{exact/path/to/file.ts}`

## Context
```{language}
{Relevant existing code}
```

## Implementation
```{language}
{Code to write - or description if complex}
```

## Verify
```bash
{command}
# Expected: {result}
```
```

## Example

**User says:** "Build a notification system"

**Created hierarchy:**

```
ENG-100: [Feature] Notification System
├── ENG-101: [Phase 1] Data Layer
│   ├── ENG-102: Create Notification model in Prisma schema
│   ├── ENG-103: Add notification repository with CRUD operations
│   └── ENG-104: Write migration for notifications table
├── ENG-105: [Phase 2] API Layer
│   ├── ENG-106: Create GET /notifications endpoint
│   ├── ENG-107: Create POST /notifications/mark-read endpoint
│   └── ENG-108: Add notification WebSocket events
├── ENG-109: [Phase 3] UI Layer
│   ├── ENG-110: Create NotificationBell component
│   ├── ENG-111: Create NotificationList dropdown
│   └── ENG-112: Add notification toast for real-time updates
└── ENG-113: [Phase 4] Verification
    ├── ENG-114: Integration tests for notification flow
    └── ENG-115: Manual E2E verification
```

**Root issue (ENG-100):**
```markdown
**Title:** [Feature] Notification System
**Labels:** feature
**Priority:** High

## Goal
Users receive real-time notifications for important events.

## Context (Auto-gathered)
**Codebase analysis:**
- Existing patterns: Uses Prisma ORM, Next.js API routes, React Query
- Related code: `src/lib/prisma.ts`, `src/pages/api/`, `src/components/ui/`
- Dependencies: Prisma, Socket.io (already installed)

## Success Criteria
- [ ] Users see unread notification count
- [ ] Clicking bell shows notification list
- [ ] Real-time updates without page refresh
- [ ] Mark as read functionality works

## Phases
1. Data Layer - Database schema and repository
2. API Layer - REST endpoints and WebSocket
3. UI Layer - Components and real-time updates
4. Verification - Tests and manual verification

## Architecture
```
User Action → API → Database
                ↓
            WebSocket → UI Update
```
```

**Atomic task (ENG-102):**
```markdown
**Title:** Create Notification model in Prisma schema
**Labels:** task
**Parent:** ENG-101

## Action
Add Notification model to Prisma schema with required fields.

## File
`prisma/schema.prisma`

## Context
```prisma
// Existing User model
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
}
```

## Implementation
```prisma
model Notification {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  type      String
  title     String
  message   String
  read      Boolean  @default(false)
  createdAt DateTime @default(now())

  @@index([userId, read])
}
```

## Verify
```bash
npx prisma validate
# Expected: No errors
```
```
