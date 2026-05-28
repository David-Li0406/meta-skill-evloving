# Coherence Anti-Patterns

Common mistakes in out-of-order implementation that cause rework and bugs.

---

## Anti-Pattern 1: Building UI Before API

### The Problem

Implementing frontend components before backend API endpoints exist.

### Example

```typescript
// ❌ BAD: Implementing UserList component first

// File: src/components/UserList.tsx (implemented today)
export function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users')  // ← This API doesn't exist yet!
      .then(res => res.json())
      .then(setUsers);
  }, []);

  return users.map(user => <UserCard user={user} />);
}

// File: src/routes/users.ts (not implemented yet)
// TODO: Implement GET /api/users endpoint
```

### The Consequence

- Frontend code written based on assumptions about API response
- API implemented later with different response structure
- Frontend breaks, requires rework
- Time wasted on double implementation

### The Solution

```typescript
// ✅ GOOD: Implement API first, then frontend

// Step 1: Implement API (Day 1)
// File: src/routes/users.ts
router.get('/users', async (req, res) => {
  const users = await userService.getAll();
  res.json(users);  // Response: [{ id, name, email }]
});

// Step 2: Test API (Day 1)
// $ curl http://localhost:3000/api/users
// [{ "id": "1", "name": "John", "email": "john@example.com" }]

// Step 3: Implement frontend (Day 2)
// File: src/components/UserList.tsx
export function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users')  // ← API exists and tested!
      .then(res => res.json())
      .then(setUsers);
  }, []);

  return users.map(user => <UserCard user={user} />);
}
```

### Detection

```bash
# Find frontend API calls
grep -r "fetch('/api/" src/components/

# Check if API endpoints exist
grep -r "router.get('/api/" src/routes/

# If frontend calls API that doesn't exist in routes → ANTI-PATTERN
```

---

## Anti-Pattern 2: Building API Before Types

### The Problem

Implementing API endpoints before defining shared types/interfaces.

### Example

```typescript
// ❌ BAD: API uses inline types

// File: src/routes/users.ts (implemented first)
router.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json({
    userId: user.id,      // ← Inconsistent field naming
    userName: user.name,
    userEmail: user.email
  });
});

// Later: Frontend expects different structure
// File: src/components/UserProfile.tsx (implemented later)
interface User {
  id: string;      // ← Expects 'id', not 'userId'
  name: string;    // ← Expects 'name', not 'userName'
  email: string;
}
// Result: Mismatch causes runtime errors
```

### The Consequence

- Each layer defines its own types independently
- Type inconsistencies between layers
- Runtime errors due to field name mismatches
- Difficult to refactor (no single source of truth)

### The Solution

```typescript
// ✅ GOOD: Define types first, then use everywhere

// Step 1: Define shared types (Day 1)
// File: src/types/user.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface CreateUserDTO {
  name: string;
  email: string;
}

// Step 2: Use types in API (Day 2)
// File: src/routes/users.ts
import { User } from '../types/user';

router.get('/users/:id', async (req, res) => {
  const user: User = await userService.getById(req.params.id);
  res.json(user);  // Type-safe, matches User interface
});

// Step 3: Use types in frontend (Day 3)
// File: src/components/UserProfile.tsx
import { User } from '../types/user';

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);  // Same type!

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then((data: User) => setUser(data));  // Type-safe
  }, [userId]);

  return <div>{user?.name}</div>;  // TypeScript validates fields
}
```

### Detection

```bash
# Find API routes without type imports
grep -L "import.*{.*}" src/routes/*.ts

# Find inline response objects (potential type mismatch)
grep -r "res.json({" src/routes/

# Recommendation: Check if types defined in src/types/
```

---

## Anti-Pattern 3: Building Service Before Repository

### The Problem

Implementing business logic (service layer) before data access (repository layer).

### Example

