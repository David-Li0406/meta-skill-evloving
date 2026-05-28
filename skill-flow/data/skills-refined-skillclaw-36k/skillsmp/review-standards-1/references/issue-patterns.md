# Issue Patterns Reference

47 distinct issue patterns for code review, ordered by frequency. Each pattern includes detection criteria, examples, and fixes. Frequency percentages are informative guidance based on common PR feedback.

## Severity Tiers

Issues are categorized into two tiers that affect priority ranking:

**Tier 1 - Correctness** (Always Higher Priority)
Issues affecting whether code works correctly:
- Security vulnerabilities
- Architecture problems
- Implementation bugs
- Type safety violations
- Functionality gaps

**Tier 2 - Cleanliness** (Lower Priority)
Issues affecting maintainability but not correctness:
- Naming clarity
- File organization
- Code duplication (when not causing bugs)
- Comment quality
- Import/style consistency

At the same P-level, Tier 1 issues should be addressed before Tier 2 issues.

---

## High Frequency Patterns (10%+ of feedback)

### BETTER_IMPLEMENTATION_APPROACH
**Frequency:** ~18% | **Tier:** 1 (Correctness)

**Detection:** Implementing without exploring existing patterns. Complex solutions when simple ones exist. Not leveraging framework features.

**Examples:**
```typescript
// Custom timing with Date.now() when Stopwatch utility exists
const start = Date.now();
// ... work
const elapsed = Date.now() - start;

// Manual JSON parsing when framework handles it
const data = JSON.parse(JSON.stringify(response));

// Custom retry logic when HTTP client has built-in retries
for (let i = 0; i < 3; i++) {
  try { await fetch(url); break; }
  catch { await sleep(1000); }
}
```

**Fix:** Before implementing, search for:
1. Similar functionality in the codebase
2. Framework/library features that handle it
3. Simpler approaches that achieve the same result

---

### TYPE_SAFETY_IMPROVEMENT
**Frequency:** ~12% | **Tier:** 1 (Correctness)

**Detection:** Incomplete type definitions. Using `any`. Type guards that don't validate properties. Nullable fields that should be required.

**Examples:**
```typescript
// Incomplete type guard
typeof x === 'object'  // null is also 'object'!

// Using any
function process(data: any) { ... }

// Optional fields always present after initialization
interface User {
  name?: string;  // Actually required after login
}
```

**Fix:**
- Complete type definitions covering all fields
- Type guards that validate specific properties
- Non-nullable types when values are guaranteed
- Generated types over manual definitions

---

### EXISTING_UTILITY_AVAILABLE
**Frequency:** ~10% | **Tier:** 2 (Cleanliness)

**Detection:** Implementing common functionality without searching for existing utilities.

**Common utility types that often exist:**
- Error message extraction
- Fire-and-forget promise handling
- Parallel execution with concurrency limits
- Precise timing/stopwatch utilities
- String formatting helpers

**Fix:** Always search codebase before implementing common patterns.

---

### CODE_DUPLICATION
**Frequency:** ~8% | **Tier:** 2 (Cleanliness)

**Detection:** Similar functionality in multiple places. Mappings/utilities that exist elsewhere. Copy-paste implementations.

**Examples:**
```ruby
# Creating status display mapping when one exists
STATUS_MAP = { pending: "Pending", done: "Done" }

# Duplicating schema definitions
class OrderSchema  # same as existing InvoiceSchema
```

**Fix:**
- Search for existing implementations first
- Extract repeated patterns into shared utilities
- Share schemas between related features

---

### NULL_HANDLING
**Frequency:** ~6% | **Tier:** 1 (Correctness)

**Detection:** Empty strings as fallbacks. Optional fields that should be required. Default values masking absence.

**Examples:**
```typescript
// Empty string hides absence
const name = user.name ?? "";

// Zero masks missing value
const count = data.count ?? 0;  // when zero is valid

// Optional when always present
interface Config {
  apiKey?: string;  // Actually required
}
```

**Fix:** Use `null` to represent absence. Handle nullable values explicitly.

---

### ADD_COMMENT_EXPLANATION
**Frequency:** ~6% | **Tier:** 2 (Cleanliness)

**Detection:** Unusual patterns without explanation. Hardcoded values. Non-obvious inheritance. Workarounds.

**Examples:**
```typescript
// Using 'as never' without explaining exhaustive check
return assertNever(action);

// Magic numbers without context
const timeout = 120000;

// Workaround without explanation
obj.__proto__ = null;
```

