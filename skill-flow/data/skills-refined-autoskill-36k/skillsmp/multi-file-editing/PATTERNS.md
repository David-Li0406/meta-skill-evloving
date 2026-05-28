# Multi-File Editing Patterns

Common patterns for coordinated changes across codebases.

---

## Pattern 1: API Contract Changes

Changing an API affects multiple layers. Follow this order.

### Scenario: Add Required Request Field

**Change:** Add `organizationId` to `/users` POST endpoint.

#### Order of Operations

```
1. Types/Schemas (contracts)
   |
2. Backend API Handler
   |
3. Backend Service Layer
   |
4. Database Schema (if needed)
   |
5. Frontend API Client
   |
6. Frontend Components
   |
7. Tests (all layers)
```

#### Step-by-Step

**Step 1: Update Request Schema**

```typescript
// src/types/api/user.ts
interface CreateUserRequest {
  email: string;
  name: string;
  organizationId: string;  // NEW: Required field
}
```

**Step 2: Update API Handler**

```typescript
// src/routes/users.routes.ts
app.post('/users', async (req, res) => {
  const { email, name, organizationId } = req.body;
  // Validate organizationId exists
  const org = await organizationService.findById(organizationId);
  if (!org) {
    return res.status(400).json({ error: 'Invalid organization' });
  }
  // Continue with user creation
});
```

**Step 3: Update Service Layer**

```typescript
// src/services/user.service.ts
async function createUser(data: CreateUserRequest): Promise<User> {
  return userRepository.create({
    ...data,
    organizationId: data.organizationId,
  });
}
```

**Step 4: Update Frontend API Client**

```typescript
// src/api/users.ts
export async function createUser(data: CreateUserRequest): Promise<User> {
  return fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(data),
  }).then(r => r.json());
}
```

**Step 5: Update Frontend Components**

```typescript
// src/components/UserForm.tsx
function UserForm({ organizationId }: Props) {
  const handleSubmit = (formData: FormData) => {
    createUser({
      email: formData.get('email'),
      name: formData.get('name'),
      organizationId,  // Pass through from props
    });
  };
}
```

**Step 6: Update Tests**

```typescript
// tests/users.routes.test.ts
it('should require organizationId', async () => {
  const res = await request(app)
    .post('/users')
    .send({ email: 'test@example.com', name: 'Test' });
  expect(res.status).toBe(400);
});

it('should create user with organizationId', async () => {
  const res = await request(app)
    .post('/users')
    .send({
      email: 'test@example.com',
      name: 'Test',
      organizationId: 'org-123',
    });
  expect(res.status).toBe(201);
});
```

### Checklist: API Contract Change

- [ ] Schema/types updated
- [ ] API handler validates new field
- [ ] Service layer uses new field
- [ ] Database schema updated (if needed)
- [ ] Frontend API client updated
- [ ] Frontend components pass new field
- [ ] Backend tests updated
- [ ] Frontend tests updated
- [ ] API documentation updated

---

## Pattern 2: Interface/Type Updates

Changing shared types ripples through the codebase.

### Scenario: Add Property to Interface

**Change:** Add `status` field to `Project` interface.

#### Identify Impact

```bash
# Find all files using Project type
rg "Project" --type ts -l

# Find direct imports
rg "import.*Project" --type ts
```

#### Order of Operations

```
1. Interface definition
   |
2. Factory/builder functions
   |
3. Database queries (if persisted)
   |
4. API response formatting
   |
5. Components using the type
   |
6. Tests with mock data
```

#### Step-by-Step

**Step 1: Update Interface**

```typescript
// src/types/project.ts
interface Project {
  id: string;
  name: string;
  status: 'active' | 'archived' | 'draft';  // NEW
  createdAt: Date;
}
```

**Step 2: Update Factory Functions**

```typescript
// src/factories/project.factory.ts
function createProject(data: CreateProjectInput): Project {
  return {
    id: generateId(),
    name: data.name,
    status: data.status ?? 'draft',  // Default value
    createdAt: new Date(),
  };
}
```

**Step 3: Update Database Queries**

```typescript
// src/repositories/project.repository.ts
async function findById(id: string): Promise<Project | null> {
  const row = await db.query('SELECT * FROM projects WHERE id = ?', [id]);
  return row ? {
    id: row.id,
    name: row.name,
    status: row.status,  // Include new field
    createdAt: row.created_at,
  } : null;
}
```

**Step 4: Update API Responses**

```typescript
// src/routes/projects.routes.ts
app.get('/projects/:id', async (req, res) => {
  const project = await projectService.findById(req.params.id);
  res.json({
    id: project.id,
    name: project.name,
    status: project.status,  // Include in response
    createdAt: project.createdAt,
  });
});
```

**Step 5: Update Components**

