# File Categories

This document defines when to use each category in the `.claude/` workspace.

## Category Definitions

### plans/

**Purpose:** Implementation plans, migration plans, project plans, feature specifications

**When to use:**
- Planning a multi-step implementation
- Documenting a migration strategy
- Breaking down a large feature into actionable steps
- Creating a project roadmap

**Status values:**
- `draft` - Initial creation, still being refined
- `in-progress` - Actively being implemented
- `approved` - Reviewed and approved for implementation
- `implemented` - Plan has been executed
- `superseded` - Replaced by a newer plan

**Example files:**
- `2025-01-07-user-authentication-migration.md`
- `2025-01-07-api-v2-implementation.md`
- `2025-01-07-database-optimization-plan.md`

---

### architecture/

**Purpose:** Architecture Decision Records (ADRs), design decisions, system diagrams, technical specifications

**When to use:**
- Making a significant architectural decision
- Documenting design rationale
- Recording trade-offs between approaches
- Capturing system structure decisions

**Status values:**
- `proposed` - Under consideration
- `accepted` - Decision made and approved
- `deprecated` - No longer recommended
- `superseded` - Replaced by a newer decision

**Example files:**
- `2025-01-07-event-sourcing-design.md`
- `2025-01-07-microservices-vs-monolith.md`
- `2025-01-07-caching-strategy.md`

---

### examples/

**Purpose:** Code examples, usage patterns, reference implementations, code snippets

**When to use:**
- Capturing a reusable code pattern
- Documenting how to use an API or library
- Creating reference implementations
- Showing before/after refactoring examples

**Status values:** None (examples are timeless)

**Example files:**
- `2025-01-07-pagination-pattern.md`
- `2025-01-07-error-handling-example.md`
- `2025-01-07-api-client-usage.md`

---

### research/

**Purpose:** Research notes, external findings, comparative analysis, library evaluations

**When to use:**
- Investigating external solutions
- Comparing libraries or frameworks
- Documenting findings from documentation
- Recording competitive analysis

**Status values:**
- `in-progress` - Research ongoing
- `complete` - Research finished

**Example files:**
- `2025-01-07-auth-library-comparison.md`
- `2025-01-07-react-state-management-options.md`
- `2025-01-07-database-performance-research.md`

---

### analysis/

**Purpose:** Code analysis, performance studies, security reviews, technical debt assessments

**When to use:**
- Analyzing existing code for issues
- Documenting performance investigations
- Recording security audit findings
- Assessing technical debt

**Status values:**
- `in-progress` - Analysis ongoing
- `complete` - Analysis finished

**Type values:**
- `code` - Code quality analysis
- `performance` - Performance investigation
- `security` - Security review
- `dependency` - Dependency audit
- `other` - Other analysis types

**Example files:**
- `2025-01-07-n-plus-one-audit.md`
- `2025-01-07-login-performance-analysis.md`
- `2025-01-07-dependency-security-review.md`

---

## Decision Guide

| Situation | Category |
|-----------|----------|
| "How should we implement X?" | plans/ |
| "Why did we choose Y over Z?" | architecture/ |
| "How do I use pattern P?" | examples/ |
| "What options exist for Q?" | research/ |
| "What's wrong with code C?" | analysis/ |

## NOT for .claude/

These should NOT go in `.claude/`:
- README files (stay in repo root or relevant directory)
- API documentation (goes in docs/)
- User-facing documentation (goes in docs/)
- Generated documentation
- Test files
