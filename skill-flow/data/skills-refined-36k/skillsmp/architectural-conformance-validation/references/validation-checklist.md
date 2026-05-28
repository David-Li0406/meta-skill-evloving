# Architectural Conformance Validation Checklist

Comprehensive checklist for validating architectural conformance.

---

## Design Pattern Conformance

### Creational Patterns
- [ ] **Singleton**: Private constructor, static getInstance(), thread-safe
- [ ] **Factory**: Creates objects without exposing instantiation logic
- [ ] **Builder**: Constructs complex objects step-by-step
- [ ] **Prototype**: Creates objects by cloning existing instance
- [ ] **Dependency Injection**: Dependencies injected, not created internally

### Structural Patterns
- [ ] **Adapter**: Converts interface to expected interface
- [ ] **Decorator**: Adds behavior without modifying object
- [ ] **Facade**: Simplifies complex subsystem interface
- [ ] **Proxy**: Controls access to another object
- [ ] **Composite**: Treats individual and composites uniformly

### Behavioral Patterns
- [ ] **Observer**: One-to-many dependency for state changes
- [ ] **Strategy**: Encapsulates algorithms, makes them interchangeable
- [ ] **Command**: Encapsulates request as object
- [ ] **State**: Alters behavior when internal state changes
- [ ] **Template Method**: Defines skeleton, subclasses override steps

---

## ADR Compliance Checks

### Technology Decisions
- [ ] Uses approved programming languages
- [ ] Uses approved frameworks (e.g., FastAPI, React, Express)
- [ ] Uses approved libraries from technology stack
- [ ] Database choice matches ADR
- [ ] No unapproved third-party dependencies

### Security/Compliance Decisions
- [ ] Authentication mechanism follows ADR
- [ ] Authorization/RBAC follows established pattern
- [ ] Data encryption follows security ADR (at rest, in transit)
- [ ] Input validation follows security standards
- [ ] Secrets management follows ADR
- [ ] Audit logging follows compliance ADR (HIPAA, PCI DSS, SOC 2)

### Algorithm/Approach Decisions
- [ ] Uses documented algorithms (e.g., Luhn validation)
- [ ] Error handling follows established pattern
- [ ] Retry logic follows resilience ADR
- [ ] Caching strategy follows performance ADR
- [ ] Rate limiting follows availability ADR

### Integration Decisions
- [ ] API contracts follow REST/GraphQL standards
- [ ] Message formats follow integration ADR
- [ ] Event schemas follow event-driven ADR
- [ ] Third-party integration follows approved patterns

---

## Structural Conformance

### Component Structure
- [ ] Component matches architecture diagram
- [ ] Component placed in correct layer (presentation, business, data)
- [ ] Component respects layer boundaries (no skipping layers)
- [ ] Component size appropriate (not too large/monolithic)
- [ ] Component responsibilities clear (single responsibility)

### Naming Conventions
- [ ] Class names follow convention (PascalCase, noun)
- [ ] Method names follow convention (camelCase, verb)
- [ ] Variable names descriptive and consistent
- [ ] File names match class/component name
- [ ] Directory structure follows convention

### Directory Structure
- [ ] Files in correct directories (src/, tests/, config/)
- [ ] Test files co-located or mirrored structure
- [ ] Configuration files in designated location
- [ ] No mixing of concerns in directories

### Dependency Management
- [ ] Dependencies declared properly (package.json, requirements.txt)
- [ ] No circular dependencies between modules
- [ ] Dependency graph follows architecture (layers, modules)
- [ ] External dependencies justified and documented

---

## API Contract Conformance

### Endpoint Design
- [ ] RESTful naming (resource-based, not action-based)
- [ ] HTTP methods used correctly (GET/POST/PUT/DELETE/PATCH)
- [ ] URL structure consistent and hierarchical
- [ ] Query parameters for filtering, not resources
- [ ] Versioning strategy followed (e.g., /v1/, /v2/)

### Request/Response
- [ ] Request schema documented and followed
- [ ] Response schema documented and followed
- [ ] Error response format consistent
- [ ] Status codes used correctly (200, 201, 400, 404, 500)
- [ ] Pagination format consistent

### Documentation
- [ ] OpenAPI/Swagger spec exists
- [ ] All endpoints documented
- [ ] Request/response examples provided
- [ ] Error codes documented

---

## Data Flow Conformance

### Data Model
- [ ] Entity relationships match architecture
- [ ] Database schema follows data model ADR
- [ ] No duplicate data storage (normalized)
- [ ] Data types consistent across system
- [ ] Validation rules applied consistently

### Data Access
- [ ] Repository pattern used (if applicable)
- [ ] ORM usage follows ADR
- [ ] Query optimization follows performance ADR
- [ ] Transaction boundaries correct
- [ ] No direct SQL in business logic (if using ORM)

### Data Flow
- [ ] Data flows through defined layers
- [ ] No bypassing business logic
- [ ] Transformations at correct boundaries
- [ ] Data validation at entry points
- [ ] Error propagation follows pattern

