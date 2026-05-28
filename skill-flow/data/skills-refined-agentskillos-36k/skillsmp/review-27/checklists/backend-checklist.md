# Backend Code Review Checklist

## Quality Score Criteria (100 points total)

### Code Cleanliness (25 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| No unused imports/variables | 5 | `go vet` passes |
| Consistent naming (PascalCase structs, camelCase vars) | 5 | Manual review |
| No duplicated code blocks | 5 | Scan for similar patterns |
| Functions < 50 lines | 5 | Large functions split |
| Clear comments for complex logic | 5 | Non-obvious code documented |

### Clean Architecture (25 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| Domain layer has no external deps | 5 | Only standard lib |
| Repository interfaces in domain | 5 | Not in infrastructure |
| Use cases in application layer | 5 | Orchestration only |
| Handlers only in presentation | 5 | No business logic |
| Dependency injection used | 5 | No hardcoded deps |

### Error Handling (25 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| All errors are handled | 10 | No ignored errors |
| Custom errors where appropriate | 5 | Domain-specific errors |
| No internal errors exposed to API | 5 | User-friendly messages |
| Proper logging (Warn for retryable) | 5 | No ERROR for retryable |

### Performance (25 points)

| Criterion | Points | Check |
|-----------|--------|-------|
| context.Context as first param | 10 | All I/O operations |
| No N+1 queries | 5 | Batch where possible |
| Proper connection pooling | 5 | DB connections managed |
| Goroutines cleaned up | 5 | No leaks |

---

## Issue Categories

### Backend Issues Format

```markdown
### Backend Issues

#### Duplications Found
- [description] in files X and Y

#### Clean Architecture Violations
- [description] - should follow pattern from [existing file]

#### Unused Code
- `function_name` in `file.go` - never called

#### Context Propagation Issues
- Missing context.Context in [function]

#### Error Handling Issues
- [description]

#### Performance Issues
- [description]
```

---

## Score Calculation

```markdown
## Backend Quality Score: X/100

| Criterion | Score | Notes |
|-----------|-------|-------|
| Code cleanliness | X/25 | [notes] |
| Clean Architecture | X/25 | [notes] |
| Error handling | X/25 | [notes] |
| Performance | X/25 | [notes] |
```

---

## Common Issues to Flag

### Critical (must fix)
- Nil pointer dereference potential
- SQL injection vulnerabilities
- Missing authentication/authorization
- Data races in concurrent code
- Exposed internal errors
- Missing context cancellation handling

### Important (should fix)
- Clean Architecture violations
- Missing error handling
- Hardcoded values
- Missing input validation
- Inefficient queries
- Missing logging

### Nice-to-have
- Code style inconsistencies
- Missing comments on complex logic
- Long functions that could be split
- Unused parameters
