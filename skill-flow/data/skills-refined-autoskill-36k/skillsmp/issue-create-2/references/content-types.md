# Content Types Reference

This document defines the content types detected by the issue-create skill and their associated templates.

## Supported Content Types

### Bug

**Detection indicators:**

- Keywords: bug, error, crash, broken, fail, exception, stacktrace
- Patterns: "not working", "doesn't work", TypeError, ReferenceError

**Template:**

```markdown
## Description

{CONTENT}

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

## Actual Behavior

## Environment

- OS:
- Version:
```

**Suggested labels:** bug, defect, error, issue

---

### Feature

**Detection indicators:**

- Keywords: feature, enhancement, add, implement, support, would be nice
- Patterns: "I want", "could you add", "suggestion"

**Template:**

```markdown
## Summary

{CONTENT}

## Use Case

## Proposed Solution

## Alternatives Considered
```

**Suggested labels:** enhancement, feature, feature-request, improvement

---

### Question

**Detection indicators:**

- Keywords: how, what, why, when, where, which
- Patterns: Questions ending with "?", "help", "confused"

**Template:**

```markdown
## Question

{CONTENT}

## Context

## What I've Tried
```

**Suggested labels:** question, help wanted, support

---

### Documentation

**Detection indicators:**

- Keywords: docs, documentation, readme, typo, spelling
- Patterns: "example", "tutorial", "guide", "outdated"

**Template:**

```markdown
## Description

{CONTENT}

## Location

## Suggested Change
```

**Suggested labels:** documentation, docs, readme

---

## Title Prefixes

| Type          | Prefix      |
| ------------- | ----------- |
| Bug           | `Bug:`      |
| Feature       | `Feature:`  |
| Question      | `Question:` |
| Documentation | `Docs:`     |
| Unknown       | (none)      |

## Detection Priority

When multiple types are detected, priority is:

1. Bug (error indicators take precedence)
2. Question (explicit question marks)
3. Feature (enhancement requests)
4. Documentation (doc-specific terms)
5. Unknown (default fallback)
