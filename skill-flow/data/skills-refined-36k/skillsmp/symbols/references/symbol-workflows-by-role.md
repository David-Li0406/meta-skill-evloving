# Symbol Workflows by Role

Practical workflow examples demonstrating how different developer roles use the symbol system efficiently. Each workflow showcases progressive loading strategies and token optimization techniques.

## Overview

The symbol system supports different development roles with tailored workflows:

1. **Frontend Developers** - UI components, hooks, and app development
2. **Backend Developers** - API services, repositories, and schemas
3. **Full-Stack Developers** - Cross-domain development patterns
4. **Debugging & QA** - Comprehensive context including tests
5. **Architecture Review** - Layer validation and pattern checking

Each workflow demonstrates:
- Targeted symbol loading for specific tasks
- Progressive context building
- Token efficiency gains
- Practical code examples

---

## Frontend Development Workflows

### Workflow 1: Building a New React Component

**Scenario:** Creating a new `ProfileCard` component in the UI library.

**Steps:**

```python
from symbol_tools import query_symbols, load_domain, get_symbol_context

# Step 1: Find existing Card components for patterns
existing_cards = query_symbols(
    name="Card",
    kind="component",
    domain="ui",
    limit=10
)
# Result: ~2KB, 99% reduction
# Returns: Card, CardHeader, CardContent, CardFooter, etc.

# Step 2: Get detailed context for base Card component
card_context = get_symbol_context(
    name="Card",
    include_related=True
)
# Result: +3KB (5KB total)
# Returns: Card component + CardProps interface + related types

# Step 3: Load UI domain symbols for additional context
ui_context = load_domain(
    domain="ui",
    max_symbols=100
)
# Result: +12KB (17KB total), still 95% reduction vs full files
# Returns: All UI components, hooks, and utilities

# Step 4: Find similar profile-related components
profile_components = query_symbols(
    name="Profile",
    domain="ui",
    limit=5
)
# Result: +1KB (18KB total)
# Returns: ProfileAvatar, ProfileBadge, etc.
```

**Token Efficiency:**
- Total loaded: ~18KB
- Full codebase alternative: ~500KB+
- **Reduction: 96.4%**

**Result:** Complete context for building new component following existing patterns.

---

### Workflow 2: Adding Data Fetching to Frontend Page

**Scenario:** Adding user data fetching to a profile page using existing hooks.

**Steps:**

```python
from symbol_tools import query_symbols, search_patterns

# Step 1: Find existing data fetching hooks
api_hooks = query_symbols(
    kind="hook",
    path="hooks/queries",
    domain="web",
    limit=15
)
# Result: ~3KB
# Returns: useUser, useAuth, useQuery patterns

# Step 2: Find user-related API integration
user_api = query_symbols(
    name="user",
    path="lib/api",
    kind="function",
    domain="web",
    limit=10
)
# Result: +2KB (5KB total)
# Returns: fetchUser, updateUser, deleteUser

# Step 3: Search for similar patterns in pages
similar_patterns = search_patterns(
    pattern="Profile",
    layer="page",
    domain="web",
    limit=5
)
# Result: +2KB (7KB total)
# Returns: ProfilePage, ProfileSettings, etc.

# Step 4: Get state management patterns
state_hooks = query_symbols(
    kind="hook",
    path="contexts",
    domain="web",
    limit=10
)
# Result: +2KB (9KB total)
# Returns: useUserContext, useAuthContext, etc.
```

**Token Efficiency:**
- Total loaded: ~9KB
- Alternative (loading all files): ~300KB+
- **Reduction: 97%**

**Result:** Complete data fetching patterns without loading full page files.

---

### Workflow 3: Refactoring UI Component Variants

**Scenario:** Standardizing button variants across the UI library.

**Steps:**

