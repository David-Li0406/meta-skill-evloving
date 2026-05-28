# Bug Issue Template

Use this template when something is broken or failing.

## Template

```markdown
**Title:** [Bug] {Component} - {Brief description}
**Labels:** bug
**Priority:** {Based on impact - Urgent/High/Medium/Low}

## Problem
{What's broken - from user's description}

## Context (Auto-gathered)
**Files involved:**
- `{path/to/file.ts}:{line}` - {what this file does}

**Current behavior:**
{From investigation}

**Related code:**
```{language}
{Relevant snippet showing the problem}
```

## Reproduction
{Steps to reproduce, or "Needs investigation" if unclear}

## Expected vs Actual
- **Expected:** {What should happen}
- **Actual:** {What happens instead}

## Fix Verification
```bash
{Test command if identifiable}
```
```

## Example

**User says:** "The login form breaks when I use special characters"

**Created issue:**
```markdown
**Title:** [Bug] LoginForm - Special characters cause validation failure
**Labels:** bug
**Priority:** High

## Problem
Login form breaks when user enters special characters in password field.

## Context (Auto-gathered)
**Files involved:**
- `src/components/LoginForm.tsx:45` - Main form component
- `src/utils/validation.ts:12` - Validation logic (missing special char handling)

**Current behavior:**
Validation function only checks length, doesn't handle special characters.

**Related code:**
```typescript
// src/utils/validation.ts:12
export function validatePassword(pwd: string): boolean {
  return pwd.length >= 8; // No special char handling
}
```

**Pattern in codebase:**
Other forms use `sanitizeInput()` from `src/utils/strings.ts`

## Reproduction
1. Go to login page
2. Enter email
3. Enter password with special chars (e.g., "p@ss!word")
4. Click submit

## Expected vs Actual
- **Expected:** Form submits successfully
- **Actual:** Validation error shown

## Fix Verification
```bash
npm test -- LoginForm.test.tsx
```
```
