# Implementation Checklists

Pre-flight and quality checklists for sprint implementation.

## SemVer Requirements

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backwards-compatible additions)
- **PATCH**: Bug fixes (backwards-compatible fixes)

### When to Update Version

| Change | Bump | Example |
|--------|------|---------|
| New feature implementation | MINOR | 0.1.0 → 0.2.0 |
| Bug fix | PATCH | 0.2.0 → 0.2.1 |
| Breaking API change | MAJOR | 0.2.1 → 1.0.0 |

### Version Update Process

1. Determine bump type based on changes
2. Update package.json version
3. Update CHANGELOG.md with sections: Added, Changed, Fixed, Removed, Security
4. Reference version in completion comments

---

## Checklists

See `resources/REFERENCE.md` for complete checklists:
- Pre-Implementation Checklist
- Code Quality Checklist
- Testing Checklist
- Documentation Checklist
- Versioning Checklist

### Red Flags (immediate action required)

- [ ] No tests for new code
- [ ] Hardcoded secrets
- [ ] Skipped error handling
- [ ] Ignored existing patterns

---

## Pre-Implementation Checklist

Before starting any task:

- [ ] Read `grimoires/loa/sprint.md` for acceptance criteria
- [ ] Read `grimoires/loa/sdd.md` for technical architecture
- [ ] Read `grimoires/loa/prd.md` for business requirements
- [ ] Check for existing feedback files in `grimoires/loa/a2a/sprint-N/`
- [ ] Review existing codebase patterns
- [ ] Identify task dependencies

---

## Code Quality Checklist

During implementation:

- [ ] Self-documenting with clear names
- [ ] Comments for complex logic only
- [ ] DRY principles applied
- [ ] Consistent formatting
- [ ] Handles edge cases
- [ ] Proper error handling
- [ ] No hardcoded values

---

## Testing Checklist

For every change:

- [ ] Unit tests for new functions
- [ ] Happy path tested
- [ ] Error conditions tested
- [ ] Edge cases covered
- [ ] Tests are readable
- [ ] Tests follow existing patterns

---

## Documentation Checklist

Before completing:

- [ ] Code is self-documenting
- [ ] Complex logic has comments
- [ ] API changes documented
- [ ] CHANGELOG updated
- [ ] Version bumped if needed

---

## Success Criteria

- **Specific**: Every task implemented per acceptance criteria
- **Measurable**: Test coverage metrics included
- **Achievable**: All sprint tasks completed
- **Relevant**: Implementation matches PRD/SDD
- **Time-bound**: Report generated for review
