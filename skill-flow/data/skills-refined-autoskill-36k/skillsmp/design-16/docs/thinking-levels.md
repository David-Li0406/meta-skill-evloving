# Thinking Levels Guide

> When to use different thinking depths during Design Ops workflow.

---

## Overview

Different phases of Design Ops require different levels of cognitive depth. This guide specifies when to use normal processing vs. explicit thinking tags for more thorough reasoning.

### Thinking Levels

| Level | Trigger | Use When |
|-------|---------|----------|
| **Normal** | (default) | Routine tasks, well-understood patterns |
| **Think** | `<think>` | Complex logic, multiple considerations |
| **Think Hard** | Extended thinking | Cross-system impacts, architecture decisions |
| **Ultrathink** | Maximum budget | Critical security, novel domains, high-stakes decisions |

---

## By Phase

### Spec Writing Phase

| Complexity | Thinking Level | Indicators |
|------------|----------------|------------|
| **Normal** | Default | Simple CRUD operations, single-entity changes, well-defined requirements |
| **Think** | `<think>` | Multiple user flows, business logic complexity, 3+ acceptance criteria |
| **Think Hard** | Extended | Cross-system data flows, integration points, state management |
| **Ultrathink** | Maximum | Architecture changes, security-critical features, new domain modules |

**Decision Criteria:**

```
IF spec_involves:
  - Single entity CRUD → Normal
  - Multiple entities with relationships → Think
  - External system integration → Think Hard
  - Security/auth changes → Ultrathink
  - New architectural pattern → Ultrathink
```

### Validation Phase

| Validation Type | Thinking Level | When |
|-----------------|----------------|------|
| **Normal** | Default | Checking obvious violations (ambiguous terms, missing sections) |
| **Think** | `<think>` | Evaluating edge cases, boundary conditions |
| **Think Hard** | Extended | Cross-referencing domain invariants, finding subtle violations |
| **Ultrathink** | Maximum | Security review, compliance checking, novel domain application |

**Decision Criteria:**

```
IF validation_involves:
  - Universal invariants only → Normal
  - Single domain module → Think
  - Multiple domains (e.g., remote + construction) → Think Hard
  - Security or compliance invariants → Ultrathink
```

### PRP Generation Phase

| PRP Complexity | Thinking Level | Indicators |
|----------------|----------------|------------|
| **Normal** | Default | PRPs under 300 lines, single domain, clear patterns exist |
| **Think** | `<think>` | 300-500 line PRPs, 2 domains, some novel elements |
| **Think Hard** | Extended | 500+ line PRPs, 3+ domains, significant customization needed |
| **Ultrathink** | Maximum | Novel project type, no existing patterns, critical infrastructure |

**Decision Criteria:**

```
IF prp_generation_involves:
  - Template with <10 customizations → Normal
  - Template with 10-30 customizations → Think
  - Significant template modification → Think Hard
  - New template creation needed → Ultrathink
```

### Implementation Phase

| Task Type | Thinking Level | Confidence Score Correlation |
|-----------|----------------|------------------------------|
| **Normal** | Default | Confidence > 7/10, clear patterns |
| **Think** | `<think>` | Confidence 5-7/10, moderate complexity |
| **Think Hard** | Extended | Confidence 3-5/10, significant unknowns |
| **Ultrathink** | Maximum | Confidence < 3/10, critical systems |

**Decision Criteria:**

```
IF implementation_involves:
  - Following existing pattern exactly → Normal
  - Adapting pattern to new context → Think
  - Combining multiple patterns → Think Hard
  - Creating new pattern → Ultrathink
```

### Review Phase

| Review Scope | Thinking Level | When |
|--------------|----------------|------|
| **Normal** | Default | Routine validation, checklist verification |
| **Think** | `<think>` | Finding subtle spec-code mismatches |
| **Think Hard** | Extended | Integration issues, cross-component impacts |
| **Ultrathink** | Maximum | Security review, production incident analysis, compliance audit |

**Decision Criteria:**

```
IF review_involves:
  - Mechanical checklist verification → Normal
  - Evaluating implementation quality → Think
  - Assessing architecture alignment → Think Hard
  - Security or incident root cause → Ultrathink
```

