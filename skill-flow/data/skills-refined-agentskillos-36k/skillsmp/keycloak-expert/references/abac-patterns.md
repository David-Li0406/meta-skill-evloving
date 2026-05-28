# ABAC Patterns Reference

## Table of Contents
1. [ABAC vs RBAC Decision Guide](#abac-vs-rbac-decision-guide)
2. [UMA Protocol Deep Dive](#uma-protocol-deep-dive)
   - [Keycloak UMA Caveats](#keycloak-uma-caveats)
   - [UMA 2.0 Flow](#uma-20-flow)
3. [Policy Patterns](#policy-patterns)
4. [JavaScript Policy Examples](#javascript-policy-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## ABAC vs RBAC Decision Guide

### When to Use RBAC
| Scenario | Reason |
|----------|--------|
| Simple role hierarchy | Clear mapping: admin > manager > user |
| Static permissions | Permissions don't change based on context |
| Small number of roles | <10 distinct roles |
| Audit simplicity needed | Easy to answer "who has access to X?" |
| Coarse-grained access | Page/module level access control |

### When to Use ABAC
| Scenario | Reason |
|----------|--------|
| Context-dependent access | Time, location, device matters |
| Resource-level attributes | Access depends on data properties |
| Complex business rules | Multiple conditions combined |
| Dynamic policies | Rules change without code deployment |
| Fine-grained control | Field/action level access |
| Avoiding role explosion | Too many role combinations |

### Hybrid Approach (Recommended)
```
RBAC for coarse-grained → Is user authenticated with valid role?
ABAC for fine-grained → Can this user perform this action on this resource?
```

```java
// RBAC: Spring Security handles this
.requestMatchers("/admin/**").hasRole("ADMIN")

// ABAC: Keycloak handles this
@AbacPolicy(resource = "document", action = "edit")
public void editDocument(Document doc) {
    // Only reached if user has permission for THIS document
}
```

## UMA Protocol Deep Dive

### Keycloak UMA Caveats

**Important**: Keycloak's UMA implementation deviates from the UMA 2.0 specification in several ways:

| Aspect | UMA 2.0 Spec | Keycloak Implementation |
|--------|--------------|------------------------|
| Resource ownership | End-user owns resources | Resource server owns resources |
| Permission management | User grants permissions | Policies configured in admin console |
| Claims gathering | Interactive claim collection | Static policy evaluation |
| Requesting party | Can be different from resource owner | Typically the authenticated user |

**Implications**:
- Resources are registered by the client (resource server), not end-users
- Users cannot dynamically share resources with other users via UMA
- Permission tickets are optional - direct token exchange is common
- External UMA documentation may not apply directly to Keycloak

**When Keycloak UMA works well**:
- Centralized policy management by administrators
- Application-defined resources with role/attribute-based access
- Backend services validating permissions

**When to consider alternatives**:
- User-to-user resource sharing (consider custom implementation)
- Dynamic permission delegation (consider OAuth scopes)

### UMA 2.0 Flow

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│  Client  │                │ Keycloak │                │ Resource │
│(Frontend)│                │   (AS)   │                │  Server  │
└────┬─────┘                └────┬─────┘                └────┬─────┘
     │                           │                           │
     │ 1. Access Token (JWT)     │                           │
     ├───────────────────────────────────────────────────────>
     │                           │                           │
     │                           │     2. 401 + permission   │
     │<───────────────────────────────────────────────────────
     │                           │        ticket             │
     │                           │                           │
     │ 3. Request RPT            │                           │
     │   (access_token +         │                           │
     │    permission ticket)     │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │   4. Evaluate policies    │                           │
     │                           │                           │
     │ 5. RPT (if permitted)     │                           │
     │<──────────────────────────│                           │
     │                           │                           │
     │ 6. Retry with RPT         │                           │
     ├───────────────────────────────────────────────────────>
     │                           │                           │
     │ 7. Resource (if valid)    │                           │
     │<───────────────────────────────────────────────────────
```

### Simplified Flow (Direct Token Exchange)

For backend services, skip the ticket dance:

```bash
# Single call to get RPT with permission
curl -X POST "${KEYCLOAK_URL}/realms/${REALM}/protocol/openid-connect/token" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  -d "audience=${CLIENT_ID}" \
  -d "permission=${RESOURCE}#${SCOPE}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}"
```

### Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 + `access_token` | Permission granted | Proceed with operation |
| 403 | Permission denied | Return AccessDeniedException |
| 400 | Invalid request | Check resource/scope names |
| 401 | Token invalid | Re-authenticate |

### RPT Token Structure

```json
{
  "authorization": {
    "permissions": [
      {
        "rsid": "resource-uuid",
        "rsname": "mailtemplate",
        "scopes": ["view"]
      }
    ]
  },
  // ... standard JWT claims
}
```

## Policy Patterns

### 1. Role-Based Policy
```java
.createPolicy("admin-only")
    .requireRoles("admin")
    .and()
```

**Keycloak JSON:**
```json
{
  "name": "admin-only",
  "type": "role",
  "logic": "POSITIVE",
  "roles": [{"id": "admin-role-uuid", "required": true}]
}
```

### 2. Time-Based Policy
```java
.createPolicy("business-hours")
    .duringBusinessHours()  // 09:00-17:00 Mon-Fri
    .and()
```

**JavaScript equivalent:**
```javascript
var context = $evaluation.getContext();
var time = new Date();
var hour = time.getHours();
var day = time.getDay();

if (hour >= 9 && hour < 17 && day >= 1 && day <= 5) {
    $evaluation.grant();
}
```

### 3. Group-Based Policy
```java
.createPolicy("premium-users")
    .requireGroups("/users/premium", "/users/enterprise")
    .and()
```

### 4. Aggregate Policy (AND logic)
```java
.createPolicy("admin-during-business-hours")
    .combining("admin-only", "business-hours")
    .withStrategy(DecisionStrategy.UNANIMOUS)  // All must pass
    .and()
```

### 5. Aggregate Policy (OR logic)
```java
.createPolicy("admin-or-owner")
    .combining("admin-only", "owner-only")
    .withStrategy(DecisionStrategy.AFFIRMATIVE)  // Any can pass
    .and()
```

### 6. Resource Owner Policy
```java
.createPolicy("owner-only")
    .withJavaScript("""
        var identity = $evaluation.getContext().getIdentity();
        var resource = $evaluation.getPermission().getResource();
        
        if (resource.getOwner() === identity.getId()) {
            $evaluation.grant();
        }
    """)
    .and()
```

## JavaScript Policy Examples

### Access Evaluation Context

```javascript
// Available objects in JavaScript policies:
var context = $evaluation.getContext();
var identity = context.getIdentity();
var permission = $evaluation.getPermission();
var resource = permission.getResource();
var realm = $evaluation.getRealm();

// Identity methods
identity.getId();              // User UUID
identity.getAttributes();      // User attributes map

// Resource methods
resource.getName();            // Resource name
resource.getType();            // Resource type URN
resource.getOwner();           // Owner user ID
resource.getAttributes();      // Resource attributes

// Permission methods
permission.getScopes();        // Requested scopes
```

### Department-Based Access

```javascript
var identity = $evaluation.getContext().getIdentity();
var resource = $evaluation.getPermission().getResource();

var userDept = identity.getAttributes().getValue('department').asString(0);
var resourceDept = resource.getAttribute('department');

if (resourceDept && resourceDept[0] === userDept) {
    $evaluation.grant();
}
```

### Clearance Level Policy

```javascript
var identity = $evaluation.getContext().getIdentity();
var resource = $evaluation.getPermission().getResource();

var userClearance = parseInt(
    identity.getAttributes().getValue('clearance_level').asString(0) || '0'
);
var requiredClearance = parseInt(
    resource.getAttribute('classification')[0] || '0'
);

if (userClearance >= requiredClearance) {
    $evaluation.grant();
}
```

### IP-Based Restriction

```javascript
var context = $evaluation.getContext();
var clientIp = context.getAttributes().getValue('kc.client.network.ip_address');

if (clientIp) {
    var ip = clientIp.asString(0);
    // Allow internal network only
    if (ip.startsWith('10.') || ip.startsWith('192.168.')) {
        $evaluation.grant();
    }
}
```

### Combined Conditions

```javascript
var identity = $evaluation.getContext().getIdentity();
var time = new Date();
var hour = time.getHours();

// Check role
var roles = identity.getAttributes().getValue('roles');
var isAdmin = roles && roles.asStringList().contains('admin');

// Check time
var isBusinessHours = hour >= 9 && hour < 17;

// Admin: anytime, Others: business hours only
if (isAdmin || isBusinessHours) {
    $evaluation.grant();
}
```

## Best Practices

### 1. Resource Naming
```
✓ urn:myapp:resources:document
✓ urn:myapp:resources:user-profile
✓ urn:myapp:resources:api:v1:orders

✗ document (too generic)
✗ my-resource (not descriptive)
```

### 2. Scope Naming
```
Standard scopes:
- view (read access)
- edit (modify access)
- delete (remove access)
- create (create new)
- admin (full control)

Custom scopes:
- approve (workflow approval)
- export (data export)
- share (sharing capability)
```

### 3. Policy Organization
```
policies/
├── role-based/
│   ├── admin-policy
│   ├── editor-policy
│   └── viewer-policy
├── time-based/
│   ├── business-hours
│   └── after-hours-admin
├── context-based/
│   ├── owner-only
│   └── same-department
└── aggregates/
    ├── admin-anytime
    └── editor-business-hours
```

### 4. Permission Granularity

**Too Coarse:**
```java
// One permission for everything
.createPermission("all-access")
    .onResource("Default Resource")  // Matches /*
    .withPolicies("authenticated")
```

**Too Fine:**
```java
// Permission per endpoint - maintenance nightmare
.createPermission("get-users")
.createPermission("post-users")
.createPermission("get-users-id")
// ... hundreds more
```

**Just Right:**
```java
// Resource-level with scope granularity
.createPermission("user-management-view")
    .onResource("users")
    .withScopes("view")
    .withPolicies("authenticated")
    
.createPermission("user-management-admin")
    .onResource("users")
    .withScopes("create", "edit", "delete")
    .withPolicies("admin-policy")
```

### 5. Caching Strategy

```java
@Cacheable(
    value = "policyCache",
    key = "#authentication.name + ':' + #resource + ':' + #action",
    unless = "#result instanceof Error"
)
public PolicyResult evaluatePolicy(...) {
    // Cache successful and forbidden results
    // Don't cache errors (transient failures)
}
```

## Troubleshooting

### Enable Debug Logging

```yaml
# application.yml
logging:
  level:
    org.keycloak: DEBUG
    org.springframework.security: DEBUG
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 on valid user | Policy not matching | Check policy logic, verify attributes |
| 400 bad request | Invalid resource/scope | Verify names match exactly |
| Token missing permissions | Wrong audience | Check `audience` param in UMA request |
| Slow policy evaluation | No caching | Implement caching with proper keys |
| Intermittent failures | Network issues | Add retry with backoff |

### Testing Policies in Keycloak Admin

1. Navigate to: Clients → [client] → Authorization → Evaluate
2. Select a user
3. Add resource and scope
4. Click "Evaluate"
5. View detailed policy evaluation results

### UMA Test Script

```bash
#!/bin/bash
KEYCLOAK_URL="https://keycloak.example.com"
REALM="toolbox"
CLIENT_ID="toolbox-webui"
CLIENT_SECRET="your-secret"

# Get access token
TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/$REALM/protocol/openid-connect/token" \
  -d "grant_type=password" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "username=testuser" \
  -d "password=testpass" \
  | jq -r '.access_token')

# Test permission
curl -X POST "$KEYCLOAK_URL/realms/$REALM/protocol/openid-connect/token" \
  -H "Authorization: Bearer $TOKEN" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  -d "audience=$CLIENT_ID" \
  -d "permission=mailtemplate#view" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -w "\nHTTP Status: %{http_code}\n"
```
