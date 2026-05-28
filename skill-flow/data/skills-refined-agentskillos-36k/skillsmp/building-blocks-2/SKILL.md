---
name: building-blocks
description: "Component specification toolkit for breaking software projects into discrete, buildable blocks. Create detailed specifications with interfaces, dependencies, test criteria, and effort estimates for Claude Code to build incrementally."
allowed-tools: [Read, Write, Edit, Bash]
---

# Building Blocks Specification

## Overview

Building blocks are discrete, independently buildable components that together form a complete software system. This skill helps you decompose projects into well-specified blocks that Claude Code can build incrementally, with clear interfaces, dependencies, and acceptance criteria.

## When to Use This Skill

This skill should be used when:
- Decomposing a system into buildable components
- Creating detailed component specifications
- Defining interfaces between components
- Specifying API contracts and events
- Estimating effort and complexity
- Planning incremental delivery

## Visual Enhancement with Project Diagrams

**When documenting building blocks, always include diagrams.**

Use the **project-diagrams** skill to generate:
- Component dependency diagrams
- Interface contract visualizations
- Data flow between components
- Build sequence diagrams

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Building Block Framework

### Block Types

| Type | Description | Examples |
|------|-------------|----------|
| **frontend** | User interface components | Dashboard, Forms, Navigation |
| **backend** | Server-side services | Auth Service, API Gateway, Business Logic |
| **infrastructure** | Platform and DevOps | CI/CD, Monitoring, Database Setup |
| **integration** | External system connectors | Payment Gateway, Email Service, Third-party APIs |
| **shared** | Cross-cutting components | Logging, Configuration, Utilities |

### Block Specification Schema

```yaml
building_block:
  # Identity
  name: "string - clear, descriptive name"
  id: "string - unique identifier (e.g., BB-001)"
  type: "frontend | backend | infrastructure | integration | shared"

  # Description
  description: "string - what this block does and why"
  responsibilities:
    - "string - specific responsibility 1"
    - "string - specific responsibility 2"

  # Dependencies
  dependencies:
    internal:
      - block_id: "BB-XXX"
        type: "required | optional"
        interface: "interface name"
    external:
      - name: "PostgreSQL"
        version: ">=14.0"
        purpose: "Primary data storage"

  # Interfaces
  interfaces:
    api_endpoints:
      - method: "GET | POST | PUT | PATCH | DELETE"
        path: "/api/v1/resource"
        description: "What this endpoint does"
        request_schema: "schema reference or inline"
        response_schema: "schema reference or inline"
        auth_required: true | false

    events_published:
      - name: "event.name"
        description: "When this event is emitted"
        payload_schema: "schema reference"

    events_consumed:
      - name: "event.name"
        description: "How this block responds"

    data_contracts:
      - name: "Contract name"
        description: "Data structure shared"
        schema: "schema reference"

  # Estimation
  complexity: "S | M | L | XL"
  estimated_hours: number
  story_points: number

  # Quality
  test_criteria:
    - "string - acceptance criterion 1"
    - "string - acceptance criterion 2"

  # Metadata
  priority: "critical | high | medium | low"
  sprint_assignment: "Sprint N"
  owner: "string - responsible team/person"
```

### Complexity Guidelines

| Complexity | Hours | Story Points | Characteristics |
|------------|-------|--------------|-----------------|
| **S (Small)** | 4-8 | 1-2 | Single responsibility, minimal dependencies, straightforward implementation |
| **M (Medium)** | 16-24 | 3-5 | Multiple responsibilities, some dependencies, standard patterns |
| **L (Large)** | 32-48 | 8-13 | Complex logic, multiple dependencies, custom implementations |
| **XL (Extra Large)** | 48-80 | 13-21 | Highly complex, many dependencies, novel solutions needed |

## Decomposition Process

### Step 1: Identify Domains

Start with domain-driven decomposition:

1. **List core domains** - What are the main business areas?
2. **Identify bounded contexts** - Where are the natural boundaries?
3. **Map domain interactions** - How do domains communicate?

### Step 2: Extract Components

For each domain, identify components:

**Questions to ask:**
- What are the distinct responsibilities?
- What could be built and deployed independently?
- What has different scaling characteristics?
- What changes together vs. changes independently?

### Step 3: Define Interfaces

For each component:

1. **API Contracts** - REST endpoints, GraphQL operations
2. **Event Contracts** - Messages published/consumed
3. **Data Contracts** - Shared data structures

