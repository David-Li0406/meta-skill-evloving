# Enrich Task Workflow

## Purpose

Add required fields (`<files>`, `<action>`, `<verify>`, `<done>`) to a task from the tasks.md file, using context from spec.md, requirements.md, and codebase patterns.

## Inputs

```typescript
interface EnrichTaskInput {
  task: {
    id: string;           // e.g., "2.1"
    name: string;         // e.g., "Write 2-8 focused tests"
    subtasks?: string[];  // Bullet points under the task
  };
  spec_context: {
    spec_md: string;      // Contents of spec.md
    requirements_md: string; // Contents of requirements.md
    codebase_patterns: {
      test_dir: string;   // e.g., "src/__tests__"
      source_dir: string; // e.g., "src"
      file_patterns: string[]; // e.g., ["*.ts", "*.tsx"]
    };
  };
}
```

## Outputs

```typescript
interface EnrichedTask {
  name: string;
  files: string[];      // Specific file paths
  action: string;       // Numbered implementation steps
  verify: string;       // Executable verification command
  done: string;         // Measurable completion criteria
  needs_clarification: boolean;
  clarification_items?: string[];
}
```

## Enrichment Process

### Step 1: Infer File Paths (`<files>`)

**Sources (in priority order):**

1. **Explicit mentions in task name/subtasks:**
   ```
   Task: "Create src/api/users/route.ts"
   -> files: ["src/api/users/route.ts"]
   ```

2. **Pattern matching from requirements.md:**
   ```
   Requirements: "API routes should be in src/api/{resource}/"
   Task: "Create user API"
   -> files: ["src/api/users/route.ts"]
   ```

3. **Codebase pattern inference:**
   ```
   Existing: src/api/posts/route.ts, src/api/comments/route.ts
   Task: "Create user API"
   -> files: ["src/api/users/route.ts"]
   ```

4. **Test file inference:**
   ```
   Task: "Write tests for user API"
   Source: src/api/users/route.ts
   Pattern: src/__tests__/*.test.ts
   -> files: ["src/__tests__/users.test.ts"]
   ```

**Fallback:** If no files can be inferred, add to `clarification_items`:
```
"File paths needed for task {id}: {name}"
```

### Step 2: Generate Action Steps (`<action>`)

**Build from:**

1. **Subtask bullets -> Numbered steps:**
   ```
   Subtasks:
   - Implement index action
   - Implement show action
   - Add validation

   -> Action:
   1. Implement index action
      - Return list of resources
      - Add pagination support
   2. Implement show action
      - Return single resource by ID
      - Handle 404 for missing
   3. Add validation
      - Validate request body schema
      - Return 400 for invalid input
   ```

2. **Add "what to avoid and WHY":**
   ```
   Action:
   1. Create REST endpoint
      - Use existing controller pattern from src/api/posts/
      - Do NOT use raw SQL queries (prevents injection, use ORM)
      - Do NOT skip input validation (security requirement)
   ```

3. **Reference existing patterns:**
   ```
   Action:
   1. Follow pattern from @src/api/posts/route.ts
   2. Reuse validation middleware from @src/middleware/validate.ts
   ```

**Fallback:** If subtasks are too vague:
```
"Implementation details needed for task {id}: What specific steps should be taken?"
```

### Step 3: Create Verify Command (`<verify>`)

**Sources (in priority order):**

1. **Test task -> Test command:**
   ```
   Task: "Write tests for user API"
   -> verify: "npm test -- src/__tests__/users.test.ts"
   ```

2. **Implementation task -> Related test:**
   ```
   Task: "Create user API endpoint"
   -> verify: "npm test -- src/__tests__/users.test.ts && npm run build"
   ```

3. **Build/compile task -> Build command:**
   ```
   Task: "Add TypeScript types"
   -> verify: "npm run typecheck"
   ```

4. **Config task -> Validation command:**
   ```
   Task: "Update ESLint config"
   -> verify: "npm run lint"
   ```

**Default fallbacks:**
- TypeScript project: `npm run build && npm test`
- JavaScript project: `npm test`
- Python project: `pytest`
- Go project: `go test ./...`

### Step 4: Define Done Criteria (`<done>`)

**Convert acceptance criteria to measurable form:**

| Vague Criteria | Measurable Done |
|----------------|-----------------|
| "Should work" | "All tests pass, endpoint returns 200 for valid requests" |
| "Properly validated" | "Returns 400 with error message for invalid input" |
| "Auth required" | "Returns 401 without token, 403 without permission" |
| "Fast enough" | "Response time < 200ms for typical request" |
| "Well documented" | "JSDoc comments on all public functions" |

**Pattern:**
```
<done>[Quantifiable outcome] + [Specific success indicators]</done>
```

**Examples:**
```
X "User API works"
V "GET /users returns 200 with array, POST /users creates user and returns 201"

X "Tests pass"
V "All 6 tests pass, coverage > 80% for new files"

X "Looks good"
V "No TypeScript errors, no ESLint warnings, build succeeds"
```

## Complete Example

**Input:**
```yaml
task:
  id: "2.1"
  name: "Create user API endpoint"
  subtasks:
    - "Implement GET /users (list)"
    - "Implement POST /users (create)"
    - "Add input validation"

spec_context:
  spec_md: "REST API for user management..."
  requirements_md: "API routes in src/api/{resource}/route.ts"
  codebase_patterns:
    test_dir: "src/__tests__"
    source_dir: "src"
```

**Output:**
```xml
<task type="auto">
  <name>Task 1: Create user API endpoint</name>
  <files>src/api/users/route.ts, src/__tests__/users.test.ts</files>
  <action>
1. Create src/api/users/route.ts following pattern from src/api/posts/route.ts
   - Implement GET /users handler returning paginated list
   - Implement POST /users handler with request body parsing
   - Do NOT use raw SQL (use Prisma ORM to prevent injection)

2. Add input validation for POST /users
   - Validate email format, required fields
   - Return 400 with descriptive error for invalid input
   - Use zod schema validation (existing pattern)

3. Write tests in src/__tests__/users.test.ts
   - Test GET returns array with correct shape
   - Test POST creates user and returns 201
   - Test validation rejects invalid input
  </action>
  <verify>npm test -- src/__tests__/users.test.ts && npm run build</verify>
  <done>GET /users returns 200 with user array, POST /users returns 201 with created user, invalid POST returns 400 with error details, all tests pass</done>
</task>
```

## Handling Vague Tasks

When a task cannot be enriched sufficiently:

1. **Set `needs_clarification: true`**
2. **Add specific items to `clarification_items`:**
   ```typescript
   {
     needs_clarification: true,
     clarification_items: [
       "2.1: What file path for user API? (e.g., src/api/users/route.ts)",
       "2.1: What validation rules for POST body?",
       "2.1: Should pagination be included in GET?"
     ]
   }
   ```

3. **Trigger clarification protocol** (see `clarification-protocol.md`)

## Error Handling

| Situation | Action |
|-----------|--------|
| No subtasks provided | Infer from task name, mark for clarification if unclear |
| No matching codebase patterns | Use spec.md hints, ask user for paths |
| Conflicting requirements | Stop, present conflict, ask for resolution |
| Missing spec.md/requirements.md | Use task name only, mark all fields for clarification |
