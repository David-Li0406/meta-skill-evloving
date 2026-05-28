# Self-Contained Bead Description Template

Use this template for every bead description to ensure it is completely self-documenting.

---

## Task

[Clear, actionable statement of what needs to be done. Start with a verb: "Implement...", "Add...", "Create...", "Fix..."]

## Background & Reasoning

[Why this task exists. Answer these questions:
- What problem does this solve?
- How does this serve the project's overarching goals?
- Why was this approach chosen over alternatives?
- What business/user value does this deliver?

This section ensures someone reading the bead understands the "why", not just the "what".]

## Key Files

[List every file that needs to be created or modified, with clear purpose for each:]

- `src/api/auth.ts` - Add the new authentication endpoint here
- `src/middleware/jwt.ts` - Reference this for token validation patterns
- `src/types/user.ts` - Add new UserSession type definition
- `tests/auth.test.ts` - Add corresponding unit tests

## Implementation Details

[Specific technical guidance to implement this task:]

### Patterns to Follow

```typescript
// Example of the pattern to use (from existing codebase)
export async function validateToken(token: string): Promise<User> {
  // Follow this structure for the new endpoint
}
```

### API Signatures / Interfaces

```typescript
// New interface to implement
interface AuthResponse {
  token: string;
  expiresAt: number;
  user: UserInfo;
}
```

### Integration Points

- Calls `UserService.findById()` for user lookup
- Uses `JWTHelper.sign()` for token generation
- Emits `auth.login` event for analytics

### Data Flow

1. Request comes in with credentials
2. Validate against database
3. Generate JWT token
4. Return response with token and user info

## Acceptance Criteria

[Specific, testable criteria with verification commands where applicable:]

- [ ] Endpoint `POST /api/auth/login` accepts `{email, password}` and returns JWT
- [ ] Invalid credentials return 401 with error message
- [ ] Token expires after 24 hours (configurable)
- [ ] Unit tests pass: `npm test -- --grep 'auth'`
- [ ] Lint passes: `npm run lint`
- [ ] Manual verification: `curl -X POST localhost:3000/api/auth/login -d '{"email":"test@example.com","password":"test"}' -H 'Content-Type: application/json'`

## Considerations & Edge Cases

[Things that might trip up the implementer:]

### Security
- Never log passwords, even in debug mode
- Use constant-time comparison for password verification
- Rate limit login attempts (max 5 per minute per IP)

### Edge Cases
- What if user doesn't exist? Return generic "invalid credentials" (don't reveal user existence)
- What if user is deactivated? Return 403 with "account deactivated" message
- What if password is empty? Validate before hitting database

### Performance
- Database query should use index on email field
- Token generation is CPU-bound; consider caching for high load

### Backwards Compatibility
- Old clients expect `accessToken` field; include both `token` and `accessToken` in response

## Notes for Future Self

[Anything else a developer would want to know:]

- Related PR: #123 added the user model this depends on
- See RFC-001 in /docs/rfcs/ for the full authentication design
- The `expiresAt` is Unix timestamp in seconds, not milliseconds
- We chose JWT over sessions because [reason from original plan]
- TODO for v2: Add refresh token support (out of scope for this bead)

---

## Usage Notes

When filling out this template:

1. **Be specific** - Vague descriptions lead to implementation guesswork
2. **Include code snippets** - Show patterns, don't just describe them
3. **Test commands** - Give exact commands to verify completion
4. **Explain trade-offs** - Why this approach? What alternatives were rejected?
5. **Link context** - Reference related beads, PRs, or documentation
6. **Think "future self"** - What would you want to know in 6 months?

### The Self-Containment Test

Before finalizing a bead, ask:

> "If I gave this bead to a competent developer who has never seen the project, could they implement it correctly without asking questions?"

If the answer is "no" or "maybe", add more context.
