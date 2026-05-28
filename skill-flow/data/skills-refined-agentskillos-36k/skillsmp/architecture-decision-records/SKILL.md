---
name: architecture-decision-records
description: Best practices for writing Architecture Decision Records (ADRs) that document significant technical decisions with comprehensive context, examples, and rationale
---

# Architecture Decision Records (ADR) - Writing Guide

This skill provides comprehensive guidance for writing high-quality Architecture Decision Records (ADRs) for the VedaGhosham project, based on the existing 13 ADRs in `docs/architecture-decisions/`.

## What is an ADR?

An Architecture Decision Record documents a significant technical decision made during the project's development. ADRs capture:
- **What** decision was made
- **Why** it was made (problem context)
- **How** it's implemented (with code examples)
- **Trade-offs** (what was gained/lost)
- **Alternatives** considered

## When to Write an ADR

Write an ADR when making decisions that:
1. **Impact the entire system** (database choice, framework selection, deployment strategy)
2. **Are difficult to reverse** (DynamoDB single-table design, monorepo structure)
3. **Involve significant trade-offs** (tRPC vs REST, Remix vs Next.js)
4. **Set architectural patterns** (entity structure, error handling, authentication)
5. **Require future context** (why we chose this approach over alternatives)

### Examples of ADR-Worthy Decisions
- ✅ Choosing DynamoDB single-table design (ADR-004)
- ✅ Selecting tRPC over REST (ADR-005)
- ✅ Email blacklist management strategy (ADR-015)
- ✅ Fresh user data from database vs JWT (ADR-001)
- ✅ Monorepo with pnpm workspaces (ADR-009)

### Examples of Non-ADR Decisions
- ❌ Adding a new field to an entity (routine change)
- ❌ Refactoring a component (implementation detail)
- ❌ Fixing a bug (not an architectural decision)
- ❌ Updating dependencies (maintenance task)

## ADR Format and Structure

### File Naming Convention
```
docs/architecture-decisions/adr-NNN-kebab-case-title.md
```

- **NNN**: Zero-padded 3-digit number (001, 002, 015, etc.)
- **kebab-case-title**: Descriptive, lowercase, hyphen-separated
- Find the next number by checking existing ADRs

**Examples:**
- `adr-001-fresh-user-data.md`
- `adr-005-trpc-over-rest.md`
- `adr-015-email-blacklist-bounce-management.md`

### Document Structure

Every ADR follows this structure:

```markdown
# ADR-NNN: Title (Clear, Concise Description)

**Date:** YYYY-MM-DD
**Status:** Accepted | Proposed | Deprecated | Superseded
**Context:** One-line summary of when/why this decision was needed

---

## Problem

[Detailed problem description with 3-5 paragraphs]

### Option 1: [First Alternative]
[Code example or description]

**Problems:**
- List specific issues
- Technical limitations
- Business concerns

### Option 2: [Second Alternative]
[Code example or description]

**Problems:**
- List specific issues

### Option 3: [Chosen Approach]
[Code example or description]

**Benefits:**
- Why this is better
- Advantages over alternatives

---

## Decision

**Use [Chosen Approach] for [Purpose].**

[1-2 paragraph explanation of the decision]

**Why [Chosen Approach]:**
1. Reason 1
2. Reason 2
3. Reason 3

---

## Implementation

[Detailed implementation with code examples]

### 1. [First Implementation Aspect]
[Code examples with comments]

### 2. [Second Implementation Aspect]
[Code examples with comments]

[Continue for all major implementation aspects]

---

## Benefits

### 1. **[Benefit Name]**
[Explanation with code/metrics examples]

### 2. **[Benefit Name]**
[Explanation with code/metrics examples]

[Continue for all major benefits]

---

## Trade-offs

### What We Gained
- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

### What We Lost
- ❌ Limitation 1
- ❌ Limitation 2
- ❌ Limitation 3

### Why Trade-offs Are Acceptable
1. **Limitation 1**: Explanation of why it's acceptable
2. **Limitation 2**: Explanation
3. **Limitation 3**: Explanation

---

## Comparison

| Feature | Alternative 1 | Alternative 2 | Chosen Approach |
|---------|--------------|---------------|-----------------|
| **Metric 1** | Value | Value | Value |
| **Metric 2** | Value | Value | Value |

---

## Real-World Example

### Scenario: [Concrete Use Case]

**With [Alternative Approach]:**
```
[Step-by-step flow showing problems]
```

**With [Chosen Approach]:**
```
[Step-by-step flow showing benefits]
```

**Winner:** [Chosen Approach] ([quantified benefit])

---

## Future Considerations

### [Future Topic 1]
[Discussion of how this decision might evolve]

### [Future Topic 2]
[Potential extensions or modifications]

**Current Status:** [Current state and future plans]

---

## Related Files

### [Category 1]
- `path/to/file1.ts` - Description
- `path/to/file2.ts` - Description

### [Category 2]
- `path/to/file3.ts` - Description

---

## References

- **[Resource Name]**: [URL]
- **[Documentation]**: [URL]
- Related: [Cross-reference to other ADRs]
```

