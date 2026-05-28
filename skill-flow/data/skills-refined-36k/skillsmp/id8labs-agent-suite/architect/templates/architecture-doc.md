# Architecture Document Template

Use this template to generate the technical specification for a project.

---

## Template

```markdown
# Architecture: {Project Name}

**Version:** 1.0
**Date:** {YYYY-MM-DD}
**Status:** {Draft / Approved / Building}
**Author:** ID8Architect

---

## Overview

### Problem Statement
{What problem are we solving? 2-3 sentences}

### Solution Summary
{What are we building? 2-3 sentences}

### Target User
{Who is this for? Be specific}

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | {requirement} | Must | {notes} |
| FR-2 | {requirement} | Must | {notes} |
| FR-3 | {requirement} | Should | {notes} |
| FR-4 | {requirement} | Could | {notes} |

### Non-Functional Requirements

| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | Page load time | < 2s |
| Availability | Uptime | 99.5% |
| Security | Authentication | Supabase Auth |
| Scalability | Concurrent users | 1,000 |

### Constraints

| Constraint | Description |
|------------|-------------|
| Budget | ${X}/month max for infrastructure |
| Timeline | {X} weeks to MVP |
| Team | Solo developer (AI-augmented) |
| Technical | Must use {constraint} |

---

## System Architecture

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                                │
│                    Next.js App Router                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Pages     │  │ Components  │  │   Hooks     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│               Next.js API Routes + Server Actions            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Routes    │  │  Services   │  │   Utils     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │  Auth   │      │ Database│      │ Storage │
    │(Supabase│      │(Supabase│      │(Supabase│
    └─────────┘      └─────────┘      └─────────┘
```

### Component Descriptions

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| Client | UI rendering, user interaction | Next.js, React, Tailwind |
| API Layer | Business logic, data access | Next.js API Routes |
| Auth | Authentication, authorization | Supabase Auth |
| Database | Data persistence | Supabase (PostgreSQL) |
| Storage | File storage | Supabase Storage |

---

## Technology Stack

### Core Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Framework | Next.js | 14.x | Full-stack React, App Router |
| Language | TypeScript | 5.x | Type safety, DX |
| Styling | Tailwind CSS | 3.x | Utility-first, fast |
| Components | shadcn/ui | Latest | Accessible, customizable |
| Database | Supabase | Latest | PostgreSQL, managed |
| Hosting | Vercel | - | Zero-config Next.js |

### Additional Libraries

| Library | Purpose | Alternative Considered |
|---------|---------|------------------------|
| React Query | Server state | SWR |
| Zustand | Client state | Jotai |
| Zod | Validation | Yup |
| React Hook Form | Forms | Formik |
| date-fns | Dates | dayjs |

### Development Tools

| Tool | Purpose |
|------|---------|
| ESLint | Code linting |
| Prettier | Code formatting |
| TypeScript | Type checking |
| Jest | Unit testing |
| Playwright | E2E testing |

---

## Data Model

### Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐
│   profiles  │       │  {entity}   │
├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ owner_id    │
│ email       │       │ id (PK)     │
│ full_name   │       │ name        │
│ avatar_url  │       │ ...         │
│ created_at  │       │ created_at  │
│ updated_at  │       │ updated_at  │
└─────────────┘       └─────────────┘
```

### Table Definitions

#### profiles

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | uuid | NO | - | FK to auth.users |
| email | text | NO | - | User email |
| full_name | text | YES | - | Display name |
| avatar_url | text | YES | - | Profile image |
| created_at | timestamptz | NO | now() | Created timestamp |
| updated_at | timestamptz | NO | now() | Updated timestamp |

#### {entity}

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | uuid | NO | gen_random_uuid() | Primary key |
| owner_id | uuid | NO | - | FK to profiles |
| name | text | NO | - | {description} |
| ... | ... | ... | ... | ... |
| created_at | timestamptz | NO | now() | Created timestamp |
| updated_at | timestamptz | NO | now() | Updated timestamp |

### Indexes

| Table | Columns | Type | Purpose |
|-------|---------|------|---------|
| {entity} | owner_id | btree | Filter by owner |
| {entity} | created_at | btree (desc) | Sort by date |

### RLS Policies

| Table | Policy | Operation | Rule |
|-------|--------|-----------|------|
| profiles | Own profile | SELECT/UPDATE | auth.uid() = id |
| {entity} | Own {entity}s | ALL | auth.uid() = owner_id |

---

## API Design

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /api/v1/{entities} | List {entities} | Required |
| POST | /api/v1/{entities} | Create {entity} | Required |
| GET | /api/v1/{entities}/{id} | Get {entity} | Required |
| PATCH | /api/v1/{entities}/{id} | Update {entity} | Required |
| DELETE | /api/v1/{entities}/{id} | Delete {entity} | Required |

### Request/Response Examples

**POST /api/v1/{entities}**

Request:
```json
{
  "name": "{entity} name",
  "description": "Optional description"
}
```

Response (201):
```json
{
  "data": {
    "id": "uuid",
    "name": "{entity} name",
    "description": "Optional description",
    "createdAt": "2024-01-15T10:00:00Z"
  }
}
```

### Error Handling

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid input |
| 401 | UNAUTHORIZED | Not authenticated |
| 403 | FORBIDDEN | Not authorized |
| 404 | NOT_FOUND | Resource not found |
| 500 | INTERNAL_ERROR | Server error |

---

## Authentication & Authorization

### Auth Flow

```
User
  │
  ▼
