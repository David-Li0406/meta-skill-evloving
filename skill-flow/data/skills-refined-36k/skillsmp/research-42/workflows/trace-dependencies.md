# Workflow: Trace Dependencies

**Purpose**: Map module dependencies and integration points
**Use for**: Impact analysis, refactoring planning, understanding module relationships
**Estimated time**: 30-45 minutes
**Output**: Dependency map with integration points

## Overview

This workflow systematically traces dependencies between modules, services, and components to understand how code is interconnected. Use this before refactoring to assess impact scope, or when planning integration points for new features.

## Required Tools

- **Grep** - Finding imports, calls, and references
- **Read** - Reading module definitions and exports
- **Glob** - Finding related files
- **Bash** - Directory analysis (optional)

## Dependency Analysis Process

### Phase 1: Module Structure Analysis

#### 1.1 Identify Module Boundaries

Understand how the project is modularized:

```markdown
Search strategy:
1. List top-level directories in src/
2. Identify module/package boundaries
3. Read module exports (index files, __init__.py)
```

**Example searches**:
```bash
# List modules
ls src/
ls src/*/

# Find module entry points
Glob: "**/index.ts"
Glob: "**/__init__.py"

# Read module exports
Read: src/users/index.ts
Read: src/auth/__init__.py
```

**Document**:
```markdown
### Module Structure

**Modules identified**:
- `users` - User management (at src/users/)
- `auth` - Authentication (at src/auth/)
- `products` - Product catalog (at src/products/)
- `shared` - Shared utilities (at src/shared/)

**Module exports**:
- `users` exports: UserService, UserRepository, User (model)
- `auth` exports: AuthService, AuthGuard, JwtStrategy
- `shared` exports: Logger, ValidationPipe, DatabaseModule
```

#### 1.2 Map Entry Points

Identify how modules are initialized:

```markdown
Search strategy:
1. Find main application entry points
2. Find module registration/initialization
3. Identify dependency injection setup
```

**Example searches**:
```bash
# Find entry points
Glob: "**/main.ts"
Glob: "**/app.py"
Glob: "**/__main__.py"

# Find module registration
Grep: "Module|@Module|register" (output_mode: content)

# Read entry points
Read: src/main.ts
```

**Document**:
- Application entry point
- Module initialization order
- Dependency injection container setup

### Phase 2: Import Dependency Analysis

#### 2.1 Map Import Dependencies

Trace import relationships between modules:

```markdown
Search strategy:
1. For each module, find all imports
2. Categorize: internal vs external, cross-module
3. Build dependency graph
```

**Example workflow for a module**:
```bash
# Find all imports in users module
Grep: "^import .* from|^from .* import" (path: src/users/, output_mode: content)

# For TypeScript/JavaScript:
Grep: "^import .* from ['\"](\\.|@)" (path: src/users/, output_mode: content)

# Analyze import sources
# - Relative imports (./): internal to module
# - Cross-module imports (@/other-module, ../other-module): dependencies
# - External imports: third-party libraries
```

**Document for each module**:
```markdown
### users Module Dependencies

**Imports from other modules**:
- `auth` - Uses AuthService for authorization checks
  - `import { AuthService } from '@/auth'` in user.controller.ts
- `shared` - Uses Logger and DatabaseModule
  - `import { Logger } from '@/shared'` in user.service.ts

**Imported by**:
- `products` - ProductService uses UserService
- `orders` - OrderService references User model

**External dependencies**:
- `bcrypt` - Password hashing
- `class-validator` - DTO validation
```

#### 2.2 Create Dependency Graph

Build visual dependency map:

