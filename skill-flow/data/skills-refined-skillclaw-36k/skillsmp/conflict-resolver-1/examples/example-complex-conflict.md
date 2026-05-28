# Example: Complex Merge Conflict (Escalate to User)

## Scenario
Two tasks modified the same function with incompatible logic changes.

## Conflict Detected

```bash
$ git merge auto/task-3
CONFLICT (content): Merge conflict in src/utils/auth.ts
```

## Conflict Content

```typescript
// src/utils/auth.ts
export async function validateToken(token: string) {
<<<<<<< HEAD
  // Task-2: Added rate limiting
  if (await isRateLimited(token)) {
    throw new RateLimitError('Too many requests');
  }

  const decoded = jwt.verify(token, SECRET);
  return decoded;
=======
  // Task-3: Added token refresh
  const decoded = jwt.verify(token, SECRET);

  if (isExpiringSoon(decoded)) {
    const newToken = await refreshToken(decoded);
    return { ...decoded, refreshedToken: newToken };
  }

  return decoded;
>>>>>>> auto/task-3
}
```

## Resolution Analysis

**Type: Semantic (logic conflict)**

Both changes are valid but interact in non-obvious ways:
- Task-2 adds rate limiting BEFORE validation
- Task-3 adds token refresh AFTER validation

Combining them requires understanding:
1. Should rate limiting apply before or after refresh check?
2. Does refreshed token need separate rate limit?

## Escalation Decision

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ Conflict Requires User Decision                         │
│                                                             │
│   File: src/utils/auth.ts                                   │
│   Function: validateToken                                   │
│   Type: Semantic conflict                                   │
│                                                             │
│   Task-2 changes:                                           │
│     + Rate limiting before validation                       │
│                                                             │
│   Task-3 changes:                                           │
│     + Token refresh after validation                        │
│                                                             │
│   Cannot auto-resolve because:                              │
│     - Both modify core logic                                │
│     - Order of operations matters                           │
│     - Business logic decision required                      │
│                                                             │
│   Options:                                                  │
│   A) Rate limit → Validate → Refresh                        │
│   B) Validate → Rate limit → Refresh                        │
│   C) Keep only Task-2 changes                               │
│   D) Keep only Task-3 changes                               │
└─────────────────────────────────────────────────────────────┘
```

## User Response

User selected: **Option A - Rate limit → Validate → Refresh**

## Resolution

```typescript
// src/utils/auth.ts (resolved)
export async function validateToken(token: string) {
  // Rate limiting first (from task-2)
  if (await isRateLimited(token)) {
    throw new RateLimitError('Too many requests');
  }

  // Validation
  const decoded = jwt.verify(token, SECRET);

  // Token refresh if needed (from task-3)
  if (isExpiringSoon(decoded)) {
    const newToken = await refreshToken(decoded);
    return { ...decoded, refreshedToken: newToken };
  }

  return decoded;
}
```

## Output

```
┌─────────────────────────────────────────────────────────────┐
│ Conflict Resolution (User-Assisted)                         │
│                                                             │
│   Resolution: Option A selected                             │
│   Order: Rate limit → Validate → Refresh                    │
│                                                             │
│   Combined logic:                                           │
│     1. Check rate limit (task-2)                            │
│     2. Verify JWT                                           │
│     3. Refresh if expiring soon (task-3)                    │
│                                                             │
│   Status: ✅ Resolved with user input                       │
└─────────────────────────────────────────────────────────────┘
```