```python
from symbol_tools import search_patterns, get_symbol_context, load_domain

# Step 1: Find all button components
buttons = search_patterns(
    pattern="Button",
    layer="component",
    domain="ui"
)
# Result: ~4KB
# Returns: Button, IconButton, LinkButton, etc.

# Step 2: Get context for each button with props
button_contexts = [
    get_symbol_context(name=btn["name"], include_related=True)
    for btn in buttons[:5]
]
# Result: +8KB (12KB total)
# Returns: Full component definitions + props interfaces

# Step 3: Load design system utilities
design_tokens = query_symbols(
    path="tokens",
    domain="ui",
    limit=20
)
# Result: +3KB (15KB total)
# Returns: Color tokens, spacing, typography

# Step 4: Check variant patterns in other components
variant_patterns = search_patterns(
    pattern="variant",
    layer="component",
    domain="ui",
    limit=15
)
# Result: +3KB (18KB total)
# Returns: Components using variant patterns
```

**Token Efficiency:**
- Total loaded: ~18KB
- Alternative: ~400KB+ (all component files)
- **Reduction: 95.5%**

**Result:** Complete variant patterns for standardization.

---

## Backend Development Workflows

### Workflow 4: Implementing New Service Method

**Scenario:** Adding a new method to `UserService` following existing patterns.

**Steps:**

```python
from symbol_tools import load_api_layer, search_patterns, get_symbol_context

# Step 1: Load only service layer (most efficient)
services = load_api_layer("services", max_symbols=50)
# Result: ~20KB
# Returns: All service classes and methods
# Efficiency: 80-85% reduction vs full backend

# Step 2: Get context for UserService specifically
user_service = get_symbol_context(
    name="UserService",
    file="api/services/user_service.py",
    include_related=True
)
# Result: +5KB (25KB total)
# Returns: UserService + related DTOs + dependencies

# Step 3: Find similar service patterns
service_patterns = search_patterns(
    pattern="Service",
    layer="service",
    domain="api",
    limit=10
)
# Result: +3KB (28KB total)
# Returns: Patterns from other services

# Step 4: Load schemas for DTO patterns
schemas = load_api_layer("schemas", max_symbols=30)
# Result: +8KB (36KB total)
# Returns: Request/response DTOs
```

**Token Efficiency:**
- Total loaded: ~36KB
- Alternative (full backend): ~250KB+
- **Reduction: 85.6%**

**Result:** Complete service patterns without loading repositories, routers, or tests.

---

### Workflow 5: Adding New API Endpoint

**Scenario:** Creating a new REST endpoint in the router layer.

**Steps:**

```python
from symbol_tools import load_api_layer, query_symbols, get_symbol_context

# Step 1: Load only router layer
routers = load_api_layer("routers", max_symbols=40)
# Result: ~18KB
# Returns: All route handlers and endpoints
# Efficiency: 85-90% reduction vs full backend

# Step 2: Find authentication patterns in routers
auth_patterns = query_symbols(
    name="auth",
    kind="function",
    path="routers",
    domain="api",
    limit=10
)
# Result: +3KB (21KB total)
# Returns: Protected route patterns

# Step 3: Load schemas for request/response models
schemas = load_api_layer("schemas", max_symbols=25)
# Result: +7KB (28KB total)
# Returns: DTOs for request validation

# Step 4: Get specific router context
user_router = get_symbol_context(
    name="user_router",
    include_related=True
)
# Result: +4KB (32KB total)
# Returns: Router file with all endpoints
```

**Token Efficiency:**
- Total loaded: ~32KB
- Alternative (full backend): ~250KB+
- **Reduction: 87.2%**

**Result:** Complete endpoint patterns without loading services, repositories, or business logic.

---

### Workflow 6: Implementing Repository Data Access

**Scenario:** Adding a new database query method to a repository.

**Steps:**

