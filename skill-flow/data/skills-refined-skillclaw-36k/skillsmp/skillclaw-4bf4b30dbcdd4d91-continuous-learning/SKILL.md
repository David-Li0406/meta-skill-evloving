---
name: continuous-learning
description: Use this skill at the end of a session to extract reusable patterns, debugging insights, and project-specific knowledge for continuous improvement.
---

# Skill body

## Trigger Conditions

- At the end of a session
- When discovering new debugging techniques
- After resolving complex issues
- When creating reusable solutions
- Upon learning project-specific knowledge

## Learning Pattern Types

### 1. Error Resolution Patterns

When resolving an error, document:
- Error message
- Root cause
- Solution
- Preventive measures

```markdown
## Error: Cannot read property 'xxx' of undefined

### Scenario
Accessing nested object properties

### Root Cause
Asynchronous data not loaded before access

### Solution
```typescript
// Use optional chaining
const value = obj?.nested?.property

// Or provide a default value
const value = obj?.nested?.property ?? defaultValue
```

### Prevention
- Always use optional chaining for potentially null properties
- Add loading state checks in components
```

### 2. Debugging Techniques

```markdown
## Technique: Debugging Next.js API Routes

### Scenario
API route returns unexpected results

### Technique
1. Add logging at the start of route.ts
```typescript
export async function GET(request: NextRequest) {
  console.log('[API] GET /api/xxx', {
    url: request.url,
    headers: Object.fromEntries(request.headers)
  })
  // ...
}
```

2. Test directly using Postman/curl
3. Check if middleware is intercepting
```

### 3. Workarounds

```markdown
## Workaround: Complex Queries Not Supported by Prisma

### Scenario
Need to execute SQL not natively supported by Prisma

### Workaround
```typescript
// Use $queryRaw to execute raw SQL
const result = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE LOWER(name) LIKE ${`%${search.toLowerCase()}%`}
`

// Or use $executeRaw to execute commands
await prisma.$executeRaw`
  UPDATE users SET updated_at = NOW()
  WHERE id = ${userId}
`
```

### Note
- Manually handle SQL injection protection
- Specify return types manually
```

### 4. Project-Specific Knowledge

```markdown
## Project: User Authentication Flow

### Flow
1. User submits credentials → POST /api/auth/login
2. Validate credentials → Check database
3. Generate JWT → Set httpOnly cookie
4. Return user information

### Key Files
- `src/app/api/auth/login/route.ts` - Login endpoint
- `src/lib/auth.ts` - Authentication utility functions
- `src/middleware.ts` - Route protection

### Considerations
- Token validity period is 7 days
- Refresh token at /api/auth/refresh
- Protected routes configured in middleware.ts
```

## Evaluation Checklist

At the end of the session, check for the following:

### Patterns Worth Documenting

```markdown
- [ ] Resolved a complex bug?
- [ ] Discovered a debugging technique?
- [ ] Created a reusable code snippet?
- [ ] Learned a new usage of a framework/library?
- [ ] Encountered and resolved a performance issue?
- [ ] Found a workaround?
- [ ] Gained project-specific knowledge?
```

### Patterns Not Worth Documenting

```markdown
- [ ] Simple typos
- [ ] One-time configuration issues
- [ ] Temporary external API failures
- [ ] Known simple problems
```

## Knowledge Base Structure

```
.claude/
└── learned/
    ├── errors/
    │   ├── prisma-connection-issues.md
    │   └── react-hydration-mismatch.md
    ├── debugging/
    │   ├── next-api-routes.md
    │   └── database-query-slow.md
    ├── workarounds/
    │   ├── prisma-raw-queries.md
    │   └── nextauth-custom-session.md
    ├── patterns/
    │   ├── error-handling.md
    │   └── api-response-format.md
    └── project/
        ├── auth-flow.md
        └── data-management.md
```