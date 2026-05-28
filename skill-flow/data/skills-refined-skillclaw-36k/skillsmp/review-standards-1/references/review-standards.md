# Review Standards

Language-agnostic best practices for code quality. These are standards that reviewers consistently enforce.

## Type System Standards

### No Type Casting for Property Access
**Rule:** Never use `as` type assertions to access properties or bypass the type checker.

**Why:** Casting is lying to the compiler. It hides bugs that surface at runtime.

**Instead:**
- Fix the underlying type definitions
- Use type guards with property validation
- Use `satisfies` for validation while keeping broader types
- Add runtime validation at system boundaries

```typescript
// BAD
const value = (response as SomeType).property;

// GOOD - type guard
function isSomeType(x: unknown): x is SomeType {
  return typeof x === 'object' && x !== null && 'property' in x;
}
if (isSomeType(response)) {
  const value = response.property;
}
```

### Complete Type Guards
**Rule:** Type guards must validate all properties that will be accessed on the narrowed type.

**Why:** `typeof x === 'object'` doesn't guarantee property existence.

```typescript
// BAD - only checks it's an object
function isUser(x: unknown): x is User {
  return typeof x === 'object' && x !== null;
}

// GOOD - validates properties without casting
function isUser(x: unknown): x is User {
  if (typeof x !== 'object' || x === null) return false;
  if (!('id' in x) || typeof x.id !== 'string') return false;
  if (!('email' in x) || typeof x.email !== 'string') return false;
  return true;
}
```

### Generated Types Preferred
**Rule:** Use generated types over manual definitions when available.

**Why:** Single source of truth. Manual types drift from reality.

### Non-Nullable When Guaranteed
**Rule:** Fields should be non-nullable when they're guaranteed to exist by the time code runs.

**Why:** Optional types create unnecessary null checks and edge cases.

### Type Hints Required (Python)
**Rule:** Type hints are mandatory in Python code.

**Why:** Consistency and IDE support. Use `dict` instead of `any` for unknown structures.

---

## Null Handling Standards

### Null Represents Absence
**Rule:** Use `null` to represent absence, never empty strings or zeros.

**Why:** `""` and `0` create edge cases. They're valid values that get confused with "missing".

```typescript
// BAD - empty string hides absence
const name = user.name ?? "";

// GOOD - null clearly indicates absence
const name = user.name ?? null;
// Or handle nullable properly
if (user.name) {
  // use user.name
}
```

### No Default Fallbacks for Absence
**Rule:** Don't use default values that mask the absence of data.

**Why:** If something doesn't exist, it should be treated as nullable, not given a fake value.

---

## Error Handling Standards

### Services Throw, Callers Decide
**Rule:** Services throw errors; callers decide how to handle them.

**Why:** Services don't know the caller's context. Let errors propagate.

```typescript
// BAD - service swallows errors
async function publishMessage(message: Message) {
  try {
    await queue.send(message);
  } catch (error) {
    logger.error('Failed to publish', error);
    // Silently fails - caller doesn't know
  }
}

// GOOD - service throws, caller handles
async function publishMessage(message: Message) {
  await queue.send(message);  // Let it throw
}

// Caller decides
await ignoreRejection(publishMessage(message));
// OR
try {
  await publishMessage(message);
} catch (error) {
  // Handle based on caller's context
}
```

### Error Messages Include Context
**Rule:** Error messages must include all relevant context for debugging.

**Why:** "Request failed with status 400" is useless. Include response body, operation details, identifiers.

```typescript
// BAD
throw new Error(`Request failed with status ${response.status}`);

// GOOD
throw new Error(
  `Failed to fetch user ${userId}: ${response.status} - ${await response.text()}`
);
```

### Graceful Degradation for External Services
**Rule:** External service integrations need graceful degradation.

**Why:** External services fail. Plan for it.

---

## Code Organization Standards

### No Barrel Files
**Rule:** No barrel files (index.ts re-exports). Import directly from source files.

**Why:** Barrel files cause circular dependencies and make imports harder to trace.

```typescript
// BAD
import { UserService, AuthService } from './services';

// GOOD
import { UserService } from './services/user-service';
import { AuthService } from './services/auth-service';
```

### Code Near Domain
**Rule:** Code lives near its domain context. No generic `utils` files.

**Why:** Easier to find, easier to understand context.

```
// BAD - generic utils file
// src/utils/auth-helpers.ts

// GOOD - in auth module
// src/auth/helpers.ts
```

### Single Args Object
**Rule:** Functions with 4+ parameters use a single args object.

**Why:** Prevents accidentally swapping same-typed arguments. Named parameters are self-documenting.

```typescript
// BAD - easy to swap projectId and agentId
function getAgent(projectId: string, agentId: string, userId: string, includeHistory: boolean)

// GOOD
function getAgent(args: {
  projectId: string;
  agentId: string;
  userId: string;
  includeHistory: boolean;
})
```

### Tests at Service Layer
**Rule:** Business logic tests belong at the service layer, not routes/controllers.

