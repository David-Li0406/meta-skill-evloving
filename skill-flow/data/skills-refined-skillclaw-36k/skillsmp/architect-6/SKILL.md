---
name: architect
description: Technical architecture engine for ID8Labs. Transforms validated ideas into buildable plans optimized for solo builder velocity. Outputs technical specs and phased roadmaps.
version: 1.0.0
mcps: []
subagents: [backend-architect, database-architect]
skills: [database-design, supabase-expert]
---

# ID8ARCHITECT - Technical Design Engine

## Purpose

Transform validated ideas into concrete, buildable technical plans. Architecture should enable velocity, not slow it down.

**Philosophy:** Boring technology, managed services, ship fast, iterate often.

---

## When to Use

- Project has a BUILD verdict from scout
- User needs to design system architecture
- User asks "how should I build this?"
- User needs database schema design
- User needs API design guidance
- User needs infrastructure decisions
- Project is in VALIDATED or ARCHITECTING state

---

## Commands

### `/architect <project-slug>`

Run full architecture design for a validated project.

**Process:**
1. REQUIREMENTS - Extract from validation report
2. ARCHITECTURE - Design system components
3. STACK - Select technologies
4. DATA - Model the database
5. API - Design interfaces
6. INFRASTRUCTURE - Plan deployment
7. ROADMAP - Phase the implementation

### `/architect stack <requirements>`

Get stack recommendations for specific requirements.

### `/architect schema <domain-description>`

Design database schema for a domain.

### `/architect api <resource-description>`

Design API endpoints for a resource.

---

## Design Philosophy

### Solo Builder Optimization

This is NOT enterprise architecture. Optimize for:

| Principle | Application |
|-----------|-------------|
| **Speed over Scale** | Launch fast, optimize later |
| **Boring Technology** | Use proven, well-documented tools |
| **Managed Services** | Let providers handle infrastructure |
| **Monolith First** | No microservices until proven need |
| **Convention over Configuration** | Use framework defaults |
| **Delete Before Build** | Question every feature |

### Technology Preferences

**Preferred Stack (default unless reason to deviate):**

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Next.js 14+ (App Router) | React + SSR + API routes |
| Styling | Tailwind CSS + shadcn/ui | Fast, consistent, accessible |
| Backend | Next.js API routes / Edge | Same deploy, simple |
| Database | Supabase (PostgreSQL) | Managed, real-time, auth included |
| Auth | Supabase Auth | Integrated, handles edge cases |
| Storage | Supabase Storage | Integrated with auth |
| Hosting | Vercel | Zero-config Next.js deploy |
| Monitoring | Vercel Analytics + Sentry | Essential observability |

**When to Deviate:**

- Heavy computation → Add dedicated backend
- Complex real-time → Consider Convex or custom WebSocket
- ML/AI workloads → Separate Python service
- Specific compliance → May need self-hosted

---

## Process Detail

### Phase 1: REQUIREMENTS

Extract from validation report:
- Core problem being solved
- Target user persona
- Must-have features (max 5 for MVP)
- Success metrics
- Constraints (budget, timeline, skills)

**Output:**
```markdown
## Requirements Summary

### Problem
{What are we solving}

### User
{Who is this for}

### MVP Features
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}

### Constraints
- Budget: ${X}/month max
- Timeline: {X} weeks to MVP
- Skills: {current skill level}
```

### Phase 2: ARCHITECTURE

Design high-level system:

```
┌─────────────────────────────────────────────────┐
│                    CLIENT                        │
│            (Next.js App Router)                 │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                 API LAYER                        │
│         (Next.js API Routes / Edge)             │
└─────────────────────────────────────────────────┘
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
       ┌────────┐  ┌────────┐  ┌────────┐
       │ Auth   │  │Database│  │Storage │
       │(Supa)  │  │(Supa)  │  │(Supa)  │
       └────────┘  └────────┘  └────────┘
```

**Decisions to Document:**
- Client rendering strategy (SSR/SSG/CSR)
- State management approach
- API design (REST vs tRPC)
- Authentication flow
- Error handling strategy

### Phase 3: STACK

