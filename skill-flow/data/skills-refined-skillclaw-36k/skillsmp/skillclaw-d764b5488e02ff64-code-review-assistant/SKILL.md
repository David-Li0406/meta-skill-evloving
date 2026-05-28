---
name: code-review-assistant
description: Use this skill when you need a systematic checklist for code reviews and pre-commit quality checks, especially for reviewing pull requests and ensuring code quality.
---

# Code Review Assistant

> **Language**: [English](../../../../../skills/claude-code/code-review-assistant/SKILL.md) | 中文

**Version**: 1.0.0  
**Last Updated**: 2025-12-24  
**Applicable Scope**: Claude Code Skills

---

## Purpose

This skill provides a systematic checklist for code reviews and pre-commit validation.

## Quick Reference

### Comment Prefixes

| Prefix | Meaning | Action Required |
|--------|---------|------------------|
| **❗ BLOCKING** | Must be fixed before merging | 🔴 Required |
| **⚠️ IMPORTANT** | Should be fixed, but does not block merging | 🟡 Suggested |
| **💡 SUGGESTION** | Areas for improvement | 🟢 Optional |
| **❓ QUESTION** | Needs clarification | 🔵 Discussion |
| **📝 NOTE** | Informational, no action needed | ⚪ Information |

### Review Checklist Categories

1. **Functionality** - Does it work as intended?
2. **Design** - Is the architecture correct?
3. **Quality** - Is the code clean?
4. **Readability** - Is it easy to understand?
5. **Testing** - Is the coverage sufficient?
6. **Security** - Are there vulnerabilities?
7. **Performance** - Is it efficient?
8. **Error Handling** - Is it handled properly?
9. **Documentation** - Is it updated?
10. **Dependencies** - Are they necessary?

### Pre-commit Checklist

- [ ] Build succeeds (zero errors, zero warnings)
- [ ] All tests pass
- [ ] Code adheres to project standards
- [ ] No security vulnerabilities
- [ ] Documentation is updated
- [ ] Branch is synced with the target

## Detailed Guide

For complete standards, refer to:
- [Review Checklist](./review-checklist.md)
- [Pre-commit Checklist](./checkin-checklist.md)

## Review Comment Examples

```markdown
❗ BLOCKING: There is a potential SQL injection vulnerability here.
Please use parameterized queries instead of string concatenation.

⚠️ IMPORTANT: This method does too much (120 lines).
Consider extracting the validation logic into a separate method.

💡 SUGGESTION: Consider using Map instead of an array for O(1) lookups.

❓ QUESTION: Why is setTimeout used here instead of async/await?

📝 NOTE: This is a clever solution! It makes good use of reduce.
```

## Core Principles

1. **Be Respectful** - Review the code, not the person.
2. **Be Thorough** - Check functionality, not just syntax.
3. **Be Timely** - Complete reviews within 24 hours.
4. **Be Clear** - Explain "why," not just "what."

---

## Configuration Detection

This skill supports project-specific configurations.

### Detection Order

1. Check the "Disabled Skills" section in `CONTRIBUTING.md`
   - If this skill is listed, disable it for this project.
2. Check the "Code Review Language" section in `CONTRIBUTING.md`
3. If not found, **default to English**

### Initial Setup

If no configuration is found and the context is unclear:

1. Ask the user: "This project has not configured a code review language. Which option would you like to use? (English / 中文)"
2. After the user selects, suggest recording it in `CONTRIBUTING.md`:

```markdown
## Code Review Language

This project uses **[chosen option]** for code review comments.
<!-- Options: English | 中文 -->
```

### Configuration Example

In the project's `CONTRIBUTING.md`:

```markdown
## Code Review Language

This project uses **English** for code review comments.
<!-- Options: English | 中文 -->

### Comment Prefixes
BLOCKING, IMPORTANT, SUGGESTION, QUESTION, NOTE
```

---

## Related Standards

- [Code Review Checklist](../../core/code-review-checklist.md)
- [Checkin Standards](../../core/checkin-standards.md)
- [Testing Standards](../../core/testing-standards.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---|