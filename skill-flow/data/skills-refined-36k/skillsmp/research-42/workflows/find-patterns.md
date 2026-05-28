# Workflow: Find Patterns

**Purpose**: Discover and document code patterns and naming conventions
**Use for**: Understanding implementation patterns, ensuring consistency, learning project style
**Estimated time**: 20-40 minutes
**Output**: Pattern catalog with examples

## Overview

This workflow systematically discovers patterns in a codebase including naming conventions, architectural patterns, code organization, and implementation approaches. Use this when you need to understand how to implement features consistently with existing code.

## Required Tools

- **Grep** - Pattern searching across codebase
- **Glob** - File pattern discovery
- **Read** - Reading example files
- **Bash** - Directory analysis (optional)

## Pattern Discovery Process

### Phase 1: Naming Convention Patterns

#### 1.1 File Naming Patterns

Discover how files are named:

```markdown
Search strategy:
1. List files in key directories
2. Identify patterns (extensions, suffixes, case style)
3. Read examples to confirm conventions
```

**Example searches**:
```bash
# Source files
Glob: "src/**/*.ts"
Glob: "src/**/*.py"
Glob: "src/**/*.js"

# Analyze results for patterns:
# - kebab-case.ts
# - PascalCase.tsx
# - snake_case.py
```

**Patterns to identify**:
- **Case style**: kebab-case, PascalCase, snake_case, camelCase
- **Suffixes**: .service.ts, .model.py, .component.tsx, .test.js
- **Prefixes**: use-*, with-*, I* (interfaces)
- **Structure**: feature/module grouping

**Document**:
```markdown
### File Naming Conventions

**Source files**:
- TypeScript: `kebab-case.ts` (e.g., `user-service.ts`)
- Components: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- Python: `snake_case.py` (e.g., `user_service.py`)

**Test files**:
- Pattern: `{name}.test.ts` or `test_{name}.py`
- Location: Co-located with source OR tests/ directory

**Examples**:
- `src/services/user-service.ts`
- `src/components/UserProfile.tsx`
- `src/models/user_model.py`
```

#### 1.2 Function/Method Naming Patterns

Discover how functions and methods are named:

```markdown
Search strategy:
1. Search for function definitions
2. Search for method definitions
3. Identify patterns in naming and parameters
```

**Example searches**:
```bash
# JavaScript/TypeScript functions
Grep: "function \w+|const \w+ = " (output_mode: content, head_limit: 50)
Grep: "export function \w+" (output_mode: content)

# Python functions
Grep: "def \w+\(" (output_mode: content, head_limit: 50)
Grep: "async def \w+\(" (output_mode: content)

# Method definitions
Grep: "^\s+\w+\s*\(" (output_mode: content)
```

**Patterns to identify**:
- **Case style**: camelCase, snake_case
- **Prefixes**: get*, set*, is*, has*, create*, update*, delete*
- **Async patterns**: async/await usage
- **Parameter patterns**: destructuring, type annotations

**Document**:
```markdown
### Function/Method Naming

**Pattern**: camelCase for JavaScript/TypeScript, snake_case for Python

**Common prefixes** (examples from codebase):
- `get*` - Retrieval: `getUserById(id: string)`
- `create*` - Creation: `createUser(data: UserData)`
- `update*` - Updates: `updateUserProfile(id, updates)`
- `delete*` - Deletion: `deleteUser(id: string)`
- `is*`/`has*` - Boolean checks: `isAuthenticated()`, `hasPermission()`
- `handle*` - Event handlers: `handleSubmit(event)`

**Examples**:
```typescript
// From src/services/user-service.ts
async function getUserById(id: string): Promise<User>
async function createUser(data: CreateUserDto): Promise<User>
function isValidEmail(email: string): boolean
```
```

#### 1.3 Class/Type Naming Patterns

Discover class and type naming conventions:

```markdown
Search strategy:
1. Search for class definitions
2. Search for interface/type definitions
3. Identify patterns and suffixes
```

**Example searches**:
```bash
# Class definitions
Grep: "class \w+" (output_mode: content, head_limit: 50)
Grep: "export class \w+" (output_mode: content)

# TypeScript interfaces/types
Grep: "interface \w+" (output_mode: content, head_limit: 50)
Grep: "type \w+ = " (output_mode: content, head_limit: 50)

# Python classes
Grep: "class \w+\(" (output_mode: content, head_limit: 50)
```