### Step 4: Map Dependencies

Create a dependency graph:

```
BB-001 (Auth) ← BB-002 (User Service)
                    ↑
              BB-003 (API Gateway)
                    ↑
              BB-004 (Frontend)
```

**Dependency Rules:**
- No circular dependencies
- Minimize dependency chains
- Shared components at the bottom
- Infrastructure before business logic

### Step 5: Estimate Effort

For each block:

1. Review similar past work
2. Consider complexity factors
3. Apply team velocity adjustments
4. Add buffer for unknowns (20-30%)

## Block Specification Examples

### Backend Service Block

```yaml
building_block:
  name: "User Authentication Service"
  id: "BB-001"
  type: "backend"

  description: |
    Handles user authentication, authorization, and session management.
    Supports email/password login and OAuth2 social providers.

  responsibilities:
    - "User registration with email verification"
    - "Login/logout with session management"
    - "JWT token generation and validation"
    - "OAuth2 integration (Google, GitHub)"
    - "Password reset flow"
    - "Role-based access control"

  dependencies:
    internal:
      - block_id: "BB-010"
        type: "required"
        interface: "Database Service"
    external:
      - name: "PostgreSQL"
        version: ">=14.0"
        purpose: "User credentials and sessions"
      - name: "Redis"
        version: ">=6.0"
        purpose: "Session cache and rate limiting"

  interfaces:
    api_endpoints:
      - method: "POST"
        path: "/api/v1/auth/register"
        description: "Register new user with email/password"
        request_schema:
          email: "string (email format)"
          password: "string (min 8 chars)"
          name: "string"
        response_schema:
          user_id: "uuid"
          message: "string"
        auth_required: false

      - method: "POST"
        path: "/api/v1/auth/login"
        description: "Authenticate user and return tokens"
        request_schema:
          email: "string"
          password: "string"
        response_schema:
          access_token: "string (JWT)"
          refresh_token: "string"
          expires_in: "number (seconds)"
        auth_required: false

      - method: "POST"
        path: "/api/v1/auth/refresh"
        description: "Refresh access token"
        auth_required: true

      - method: "POST"
        path: "/api/v1/auth/logout"
        description: "Invalidate session"
        auth_required: true

      - method: "GET"
        path: "/api/v1/auth/me"
        description: "Get current user profile"
        auth_required: true

    events_published:
      - name: "user.registered"
        description: "Emitted when new user completes registration"
        payload_schema:
          user_id: "uuid"
          email: "string"
          registered_at: "timestamp"

      - name: "user.logged_in"
        description: "Emitted on successful login"
        payload_schema:
          user_id: "uuid"
          login_at: "timestamp"
          method: "password | oauth"

  complexity: "M"
  estimated_hours: 24
  story_points: 5

  test_criteria:
    - "User can register with valid email and password"
    - "Registration fails with invalid email format"
    - "Registration fails with weak password"
    - "User can login with correct credentials"
    - "Login fails with incorrect password (returns 401)"
    - "User receives valid JWT token on login"
    - "JWT token contains correct claims (user_id, roles)"
    - "Token refresh works with valid refresh token"
    - "Logout invalidates session"
    - "Protected endpoints reject invalid tokens"
    - "Rate limiting prevents brute force attacks"

  priority: "critical"
  sprint_assignment: "Sprint 1"
```

### Frontend Component Block

```yaml
building_block:
  name: "Dashboard UI"
  id: "BB-020"
  type: "frontend"

  description: |
    Main dashboard interface showing key metrics, recent activity,
    and navigation to other features.

  responsibilities:
    - "Display key performance metrics"
    - "Show recent user activity feed"
    - "Provide navigation to features"
    - "Handle responsive layout"
    - "Manage loading and error states"

  dependencies:
    internal:
      - block_id: "BB-001"
        type: "required"
        interface: "Auth Service (for user context)"
      - block_id: "BB-005"
        type: "required"
        interface: "Metrics API"
      - block_id: "BB-025"
        type: "required"
        interface: "Design System Components"
    external:
      - name: "React"
        version: ">=18.0"
        purpose: "UI framework"
      - name: "TanStack Query"
        version: ">=5.0"
        purpose: "Data fetching and caching"

  interfaces:
    api_consumed:
      - endpoint: "GET /api/v1/metrics/summary"
        purpose: "Load dashboard metrics"
      - endpoint: "GET /api/v1/activity/recent"
        purpose: "Load activity feed"

    components_exposed:
      - name: "DashboardPage"
        description: "Main dashboard route component"
      - name: "MetricsWidget"
        description: "Reusable metrics display widget"

  complexity: "M"
  estimated_hours: 20
  story_points: 5

  test_criteria:
    - "Dashboard loads and displays metrics"
    - "Activity feed shows recent items"
    - "Loading state shown while fetching"
    - "Error state shown on API failure"
    - "Responsive layout works on mobile"
    - "Navigation links work correctly"
    - "Auto-refresh updates data periodically"

  priority: "high"
  sprint_assignment: "Sprint 2"
```

