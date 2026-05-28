# Analysis Patterns

This document describes common analysis approaches and methodologies for codebase research. Use these patterns to conduct systematic, reproducible analysis.

## Overview

Effective codebase analysis follows proven patterns that ensure comprehensive understanding while managing complexity. These patterns can be combined based on your research goals.

---

## Core Analysis Patterns

### 1. Breadth-First Analysis

**Pattern**: Survey broadly before diving deep

**When to use**:
- Initial codebase exploration
- Understanding project structure
- Onboarding to new projects
- Creating overview documentation

**Approach**:
```markdown
1. Read high-level documentation (README, architecture docs)
2. Map directory structure (top-level only)
3. Identify major modules/domains
4. Understand technology stack
5. Survey key files without deep reading
6. Only then: Deep dive into specific areas
```

**Benefits**:
- Builds mental model before details
- Prevents getting lost in details
- Identifies what matters most
- Provides context for deep dives

**Example**:
```markdown
# Breadth-first for new project:
1. Read README.md - Project purpose, setup
2. ls src/ - See top-level organization
3. Read package.json - Dependencies, scripts
4. Glob **/*.service.ts - Identify service count
5. Read one example service.ts - Understand pattern
6. NOW: Deep dive into specific services
```

**Avoid**: Starting with random deep files - you'll lack context

---

### 2. Pattern Matching Analysis

**Pattern**: Find and compare similar implementations

**When to use**:
- Understanding how to implement features consistently
- Discovering project conventions
- Learning established patterns
- Ensuring consistency

**Approach**:
```markdown
1. Identify what you need to implement
2. Search for similar existing features
3. Read 2-3 representative examples
4. Identify common patterns
5. Document the pattern
6. Apply pattern to new implementation
```

**Search strategy**:
```bash
# Example: Understanding service pattern
1. Glob: "**/*service*.ts" (find all services)
2. Read: 3 different services (user, auth, product)
3. Compare: Structure, methods, dependencies
4. Document: Common service pattern
5. Apply: Use pattern for new service
```

**Benefits**:
- Ensures consistency with existing code
- Faster learning than documentation alone
- Reveals unwritten conventions
- Reduces decision fatigue

**Example**:
```markdown
# Pattern discovery for API endpoints:
1. Grep: "@Get|@Post" → Find all endpoints
2. Read: 5 different controllers
3. Identify pattern:
   - Standard CRUD operations
   - Consistent error handling
   - DTOs for validation
   - AuthGuard on protected routes
4. Document pattern
5. Apply to new endpoint
```

**Avoid**: Assuming first example is the pattern - verify with multiple samples

---

### 3. Dependency Tracing

**Pattern**: Follow the chain of dependencies

**When to use**:
- Understanding how components interact
- Impact analysis before changes
- Finding root causes of issues
- Identifying coupling

**Approach**:
```markdown
1. Start with entry point (endpoint, main function)
2. Trace imports and calls
3. Map dependency chain
4. Identify shared dependencies
5. Document integration points
```

**Tracing techniques**:

**Forward tracing** (what this calls):
```bash
# Starting from UserController
1. Read: user.controller.ts
2. Find: calls to UserService
3. Read: user.service.ts
4. Find: calls to UserRepository, EmailService
5. Continue until reaching database/external APIs
```

**Backward tracing** (what calls this):
```bash
# Starting from UserService
1. Grep: "import.*UserService" → Find all imports
2. Grep: "userService\\." → Find all method calls
3. Map all consumers
4. Understand usage patterns
```

**Benefits**:
- Reveals actual (not just planned) architecture
- Identifies tight coupling
- Assesses change impact
- Finds circular dependencies

**Example**:
```markdown
# Dependency trace for profile update:
ProfileController.updateProfile
  → AuthGuard (dependency)
  → ProfileService.update (calls)
      → ProfileRepository.findById (calls)
      → StorageService.validateImage (calls)
      → ProfileRepository.update (calls)
      → EventEmitter.emit (calls)
          → NotificationService (listener)
          → SearchIndexer (listener)
```

**Avoid**: Stopping at first layer - trace to actual boundaries

---

### 4. Data Flow Analysis

**Pattern**: Follow data transformations through the system

**When to use**:
- Understanding feature behavior
- Debugging data issues
- Planning data migrations
- Optimizing performance

**Approach**:
```markdown
1. Identify entry point (API request, user input)
2. Trace data through each layer
3. Document transformations
4. Identify validation points
5. Map persistence/retrieval
6. Document output format
```