Login Form ──► Supabase Auth ──► Session Created
                                      │
                                      ▼
                               Cookie Set
                                      │
                                      ▼
                             Subsequent Requests
                                      │
                                      ▼
                          Middleware validates session
                                      │
                                      ▼
                             RLS enforces access
```

### Authorization Rules

| Role | Permissions |
|------|-------------|
| Anonymous | View public content |
| Authenticated | CRUD own resources |
| Admin | All operations |

---

## Infrastructure

### Environments

| Environment | URL | Database | Deploy |
|-------------|-----|----------|--------|
| Local | localhost:3000 | Supabase local | Manual |
| Preview | *.vercel.app | Supabase branch | On PR |
| Production | {domain} | Supabase prod | On merge |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| NEXT_PUBLIC_SUPABASE_URL | Yes | Supabase project URL |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Yes | Supabase anon key |
| SUPABASE_SERVICE_ROLE_KEY | Yes | Service role key (server only) |
| NEXT_PUBLIC_APP_URL | No | App URL for redirects |

### Monitoring

| Service | Purpose | Alerts |
|---------|---------|--------|
| Sentry | Error tracking | On error spike |
| Vercel Analytics | Performance | On degradation |
| Supabase Dashboard | Database health | On resource limits |

---

## Security Considerations

### Threats Addressed

| Threat | Mitigation |
|--------|------------|
| SQL Injection | Parameterized queries via Supabase client |
| XSS | React escaping, CSP headers |
| CSRF | SameSite cookies |
| Auth bypass | Supabase RLS on all tables |
| Data exposure | RLS policies, no direct DB access |

### Security Checklist

- [ ] RLS enabled on all tables
- [ ] Service role key only on server
- [ ] Input validation on all endpoints
- [ ] Auth redirects use allowlist
- [ ] HTTPS enforced
- [ ] Security headers configured

---

## Performance Considerations

### Optimization Strategies

| Area | Strategy |
|------|----------|
| Initial load | SSR for critical pages |
| Images | next/image optimization |
| Data fetching | React Query caching |
| Bundle size | Dynamic imports for large components |
| Database | Indexes on common queries |

### Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| TTFB | < 600ms |

---

## Migration Plan

### Phase 1: Setup (Week 1)
1. Initialize Next.js project
2. Configure Supabase
3. Set up Vercel deployment
4. Configure CI/CD

### Phase 2: Foundation (Week 2)
1. Authentication flow
2. Database schema
3. Base UI components
4. API structure

### Phase 3: Core Features (Weeks 3-4)
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}

### Phase 4: Polish (Week 5)
1. Error handling
2. Loading states
3. Edge cases
4. Testing

---

## Open Questions

| Question | Status | Decision |
|----------|--------|----------|
| {question} | Open | - |
| {question} | Decided | {decision} |

---

## Appendix

### File Structure

```
src/
├── app/
│   ├── (auth)/
│   ├── (marketing)/
│   ├── api/
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/
│   └── features/
├── lib/
│   ├── supabase/
│   ├── services/
│   └── utils/
├── hooks/
├── types/
└── config/
```

### References

- [Next.js Docs](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
```

---

## Usage Notes

1. Fill in all `{placeholders}` with project-specific information
2. Remove sections not applicable to your project
3. Add project-specific sections as needed
4. Keep this document updated as architecture evolves
5. Store in `docs/ARCHITECTURE.md` in the project repository
