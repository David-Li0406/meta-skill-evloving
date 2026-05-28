---
name: code-review
description: Quick code review for staged changes or specific files. Checks for security issues, missing error handling, i18n, dark mode, and project patterns. Use /review [file|staged|recent].
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git status:*)
---

# Code Review Skill

## Overview

Performs lightweight code reviews focused on:
- Security vulnerabilities
- Missing error handling
- Project pattern compliance
- i18n completeness
- Dark mode support
- TypeScript best practices

## Commands

- `/review staged` - Review all staged changes
- `/review recent` - Review changes in last commit
- `/review [file]` - Review specific file
- `/review [pattern]` - Review files matching glob pattern

## Review Checklist

### 1. Security (Critical)

**API Routes:**
- [ ] Session authentication check
- [ ] Restaurant access verification
- [ ] Role-based access for write operations
- [ ] Input validation before database operations
- [ ] No SQL injection vulnerabilities
- [ ] No exposed secrets/credentials

**Components:**
- [ ] No dangerouslySetInnerHTML with user content
- [ ] Proper sanitization of displayed data
- [ ] No exposed API keys or secrets

### 2. Error Handling

**API Routes:**
- [ ] Try-catch blocks around database operations
- [ ] Proper error logging with console.error
- [ ] Appropriate HTTP status codes
- [ ] User-friendly error messages

**Components:**
- [ ] Loading states handled
- [ ] Error states displayed
- [ ] Empty states handled

### 3. Project Patterns

**API Routes:**
- [ ] Uses `getServerSession(authOptions)`
- [ ] Checks `session?.user?.id`
- [ ] Verifies restaurant access via UserRestaurant
- [ ] Uses proper response format: `{ data }` or `{ error }`

**Components:**
- [ ] Uses `useLocale()` for text
- [ ] Has dark mode classes paired
- [ ] Uses design system colors (gold-600)
- [ ] Follows naming conventions

### 4. i18n Compliance

- [ ] No hardcoded user-facing strings
- [ ] Uses `t('key')` for all text
- [ ] Keys exist in both en.json and fr.json

### 5. Dark Mode

- [ ] Background: `bg-white dark:bg-gray-800`
- [ ] Border: `border-gray-200 dark:border-gray-700`
- [ ] Text: `text-gray-900 dark:text-white`
- [ ] Muted: `text-gray-500 dark:text-gray-400`

### 6. TypeScript

- [ ] No `any` types (prefer unknown + type guards)
- [ ] Proper interface definitions
- [ ] Nullable types handled

## Output Format

```markdown
## Code Review: {file/scope}

### Critical Issues
- [ ] **Security**: [Description] - Line {n}
- [ ] **Error Handling**: [Description] - Line {n}

### Improvements
- [ ] **i18n**: Missing translations for "..." - Line {n}
- [ ] **Dark Mode**: Missing dark variant for class - Line {n}
- [ ] **Pattern**: Should use [pattern] instead - Line {n}

### Positive Notes
- Good use of [pattern]
- Proper error handling in [function]

### Summary
{X} critical issues, {Y} improvements suggested
```

## Quick Checks by File Type

### API Route (app/api/**/*.ts)

```typescript
// Must have:
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

// Must check:
if (!session?.user?.id) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
}

// Must verify restaurant access:
const userRestaurant = await prisma.userRestaurant.findUnique({...})
```

### Component (components/**/*.tsx)

```typescript
// Must have:
import { useLocale } from '@/components/providers/LocaleProvider'

// Must use:
const { t } = useLocale()

// Must have dark mode pairs:
className="bg-white dark:bg-gray-800"
className="text-gray-900 dark:text-white"
className="border-gray-200 dark:border-gray-700"
```

## Process

When user invokes `/review`:

1. **Identify scope:**
   - `staged` → Run `git diff --cached`
   - `recent` → Run `git diff HEAD~1`
   - `[file]` → Read the specific file
   - `[pattern]` → Glob and read matching files

2. **Analyze each file** against the checklist

3. **Generate report** with:
   - Critical issues (security, errors)
   - Improvement suggestions
   - Positive notes (good patterns found)
   - Summary counts

4. **Provide actionable recommendations**

## Common Issues by Module

### Sales Module
- Missing payment method validation
- Missing status transition validation
- Credit sale without customer reference

### Inventory Module
- Missing stock level validation
- No negative quantity check
- Missing unit conversion handling

### Expenses Module
- Missing receipt URL validation
- No expense group validation
- Missing approval workflow check

## Tips

- Run `/review staged` before committing
- Focus on critical issues first
- Don't over-engineer fixes
- Reference specific line numbers
- Suggest minimal changes