**Analysis framework**:
```markdown
For each data flow:
1. **Input**: Format, source, validation
2. **Transformations**: DTO → Entity → DTO
3. **Business logic**: Rules applied, calculations
4. **Persistence**: Database operations
5. **Side effects**: Events, cache, external calls
6. **Output**: Response format, serialization
```

**Benefits**:
- Reveals data contracts
- Identifies validation layers
- Shows transformation logic
- Exposes side effects

**Example**:
```markdown
# Data flow: Create User
Input:
  POST /api/users
  { email, password, name }
  ↓
Controller:
  Validate against CreateUserDto
  { email: string, password: string, name: string }
  ↓
Service:
  Transform: Hash password
  Enrich: Add createdAt, id (UUID)
  { id, email, hashedPassword, name, createdAt }
  ↓
Repository:
  Insert into users table
  ↓
Side effects:
  - Emit user.created event
  - Send welcome email
  - Cache user profile
  ↓
Output:
  Serialize (hide hashedPassword)
  { id, email, name, createdAt }
```

**Avoid**: Assuming data stays constant - watch for transformations

---

### 5. Architecture Layer Mapping

**Pattern**: Identify and document architectural layers

**When to use**:
- Understanding system architecture
- Ensuring layer separation
- Planning architecture changes
- Code review

**Common architectures to recognize**:

**Layered (N-Tier)**:
```
Presentation Layer (Controllers, API)
       ↓
Business Logic Layer (Services)
       ↓
Data Access Layer (Repositories)
       ↓
Database
```

**Clean Architecture**:
```
External Interfaces (Controllers, UI)
       ↓
Application Layer (Use Cases)
       ↓
Domain Layer (Entities, Business Rules)
       ↓
Infrastructure (Database, External APIs)
```

**Hexagonal (Ports & Adapters)**:
```
Core Domain
  ← Ports (interfaces) →
Adapters (implementations)
```

**Analysis approach**:
```markdown
1. List all directories/modules
2. Identify purpose of each
3. Map dependencies between layers
4. Verify dependencies flow correctly
5. Identify violations (if any)
6. Document architecture pattern
```

**Benefits**:
- Understands intended architecture
- Identifies architecture violations
- Guides new code placement
- Supports refactoring decisions

**Example**:
```markdown
# Architecture mapping
Identified pattern: Layered Architecture

Layer 1: API (controllers/)
  - Depends on: Services
  - Should NOT depend on: Repositories, Database

Layer 2: Business Logic (services/)
  - Depends on: Repositories, Models
  - Should NOT depend on: Controllers, HTTP

Layer 3: Data Access (repositories/)
  - Depends on: Database, Models
  - Should NOT depend on: Services

Layer 4: Models (models/)
  - Depends on: Nothing
  - Pure data structures

Violation found:
  - UserController imports UserRepository directly
  - Should go through UserService
  - Recommendation: Refactor to respect layers
```

**Avoid**: Forcing architecture that doesn't exist - document what IS, not what SHOULD BE

---

### 6. Feature Isolation

**Pattern**: Understand features in isolation before integration

**When to use**:
- Extending existing features
- Microservice extraction
- Feature refactoring
- Understanding complex features

**Approach**:
```markdown
1. Define feature boundaries
2. Find all feature-related files
3. Map feature data models
4. Trace feature data flows
5. Identify external dependencies
6. Document integration points
7. Assess: Can it stand alone?
```

**Isolation analysis**:
```markdown
For each feature:
1. **Files**: List all files belonging to feature
2. **Data**: Models/tables owned by feature
3. **APIs**: Endpoints provided by feature
4. **Dependencies**: What feature needs from outside
5. **Consumers**: What depends on this feature
6. **Coupling level**: Tight, moderate, or loose
```

**Benefits**:
- Clear feature boundaries
- Easier to reason about changes
- Supports microservice extraction
- Identifies coupling issues

**Example**:
```markdown
# Feature isolation: User Profile

Files owned:
  - src/users/profile.service.ts
  - src/users/profile.controller.ts
  - src/users/profile.repository.ts
  - src/models/user-profile.model.ts

Data owned:
  - user_profiles table

APIs provided:
  - GET /api/users/:id/profile
  - PATCH /api/users/:id/profile

Dependencies (tight coupling):
  - User model (1:1 relationship)
  - AuthService (permission checks)
  - StorageService (avatar upload)

Consumers:
  - NotificationService (profile updates)
  - SearchService (profile indexing)

Isolation assessment:
  - Cannot extract as microservice (tight to User)
  - Can refactor internally without affecting consumers
  - Well-defined API boundary
```