**Fix:** Add comments explaining "why", not "what".

---

## Medium Frequency Patterns (5-10%)

### NAMING_CLARITY
**Frequency:** ~5.5% | **Tier:** 2 (Cleanliness)

**Detection:** Names conflicting with domain terms. Abbreviations in APIs. Inconsistent terminology.

**Examples:**
```typescript
// 'config' when "Config" is a domain concept
const config = { ... };  // Conflicts with Config entity

// Inconsistent terminology
user.state vs user.status  // Pick one

// Abbreviations in public API
getUserAcct()  // Use getAccount
```

**Fix:** Avoid domain-specific terms for unrelated concepts. Use full words in APIs.

---

### FILE_ORGANIZATION
**Frequency:** ~5% | **Tier:** 2 (Cleanliness)

**Detection:** Barrel files. Code in wrong directories. Utils files instead of domain placement.

**Examples:**
```typescript
// Barrel file (index.ts re-exports)
export { UserService } from './user-service';
export { AuthService } from './auth-service';

// Auth code moved out of auth module
// utils/auth-helpers.ts  // Should be auth/helpers.ts

// Generic utils file
// utils.py with unrelated functions
```

**Fix:** No barrel files. Code lives near its domain context.

---

### REDUNDANT_LOGIC
**Frequency:** ~5% | **Tier:** 2 (Cleanliness)

**Detection:** Checks that constraints already enforce. Constants in return types. Async without await. Duplicate validation.

**Examples:**
```typescript
// Null check when column has NOT NULL constraint
if (user.email != null) { ... }  // DB guarantees non-null

// Including type field that's always the same
return items.filter(i => i.type === 'order')
  .map(i => ({ type: i.type, ...rest }));  // type is always 'order'

// Async but never awaiting
async function getData() {
  return cachedValue;  // No await needed
}
```

**Fix:** Understand what's enforced by schemas, database, upstream validation.

---

### UNNECESSARY_CAST
**Frequency:** ~5% | **Tier:** 1 (Correctness)

**Detection:** `as` assertions to access properties. Bypassing TypeScript. Casting already-typed values.

**Examples:**
```typescript
// Casting to access properties
const id = (value as SomeType).property;

// Casting to avoid fixing types
const data = response as unknown as ExpectedType;

// Already typed value cast again
const user: User = data as User;  // data is already typed
```

**Fix:** Never cast to access properties. Fix underlying types. Use runtime validation.

---

### ARCHITECTURAL_CONCERN
**Frequency:** ~5% | **Tier:** 1 (Correctness)

**Detection:** Adding use-case-specific fields to shared infrastructure. Rigid abstractions. Missing extensibility.

**Examples:**
```typescript
// Feature-specific fields in generic notification context
interface NotificationContext {
  userId: string;
  agentId: string;  // Only used by agents feature
}

// Service that immediately needs customization
class EmailService {
  send() { /* One-size-fits-all */ }
}
```

**Fix:** Keep shared infrastructure generic. Design for extensibility.

---

### ERROR_HANDLING_NEEDED
**Frequency:** ~4% | **Tier:** 1 (Correctness)

**Detection:** Missing fallbacks for external services. Silently caught errors. Undefined limit behavior.

**Examples:**
```typescript
// Catching and logging instead of throwing
try {
  await externalApi.call();
} catch (e) {
  console.error(e);  // Caller doesn't know it failed
}

// No graceful degradation
const result = await thirdPartyService.fetch();  // What if it fails?

// Limits without defined behavior
if (items.length > MAX_ITEMS) { /* ??? */ }
```

**Fix:** Let errors propagate. Implement graceful degradation. Define limit behavior.

---

## Medium-Low Frequency Patterns (2-5%)

### REMOVE_UNUSED_CODE
**Frequency:** ~4% | **Tier:** 2 (Cleanliness)

**Detection:** Fields added "for the future". Code unnecessary after refactoring. Unused interface properties.

**Fix:** Only add fields/code with immediate use. Remove what becomes unnecessary.

---

### CONSOLIDATE_LOGIC
**Frequency:** ~4% | **Tier:** 2 (Cleanliness)

**Detection:** Split conditionals. Separate classes that could be methods. Overlapping indexes.

**Fix:** Review control flow for consolidation. Question if new classes are needed.

---

### NIT_MINOR_ISSUE
**Frequency:** ~4% | **Tier:** 2 (Cleanliness)

