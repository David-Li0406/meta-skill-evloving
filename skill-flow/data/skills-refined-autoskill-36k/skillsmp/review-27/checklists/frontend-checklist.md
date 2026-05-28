# Frontend Code Review Checklist

## Quality Score Criteria (100 points total)

### Code Correctness (20 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| No runtime errors | 5 | Code runs without crashes |
| Proper null/undefined handling | 5 | Optional chaining, guards |
| Correct hook dependencies | 5 | useEffect/useMemo deps |
| No stale closures | 5 | Refs for callbacks |

### TypeScript Usage (20 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| No `any` types | 5 | Strict typing |
| Proper interface definitions | 5 | Props, API responses typed |
| Generic types where appropriate | 5 | Reusable type patterns |
| Type guards for runtime checks | 5 | Discriminated unions |

### Performance (20 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| Proper memoization | 5 | useMemo/useCallback |
| No unnecessary re-renders | 5 | React DevTools check |
| Suspense boundaries | 5 | For async components |
| Lazy loading where needed | 5 | Dynamic imports |

### i18n Compliance (20 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| All user-facing text uses next-intl | 10 | No hardcoded strings |
| Messages in locale files | 5 | `messages/{locale}.json` |
| Proper pluralization | 5 | When applicable |

### Best Practices (20 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| Components < 200 lines | 5 | Split large components |
| Proper error boundaries | 5 | Graceful error handling |
| Accessibility (a11y) | 5 | aria-labels, keyboard nav |
| Consistent naming | 5 | PascalCase components |

---

## Issue Categories

### Frontend Issues Format

```markdown
### Frontend Issues

#### Duplications Found
- [description] in components X and Y

#### Pattern Violations
- [description] - should follow pattern from [existing component]

#### Unused Code
- `ComponentName` in `file.tsx` - never used

#### TypeScript Issues
- `any` type used in [file]
- Missing types for [props/state]

#### i18n Issues
- Hardcoded string "[text]" in [component] - use next-intl

#### Accessibility Issues
- Missing aria-label in [component]
- Missing keyboard navigation in [component]

#### Performance Issues
- Missing memoization in [component]
- Unnecessary re-renders in [component]
- Missing Suspense boundaries
```

---

## Score Calculation

```markdown
## Frontend Quality Score: X/100

| Criterion | Score | Notes |
|-----------|-------|-------|
| Code correctness | X/20 | [notes] |
| TypeScript usage | X/20 | [notes] |
| Performance | X/20 | [notes] |
| i18n compliance | X/20 | [notes] |
| Best practices | X/20 | [notes] |
```

---

## Common Issues to Flag

### Critical (must fix)
- XSS vulnerabilities (dangerouslySetInnerHTML)
- Missing authentication checks
- Exposed API keys/secrets
- Memory leaks (uncleared intervals/subscriptions)
- Broken accessibility (no keyboard nav for interactive elements)

### Important (should fix)
- Hardcoded strings (i18n violations)
- Missing TypeScript types
- Missing error handling
- Missing loading states
- Missing form validation
- Uncaught promise rejections

### Nice-to-have
- Missing memoization
- Long components that could be split
- Inconsistent naming
- Missing JSDoc comments
- Unused imports
