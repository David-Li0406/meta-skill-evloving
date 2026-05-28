---
name: wave-coherence-validation
description: Validates that wave tasks build upon existing implementations in logical dependency order
tier: 2
category: Quality & Architecture
depends_on:
  - architectural-conformance-validation
  - development-best-practices
related_agents:
  - wave-planner
  - backend-specialist
  - frontend-specialist
  - implementation-validator
---

# Wave Coherence Validation Skill

## Purpose

This skill ensures that tasks within a wave are implemented in the correct dependency order by:

1. Analyzing existing implementations in current and parent branches
2. Detecting dependencies between components (database → API → UI)
3. Verifying API endpoints match expected contracts before integration
4. Preventing out-of-order implementation that causes rework
5. Building dependency graphs to guide implementation sequence

**Key Insight**: Code changes should build coherently upon existing implementations, not assume future implementations or ignore existing patterns.

---

## When to Invoke This Skill

### Required Invocation (MUST Use)

Invoke this skill **before starting implementation work** in these scenarios:

- [ ] **Wave Planning**: Before breaking down wave tasks
- [ ] **Implementation Start**: Before backend-specialist or frontend-specialist begins work
- [ ] **Integration Work**: Before connecting frontend to backend APIs
- [ ] **Database Changes**: Before modifying schema that affects APIs

### Recommended Invocation (SHOULD Use)

Invoke this skill when:

- [ ] **PR Review**: Validate changes follow dependency order
- [ ] **Merge Preparation**: Ensure no missing dependencies before merge
- [ ] **Bug Investigation**: Check if issue caused by out-of-order implementation

### Working With Other Skills

**Before this skill**:
1. `architectural-conformance-validation` - Ensure architecture decisions are followed
2. `git-repository-setup-validation` - Verify branches are properly setup

**After this skill**:
1. `development-best-practices` - Implement with proper standards
2. `implementation-velocity-tracking` - Track completion after validation

---

## Skill Workflow

### Step 1: Scope Analysis

**Objective**: Determine what code is available in current and parent branches

**Actions**:

1. **Identify current branch and parent**
   ```bash
   # Get current branch
   git branch --show-current

   # Get parent branch (epic or development)
   git show-branch | grep '*' | grep -v "$(git rev-parse --abbrev-ref HEAD)" | head -1 | sed 's/.*\[\(.*\)\].*/\1/'
   ```

2. **Get commit history for context**
   ```bash
   # What's in current branch (not yet merged to parent)
   git log --oneline parent-branch..HEAD

   # What's in parent branch
   git log --oneline HEAD..parent-branch
   ```

3. **List files changed in current branch**
   ```bash
   git diff --name-status parent-branch...HEAD
   ```

**Validation Checklist**:
- [ ] Current branch identified
- [ ] Parent branch identified
- [ ] Commit scope understood
- [ ] Changed files cataloged

---

### Step 2: Dependency Detection

**Objective**: Identify dependencies between components in the wave

**Actions**:

1. **Scan for database schema changes**
   ```bash
   # Find migration files
   find . -path "*/migrations/*" -name "*.sql" -o -name "*.js" -o -name "*.ts"

   # Find schema definitions
   find . -name "*schema*" -o -name "*model*" | grep -E "\.(ts|js|py|sql)$"
   ```

2. **Scan for API endpoints**
   ```bash
   # Find route definitions (Node.js/Express example)
   grep -r "router\.\(get\|post\|put\|delete\|patch\)" --include="*.ts" --include="*.js"

   # Find controller methods
   grep -r "@\(Get\|Post\|Put\|Delete\|Patch\)" --include="*.ts" --include="*.java"

   # Find API decorators (Python/FastAPI example)
   grep -r "@app\.\(get\|post\|put\|delete\|patch\)" --include="*.py"
   ```

3. **Scan for service layer components**
   ```bash
   # Find service files
   find . -name "*service*" -o -name "*repository*" | grep -E "\.(ts|js|py|java)$"

   # Find business logic classes
   grep -r "class.*Service\|class.*Repository" --include="*.ts" --include="*.js" --include="*.py"
   ```

4. **Scan for UI components**
   ```bash
   # Find component files
   find . -name "*.tsx" -o -name "*.jsx" -o -name "*.vue"

   # Find API calls in frontend
   grep -r "fetch\|axios\|http\.get\|http\.post" --include="*.tsx" --include="*.jsx" --include="*.vue"
   ```