```typescript
// ❌ BAD: Service implemented first

// File: src/services/userService.ts (implemented first)
export class UserService {
  async getUser(id: string) {
    // Directly querying database without repository
    const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return user;
  }

  async createUser(data: CreateUserDTO) {
    // Direct database access
    const user = await db.insert('users', data);
    return user;
  }
}

// Problem: Service tightly coupled to database
// Can't swap data sources, hard to test
```

### The Consequence

- Service layer tightly coupled to database implementation
- Hard to test (requires actual database)
- Can't swap data sources (Redis, API, etc.)
- Violates separation of concerns

### The Solution

```typescript
// ✅ GOOD: Repository first, then service

// Step 1: Implement repository (Day 1)
// File: src/repositories/userRepository.ts
export class UserRepository {
  async findById(id: string): Promise<User | null> {
    return db.users.findUnique({ where: { id } });
  }

  async create(data: CreateUserDTO): Promise<User> {
    return db.users.create({ data });
  }
}

// Step 2: Implement service using repository (Day 2)
// File: src/services/userService.ts
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async createUser(data: CreateUserDTO): Promise<User> {
    // Business logic: validate email
    if (!this.isValidEmail(data.email)) {
      throw new Error('Invalid email');
    }
    return this.userRepository.create(data);
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

### Detection

```bash
# Find services that directly access database
grep -r "db\.\(query\|insert\|update\|delete\)" src/services/

# Should use repository instead
# Expected: userRepository.findById() not db.query()
```

---

## Anti-Pattern 4: Building Database Schema Last

### The Problem

Implementing application code before database schema exists.

### Example

```typescript
// ❌ BAD: Code written assuming schema exists

// File: src/repositories/userRepository.ts (implemented first)
export class UserRepository {
  async findById(id: string) {
    return db.users.findUnique({ where: { id } });
    //     ↑
    //     Assumes 'users' table exists - but it doesn't!
  }
}

// File: migrations/ (empty - no migrations run yet)
// Result: Code crashes at runtime - table doesn't exist
```

### The Consequence

- Code written but can't run (database error)
- Can't test implementation
- Discover schema issues too late
- Have to retrofit schema changes into existing code

### The Solution

```sql
-- ✅ GOOD: Database schema first

-- Step 1: Create schema (Day 1)
-- File: migrations/001_create_users_table.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Step 2: Run migration
-- $ npm run migrate
-- ✅ Table created

-- Step 3: Implement repository (Day 2)
-- File: src/repositories/userRepository.ts
export class UserRepository {
  async findById(id: string) {
    return db.users.findUnique({ where: { id } });
    //     ↑
    //     Table exists! Code works!
  }
}
```

### Detection

```bash
# Find repository/model references
grep -r "db\.[a-zA-Z_]*\." src/repositories/

# Check if migrations exist for each table
ls migrations/ | grep -E "create.*table"

# If repositories reference tables not in migrations → ANTI-PATTERN
```

---

## Anti-Pattern 5: Skipping API Testing Before Integration

### The Problem

Integrating frontend to backend API without testing API first.

### Example

```typescript
// ❌ BAD: API implemented but not tested

// File: src/routes/users.ts (implemented)
router.post('/users', async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json(user);
});

// Frontend immediately integrates (same day)
// File: src/api/userApi.ts
export async function createUser(data: CreateUserDTO) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response.json();
}

// Problem: API has bugs, frontend also breaks
// Bug discovered: API doesn't validate email format
// Now both API and frontend need fixes
```

### The Consequence

- API bugs discovered during frontend integration
- Frontend code needs rework due to API changes
- Debugging is harder (backend bug vs frontend bug?)
- Double the rework

### The Solution

```bash
# ✅ GOOD: Test API before integration

# Step 1: Implement API (Day 1)
# File: src/routes/users.ts
router.post('/users', async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json(user);
});

# Step 2: Test API thoroughly (Day 1)
$ curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'

# Response: {"id":"123","name":"Test","email":"test@example.com"}
# ✅ Works!

# Test error cases
$ curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"invalid-email"}'