**Patterns to identify**:
- **Case style**: PascalCase
- **Suffixes**: Service, Repository, Controller, Model, Dto, Interface
- **Prefixes**: I* (interfaces), Base*, Abstract*
- **Generics**: Usage of type parameters

**Document**:
```markdown
### Class/Type Naming

**Pattern**: PascalCase

**Suffixes by purpose**:
- `*Service` - Business logic: `UserService`, `AuthService`
- `*Repository` - Data access: `UserRepository`
- `*Controller` - API handlers: `UserController`
- `*Model` - Data models: `UserModel`
- `*Dto` - Data transfer objects: `CreateUserDto`, `UpdateUserDto`
- `*Interface` or `I*` - Interfaces: `IUserService` or `UserInterface`

**Examples**:
```typescript
// From src/services/
export class UserService implements IUserService { }

// From src/models/
export interface User {
  id: string;
  email: string;
}

// From src/dto/
export class CreateUserDto {
  email: string;
  password: string;
}
```
```

#### 1.4 Database Naming Patterns

Discover database naming conventions:

```markdown
Search strategy:
1. Search for table/model definitions
2. Search for column definitions
3. Identify SQL queries for naming
```

**Example searches**:
```bash
# ORM Models
Grep: "@Table|__tablename__|table_name" (output_mode: content)
Grep: "@Column|Column\(" (output_mode: content, head_limit: 30)

# SQL queries
Grep: "CREATE TABLE|INSERT INTO|SELECT.*FROM" (output_mode: content)
```

**Patterns to identify**:
- **Table names**: snake_case, plural vs singular
- **Column names**: snake_case
- **Primary keys**: id, uuid, {table}_id
- **Foreign keys**: {related_table}_id
- **Timestamps**: created_at, updated_at

**Document**:
```markdown
### Database Naming

**Tables**: `snake_case` plural (e.g., `users`, `user_profiles`)
**Columns**: `snake_case` (e.g., `first_name`, `email_address`)
**Primary keys**: `id` (auto-increment) or `uuid`
**Foreign keys**: `{table}_id` (e.g., `user_id`, `organization_id`)
**Timestamps**: `created_at`, `updated_at`, `deleted_at` (soft deletes)

**Examples**:
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_profiles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  display_name VARCHAR(100)
);
```
```

#### 1.5 API Endpoint Patterns

Discover API naming and structure:

```markdown
Search strategy:
1. Search for route definitions
2. Search for API path strings
3. Identify versioning and structure
```

**Example searches**:
```bash
# Express/FastAPI routes
Grep: "@app.route|@router.get|@router.post|app.get|app.post" (output_mode: content)
Grep: '"/api/' (output_mode: content)

# Path parameters
Grep: "/:id|/{id}|/:userId|/{user_id}" (output_mode: content)
```

**Patterns to identify**:
- **Base path**: /api, /v1, /api/v1
- **Resource naming**: plural vs singular, kebab-case vs snake_case
- **Versioning**: path-based, header-based
- **Path parameters**: :id vs {id}
- **Query parameters**: conventions for filtering, pagination

**Document**:
```markdown
### API Endpoint Naming

**Structure**: `/api/v1/{resource}/{id?}/{action?}`

**Conventions**:
- **Base**: `/api/v1/`
- **Resources**: plural, kebab-case (e.g., `/api/v1/user-profiles`)
- **IDs**: UUID or numeric: `/api/v1/users/123`
- **Actions**: Verb for non-REST: `/api/v1/users/123/reset-password`

**HTTP Methods**:
- `GET /api/v1/users` - List users
- `GET /api/v1/users/:id` - Get single user
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/:id` - Update user (full)
- `PATCH /api/v1/users/:id` - Update user (partial)
- `DELETE /api/v1/users/:id` - Delete user

**Examples**:
```typescript
// From src/routes/user.routes.ts
router.get('/api/v1/users', getUsers);
router.post('/api/v1/users', createUser);
router.put('/api/v1/users/:id', updateUser);
router.delete('/api/v1/users/:id', deleteUser);
```
```

### Phase 2: Architectural Patterns

#### 2.1 Service Layer Pattern

Discover how services are structured:

```markdown
Search strategy:
1. Find service files
2. Read representative services
3. Identify common patterns
```

**Example searches**:
```bash
# Find services
Glob: "**/*service*.ts"
Glob: "**/*service*.py"

# Read examples
Read: src/services/user-service.ts
Read: src/services/auth-service.ts
```

**Patterns to identify**:
- **Class vs function** based services
- **Dependency injection** patterns
- **Error handling** approaches
- **Async patterns**
- **Method organization**

**Document**:
```markdown
### Service Layer Pattern

**Structure**: Class-based services with dependency injection

**Common pattern**:
```typescript
// Service class structure
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    // 1. Validation
    // 2. Business logic
    // 3. Repository call
    // 4. Side effects (emails, events)
    // 5. Return result
  }
}
```

**Conventions**:
- One service per domain/feature
- Services injected into controllers
- Services call repositories for data
- Services contain business logic
```

#### 2.2 Repository Pattern

Discover data access patterns:

```markdown
Search strategy:
1. Find repository files
2. Read representative repositories
3. Identify ORM usage patterns
```

**Example searches**:
```bash
# Find repositories
Glob: "**/*repository*.ts"
Glob: "**/*repo*.py"

# Read examples
Read: src/repositories/user-repository.ts
```

**Document**:
```markdown
### Repository Pattern

**Structure**: Class-based repositories wrapping ORM

**Common pattern**:
```typescript
export class UserRepository {
  async findById(id: string): Promise<User | null> {
    return await db.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserData): Promise<User> {
    return await db.user.create({ data });
  }
}
```

**Conventions**:
- One repository per model/entity
- Standard methods: findById, findAll, create, update, delete
- Repositories don't contain business logic
- Return domain models, not ORM objects
```

#### 2.3 Controller Pattern

Discover API controller/route patterns:

```markdown
Search strategy:
1. Find controller/route files
2. Read representative controllers
3. Identify request/response patterns
```

**Example searches**:
```bash
# Find controllers
Glob: "**/*controller*.ts"
Glob: "**/*routes*.py"

# Read examples
Read: src/controllers/user-controller.ts
```

**Document**:
```markdown
### Controller/Route Pattern

**Structure**: Thin controllers delegating to services

**Common pattern**:
```typescript
export class UserController {
  constructor(private userService: UserService) {}

  async createUser(req: Request, res: Response) {
    try {
      // 1. Validate request (may use middleware)
      const data = validateCreateUserDto(req.body);

      // 2. Delegate to service
      const user = await this.userService.createUser(data);

      // 3. Return response
      return res.status(201).json(user);
    } catch (error) {
      // 4. Error handling
      return handleError(error, res);
    }
  }
}
```

**Conventions**:
- Controllers are thin - just request/response handling
- Business logic in services
- Validation via middleware or DTOs
- Consistent error handling
```

### Phase 3: Code Organization Patterns

#### 3.1 Directory Organization

Analyze how code is grouped:

```markdown
Patterns to identify:
- Feature-based organization (by domain)
- Layer-based organization (by type)
- Hybrid approach
```

**Example analysis**:
```bash
# List directories to see organization
ls src/
ls src/*/
```

**Document**:
```markdown
### Directory Organization

**Pattern**: Feature-based with layer subdirectories

**Structure**:
```
src/
├── users/              # Feature: Users
│   ├── user.service.ts
│   ├── user.repository.ts
│   ├── user.controller.ts
│   └── user.model.ts
├── auth/               # Feature: Authentication
│   ├── auth.service.ts
│   ├── auth.controller.ts
│   └── strategies/
└── shared/             # Shared utilities
    ├── utils/
    └── middlewares/
```

**Co-location**:
- Related files grouped by feature
- Tests co-located or mirrored in tests/
- Shared code in shared/ or utils/
```

#### 3.2 Import Patterns

Discover import/export conventions:

```markdown
Search strategy:
1. Search for import statements
2. Identify patterns (absolute vs relative, barrel exports)
```

**Example searches**:
```bash
# Import patterns
Grep: "^import .* from" (output_mode: content, head_limit: 50)

# Barrel exports (index files)
Glob: "**/index.ts"
Read: src/services/index.ts
```