```markdown
Dependency Graph:

┌─────────┐
│  main   │
└────┬────┘
     │
     ├──→ ┌─────────┐
     │    │  auth   │←─────┐
     │    └─────────┘      │
     │                     │
     ├──→ ┌─────────┐      │
     │    │  users  │──────┤ (uses AuthService)
     │    └─────────┘      │
     │         │           │
     │         │           │
     ├──→ ┌─────────┐      │
     │    │products │──────┘ (uses AuthService, UserService)
     │    └─────────┘
     │
     └──→ ┌─────────┐
          │ shared  │←──── (used by all)
          └─────────┘

**Layers**:
- Layer 1 (Foundation): shared
- Layer 2 (Core): auth, users
- Layer 3 (Features): products, orders
- Entry Point: main
```

### Phase 3: Runtime Dependency Analysis

#### 3.1 Service Dependencies

Map service-to-service dependencies:

```markdown
Search strategy:
1. Find all service classes
2. Analyze constructor parameters (dependency injection)
3. Find method calls to other services
```

**Example searches**:
```bash
# Find service constructors
Grep: "constructor\\(" (glob: "**/*service*.ts", output_mode: content)

# Find service injections
Grep: "private.*Service|protected.*Service" (output_mode: content)

# Read service files
Read: src/users/user.service.ts
Read: src/products/product.service.ts
```

**Document**:
```markdown
### Service Dependencies

**UserService** (`src/users/user.service.ts`)
```typescript
constructor(
  private userRepository: UserRepository,
  private authService: AuthService,
  private emailService: EmailService
) {}
```
- **Depends on**: UserRepository, AuthService, EmailService
- **Used by**: ProductService, OrderService

**ProductService** (`src/products/product.service.ts`)
```typescript
constructor(
  private productRepository: ProductRepository,
  private userService: UserService,
  private inventoryService: InventoryService
) {}
```
- **Depends on**: ProductRepository, UserService, InventoryService
- **Used by**: OrderService, CartService
```

#### 3.2 Data Model Dependencies

Map relationships between data models:

```markdown
Search strategy:
1. Find model/entity definitions
2. Identify foreign keys and relationships
3. Map database constraints
```

**Example searches**:
```bash
# Find models
Glob: "**/models/*.ts"
Glob: "**/models/*.py"

# Find relationships
Grep: "@ManyToOne|@OneToMany|@ManyToMany" (output_mode: content)
Grep: "ForeignKey|relationship\\(" (output_mode: content)

# Read model files
Read: src/models/user.model.ts
Read: src/models/product.model.ts
```

**Document**:
```markdown
### Data Model Relationships

**User** ←──→ **UserProfile** (One-to-One)
- User.profileId → UserProfile.id
- Cascade delete: Yes

**User** ←──── **Product** (One-to-Many)
- Product.ownerId → User.id
- A user can own many products

**Product** ←──→ **Category** (Many-to-Many)
- Junction table: product_categories
- product_categories.productId → Product.id
- product_categories.categoryId → Category.id

**Dependency Order** (for migrations):
1. User
2. UserProfile (depends on User)
3. Category
4. Product (depends on User)
5. product_categories (depends on Product, Category)
```

#### 3.3 API Dependencies

Map API endpoint dependencies:

```markdown
Search strategy:
1. Find route/controller definitions
2. Identify which services endpoints call
3. Map authentication/authorization dependencies
```

**Example searches**:
```bash
# Find routes
Glob: "**/routes/*.ts"
Glob: "**/*controller*.ts"

# Find endpoint definitions
Grep: "@Get|@Post|@Put|@Delete|@Patch" (output_mode: content)
Grep: "router.get|router.post" (output_mode: content)

# Read route files
Read: src/routes/user.routes.ts
```

**Document**:
```markdown
### API Endpoint Dependencies

**GET /api/users/:id**
- Controller: UserController.getUser()
- Services: UserService.findById()
- Auth: Requires JWT token
- Dependencies: AuthGuard → UserService → UserRepository

**POST /api/products**
- Controller: ProductController.createProduct()
- Services: ProductService.create(), UserService.findById()
- Auth: Requires JWT + admin role
- Dependencies: AuthGuard → ProductService → ProductRepository + UserService

**Shared Dependencies**:
- All authenticated endpoints depend on AuthGuard
- Most endpoints depend on ValidationPipe
- All endpoints depend on error handling middleware
```

