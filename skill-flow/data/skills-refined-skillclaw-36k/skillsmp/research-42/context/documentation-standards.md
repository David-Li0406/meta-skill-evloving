# Documentation Standards

This document defines standards and templates for documenting research findings. Follow these guidelines to create clear, actionable, and reproducible research documentation.

## Overview

Good research documentation:
- Enables others to understand your findings quickly
- Provides evidence for conclusions
- Supports decision-making with clear recommendations
- Can be reproduced by others following your methodology
- Serves as reference for future work

---

## Core Principles

### 1. Evidence-Based Documentation

**Always cite sources**:
```markdown
❌ Bad: "Services use dependency injection"

✅ Good: "Services use dependency injection (see UserService at src/services/user.service.ts, lines 15-20)"
```

**Include code examples**:
```markdown
❌ Bad: "Functions are named using camelCase"

✅ Good:
Functions use camelCase naming:
```typescript
// From src/utils/validation.ts
function validateEmail(email: string): boolean { }
function parseUserInput(input: string): Data { }
```
```

**Cite file paths**:
- Use absolute paths from project root: `/src/services/user.service.ts`
- Or relative paths with clear root: `src/services/user.service.ts` (from project root)
- Include line numbers for precision: `src/models/user.ts:45-67`

### 2. Actionable Recommendations

**Be specific**:
```markdown
❌ Bad: "Follow existing patterns"

✅ Good: "Use the service pattern found in src/services/user.service.ts:
1. Class-based with dependency injection
2. Constructor injects repository and dependencies
3. Public methods for business operations
4. Private methods for internal logic"
```

**Provide next steps**:
```markdown
❌ Bad: "Integration points identified"

✅ Good:
Integration points:
1. UserService.findById() at src/services/user.service.ts:34
   - Call this to retrieve user data
   - Returns Promise<User | null>
   - Handles not-found internally

2. AuthService.validateToken() at src/auth/auth.service.ts:67
   - Use this for permission checks
   - Throws UnauthorizedException on failure
```

### 3. Structured Information

**Use consistent formatting**:
- Tables for comparisons
- Lists for sequences/enumerations
- Code blocks for examples
- Diagrams for relationships
- Headers for organization

**Hierarchy matters**:
```markdown
# Main Topic
## Category
### Specific Item
#### Detail
```

### 4. Reproducibility

**Document your methodology**:
```markdown
## Analysis Method

1. Searched for all service files: `Glob: "**/*service*.ts"`
2. Read 3 representative services:
   - src/services/user.service.ts
   - src/services/product.service.ts
   - src/auth/auth.service.ts
3. Identified common patterns
4. Verified pattern across remaining services
```

**Include search commands**:
```markdown
To reproduce this analysis:
```bash
# Find all services
Glob: "**/*service*.ts"

# Read examples
Read: src/services/user.service.ts

# Find usage
Grep: "import.*UserService" (output_mode: files_with_matches)
```
```

---

## Document Templates

### Template: Research Report (Comprehensive)

