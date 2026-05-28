---
name: eridu-authentication-authorization-backend
description: Provides backend-specific authentication and authorization implementation patterns for NestJS/TypeScript servers. This skill should be used when implementing JWT validation, role-based access control, API key guards, token lifecycle management, or designing protected endpoints.
---

# Eridu Services - Backend Authentication & Authorization Skill

## Backend Responsibilities

1. **Validate incoming credentials** - Verify JWTs, API keys, session tokens
2. **Determine user context** - Extract user information from credentials
3. **Enforce authorization** - Check permissions before processing requests
4. **Handle failures gracefully** - Return proper HTTP status codes and messages
5. **Audit sensitive operations** - Log who did what and when

## Core Principles

### Always Protect Sensitive Operations

**Rule**: Require authentication for any operation that:
- Modifies user data
- Accesses user-specific resources
- Changes permissions or roles
- Accesses client/studio-specific data

### Validate on Every Request

**Rule**: Don't trust client-sent credentials or user IDs
- Validate tokens/credentials on every request
- Look up user context from authoritative source (database)
- Never assume identity without verification

### Fail Securely

**Authentication Failures** (401):
- Return 401 Unauthorized
- Don't reveal if username exists
- Don't expose password requirements in error messages

**Authorization Failures** (403):
- Return 403 Forbidden
- Log the failed attempt (for audit)
- Don't expose which permissions are missing
- Don't reveal what resources exist

### Token Security

**Best Practices**:
- ✅ Use industry-standard token formats (JWT with RS256/EdDSA)
- ✅ Include token expiration times
- ✅ Implement token refresh mechanism
- ✅ Validate token signature using public keys
- ✅ Use HTTPS/TLS for all token transmission
- ❌ Never store plaintext passwords
- ❌ Never log tokens
- ❌ Never expose token validation logic to client

## Implementation Patterns

### Public Endpoints

```typescript
// Mark endpoints that don't require authentication
// Explicitly allow unauthenticated access
// Examples: /health, /api-reference, /login
```

**Checklist**:
- [ ] Endpoint is truly non-sensitive
- [ ] No user data is returned
- [ ] No internal information exposed
- [ ] Endpoint is explicitly marked as public

### User Authentication Required

```typescript
// Require valid credentials but any authenticated user can access
// Examples: /me, /user-profile, /my-settings
```

**Checklist**:
- [ ] User context is available (from validated credentials)
- [ ] User ID is from credentials, not from client input
- [ ] Request is validated before processing
- [ ] Response only includes user's own data

### Role-Based Authorization

```typescript
// Require specific roles (admin, moderator, etc.)
// Examples: /admin, /moderation, /financial-reports
```

**Checklist**:
- [ ] Role is checked from authoritative source (database, token)
- [ ] Role is not passed as client input
- [ ] Authorization is checked before processing
- [ ] Failed authorization is logged

### Resource-Level Authorization

```typescript
// User can only access resources they own or have permission for
// Examples: edit own comment, view client-specific data, manage team
```

**Checklist**:
- [ ] Resource owner/permissions are checked
- [ ] User cannot access resources they don't own
- [ ] Resource ID is from database, not assumed from URL
- [ ] Permissions are checked before returning data

## Service-to-Service Authentication

**Purpose**: Authenticate privileged operations between services (not from end users)

**Patterns**:
- API keys for backend-to-backend communication
- Service-specific credentials for external integrations
- Separate endpoints from user-facing APIs

**Key Rules**:
- ✅ Use different credentials per service
- ✅ Use separate endpoints (`/backdoor/*`, `/google-sheets/*`)
- ✅ Store credentials in environment variables
- ✅ Rotate credentials periodically
- ❌ Never use same credentials for multiple services
- ❌ Never expose service credentials in logs
- ❌ Never accept service calls from untrusted networks (without additional validation)

## Error Handling

### Authentication Errors

```
Status: 401 Unauthorized
Body: { error: "Authentication required" }

Don't reveal:
- Whether username exists
- Password requirements
- User IDs
- Token structure
```

### Authorization Errors

```
Status: 403 Forbidden
Body: { error: "Access denied" }

Don't reveal:
- Which permissions are required
- What resources exist
- User's current permissions
- Why access was denied (be vague)
```

### Validation Errors

```
Status: 400 Bad Request
Body: { error: "Invalid request format" }

Can reveal:
- Which fields are invalid
- Format requirements
- Type mismatches
```

## Backend Implementation Checklist

**General**:
- [ ] Authentication is required for all sensitive endpoints
- [ ] Authorization is enforced server-side (never trust client)
- [ ] Unauthorized access returns proper HTTP status (401/403)
- [ ] User context is validated on each request
- [ ] Public endpoints are explicitly marked
- [ ] Failed auth/authz is logged for audit
- [ ] Error messages don't expose internal structure
- [ ] No hardcoded credentials or secrets

**Token Management**:
- [ ] Token validation uses secure methods
- [ ] Token signature is verified
- [ ] Token expiration is checked
- [ ] Token refresh is implemented
- [ ] User context is extracted from token
- [ ] Token is not exposed in logs
- [ ] Token is transmitted over HTTPS

**User Context**:
- [ ] User ID is from validated credentials, never from client input
- [ ] User permissions are fetched from authoritative source
- [ ] User context is available to all request handlers
- [ ] User context is cleared after response
- [ ] User data is not cached longer than token lifetime

**API Keys** (Service-to-Service):
- [ ] API keys are stored in environment variables
- [ ] API keys are validated on every request
- [ ] API keys are rotated periodically
- [ ] Failed API key validation is logged
- [ ] Service identity is tracked with API keys
- [ ] API key endpoints are separate from user endpoints

**Audit & Logging**:
- [ ] All authentication failures are logged
- [ ] All authorization failures are logged
- [ ] User identity is logged with each operation
- [ ] Timestamps are recorded
- [ ] Tokens are NOT logged
- [ ] Passwords are NOT logged
- [ ] Internal error details are NOT exposed to clients

## Related Skills

- **service-pattern/SKILL.md** - Services receive authenticated user context
- **controller-pattern/SKILL.md** - Controllers validate and enforce permissions
- **data-validation/SKILL.md** - Input validation (complement to auth)
- **authentication-authorization-frontend/SKILL.md** - Frontend token handling

## Documentation References

For implementation details in specific frameworks:

**NestJS/erify_api**:
- `docs/AUTHENTICATION_GUIDE.md` - JWT guards, decorators, module setup
- `docs/SERVER_TO_SERVER_AUTH.md` - API key guards configuration

**Other Backends**:
- Follow the same principles documented here
- Adjust implementation to your framework
- Always validate on server-side