### Phase 4: Integration Point Analysis

#### 4.1 Identify Shared Utilities

Find utilities used across modules:

```markdown
Search strategy:
1. Find shared/common/utils directories
2. Search for import patterns
3. Identify most-used utilities
```

**Example searches**:
```bash
# Find shared utilities
ls src/shared/utils/
Glob: "src/shared/**/*.ts"

# Find usage of specific utility
Grep: "import.*Logger" (output_mode: files_with_matches)
Grep: "import.*ValidationPipe" (output_mode: files_with_matches)
```

**Document**:
```markdown
### Shared Utilities

**Logger** (`src/shared/utils/logger.ts`)
- Used by: All services (20+ files)
- Purpose: Centralized logging
- Dependencies: winston library

**ValidationPipe** (`src/shared/pipes/validation.pipe.ts`)
- Used by: All controllers (15+ files)
- Purpose: DTO validation
- Dependencies: class-validator

**DatabaseModule** (`src/shared/database/database.module.ts`)
- Used by: All repositories
- Purpose: Database connection management
- Dependencies: TypeORM/Prisma
```

#### 4.2 Identify Circular Dependencies

Detect circular dependency issues:

```markdown
Search strategy:
1. Build import graph
2. Identify circular references
3. Suggest refactoring if needed
```

**Analysis approach**:
```markdown
For each module:
1. List all imports
2. For each imported module, check if it imports back
3. Flag circular dependencies

Example circular dependency:
- users/user.service.ts imports products/product.service.ts
- products/product.service.ts imports users/user.service.ts
→ CIRCULAR DEPENDENCY DETECTED
```

**Document**:
```markdown
### Circular Dependencies

**Issue 1**: users ↔ products
- `UserService` imports `ProductService`
- `ProductService` imports `UserService`
- **Resolution**: Extract shared types to separate module

**Issue 2**: auth ↔ users
- `AuthService` imports `User` model
- `UserService` imports `AuthService`
- **Resolution**: OK - model import is not circular (only type, not service)
```

#### 4.3 External Dependency Analysis

Map external library usage:

```markdown
Search strategy:
1. Read package.json / pyproject.toml
2. Find where each major library is used
3. Identify version constraints
```

**Example**:
```bash
# Read dependency file
Read: package.json

# Find usage of specific library
Grep: "import.*express" (output_mode: files_with_matches)
Grep: "from fastapi import" (output_mode: files_with_matches)
```

**Document**:
```markdown
### External Dependencies

**Production Dependencies**:
| Library | Version | Used In | Purpose |
|---------|---------|---------|---------|
| express | ^4.18.0 | main.ts, middleware/ | Web framework |
| typeorm | ^0.3.0 | repositories/, models/ | ORM |
| bcrypt | ^5.1.0 | auth/auth.service.ts | Password hashing |

**Critical Dependencies** (used in 10+ files):
- `class-validator` - DTO validation
- `class-transformer` - Object mapping
- `winston` - Logging

**Upgrade Risks**:
- TypeORM upgrade may break repository layer (23 files affected)
```

### Phase 5: Impact Analysis

#### 5.1 Change Impact Assessment

For a specific change, assess impact scope:

```markdown
Workflow:
1. Identify module/file to change
2. Find all direct imports of this module
3. Find all services/controllers using it
4. Estimate testing scope
```

**Example - Changing UserService**:
```bash
# Find direct imports
Grep: "import.*UserService" (output_mode: files_with_matches)

# Find indirect usage (through other services)
# - ProductService uses UserService
# - OrderService uses ProductService
# → OrderService is indirectly affected
```

