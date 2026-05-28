---
name: plan
description: Create technical implementation plans with chosen tech stack and architecture decisions
---

# Plan - Technical Implementation Plan

## Overview

Create detailed technical implementation plans based on functional specifications and chosen technology stack.

**Announce at start:** "I'm using the plan skill to create technical implementation plan."

## When to Use

- After creating and clarifying functional specification
- When you have chosen the technology stack
- Before breaking down into tasks
- When architecture decisions need to be documented

## Prerequisites

- ✅ Project constitution established (`SpecKit/constitution`)
- ✅ Functional specification created (`SpecKit/specify`)
- ✅ Specification clarified if needed (`SpecKit/clarify`)
- ✅ Technology stack chosen

## The Process

### Step 1: Review Inputs

1. Read project constitution (`.specify/memory/constitution.md`)
2. Read functional specification (`specs/<feature-id>/spec.md`)
3. Understand technology stack requirements from user

### Step 2: Create Implementation Plan

Create plan in `specs/<feature-id>/plan.md`:

**Required Sections:**

1. **Architecture Overview**
   - High-level architecture
   - Component breakdown
   - Data flow
   - Technology choices and rationale

2. **Data Model**
   - Database schema (if applicable)
   - Data structures
   - Relationships
   - Constraints

3. **API Design** (if applicable)
   - Endpoints
   - Request/response formats
   - Authentication/authorization
   - Error handling

4. **Component Design**
   - Components/modules
   - Responsibilities
   - Interfaces
   - Dependencies

5. **Implementation Details**
   - Key algorithms
   - Design patterns
   - Third-party libraries
   - Configuration

6. **Testing Strategy**
   - Unit tests
   - Integration tests
   - E2E tests
   - Test data requirements

7. **Deployment & Operations**
   - Deployment process
   - Configuration management
   - Monitoring and logging
   - Rollback strategy

### Step 3: Create Supporting Documents

Create additional documents as needed:

- `specs/<feature-id>/data-model.md` - Detailed data model
- `specs/<feature-id>/api-spec.json` - API specification (OpenAPI/Swagger)
- `specs/<feature-id>/research.md` - Technology research and decisions
- `specs/<feature-id>/quickstart.md` - Quick start guide

### Step 4: Research Technology Stack

If using rapidly changing technologies:
- Research specific versions
- Document compatibility requirements
- Identify potential issues
- Update `research.md` with findings

### Step 5: Validate Plan

Review plan for:
- Completeness: All aspects covered?
- Consistency: Aligns with constitution and spec?
- Feasibility: Can this be implemented?
- Over-engineering: Are there unnecessary components?

## Example Prompt

```
/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla 
HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and 
metadata is stored in a local SQLite database.
```

## Output Structure

```
specs/
└── 001-<feature-name>/
    ├── spec.md
    ├── plan.md
    ├── data-model.md
    ├── api-spec.json (if applicable)
    ├── research.md
    └── quickstart.md
```

## Key Principles

- **Be specific**: Include exact technologies, versions, patterns
- **Be complete**: Cover all aspects (data, API, components, tests)
- **Be consistent**: Align with constitution and specification
- **Be practical**: Avoid over-engineering
- **Be research-backed**: Document technology choices

## Integration with Other Skills

- **Before**: Use `SpecKit/specify` and `SpecKit/clarify`
- **After**: Use `SpecKit/tasks` to break down into actionable tasks
- **Alternative**: Use `Superpowers/writing-plans` for more detailed, bite-sized task breakdown

## Difference from Superpowers/writing-plans

- **SpecKit/plan**: High-level technical plan (architecture, components, APIs)
- **Superpowers/writing-plans**: Detailed implementation plan with bite-sized tasks, exact code, file paths

You can use both:
1. `SpecKit/plan` for high-level technical architecture
2. `Superpowers/writing-plans` for detailed implementation steps