**Avoid**: Trying to isolate features that are inherently coupled

---

## Analysis Workflows

### Combining Patterns

Effective analysis combines multiple patterns:

**For new project**:
1. Breadth-first (overview)
2. Architecture layer mapping (structure)
3. Pattern matching (conventions)
4. Feature isolation (understand key features)

**For feature implementation**:
1. Pattern matching (find similar features)
2. Data flow analysis (understand current flows)
3. Dependency tracing (identify integration points)
4. Feature isolation (assess extension points)

**For refactoring**:
1. Feature isolation (define boundaries)
2. Dependency tracing (assess impact)
3. Architecture layer mapping (ensure layering)
4. Data flow analysis (understand transformations)

**For debugging**:
1. Data flow analysis (trace the bug)
2. Dependency tracing (find root cause)
3. Pattern matching (verify expected behavior)

---

## Analysis Best Practices

### Do's

1. **Start broad, go deep** - Breadth-first before deep dives
2. **Follow multiple paths** - Don't rely on single code path
3. **Document as you go** - Don't wait until end
4. **Verify with code** - Read actual implementation
5. **Use multiple techniques** - Combine search, read, trace
6. **Note inconsistencies** - Real codebases have them
7. **Cite evidence** - Always include file paths

### Don'ts

1. **Don't assume uniformity** - Patterns may vary
2. **Don't skip documentation** - It provides context
3. **Don't ignore tests** - Tests reveal contracts
4. **Don't analyze everything** - Focus on relevant areas
5. **Don't trust comments** - Verify with code
6. **Don't work in isolation** - Consider whole system
7. **Don't over-analyze** - Analysis should enable action

### Time Management

Set time boxes based on analysis depth:

- **Quick analysis** (15-20 min): Breadth-first + pattern matching
- **Standard analysis** (30-45 min): Add dependency tracing + data flow
- **Deep analysis** (60-90 min): Add feature isolation + architecture mapping

Stop when you have enough information to proceed - perfect understanding is impossible and unnecessary.

---

## Common Analysis Anti-Patterns

### 1. Random Walk

**Anti-pattern**: Jumping between files without systematic approach

**Problem**: Get lost, miss important code, waste time

**Fix**: Use breadth-first pattern, follow dependency chains

### 2. Analysis Paralysis

**Anti-pattern**: Analyzing everything before starting

**Problem**: Never start implementation, diminishing returns

**Fix**: Set time limits, analyze only what's needed, iterate

### 3. Copy-Pasta Analysis

**Anti-pattern**: Copying first pattern found without verification

**Problem**: Propagate bad patterns, inconsistencies

**Fix**: Use pattern matching on multiple examples

### 4. Documentation Worship

**Anti-pattern**: Trusting docs without verifying code

**Problem**: Docs often outdated, incomplete

**Fix**: Read code as source of truth, docs as guide

### 5. Tunnel Vision

**Anti-pattern**: Only looking at one file/module

**Problem**: Miss dependencies, integration issues

**Fix**: Use dependency tracing, understand context

---

## Tool-Specific Techniques

### Using Grep Effectively

```markdown
**Broad search first**:
Grep: "UserService" (output_mode: files_with_matches)
→ See where it's used

**Then narrow down**:
Grep: "UserService" (path: src/controllers/, output_mode: content)
→ See how controllers use it

**Sample with head_limit**:
Grep: "function.*User" (output_mode: content, head_limit: 20)
→ See pattern without overwhelming results
```

### Using Read Strategically

```markdown
**Read in logical order**:
1. README.md (context)
2. Config files (setup understanding)
3. Entry points (main.ts, app.py)
4. Core models (understand data)
5. Services (understand logic)
6. Tests (understand contracts)

**Don't read sequentially** - prioritize by importance
```

### Using Glob for Discovery

```markdown
**Find patterns**:
Glob: "**/*service*.ts" → Discover services
Glob: "**/*.test.ts" → Find all tests
Glob: "**/models/*.py" → Locate all models

**Understand organization**:
Number of matches reveals architecture
- 50+ services? Likely microservices or large monolith
- Co-located tests? Modern testing approach
- Nested models? Complex domain
```

---

## Summary

Effective analysis requires:
1. **Systematic approach** - Use proven patterns
2. **Right tools** - Grep, Read, Glob strategically
3. **Clear goals** - Know what you need to learn
4. **Time management** - Don't over-analyze
5. **Documentation** - Capture findings
6. **Iteration** - Refine understanding over time

Choose patterns based on your goal, combine as needed, and always balance thoroughness with productivity.
