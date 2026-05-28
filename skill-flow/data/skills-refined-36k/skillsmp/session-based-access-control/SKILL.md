---
name: session-based-access-control
description: Security pattern combining session authentication with authorization. Use when implementing web application security requiring both user authentication via session IDs and authorization checks for resource access. Combines Opaque token-based authentication with Authorisation pattern.
---

# Session-Based Access Control Security Pattern

Combines session-based authentication (opaque tokens) with authorization. Subject is first authenticated via session ID, then authorized based on their principal's privileges before action execution.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Requests actions with session ID |
| **Authentication Enforcer** | Enforcement Point | Verifies session ID |
| **Verifier** | Decision Point | Validates session, retrieves principal |
| **Session Manager** | Entity | Maintains open sessions |
| **Session ID Generator** | Cryptographic Primitive | Generates secure session IDs |
| **Authorisation Enforcer** | Enforcement Point | Checks action authorization |
| **Decider** | Decision Point | Makes authorization decisions |
| **Policy Provider** | Information Point | Manages access policies |

### Data Elements

- **sessionId**: Opaque token identifying session
- **principal**: Authenticated identity
- **actionId**: Identifier for requested action
- **objectId**: Identifier for target resource
- **privileges**: Permissions granted to principal

## Combined Flow

```
Subject → [action + sessionId] → Auth Enforcer
Auth Enforcer → [sessionId] → Verifier
Verifier → [get_principal] → Session Manager
Session Manager → [principal] → Verifier
Verifier → [principal] → Auth Enforcer
Auth Enforcer → [action + principal] → Authz Enforcer
Authz Enforcer → [authorise(principal, actionId, objectId)] → Decider
Decider → [get_privileges(principal)] → Policy Provider
Policy Provider → [privileges] → Decider
Decider → [allowed/denied] → Authz Enforcer
Authz Enforcer → [action] → System (if allowed)
```

### Step-by-Step

1. Subject sends request with session ID
2. Authentication Enforcer forwards session ID to Verifier
3. Verifier queries Session Manager for associated principal
4. If valid session, principal returned to Auth Enforcer
5. Auth Enforcer forwards request (with principal) to Authz Enforcer
6. Authz Enforcer extracts actionId and objectId from request
7. Decider queries Policy Provider for principal's privileges
8. Decider determines if action on object is permitted
9. If authorized, request forwarded to System

## Session Management

### Session Creation
1. Subject authenticates (e.g., password login)
2. Session Manager creates new session
3. Session ID Generator produces secure random ID
4. Session Manager stores sessionId→principal mapping
5. Session ID returned to Subject

### Session ID Requirements
- Minimum 64 bits of entropy
- Generate 128+ bits using CSPRNG
- Check for duplicates before storing

### Session Lifetime
- Idle timeout (configurable)
- Absolute maximum duration
- Invalidate on logout
- Invalidate on credential change

## Authorization Model

### Privilege Determination
- Policy Provider maintains access rules
- Common models: RBAC, ABAC, ACL
- Consider both action AND object in decisions

### Critical: Object-Level Authorization
Always verify:
- Principal can perform this action type
- Principal can access this specific object

**IDOR Prevention**: Never skip object-level checks; verify principal has access to the specific objectId.

## Security Considerations

### Authentication Layer
- All session management best practices apply
- See: Opaque token-based authentication pattern

### Authorization Layer
- Default deny: reject unless explicitly allowed
- Policy integrity: protect rules from tampering
- Complete mediation: check every request

### Separation of Concerns
- Authentication determines WHO
- Authorization determines WHAT they can do
- Both must pass for action to proceed

### Resource Protection
- Auth and Authz enforcers on critical path
- Potential DoS target—implement rate limiting
- Consider caching for performance

### Session Data Security
- If storing sensitive data in session, encrypt it
- Minimize session data exposure

## Implementation Checklist

- [ ] Secure session ID generation (128+ bits, CSPRNG)
- [ ] Session timeout policies (idle + absolute)
- [ ] New session ID on login
- [ ] Session invalidation on logout
- [ ] Authorization check on every request
- [ ] Object-level authorization (IDOR prevention)
- [ ] Default deny policy
- [ ] Policy integrity protection
- [ ] Rate limiting on enforcers

## Related Patterns

- Opaque token-based authentication (session component)
- Authorisation (access control component)
- Limit request rate (DoS protection)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/01_01_006__session_based_access_control/
- OWASP Session Management Cheat Sheet
- OWASP Authorization Cheat Sheet
