---
id: writing-design-documents
name: "Writing Design Documents"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Writing Design Documents

## Metadata

| Field | Value |
|-------|-------|
| **ID** | writing-design-documents |
| **Version** | 2.0.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #design, #architecture |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-design-reviewer-agent |

---

## Methodology Reference

**Primary:** writing-design-documents (Writing Design Documents v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| BA | requirements-traceability | Requirements traceability (FR-X → AD-X) |
| BA | business-process-modeling | Business process modeling |
| Dev | architecture-patterns | Architecture patterns |
| Dev | rest-api-design | REST API design |
| Dev | testing-strategy | Testing strategy |
| DevOps | infrastructure-patterns | Infrastructure considerations |
| PdM | product-discovery | Technical debt awareness |
| PM | risk-assessment | Risk assessment |
| UX | usability-heuristics | Component design patterns |

---

## Problem

Developers jump from requirements to coding without planning architecture. This causes:
- Inconsistent code patterns across the codebase
- Wrong technology choices discovered too late
- Rewrites when architecture doesn't scale
- Onboarding struggles - new devs can't understand the system
- Decisions lost - no one remembers WHY something was built this way
- Technical debt accumulates untracked

**The root cause:** No documented decisions about HOW to build.

---

## Framework

### What is a Design Document?

A design document answers: **"HOW are we building this?"**

It bridges the gap between specification (what) and implementation (code).

### Document Hierarchy

```
CONSTITUTION (project-wide)
    ↓ informs
SPEC (feature-specific) → DESIGN (feature-specific) → IMPL PLAN → TASKS
    FR-X requirements     ↓ implements               ↓ breaks down
                         AD-X decisions              TASK-XXX
```

### Design vs Spec vs Implementation Plan

| Aspect | Specification | Design | Implementation Plan |
|--------|---------------|--------|---------------------|
| Question | What to build? | How to build it? | In what order? |
| Audience | Stakeholders, PMs | Developers | Developers, AI agents |
| Content | Requirements, AC | Architecture, APIs | Tasks, estimates |
| Changes | Needs approval | Technical decision | May adjust during dev |
| Output | FR-X, NFR-X | AD-X, file list | TASK-XXX list |

### Design Document Structure v2.0

```markdown
# Design: [Feature Name]

## Reference Documents
[Links to spec, constitution, related designs]

## Overview
[Brief summary of technical approach]

## Spec Coverage
[FR-X → AD-X traceability matrix]

## Architectural Decisions
[AD-X with rationale, alternatives, consequences]

## File Structure
[What files to create/modify with patterns]

## Data Models
[Database schemas, TypeScript types]

## API Contracts
[Endpoints with OpenAPI-style documentation]

## Component Design (if frontend)
[React/Vue components, state management]

## Dependencies
[Libraries, services, infrastructure]

## Security Considerations
[Auth, validation, encryption]

## Performance Considerations
[Caching, optimization, scaling]

## Testing Strategy
[Unit, integration, E2E approach]

## Migration Strategy (if applicable)
[Data migration, backwards compatibility]

## Recommended Skills & Methodologies
[For implementation phase]
```

---

## Writing Process

### Phase 1: Load Full SDD Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles, tech stack
2. .aidocs/contracts.md - existing API contracts
3. {FEATURE_DIR}/spec.md - requirements to implement (FR-X)
4. features/done/ - completed designs for patterns
```

Extract:
- Tech stack constraints (from constitution)
- Existing patterns (from done features)
- API naming conventions (from contracts)
- All FR-X and NFR-X to implement

### Phase 2: Codebase Research

**This phase is critical. Invest tokens here.**

#### 2.1 Find Existing Patterns

```bash
# Find similar implementations
Grep: pattern from spec keyword
Glob: **/similar_feature/**

# Find existing architecture patterns
Grep: class.*Service
Grep: class.*Controller
Grep: export.*Router

# Read project CLAUDE.md files
Read: app/CLAUDE.md
Read: app/components/CLAUDE.md
```

#### 2.2 Map Patterns for Each Component

| Component Type | Pattern Source | What to Extract |
|----------------|----------------|-----------------|
| API endpoints | existing routes | URL structure, middleware |
| Services | existing services | Base class, error handling |
| Models | existing models | Field naming, relationships |
| Components | existing UI | Props interface, styling |
| Tests | existing tests | Setup, mocking strategy |

### Phase 3: Create Traceability Matrix (BA: requirements-traceability)

**Every FR-X must map to at least one AD-X.**

```markdown
## Spec Coverage

| FR | Requirement Summary | Implemented By |
|----|---------------------|----------------|
| FR-001 | User registration | AD-001, AD-002 |
| FR-002 | Email validation | AD-001 |
| FR-003 | Password requirements | AD-002, AD-003 |
| NFR-001 | Response < 500ms | AD-004 |
| NFR-002 | bcrypt hashing | AD-003 |
```

### Phase 4: Architecture Decisions (Dev: architecture-patterns)

#### 4.1 Decision Format (ADR-Style)

```markdown
### AD-001: [Decision Title]

**Context:** [Background, constraints, why decision needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Option A] | [+] | [-] | [Reason] |
| [Option B] | [+] | [-] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

**Traces to:** FR-001, NFR-002
```

#### 4.2 Decision Categories

| Category | Examples |
|----------|----------|
| **Data** | Database choice, schema design, caching |
| **API** | REST vs GraphQL, authentication, versioning |
| **Architecture** | Monolith vs microservice, module structure |
| **Libraries** | Framework choice, utility libraries |
| **Security** | Auth mechanism, encryption, validation |
| **Performance** | Indexing, caching strategy, CDN |

### Phase 5: File Structure (BA: business-process-modeling)

#### 5.1 List All File Changes

```markdown
## File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/auth/handlers/register.ts` | Registration endpoint | FR-001 | AD-001 |
| CREATE | `src/auth/services/password.ts` | Password hashing | FR-003 | AD-003 |
| MODIFY | `src/middleware/auth.ts` | Add JWT validation | FR-004 | AD-002 |
| CREATE | `tests/auth/register.test.ts` | Registration tests | FR-001 | AD-001 |
```

#### 5.2 Directory Tree

```
src/
├── auth/
│   ├── handlers/
│   │   ├── register.ts    # CREATE - FR-001
│   │   ├── login.ts       # CREATE - FR-004
│   │   └── logout.ts      # CREATE - FR-005
│   ├── services/
│   │   ├── password.ts    # CREATE - FR-003
│   │   └── jwt.ts         # CREATE - FR-002
│   ├── middleware/
│   │   └── protect.ts     # CREATE - FR-006
│   └── index.ts           # CREATE - router
└── tests/
    └── auth/
        ├── register.test.ts
        └── login.test.ts
```

### Phase 6: Data Models

#### 6.1 TypeScript Types

```typescript
// src/auth/types.ts

interface User {
  id: string;           // UUID v4
  email: string;        // Unique, RFC 5322 format
  passwordHash: string; // bcrypt hash
  createdAt: Date;
  verifiedAt: Date | null;
}

interface Session {
  id: string;           // UUID v4
  userId: string;       // FK → User.id
  expiresAt: Date;      // 7 days from creation
}
```

#### 6.2 Database Schema

```sql
-- migrations/001_create_users.sql

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  verified_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/002_create_sessions.sql

CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
```

### Phase 7: API Contracts (Dev: rest-api-design)

#### 7.1 OpenAPI-Style Documentation

```markdown
### POST /api/auth/register

**Summary:** Register a new user account

**Authentication:** None

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass1"
}
```

**Request Validation:**
| Field | Rules |
|-------|-------|
| email | Required, RFC 5322 format, max 255 chars |
| password | Required, min 8 chars, 1 uppercase, 1 number |

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "createdAt": "2026-01-19T10:00:00Z"
  }
}
```
*Sets HTTP-only cookie: access_token*

**Error Responses:**
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Invalid email format | `{"error": "Invalid email format"}` |
| 400 | Password too weak | `{"error": "Password must be 8+ chars with 1 uppercase and 1 number"}` |
| 409 | Email exists | `{"error": "Email already registered"}` |
| 500 | Server error | `{"error": "Internal server error"}` |
```

### Phase 8: Component Design (if frontend)

#### 8.1 Component Hierarchy

```
<AuthLayout>
├── <RegisterForm>
│   ├── <EmailInput />
│   ├── <PasswordInput />
│   ├── <PasswordStrengthMeter />
│   └── <SubmitButton />
└── <AuthFooter>
    └── <LoginLink />
```

#### 8.2 Component Specification

```markdown
### RegisterForm Component

**Location:** `src/components/auth/RegisterForm.tsx`

**Props:**
```typescript
interface RegisterFormProps {
  onSuccess: (user: User) => void;
  onError?: (error: Error) => void;
}
```

**State:**
- email: string
- password: string
- isLoading: boolean
- errors: ValidationErrors

**Behavior:**
1. Validates email format on blur
2. Shows password strength meter on input
3. Disables submit while loading
4. Calls onSuccess with user data
```

### Phase 9: Dependencies

#### 9.1 New Packages

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| bcrypt | ^5.1.0 | Password hashing | MIT |
| jsonwebtoken | ^9.0.0 | JWT tokens | MIT |
| zod | ^3.22.0 | Request validation | MIT |

#### 9.2 External Services

| Service | Purpose | Required | Fallback |
|---------|---------|----------|----------|
| SendGrid | Email delivery | Yes | Log to console (dev) |
| Redis | Session blacklist | No | In-memory (dev) |

### Phase 10: Security Considerations

| Concern | Mitigation | AD Reference |
|---------|------------|--------------|
| Password storage | bcrypt with cost 12 | AD-003 |
| XSS prevention | HTTP-only cookies | AD-002 |
| CSRF protection | SameSite=Strict cookie | AD-002 |
| SQL injection | Parameterized queries | AD-001 |
| Rate limiting | 5 attempts/minute/IP | AD-005 |
| Input validation | Zod schema validation | AD-001 |

### Phase 11: Performance Considerations

| Concern | Strategy | Target | AD Reference |
|---------|----------|--------|--------------|
| Login latency | Connection pooling | < 500ms p95 | AD-004 |
| Token validation | JWT (stateless) | < 10ms | AD-002 |
| Database queries | Indexed email lookup | < 50ms | AD-001 |
| Password hashing | bcrypt cost 12 | < 300ms | AD-003 |

### Phase 12: Testing Strategy (Dev: testing-strategy)

#### 12.1 Test Pyramid

```
         E2E Tests
        (Playwright)
       ┌───────────┐
       │  Critical │
       │  Flows    │
       └─────┬─────┘
             │
    Integration Tests
       (Supertest)
    ┌─────────────────┐
    │ API endpoints   │
    │ Service layers  │
    └───────┬─────────┘
            │
      Unit Tests
       (Vitest)
   ┌───────────────────┐
   │ Pure functions    │
   │ Utilities         │
   │ Validators        │
   └───────────────────┘
```

#### 12.2 Test Coverage Requirements

| Layer | Coverage Target | What to Test |
|-------|-----------------|--------------|
| Unit | 80%+ | Password hashing, JWT utils, validators |
| Integration | 100% endpoints | All API routes with happy/error paths |
| E2E | Critical flows | Registration, Login, Logout |

### Phase 13: Migration Strategy (if applicable)

```markdown
## Migration Strategy

### Data Migration
- No existing user data (greenfield)

### Backwards Compatibility
- N/A (new feature)

### Rollout Plan
1. Deploy database migrations
2. Deploy API changes (behind feature flag)
3. Enable feature flag for 10% users
4. Monitor error rates
5. Gradual rollout to 100%

### Rollback Plan
1. Disable feature flag
2. No data migration needed (new tables)
```

---

## Templates

### Full Design Template v2.0

```markdown
# Design: [Feature Name]

**Version:** 1.0
**Spec:** `{FEATURE_DIR}/spec.md`
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, patterns |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, NFR-X to implement |
| Contracts | `.aidocs/contracts.md` | Existing API patterns |
| Related Design | `features/done/{NN}-{feature}/design.md` | Patterns to follow |

---

## Overview

[2-3 sentences summarizing technical approach and key decisions]

---

## Spec Coverage

| FR/NFR | Requirement | Implemented By |
|--------|-------------|----------------|
| FR-001 | [Summary] | AD-001, AD-002 |
| FR-002 | [Summary] | AD-001 |
| NFR-001 | [Summary] | AD-003 |

---

## Architectural Decisions

### AD-001: [Decision Title]

**Context:** [Why this decision is needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Considered:**
| Alternative | Why Rejected |
|-------------|--------------|
| [Option A] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]

**Traces to:** FR-001, FR-002

---

## File Structure

```
src/
├── feature/
│   ├── handlers/
│   │   └── create.ts    # CREATE - FR-001
│   ├── services/
│   │   └── logic.ts     # CREATE - FR-002
│   └── index.ts         # CREATE
└── tests/
    └── feature/
        └── create.test.ts  # CREATE
```

### File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/feature/handlers/create.ts` | Create handler | FR-001 | AD-001 |
| MODIFY | `src/middleware/auth.ts` | Add permission | FR-003 | AD-002 |

---

## Data Models

### [Model Name]

```typescript
interface ModelName {
  id: string;
  field1: string;
  createdAt: Date;
}
```

**Database:**
```sql
CREATE TABLE model_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  field1 VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Contracts

### [METHOD] /api/[endpoint]

**Summary:** [What this endpoint does]
**Authentication:** Required | None

**Request:**
```json
{
  "field1": "value"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field1": "value"
}
```

**Errors:**
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Invalid input | `{"error": "..."}` |

---

## Dependencies

### Packages
| Package | Version | Purpose |
|---------|---------|---------|
| [name] | ^X.Y.Z | [Why needed] |

### External Services
| Service | Purpose | Required |
|---------|---------|----------|
| [name] | [Why] | Yes/No |

---

## Security Considerations

| Concern | Mitigation | AD |
|---------|------------|-----|
| [Concern] | [Strategy] | AD-X |

---

## Performance Considerations

| Concern | Strategy | Target |
|---------|----------|--------|
| [Concern] | [Approach] | [Metric] |

---

## Testing Strategy

### Unit Tests
- [ ] [What to test]

### Integration Tests
- [ ] [What to test]

### E2E Tests
- [ ] [Critical flow]

---

## Migration Strategy

### Data Migration
- [Required migrations]

### Backwards Compatibility
- [Considerations]

### Rollback Plan
- [Steps to rollback]

---

## Related Designs

| Feature | Relationship | Patterns to Reuse |
|---------|-------------|-------------------|
| [feature] | [dependency/similar] | [patterns] |

---

## Recommended Skills & Methodologies

### Skills
| Skill | Purpose |
|-------|---------|
| faion-software-developer | Implementation |
| faion-devops-engineer | Infrastructure |

### Methodologies
| ID | Name | Purpose |
|----|------|---------|
| M-DEV-XXX | [Name] | [How it helps] |

---

## Open Questions

- [ ] [Question to resolve before implementation]

---

## References

- [Link to external documentation]
- [Link to similar design]
```

---

## Quality Checklist

### Design Quality Gate (Before Implementation Plan)

**Completeness:**
- [ ] All FR-X from spec have corresponding AD-X
- [ ] All NFR-X addressed (performance, security, scalability)
- [ ] All files listed with CREATE/MODIFY actions
- [ ] All API endpoints documented with request/response
- [ ] All data models defined (TypeScript + SQL)
- [ ] Dependencies listed with versions

**Clarity:**
- [ ] Each AD-X has context, decision, rationale
- [ ] Alternatives considered and rejected
- [ ] Consequences documented (positive and negative)
- [ ] File changes traced to FR-X and AD-X

**Traceability:**
- [ ] Spec Coverage matrix complete
- [ ] Every FR maps to at least one AD
- [ ] Every file change traces to FR and AD

**Context:**
- [ ] Constitution referenced
- [ ] Related designs identified
- [ ] Existing patterns documented
- [ ] Skills/methodologies recommended

**Risk:**
- [ ] Security considerations documented
- [ ] Performance targets defined
- [ ] Migration/rollback plan (if applicable)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No rationale for decisions | Always explain WHY, not just what |
| Missing file list | Every file touched must be listed |
| Vague API contracts | Specify exact request/response JSON |
| No traceability | Every AD must trace to FR-X |
| Forgetting security | Add security section for all features |
| No testing strategy | Define what tests you'll write |
| Missing alternatives | Document at least 2 alternatives per AD |
| No related designs | Check features/done/ for patterns |

---

## Related Methodologies

- **writing-specifications:** Writing Specifications
- **writing-implementation-plans:** Writing Implementation Plans
- **requirements-traceability:** Requirements Traceability
- **business-process-modeling:** Business Process Modeling
- **architecture-patterns:** Architecture Patterns
- **rest-api-design:** REST API Design
- **testing-strategy:** Testing Strategy
- **infrastructure-patterns:** Infrastructure Patterns
- **risk-assessment:** Risk Assessment

---

## Agent

**faion-design-reviewer-agent** reviews design documents. Invoke with:
- "Review this design for completeness"
- "Suggest architectural decisions for [feature]"
- "Generate API contracts from spec"
- "Check FR-X to AD-X traceability"

---

*Methodology | SDD Foundation | Version 2.0.0*
*Integrates BA, Dev, DevOps, PM best practices*
