---
name: coderabbit
description: "Use when working with CodeRabbit AI code review. Covers triggering reviews, interpreting feedback, addressing comments, and PR workflow integration."
---

# CodeRabbit Integration

## Overview

CodeRabbit provides AI-powered code review for pull requests. This skill covers how to trigger reviews, interpret feedback, and address comments effectively.

## When to Use

- PR created and awaiting review
- Need to understand CodeRabbit comments
- Want to re-trigger or customize review
- Integrating CodeRabbit into PR workflow

## Quick Reference

| Action | Command/Method |
|--------|----------------|
| **Trigger review** | Auto on PR, or `@coderabbitai review` |
| **Full review** | `@coderabbitai full review` |
| **Specific files** | `@coderabbitai review src/auth/*` |
| **Ignore file** | `@coderabbitai ignore` on comment |
| **Summary** | `@coderabbitai summary` |

---

## Triggering CodeRabbit Review

### Automatic Trigger
CodeRabbit reviews PRs automatically when:
- New PR is opened
- New commits are pushed to PR branch

### Manual Triggers

```markdown
# Full review of entire PR
@coderabbitai full review

# Review specific files
@coderabbitai review src/components/Button.tsx

# Review specific paths
@coderabbitai review src/auth/*

# Get summary only
@coderabbitai summary

# Generate PR description
@coderabbitai generate description
```

---

## Interpreting Feedback

### Comment Types

| Type | Meaning | Action Required |
|------|---------|-----------------|
| **Bug** | Potential runtime error | Fix immediately |
| **Security** | Security vulnerability | Fix immediately |
| **Performance** | Inefficient code | Evaluate and fix |
| **Best Practice** | Code quality suggestion | Consider applying |
| **Style** | Formatting/convention | Apply if team standard |
| **Nitpick** | Minor suggestion | Optional |

### Priority Order

1. **Security issues** - Fix before merge
2. **Bugs** - Fix before merge
3. **Performance** - Evaluate impact, usually fix
4. **Best practices** - Apply when reasonable
5. **Style/Nitpicks** - Team discretion

---

## Addressing Comments

### Workflow

```markdown
1. Read CodeRabbit comment
2. Determine action:
   - Fix: Make code change, push commit
   - Explain: Reply with reasoning
   - Disagree: Reply with justification
   - Ignore: Mark as resolved with reason

3. Reply to comment:
   - "Fixed in abc123"
   - "Intentional because [reason]"
   - "Won't fix: [justification]"

4. Resolve conversation when addressed
```

### Response Templates

**Fixed:**
```markdown
Fixed in [commit hash]. Added validation as suggested.
```

**Intentional:**
```markdown
Intentional - this pattern is used for [reason].
See [link to docs/discussion] for context.
```

**Won't Fix:**
```markdown
Acknowledged, but won't fix because:
- [reason 1]
- [reason 2]
Marking as resolved.
```

**Need Clarification:**
```markdown
@coderabbitai Can you clarify? I don't understand how [X] applies here.
```

---

## CodeRabbit Commands

### In PR Comments

```markdown
# Pause reviews on this PR
@coderabbitai pause

# Resume reviews
@coderabbitai resume

# Ignore specific file in future reviews
@coderabbitai ignore path/to/file.ts

# Get help
@coderabbitai help
```

### Configuration

CodeRabbit is configured via `.coderabbit.yaml`:

```yaml
reviews:
  auto_review: true
  path_instructions:
    - path: "src/components/**"
      instructions: "Focus on React best practices"
    - path: "src/api/**"
      instructions: "Check for proper error handling"
```

---

## Common Patterns

### Bulk Address Feedback

When CodeRabbit raises multiple similar issues:

```bash
# 1. List all comments
gh pr view --comments | grep -A5 "coderabbit"

# 2. Make bulk fix
# ... apply pattern fix across files ...

# 3. Single commit addressing all
git commit -m "fix: address CodeRabbit review feedback

- Add error handling to all API calls
- Fix type safety issues
- Update deprecated APIs"

# 4. Push and reply
git push
```

### Disagree Professionally

```markdown
Thanks for the suggestion. I've considered this but will keep
the current approach because:

1. [Technical reason]
2. [Team convention]
3. [Performance consideration]

Happy to discuss further if you see issues I'm missing.
```

---

## Integration with PR Workflow

### Pre-Merge Checklist

- [ ] All CodeRabbit security issues addressed
- [ ] All CodeRabbit bugs fixed
- [ ] Performance suggestions evaluated
- [ ] Unaddressed comments explained

### When to Request Human Review

After CodeRabbit review:
1. Address all critical issues
2. Reply to suggestions
3. Push fixes
4. Then request human reviewers

---

## Red Flags - STOP

**Never:**
- Ignore security findings
- Merge with unresolved bugs
- Dismiss without explanation

**Always:**
- Read each comment fully
- Respond to actionable items
- Document disagreements
- Fix security issues immediately

---

## Integration

**Related skills:** submit-pr, git-expert
**Pairs with:** verification, tdd
