# File Structure Templates

Templates for all spec files created by the feature development workflow.

## Directory Structure

```
.works/spec/{feature-name}/
├── progress.md        # Progress tracking (YAML + markdown)
├── README.md          # Index + core decisions
├── contracts.md       # Data contracts (input/output/API)
├── tasks.md           # Task breakdown with status
└── PR.md              # PR description template
```

---

## progress.md Template

```markdown
---
feature: {feature-name}
phase: 1
phase_name: discovery
status: in_progress
branch: feat/{feature-name}
started_at: 2025-01-13T10:00:00Z
updated_at: 2025-01-13T10:00:00Z
decisions:
  - id: Q1
    question: What format for API response?
    answer: JSON with pagination
  - id: Q2
    question: Caching strategy?
    answer: Redis with 5min TTL
completed_phases:
  - phase: 1
    completed_at: 2025-01-13T11:00:00Z
    artifacts:
      - README.md
---

# Progress: {Feature Name}

## Current State
- **Phase**: 2 - Codebase Exploration
- **Status**: In Progress
- **Last Updated**: 2025-01-13 11:00

## Completed Phases

### Phase 1: Discovery ✅
- Completed: 2025-01-13 11:00
- Decisions: Q1-Q3 recorded in README.md

## Pending Phases
- [x] Phase 1: Discovery
- [ ] Phase 2: Codebase Exploration (current)
- [ ] Phase 3: Documentation & Tasks
- [ ] Phase 4: Implementation
- [ ] Phase 5: Review & PR

## Resume Context
<!-- Essential info for session recovery -->
- Last action: Launched codebase-explorer agents
- Blocking issues: None
- Next steps: Wait for agent results, synthesize findings

## Decision Log
- Q1: API format → JSON with pagination
- Q2: Caching → Redis 5min TTL
- Q3: Auth → JWT with refresh tokens
```

### YAML Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| feature | string | Feature identifier (kebab-case) |
| phase | number | Current phase (1-5) |
| phase_name | string | Phase name (discovery/exploration/documentation/implementation/review) |
| status | string | in_progress / completed / blocked |
| branch | string | Git branch name |
| started_at | ISO8601 | Start timestamp |
| updated_at | ISO8601 | Last update timestamp |
| decisions | array | List of {id, question, answer} |
| completed_phases | array | List of {phase, completed_at, artifacts} |

---

## README.md Template

```markdown
# {Feature Name}

> Goal: [One sentence describing the problem this solves]
> Scope: [What's included / what's NOT included]

## Core Decisions

- Q1: **[Choice]** - [brief explanation]
- Q2: **[Choice]** - [brief explanation]
- Q3: **[Choice]** - [brief explanation]

## Document Navigation

- Progress: `progress.md`
- Data Contracts: `contracts.md`
- Task Breakdown: `tasks.md`

## Execution Guide

- To check current state: read `progress.md`
- To modify a module: check `tasks.md` for the corresponding task
- To modify fields/API: refer to `contracts.md` as source of truth

## Architecture Overview

[High-level diagram or description of the feature architecture]

## Key Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| Schema | `shared/schemas/` | Zod definitions |
| Service | `functions/services/` | Business logic |
| Route | `functions/routes/` | API handlers |
| Component | `src/components/` | UI elements |
```

---

## contracts.md Template

```markdown
# {Feature Name} Data Contracts

> This document defines input/output contracts to ensure doc-code consistency.

## 1. Input Contracts

### 1.1 User Input

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | yes | 1-100 chars |
| email | string | yes | valid email |
| count | number | no | 1-1000, default 10 |

### 1.2 Query Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | number | 1 | Page number |
| limit | number | 20 | Items per page |

## 2. Output Contracts

### 2.1 Response Structure

```typescript
interface FeatureResponse {
  success: boolean;
  data: FeatureData;
  meta: {
    page: number;
    totalPages: number;
    totalItems: number;
  };
}

interface FeatureData {
  id: string;
  name: string;
  createdAt: string;
  // ... other fields
}
```

### 2.2 Example Response

```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "name": "Example",
    "createdAt": "2025-01-13T10:00:00Z"
  },
  "meta": {
    "page": 1,
    "totalPages": 5,
    "totalItems": 100
  }
}
```

## 3. API Contracts

### 3.1 Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/feature` | Create item | Required |
| GET | `/api/feature/:id` | Get item | Required |
| PUT | `/api/feature/:id` | Update item | Required |
| DELETE | `/api/feature/:id` | Delete item | Admin |

### 3.2 Error Responses

| Code | Error | Description |
|------|-------|-------------|
| 400 | INVALID_INPUT | Validation failed |
| 401 | UNAUTHORIZED | Authentication required |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 500 | INTERNAL_ERROR | Server error |

### 3.3 Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```
```

---

## tasks.md Template

```markdown
# {Feature Name} Tasks

> Update status after each task completion.

## Summary

| Task | Size | Status |
|------|------|--------|
| T1: Schema definition | S | pending |
| T2: Service implementation | M | pending |
| T3: API routes | M | pending |
| T4: Frontend integration | L | pending |

---

## T1: Schema Definition

**Goal**: Define Zod schemas for input validation
**Size**: S (30min)
**Dependencies**: None
**Files**:
- [ ] `shared/schemas/feature.schema.ts`

**Acceptance**:
- [ ] Input schema with all validations
- [ ] Output type exports
- [ ] Unit tests pass

**Status**: pending

---

## T2: Service Implementation

**Goal**: Implement core business logic
**Size**: M (1-2h)
**Dependencies**: T1
**Files**:
- [ ] `functions/services/feature.service.ts`
- [ ] `functions/services/feature.service.test.ts`

**Acceptance**:
- [ ] CRUD operations implemented
- [ ] Error handling complete
- [ ] Tests written and passing

**Status**: pending

---

## T3: API Routes

**Goal**: Create REST endpoints
**Size**: M (1-2h)
**Dependencies**: T1, T2
**Files**:
- [ ] `functions/routes/feature.ts`

**Acceptance**:
- [ ] All endpoints from contracts.md implemented
- [ ] Request validation using schemas
- [ ] Proper error responses

**Status**: pending

---

## T4: Frontend Integration

**Goal**: Connect UI to API
**Size**: L (half day)
**Dependencies**: T3
**Files**:
- [ ] `src/lib/api/feature.ts`
- [ ] `src/lib/query/feature.ts`
- [ ] `src/components/modules/FeatureModule.tsx`

**Acceptance**:
- [ ] API client functions
- [ ] TanStack Query hooks
- [ ] Basic UI component
- [ ] Loading and error states

**Status**: pending
```

---

## PR.md Template

```markdown
## Summary

Brief description of what this PR does and why.

## Changes

- Added `/api/feature` endpoints for CRUD operations
- Created `FeatureModule` component with list/detail views
- Implemented caching with Redis (5min TTL)

## Key Decisions

- Used Redis for caching due to [reason]
- Chose pagination over infinite scroll for [reason]

## Testing

- [x] `bun run check` passes
- [x] `bun run test` passes
- [x] `bun run build` passes
- [ ] Manual testing of core flow

## Screenshots (if applicable)

[Add screenshots for UI changes]

## Related

- Spec: `.works/spec/{feature-name}/`
- Issue: #123 (if applicable)

---

🤖 Generated with [Claude Code](https://claude.ai/code)
```