## Writing Guidelines

### 1. Title and Header

**Title Format:**
```markdown
# ADR-NNN: Clear, Concise Description
```

**Examples:**
- ✅ `ADR-001: Load Fresh User Data from Database (Not Stale JWT)`
- ✅ `ADR-005: tRPC Over REST API`
- ✅ `ADR-015: Email Blacklist and Bounce Management`
- ❌ `ADR-001: User Data` (too vague)
- ❌ `ADR-005: API Decision` (not descriptive)

**Header Fields:**
```markdown
**Date:** 2025-12-17 (ISO format)
**Status:** Accepted (current state)
**Context:** Brief one-liner about when/why this decision was needed
```

**Status Values:**
- `Proposed` - Under consideration
- `Accepted` - Active and implemented
- `Deprecated` - No longer recommended
- `Superseded` - Replaced by another ADR (reference ADR-XXX)

### 2. Problem Section

The Problem section should:
- **Explain the context** (3-5 paragraphs minimum)
- **Show code examples** of the problem or alternatives
- **List 2-4 alternatives** considered
- **Explain trade-offs** for each alternative

**Good Problem Description Example:**
```markdown
## Problem

VedaGhosham sends authentication OTP emails via AWS SES. Without proper bounce 
and complaint handling, we risk:

1. **Sender Reputation Damage**: Repeated bounces to invalid emails harm sender reputation
2. **Service Suspension**: AWS SES may suspend service if bounce rate exceeds 5%
3. **Wasted Resources**: Sending emails to blacklisted addresses wastes API calls and costs
4. **Poor User Experience**: Users with invalid emails get stuck in auth flow
5. **No Visibility**: No tracking of email delivery issues or spam complaints

### Without Blacklist Management

```typescript
// ❌ Sends to all emails without checking
export async function sendOTPEmail(email: string, code: string) {
  // Always sends, even if email previously bounced
  await sesClient.send(new SendEmailCommand({ ... }));
}
```

**Problems:**
- Hard bounces (permanent failures) get retried every login
- Spam complaints not tracked (user marked email as spam)
- No way to prevent sending to known-bad addresses
- AWS SES reputation degrades over time
```

**Key Points:**
- Start with business impact (reputation, cost, UX)
- Show concrete code examples
- List specific, actionable problems

### 3. Decision Section

**Format:**
```markdown
## Decision

**Use [Technology/Pattern] for [Purpose].**

[1-2 paragraph justification]

**Why [Chosen Approach]:**
1. Reason 1 (with evidence)
2. Reason 2 (with evidence)
3. Reason 3 (with evidence)
```

**Example:**
```markdown
## Decision

**Use tRPC (TypeScript Remote Procedure Call) instead of REST or GraphQL.**

tRPC provides end-to-end type safety without codegen, perfect for our TypeScript monorepo.

**Why tRPC:**
1. **Full type safety with zero codegen**: Types flow automatically through AppRouter export
2. **Automatic validation**: Zod schemas validate input before handler runs
3. **Middleware composition**: Reusable auth/permission middleware
4. **Request batching**: Reduces Lambda invocations and latency
```

### 4. Implementation Section

The Implementation section should:
- **Show working code examples** (not pseudocode)
- **Include file paths** in code comments
- **Explain key patterns** with inline comments
- **Cover all major aspects** of implementation

**Structure:**
```markdown
## Implementation

### 1. [Infrastructure/Configuration]
[SST/config code with explanations]

### 2. [Core Business Logic]
[Entity/service code]

### 3. [API Layer]
[tRPC router/endpoint code]

### 4. [Frontend Integration]
[Remix route/component code]

### 5. [Testing/Monitoring]
[Test examples, CloudWatch alarms]
```