```markdown
# Project Research Report: {Feature/Project Name}

**Date**: {YYYY-MM-DD}
**Researcher**: {agent-name or your-name}
**Feature Context**: {What you're researching for}
**Repository**: {URL or path}

## Executive Summary

{2-3 sentences summarizing key findings and primary recommendation}

**Key Findings**:
- {Finding 1}
- {Finding 2}
- {Finding 3}

**Primary Recommendation**: {Main actionable recommendation}

---

## Project Structure

### Directory Organization

{Description of how project is organized - feature-based, layer-based, etc.}

```
src/
├── feature1/
│   ├── service.ts
│   └── model.ts
├── feature2/
└── shared/
```

### Key Directories for This Feature

| Directory | Purpose | Relevance |
|-----------|---------|-----------|
| `src/users/` | User management | Contains similar profile feature |
| `src/auth/` | Authentication | Integration needed for permissions |
| `src/shared/` | Shared utilities | Reusable validation functions |

---

## Coding Standards

### Naming Conventions

**Files**: `{pattern}` (e.g., kebab-case.ts)
- Example: `user-profile.service.ts`, `create-user.dto.ts`

**Functions**: `{pattern}` (e.g., camelCase)
- Example: `getUserById()`, `validateEmail()`
- Prefixes: `get*`, `create*`, `update*`, `delete*`, `is*`, `has*`

**Classes**: `{pattern}` (e.g., PascalCase)
- Example: `UserService`, `CreateUserDto`, `UserProfileModel`
- Suffixes: `*Service`, `*Repository`, `*Controller`, `*Dto`, `*Model`

**Database**: `{pattern}` (e.g., snake_case)
- Tables: `users`, `user_profiles` (plural, snake_case)
- Columns: `user_id`, `created_at` (snake_case)
- Foreign keys: `{table}_id`

**API Endpoints**: `{pattern}`
- Structure: `/api/v1/{resource}/{id?}/{action?}`
- Example: `/api/v1/users/:id`, `/api/v1/users/:id/reset-password`

### Code Style

**Linting**: {Tool and config}
- Tool: ESLint / Ruff / etc.
- Config: `.eslintrc.json` / `ruff.toml`
- Key rules: {notable rules}

**Formatting**: {Tool and config}
- Tool: Prettier / Black
- Line length: {number}
- Trailing commas: yes/no

**Documentation**: {Standard}
- Style: JSDoc / docstrings / etc.
- Required for: Public APIs, complex logic
- Example:
```typescript
/**
 * Retrieves user by ID
 * @param id - User UUID
 * @returns User object or null if not found
 * @throws DatabaseException if connection fails
 */
async getUserById(id: string): Promise<User | null> { }
```

### Testing Standards

**Framework**: {Jest/Pytest/etc.}
**Coverage Requirements**: {percentage if specified}
**Test Organization**: {pattern}

- Unit tests: `{pattern}` (e.g., co-located as `*.test.ts`)
- Integration tests: `{pattern}` (e.g., `tests/integration/`)
- E2E tests: `{pattern}` (e.g., `tests/e2e/`)

---

## Technology Stack

### Backend

| Layer | Technology | Version | Usage Pattern |
|-------|------------|---------|---------------|
| Framework | {e.g., FastAPI} | {0.100.0} | Async endpoints with dependency injection |
| ORM | {e.g., SQLAlchemy} | {2.0} | Declarative models, async queries |
| Database | {e.g., PostgreSQL} | {15} | Via Supabase/direct connection |
| Auth | {e.g., JWT} | {pyjwt 2.8} | Token-based authentication |

### Frontend

| Layer | Technology | Version | Usage Pattern |
|-------|------------|---------|---------------|
| Framework | {e.g., Vue 3} | {3.3} | Composition API, TypeScript |
| State | {e.g., Pinia} | {2.1} | Store modules per feature |
| Styling | {e.g., Tailwind} | {3.3} | Utility-first, custom design system |
| Components | {e.g., Radix} | {1.0} | Headless UI components |

### DevOps

| Component | Technology | Notes |
|-----------|------------|-------|
| CI/CD | {e.g., GitHub Actions} | Workflows in `.github/workflows/` |
| Containers | {e.g., Docker} | `Dockerfile` at root |
| Deployment | {e.g., Vercel/AWS} | {deployment details} |

---

## Related Existing Features

### Similar Implementations Found

#### {Feature 1 Name}

**Location**: `{file path}`

**Pattern**:
{Description of how it's implemented}

```typescript
// Example code from implementation
class ExampleService {
  // Pattern demonstrated
}
```

**Relevance**: {Why this matters for new feature}

**Reusable components**:
- `{Component/Function}` at `{path}` - {what it does}

#### {Feature 2 Name}

{Same structure as above}

### Extension vs. New Code Analysis

| Existing Code | Extend? | Rationale |
|---------------|---------|-----------|
| `UserService` | No | Already handles too much (SRP violation) |
| `AuthMiddleware` | Yes | Has plugin pattern designed for extension |
| `ValidationPipe` | Yes | Reusable across features |

---

## Integration Points

### Services to Integrate With

**{ServiceName}** (`{path}`)
- **What it provides**: {description}
- **How to use**: {method calls, examples}
- **Integration needed**: {what you'll need to do}

Example:
```typescript
// From src/services/email.service.ts
await this.emailService.sendWelcomeEmail(user.email, user.name);
```

### Shared Utilities Available

**{UtilityName}** (`{path}`)
- **Purpose**: {what it does}
- **Usage**: {how to use it}

### Database Relationships

**Existing tables**:
- `{table_name}` - {how new feature relates}
  - Relationship: {1:1, 1:N, N:M}
  - Foreign key: `{column_name}`

**New tables needed**:
- `{table_name}` - {purpose}

---

## Recommendations

### Do's

1. **{Specific recommendation}**
   - Rationale: {why}
   - Example: {code or reference}

2. **{Another recommendation}**
   - Found in: {where in codebase}
   - Approach: {how to do it}

### Don'ts

1. **{Anti-pattern to avoid}**
   - Why not: {reasoning}
   - Instead: {alternative}

2. **{Another thing to avoid}**
   - Reason: {why it's problematic}

### Files Likely to Create/Modify

**New Files** (create these):
```
src/
├── feature-name/
│   ├── feature.service.ts - Business logic
│   ├── feature.repository.ts - Data access
│   ├── feature.controller.ts - API endpoints
│   ├── feature.model.ts - Data model
│   └── dto/
│       ├── create-feature.dto.ts
│       └── update-feature.dto.ts
tests/
├── unit/
│   └── feature.service.test.ts
└── integration/
    └── feature-api.test.ts