```typescript
// src/components/ProjectCard.tsx
function ProjectCard({ project }: { project: Project }) {
  return (
    <div>
      <h3>{project.name}</h3>
      <Badge>{project.status}</Badge>  {/* Display new field */}
    </div>
  );
}
```

**Step 6: Update Test Mocks**

```typescript
// tests/fixtures/projects.ts
export const mockProject: Project = {
  id: 'proj-1',
  name: 'Test Project',
  status: 'active',  // Include in mocks
  createdAt: new Date('2024-01-01'),
};
```

### Checklist: Interface Update

- [ ] Interface definition updated
- [ ] Factory functions include new property
- [ ] Database queries return new property
- [ ] API responses include new property
- [ ] Components handle new property
- [ ] Test fixtures include new property
- [ ] Default value defined (if optional)
- [ ] Migration created (if database)

---

## Pattern 3: Database Migrations

Schema changes require coordinated updates across layers.

### Scenario: Add Column to Table

**Change:** Add `deleted_at` column for soft deletes.

#### Order of Operations

```
1. Create migration file
   |
2. Update ORM/repository
   |
3. Update service layer
   |
4. Update API (filter deleted)
   |
5. Update types/interfaces
   |
6. Run migration
   |
7. Update tests
```

#### Step-by-Step

**Step 1: Create Migration**

```typescript
// migrations/20240115_add_deleted_at_to_users.ts
export async function up(db: Database) {
  await db.exec(`
    ALTER TABLE users
    ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL
  `);
}

export async function down(db: Database) {
  await db.exec(`
    ALTER TABLE users
    DROP COLUMN deleted_at
  `);
}
```

**Step 2: Update Repository**

```typescript
// src/repositories/user.repository.ts
async function findAll(): Promise<User[]> {
  // Filter out soft-deleted records
  return db.query('SELECT * FROM users WHERE deleted_at IS NULL');
}

async function softDelete(id: string): Promise<void> {
  await db.query(
    'UPDATE users SET deleted_at = ? WHERE id = ?',
    [new Date(), id]
  );
}
```

**Step 3: Update Service**

```typescript
// src/services/user.service.ts
async function deleteUser(id: string): Promise<void> {
  // Use soft delete instead of hard delete
  await userRepository.softDelete(id);
}

async function getActiveUsers(): Promise<User[]> {
  return userRepository.findAll();  // Already filtered
}
```

**Step 4: Update Types**

```typescript
// src/types/user.ts
interface User {
  id: string;
  email: string;
  name: string;
  deletedAt: Date | null;  // NEW: Soft delete timestamp
  createdAt: Date;
}
```

**Step 5: Update API**

```typescript
// src/routes/users.routes.ts
app.delete('/users/:id', async (req, res) => {
  await userService.deleteUser(req.params.id);
  res.status(204).send();  // Soft delete, not 200 with body
});
```

**Step 6: Run Migration**

```bash
bun run db:migrate
```

**Step 7: Update Tests**

```typescript
// tests/user.repository.test.ts
describe('softDelete', () => {
  it('should set deleted_at timestamp', async () => {
    const user = await createTestUser();
    await userRepository.softDelete(user.id);

    const deleted = await db.query(
      'SELECT deleted_at FROM users WHERE id = ?',
      [user.id]
    );
    expect(deleted.deleted_at).not.toBeNull();
  });

  it('should exclude from findAll', async () => {
    const user = await createTestUser();
    await userRepository.softDelete(user.id);

    const users = await userRepository.findAll();
    expect(users.find(u => u.id === user.id)).toBeUndefined();
  });
});
```

### Checklist: Database Migration

- [ ] Migration file created
- [ ] Rollback (down) migration works
- [ ] Repository queries updated
- [ ] Service layer updated
- [ ] API endpoints updated
- [ ] Types/interfaces updated
- [ ] Migration tested locally
- [ ] Tests updated
- [ ] Migration deployed to staging

---

## Pattern 4: Import/Export Updates

Restructuring module exports requires careful coordination.

### Scenario: Extract to New Module

**Change:** Move date utilities from `utils.ts` to `date.utils.ts`.

#### Order of Operations

```
1. Create new module with exports
   |
2. Re-export from old location (backward compat)
   |
3. Update imports in consuming files
   |
4. Remove re-exports from old location
   |
5. Delete old code (if moved)
```

#### Step-by-Step

**Step 1: Create New Module**

```typescript
// src/utils/date.utils.ts (NEW FILE)
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}

export function parseDate(str: string): Date {
  return new Date(str);
}

export function addDays(date: Date, days: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}
```

**Step 2: Re-export for Backward Compatibility**

```typescript
// src/utils/utils.ts (EXISTING FILE)
// Keep old exports working during transition
export { formatDate, parseDate, addDays } from './date.utils';

// Other non-date utilities remain here
export function generateId(): string {
  return crypto.randomUUID();
}
```

**Step 3: Update Imports Gradually**