**Code Example Standards:**
```typescript
// ✅ Good: Working code with comments
// packages/core/src/email/blacklist.ts
export async function checkEmailBlacklist(
  email: string,
): Promise<BlacklistCheckResult> {
  const normalizedEmail = normalizeEmail(email);

  try {
    const result = await User.query.byEmail({ email: normalizedEmail }).go();

    if (result.data.length > 0) {
      const user = result.data[0];

      if (user.emailBlacklisted) {
        return {
          isBlacklisted: true,
          reason: user.emailBlacklistReason || 'UNKNOWN',
          userId: user.userId,
          blacklistedAt: user.emailBlacklistedAt,
        };
      }
    }

    return { isBlacklisted: false };
  } catch (error) {
    // Database error - fail open to prevent auth system breakage
    console.error('Failed to check email blacklist, allowing send:', error);
    return { isBlacklisted: false };
  }
}

// ❌ Bad: Pseudocode without context
function checkBlacklist(email) {
  // Check if email is blacklisted
  return query(email);
}
```

### 5. Benefits Section

**Format:**
```markdown
## Benefits

### 1. **[Concrete Benefit]**
[Explanation with evidence]

**Example/Metric:**
[Code example or quantified metric]

### 2. **[Concrete Benefit]**
[Explanation with evidence]
```

**Good Benefits Example:**
```markdown
## Benefits

### 1. **Cost Efficiency**
Single table = one set of provisioned capacity. No cross-table query overhead.

**Example:**
- Multi-table: 7 tables × $5/month = **$35/month** (minimum)
- Single-table: 1 table × $5/month = **$5/month**
- **Savings: 85%** (at small scale)

### 2. **Consistent Performance**
All queries within one table (no cross-table latency). GSIs provide O(1) lookups 
for all access patterns. Single-digit millisecond latency.
```

**Key Points:**
- Use bold for benefit names
- Provide concrete evidence (metrics, code examples)
- Quantify when possible (percentages, time, cost)

### 6. Trade-offs Section

**Format:**
```markdown
## Trade-offs

### What We Gained
- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

### What We Lost
- ❌ Limitation 1
- ❌ Limitation 2
- ❌ Limitation 3

### Why Trade-offs Are Acceptable

1. **Limitation 1**: Detailed explanation of why this is acceptable
2. **Limitation 2**: Explanation with context
3. **Limitation 3**: Explanation
```

**Good Trade-offs Example:**
```markdown
## Trade-offs

### What We Gained
- ✅ Full type safety with zero codegen
- ✅ Automatic validation (Zod schemas)
- ✅ Simplified error handling (TRPCError)
- ✅ Middleware composition for auth/permissions
- ✅ Request batching (reduces Lambda invocations)
- ✅ IntelliSense for all procedures

### What We Lost
- ❌ No OpenAPI/Swagger documentation (tRPC-specific)
- ❌ Smaller ecosystem than REST (fewer tools/integrations)
- ❌ TypeScript-only (can't call from Python, Go, etc.)
- ❌ Less familiar to REST-only developers

### Why Trade-offs Are Acceptable

1. **No OpenAPI**: Internal API only (not public-facing); tRPC docs are code itself
2. **Smaller Ecosystem**: TypeScript ecosystem is sufficient for our needs
3. **TypeScript-Only**: Entire stack is TypeScript (no other languages planned)
4. **Learning Curve**: One-time cost; tRPC is simpler than REST + OpenAPI codegen
```

### 7. Comparison Section

Use tables to compare alternatives across multiple dimensions:

```markdown
## Comparison

| Feature | Alternative 1 | Alternative 2 | Chosen Approach |
|---------|--------------|---------------|-----------------|
| **Feature 1** | ❌ No | ⚠️ Partial | ✅ Yes |
| **Feature 2** | Value | Value | Value |
| **Cost** | $X/month | $Y/month | $Z/month |
| **Performance** | Metric | Metric | Metric |
```

**Symbols to Use:**
- ✅ = Advantage
- ❌ = Disadvantage
- ⚠️ = Partial/Conditional
- Use actual values when possible (numbers, percentages)

### 8. Real-World Example

Provide a concrete scenario showing the decision in action:

```markdown
## Real-World Example

### Scenario: Add "dateOfBirth" field to User

**With Polyrepo (Multi-Repository):**
```bash
# 1. Update core
cd vedaghosham-core
# Edit User entity
git commit -m "Add dateOfBirth"
npm version patch      # 1.2.0 → 1.2.1
npm publish

# 2. Update API
cd ../vedaghosham-api
npm install @vedaghosham/core@1.2.1  # Wait for npm registry propagation
# Update API code
git commit -m "Support dateOfBirth"

# 3. Update Web
cd ../vedaghosham-web
npm install @vedaghosham/core@1.2.1
# Update web code
git commit -m "Show dateOfBirth in profile"

# Total time: 30-60 minutes
```

**With Monorepo (Chosen Approach):**
```bash
# 1. Update core
cd packages/core/src/user
# Edit entity.ts and types.ts

# 2. Update functions (TypeScript error guides you!)
cd packages/functions/src/user
# Update router.ts

# 3. Update web (TypeScript error guides you!)
cd packages/web/app/routes
# Update profile route

# 4. Commit everything
git commit -m "Add dateOfBirth field"

# Total time: 5-10 minutes ✅
```

**Winner:** Monorepo (6× faster, no versioning hassle)
```

### 9. Future Considerations

Discuss how the decision might evolve:

```markdown
## Future Considerations

### Adding Public API
If we need a public API (for mobile apps, third-party integrations):
- **Option A**: Keep tRPC for internal use; add separate REST API for public
- **Option B**: Use tRPC + tRPC-OpenAPI adapter (generates OpenAPI from tRPC)

**Current Status:** Internal API only; no public API needed yet.

### Non-TypeScript Clients
If we need Python/Go clients:
- **Option A**: Create thin REST wrapper around tRPC backend
- **Option B**: Use HTTP directly (tRPC is just JSON-RPC over HTTP)

**Current Status:** Full TypeScript stack; no other languages planned.
```

### 10. Related Files

List all files implementing the decision:

```markdown
## Related Files

### Backend
- `packages/functions/src/shared/trpc.ts` - tRPC initialization
- `packages/functions/src/shared/middleware.ts` - Auth middleware
- `packages/functions/src/{entity}/router.ts` - Entity routers

### Frontend
- `packages/web/app/lib/trpc.ts` - tRPC client factory
- `packages/web/app/routes/_app.*.tsx` - Usage in Remix routes

### Schemas
- `packages/core/src/{entity}/schema.ts` - Zod schemas used by tRPC
```

### 11. References

Include all relevant resources:

```markdown
## References

- **tRPC Documentation**: https://trpc.io/
- **tRPC vs REST**: https://trpc.io/docs/concepts
- **ElectricSQL tRPC Talk**: https://www.youtube.com/watch?v=2LYM8gf184U
- **Zod Validation**: https://zod.dev/
- Related: ADR-004 (Single-Table DynamoDB)
- Related: ADR-010 (Zod Shared Validation)
```

## Code Example Standards

### 1. Use Real, Working Code
```typescript
// ✅ Good: Actual code from codebase
export async function loader({ request }: LoaderFunctionArgs) {
  await requireAuth(request);
  const trpc = await createServerClient(request);
  const user = await trpc.user.me.query();
  return json({ user });
}

// ❌ Bad: Pseudocode
export function loader() {
  // Get user
  return user;
}
```

### 2. Include File Paths
```typescript
// ✅ Good: Shows where code lives
// packages/web/app/routes/_app.tsx
export async function loader({ request }: LoaderFunctionArgs) {
  // ...
}

// ❌ Bad: No context
export async function loader() {
  // ...
}
```

### 3. Add Explanatory Comments
```typescript
// ✅ Good: Explains why
try {
  const result = await User.query.byEmail({ email: normalizedEmail }).go();
  return { isBlacklisted: false };
} catch (error) {
  // Database error - fail open to prevent auth system breakage
  console.error('Failed to check email blacklist, allowing send:', error);
  return { isBlacklisted: false };
}

// ❌ Bad: No explanation for non-obvious behavior
} catch (error) {
  return { isBlacklisted: false };
}
```

### 4. Show Before/After
```typescript
// ❌ WRONG: Checks stale JWT token
export async function loader({ request }: LoaderFunctionArgs) {
  const userData = await requireCompleteProfile(request);
  // userData.profileCompleted is STALE!
}

// ✅ CORRECT: Loads fresh data from database
export async function loader({ request }: LoaderFunctionArgs) {
  await requireAuth(request);
  const trpc = await createServerClient(request);
  const user = await trpc.user.me.query();
  // user.profileCompleted is always fresh! ✅
}
```