Use the `frameworks/stack-selection.md` decision matrix.

For each technology choice:
1. State the requirement
2. List 2-3 options
3. Pick one with brief rationale
4. Document trade-offs

### Phase 4: DATA

Design database schema using `frameworks/database-patterns.md`.

**Key Tables to Define:**
- Core domain entities
- User/auth tables (if not using Supabase defaults)
- Relationship tables
- Audit/logging tables

**For Each Table:**
- Fields with types
- Primary keys
- Foreign keys
- Indexes
- RLS policies (Supabase)

### Phase 5: API

Design API using `frameworks/api-design.md`.

**For Each Endpoint:**
- Method + Path
- Request body/params
- Response shape
- Error cases
- Auth requirements

### Phase 6: INFRASTRUCTURE

Plan deployment using `frameworks/infrastructure.md`.

**Define:**
- Hosting configuration
- Environment management
- CI/CD pipeline
- Monitoring setup
- Backup strategy

### Phase 7: ROADMAP

Create phased implementation plan using `templates/build-roadmap.md`.

**Phases:**
- **MVP (Weeks 1-4):** Core loop, basic auth, essential features
- **V1 (Weeks 5-8):** Polish, secondary features, onboarding
- **V2 (Weeks 9-12):** Growth features, integrations, optimization

---

## Framework References

### System Design
`frameworks/system-design.md` - Component patterns, coupling, boundaries

### Stack Selection
`frameworks/stack-selection.md` - Technology decision matrix

### Database Patterns
`frameworks/database-patterns.md` - Schema design, Supabase patterns

### API Design
`frameworks/api-design.md` - REST patterns, error handling, versioning

### Infrastructure
`frameworks/infrastructure.md` - Deploy, CI/CD, monitoring

---

## Output Templates

### Architecture Document
`templates/architecture-doc.md` - Full technical specification

### Build Roadmap
`templates/build-roadmap.md` - Phased implementation plan

---

## Tool Integration

### Subagents

**backend-architect:**
- System design decisions
- API contract design
- Integration patterns

**database-architect:**
- Schema design
- Query optimization
- Data modeling

### Skills

**database-design:**
- Supabase-specific patterns
- RLS policy design
- Migration strategies

**supabase-expert:**
- Edge functions
- Real-time subscriptions
- Storage configuration

---

## Handoff

After completing architecture:

1. **Save outputs:**
   - Architecture doc → `docs/ARCHITECTURE.md` in project
   - Build roadmap → `docs/BUILD_ROADMAP.md` in project

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "ARCHITECT: Architecture complete. Stack: {stack}. MVP scope: {features}. Estimated timeline: {weeks} weeks."
   ```

3. **Update state:**
   ```
   /tracker update {project-slug} BUILDING
   ```

4. **Next steps:**
   - Proceed to 11-stage pipeline Stage 4 (Foundation Pour)
   - Begin scaffolding based on architecture doc

---

## Anti-Patterns

### Avoid These

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Microservices from start | Complexity overhead | Monolith first |
| Custom auth | Security risk, time sink | Use Supabase Auth |
| Premature optimization | Waste of time | Ship, measure, optimize |
| Complex state management | Redux overkill for most apps | Zustand or Context |
| Self-hosted everything | Ops overhead | Managed services |
| GraphQL for simple CRUD | Overhead without benefit | REST or tRPC |

### Right-Size Your Architecture

```
Simple CRUD app → Next.js + Supabase, done
Real-time features → Add Supabase Realtime
Complex forms → Add React Hook Form + Zod
Heavy compute → Add Edge Functions or separate service
ML/AI → Separate Python service
Enterprise needs → Then consider more complex patterns
```

---

## Quality Checks

Before signing off on architecture:

- [ ] Every component has a clear purpose
- [ ] No premature optimization
- [ ] Stack is boring and proven
- [ ] MVP scope is minimal (3-5 features)
- [ ] Timeline is realistic for solo builder
- [ ] Infrastructure is managed (not self-hosted)
- [ ] Security basics are addressed (auth, validation)
- [ ] Monitoring strategy exists
