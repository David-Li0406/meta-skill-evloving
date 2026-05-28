---
id: error-recovery
name: "Help Users Recognize, Diagnose, and Recover from Errors"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Help Users Recognize, Diagnose, and Recover from Errors

## Metadata
- **Category:** UX / Usability Heuristic #9
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #heuristics #nielsen-norman #errors
- **Agent:** faion-usability-agent

---

## Problem

Error messages are cryptic and unhelpful. Users see "Error occurred" with no explanation. Technical codes mean nothing to regular users. Messages blame users instead of helping. Users do not know how to fix the problem and cannot continue.

Without good error handling:
- Users stuck
- Abandonment
- Support tickets
- Frustration and distrust

---

## The Heuristic

**Usability Heuristic #9:** Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.

---

## Framework

### Effective Error Messages

| Component | Purpose | Example |
|-----------|---------|---------|
| **What happened** | Explain the problem | "Password is too short" |
| **Why it happened** | Provide context | "Passwords must be at least 8 characters" |
| **How to fix it** | Guide to solution | "Add 3 more characters" |

### Error Message Principles

1. **Be human** - Plain language, not technical
2. **Be specific** - Exact problem, not generic
3. **Be helpful** - Show how to fix
4. **Be humble** - Do not blame the user
5. **Be visible** - Clearly noticeable

---

## Implementation Patterns

### Clear Problem Statement

**Bad:**
```
Error 403
```

**Better:**
```
Access denied
```

**Best:**
```
You don't have permission to view this page.
Contact your administrator for access.
```

### Specific Details

**Bad:**
```
Invalid input
```

**Better:**
```
Invalid email address
```

**Best:**
```
This email address is missing the @ symbol.
Example: name@company.com
```

### Actionable Solutions

**Bad:**
```
Connection failed
```

**Better:**
```
Cannot connect to server
```

**Best:**
```
Cannot connect to server.
Please check your internet connection and try again.
[Retry] [Work Offline]
```

### Proper Placement

**Inline validation:**
```
Place error message next to the field with the problem
User does not need to search for the issue
```

**Form summary:**
```
When multiple errors exist:
"Please fix 3 errors below" (with links)
Plus inline errors at each field
```

---

## Templates

### Error Message Template

```markdown
# Error Message Design: [Error Type]

## Error Details
- **When it occurs:** [Trigger condition]
- **Technical cause:** [System reason]
- **User impact:** [What user cannot do]

## Message Content

### What happened
[Human-readable description of the problem]

### Why it happened
[Brief explanation of the cause]

### How to fix it
[Specific action the user can take]

## Visual Design
- **Placement:** [Where to show]
- **Style:** [Error styling - red border, icon, etc.]
- **Timing:** [When to show/hide]

## Actions Available
- [Primary action button]
- [Secondary action if applicable]

## Example Message
```
[Title/Summary]

[Detailed explanation]

[Suggested fix]

[Action buttons]
```
```

### Error Handling Audit

```markdown
# Error Handling Audit: [Feature]

**Date:** [Date]
**Reviewer:** [Name]

## Error Messages Reviewed

| Error | Current Message | Issues | Improved Message |
|-------|-----------------|--------|------------------|
| [Error] | [Current] | [Problems] | [Better version] |

## Error Placement

| Context | Placement | Appropriate? | Notes |
|---------|-----------|--------------|-------|
| [Context] | [Location] | Y/N | [Notes] |

## Recovery Options

| Error | Recovery Path | Clear? | Additional Options |
|-------|---------------|--------|-------------------|
| [Error] | [Current path] | Y/N | [Suggestions] |

## Priority Fixes

1. [Highest priority error to improve]
2. [Second priority]
3. [Third priority]
```

---

## Examples

### Good Examples

**Stripe payment error:**
```
Your card was declined

Your card number is incorrect. Please check
the number and try again.

[Try a different card]
```

**GitHub 404:**
```
This is not the web page you are looking for.

The page you requested doesn't exist. You may have
typed the address incorrectly or the page may have moved.

[Go to GitHub.com] [Search GitHub]
```

**Form validation:**
```
Password must contain:
✓ At least 8 characters
✗ One uppercase letter (add one)
✗ One number (add one)
```

### Bad Examples

**Cryptic error:**
```
Error: ECONNREFUSED
```

**Vague error:**
```
Something went wrong
```

**Blaming error:**
```
You entered invalid data
```

**Dead end:**
```
Error occurred
[OK]
(No way to fix or retry)
```

---

## Error Types and Handling

### Validation Errors

```
Show: Immediately as user types or on blur
Message: What is wrong + how to fix
Placement: Inline, next to field
Recovery: User corrects input
```

### System Errors

```
Show: When operation fails
Message: What happened + suggested action
Placement: Modal or banner
Recovery: Retry, alternative action, support contact
```

### 404 Not Found

```
Show: When page does not exist
Message: Page not found + suggestions
Placement: Full page
Recovery: Links to home, search, common pages
```

### Network Errors

```
Show: When connection fails
Message: Connection issue + retry option
Placement: Banner or modal
Recovery: Retry, offline mode, check connection
```

---

## Common Mistakes

1. **Technical language** - Error codes instead of words
2. **Generic messages** - "Error" without specifics
3. **No solution** - Problem stated but no fix
4. **Hidden errors** - Errors not visible
5. **Blame language** - "You did something wrong"

---

## Writing Guidelines

### Do
- Use plain language
- Be specific about the problem
- Provide a clear solution
- Use a calm, helpful tone
- Include actions (buttons/links)

### Don't
- Use technical jargon
- Use error codes alone
- Blame the user
- Be vague
- Create dead ends

---

## Accessibility Requirements

- Do not rely on color alone (use icons/text)
- Use ARIA for error announcements
- Focus management to error location
- Sufficient color contrast
- Error text readable by screen readers

---

## Checklist

- [ ] All error messages are in plain language
- [ ] Messages explain what went wrong
- [ ] Messages tell users how to fix the problem
- [ ] Messages do not blame users
- [ ] Errors are placed near the problem
- [ ] Form errors have summary and inline placement
- [ ] Recovery actions are available
- [ ] Errors are accessible (not color-only)

---

## References

- UX research community: 10 Usability Heuristics
- Error Message Guidelines
- Microcopy Best Practices