5. **Scan for type definitions/interfaces**
   ```bash
   # Find TypeScript interfaces
   grep -r "interface\|type.*=" --include="*.ts" --include="*.tsx"

   # Find DTOs
   find . -name "*dto*" -o -name "*interface*" | grep -E "\.(ts|js|java)$"
   ```

**Build Dependency Map**:

```
Database Schema
  ↓
Types/Interfaces (DTOs)
  ↓
Repository/Data Access Layer
  ↓
Service Layer (Business Logic)
  ↓
API Controllers/Endpoints
  ↓
Frontend API Clients
  ↓
UI Components
```

**Validation Checklist**:
- [ ] Database changes identified
- [ ] API endpoints cataloged
- [ ] Service layer components found
- [ ] UI components mapped
- [ ] Type definitions documented
- [ ] Dependency relationships mapped

---

### Step 3: API Endpoint Verification (Priority Order)

**Objective**: Verify existing API endpoints match expected contracts

**Priority 1: Test Endpoint (If Running Locally)**

```bash
# Check if dev server is running
curl -s http://localhost:3000/health || echo "Server not running"

# Test GET endpoint
curl -X GET http://localhost:3000/api/users/123

# Test POST endpoint
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'
```

**Capture Response Format**:
```json
{
  "actual_response": {
    "id": "123",
    "name": "Test User",
    "email": "test@example.com"
  },
  "status_code": 200,
  "headers": {
    "content-type": "application/json"
  }
}
```

**Priority 2: Read Code Implementation**

If endpoint cannot be tested, read the code:

```typescript
// Example: Read route handler
// File: src/routes/users.ts

router.get('/users/:id', async (req, res) => {
  const user = await userService.getById(req.params.id);
  res.json(user);  // ← Identify response format
});

// Document findings:
// - Endpoint: GET /api/users/:id
// - Parameters: id (path parameter)
// - Response: User object { id, name, email }
// - Error handling: (check for try-catch)
```

**Priority 3: Check Existing Tests**

If code is unclear, look for tests:

```bash
# Find test files for endpoint
find . -name "*.test.ts" -o -name "*.spec.ts" | xargs grep -l "users"

# Read test to understand contract
cat src/routes/users.test.ts
```

```typescript
// Example test that documents contract
it('should return user by id', async () => {
  const response = await request(app)
    .get('/api/users/123')
    .expect(200);

  expect(response.body).toEqual({
    id: '123',
    name: expect.any(String),
    email: expect.any(String)
  });
});
// ← This documents expected response structure
```

**Validation Checklist**:
- [ ] API endpoints tested (if server running)
- [ ] Response format documented
- [ ] Request parameters documented
- [ ] Error responses documented
- [ ] Code implementation reviewed (if testing failed)
- [ ] Existing tests reviewed (if code unclear)

---

### Step 4: Coherence Analysis

**Objective**: Identify out-of-order implementations and missing dependencies

**Check 1: Missing Lower-Layer Dependencies**

```bash
# Example: UI component calls API that doesn't exist yet

# Frontend code (current wave)
grep -r "fetch('/api/users')" src/components/

# But API doesn't exist
grep -r "router.get('/users')" src/routes/
# ← Returns nothing = BLOCKER
```

**Warning Example**:
```
⚠️ BLOCKER: UI component calls /api/users but endpoint not implemented
  Location: src/components/UserList.tsx:15
  Missing: GET /api/users endpoint
  Action Required: Implement API endpoint before UI component
```

**Check 2: Schema Mismatch Between Layers**

```typescript
// Example: API returns different format than UI expects

// API code (already implemented)
// File: src/routes/users.ts
res.json({ user_id: user.id, user_name: user.name });

// Frontend code (current wave)
// File: src/components/UserList.tsx
const { id, name } = await response.json();  // ← Expects 'id', but API returns 'user_id'
```

**Warning Example**:
```
⚠️ SCHEMA MISMATCH: Frontend expects different field names than API provides
  API Response: { user_id, user_name }
  Frontend Expects: { id, name }
  Location: src/components/UserList.tsx:20
  Action Required: Either update frontend to use user_id/user_name OR update API to use id/name
```

**Check 3: Missing Type Definitions**

```typescript
// Example: Service uses types that don't exist

// Service code (current wave)
// File: src/services/userService.ts
export function getUser(id: string): Promise<User> { ... }
//                                              ↑
//                                              Type 'User' not found
```

**Warning Example**:
```
⚠️ MISSING DEPENDENCY: Service references undefined type 'User'
  Location: src/services/userService.ts:5
  Missing: User interface/type definition
  Action Required: Define User interface before implementing service
```

