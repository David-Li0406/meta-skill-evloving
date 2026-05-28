# Design Document Template

## File Location

**IMPORTANT: Design documents go to PROJECT directory (NOT session directory).**

```bash
# Get working directory from session
WORKING_DIR=$(bun $SCRIPTS/session-get.js --session ${CLAUDE_SESSION_ID} --field working_dir)

# Design document path
# Format: {working_dir}/docs/plans/YYYY-MM-DD-{goal-slug}-design.md
DESIGN_PATH="$WORKING_DIR/docs/plans/$(date +%Y-%m-%d)-{goal-slug}-design.md"

# Create directory if needed
mkdir -p "$WORKING_DIR/docs/plans"
```

---

## Template

```markdown
# Design: {Goal}

## Overview
[High-level description of what will be built]

## Approach Selection

### Considered Options
| Option              | Pros | Cons | Fit               |
| ------------------- | ---- | ---- | ----------------- |
| Option A (Selected) | ...  | ...  | Best for our case |
| Option B            | ...  | ...  | ...               |
| Option C            | ...  | ...  | ...               |

### Selected: Option A
**Rationale**: [Why this approach was chosen]

## Decisions

### {Decision Topic 1}
- **Choice**: [Selected option]
- **Rationale**: [Why this was chosen]
- **Alternatives Considered**: [Other options]
- **Asked User**: Yes/No

## Architecture

### Components

#### 1. {Component Name}
- **Files**: `path/to/file.ts`
- **Dependencies**: package-name
- **Description**: What this component does

### Data Flow
```
[Diagram or description of data flow]
```

## Error Handling

### Error Categories
| Category   | Example            | Handling Strategy             |
| ---------- | ------------------ | ----------------------------- |
| Validation | Invalid input      | Return 400 with details       |
| Auth       | Invalid token      | Return 401, redirect to login |
| Not Found  | Resource missing   | Return 404                    |
| Server     | DB connection fail | Return 500, log, alert        |

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": [...]
  }
}
```

### Fallback Strategies
- [Graceful degradation approach]
- [Retry logic if applicable]
- [Circuit breaker if applicable]

## Testing Strategy

### Test Levels
| Level       | Coverage              | Tools              |
| ----------- | --------------------- | ------------------ |
| Unit        | Business logic, utils | Jest/Vitest        |
| Integration | API endpoints, DB     | Supertest          |
| E2E         | Critical user flows   | Playwright/Cypress |

### Key Test Cases
- [ ] Happy path: [describe]
- [ ] Edge case: [describe]
- [ ] Error case: [describe]
- [ ] Auth: [describe]

### Test Data
- Fixtures location: `__tests__/fixtures/`
- Mock strategy: [describe]

## Documentation

### Code Documentation
- JSDoc for public APIs
- README for each module (if complex)
- Inline comments for non-obvious logic only

### API Documentation
- OpenAPI/Swagger spec location: `docs/api/`
- Auto-generated from code annotations

### User Documentation
- [ ] Feature guide in docs/
- [ ] Changelog entry
- [ ] Migration guide (if breaking changes)

## Scope

### In Scope
- Feature 1
- Feature 2

### Out of Scope
- Future feature 1
- Future feature 2

## Assumptions
1. [Assumption 1]
2. [Assumption 2]

## Risks & Mitigations
| Risk     | Impact       | Mitigation        |
| -------- | ------------ | ----------------- |
| [Risk 1] | High/Med/Low | [How to mitigate] |
| [Risk 2] | High/Med/Low | [How to mitigate] |
```

---

## Checklist Before Finalizing

### YAGNI Checklist

- [ ] No features beyond stated goal
- [ ] No "future-proofing" abstractions
- [ ] No optional enhancements
- [ ] Minimum viable scope only