```

**Modified Files** (update these):
- `{path}` - {what changes needed}
- `{path}` - {what changes needed}

---

## Open Questions

1. **{Question requiring team input}**
   - Context: {background}
   - Options: {possible approaches}
   - Recommendation: {your suggestion}

2. **{Technical decision needed}**
   - Trade-offs: {list}
   - Impact: {scope}

---

## References

**Documentation**:
- Project README: `{path}`
- Architecture docs: `{path}`
- Coding standards: `{path}`

**Related Features**:
- {Feature name}: `{path}`

**External Resources**:
- {Library docs}: {URL}
- {Related article}: {URL}

---

## Appendix

### Search Commands Used

```bash
# Project structure
ls src/
Glob: "**/*service*.ts"

# Pattern discovery
Grep: "class \w+Service" (output_mode: content, head_limit: 10)

# Feature analysis
Read: src/services/user.service.ts
Grep: "import.*UserService" (output_mode: files_with_matches)
```

### Analysis Metadata

- Time spent: {hours}
- Files analyzed: {count}
- Services reviewed: {count}
- Test coverage reviewed: Yes/No
```

---

### Template: Pattern Catalog (Focused)

```markdown
# Code Pattern Catalog: {Project Name}

**Date**: {YYYY-MM-DD}
**Scope**: {What patterns were analyzed}

## Naming Conventions

### File Naming

**Pattern**: {description}

**Examples**:
- `user-profile.service.ts` - Service files
- `CreateUserDto.ts` - DTO classes
- `user.test.ts` - Test files

**Rule**: {specific rule}

### {Other naming categories...}

## Architectural Patterns

### {Pattern Name} (e.g., Service Layer Pattern)

**Structure**:
```typescript
// Standard service structure
export class FeatureService {
  constructor(
    private repository: FeatureRepository,
    private dependency: OtherService
  ) {}

  async method(): Promise<Result> {
    // Business logic
  }
}
```

**Key characteristics**:
- {characteristic 1}
- {characteristic 2}

**Found in**:
- `src/services/user.service.ts`
- `src/services/product.service.ts`
- `src/services/order.service.ts`

**When to use**: {guidance}

## Implementation Patterns

### {Pattern Name}

{Same structure as architectural patterns}

## Consistency Assessment

**Overall**: {High/Medium/Low}

**Strengths**:
- {What's consistently done well}

**Weaknesses**:
- {Where patterns vary}

**Recommendations**:
- {How to maintain consistency}
```

