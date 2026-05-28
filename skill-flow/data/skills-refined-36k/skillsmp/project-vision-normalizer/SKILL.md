---
name: project-vision-normalizer
description: Normalizes raw project ideas into a consistent internal vision for this workspace. Use when starting a new project.
triggers: [new-project, ambiguous-ideas]
outputs: [vision-statement, normalized-requirements]
depends_on: []
---

# Project Vision Normalizer

## Purpose

Transforms **raw, fragmented project ideas** into a consistent, actionable internal vision. This ensures all stakeholders and the AI have a shared understanding before planning begins.

---

## When to Use

- New project kickoff
- Ambiguous or fragmented requirements
- Conflicting stakeholder inputs
- Before any spec development

---

## Instructions

### 1. Rewrite Using Consistent Terminology

```markdown
## Raw Input
"We need a login thing, maybe with social stuff later. 
Users should be able to reset passwords. Oh and we need admin access."

## Normalized Vision
"Implement user authentication with email/password login.
Deferred: Social login (Phase 2).
Included: Password reset flow.
Included: Admin role with elevated permissions."
```

### 2. Align with Workspace Conventions

| Convention | Application |
|------------|-------------|
| Naming: `kebab-case` for endpoints | `/password-reset` |
| Auth: JWT tokens | Use JWT, not sessions |
| API: REST | RESTful endpoint design |

### 3. Remove Contradictions

```markdown
## Contradictions Identified

❌ "Simple login" vs "enterprise-grade security"
✅ Resolution: "Secure authentication suitable for MVP"

❌ "Fast delivery" vs "comprehensive testing"
✅ Resolution: "MVP scope with critical path testing"
```

### 4. Produce Stable Vision Statement

```markdown
# Project Vision: User Authentication System

## Core Objective
Enable secure user authentication for the application.

## Included (MVP)
- Email/password login
- JWT token-based sessions
- Password reset via email
- Admin role

## Deferred (Post-MVP)
- Social login (Google, GitHub)
- Multi-factor authentication
- Session management dashboard

## Non-Goals
- Enterprise SSO integration
- Biometric authentication
```

---

## Integration

- **Precedes:** `mvp-scope-guard`, `spec-driven-planning`
- **Follows:** Initial user input
- **Produces:** Stable vision for downstream skills

---

## Constraints

- Do not ask questions unless critical info is missing
- Resolve ambiguity through sensible defaults
- Document all assumptions explicitly

Clear vision enables focused execution.