## Writing Style Guidelines

### 1. Be Concrete, Not Abstract
- ✅ "Single table costs $5/month vs multi-table $35/month (85% savings)"
- ❌ "Single table is cheaper"

### 2. Use Numbers and Metrics
- ✅ "3-6× faster initial load (300-500ms vs 2-3 seconds)"
- ❌ "Much faster initial load"

### 3. Show, Don't Just Tell
- ✅ Include code examples showing the problem and solution
- ❌ "The old approach had issues"

### 4. Explain Trade-offs Honestly
- ✅ "What we lost: No OpenAPI docs. Why acceptable: Internal API only"
- ❌ "Perfect solution with no downsides"

### 5. Future-Proof with Considerations
- ✅ "If we need public API: Option A vs Option B. Current status: Not needed"
- ❌ "We'll never need a public API"

## Common Pitfalls to Avoid

### ❌ Don't Write Vague ADRs
```markdown
## Decision
We decided to use a database.
```

### ❌ Don't Skip Alternatives
```markdown
## Problem
We need to store data.

## Decision
Use DynamoDB.
```
(Missing: Why not PostgreSQL? MongoDB? What were the trade-offs?)

### ❌ Don't Use Pseudocode
```typescript
function doSomething() {
  // Do the thing
}
```

### ❌ Don't Ignore Trade-offs
```markdown
## Benefits
- Fast
- Cheap
- Easy

(Missing: What did we lose? Every decision has trade-offs)
```

### ❌ Don't Skip Real Examples
```markdown
## Implementation
We implemented the feature.

(Missing: How? Show code!)
```

## Checklist for Reviewing ADRs

Before finalizing an ADR, ensure:

- [ ] **Title** is clear and descriptive (ADR-NNN format)
- [ ] **Date** is in YYYY-MM-DD format
- [ ] **Status** is set (Proposed/Accepted/Deprecated/Superseded)
- [ ] **Problem** section explains context with 3+ paragraphs
- [ ] **Alternatives** section lists 2-4 options considered
- [ ] **Decision** section has clear justification (3+ reasons)
- [ ] **Implementation** has real code examples with file paths
- [ ] **Benefits** section quantifies advantages (metrics/percentages)
- [ ] **Trade-offs** section honestly discusses limitations
- [ ] **Comparison** table compares alternatives across multiple dimensions
- [ ] **Real-World Example** shows concrete scenario
- [ ] **Future Considerations** discusses evolution/extensions
- [ ] **Related Files** lists all implementation files
- [ ] **References** includes external docs and cross-references
- [ ] Code examples use ✅/❌ to show right/wrong patterns
- [ ] Numbers and metrics used throughout (not just "better/faster")
- [ ] All code examples include comments explaining why

## ADR Template

Use this template when creating a new ADR:

```markdown
# ADR-NNN: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Context:** [One-line summary]

---

## Problem

[3-5 paragraph problem description]

### Option 1: [First Alternative]
[Code/description]

**Problems:**
- Issue 1
- Issue 2

### Option 2: [Second Alternative]
[Code/description]

**Problems:**
- Issue 1
- Issue 2

---

## Decision

**Use [Chosen Approach] for [Purpose].**

[1-2 paragraph justification]

**Why [Chosen Approach]:**
1. Reason 1
2. Reason 2
3. Reason 3

---

## Implementation

### 1. [Implementation Aspect 1]
[Code examples]

### 2. [Implementation Aspect 2]
[Code examples]

---

## Benefits

### 1. **[Benefit Name]**
[Explanation with evidence]

### 2. **[Benefit Name]**
[Explanation with evidence]

---

## Trade-offs

### What We Gained
- ✅ Benefit 1
- ✅ Benefit 2

### What We Lost
- ❌ Limitation 1
- ❌ Limitation 2

### Why Trade-offs Are Acceptable
1. **Limitation 1**: Explanation
2. **Limitation 2**: Explanation

---

## Comparison

| Feature | Alternative 1 | Alternative 2 | Chosen |
|---------|--------------|---------------|--------|
| **Feature 1** | Value | Value | Value |

---

## Real-World Example

### Scenario: [Use Case]

**With [Alternative]:**
[Step-by-step flow]

**With [Chosen Approach]:**
[Step-by-step flow]

**Winner:** [Chosen] ([quantified benefit])

---

## Future Considerations

### [Topic 1]
[Discussion]

**Current Status:** [State]

---

## Related Files

### [Category 1]
- `path/to/file.ts` - Description

---

## References

- **[Resource]**: [URL]
- Related: ADR-XXX
```

