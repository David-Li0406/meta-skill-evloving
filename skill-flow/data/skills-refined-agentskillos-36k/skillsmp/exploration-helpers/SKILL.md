---
name: Exploration Helpers
description: |
  Use this skill when the user needs to explore the codebase, understand database schema, navigate API endpoints, or validate TypeScript types. Triggers on: "Explore the database", "Understand codebase structure", "Validate TypeScript types", "Find API endpoints", "Database schema", "How is the code organized?", "What tables exist?".
version: 1.0.0
---

# Exploration Helpers

Guidance for exploring and understanding codebases, databases, and APIs.

## Database Exploration

### Understanding Schema

When exploring a database, gather:

1. **Tables and Relationships**
   - List all tables
   - Identify primary keys
   - Map foreign key relationships
   - Note junction tables for many-to-many

2. **Column Details**
   - Data types
   - Nullable vs required
   - Default values
   - Constraints

3. **Indexes**
   - Primary indexes
   - Unique indexes
   - Composite indexes
   - Performance indexes

### Common Exploration Queries

**List all tables:**

```sql
-- PostgreSQL
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- MySQL
SHOW TABLES;

-- SQLite
SELECT name FROM sqlite_master WHERE type='table';
```

**Get table structure:**

```sql
-- PostgreSQL
\d table_name

-- MySQL
DESCRIBE table_name;

-- SQLite
.schema table_name
```

**Find foreign keys:**

```sql
-- PostgreSQL
SELECT
    tc.table_name, kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### Database Documentation Pattern

Document schema discoveries in this format:

```markdown
## Table: users

| Column     | Type         | Nullable | Default           | Description   |
| ---------- | ------------ | -------- | ----------------- | ------------- |
| id         | uuid         | NO       | gen_random_uuid() | Primary key   |
| email      | varchar(255) | NO       | -                 | Unique email  |
| created_at | timestamp    | NO       | now()             | Creation time |

**Relationships:**

- Has many: orders, sessions
- Belongs to: organization

**Indexes:**

- users_pkey (id)
- users_email_key (email) UNIQUE
```

---

## Codebase Exploration

### Understanding Project Structure

When exploring a codebase:

1. **Entry Points**
   - Main application file
   - Router/routing configuration
   - Configuration files

2. **Architecture Patterns**
   - Folder organization (by feature, by type)
   - Naming conventions
   - Module boundaries

3. **Key Abstractions**
   - Base classes/interfaces
   - Shared utilities
   - Common patterns

### Common Exploration Patterns

**Find all components:**

```bash
# React/Vue components
find src -name "*.tsx" -o -name "*.vue"

# Or use glob in Claude Code
# Pattern: **/*.tsx
```

**Find API routes:**

```bash
# Express routes
grep -r "router\." --include="*.ts"

# Next.js API routes
ls -la app/api/
ls -la pages/api/

# FastAPI routes
grep -r "@app\." --include="*.py"
grep -r "@router\." --include="*.py"
```

**Find configuration:**

```bash
# Config files
find . -name "*.config.*" -o -name ".env*" -o -name "*.json"
```

### Codebase Documentation Pattern

Document findings in this format:

```markdown
## Project Structure
```

src/
├── app/ # Next.js app router
├── components/ # Shared React components
│ ├── ui/ # Base UI components
│ └── features/ # Feature-specific components
├── lib/ # Shared utilities
├── hooks/ # Custom React hooks
└── types/ # TypeScript types

```

## Key Files

| File | Purpose |
|------|---------|
| src/app/layout.tsx | Root layout with providers |
| src/lib/api.ts | API client configuration |
| src/types/index.ts | Shared type definitions |

## Patterns Identified

- **State Management:** React Query for server state
- **Styling:** Tailwind CSS with shadcn/ui components
- **API:** REST endpoints in /app/api/
```

---

## API Exploration

### Understanding API Structure

When exploring an API:

1. **Endpoints**
   - Routes and HTTP methods
   - Request/response formats
   - Authentication requirements

2. **Patterns**
   - Error handling approach
   - Pagination style
   - Filtering/sorting

3. **Authentication**
   - Auth mechanism (JWT, session, API key)
   - Protected vs public routes
   - Role-based access

### API Documentation Pattern

````markdown
## API Endpoints

### Users

| Method | Path           | Auth  | Description    |
| ------ | -------------- | ----- | -------------- |
| GET    | /api/users     | Yes   | List all users |
| GET    | /api/users/:id | Yes   | Get user by ID |
| POST   | /api/users     | Yes   | Create user    |
| PUT    | /api/users/:id | Yes   | Update user    |
| DELETE | /api/users/:id | Admin | Delete user    |

### Request/Response Examples

**GET /api/users**

```json
// Response
{
  "data": [{ "id": "1", "email": "user@example.com" }],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```
````

````

---

## Type Validation

### TypeScript Type Checking

When validating types:

1. **Check for Type Errors**
   ```bash
   npx tsc --noEmit
````

2. **Find Type Definitions**

   ```bash
   find src -name "*.d.ts" -o -name "types.ts" -o -name "types/*.ts"
   ```

3. **Verify API Types Match**
   - Compare API response shapes with TypeScript interfaces
   - Check for optional vs required mismatches
   - Verify enum values align

### Common Type Issues

**Missing Properties:**

```typescript
// API returns more fields than type defines
interface User {
  id: string;
  name: string;
  // Missing: email, createdAt from API
}
```

**Optional Mismatches:**

```typescript
// API always returns field, but type marks optional
interface User {
  id: string;
  name?: string; // Should be required
}
```

**Enum Misalignment:**

```typescript
// Type has different values than API
type Status = "active" | "inactive";
// API returns: 'ACTIVE' | 'INACTIVE'
```

### Type Validation Checklist

- [ ] Run `tsc --noEmit` with no errors
- [ ] API response types match actual responses
- [ ] Database schema types match ORM models
- [ ] Enum values match across frontend/backend
- [ ] Optional fields correctly marked
- [ ] Null vs undefined handled consistently

---

## Exploration Workflow

### Step-by-Step Process

1. **Start with Entry Points**
   - Find main files, configs, routes
   - Understand how the app bootstraps

2. **Map the Architecture**
   - Identify folder patterns
   - Find shared abstractions
   - Note naming conventions

3. **Trace a Feature**
   - Pick one feature end-to-end
   - Follow from UI to API to database
   - Document the patterns

4. **Document Findings**
   - Create exploration notes
   - List key files and purposes
   - Note patterns for future reference

### Using Claude Code Agents

**For Database Exploration:**

```
Use the Explore agent with prompt:
"Find all database tables and their relationships in this project"
```

**For Codebase Navigation:**

```
Use the Explore agent with prompt:
"How is authentication implemented? Trace from login form to API"
```

**For API Discovery:**

```
Use the Explore agent with prompt:
"List all API endpoints and their request/response formats"
```