---

## Quality Attributes

### Performance
- [ ] Caching strategy implemented as per ADR
- [ ] Query optimization applied
- [ ] Lazy loading where appropriate
- [ ] No N+1 query problems
- [ ] Resource cleanup (connections, files)

### Scalability
- [ ] Stateless components (where required)
- [ ] Horizontal scaling considered
- [ ] No hardcoded limits (configurable)
- [ ] Connection pooling used
- [ ] Async processing where appropriate

### Maintainability
- [ ] Code modular and loosely coupled
- [ ] Clear separation of concerns
- [ ] Configuration externalized
- [ ] No magic numbers (constants defined)
- [ ] Documentation comments where needed

### Testability
- [ ] Dependencies mockable/injectable
- [ ] Pure functions where possible
- [ ] Test data fixtures available
- [ ] Integration test points identified
- [ ] No untestable code patterns

---

## Security Conformance

### Authentication
- [ ] Authentication required on protected endpoints
- [ ] Token validation correct
- [ ] Session management secure
- [ ] Password handling secure (hashing, no plaintext)

### Authorization
- [ ] Role-based access control implemented
- [ ] Permission checks at boundaries
- [ ] No privilege escalation possible
- [ ] Resource-level authorization checked

### Input Validation
- [ ] All inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection (for web apps)
- [ ] File upload validation (type, size)

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (HTTPS)
- [ ] No sensitive data in logs
- [ ] No sensitive data in error messages
- [ ] PII handling follows compliance ADR

---

## Compliance Conformance

### HIPAA (if applicable)
- [ ] PHI encrypted at rest and in transit
- [ ] Audit logging for PHI access
- [ ] Access controls implemented
- [ ] Data retention policy followed
- [ ] Breach notification process defined

### PCI DSS (if applicable)
- [ ] Cardholder data encrypted
- [ ] No storage of sensitive authentication data (CVV)
- [ ] Access to cardholder data logged
- [ ] Secure transmission protocols (TLS 1.2+)
- [ ] Regular security testing

### GDPR (if applicable)
- [ ] Consent management implemented
- [ ] Data portability supported
- [ ] Right to erasure supported
- [ ] Privacy by design principles followed
- [ ] Data processing agreement in place

---

## Common Violation Examples

### 🔴 Critical Violations

**Example 1**: Using HTTP instead of HTTPS
```typescript
// ❌ CRITICAL: Violates ADR-012 security requirements
const apiUrl = "http://api.example.com/users";

// ✅ CORRECT: Uses HTTPS
const apiUrl = "https://api.example.com/users";
```

**Example 2**: Direct instantiation instead of DI
```typescript
// ❌ CRITICAL: Violates dependency injection pattern
class UserService {
  private logger = new Logger();  // Direct instantiation
}

// ✅ CORRECT: Dependency injected
class UserService {
  constructor(private logger: Logger) {}  // Injected
}
```

### 🟡 Warning Violations

**Example 1**: Pattern variation without justification
```typescript
// ⚠️ WARNING: Singleton pattern variation
class ConfigManager {
  private static instance?: ConfigManager;

  // Public constructor (should be private)
  constructor() {
    if (ConfigManager.instance) {
      throw new Error("Use getInstance()");
    }
  }
}

// ✅ CORRECT: Standard singleton
class ConfigManager {
  private static instance?: ConfigManager;
  private constructor() {}  // Private constructor

  static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }
}
```

**Example 2**: Missing error handling pattern
```typescript
// ⚠️ WARNING: No error handling (ADR-015 requires it)
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// ✅ CORRECT: Error handling included
async function fetchUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  } catch (error) {
    logger.error("Failed to fetch user", { id, error });
    throw new ApplicationError("User fetch failed", error);
  }
}
```

### 🔵 Information Items

**Example 1**: Could use more common pattern
```typescript
// ℹ️ INFO: Factory pattern would be clearer
function createUser(type: string) {
  if (type === "admin") return new AdminUser();
  if (type === "regular") return new RegularUser();
  return new GuestUser();
}

// ✅ BETTER: Explicit factory pattern
class UserFactory {
  static create(type: UserType): User {
    switch (type) {
      case UserType.Admin: return new AdminUser();
      case UserType.Regular: return new RegularUser();
      case UserType.Guest: return new GuestUser();
      default: throw new Error(`Unknown type: ${type}`);
    }
  }
}
```

---

## Validation Severity Guidelines

**Assign CRITICAL (🔴) when:**
- Security vulnerability introduced
- Breaking change to established API
- Violates compliance requirement (HIPAA, PCI DSS)
- Incompatible with core architecture

**Assign WARNING (🟡) when:**
- Pattern variation without clear justification
- Missing established error handling
- Inconsistent with team conventions
- Potential maintainability issue

**Assign INFO (🔵) when:**
- Opportunity for optimization
- Alternative pattern would be clearer
- Documentation could be enhanced
- Best practice not followed (but not required)

---

**Last Updated**: 2025-01-21