```bash
# Find all files importing date functions from utils
rg "from.*utils.*formatDate|parseDate|addDays" --type ts -l
```

```typescript
// BEFORE
import { formatDate, generateId } from '../utils/utils';

// AFTER
import { formatDate } from '../utils/date.utils';
import { generateId } from '../utils/utils';
```

**Step 4: Remove Re-exports**

Once all imports updated:

```typescript
// src/utils/utils.ts
// Remove the re-exports
// export { formatDate, parseDate, addDays } from './date.utils';

export function generateId(): string {
  return crypto.randomUUID();
}
```

**Step 5: Verify No Broken Imports**

```bash
bun run typecheck
bun test
```

### Checklist: Module Restructure

- [ ] New module created with exports
- [ ] Re-exports added for backward compatibility
- [ ] Consuming files identified
- [ ] Imports updated in all files
- [ ] Re-exports removed
- [ ] Type check passes
- [ ] All tests pass
- [ ] No runtime import errors

---

## Pattern 5: Bulk Symbol Rename

Renaming symbols across the codebase safely.

### Scenario: Rename Function

**Change:** Rename `getUserData` to `getUserProfile`.

#### Finding All Occurrences

```bash
# Find definition and usages
rg "getUserData" --type ts

# Find just files
rg -l "getUserData" --type ts

# Count occurrences per file
rg -c "getUserData" --type ts
```

#### Order of Operations

```
1. Rename in definition file
   |
2. Update exports (if named export)
   |
3. Update imports in consuming files
   |
4. Update call sites in consuming files
   |
5. Update test files
   |
6. Search for string references
```

#### Step-by-Step

**Step 1: Rename Definition**

```typescript
// src/services/user.service.ts
// BEFORE
export async function getUserData(id: string): Promise<UserData> { ... }

// AFTER
export async function getUserProfile(id: string): Promise<UserProfile> { ... }
```

**Step 2: Update Named Exports (if barrel file)**

```typescript
// src/services/index.ts
// BEFORE
export { getUserData } from './user.service';

// AFTER
export { getUserProfile } from './user.service';
```

**Step 3: Update Imports**

```typescript
// src/routes/user.routes.ts
// BEFORE
import { getUserData } from '../services/user.service';

// AFTER
import { getUserProfile } from '../services/user.service';
```

**Step 4: Update Call Sites**

```typescript
// src/routes/user.routes.ts
// BEFORE
const userData = await getUserData(userId);

// AFTER
const userProfile = await getUserProfile(userId);
```

**Step 5: Update Tests**

```typescript
// tests/user.service.test.ts
// BEFORE
describe('getUserData', () => { ... });

// AFTER
describe('getUserProfile', () => { ... });
```

**Step 6: Check String References**

```bash
# Look for the name in strings (API paths, logs, etc.)
rg "getUserData" --type ts

# Check for no remaining references
rg "getUserData" --type ts
# Should return nothing
```

### Checklist: Symbol Rename

- [ ] All occurrences found with rg
- [ ] Definition renamed
- [ ] Exports updated
- [ ] All imports updated
- [ ] All call sites updated
- [ ] Tests updated
- [ ] String references updated
- [ ] No remaining occurrences
- [ ] Type check passes
- [ ] Tests pass

---

## Pattern 6: Cross-Package Changes (Monorepo)

Changes spanning multiple packages in a monorepo.

### Scenario: Update Shared Package

**Change:** Add field to shared `User` type in `@repo/types` package.

#### Order of Operations

```
1. Update shared package
   |
2. Build shared package
   |
3. Update consuming packages (in dependency order)
   |
4. Build and test all packages
```

#### Step-by-Step

**Step 1: Update Shared Package**

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  role: 'admin' | 'user';  // NEW FIELD
}
```

**Step 2: Build Shared Package**

```bash
cd packages/types
bun run build
```

**Step 3: Update API Package**

```typescript
// packages/api/src/routes/users.ts
import { User } from '@repo/types';

app.post('/users', (req, res) => {
  const user: User = {
    id: generateId(),
    email: req.body.email,
    role: req.body.role ?? 'user',  // Handle new field
  };
});
```

**Step 4: Update Web Package**

```typescript
// packages/web/src/components/UserBadge.tsx
import { User } from '@repo/types';

function UserBadge({ user }: { user: User }) {
  return (
    <Badge variant={user.role === 'admin' ? 'red' : 'blue'}>
      {user.role}
    </Badge>
  );
}
```

**Step 5: Build and Test All**

```bash
# From monorepo root
bun run build
bun test
```

### Checklist: Monorepo Change

- [ ] Shared package updated
- [ ] Shared package builds
- [ ] Consuming packages identified
- [ ] Each consuming package updated
- [ ] Each consuming package builds
- [ ] All tests pass
- [ ] Integration tests pass
- [ ] Changeset/version bump (if publishing)