# Response: {"error":"Invalid email format"}
# ✅ Error handling works!

# Step 3: Document API contract (Day 1)
# See: API_CONTRACT.md

# Step 4: Implement frontend (Day 2)
# File: src/api/userApi.ts
# Now implementation matches tested API behavior
```

### Detection

```bash
# Find API routes
grep -r "router\.\(get\|post\|put\|delete\)" src/routes/

# Check if tests exist
find tests/ -name "*api*.test.ts" -o -name "*routes*.test.ts"

# If routes exist but no tests → ANTI-PATTERN
```

---

## Anti-Pattern 6: Parallel Implementation Without Communication

### The Problem

Multiple developers/agents working on different layers simultaneously without coordination.

### Example

```typescript
// ❌ BAD: Two agents working simultaneously without coordination

// Agent 1 (Backend): Implements API (10:00 AM)
// File: src/routes/users.ts
router.get('/users', async (req, res) => {
  const users = await userService.getAll();
  res.json({
    data: users,           // ← Nested under 'data'
    total: users.length
  });
});

// Agent 2 (Frontend): Implements UI (10:00 AM - parallel!)
// File: src/components/UserList.tsx
const response = await fetch('/api/users');
const users = await response.json();  // ← Expects flat array!
setUsers(users);  // ← users is { data, total }, not array!

// Result: Runtime error, frontend displays "undefined"
```

### The Consequence

- Integration fails due to assumptions
- Both implementations need rework
- Time wasted on parallel work
- Merge conflicts

### The Solution

```typescript
// ✅ GOOD: Sequential implementation with contract-first approach

// Step 1: Define contract FIRST (10:00 AM)
// File: API_CONTRACT.md
/**
 * GET /api/users
 *
 * Response:
 * {
 *   "data": User[],
 *   "total": number
 * }
 */

// Step 2: Backend implements contract (10:15 AM)
// File: src/routes/users.ts
router.get('/users', async (req, res) => {
  const users = await userService.getAll();
  res.json({
    data: users,
    total: users.length
  });
});

// Step 3: Backend tests and confirms (10:30 AM)
// $ curl http://localhost:3000/api/users
// {"data":[...],"total":5}
// ✅ Matches contract!

// Step 4: Frontend implements using contract (11:00 AM)
// File: src/components/UserList.tsx
const response = await fetch('/api/users');
const { data: users, total } = await response.json();  // ← Matches contract!
setUsers(users);
```

### Detection

```bash
# Check git history for simultaneous commits
git log --all --since="1 day ago" --pretty=format:"%h %an %s" | grep -E "(routes|components)"

# If routes and components committed at same time → POTENTIAL ANTI-PATTERN
# Check if contract was defined first
```

---

## Anti-Pattern 7: Assuming Future Implementations

### The Problem

Writing code that depends on features not yet implemented.

### Example

```typescript
// ❌ BAD: Assuming caching layer exists

// File: src/services/userService.ts
export class UserService {
  async getUser(id: string) {
    // Check cache first
    const cached = await cacheService.get(`user:${id}`);
    //                  ↑
    //                  cacheService doesn't exist yet!

    if (cached) return cached;

    const user = await userRepository.findById(id);

    // Cache for next time
    await cacheService.set(`user:${id}`, user);

    return user;
  }
}

// File: src/services/cacheService.ts (not implemented yet)
// TODO: Implement Redis caching

// Result: Code crashes - cacheService is undefined
```

### The Consequence

- Code can't run without future implementation
- Blocks testing and development
- Creates false dependency

### The Solution

```typescript
// ✅ GOOD: Implement without dependencies first, add enhancements later

// Step 1: Implement basic version (Day 1)
// File: src/services/userService.ts
export class UserService {
  async getUser(id: string) {
    return userRepository.findById(id);  // Simple, works now
  }
}

// Step 2: Test and deploy basic version (Day 1)
// ✅ Works without caching