---

### Template: Dependency Analysis (Technical)

```markdown
# Dependency Analysis: {Module/Feature Name}

**Date**: {YYYY-MM-DD}
**Scope**: {What was analyzed}
**Purpose**: {Why - e.g., impact analysis for refactoring}

## Module Dependencies

### {Module Name}

**Depends on** (imports from):
- `{module}` - {what it uses}
  - Example: `import { UserService } from '@/users'`
  - Used in: {file}:{line}

**Used by** (imported by):
- `{module}` - {what they use}
  - Example: `import { ProductService } from '@/products'`
  - Files: {count} files

**External dependencies**:
- `{library}` - {purpose}

## Dependency Graph

```
┌──────────┐
│   main   │
└────┬─────┘
     │
     ├──→ ┌──────────┐
     │    │   auth   │←────┐
     │    └──────────┘     │
     │                     │
     ├──→ ┌──────────┐     │
     │    │  users   │─────┘ (uses auth)
     │    └──────────┘
     │         │
     ├──→ ┌──────────┐
          │ products │───→ (uses users)
          └──────────┘
```

**Layers**:
- Layer 1 (Foundation): {modules}
- Layer 2 (Core): {modules}
- Layer 3 (Features): {modules}

## Circular Dependencies

**Found**: {Yes/No}

{If yes, list them:}
- `{module A}` ↔ `{module B}`
  - A imports B: {file}:{line}
  - B imports A: {file}:{line}
  - **Resolution**: {recommendation}

## Impact Analysis

**If modifying {module}**:

**Direct impact** ({count} files):
- `{file}` - {how it uses the module}

**Indirect impact** ({count} files):
- Via `{intermediate module}`
- Affects: {list}

**Testing scope**:
- Unit tests: {files}
- Integration tests: {files}
- E2E tests: {scenarios}

**Risk level**: {Low/Medium/High}

**Recommendation**: {specific guidance}
```

---

### Template: Feature Documentation (Detailed)

```markdown
# Feature Documentation: {Feature Name}

**Date**: {YYYY-MM-DD}
**Analyst**: {name}
**Version**: {if applicable}
**Status**: {Active/Deprecated/Planned}

## Feature Overview

{2-3 sentences describing the feature}

**User-facing functionality**:
- {What users can do}
- {Another capability}

**Business value**: {Why this feature exists}

**Scope**: {Modules/services involved}

## Data Models

### {ModelName}

```typescript
// From src/models/model-name.ts
@Entity('table_name')
export class ModelName {
  @PrimaryKey()
  id: string;

  @Column()
  field: string;

  // ... other fields
}
```

**Relationships**:
- {RelatedModel} - {1:1, 1:N, N:M} - {description}

**Validation**:
- {field}: {rules}

**Database table**: `{table_name}`

## Data Flows

### {Flow Name} (e.g., "Create User")

**Entry point**: `POST /api/v1/users`

**Request**:
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Flow**:
```
1. Controller receives request
   └─ UserController.create() at src/controllers/user.controller.ts:45

2. Validates DTO
   └─ CreateUserDto validation (class-validator)

3. Service processes
   └─ UserService.create() at src/services/user.service.ts:78
      ├─ Checks if email exists
      ├─ Hashes password
      ├─ Creates user via repository
      └─ Emits user.created event

4. Repository persists
   └─ UserRepository.create() at src/repositories/user.repository.ts:34
      └─ INSERT INTO users ...

5. Side effects
   ├─ Welcome email sent (EmailService)
   └─ Profile created (ProfileService, event listener)

6. Response returned
   └─ User object (serialized, password hidden)
