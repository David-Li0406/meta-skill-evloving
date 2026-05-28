# Authorization Patterns Reference

## Table of Contents
1. [RBAC (Role-Based Access Control)](#rbac)
2. [ABAC (Attribute-Based Access Control)](#abac)
3. [ReBAC (Relationship-Based Access Control)](#rebac)
4. [Policy Engines](#policy-engines)
5. [Implementation Examples](#implementation-examples)

## RBAC

### Concept
Users → Roles → Permissions

### When to Use
- Well-defined job functions
- Stable permission requirements
- Audit/compliance requirements
- Simple access patterns

### Implementation Pattern
```java
// Define roles
public enum Role {
    USER,
    EDITOR,
    ADMIN
}

// Define permissions
public enum Permission {
    READ_DOCUMENT,
    WRITE_DOCUMENT,
    DELETE_DOCUMENT,
    MANAGE_USERS
}

// Role-permission mapping
Map<Role, Set<Permission>> rolePermissions = Map.of(
    Role.USER, Set.of(READ_DOCUMENT),
    Role.EDITOR, Set.of(READ_DOCUMENT, WRITE_DOCUMENT),
    Role.ADMIN, Set.of(READ_DOCUMENT, WRITE_DOCUMENT, DELETE_DOCUMENT, MANAGE_USERS)
);

// Check access
public boolean hasPermission(User user, Permission permission) {
    return user.getRoles().stream()
        .flatMap(role -> rolePermissions.get(role).stream())
        .anyMatch(p -> p == permission);
}
```

### Hierarchical RBAC
```java
// Role hierarchy in Spring Security
@Bean
public RoleHierarchy roleHierarchy() {
    RoleHierarchyImpl hierarchy = new RoleHierarchyImpl();
    hierarchy.setHierarchy("""
        ROLE_ADMIN > ROLE_MANAGER
        ROLE_MANAGER > ROLE_USER
        ROLE_USER > ROLE_GUEST
        """);
    return hierarchy;
}
```

## ABAC

### Concept
Access = f(Subject attributes, Resource attributes, Action, Environment)

### When to Use
- Context-dependent decisions (time, location, device)
- Resource-level attributes matter
- Complex business rules
- Dynamic policies

### XACML-Style Policy Structure
```
Policy:
  Target: resource.type == "document"
  Rules:
    - Effect: Permit
      Condition: 
        subject.department == resource.department AND
        action == "read"
    - Effect: Permit
      Condition:
        subject.clearance >= resource.classification AND
        action in ["read", "write"]
    - Effect: Deny (default)
```

### Implementation Pattern
```java
public interface PolicyDecisionPoint {
    AuthorizationDecision evaluate(AuthorizationContext context);
}

@Data
public class AuthorizationContext {
    private Subject subject;      // Who: user attributes
    private Resource resource;    // What: resource attributes
    private String action;        // How: read, write, delete
    private Environment environment;  // When/Where: time, IP, device
}

@Component
public class DocumentAccessPDP implements PolicyDecisionPoint {
    
    @Override
    public AuthorizationDecision evaluate(AuthorizationContext ctx) {
        // Rule 1: Same department can read
        if ("read".equals(ctx.getAction()) && 
            ctx.getSubject().getDepartment().equals(ctx.getResource().getDepartment())) {
            return AuthorizationDecision.PERMIT;
        }
        
        // Rule 2: Clearance-based access
        if (ctx.getSubject().getClearanceLevel() >= ctx.getResource().getClassification()) {
            return AuthorizationDecision.PERMIT;
        }
        
        // Rule 3: Time-based restriction
        LocalTime now = LocalTime.now();
        if (now.isBefore(LocalTime.of(9, 0)) || now.isAfter(LocalTime.of(18, 0))) {
            if (ctx.getResource().isConfidential()) {
                return AuthorizationDecision.DENY;
            }
        }
        
        return AuthorizationDecision.DENY;
    }
}
```

### Spring Security Integration
```java
@Component
public class AbacPermissionEvaluator implements PermissionEvaluator {
    
    private final PolicyDecisionPoint pdp;
    
    @Override
    public boolean hasPermission(Authentication auth, Object target, Object permission) {
        AuthorizationContext ctx = AuthorizationContext.builder()
            .subject(extractSubject(auth))
            .resource(extractResource(target))
            .action(permission.toString())
            .environment(Environment.current())
            .build();
        
        return pdp.evaluate(ctx) == AuthorizationDecision.PERMIT;
    }
}

// Usage
@PreAuthorize("hasPermission(#document, 'write')")
public void updateDocument(Document document) { }
```

## ReBAC

### Concept
Access based on relationships between entities (like Google Zanzibar/SpiceDB)

### When to Use
- Social/collaborative applications
- Complex ownership hierarchies
- Shared resources
- Organization structures

### Relationship Model
```
// Tuples: (object, relation, subject)
document:report#owner@user:alice
document:report#viewer@team:engineering#member
folder:projects#parent@document:report
team:engineering#member@user:bob
```

### Permission Derivation
```
// Define relations and permissions
type document {
    relation owner: user
    relation viewer: user | team#member
    relation parent: folder
    
    permission read = viewer + owner + parent->read
    permission write = owner
    permission delete = owner
}

type folder {
    relation owner: user
    relation viewer: user | team#member
    
    permission read = viewer + owner
}

type team {
    relation member: user
}
```

### Check Flow
```
Q: Can bob read document:report?

1. Is bob a direct viewer? → Check (document:report, viewer, user:bob)
2. Is bob an owner? → Check (document:report, owner, user:bob)
3. Is bob in a team that's a viewer? 
   → Find teams where bob is member
   → Check (document:report, viewer, team:X#member)
4. Can bob read parent folder?
   → Find parent folder
   → Recursively check read permission
```

### SpiceDB Example
```java
// Using SpiceDB Java client
SpiceDbClient client = SpiceDbClient.builder()
    .target("localhost:50051")
    .build();

// Create relationship
client.writeRelationships(WriteRelationshipsRequest.newBuilder()
    .addUpdates(RelationshipUpdate.newBuilder()
        .setOperation(Operation.TOUCH)
        .setRelationship(Relationship.newBuilder()
            .setResource(ObjectReference.newBuilder()
                .setObjectType("document")
                .setObjectId("report"))
            .setRelation("owner")
            .setSubject(SubjectReference.newBuilder()
                .setObject(ObjectReference.newBuilder()
                    .setObjectType("user")
                    .setObjectId("alice")))))
    .build());

// Check permission
CheckPermissionResponse response = client.checkPermission(
    CheckPermissionRequest.newBuilder()
        .setResource(ObjectReference.newBuilder()
            .setObjectType("document")
            .setObjectId("report"))
        .setPermission("read")
        .setSubject(SubjectReference.newBuilder()
            .setObject(ObjectReference.newBuilder()
                .setObjectType("user")
                .setObjectId("bob")))
        .build());

boolean canRead = response.getPermissionship() == Permissionship.HAS_PERMISSION;
```

## Policy Engines

### Open Policy Agent (OPA)
```rego
# policy.rego
package authz

default allow = false

# Allow if user is admin
allow {
    input.user.roles[_] == "admin"
}

# Allow read if same department
allow {
    input.action == "read"
    input.user.department == input.resource.department
}

# Allow during business hours
allow {
    input.action == "read"
    time.hour(time.now_ns()) >= 9
    time.hour(time.now_ns()) < 18
}
```

```java
// OPA integration
@Component
public class OpaAuthorizationManager {
    
    private final WebClient opaClient;
    
    public boolean isAuthorized(User user, Resource resource, String action) {
        Map<String, Object> input = Map.of(
            "user", Map.of(
                "id", user.getId(),
                "roles", user.getRoles(),
                "department", user.getDepartment()
            ),
            "resource", Map.of(
                "id", resource.getId(),
                "type", resource.getType(),
                "department", resource.getDepartment()
            ),
            "action", action
        );
        
        OpaResponse response = opaClient.post()
            .uri("/v1/data/authz/allow")
            .bodyValue(Map.of("input", input))
            .retrieve()
            .bodyToMono(OpaResponse.class)
            .block();
        
        return response.getResult();
    }
}
```

### Casbin
```ini
# model.conf
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

```csv
# policy.csv
p, admin, /api/*, *
p, user, /api/documents, read
p, editor, /api/documents, write
g, alice, admin
g, bob, editor
```

## Implementation Examples

### Combined RBAC + ABAC
```java
@Component
public class HybridAuthorizationService {
    
    public boolean authorize(Authentication auth, Object resource, String action) {
        // First check: RBAC for coarse-grained access
        if (!hasRequiredRole(auth, resource, action)) {
            return false;
        }
        
        // Second check: ABAC for fine-grained rules
        return evaluateAbacPolicy(auth, resource, action);
    }
    
    private boolean hasRequiredRole(Authentication auth, Object resource, String action) {
        if (resource instanceof Document) {
            return switch (action) {
                case "read" -> hasAnyRole(auth, "USER", "EDITOR", "ADMIN");
                case "write" -> hasAnyRole(auth, "EDITOR", "ADMIN");
                case "delete" -> hasAnyRole(auth, "ADMIN");
                default -> false;
            };
        }
        return false;
    }
    
    private boolean evaluateAbacPolicy(Authentication auth, Object resource, String action) {
        // Additional contextual checks
        if (resource instanceof Document doc) {
            // Owner can always access their documents
            if (doc.getOwnerId().equals(auth.getName())) {
                return true;
            }
            
            // Check department access
            String userDept = extractDepartment(auth);
            if (doc.getDepartment().equals(userDept)) {
                return true;
            }
            
            // Time-based restrictions for confidential docs
            if (doc.isConfidential() && !isBusinessHours()) {
                return false;
            }
        }
        return true;
    }
}
```

### Resource-Level Permissions Table
```sql
CREATE TABLE resource_permissions (
    id UUID PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID NOT NULL,
    principal_type VARCHAR(20) NOT NULL,  -- 'user' or 'group'
    principal_id UUID NOT NULL,
    permission VARCHAR(20) NOT NULL,      -- 'read', 'write', 'admin'
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(resource_type, resource_id, principal_type, principal_id, permission)
);

-- Check permission
SELECT EXISTS(
    SELECT 1 FROM resource_permissions
    WHERE resource_type = 'document'
    AND resource_id = :resourceId
    AND (
        (principal_type = 'user' AND principal_id = :userId)
        OR (principal_type = 'group' AND principal_id IN (:userGroupIds))
    )
    AND permission IN ('read', 'write', 'admin')
);
```
