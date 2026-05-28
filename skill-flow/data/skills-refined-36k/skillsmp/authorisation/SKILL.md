---
name: authorisation
description: Security pattern for implementing access control and authorization. Use when designing permission systems, implementing RBAC/ABAC, preventing unauthorized access, addressing privilege escalation, or ensuring users can only perform allowed actions on permitted resources. Addresses "Entity performs disallowed action" problem.
---

# Authorisation Security Pattern

Ensures entities can only perform actions they are permitted to perform on resources they are permitted to access. Prevents privilege escalation and unauthorized access.

## Problem Addressed

**Entity performs disallowed action**: An unprivileged user performs actions reserved for administrators, accesses other users' data, or manipulates resources beyond their permissions.

Examples:
- User changes another customer's account details
- Unprivileged entity performs admin operations
- Attacker accesses internal documents by guessing identifiers

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Requests actions on resources |
| **System** | Entity | Manages protected resources |
| **Enforcer** | Enforcement Point | Intercepts requests, enforces decisions |
| **Decider** | Decision Point | Makes allow/deny decisions |
| **Policy Provider** | Information Point | Manages access control rules |

### Data Elements

- **action**: Operation Subject wants to perform
- **principal**: Authenticated identity of Subject
- **actionId**: Identifier for the action type
- **objectId**: Identifier for the target resource
- **privileges**: Permissions granted to principal

## Authorisation Flow

```
Subject → [action(principal)] → Enforcer
Enforcer → [authorise(principal, actionId, objectId)] → Decider
Decider → [get_privileges(principal)] → Policy Provider
Policy Provider → [privileges] → Decider
Decider → [allowed/denied] → Enforcer
Enforcer → [action] → System (if allowed)
        → [error] → Subject (if denied)
```

1. Subject (with established principal) requests action
2. Enforcer intercepts and extracts actionId, objectId
3. Decider queries Policy Provider for privileges
4. Decider evaluates request against privileges
5. If allowed: forward to System
6. If denied: return error to Subject

## Critical Considerations

### Authorise After Authentication
- Enforcer must only process authenticated requests
- Principal must be established before authorization
- Combine with Authentication pattern

### Default Deny
- Deny all requests unless explicitly allowed
- Policy should grant permissions, not revoke them
- Missing rule = denied

### Object-Level Authorization (IDOR Prevention)
**Critical**: Always check both:
1. Can principal perform this ACTION type?
2. Can principal access this specific OBJECT?

Failing to check objectId leads to Insecure Direct Object Reference (IDOR) vulnerabilities.

### Complete Mediation
- Check EVERY request
- No bypass paths
- Enforcer must be unavoidable

### Policy Integrity
- Protect policy from unauthorized modification
- Policy changes = security-sensitive operations
- Audit policy modifications

### Resource Concerns
- Enforcer/Decider on every request path
- Potential performance bottleneck
- Potential DoS target
- Consider caching, rate limiting

## Authorization Models

### Role-Based Access Control (RBAC)
```
Principal → Roles → Permissions
```
- Assign roles to users
- Assign permissions to roles
- Check if principal's roles include required permission

### Attribute-Based Access Control (ABAC)
```
if (subject.dept == resource.dept AND
    subject.clearance >= resource.classification)
    then allow
```
- Evaluate attributes of subject, resource, environment
- Flexible policy expressions

### Access Control Lists (ACL)
```
Resource → [allowed principals/operations]
```
- Per-resource permission lists
- Direct mapping of who can do what

## Implementation Checklist

- [ ] Authentication precedes authorization
- [ ] Default deny policy
- [ ] Action-level authorization check
- [ ] Object-level authorization check (IDOR prevention)
- [ ] Enforcer cannot be bypassed
- [ ] Policy protected from tampering
- [ ] Policy changes audited
- [ ] Consistent error messages (no information leakage)
- [ ] Rate limiting on authorization endpoints

## Error Handling

Return consistent errors:
- Don't reveal whether resource exists
- Don't reveal why authorization failed specifically
- Log details server-side, return generic errors to client

## Related Patterns

- Authentication (establishes principal)
- Session-based access control (combines both)
- Log entity actions (audit trail)
- Limit request rate (DoS protection)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/
- OWASP Authorization Cheat Sheet
- OWASP IDOR Prevention