**Check 4: Database Changes Not Reflected in Code**

```sql
-- Migration (already applied)
-- File: migrations/001_add_user_role.sql
ALTER TABLE users ADD COLUMN role VARCHAR(50);
```

```typescript
// But API doesn't use new field
// File: src/routes/users.ts
res.json({ id: user.id, name: user.name });  // ← Missing 'role' field
```

**Warning Example**:
```
⚠️ UNUSED SCHEMA CHANGE: Database column 'role' added but not used in API
  Migration: migrations/001_add_user_role.sql
  API: src/routes/users.ts (doesn't include 'role' in response)
  Action Required: Either use 'role' in API response OR remove migration if not needed
```

**Validation Checklist**:
- [ ] All API calls have corresponding endpoints
- [ ] Schema matches between layers (database → API → UI)
- [ ] Type definitions exist before usage
- [ ] Database changes reflected in code
- [ ] No orphaned code (unused implementations)

---

### Step 5: Dependency Graph Generation

**Objective**: Create visual dependency graph showing implementation order

**Example Output**:

```
Wave Coherence Validation Report
================================

Current Branch: feature-1.10-infrastructure
Parent Branch: epic-1-progressive-coherence

Dependency Graph (Bottom-Up Order):
====================================

1. [✅ DONE] Database Schema
   └─ migrations/001_create_users_table.sql (committed: abc123)

2. [✅ DONE] Type Definitions
   └─ src/types/user.ts (committed: def456)
      └─ Exports: User interface

3. [✅ DONE] Repository Layer
   └─ src/repositories/userRepository.ts (committed: ghi789)
      └─ Depends on: User interface
      └─ Exports: UserRepository class

4. [✅ DONE] Service Layer
   └─ src/services/userService.ts (committed: jkl012)
      └─ Depends on: UserRepository
      └─ Exports: UserService class

5. [⚠️ IN PROGRESS] API Endpoints
   └─ src/routes/users.ts (uncommitted changes)
      └─ Depends on: UserService
      └─ Implements: GET /api/users, POST /api/users
      └─ ⚠️ WARNING: POST /api/users not tested yet

6. [🔴 BLOCKED] Frontend API Client
   └─ src/api/userApi.ts (not implemented)
      └─ Depends on: API endpoints (GET /api/users, POST /api/users)
      └─ 🔴 BLOCKER: Cannot implement until API endpoints tested and merged

7. [🔴 BLOCKED] UI Components
   └─ src/components/UserList.tsx (not implemented)
      └─ Depends on: Frontend API client
      └─ 🔴 BLOCKER: Cannot implement until API client exists

Blockers Summary:
=================
🔴 2 blockers found

1. Frontend API Client (src/api/userApi.ts)
   - BLOCKED BY: Untested API endpoint POST /api/users
   - ACTION: Test API endpoint, verify request/response format
   - SEQUENCE: Complete #5 (API Endpoints) before starting #6

2. UI Components (src/components/UserList.tsx)
   - BLOCKED BY: Missing frontend API client
   - ACTION: Implement API client first
   - SEQUENCE: Complete #6 (Frontend API Client) before starting #7

Warnings:
=========
⚠️ 1 warning found

1. API Endpoint Not Tested
   - LOCATION: src/routes/users.ts:25 (POST /api/users)
   - ISSUE: Endpoint implemented but no test verification
   - ACTION: Start dev server and test endpoint OR write unit test
   - PRIORITY: High (blocks frontend work)

Recommended Implementation Sequence:
====================================
✅ Steps 1-4 complete
➡️ Next: Complete step 5 (test API endpoint)
Then: Proceed to step 6 (frontend API client)
Finally: Proceed to step 7 (UI components)

Coherence Status: ⚠️ WARNINGS (safe to proceed with caution)
```

---

### Step 6: Integration Contract Validation

**Objective**: When integrating frontend ↔ backend, verify contracts match

**Example Workflow**:

1. **API Contract (Already Implemented)**
   ```typescript
   // src/routes/users.ts
   router.post('/users', async (req, res) => {
     // Expected request body:
     // { name: string, email: string }
     const user = await userService.create(req.body);

     // Response format:
     // { id: string, name: string, email: string, createdAt: string }
     res.status(201).json(user);
   });
   ```

2. **Frontend Implementation (Current Wave)**
   ```typescript
   // src/api/userApi.ts
   export async function createUser(userData: CreateUserDTO) {
     const response = await fetch('/api/users', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(userData)
     });
     return response.json();
   }
   ```

