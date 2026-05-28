---
name: code-reviewer
description: "Expert code review for Java/Spring Boot and TypeScript/Next.js codebases. Performs multi-dimensional reviews covering correctness, security, testability, architecture, and maintainability. Automatically delegates to specialized skills when detecting: security vulnerabilities → security-expert, auth/Keycloak → keycloak-skill, Java test quality → java-test-engineer, TypeScript/React test quality → ts-test-engineer, architecture issues → architecture-tech-lead, frontend patterns → frontend-design-skill. Use for PR reviews, code audits, pre-merge checks, or general code quality assessment."
---

# Code Reviewer Skill

Expert code review with automatic delegation to specialized skills based on detected concerns.

## Review Dimensions

Every review covers these dimensions, with automatic skill delegation:

| Dimension | Checks | Delegates To |
|-----------|--------|--------------|
| **Correctness** | Logic errors, edge cases, null handling | - |
| **Security** | OWASP Top 10, injection, auth flaws | `security-expert` |
| **Auth/Keycloak** | JWT handling, ABAC, realm config | `keycloak-skill` |
| **Testability (Java)** | JUnit, jqwik, mocking | `java-test-engineer` |
| **Testability (TS/React)** | Vitest, RTL, Playwright | `ts-test-engineer` |
| **Architecture** | Coupling, SRP, functional core | `architecture-tech-lead` |
| **Frontend** | Component patterns, a11y, performance | `frontend-design-skill` |
| **Performance** | N+1 queries, caching, complexity | - |
| **Maintainability** | Naming, complexity, documentation | - |

## Review Process

### 1. Triage Phase
Scan code to identify which dimensions need deep review:

```
□ Security-sensitive code? (auth, crypto, input handling)
□ Keycloak/OAuth2 integration?
□ New/modified tests or testability concerns?
□ Architectural changes or coupling issues?
□ Frontend components?
□ Performance-critical paths?
```

### 2. Deep Review Phase
For each flagged dimension, apply specialized review criteria.

### 3. Synthesis Phase
Consolidate findings into actionable feedback.

---

## Quick Review Checklists

### Java/Spring Boot

**Correctness**
- [ ] Null checks via Optional or @NonNull
- [ ] Exception handling is specific, not catch-all
- [ ] Stream operations handle empty collections
- [ ] BigDecimal for money, not double
- [ ] Thread safety in shared state

**Spring Patterns**
- [ ] Constructor injection, not @Autowired fields
- [ ] @Transactional at correct scope
- [ ] No business logic in controllers
- [ ] DTOs for API boundaries
- [ ] Validation via Bean Validation annotations

**Security (→ security-expert for deep dive)**
- [ ] No SQL string concatenation
- [ ] Input validation before processing
- [ ] Secrets not in code/logs
- [ ] @PreAuthorize or @AbacPolicy on sensitive endpoints
- [ ] Rate limiting on auth endpoints

**Database**
- [ ] N+1 query prevention (join fetch, @EntityGraph)
- [ ] Pagination for large result sets
- [ ] Proper indexing for query patterns
- [ ] Transaction boundaries appropriate

### TypeScript/Next.js

**Correctness**
- [ ] Strict null checks respected
- [ ] Error boundaries in place
- [ ] Async/await error handling
- [ ] Type narrowing, not type casting

**React Patterns**
- [ ] Server vs Client components correct
- [ ] useMemo/useCallback where needed (not everywhere)
- [ ] Key props on lists
- [ ] No state for derived values
- [ ] Effects have proper dependencies

**Frontend (→ frontend-design-skill for deep dive)**
- [ ] Semantic HTML
- [ ] Keyboard navigation works
- [ ] Loading/error states
- [ ] Mobile responsive

---

## Severity Levels

```
🔴 CRITICAL - Must fix before merge
   Security vulnerabilities, data loss risk, crashes

🟠 HIGH - Strong recommendation to fix
   Logic bugs, performance issues, maintainability debt

🟡 MEDIUM - Should fix, can discuss
   Code quality, missed optimizations, naming

🔵 LOW - Suggestion/nitpick
   Style preferences, minor improvements

💚 PRAISE - Call out good patterns
   Reinforce excellent code worth emulating
```

---

## Delegation Triggers

### → security-expert