### Infrastructure Block

```yaml
building_block:
  name: "CI/CD Pipeline"
  id: "BB-100"
  type: "infrastructure"

  description: |
    Continuous integration and deployment pipeline using GitHub Actions.
    Handles testing, building, and deploying to staging and production.

  responsibilities:
    - "Run tests on pull requests"
    - "Build Docker images"
    - "Push to container registry"
    - "Deploy to staging automatically"
    - "Deploy to production with approval"
    - "Run database migrations"

  dependencies:
    external:
      - name: "GitHub Actions"
        purpose: "CI/CD platform"
      - name: "Docker Hub / ECR"
        purpose: "Container registry"
      - name: "AWS ECS / Kubernetes"
        purpose: "Deployment target"

  interfaces:
    triggers:
      - event: "push to main"
        action: "Deploy to staging"
      - event: "release tag"
        action: "Deploy to production"
      - event: "pull request"
        action: "Run tests"

    outputs:
      - name: "Docker images"
        format: "project/service:version"
      - name: "Test reports"
        format: "JUnit XML"
      - name: "Coverage reports"
        format: "Cobertura XML"

  complexity: "M"
  estimated_hours: 16
  story_points: 3

  test_criteria:
    - "Pipeline triggers on push to main"
    - "Tests run and report results"
    - "Build creates valid Docker image"
    - "Image is pushed to registry"
    - "Staging deployment succeeds"
    - "Production requires manual approval"
    - "Rollback mechanism works"
    - "Secrets are not exposed in logs"

  priority: "critical"
  sprint_assignment: "Sprint 1"
```

## Output Format

### building_blocks.yaml

Primary output file listing all blocks:

```yaml
# Building Blocks Specification
# Project: [Project Name]
# Generated: [Date]

metadata:
  project: "[Project Name]"
  total_blocks: N
  total_estimated_hours: N
  version: "1.0.0"

building_blocks:
  - name: "Block 1"
    id: "BB-001"
    # ... full specification

  - name: "Block 2"
    id: "BB-002"
    # ... full specification

dependency_graph:
  - from: "BB-002"
    to: "BB-001"
    type: "required"
  - from: "BB-003"
    to: "BB-001"
    type: "required"

build_order:
  - phase: 1
    blocks: ["BB-001", "BB-100"]
  - phase: 2
    blocks: ["BB-002", "BB-003"]
  - phase: 3
    blocks: ["BB-020", "BB-021"]
```

### Component Specifications Directory

For complex blocks, create detailed specs:

```
components/
├── building_blocks.yaml          # Master list
├── component_specs/
│   ├── BB-001_auth_service.md   # Detailed spec
│   ├── BB-002_user_service.md
│   └── BB-020_dashboard_ui.md
└── interfaces/
    ├── api_contracts.yaml        # OpenAPI specs
    └── event_contracts.yaml      # Event schemas
```

## Quality Checklist

Before completing building blocks specification:

- [ ] All system functionality covered by blocks
- [ ] No overlapping responsibilities between blocks
- [ ] Dependencies form DAG (no circular dependencies)
- [ ] All interfaces specified with schemas
- [ ] Complexity estimates are realistic
- [ ] Test criteria are specific and testable
- [ ] Build order respects dependencies
- [ ] Shared/infrastructure blocks identified
- [ ] Dependency diagram generated

## Best Practices

### Do's
- Keep blocks focused (single responsibility)
- Make blocks independently testable
- Define interfaces before implementation details
- Include error handling in test criteria
- Version interface contracts
- Document why blocks are separated

### Don'ts
- Don't create blocks that are too small (< 4 hours)
- Don't create blocks that are too large (> 80 hours)
- Don't have hidden dependencies
- Don't specify implementation details in interfaces
- Don't skip test criteria
- Don't forget infrastructure blocks
