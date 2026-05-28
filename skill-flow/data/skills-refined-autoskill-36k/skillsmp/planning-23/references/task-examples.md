# Task Decomposition Examples

## Example 1: OAuth Authentication Feature

**Goal**: "Add OAuth authentication with Google"

### Task Breakdown

```
Wave 1 (Parallel - no dependencies):
├─ Task 1: Setup NextAuth.js [standard]
│  └─ Install nextauth, create config, add env vars
│
└─ Task 2: Create user database schema [standard]
   └─ Add User model with OAuth fields

Wave 2 (After Wave 1):
├─ Task 3: Implement auth API routes [standard]
│  └─ Depends on: [1]
│  └─ /api/auth/[...nextauth]/route.ts
│
├─ Task 4: Add session provider [standard]
│  └─ Depends on: [1]
│  └─ Wrap app with SessionProvider in layout.tsx
│
└─ Task 5: Create login UI [standard]
   └─ Depends on: [1, 4]
   └─ Login button, callback page

Wave 3 (Verification):
└─ Task 6: [VERIFY] Auth integration [complex]
   └─ Depends on: [1, 2, 3, 4, 5]
   └─ Test OAuth flow, session persistence, logout
```

### Script Commands

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/src/scripts"

# Wave 1 - Independent
bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "1" \
  --subject "Setup NextAuth.js configuration" \
  --description "Install next-auth@5, create auth config with Google provider, add environment variables" \
  --complexity standard \
  --criteria "next-auth installed|auth.ts config created|GOOGLE_CLIENT_ID in .env"

bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "2" \
  --subject "Create user database schema" \
  --description "Add User model to Prisma schema with OAuth fields (id, email, name, image, provider)" \
  --complexity standard \
  --criteria "Schema updated|Migration created|Types generated"

# Wave 2 - Sequential
bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "3" \
  --subject "Implement auth API routes" \
  --description "Create /api/auth/[...nextauth]/route.ts with NextAuth handler" \
  --blocked-by "1" \
  --complexity standard \
  --criteria "Route file created|Auth endpoints respond 200"

bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "4" \
  --subject "Add session provider to app" \
  --description "Wrap root layout with SessionProvider from next-auth/react" \
  --blocked-by "1" \
  --complexity standard \
  --criteria "SessionProvider added|useSession hook works"

bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "5" \
  --subject "Create login UI components" \
  --description "Add login button, callback page, user menu with signOut" \
  --blocked-by "1,4" \
  --complexity standard \
  --criteria "Login button works|Callback page created|User menu functional"

# Wave 3 - Verification
bun $SCRIPTS/task-create.js --session ${CLAUDE_SESSION_ID} \
  --id "verify" \
  --subject "[VERIFY] OAuth authentication integration" \
  --description "Verify complete OAuth flow: login, session persistence, user data storage, logout" \
  --blocked-by "1,2,3,4,5" \
  --complexity complex \
  --criteria "OAuth login succeeds|Session persists across refreshes|User data in DB|Logout works"
```

---

## Example 2: Database Migration (Prisma)

**Goal**: "Migrate from direct SQL to Prisma ORM"

### Task Breakdown

```
Wave 1 (Foundation):
└─ Task 1: Setup Prisma and define schema [standard]
   └─ Install prisma, create schema from existing tables

Wave 2 (Migration):
├─ Task 2: Migrate user queries [standard]
│  └─ Depends on: [1]
│  └─ Replace SQL in user.service.ts
│
├─ Task 3: Migrate post queries [standard]
│  └─ Depends on: [1]
│  └─ Replace SQL in post.service.ts
│
└─ Task 4: Migrate auth queries [standard]
   └─ Depends on: [1]
   └─ Replace SQL in auth.service.ts

Wave 3 (Testing):
├─ Task 5: Update unit tests [standard]
│  └─ Depends on: [2, 3, 4]
│  └─ Mock Prisma client in tests
│
└─ Task 6: Update integration tests [standard]
   └─ Depends on: [2, 3, 4]
   └─ Use test database with Prisma

Wave 4 (Verification):
└─ Task 7: [VERIFY] Migration complete [complex]
   └─ Depends on: [all]
   └─ All queries work, tests pass, no SQL strings remain
```

**Key Considerations**:
- Task 1 must complete first (foundation)
- Tasks 2-4 can run in parallel (independent services)
- Tasks 5-6 can run in parallel (different test types)
- Task 7 verifies everything together

---

## Example 3: REST API Endpoints

**Goal**: "Add CRUD endpoints for products"

### Task Breakdown

```
Wave 1 (Model):
└─ Task 1: Create product model [standard]
   └─ Schema, types, validation

Wave 2 (API Routes - Parallel):
├─ Task 2: Create GET endpoints [standard]
│  └─ GET /products, GET /products/:id
│
├─ Task 3: Create POST endpoint [standard]
│  └─ POST /products with validation
│
├─ Task 4: Create PUT endpoint [standard]
│  └─ PUT /products/:id
│
└─ Task 5: Create DELETE endpoint [standard]
   └─ DELETE /products/:id

Wave 3 (Tests - Parallel):
├─ Task 6: Unit tests [standard]
│  └─ Test service functions
│
└─ Task 7: Integration tests [standard]
   └─ Test API endpoints

Wave 4 (Verification):
└─ Task 8: [VERIFY] API complete [complex]
   └─ All endpoints work, tests pass
```

---

## Task Granularity Rules

| Rule                       | Guideline                     |
| -------------------------- | ----------------------------- |
| One task = one deliverable | Single focused outcome        |
| Max time                   | ~30 minutes of work           |
| Single worker              | Can be completed by one agent |
| Testable                   | Has clear success criteria    |

---

## Complexity Guidelines

| Complexity | Model  | When to Use                                           |
| ---------- | ------ | ----------------------------------------------------- |
| `standard` | sonnet | CRUD, simple features, tests, straightforward changes |
| `complex`  | opus   | Architecture, security, algorithms, 5+ files          |

---

## Dependency Patterns

```
Independent tasks      → blockedBy: []     (parallel)
Sequential dependency  → blockedBy: ["1"]  (after task 1)
Multi-dependency      → blockedBy: ["1","2"] (after both)
Verify task           → blockedBy: [all]   (after everything)
```