```

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

## Business Rules

1. **{Rule name}**: {description}
   - Enforced at: {layer/file}
   - Validation: {how}

2. **{Another rule}**: {description}

## Extension Points

**Events emitted**:
- `{event.name}` - {when emitted} - {payload}
  - Emitted in: {file}:{line}
  - Listeners: {list}

**Hooks/Plugins**:
- {Description of plugin system if exists}

**Configuration**:
- Feature flag: `{config.feature.name}`
- Configurable: {what can be configured}

## Testing

**Coverage**: {percentage}

**Test files**:
- `tests/unit/feature.test.ts` - {test count} tests
- `tests/integration/feature-api.test.ts` - {test count} tests

**Critical test cases**:
1. {Test scenario} - {why it's important}
2. {Another scenario}

## Known Issues & Limitations

**Issues**:
- {Issue description} - {impact}
  - Workaround: {if any}

**Limitations**:
- {Limitation} - {reason}

## Extension Recommendation

{If this is analysis for extension}

**Planned addition**: {what you want to add}

**Recommended approach**: {which option}

**Rationale**: {why}

**Implementation steps**:
1. {Step}
2. {Step}

**Files to modify**:
- {file} - {changes}

**New tests needed**:
- {test scenario}
```

---

## Formatting Guidelines

### Code Examples

**Always include language** for syntax highlighting:

```typescript
// Good - language specified
export class UserService { }
```

**Include context**:
```typescript
// From src/services/user.service.ts, lines 45-52
async getUserById(id: string): Promise<User | null> {
  const user = await this.repository.findById(id);
  if (!user) return null;
  return user;
}
```

### Tables

**Use for comparisons and structured data**:

| Item | Value | Notes |
|------|-------|-------|
| Row 1 | Data | Comment |

**Align for readability** (markdown processors will format):

```markdown
| Long Header | Short | Really Long Header Text |
|-------------|-------|-------------------------|
| Data        | X     | More data here          |
```

### Lists

**Ordered** for sequences/steps:
```markdown
1. First step
2. Second step
3. Third step
```

**Unordered** for collections:
```markdown
- Item one
- Item two
- Item three
```

**Nested** for hierarchy:
```markdown
- Category 1
  - Subcategory A
  - Subcategory B
- Category 2
  - Subcategory C
```

### Diagrams

**Simple ASCII diagrams** for relationships:

```
Controller → Service → Repository → Database
```

**Tree structures**:
```
src/
├── services/
│   ├── user.service.ts
│   └── auth.service.ts
└── models/
    └── user.model.ts
```

**Dependency graphs**:
```
    ┌─────────┐
    │  Module │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│ Dep 1 │ │ Dep 2 │
└───────┘ └───────┘
```

### Emphasis

**Bold** for importance:
```markdown
**Important**: This is critical information
```

**Italic** for emphasis:
```markdown
This is *emphasized* text
```

**Code** for technical terms:
```markdown
The `UserService` class handles business logic
```

### Sections

**Hierarchy**:
```markdown
# Top Level (Document Title)
## Major Section
### Subsection
#### Detail Section
```

**Separators** for visual breaks:
```markdown
---
```

---

## Documentation Quality Checklist

### Before Publishing

- [ ] **Evidence**: All claims cite file paths or code examples
- [ ] **Actionable**: Recommendations are specific and implementable
- [ ] **Structured**: Information organized with clear headers
- [ ] **Examples**: Code examples included for patterns
- [ ] **Reproducible**: Search commands and methodology documented
- [ ] **Complete**: All template sections filled (or marked N/A)
- [ ] **Accurate**: Information verified by reading actual code
- [ ] **Formatted**: Proper markdown syntax, code blocks have language tags
- [ ] **Linked**: File paths use consistent format (absolute or relative from root)
- [ ] **Proofread**: No typos, clear sentences

### Content Quality

- [ ] Executive summary captures key findings
- [ ] Recommendations prioritized (most important first)
- [ ] Code examples are real (from actual codebase)
- [ ] Patterns verified across multiple examples
- [ ] Inconsistencies noted and documented
- [ ] Open questions clearly stated
- [ ] Next steps identified

### Technical Accuracy

- [ ] File paths verified (files actually exist)
- [ ] Code examples tested (copy-pasted correctly)
- [ ] Versions noted for dependencies
- [ ] Relationships accurately mapped
- [ ] Dependencies complete (not missing critical ones)