---

## By Confidence Score

The PRP confidence score correlates with recommended thinking level:

| Confidence Score | Risk Level | Thinking Recommendation |
|------------------|------------|------------------------|
| 8-10 | Low/Green | Normal (patterns clear, risks understood) |
| 6-7.9 | Medium/Yellow | Think (some unknowns, moderate risk) |
| 4-5.9 | Elevated/Orange | Think Hard (significant unknowns) |
| 1-3.9 | High/Red | Ultrathink (critical gaps, major risks) |

---

## By Invariant Count

The number of applicable invariants indicates complexity:

| Invariant Count | Thinking Level |
|-----------------|----------------|
| 1-10 (universal only) | Normal |
| 11-20 (universal + 1 domain) | Think |
| 21-30 (universal + 2 domains) | Think Hard |
| 30+ (universal + 3+ domains) | Ultrathink |

---

## By File Impact

The number of files affected indicates scope:

| Files Affected | Thinking Level |
|----------------|----------------|
| 1-3 files | Normal |
| 4-10 files | Think |
| 11-20 files | Think Hard |
| 20+ files | Ultrathink |

---

## Domain-Specific Guidance

### Consumer Product Domain

| Scenario | Level | Why |
|----------|-------|-----|
| UI text change | Normal | Low risk, easy rollback |
| New user flow | Think | Emotional mapping needed |
| Onboarding redesign | Think Hard | Critical first impression |
| Payment flow | Ultrathink | Financial/trust critical |

### Integration Domain

| Scenario | Level | Why |
|----------|-------|-----|
| Adding API parameter | Normal | Backward compatible |
| New API endpoint | Think | Contract design matters |
| Third-party integration | Think Hard | External dependency |
| Authentication change | Ultrathink | Security critical |

### Data Architecture Domain

| Scenario | Level | Why |
|----------|-------|-----|
| Add nullable column | Normal | Non-breaking change |
| Schema migration | Think | Data integrity concerns |
| Cross-database query | Think Hard | Performance and consistency |
| Production data migration | Ultrathink | Data loss risk |

### Physical Construction Domain

| Scenario | Level | Why |
|----------|-------|-----|
| Material selection | Normal | Standard choices |
| Structural change | Think | Safety implications |
| Multi-contractor coordination | Think Hard | Dependency management |
| Foundation/structural work | Ultrathink | Irreversible, safety-critical |

### Remote Management Domain

| Scenario | Level | Why |
|----------|-------|-----|
| Status update | Normal | Information only |
| Task assignment | Think | Coordination needed |
| Quality inspection | Think Hard | Remote verification challenges |
| Dispute resolution | Ultrathink | Relationship and financial impact |

---

## Integration with spec-to-prp.sh

The `spec-to-prp.sh` generator should analyze the spec and suggest a thinking level:

```bash
# Example output in generated PRP
## Recommended Thinking Level

Based on analysis of this spec:
- Confidence Score: 5.8/10
- Domains: universal + integration (20 invariants)
- Files Affected: ~8 files
- Novel Elements: Third-party API integration

**Recommended: Think Hard**

Use extended thinking for:
- API contract design decisions
- Error handling strategy
- Fallback mechanism design

Use Ultrathink for:
- Security review of authentication flow
- Production rollout decision
```

---

## Quick Reference Card

```
THINKING LEVEL SELECTION:

Simple + Patterns + High Confidence → Normal
  Examples: Bug fix, config change, UI tweak

Multiple Concerns + Moderate Confidence → Think
  Examples: New feature, refactor, new endpoint

Cross-System + Low Confidence + Multiple Domains → Think Hard
  Examples: Integration, migration, multi-phase project

Critical + Novel + Security + Very Low Confidence → Ultrathink
  Examples: Auth system, production migration, new architecture
```

---

## Anti-Patterns

### Over-Thinking

Don't use Ultrathink for:
- Simple configuration changes
- Well-understood patterns
- Tasks with clear existing examples
- Non-production environments

### Under-Thinking

Don't use Normal for:
- Production database changes
- Security-related code
- Cross-system integrations
- Novel domains without patterns

---

*Guide version: 1.0*
*Last updated: 2026-01-19*