## Example: Simplified ADR

Here's a simplified example showing the key elements:

```markdown
# ADR-016: Rate Limiting for API Endpoints

**Date:** 2025-12-20
**Status:** Proposed
**Context:** Protecting API from abuse and ensuring fair usage

---

## Problem

VedaGhosham's tRPC API is publicly accessible (after authentication). Without 
rate limiting, we risk:

1. **DoS Attacks**: Malicious users could overwhelm Lambda functions
2. **Cost Spikes**: Unlimited requests = unlimited AWS costs
3. **Poor UX**: One user's heavy usage slows down others
4. **No Abuse Protection**: No mechanism to block bad actors

### Option 1: No Rate Limiting
```typescript
// No protection - anyone can spam requests
export const userRouter = router({
  list: protectedProcedure.query(async () => {
    return await User.scan.go(); // Expensive query, no limits
  }),
});
```

**Problems:**
- No protection against abuse
- AWS costs unbounded
- Poor experience for legitimate users

### Option 2: Lambda Concurrency Limits
Set reserved concurrency on Lambda functions.

**Problems:**
- All-or-nothing (affects all users equally)
- No per-user fairness
- Hard to configure correctly

### Option 3: DynamoDB-Based Rate Limiting
Track request counts per user in DynamoDB with TTL.

**Benefits:**
- Per-user fairness
- Serverless (no Redis needed)
- Fine-grained control

---

## Decision

**Use DynamoDB-based rate limiting with per-user counters and TTL.**

We'll create a RateLimit entity tracking requests per user per time window.

**Why DynamoDB Rate Limiting:**
1. **Serverless**: No Redis/Memcached infrastructure needed
2. **Per-User Fairness**: Each user has independent limit
3. **Automatic Cleanup**: DynamoDB TTL removes old records
4. **Fine-Grained**: Can set limits per endpoint or globally

---

## Implementation

### 1. RateLimit Entity

```typescript
// packages/core/src/rate-limit/entity.ts
export const RateLimit = new Entity({
  model: {
    entity: 'RateLimit',
    version: '1',
    service: 'vedaghosham',
  },
  attributes: {
    userId: { type: 'string', required: true },
    endpoint: { type: 'string', required: true },
    windowStart: { type: 'number', required: true }, // Unix timestamp
    requestCount: { type: 'number', required: true, default: 0 },
    ttl: { type: 'number' }, // DynamoDB TTL (auto-delete after 1 hour)
  },
  indexes: {
    primary: {
      pk: { field: 'pk', composite: ['userId', 'endpoint'] },
      sk: { field: 'sk', composite: ['windowStart'] },
    },
  },
}, configuration);
```

### 2. Rate Limiting Middleware

```typescript
// packages/functions/src/shared/rate-limit.ts
const RATE_LIMITS = {
  'user.list': { requests: 100, windowMs: 60000 }, // 100 req/min
  'course.create': { requests: 10, windowMs: 60000 }, // 10 req/min
  default: { requests: 1000, windowMs: 60000 }, // 1000 req/min
};

export const rateLimitMiddleware = t.middleware(async ({ ctx, path, next }) => {
  const userId = ctx.user?.userId;
  if (!userId) return next(); // Skip for unauthenticated

  const limit = RATE_LIMITS[path] || RATE_LIMITS.default;
  const windowStart = Math.floor(Date.now() / limit.windowMs) * limit.windowMs;

  // Check current count
  const result = await RateLimit.get({
    userId,
    endpoint: path,
    windowStart,
  }).go();

  if (result.data && result.data.requestCount >= limit.requests) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: `Rate limit exceeded. Try again in ${limit.windowMs / 1000}s`,
    });
  }

  // Increment counter
  await RateLimit.upsert({
    userId,
    endpoint: path,
    windowStart,
    requestCount: (result.data?.requestCount || 0) + 1,
    ttl: Math.floor(Date.now() / 1000) + 3600, // Expire after 1 hour
  }).go();

  return next();
});
```

### 3. Apply to Procedures

```typescript
// packages/functions/src/shared/procedures.ts
export const protectedProcedure = t.procedure
  .use(isAuthenticated)
  .use(rateLimitMiddleware);