**Why:** Routes should be thin. Test the business logic directly.

---

## Naming Standards

### Avoid Domain Term Collision
**Rule:** Don't use domain-specific terms for unrelated concepts.

**Why:** If "Agent" or "Config" means something specific in your domain, don't reuse it casually.

### No Abbreviations in APIs
**Rule:** Avoid abbreviations in public APIs.

**Why:** Clarity over brevity in interfaces.

### Consistent Terminology
**Rule:** Use consistent terminology. Don't mix "state" and "status" for the same concept.

**Why:** Reduces cognitive load and bugs from misunderstanding.

### Language-Specific Casing
- Python: snake_case for variables, functions, methods
- JavaScript/TypeScript: camelCase for variables, functions, PascalCase for classes
- Ruby: snake_case for methods, PascalCase for classes
- Follow the conventions of your codebase

---

## Database Standards

### Verify Indexes Exist
**Rule:** Verify indexes exist for all WHERE clause columns before adding queries.

**Why:** Missing indexes cause performance issues at scale.

```sql
-- Before adding a query that filters by email
-- Run: EXPLAIN ANALYZE SELECT ... WHERE email = '...'
-- Check index usage
```

### Query Builder Over Raw SQL
**Rule:** Use query builders (Kysely, SQLAlchemy, ActiveRecord) over raw SQL.

**Why:** Type safety. Raw SQL bypasses type checks.

### Consolidate Overlapping Indexes
**Rule:** Review existing indexes before creating new ones. Drop redundant indexes.

**Why:** Indexes have maintenance cost. Overlapping indexes waste resources.

---

## Schema Standards

### Strict Schemas by Default
**Rule:** JSON schemas must include `required` array and `additionalProperties: false`.

**Why:** Strict by default catches invalid data early.

```json
{
  "type": "object",
  "required": ["name", "email"],
  "additionalProperties": false,
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" }
  }
}
```

---

## Comment Standards

### Comments Explain Why
**Rule:** Comments explain "why", not "what". Code should be self-describing.

**Why:** "What" comments become outdated. "Why" comments provide context code can't.

```typescript
// BAD - describes what (obvious from code)
// Increment counter by 1
counter++;

// GOOD - explains why
// Offset by 1 because the API uses 1-based indexing
counter++;
```

### Explain Unusual Patterns
**Rule:** Unusual patterns require explanation comments.

**Why:** Future readers need to know why you did something unexpected.

Examples requiring comments:
- Using `as never` for exhaustive checks
- Hardcoded values with non-obvious rationale
- Workarounds for library bugs
- Performance optimizations that sacrifice readability

---

## PR Hygiene Standards

### Remove Debug Code
**Rule:** Remove all debug code (print, console.log) before PR submission.

**Why:** Debug code in production is noise.

### Focused PRs
**Rule:** PRs focus on a single concern. Separate unrelated changes into separate PRs.

**Why:** Easier to review, easier to rollback, clearer git history.

### No AI Artifacts
**Rule:** Review AI-generated code for unnecessary changes, diff noise, and unusual patterns.

**Why:** AI tools often reorganize code or add unnecessary comments.

### Diff Only Intentional
**Rule:** The diff should only contain intentional modifications.

**Why:** Reordering, reformatting, or "cleanup" of unrelated code obscures real changes.

---

## Configuration Standards

### Named Constants for Durations
**Rule:** Use named constants for time durations and magic values.

**Why:** `120000` is unclear. `TWO_MINUTES_MS` is self-documenting.

```typescript
// BAD
setTimeout(fn, 120000);

// GOOD
const TWO_MINUTES_MS = 2 * 60 * 1000;
setTimeout(fn, TWO_MINUTES_MS);
```

### Fallback Values as Constants
**Rule:** Hardcoded fallback values in nullish coalescing (`??`) should be extracted to named constants.

**Why:** Fallback values are often reused. Named constants make them discoverable.

```typescript
// BAD - hardcoded fallback
const language = userLanguage ?? "en";

// GOOD - named constant
const DEFAULT_LANGUAGE = "en";
const language = userLanguage ?? DEFAULT_LANGUAGE;
```

### Rate Limit Keys Include Tenant
**Rule:** Rate limit keys must include tenant identifiers.

**Why:** Isolation between tenants.

### Document Config Rationale
**Rule:** Document the rationale for non-obvious configuration values.

**Why:** Future maintainers need to know why limits/timeouts have specific values.

---

## Security Standards (Always P1)

### Parameterized Queries Only
Never interpolate user input into queries. Use parameterized queries or query builders.

### Validate at Boundaries
All external input must be validated before use. Trust nothing from outside.

### No Secrets in Code
API keys, passwords, and secrets belong in environment variables, not source code.

### Log Safely
Never log passwords, tokens, or PII. Sanitize sensitive data before logging.

### Authorization on Every Endpoint
Every data-modifying endpoint must verify the user has permission to perform the action.