**Document**:
```markdown
### Import/Export Patterns

**Import style**: Path aliases for cleaner imports

**Pattern**:
```typescript
// Absolute imports via path alias (preferred)
import { UserService } from '@/services';
import { User } from '@/models';

// Relative imports (for nearby files)
import { validateUser } from './validators';

// Barrel exports in index.ts
export * from './user.service';
export * from './auth.service';
```

**Path aliases** (from tsconfig.json):
```json
{
  "@/": "./src/",
  "@services/": "./src/services/",
  "@models/": "./src/models/"
}
```
```

### Phase 4: Implementation Patterns

#### 4.1 Error Handling

Discover error handling approaches:

```markdown
Search strategy:
1. Search for error classes
2. Search for try-catch patterns
3. Search for error middleware
```

**Example searches**:
```bash
# Error classes
Grep: "class \w+Error extends" (output_mode: content)

# Error handling
Grep: "try \{|catch \(" (output_mode: content, head_limit: 30)
Grep: "throw new" (output_mode: content, head_limit: 30)
```

**Document error patterns found**

#### 4.2 Testing Patterns

Discover testing conventions:

```markdown
Search strategy:
1. Search for test files
2. Read representative tests
3. Identify patterns (AAA, mocking, fixtures)
```

**Example searches**:
```bash
# Find tests
Glob: "**/*.test.ts"
Glob: "**/test_*.py"

# Read examples
Read: src/services/user-service.test.ts
```

**Document testing patterns found**

#### 4.3 Async Patterns

Discover async/await usage:

```markdown
Search strategy:
1. Search for async functions
2. Identify promise handling patterns
3. Check for Promise.all usage
```

**Document async patterns found**

## Output Format

Create pattern catalog:

```markdown
# Code Pattern Catalog: {Project Name}

**Date**: {YYYY-MM-DD}
**Scope**: {Areas analyzed}

## Naming Conventions

### Files
{patterns with examples}

### Functions/Methods
{patterns with examples}

### Classes/Types
{patterns with examples}

### Database
{patterns with examples}

### API Endpoints
{patterns with examples}

## Architectural Patterns

### Service Layer
{pattern description with examples}

### Repository Layer
{pattern description with examples}

### Controller Layer
{pattern description with examples}

## Code Organization

### Directory Structure
{pattern with examples}

### Import/Export
{pattern with examples}

## Implementation Patterns

### Error Handling
{pattern with examples}

### Testing
{pattern with examples}

### Async/Await
{pattern with examples}

## Summary & Recommendations

**Consistency**: {level of consistency observed}
**Recommendations**: {how to match these patterns}
**Exceptions**: {any anti-patterns or inconsistencies noted}
```

## Success Criteria

Pattern discovery is complete when:
- [ ] File naming patterns documented with examples
- [ ] Function/method naming patterns documented
- [ ] Class/type naming patterns documented
- [ ] Database naming patterns documented (if applicable)
- [ ] API endpoint patterns documented (if applicable)
- [ ] Architectural patterns identified and documented
- [ ] Code organization patterns understood
- [ ] Implementation patterns cataloged
- [ ] Examples cited from actual codebase
- [ ] Inconsistencies noted

## Tips & Best Practices

### Do's
1. **Search broadly first** - Use head_limit to sample patterns
2. **Cite real examples** - Copy actual code snippets
3. **Note exceptions** - Document when patterns vary
4. **Be specific** - "camelCase for functions" not just "consistent naming"
5. **Focus on what matters** - Prioritize patterns you'll use

### Don'ts
1. **Don't assume uniformity** - Projects often have mixed patterns
2. **Don't document everything** - Focus on relevant patterns
3. **Don't rely on one example** - Verify patterns across multiple files
4. **Don't ignore context** - Some patterns are framework-specific

### Search Strategy Tips
- Use **Grep with head_limit** to sample without overwhelming results
- Use **Glob** to discover file organization
- Use **Read** on representative files for deeper understanding
- Search **incrementally** - refine based on results

## Related Workflows

- Use **analyze-codebase** for comprehensive context before pattern discovery
- Use **understand-feature** to see patterns in practice
- Output feeds into coding standards documentation

## Related Context Files

- `../context/search-strategies.md` - Search techniques
- `../context/analysis-patterns.md` - Analysis methodologies
- `../context/documentation-standards.md` - Documentation formatting