```python
from symbol_tools import load_api_layer, search_patterns, get_symbol_context

# Step 1: Load only repository layer
repositories = load_api_layer("repositories", max_symbols=35)
# Result: ~16KB
# Returns: All data access patterns
# Efficiency: 80-85% reduction vs full backend

# Step 2: Search for similar query patterns
query_patterns = search_patterns(
    pattern="query|find|get",
    layer="repository",
    domain="api",
    limit=15
)
# Result: +4KB (20KB total)
# Returns: Common query method patterns

# Step 3: Get context for specific repository
user_repo = get_symbol_context(
    name="UserRepository",
    file="api/repositories/user_repository.py",
    include_related=True
)
# Result: +5KB (25KB total)
# Returns: Repository + model references

# Step 4: Load cores for model definitions
cores = load_api_layer("cores", max_symbols=30)
# Result: +10KB (35KB total)
# Returns: Domain models and ORM entities
```

**Token Efficiency:**
- Total loaded: ~35KB
- Alternative (full backend): ~250KB+
- **Reduction: 86%**

**Result:** Complete data access patterns without loading routers or services.

---

### Workflow 7: Working with DTOs and Validation

**Scenario:** Creating new request/response schemas with validation.

**Steps:**

```python
from symbol_tools import load_api_layer, search_patterns, query_symbols

# Step 1: Load only schema layer
schemas = load_api_layer("schemas", max_symbols=50)
# Result: ~22KB
# Returns: All DTOs and validation schemas
# Efficiency: 85-90% reduction vs full backend

# Step 2: Find validation patterns
validation_patterns = search_patterns(
    pattern="validate|validator",
    layer="schema",
    domain="api",
    limit=10
)
# Result: +3KB (25KB total)
# Returns: Validation decorators and patterns

# Step 3: Find similar entity schemas
user_schemas = query_symbols(
    name="User",
    kind="class",
    path="schemas",
    domain="api",
    limit=8
)
# Result: +3KB (28KB total)
# Returns: UserCreate, UserUpdate, UserResponse, etc.

# Step 4: Load cores for base models
base_models = load_api_layer("cores", max_symbols=20)
# Result: +7KB (35KB total)
# Returns: Base DTO classes and utilities
```

**Token Efficiency:**
- Total loaded: ~35KB
- Alternative (full backend): ~250KB+
- **Reduction: 86%**

**Result:** Complete DTO patterns without loading any business logic or data access code.

---

## Full-Stack Development Workflows

### Workflow 8: Cross-Domain Feature Implementation

**Scenario:** Building a feature that touches frontend UI, web app, and backend API.

**Steps:**

```python
from symbol_tools import load_domain, load_api_layer, query_symbols

# Step 1: Load UI components (small, focused set)
ui_context = load_domain(
    domain="ui",
    max_symbols=50
)
# Result: ~8KB
# Returns: Core UI components

# Step 2: Load web app hooks and utilities
web_hooks = query_symbols(
    kind="hook",
    domain="web",
    limit=15
)
# Result: +3KB (11KB total)
# Returns: Data fetching hooks

# Step 3: Load backend service layer only
services = load_api_layer("services", max_symbols=30)
# Result: +12KB (23KB total)
# Returns: Business logic layer

# Step 4: Load backend schemas for DTOs
schemas = load_api_layer("schemas", max_symbols=25)
# Result: +8KB (31KB total)
# Returns: API contracts

# Step 5: Check shared types
shared_types = load_domain(
    domain="shared",
    max_symbols=20
)
# Result: +5KB (36KB total)
# Returns: Shared interfaces and types
```

**Token Efficiency:**
- Total loaded: ~36KB
- Alternative (all domains): ~800KB+
- **Reduction: 95.5%**

**Result:** Complete cross-domain context for full-stack feature.

---

### Workflow 9: Architecture Pattern Validation

**Scenario:** Validating that code follows layered architecture (Router → Service → Repository).

**Steps:**