**Detection:** Style inconsistencies. Minor naming issues. Non-idiomatic code.

**Fix:** Follow existing patterns in the codebase.

---

### NAMING_CONVENTION
**Frequency:** ~3% | **Tier:** 2 (Cleanliness)

**Detection:** Wrong casing. Non-idiomatic names. Abbreviations.

**Fix:** Python uses snake_case. JavaScript/TypeScript uses camelCase. Avoid abbreviations. Follow conventions.

---

### TESTING_VERIFICATION
**Frequency:** ~3% | **Tier:** 1 (Correctness)

**Detection:** Tests not matching names. Missing test updates. Unverified queries.

**Fix:** Test names describe what's tested. Update tests with implementation. EXPLAIN ANALYZE queries.

---

### EXTRACT_TO_HELPER
**Frequency:** ~3% | **Tier:** 2 (Cleanliness)

**Detection:** Same authorization pattern copied. Repeated filtering. Useful inline types.

**Fix:** Extract patterns that will be reused. Shared type utilities.

---

### CONFIGURATION_VERIFICATION
**Frequency:** ~3% | **Tier:** 1 (Correctness)

**Detection:** Missing config updates. Terraform conflicts. Wrong retention periods.

**Fix:** Update all related configs. Verify values make sense.

---

### USE_CONSTANT
**Frequency:** ~3% | **Tier:** 2 (Cleanliness)

**Detection:** Hardcoded durations. Magic strings. Environment-specific URLs hardcoded. Hardcoded fallback values.

**Examples:**
```typescript
// Hardcoded duration
setTimeout(fn, 120000);

// Hardcoded fallback
const locale = userLocale ?? "en";

// Magic string
if (status === "pending_review") { ... }
```

**Fix:** Extract hardcoded strings to named constants. Use `DEFAULT_*` or `FALLBACK_*` naming.

---

### WRONG_LOCATION
**Frequency:** ~3% | **Tier:** 2 (Cleanliness)

**Detection:** Timing in wrong lifecycle. Tests at wrong layer. Config in service classes.

**Fix:** Tests at appropriate level. Config in config. Domain logic in domain modules.

---

### DATABASE_INDEX_MISSING
**Frequency:** ~2.5% | **Tier:** 1 (Correctness)

**Detection:** Queries filtering columns without indexes. Changed query columns.

**Fix:** Verify indexes exist. EXPLAIN ANALYZE before deploying.

---

### PERFORMANCE_OPTIMIZATION
**Frequency:** ~2.5% | **Tier:** 1 (Correctness)

**Detection:** Over-fetching across parallel queries. Memory loading for streaming. Re-validating data.

**Fix:** Calculate actual needs. Stream large data. Skip validation for already-validated data.

---

### FUNCTION_SIGNATURE_REFACTOR
**Frequency:** ~2% | **Tier:** 2 (Cleanliness)

**Detection:** Many parameters. Same-typed parameters that could be swapped.

**Fix:** Single args object for 4+ parameters.

---

### SCOPE_REDUCTION
**Frequency:** ~2% | **Tier:** 2 (Cleanliness)

**Detection:** Including too much. Generated files not ignored.

**Fix:** Filter to only what's needed.

---

### SCOPE_CREEP
**Frequency:** ~2% | **Tier:** 2 (Cleanliness)

**Detection:** Unrelated changes in feature PRs. Mixed concerns.

**Fix:** Keep PRs focused. Separate concerns into separate PRs.

---

### FRAGILE_IMPLEMENTATION
**Frequency:** ~2% | **Tier:** 1 (Correctness)

**Detection:** Relying on `__str__`. Using `getattr` with defaults. Non-deterministic LLM instructions.

**Fix:** Explicit property access. Code-side deterministic logic.

---

### RUNTIME_VALIDATION
**Frequency:** ~2% | **Tier:** 1 (Correctness)

**Detection:** Missing runtime checks at boundaries. Trusting external data.

**Fix:** Validate at system boundaries.

---

### REMOVE_DEBUG_CODE
**Frequency:** ~2% | **Tier:** 2 (Cleanliness)

**Detection:** Print statements. Console.log. Test infrastructure in production code.

**Fix:** Remove before PR. Use proper logging.

---

### IMPORT_STYLE_CONSISTENCY
**Frequency:** ~2% | **Tier:** 2 (Cleanliness)

**Detection:** Dynamic imports in tests. Mixed relative/absolute. Different packages for same thing.