// Step 3: Add caching later (Day 5 - after cache service implemented)
// File: src/services/userService.ts
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private cacheService?: CacheService  // ← Optional!
  ) {}

  async getUser(id: string) {
    // Only use cache if available
    if (this.cacheService) {
      const cached = await this.cacheService.get(`user:${id}`);
      if (cached) return cached;
    }

    const user = await this.userRepository.findById(id);

    // Cache if service available
    if (this.cacheService) {
      await this.cacheService.set(`user:${id}`, user);
    }

    return user;
  }
}
```

### Detection

```bash
# Find imports that don't exist
grep -r "import.*from" src/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  import=$(echo "$line" | grep -oP "from ['\"]\K[^'\"]+")

  if [[ ! -f "$import" ]]; then
    echo "MISSING IMPORT: $file imports $import (doesn't exist)"
  fi
done
```

---

## Anti-Pattern 8: Ignoring Existing Patterns

### The Problem

Implementing new features without checking how similar features are implemented.

### Example

```typescript
// ❌ BAD: New feature ignores existing pattern

// Existing code (already implemented)
// File: src/routes/users.ts
router.get('/users/:id', authenticateUser, async (req, res) => {
  try {
    const user = await userService.getById(req.params.id);
    res.json({ data: user });  // ← Wraps in { data }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// New feature (implemented today)
// File: src/routes/posts.ts
router.get('/posts/:id', async (req, res) => {
  const post = await postService.getById(req.params.id);
  res.json(post);  // ← Returns unwrapped! Different pattern!
});
// No authentication middleware!
// No error handling!
// Different response structure!

// Result: Inconsistent API behavior
```

### The Consequence

- Inconsistent API behavior
- Frontend needs different handling for each endpoint
- Security vulnerabilities (forgot authentication)
- Hard to maintain

### The Solution

```typescript
// ✅ GOOD: Follow existing patterns

// Step 1: Review existing implementation (Day 1)
// Read: src/routes/users.ts
// Pattern identified:
// - Use authenticateUser middleware
// - Wrap response in { data }
// - Try-catch for error handling

// Step 2: Implement new feature following pattern (Day 1)
// File: src/routes/posts.ts
router.get('/posts/:id', authenticateUser, async (req, res) => {
  //                     ↑ Same middleware as users
  try {
    const post = await postService.getById(req.params.id);
    res.json({ data: post });  // ← Same response structure
  } catch (error) {
    res.status(500).json({ error: error.message });  // ← Same error handling
  }
});

// ✅ Consistent with existing code!
```

### Detection

```bash
# Find routes without authentication
grep -r "router\.\(get\|post\|put\|delete\)" src/routes/ | grep -v "authenticate"

# Find routes without error handling
grep -r "router\.\(get\|post\)" src/routes/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  if ! grep -q "try.*catch" "$file"; then
    echo "MISSING ERROR HANDLING: $file"
  fi
done
```

---

## Summary: Dependency Order Rules

**Correct Implementation Order**:

```
1. Database Schema (migrations)
   ↓
2. Type Definitions (interfaces, DTOs)
   ↓
3. Repository Layer (data access)
   ↓
4. Service Layer (business logic)
   ↓
5. API Endpoints (controllers, routes)
   ↓
6. Test API (verify contracts)
   ↓
7. Frontend API Clients
   ↓
8. UI Components
```

**Anti-Pattern Detection Checklist**:

- [ ] Check if UI implemented before API → ANTI-PATTERN #1
- [ ] Check if API lacks type definitions → ANTI-PATTERN #2
- [ ] Check if service directly accesses database → ANTI-PATTERN #3
- [ ] Check if code references non-existent tables → ANTI-PATTERN #4
- [ ] Check if API not tested before frontend integration → ANTI-PATTERN #5
- [ ] Check if parallel work without coordination → ANTI-PATTERN #6
- [ ] Check if code assumes future implementations → ANTI-PATTERN #7
- [ ] Check if new code ignores existing patterns → ANTI-PATTERN #8

---

**Last Updated**: 2025-01-30