---

## Common Mistakes to Avoid

### 1. Vague Statements

❌ **Bad**:
```markdown
The system uses services for business logic.
```

✅ **Good**:
```markdown
The system uses class-based services with dependency injection for business logic.
Services are located in src/services/ and follow this pattern:
```typescript
// From src/services/user.service.ts
export class UserService {
  constructor(
    private repository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    // Business logic here
  }
}
```
Found in: user.service.ts, product.service.ts, order.service.ts
```

### 2. Missing Context

❌ **Bad**:
```markdown
Uses JWT authentication.
```

✅ **Good**:
```markdown
Uses JWT authentication via passport-jwt library (v4.0.0):
- Tokens generated in AuthService.login() (src/auth/auth.service.ts:45)
- Tokens validated by JwtStrategy (src/auth/jwt.strategy.ts)
- Token expiry: 1 hour (configured in .env: JWT_EXPIRY=3600)
- Refresh token not implemented
```

### 3. Assuming Instead of Verifying

❌ **Bad**:
```markdown
All endpoints require authentication (assumed based on one example).
```

✅ **Good**:
```markdown
Most endpoints require authentication, but some are public:

**Authenticated** (23 endpoints):
- All /api/users/* except GET /api/users/public/:username
- All /api/products/admin/*
- Protected by @UseGuards(AuthGuard) decorator

**Public** (5 endpoints):
- GET /api/health (health check)
- POST /api/auth/login (login endpoint)
- POST /api/auth/register (registration)
- GET /api/users/public/:username (public profiles)
- GET /api/products (product listing)

Verified by searching for @UseGuards and @Public decorators.
```

### 4. No Evidence

❌ **Bad**:
```markdown
Database uses PostgreSQL.
```

✅ **Good**:
```markdown
Database: PostgreSQL 15.3

**Evidence**:
- Configured in .env: `DATABASE_URL=postgresql://...`
- TypeORM connection (src/config/database.config.ts:12):
  ```typescript
  type: 'postgres',
  host: process.env.DB_HOST,
  port: 5432,
  ```
- Dependencies (package.json): `"pg": "^8.11.0"`
```

### 5. Incomplete Analysis

❌ **Bad**:
```markdown
## Recommendations
Use existing patterns.
```

✅ **Good**:
```markdown
## Recommendations

### 1. Use Service Layer Pattern (High Priority)

**Pattern** (from UserService at src/services/user.service.ts):
```typescript
export class FeatureService {
  constructor(
    private repository: FeatureRepository,
    private dependency: SharedService
  ) {}

  async operation(data: Dto): Promise<Result> {
    // 1. Validation
    // 2. Business logic
    // 3. Repository call
    // 4. Return result
  }
}
```

**Apply to your feature**:
1. Create `src/feature/feature.service.ts`
2. Inject FeatureRepository + dependencies
3. Implement business methods
4. Write tests at `tests/unit/feature.service.test.ts`

### 2. Follow Naming Conventions (High Priority)

- Service class: `{Feature}Service` (PascalCase)
- Service file: `{feature}.service.ts` (kebab-case)
- Methods: `camelCase` with CRUD prefixes (get, create, update, delete)

### 3. Use DTO Validation (Medium Priority)

**Pattern** (from CreateUserDto at src/dto/create-user.dto.ts):
```typescript
export class CreateFeatureDto {
  @IsString()
  @MinLength(3)
  field: string;
}
```

Apply class-validator decorators for all inputs.
```

---

## Summary

Good documentation:
1. **Cites evidence** - File paths, code examples, line numbers
2. **Is actionable** - Specific steps, not vague advice
3. **Is structured** - Clear organization with hierarchy
4. **Is reproducible** - Others can verify findings
5. **Is complete** - All relevant aspects covered
6. **Is accurate** - Verified by reading actual code

Use templates as starting points, adapt as needed, and always prioritize clarity and usefulness over completeness.