```

---

## Benefits

### 1. **Cost Protection**
Rate limiting prevents runaway costs from abuse.

**Example:**
- Without limit: Malicious user makes 1M requests = $200+ Lambda cost
- With limit: Blocked at 1,000 requests = $0.20 maximum cost per user
- **Savings: 99.9%** in abuse scenario

### 2. **Fair Resource Allocation**
Each user has independent quota (one user can't starve others).

### 3. **No Additional Infrastructure**
Uses existing DynamoDB table (no Redis/Memcached needed).

---

## Trade-offs

### What We Gained
- ✅ Protection from abuse and DoS
- ✅ Cost predictability
- ✅ Per-user fairness
- ✅ Serverless (no Redis)

### What We Lost
- ❌ DynamoDB write costs (1 write per request)
- ❌ Slight latency increase (~10ms per request)
- ❌ Complexity (middleware + entity)

### Why Trade-offs Are Acceptable

1. **DynamoDB Writes**: ~$0.001 per 1,000 requests (negligible vs abuse cost)
2. **Latency**: 10ms overhead acceptable for cost/abuse protection
3. **Complexity**: Essential for production API

---

## Comparison

| Feature | No Limit | Lambda Limits | DynamoDB Limit |
|---------|----------|---------------|----------------|
| **Cost Protection** | ❌ No | ⚠️ Global | ✅ Per-user |
| **Fairness** | ❌ No | ❌ No | ✅ Yes |
| **Infrastructure** | ✅ None | ✅ None | ✅ Existing DB |
| **Granularity** | N/A | ❌ Coarse | ✅ Fine-grained |

---

## Real-World Example

### Scenario: User spams "list all courses" endpoint

**Without Rate Limiting:**
```
User makes 10,000 requests in 1 minute
→ 10,000 Lambda invocations × $0.0000002 = $2.00
→ 10,000 DynamoDB scans × $0.00025 = $2.50
→ Total cost: $4.50 per abuse incident
→ API slow for all users
```

**With Rate Limiting (100 req/min):**
```
User makes 10,000 requests in 1 minute
→ First 100 succeed
→ Next 9,900 blocked with 429 error
→ Cost: 100 requests = $0.045
→ Other users unaffected
```

**Winner:** Rate limiting (99% cost reduction, better UX)

---

## Future Considerations

### Distributed Rate Limiting
If we need multi-region:
- Use DynamoDB Global Tables for consistent limits across regions

**Current Status:** Single region sufficient.

### Redis Alternative
If DynamoDB becomes too expensive:
- Switch to ElastiCache Redis (faster, lower per-request cost)

**Current Status:** DynamoDB cost acceptable (<$1/month).

---

## Related Files

### Core
- `packages/core/src/rate-limit/entity.ts` - RateLimit entity

### Functions
- `packages/functions/src/shared/rate-limit.ts` - Middleware
- `packages/functions/src/shared/procedures.ts` - Applied to procedures

### Infrastructure
- `infra/database.ts` - DynamoDB table (already has TTL enabled)

---

## References

- **DynamoDB TTL**: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
- **Rate Limiting Patterns**: https://aws.amazon.com/blogs/architecture/rate-limiting-strategies-for-serverless-applications/
- **tRPC Middleware**: https://trpc.io/docs/server/middlewares
- Related: ADR-004 (Single-Table DynamoDB)
- Related: ADR-005 (tRPC Over REST)
```

---

## Summary

High-quality ADRs in VedaGhosham:
1. **Document significant decisions** (not routine changes)
2. **Show alternatives considered** (2-4 options with trade-offs)
3. **Provide working code examples** (real code from codebase)
4. **Quantify benefits** (metrics, percentages, cost savings)
5. **Explain trade-offs honestly** (what we lost and why it's acceptable)
6. **Include comparison tables** (features across alternatives)
7. **Show real-world scenarios** (concrete before/after examples)
8. **Discuss future evolution** (how decision might change)
9. **List all related files** (where implementation lives)
10. **Reference external docs** (AWS docs, library docs, related ADRs)

Use the ADR template and checklist to ensure comprehensive, maintainable architecture documentation that will serve the project for years to come.
