---
name: tech-debt-inventory
description: Systematically catalog and prioritize technical debt across the codebase. Use during planning cycles, before major refactors, or when the codebase feels increasingly difficult to work with.
---

# Tech Debt Inventory

Systematic identification, categorization, and prioritization of technical debt.

## Debt Categories

### 1. Code Debt
- Functions exceeding 50 lines
- Files approaching 300 lines (per AGENTS.md)
- `any` types that need proper typing
- TODO/FIXME/HACK comments in code
- Commented-out code blocks
- Copy-pasted logic (DRY violations)
- Inconsistent patterns across similar features

### 2. Architecture Debt
- Tight coupling between modules
- Circular dependencies
- Misplaced responsibilities (wrong layer)
- Missing abstractions
- Over-engineered abstractions
- Inconsistent data flow patterns

### 3. Testing Debt
- Missing unit tests for utilities
- Missing integration tests for APIs
- No E2E coverage for critical paths
- Flaky tests that are skipped
- Test data that's hard to maintain

### 4. Documentation Debt
- Outdated README sections
- Missing API documentation
- Stale inline comments
- Undocumented environment variables
- Missing architectural decision records

### 5. Dependency Debt
- Outdated packages with security issues
- Deprecated APIs still in use
- Multiple libraries for same purpose
- Packages not tree-shaking properly

### 6. Infrastructure Debt
- Manual deployment steps
- Missing environment parity
- Hardcoded configuration
- Missing health checks
- Inadequate monitoring

### 7. Schema Debt
- Missing database indexes
- Denormalization without justification
- Inconsistent naming conventions
- Missing foreign key constraints
- Orphan data potential

### 8. UX Debt
- Inconsistent UI patterns
- Missing loading states
- Poor error messages
- Accessibility gaps
- Mobile responsiveness issues

## Debt Scoring Matrix

| Factor | Weight | Description |
|--------|--------|-------------|
| **Impact** | 40% | How much does this slow down development? |
| **Risk** | 30% | Could this cause production issues? |
| **Effort** | 20% | How hard is it to fix? (inverse) |
| **Age** | 10% | How long has this existed? |

### Impact Scoring
- **5**: Blocks feature development
- **4**: Significantly slows every PR
- **3**: Regularly causes confusion
- **2**: Occasional friction
- **1**: Minor annoyance

### Risk Scoring
- **5**: Security vulnerability or data loss potential
- **4**: Could cause production outage
- **3**: Could cause user-facing bugs
- **2**: Internal tooling issues
- **1**: Code aesthetics only

## Output Format

```
## Debt Item: [Short Title]

**ID**: DEBT-XXX
**Category**: Code|Architecture|Testing|Documentation|Dependency|Infrastructure|Schema|UX
**Location**: File path or module name
**Introduced**: Approximate date or PR if known

**Description**:
[What the debt is and why it exists]

**Impact**: X/5
[How it affects development velocity]

**Risk**: X/5
[What could go wrong]

**Effort**: S|M|L|XL
[Estimated fix effort]

**Priority Score**: X.X
[Calculated from matrix]

**Proposed Solution**:
[How to address this debt]

**Dependencies**:
[Other debt items or features this relates to]

---
```

## Actions

1. Scan for TODO/FIXME/HACK comments
2. Identify files over 300 lines
3. Find `any` types in TypeScript
4. Check for outdated dependencies
5. Review missing test coverage
6. Audit documentation freshness
7. Check for inconsistent patterns

## Inventory Process

1. **Discover**: Automated scans + team input
2. **Categorize**: Assign to debt category
3. **Score**: Apply scoring matrix
4. **Prioritize**: Rank by priority score
5. **Plan**: Allocate to sprints/quarters
6. **Track**: Update as debt is addressed

## Integration with Development

Per AGENTS.md principles:
- Don't add new debt without documenting it
- Address debt opportunistically during related work
- Allocate ~20% of sprint capacity to debt reduction
- Celebrate debt payoff in retrospectives

## Post-Inventory

Generate:
- Prioritized debt backlog
- Debt by category breakdown
- High-risk items requiring immediate attention
- Quick wins (high impact, low effort)
- Quarterly debt reduction plan
- Metrics for tracking debt over time
