# Code Review Report Template

## Review Summary

```markdown
## Review Complete

### Source: [mode/spec/commit/feature]
### Scope: [backend/frontend/both]

### Files Reviewed
- [count] backend files
- [count] frontend files

### Issues Found
- [count] Critical
- [count] Important
- [count] Minor

### Fixes Applied
- [list or "None requested"]

### Final Scores
- Backend: X/100
- Frontend: X/100
- Global: X/100

### Recommendations
- [follow-up actions]
```

---

## Detailed Analysis Section

### Files Reviewed

```markdown
### Files Reviewed (from agent reports)
- `path/to/file.go` - [purpose of changes]
- `path/to/file.tsx` - [purpose of changes]
```

### Positive Observations

```markdown
### Positive Observations
- [what was done well]
- [good patterns followed]
- [clean code examples]
```

---

## Quality Score Summary

```markdown
## Global Quality Score: X/100

### Backend Score: X/100
| Criterion | Score | Notes |
|-----------|-------|-------|
| Code cleanliness | X/25 | [notes] |
| Clean Architecture | X/25 | [notes] |
| Error handling | X/25 | [notes] |
| Performance | X/25 | [notes] |

### Frontend Score: X/100
| Criterion | Score | Notes |
|-----------|-------|-------|
| Code correctness | X/20 | [notes] |
| TypeScript usage | X/20 | [notes] |
| Performance | X/20 | [notes] |
| i18n compliance | X/20 | [notes] |
| Best practices | X/20 | [notes] |

**Formula:** (Backend Score x backend_files + Frontend Score x frontend_files) / total_files
```

---

## Recommended Fixes

```markdown
## Recommended Fixes

### Critical (must fix)
1. **[Issue Title]**
   - File: `path/to/file.go:123`
   - Problem: [clear description of what's wrong]
   - Fix: [specific steps to fix]
   - Risk if not fixed: [impact]

### Important (should fix)
1. **[Issue Title]**
   - File: `path/to/file.tsx:45`
   - Problem: [description]
   - Fix: [how to fix]

### Nice-to-have
1. **[Issue Title]**
   - File: `path/to/file.ts:78`
   - Suggestion: [improvement]
```

---

## Verification Checklist

```markdown
## Verification

### Build Status
- [ ] Backend: `go build ./...` passes
- [ ] Backend: `go vet ./...` passes
- [ ] Frontend: `npm run build` passes

### Database (if applicable)
- [ ] No security advisors: `mcp__supabase-dev__get_advisors`
- [ ] RLS policies in place

### Manual Testing
- [ ] [Specific test case 1]
- [ ] [Specific test case 2]
```

---

## Next Steps

```markdown
## Next Steps

1. [Immediate action needed]
2. [Follow-up task]
3. [Future improvement to consider]
```