3. **Validation Checks**
   - [ ] Request body format matches API expectations
   - [ ] Response parsing matches API response format
   - [ ] Error handling covers API error responses
   - [ ] Content-Type headers correct
   - [ ] HTTP method correct (GET/POST/PUT/DELETE)

4. **Test Integration**
   ```typescript
   // Test the actual API call
   const testData = { name: 'Test User', email: 'test@example.com' };
   const result = await createUser(testData);

   // Verify response structure
   console.log('API Response:', result);
   // Expected: { id: '...', name: 'Test User', email: 'test@example.com', createdAt: '...' }
   ```

**Validation Checklist**:
- [ ] Request format verified
- [ ] Response format verified
- [ ] Error handling verified
- [ ] Integration tested (if possible)
- [ ] Type definitions match contract

---

## Output Format

### Successful Validation

```yaml
status: PASS
message: "Wave coherence validated. All dependencies in correct order."
branch:
  current: feature-1.10-infrastructure
  parent: epic-1-progressive-coherence
dependencies:
  total: 7
  completed: 7
  in_progress: 0
  blocked: 0
blockers: []
warnings: []
recommendation: "Proceed with implementation. All dependencies available."
```

### Validation with Warnings

```yaml
status: WARNING
message: "Wave coherence validated with warnings. Review before proceeding."
branch:
  current: feature-1.10-infrastructure
  parent: epic-1-progressive-coherence
dependencies:
  total: 7
  completed: 4
  in_progress: 1
  blocked: 2
blockers:
  - component: "Frontend API Client"
    file: "src/api/userApi.ts"
    blocked_by: "Untested API endpoint POST /api/users"
    action: "Test API endpoint before implementing frontend client"
    sequence: "Complete API testing (#5) before starting #6"
warnings:
  - type: "UNTESTED_API"
    location: "src/routes/users.ts:25"
    message: "POST /api/users implemented but not tested"
    priority: "high"
    action: "Test endpoint to verify request/response format"
recommendation: "Complete API testing before proceeding to frontend work."
dependency_graph: |
  1. [✅] Database Schema
  2. [✅] Type Definitions
  3. [✅] Repository Layer
  4. [✅] Service Layer
  5. [⚠️] API Endpoints (untested)
  6. [🔴] Frontend API Client (blocked)
  7. [🔴] UI Components (blocked)
```

### Validation Failure

```yaml
status: FAIL
message: "Wave coherence validation failed. Critical blockers found."
branch:
  current: feature-1.10-infrastructure
  parent: epic-1-progressive-coherence
dependencies:
  total: 7
  completed: 2
  in_progress: 1
  blocked: 4
blockers:
  - component: "Service Layer"
    file: "src/services/userService.ts"
    blocked_by: "Missing type definition 'User'"
    action: "Define User interface before implementing service"
    sequence: "Must complete #2 (Type Definitions) before #4 (Service Layer)"
  - component: "API Endpoints"
    file: "src/routes/users.ts"
    blocked_by: "Missing service layer implementation"
    action: "Implement UserService before API routes"
    sequence: "Must complete #4 (Service Layer) before #5 (API Endpoints)"
warnings:
  - type: "OUT_OF_ORDER"
    location: "src/routes/users.ts"
    message: "Attempting to implement API before service layer exists"
    priority: "critical"
    action: "Stop. Implement dependencies in correct order."
recommendation: "STOP. Resolve blockers before proceeding. Implementation order incorrect."
dependency_graph: |
  1. [✅] Database Schema
  2. [✅] Type Definitions
  3. [🔴] Repository Layer (blocked by missing types)
  4. [🔴] Service Layer (blocked by missing repository)
  5. [⚠️] API Endpoints (blocked by missing service - OUT OF ORDER!)
  6. [🔴] Frontend API Client (blocked)
  7. [🔴] UI Components (blocked)
```

---

## Integration with Other Skills

### Works With: architectural-conformance-validation

**Sequence**:
1. Run `architectural-conformance-validation` first (verify architecture decisions)
2. Run `wave-coherence-validation` second (verify implementation order)

**Example**:
```yaml
# Step 1: Architectural validation
architectural-conformance-validation:
  status: PASS
  message: "Changes conform to layered architecture pattern"

# Step 2: Coherence validation
wave-coherence-validation:
  status: PASS
  message: "Dependencies in correct order"

# Both pass → Safe to proceed
```

### Works With: development-best-practices