```python
from symbol_tools import load_api_layer, search_patterns

# Step 1: Load routers to check routing layer
routers = load_api_layer("routers")
# Result: ~18KB
# Returns: All route handlers

# Step 2: Load services to check business logic layer
services = load_api_layer("services")
# Result: +20KB (38KB total)
# Returns: All service classes

# Step 3: Load repositories to check data access layer
repositories = load_api_layer("repositories")
# Result: +16KB (54KB total)
# Returns: All data access methods

# Step 4: Validate pattern compliance
# Check that routers call services (not repositories directly)
router_service_calls = search_patterns(
    pattern="Service",
    layer="router",
    domain="api"
)
# Result: +2KB (56KB total)

# Check that services call repositories (not direct DB access)
service_repo_calls = search_patterns(
    pattern="Repository",
    layer="service",
    domain="api"
)
# Result: +2KB (58KB total)
```

**Token Efficiency:**
- Total loaded: ~58KB
- Alternative (full backend): ~250KB+
- **Reduction: 76.8%**

**Result:** Complete architectural validation without loading models, schemas, or tests.

---

## Debugging & QA Workflows

### Workflow 10: Bug Investigation with Tests

**Scenario:** Investigating a bug in a component, including test coverage.

**Steps:**

```python
from symbol_tools import get_symbol_context, load_domain, query_symbols

# Step 1: Get component context with related symbols
component = get_symbol_context(
    name="Button",
    include_related=True
)
# Result: ~5KB
# Returns: Button + ButtonProps + utilities

# Step 2: Load UI domain WITH tests
ui_with_tests = load_domain(
    domain="ui",
    include_tests=True,
    max_symbols=50
)
# Result: +15KB (20KB total)
# Returns: Components + test files

# Step 3: Find test files for this component
button_tests = query_symbols(
    name="Button",
    kind="function",
    path="test",
    domain="ui"
)
# Result: +2KB (22KB total)
# Returns: Test cases for Button

# Step 4: Find related hooks and utilities
related_hooks = query_symbols(
    path="hooks",
    domain="web",
    limit=10
)
# Result: +2KB (24KB total)
# Returns: Hooks that might be used by component
```

**Token Efficiency:**
- Total loaded: ~24KB
- Alternative (all files + tests): ~400KB+
- **Reduction: 94%**

**Result:** Complete debugging context including tests and related code.

---

### Workflow 11: Integration Testing Pattern Discovery

**Scenario:** Finding integration test patterns across backend services.

**Steps:**

```python
from symbol_tools import load_domain, search_patterns, query_symbols

# Step 1: Load API domain with tests
api_with_tests = load_domain(
    domain="api",
    include_tests=True,
    max_symbols=80
)
# Result: ~30KB
# Returns: API code + test files

# Step 2: Find integration test patterns
integration_tests = search_patterns(
    pattern="integration|Integration",
    layer="test",
    domain="api",
    limit=15
)
# Result: +4KB (34KB total)
# Returns: Integration test classes/functions

# Step 3: Find test fixtures and utilities
test_utils = query_symbols(
    kind="function",
    path="tests/fixtures",
    domain="api",
    limit=20
)
# Result: +3KB (37KB total)
# Returns: Test utilities and fixtures

# Step 4: Load services being tested
services = load_api_layer("services", max_symbols=30)
# Result: +12KB (49KB total)
# Returns: Service implementations
```

**Token Efficiency:**
- Total loaded: ~49KB
- Alternative (all backend + all tests): ~350KB+
- **Reduction: 86%**

**Result:** Complete test patterns with service context.

---

## Architecture Review Workflows

### Workflow 12: Layer Compliance Audit

**Scenario:** Auditing that all code follows proper architectural layers.

**Steps:**

```python
from symbol_tools import search_patterns, load_api_layer

# Step 1: Audit router layer
routers = load_api_layer("routers")
# Check: Routers should call services, not repositories directly

# Step 2: Audit service layer
services = load_api_layer("services")
# Check: Services should call repositories, not direct DB

# Step 3: Audit repository layer
repositories = load_api_layer("repositories")
# Check: Repositories should only access data layer

# Step 4: Find violations
# Example: Routers calling repositories directly
violations = search_patterns(
    pattern="Repository",
    layer="router",
    domain="api"
)
# Result: If found, indicates architecture violation
```