Invoke when detecting:
- Authentication/authorization logic
- Cryptographic operations
- Input validation at trust boundaries
- Session/token management
- CORS/CSP configuration
- Secrets handling

### → keycloak-skill

Invoke when detecting:
- JWT parsing/validation
- @AbacPolicy annotations
- UMA token exchange
- Realm/client configuration
- Identity provider integration
- Role/group mapping

### → java-test-engineer

Invoke when detecting (Java/Spring):
- JUnit/jqwik test files
- Untested Java business logic
- Complex conditionals needing property tests
- Mock-heavy tests that could be simplified
- Spring integration test patterns

### → ts-test-engineer

Invoke when detecting (TypeScript/React - Vite/Next.js):
- Vitest/Jest test files
- Untested TypeScript/React code
- React component test issues
- Vite or Next.js specific testing patterns
- MSW API mocking patterns
- Playwright E2E tests

### → architecture-tech-lead

Invoke when detecting:
- Service with 5+ dependencies
- Business logic mixed with I/O
- Circular dependencies
- God classes (500+ lines)
- Tight coupling between modules

### → frontend-design-skill

Invoke when detecting:
- React component files
- CSS/styling changes
- Layout/UX patterns
- Animation implementations
- Design system components

---

## Review Output Format

### For PR Reviews

```markdown
## Code Review Summary

**Files reviewed**: N files, M lines changed
**Risk level**: 🔴/🟠/🟡/🔵
**Blocking issues**: N

### Critical Issues 🔴
- [file:line] Issue description
  **Fix**: Recommended solution

### High Priority 🟠
- ...

### Suggestions 🟡
- ...

### Praise 💚
- Good use of X pattern in file.ts

### Specialist Reviews Needed
- [ ] Security review recommended for auth changes
- [ ] Architecture review for new service design
```

### For Code Audit

```markdown
## Audit Report: [Component/Service Name]

### Executive Summary
Overall health: Good/Fair/Needs Attention
Key risks: ...

### Findings by Category

#### Security
- ...

#### Architecture
- ...

#### Testing
- ...

### Recommendations
1. Immediate: ...
2. Short-term: ...
3. Long-term: ...
```

---

## Anti-Pattern Detection

### Java

```java
// ❌ Catch-all exception
catch (Exception e) { log.error("Error", e); }

// ❌ Field injection
@Autowired private Service service;

// ❌ Business logic in controller
@GetMapping public Response get() {
    if (condition) { /* 50 lines of logic */ }
}

// ❌ N+1 query
users.stream().map(u -> u.getOrders()).collect(toList());

// ❌ Mutable shared state
private List<String> cache = new ArrayList<>();
```

### TypeScript

```typescript
// ❌ Type assertion instead of narrowing
const user = data as User;

// ❌ useEffect with missing dependencies
useEffect(() => { fetchData(id) }, []);

// ❌ State for derived values
const [fullName, setFullName] = useState(first + last);

// ❌ Inline object causing re-renders
<Component style={{ margin: 10 }} />

// ❌ Any type
function process(data: any) { ... }
```

---

## Reference Files

- **[references/java-patterns.md](references/java-patterns.md)**: Common Java/Spring anti-patterns with fixes
- **[references/typescript-patterns.md](references/typescript-patterns.md)**: TypeScript/React review patterns
- **[references/review-workflow.md](references/review-workflow.md)**: Detailed review workflow and communication

---

## Communication Style

**Be direct and constructive:**
- State the issue clearly
- Explain why it matters
- Suggest a specific fix
- Link to documentation if helpful

**Avoid:**
- Vague criticism ("this could be better")
- Condescending tone
- Nitpicking style choices unless impactful
- Blocking on non-issues

**Examples:**

```
❌ "This is wrong"
✅ "This catches all exceptions, masking bugs. Catch specific exceptions instead."

❌ "Consider maybe using Optional here?"
✅ "Use Optional.ofNullable() to prevent NPE when user is null."

❌ "I would do this differently"
✅ "Extract this validation into a pure function for easier unit testing."
```

---

## Checklist Before Approving

```
□ No critical or high-priority issues remain
□ Security-sensitive changes have specialist review
□ Tests exist for new logic
□ No obvious performance regressions
□ Code is understandable without author's explanation
□ Changes match PR description
```