**Sequence**:
1. Run `wave-coherence-validation` (verify dependencies available)
2. Run `development-best-practices` during implementation (verify code quality)

**Example**:
```yaml
# Step 1: Validate coherence
wave-coherence-validation:
  status: PASS
  recommendation: "Proceed with API endpoint implementation"

# Step 2: Implement following best practices
development-best-practices:
  - Check file existence before import ✅
  - Verify API signatures ✅
  - Externalize configuration ✅
```

### Used By: wave-planner

**Workflow**:
```
wave-planner invokes wave-coherence-validation
  ↓
Skill analyzes dependencies
  ↓
Returns dependency graph + blockers
  ↓
wave-planner creates tasks in correct sequence
  ↓
wave-planner assigns tasks respecting dependency order
```

### Used By: Implementation Agents

**Workflow**:
```
backend-specialist invoked for API implementation
  ↓
Invokes wave-coherence-validation
  ↓
Skill checks: Are service layer dependencies available?
  ↓
Status: PASS → Proceed with implementation
Status: FAIL → Report blockers to user, wait for dependencies
```

---

## Reference Files

See `references/` directory for:

- **dependency-detection-patterns.md**: Common code patterns for detecting dependencies
- **api-contract-verification.md**: Detailed API testing and verification procedures
- **coherence-anti-patterns.md**: Common out-of-order implementation mistakes

---

## Scripts

See `scripts/` directory for:

- **analyze-dependencies.sh**: Automated dependency scanning
- **test-api-contract.sh**: API endpoint testing script
- **generate-dependency-graph.sh**: Dependency graph generation

---

## Common Issues

### Issue 1: "Cannot find dependency in current or parent branch"

**Problem**: Code references component that doesn't exist in git history

**Solution**:
1. Check if component is in uncommitted changes
2. Check if component is in different feature branch (needs merge)
3. Create component if truly missing

### Issue 2: "API endpoint returns different format than expected"

**Problem**: Frontend expects one format, API returns another

**Solution**:
1. Test API endpoint to see actual response
2. Update frontend to match API response
3. OR update API to match expected format (if API is wrong)
4. Ensure both use same type definitions

### Issue 3: "Circular dependency detected"

**Problem**: Component A depends on B, but B also depends on A

**Solution**:
1. Extract shared code to separate module
2. Use dependency injection to break cycle
3. Refactor to remove circular dependency

---

## Success Criteria

**This skill is successful when**:

✅ All dependencies identified correctly
✅ Dependency order validated (no out-of-order implementations)
✅ API contracts verified (if endpoints exist)
✅ Blockers clearly identified with actionable guidance
✅ Dependency graph generated and easy to understand
✅ Implementation sequence recommended
✅ Integration between layers validated

**This skill has failed if**:

❌ Dependencies missed (implementation fails due to missing code)
❌ False positives (reports blockers that don't exist)
❌ Unclear guidance (user doesn't know what to do next)
❌ API contract mismatch not detected (integration breaks)

---

## Example Usage

### Example 1: Starting Wave Implementation

```yaml
# User requests: "Implement user management feature"

# Agent invokes: wave-coherence-validation

Input:
  current_branch: feature-1.10-infrastructure
  parent_branch: epic-1-progressive-coherence
  wave_tasks:
    - Implement user database schema
    - Create user API endpoints
    - Build user management UI

Output:
  status: PASS
  recommendation: "Implement in sequence: schema → API → UI"
  dependency_graph:
    1. [⚠️ TODO] Database Schema (migrations/create_users.sql)
    2. [🔴 BLOCKED] API Endpoints (blocked by #1)
    3. [🔴 BLOCKED] UI Components (blocked by #2)
  next_step: "Start with database schema (task #1)"
```

### Example 2: Frontend Integration

```yaml
# User requests: "Connect user list UI to backend API"

# Agent invokes: wave-coherence-validation

Input:
  current_branch: feature-1.10-infrastructure
  parent_branch: epic-1-progressive-coherence
  integration_points:
    - Frontend: src/components/UserList.tsx
    - API: GET /api/users

Output:
  status: WARNING
  warnings:
    - type: UNTESTED_API
      message: "API endpoint exists but not tested"
  recommendation: "Test API endpoint before integration"
  api_test_result:
    endpoint: GET /api/users
    test_command: "curl http://localhost:3000/api/users"
    expected_response: "[{ id, name, email }]"
  next_step: "Run API test, verify response format, then implement frontend"
```

---

**Last Updated**: 2025-01-30
**Version**: 1.0