**Document**:
```markdown
### Impact Analysis: Modifying UserService

**Direct impact** (9 files):
- `src/users/user.controller.ts` - API endpoints
- `src/products/product.service.ts` - User lookup
- `src/orders/order.service.ts` - User validation
- `src/auth/auth.service.ts` - User authentication
- ... (5 more files)

**Indirect impact** (15 files):
- Any service using ProductService or OrderService
- All API endpoints using affected controllers

**Testing scope**:
- Unit tests: UserService (src/users/user.service.test.ts)
- Integration tests: All endpoints using UserService (9 test files)
- E2E tests: User flows, product flows, order flows

**Database impact**:
- If changing User model: Migration required
- Affects: users table, related foreign keys
```

## Output Format

Create dependency analysis document:

```markdown
# Dependency Analysis: {Project/Module Name}

**Date**: {YYYY-MM-DD}
**Scope**: {What was analyzed}
**Purpose**: {Why this analysis was done}

## Module Structure

{Module boundaries and exports}

## Dependency Graph

{Visual dependency map}

## Module Dependencies

### {Module Name}

**Imports from other modules**:
- {module} - {what it uses}

**Imported by**:
- {module} - {what they use from this module}

**External dependencies**:
- {library} - {purpose}

{Repeat for each module}

## Service Dependencies

{Service-to-service dependency map}

## Data Model Relationships

{Model relationship diagram and descriptions}

## API Dependencies

{Endpoint dependency map}

## Shared Utilities

{Cross-cutting utilities and their usage}

## Issues Identified

### Circular Dependencies
{Any circular dependencies found}

### Tight Coupling
{Areas of high coupling}

### Recommendations
{Suggestions for improvement}

## Impact Analysis

{If analyzing for specific change}

**Direct impact**: {files}
**Indirect impact**: {files}
**Testing scope**: {what to test}

## Summary

**Module count**: {number}
**Total dependencies**: {number}
**Circular dependencies**: {number}
**Complexity assessment**: {Low/Medium/High}
```

## Success Criteria

Dependency analysis is complete when:
- [ ] Module boundaries identified and documented
- [ ] Import dependencies mapped for key modules
- [ ] Dependency graph created
- [ ] Service dependencies documented
- [ ] Data model relationships mapped
- [ ] API dependencies traced
- [ ] Shared utilities identified
- [ ] Circular dependencies detected (if any)
- [ ] External dependencies cataloged
- [ ] Impact analysis completed (if applicable)

## Tips & Best Practices

### Do's
1. **Start with high-level** - Module dependencies before file-level
2. **Use visual diagrams** - Graphs communicate better than lists
3. **Identify patterns** - Look for layered architecture, dependency injection
4. **Note coupling levels** - Flag tight coupling for potential refactoring
5. **Document bidirectional** - Show both "imports" and "imported by"

### Don'ts
1. **Don't analyze everything** - Focus on relevant modules
2. **Don't ignore external deps** - They matter for upgrades
3. **Don't skip circular detection** - Circular deps cause issues
4. **Don't forget data dependencies** - Database relationships matter too
5. **Don't overlook runtime deps** - DI and service calls, not just imports

### Analysis Depth

**Quick analysis** (15-20 min):
- Module structure only
- High-level dependency graph
- Critical shared utilities

**Standard analysis** (30-45 min):
- Module + service dependencies
- Data model relationships
- Circular dependency detection

**Deep analysis** (60+ min):
- Full dependency graph
- Impact analysis for specific changes
- Refactoring recommendations

### Common Patterns

**Layered Architecture**:
```
Presentation (Controllers) → Business (Services) → Data (Repositories)
```

**Dependency Injection**:
- Services injected via constructors
- Managed by DI container

**Repository Pattern**:
- Services depend on repositories
- Repositories depend on ORM/database

## Related Workflows

- Use **analyze-codebase** for initial context
- Use **understand-feature** to see dependencies in practice
- Use **find-patterns** to understand architecture patterns
- Output informs refactoring and architecture decisions

## Related Context Files

- `../context/analysis-patterns.md` - Dependency analysis techniques
- `../context/search-strategies.md` - Finding imports and references
- `../context/documentation-standards.md` - Dependency map formatting
