# Sample Codex Consultation

This document shows example inputs and outputs for the codex-consult skill.

## Example 1: Plan Mode - API Design

### Input
```bash
bash scripts/codex-exec.sh "Design a REST API for a task management system with CRUD operations"
```

### Output
```markdown
## Summary

Design a RESTful API for task management with standard CRUD operations, following REST best practices and JSON:API conventions.

**Assumptions:**
- Using Express.js or similar framework
- PostgreSQL for data persistence
- JWT authentication already in place

**Impact:**
- Creates: src/routes/tasks.ts, src/controllers/taskController.ts
- Creates: src/models/Task.ts, src/validators/taskValidator.ts

## Implementation Approach

### Step 1: Define Task Model
- File: src/models/Task.ts
- Fields: id, title, description, status, priority, dueDate, createdAt, updatedAt
- Status enum: pending, in_progress, completed, cancelled

### Step 2: Create Task Validator
- File: src/validators/taskValidator.ts
- Validate required fields (title)
- Validate status and priority enums
- Validate date formats

### Step 3: Implement Task Controller
- File: src/controllers/taskController.ts
- Methods: create, getAll, getById, update, delete
- Handle pagination for getAll
- Implement soft delete

### Step 4: Define Routes
- File: src/routes/tasks.ts
- GET /tasks - List all tasks (with pagination)
- GET /tasks/:id - Get single task
- POST /tasks - Create task
- PUT /tasks/:id - Update task
- DELETE /tasks/:id - Delete task

### Step 5: Add to Main Router
- Register task routes under /api/v1/tasks
- Apply auth middleware

## Verification Steps

### Unit Tests
- Test each controller method
- Test validator with valid/invalid inputs
- Test model constraints

### Integration Tests
```bash
# Create task
curl -X POST http://localhost:3000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high"}'

# List tasks
curl http://localhost:3000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN"
```

### Edge Cases
- [ ] Empty title rejected
- [ ] Invalid status rejected
- [ ] Pagination works correctly
- [ ] Unauthorized access blocked
```

---

## Example 2: Patch Mode - Bug Fix

### Input
```bash
bash scripts/codex-exec.sh --mode=patch "Fix the race condition in the database connection pool"
```

### Output
```markdown
## Summary

Fix race condition in database connection pool by implementing proper mutex locking and connection state management.

**Root Cause:**
Multiple concurrent requests can acquire the same connection before it's marked as in-use, leading to data corruption.

**Solution:**
Add mutex lock around connection acquisition and implement proper state transitions.

## Proposed Changes

### src/db/connectionPool.ts
\`\`\`diff
--- a/src/db/connectionPool.ts
+++ b/src/db/connectionPool.ts
@@ -1,5 +1,6 @@
 import { Pool, PoolClient } from 'pg';
+import { Mutex } from 'async-mutex';

 class ConnectionPool {
   private pool: Pool;
   private connections: Map<string, PoolClient> = new Map();
+  private mutex = new Mutex();

-  async acquire(): Promise<PoolClient> {
-    const connection = await this.pool.connect();
-    const id = generateId();
-    this.connections.set(id, connection);
-    return connection;
+  async acquire(): Promise<PoolClient> {
+    const release = await this.mutex.acquire();
+    try {
+      const connection = await this.pool.connect();
+      const id = generateId();
+      this.connections.set(id, connection);
+      return connection;
+    } finally {
+      release();
+    }
   }

-  async release(connection: PoolClient): Promise<void> {
-    connection.release();
+  async release(connection: PoolClient): Promise<void> {
+    const release = await this.mutex.acquire();
+    try {
+      connection.release();
+    } finally {
+      release();
+    }
   }
 }
\`\`\`

### package.json
\`\`\`diff
--- a/package.json
+++ b/package.json
@@ -15,6 +15,7 @@
   "dependencies": {
     "pg": "^8.11.0",
+    "async-mutex": "^0.4.0",
     "express": "^4.18.0"
   }
 }
\`\`\`

## Verification Steps

### Install New Dependency
\`\`\`bash
npm install async-mutex
\`\`\`

### Run Existing Tests
\`\`\`bash
npm test src/db/connectionPool.test.ts
\`\`\`

### Stress Test
\`\`\`bash
# Run concurrent connection test
npm run test:stress -- --concurrent=100 --duration=30s
\`\`\`

### Edge Cases
- [ ] 100 concurrent connections handled correctly
- [ ] No duplicate connection IDs
- [ ] Connections properly released on error
- [ ] Pool exhaustion handled gracefully
```

---

## Example 3: Architecture Review

### Input
```bash
bash scripts/codex-exec.sh "Review the current authentication architecture and suggest improvements"
```

### Output
```markdown
## Summary

Analysis of current authentication architecture reveals several areas for improvement in security, scalability, and maintainability.

**Current State:**
- Session-based auth with server-side storage
- Single database for session storage
- No rate limiting on login attempts

**Recommendations:**
- Migrate to JWT with refresh tokens
- Implement Redis for session/token storage
- Add rate limiting and brute force protection

## Implementation Approach

### Phase 1: Security Hardening (Immediate)
1. Add rate limiting to login endpoint
   - Max 5 attempts per minute per IP
   - Progressive delays after failures

2. Implement account lockout
   - Lock after 10 failed attempts
   - Require email verification to unlock

### Phase 2: JWT Migration (Short-term)
1. Implement JWT token generation
   - Access token: 15 minutes expiry
   - Refresh token: 7 days expiry

2. Add refresh token rotation
   - Issue new refresh token on each use
   - Invalidate old tokens

### Phase 3: Infrastructure (Medium-term)
1. Add Redis for token storage
   - Store refresh tokens
   - Enable token revocation

2. Implement token blacklist
   - Blacklist tokens on logout
   - Clean up expired entries

## Verification Steps

### Security Testing
\`\`\`bash
# Test rate limiting
for i in {1..10}; do
  curl -X POST http://localhost:3000/login \
    -d '{"email": "test@test.com", "password": "wrong"}'
done

# Verify rate limit response
# Should see 429 after 5 attempts
\`\`\`

### Load Testing
\`\`\`bash
# Test authentication under load
k6 run scripts/auth-load-test.js
\`\`\`

### Edge Cases
- [ ] Token refresh works correctly
- [ ] Expired tokens rejected
- [ ] Concurrent refresh requests handled
- [ ] Logout invalidates all tokens
```