**Token Efficiency:**
- Total loaded: ~54KB (all layers)
- Alternative (full backend): ~250KB+
- **Reduction: 78.4%**

**Result:** Complete architecture compliance audit.

---

### Workflow 13: Component Design System Audit

**Scenario:** Ensuring all UI components follow design system patterns.

**Steps:**

```python
from symbol_tools import load_domain, search_patterns, get_symbol_context

# Step 1: Load all UI components
ui_components = load_domain(
    domain="ui",
    max_symbols=100
)
# Result: ~15KB
# Returns: All design system components

# Step 2: Check variant patterns
variant_usage = search_patterns(
    pattern="variant",
    layer="component",
    domain="ui"
)
# Result: +4KB (19KB total)
# Returns: Components using variants

# Step 3: Check accessibility props
a11y_patterns = search_patterns(
    pattern="aria|role|label",
    layer="component",
    domain="ui"
)
# Result: +3KB (22KB total)
# Returns: Accessibility implementations

# Step 4: Load design tokens
tokens = query_symbols(
    path="tokens",
    domain="ui",
    limit=25
)
# Result: +4KB (26KB total)
# Returns: Design token definitions
```

**Token Efficiency:**
- Total loaded: ~26KB
- Alternative (all component files): ~300KB+
- **Reduction: 91.3%**

**Result:** Complete design system compliance audit.

---

## Progressive Loading Strategy

All workflows follow a three-tier progressive loading approach:

### Tier 1: Essential Context (25-30% of budget)

Load 10-20 symbols directly related to current task.

**Techniques:**
- Targeted queries: `query_symbols(name="specific", limit=10)`
- Specific symbol context: `get_symbol_context(name="Component")`
- Layer-specific loading: `load_api_layer("services", max_symbols=20)`

### Tier 2: Supporting Context (15-20% of budget)

Load related patterns and utilities.

**Techniques:**
- Domain loading with limits: `load_domain(domain="ui", max_symbols=50)`
- Pattern searches: `search_patterns(pattern="pattern", layer="layer")`
- Cross-domain interfaces: `load_domain(domain="shared", max_symbols=30)`

### Tier 3: On-Demand Context (remaining budget)

Specific lookups when needed.

**Techniques:**
- Deep dependency analysis: `get_symbol_context(include_related=True)`
- Full domain loading: `load_domain(domain="api", include_tests=True)`
- Additional layer loading: `load_api_layer("repositories")`

---

## Token Efficiency Summary

| Workflow Type | Typical Load | Alternative | Reduction |
|---------------|-------------|-------------|-----------|
| Frontend component | ~18KB | ~500KB | 96.4% |
| Frontend data fetch | ~9KB | ~300KB | 97% |
| Backend service | ~36KB | ~250KB | 85.6% |
| Backend endpoint | ~32KB | ~250KB | 87.2% |
| Backend repository | ~35KB | ~250KB | 86% |
| Full-stack feature | ~36KB | ~800KB | 95.5% |
| Debug with tests | ~24KB | ~400KB | 94% |
| Architecture audit | ~54KB | ~250KB | 78.4% |

**Average token reduction: 89.5%**

---

## Best Practices

1. **Start Specific** - Use targeted queries before broad loading
2. **Layer-Based for Backend** - Always prefer `load_api_layer()` over full domain
3. **Use Limits** - Apply `max_symbols` to control context size
4. **Progressive Loading** - Load in tiers, not all at once
5. **Include Tests Sparingly** - Only load tests when debugging
6. **Summary-Only Scans** - Use `summary_only=True` for quick overviews

---

## See Also

- **[symbol-api-reference.md](./symbol-api-reference.md)** - Complete API documentation
- **[symbol-script-operations.md](./symbol-script-operations.md)** - Symbol maintenance operations
- **[symbol-schema-architecture.md](./symbol-schema-architecture.md)** - Symbol structure and layer taxonomy
- **[symbol-performance-metrics.md](./symbol-performance-metrics.md)** - Detailed benchmarks
