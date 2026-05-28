# Thinking Level Rubric

> Quick reference for selecting appropriate thinking depth.

---

## Decision Matrix

| Factor | Normal | Think | Think Hard | Ultrathink |
|--------|--------|-------|------------|------------|
| **Confidence Score** | 8-10 | 6-7.9 | 4-5.9 | 1-3.9 |
| **Invariants Applied** | 1-10 | 11-20 | 21-30 | 30+ |
| **Files Affected** | 1-3 | 4-10 | 11-20 | 20+ |
| **Domains Involved** | 1 | 2 | 3 | 4+ |
| **Pattern Availability** | Exact match | Minor adapt | Major adapt | None |
| **Rollback Difficulty** | Trivial | Easy | Moderate | Difficult |

---

## Quick Selection

### Use Normal When:

- [ ] Following an exact existing pattern
- [ ] Confidence score > 7/10
- [ ] Single file or few-file change
- [ ] Non-production impact
- [ ] Easy rollback path

### Use Think When:

- [ ] Adapting pattern to new context
- [ ] Multiple acceptance criteria
- [ ] Cross-file changes
- [ ] Moderate business logic
- [ ] Some unknowns exist

### Use Think Hard When:

- [ ] Multiple domains apply
- [ ] Cross-system integration
- [ ] Data migration involved
- [ ] External dependencies
- [ ] Confidence 4-6/10

### Use Ultrathink When:

- [ ] Security/authentication changes
- [ ] Production data at risk
- [ ] No existing patterns
- [ ] Critical infrastructure
- [ ] Confidence < 4/10

---

## By Task Type

| Task | Default Level |
|------|---------------|
| Config change | Normal |
| Bug fix (known cause) | Normal |
| UI text update | Normal |
| New API endpoint | Think |
| New user flow | Think |
| Database schema change | Think Hard |
| Third-party integration | Think Hard |
| Auth system change | Ultrathink |
| Production migration | Ultrathink |
| New architectural pattern | Ultrathink |

---

## Escalation Triggers

Bump up one level if:

- [ ] Previous attempt at this level failed
- [ ] Stakeholder flagged as high-priority
- [ ] Timeline is tight (less margin for error)
- [ ] Similar past project had issues
- [ ] Team unfamiliar with domain

---

## PRP Template Section

Add to PRP after Confidence Score:

```markdown
## Recommended Thinking Level

**Level**: [Normal | Think | Think Hard | Ultrathink]

**Factors**:
- Confidence: X/10
- Domains: [list]
- Invariants: X applicable
- Files: ~X affected
- Pattern: [exact | adapt | none]

**Apply higher thinking to**:
- [Specific decision or component]
- [Specific decision or component]
```

---

*Rubric version: 1.0*
