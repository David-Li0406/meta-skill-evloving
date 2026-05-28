# Principles Guide

> **SoT 참조**: Constitution 원칙의 정의는 `semo-core/PRINCIPLES.md`에서 관리됩니다.

## Constitution Structure

```markdown
# Project Constitution v1.2.0

**Last Updated**: 2025-01-20
**Status**: ACTIVE

---

## Preamble
[Purpose and scope]

---

## I. [Principle Name] (NON-NEGOTIABLE | FLEXIBLE)

**Statement**: [Core principle]

**Rationale**: [Why this matters]

**Implementation**:
- [Requirement 1]
- [Requirement 2]
- **Exception**: [If any]

**Validation**: [How to check compliance]

---

## Changelog

### v1.2.0 (2025-01-20)
- Updated Principle VII: Added RPC type assertion exception
```

## Principle Categories

### NON-NEGOTIABLE

Cannot be violated without Constitution amendment:

- Principle I: DDD Architecture
- Principle II: SSR-First
- Principle III: Test-Driven Quality
- Principle VII: Type Safety
- Principle VIII: Spec-Driven Development

### FLEXIBLE

Can have exceptions with justification:

- Principle IV: Performance Excellence
- Principle V: API Mode Flexibility
- Principle VI: Atomic Design System
- Principle IX: Agent-Driven Collaboration

## Template Synchronization

These files must stay synchronized with Constitution:

### Required Updates

- `.specify/memory/constitution.md` (primary source)
- `.claude/commands/help.md` (user-facing guide)
- `README.md` (quick reference)

### Conditional Updates

- `.claude/commands/speckit.*.md` (if principles referenced)
- `.claude/skills/*/SKILL.md` (if principles mentioned)
- `docs/` directory (if principle guides exist)

## Versioning Rules

### Version Format: `vMAJOR.MINOR.PATCH`

**MAJOR** (v1 → v2):

- Complete Constitution rewrite
- Fundamental principle changes
- Breaking changes to workflow

**MINOR** (v1.1 → v1.2):

- New principle added
- Existing principle significantly updated
- Non-breaking enhancements

**PATCH** (v1.1.0 → v1.1.1):

- Clarifications
- Typo fixes
- Minor wording improvements
