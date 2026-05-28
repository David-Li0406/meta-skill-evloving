# Example: API Endpoints Decomposition

## User Request
"Add CRUD endpoints for blog posts with authentication"

## Decomposition Output

### Task Analysis
- Multiple API routes needed (create, read, update, delete)
- Authentication middleware required
- Database operations

### Tasks

```
Task 1: Create Post Types
- Depends on: none
- Files: types/post.ts
- Done when: TypeScript types for Post entity exist
- Complexity: S

Task 2: Create Auth Middleware
- Depends on: none
- Files: middleware/auth.ts
- Done when: JWT validation middleware works
- Complexity: S

Task 3: Create Posts API - List
- Depends on: [Task 1]
- Files: api/posts/route.ts
- Done when: GET /api/posts returns paginated posts
- Complexity: S

Task 4: Create Posts API - Get Single
- Depends on: [Task 1]
- Files: api/posts/[id]/route.ts
- Done when: GET /api/posts/:id returns single post
- Complexity: S

Task 5: Create Posts API - Create
- Depends on: [Task 1, Task 2]
- Files: api/posts/route.ts
- Done when: POST /api/posts creates post (auth required)
- Complexity: M

Task 6: Create Posts API - Update
- Depends on: [Task 1, Task 2]
- Files: api/posts/[id]/route.ts
- Done when: PUT /api/posts/:id updates post (auth required)
- Complexity: M

Task 7: Create Posts API - Delete
- Depends on: [Task 1, Task 2]
- Files: api/posts/[id]/route.ts
- Done when: DELETE /api/posts/:id removes post (auth required)
- Complexity: S
```

### Execution Strategy

```
Group 1 (Parallel - no dependencies):
  ├── Task 1: Create Post Types
  └── Task 2: Create Auth Middleware

Group 2 (Parallel - depends on Group 1):
  ├── Task 3: Create Posts API - List
  ├── Task 4: Create Posts API - Get Single
  ├── Task 5: Create Posts API - Create
  ├── Task 6: Create Posts API - Update
  └── Task 7: Create Posts API - Delete
```

### Feature List

```yaml
features:
  - id: task-001
    description: "Create TypeScript types for Post entity"
    status: failing
    verification_command: "npx tsc --noEmit types/post.ts"
    expected_output: "no output (success)"
    evidence_required: true
    can_be_removed: false

  - id: task-002
    description: "Create JWT auth middleware"
    status: failing
    verification_command: "npm test -- --testPathPattern='auth.test'"
    expected_output: "Tests: X passed"
    evidence_required: true
    can_be_removed: false
```