**Fix:** Follow established patterns. Use absolute imports.

---

## Lower Frequency Patterns (<2%)

### DATABASE_QUERY_OPTIMIZATION
**Frequency:** ~1.5% | **Tier:** 1 (Correctness)

Regex vs ILIKE. Missing indexed columns. Raw SQL vs query builder.

---

### PARALLELIZATION_OPPORTUNITY
**Frequency:** ~1.5% | **Tier:** 1 (Correctness)

Sequential independent queries. Sequential API calls that could be parallel.

---

### MAGIC_NUMBER
**Frequency:** ~1.5% | **Tier:** 2 (Cleanliness)

Unexplained numeric constants. Array slices without context.

---

### ERROR_MESSAGE_CLARITY
**Frequency:** ~1.5% | **Tier:** 1 (Correctness)

Status codes without response text. Missing operation context.

---

### AI_GENERATED_CODE_CONCERN
**Frequency:** ~1.5% | **Tier:** 2 (Cleanliness)

Unnecessary reorganization. Non-standard comments. Unusual patterns.

---

### REMOVE_COMMENT
**Frequency:** ~1.5% | **Tier:** 2 (Cleanliness)

Unnecessary comments. Commented-out code.

---

### BREAKING_CHANGE_CONCERN
**Frequency:** ~1% | **Tier:** 1 (Correctness)

Frontend-breaking API changes. Schema changes without migration.

---

### SECURITY_PERMISSIONS
**Frequency:** ~1% | **Tier:** 1 (Correctness)

Too permissive authorization. Unsanitized HTML. Logging PII.

---

### LIMIT_BOUNDARY_CONCERN
**Frequency:** ~1% | **Tier:** 1 (Correctness)

Undefined behavior at limits. Missing rate limiting.

---

### SCHEMA_VALIDATION_MISSING
**Frequency:** ~1% | **Tier:** 1 (Correctness)

Missing `required`. Missing `additionalProperties: false`.

---

### ENVIRONMENT_CONFIGURATION
**Frequency:** ~1% | **Tier:** 1 (Correctness)

Wrong defaults. Missing environment awareness.

---

### TYPE_CHOICE_QUESTION
**Frequency:** ~1% | **Tier:** 2 (Cleanliness)

Why Mapping vs dict? Why this cast?

---

### VERIFY_DOCUMENTATION_ACCURACY
**Frequency:** ~1% | **Tier:** 2 (Cleanliness)

Outdated references. Wrong links.

---

### RATE_LIMITING_NEEDED
**Frequency:** <1% | **Tier:** 1 (Correctness)

Expensive endpoints without limits.

---

### REVERT_UNRELATED_CHANGES
**Frequency:** <1% | **Tier:** 2 (Cleanliness)

Changes outside PR scope.

---

### RECENT_CHANGE_CONFUSION
**Frequency:** <1% | **Tier:** 1 (Correctness)

Contradicting recent changes.

---

## Security-Specific Patterns (Always P1)

### INJECTION_VULNERABILITY
**Tier:** 1 (Correctness) | **Severity:** Always P1

SQL injection, command injection, LDAP injection. Any unsanitized user input in queries or commands.

---

### AUTHENTICATION_BYPASS
**Tier:** 1 (Correctness) | **Severity:** Always P1

Weak token generation, session not invalidated, missing auth checks.

---

### AUTHORIZATION_BYPASS
**Tier:** 1 (Correctness) | **Severity:** Always P1

Missing ownership checks, IDOR vulnerabilities, permission escalation.

---

### SENSITIVE_DATA_EXPOSURE
**Tier:** 1 (Correctness) | **Severity:** P1/P2

Logging passwords, exposing internal IDs, credentials in code.

---

### XSS_VULNERABILITY
**Tier:** 1 (Correctness) | **Severity:** Always P1

Unescaped user input in HTML, innerHTML with user data.

---

## Quick Reference

**Top 5 by frequency:**
1. BETTER_IMPLEMENTATION_APPROACH (18%) - Search first, leverage framework features
2. TYPE_SAFETY_IMPROVEMENT (12%) - No casting, complete type guards
3. EXISTING_UTILITY_AVAILABLE (10%) - Search codebase before implementing
4. CODE_DUPLICATION (8%) - Check for existing implementations
5. NULL_HANDLING (6%) - Use null, not empty strings

**Always P1 (Critical):**
- Any injection vulnerability
- Authentication/authorization bypass
- XSS in user content
- Security boundary violations
