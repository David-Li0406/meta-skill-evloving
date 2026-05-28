# Implementation Details Reference

Extended reference for `agent-ops-impl-details` skill with examples and templates.

---

## What "Extensive" Means

**Extensive level MUST include actual, executable code — NOT pseudo-code.**

❌ **Wrong** (pseudo-code):
```
function processUser:
  validate input
  fetch from database
  return result
```

✅ **Correct** (actual code):
```python
def process_user(user_id: str, db: Database) -> UserResult:
    """Process user with full validation and error handling."""
    if not user_id or not isinstance(user_id, str):
        raise ValueError(f"Invalid user_id: {user_id!r}")
    
    user = db.get_user(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    
    return UserResult(
        id=user.id,
        name=user.name,
        email=user.email,
        processed_at=datetime.utcnow(),
    )
```

**Extensive output MUST include:**
- Complete function/method implementations
- Import statements
- Type annotations
- Error handling
- Docstrings
- Complete test functions

---

## Output Template (Normal Level)

```markdown
# Implementation Details: {ISSUE-ID}

## Summary
{One-paragraph overview of the change}

## Files Affected
| File | Action | Changes |
|------|--------|---------|
| path/to/file.ts | modify | Add authentication check |

## Approach
{Technical approach and rationale}

## Detailed Changes

### {file1.ts}
```typescript
// Add after line 45
function validateAuth(token: string): boolean {
    // Implementation
}
```

### {file2.ts}
```typescript
// Modify existing function
function existingFunc() {
    // New code here
}
```

## Dependencies
- Requires: {other issue or component}
- Blocks: {what this enables}

## Risks
- {Risk 1}: {mitigation}

## Test Strategy
- Unit test: {description}
- Integration: {description}

## Open Questions
- {Question if any}
```

---

## Output Template (Extensive Level)

Same as normal, PLUS:

```markdown
## Complete Implementation

### {file.ts}
```typescript
// Complete file with all changes
import { Dependency } from './dependency';

/**
 * Full implementation with docstring.
 * @param param - Description
 * @returns Description
 */
export function newFunction(param: string): Result {
    if (!param) {
        throw new ValidationError('param required');
    }
    
    // Full implementation
    const result = processParam(param);
    return result;
}
```

## Edge Cases
| Case | Expected Behavior | Code Path |
|------|-------------------|-----------|
| Empty input | Throw ValidationError | Line 10 |

## Test Cases
```typescript
describe('newFunction', () => {
    it('should process valid input', () => {
        const result = newFunction('valid');
        expect(result).toBeDefined();
    });
    
    it('should throw on empty input', () => {
        expect(() => newFunction('')).toThrow(ValidationError);
    });
});
```
```

---

## Reference File Naming

| Mode | Naming Pattern |
|------|----------------|
| Plan | `{ISSUE-ID}-impl-plan.md` |
| Extract | `{context}-impl-extract.md` |
| Propose | `{context}-impl-proposal.md` |

Location: `.agent/issues/references/`

---

## Example: Extract Mode Output

```markdown
# Implementation Details: AuthService (Extract)

## Summary
The AuthService handles user authentication via JWT tokens...

## Files Affected
| File | Purpose |
|------|---------|
| src/services/auth.ts | Core auth logic |
| src/middleware/auth.ts | Express middleware |

## Components

### AuthService Class
```typescript
class AuthService {
    constructor(private jwtSecret: string) {}
    
    validateToken(token: string): TokenPayload {
        return jwt.verify(token, this.jwtSecret);
    }
    
    generateToken(user: User): string {
        return jwt.sign({ userId: user.id }, this.jwtSecret);
    }
}
```

## Dependencies
- jsonwebtoken: JWT operations
- bcrypt: Password hashing

## Risks
- Token expiry not configurable (hardcoded 24h)
```

---

## Confidence Indicators in Output

```markdown
## Confidence Indicators

### ✅ High Confidence
- All affected files identified
- Clear API contracts
- Test strategy defined

### ⚠️ Areas of Uncertainty
- {Specific area}: {Why uncertain}
- {Another area}: {Mitigation}

### ❓ Blockers / Needs Clarification
- {Question requiring answer before implementation}
```

---

## Anti-patterns (Avoid)

| Anti-pattern | Why Bad | Better Approach |
|--------------|---------|-----------------|
| Too shallow | Doesn't help implementation | Add function signatures at minimum |
| Too verbose | Hard to navigate | Use collapsible sections, keep focused |
| No code examples | Implementation unclear | Include at least pseudo-code at normal, real code at extensive |
| Missing risks | Surprises during implementation | Always list potential issues |
| No test strategy | Quality unclear | Include test scenarios |
