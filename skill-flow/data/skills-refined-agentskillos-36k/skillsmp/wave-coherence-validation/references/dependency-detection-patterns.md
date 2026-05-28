# Dependency Detection Patterns

Common code patterns for detecting dependencies across different layers and technologies.

---

## Database Layer

### PostgreSQL/MySQL Migrations

```sql
-- Pattern: Table creation
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Detection command:
grep -r "CREATE TABLE" migrations/
```

### TypeScript/Prisma Schema

```typescript
// Pattern: Prisma model
model User {
  id    String @id @default(uuid())
  name  String
  email String @unique
}

// Detection command:
grep -r "model " prisma/schema.prisma
```

### MongoDB Schema

```typescript
// Pattern: Mongoose schema
const userSchema = new Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true }
});

// Detection command:
grep -r "new Schema" --include="*.ts" --include="*.js"
```

---

## Type Definitions / DTOs

### TypeScript Interfaces

```typescript
// Pattern: Interface export
export interface User {
  id: string;
  name: string;
  email: string;
}

// Detection command:
grep -r "export interface" --include="*.ts"
```

### TypeScript Types

```typescript
// Pattern: Type alias export
export type CreateUserDTO = {
  name: string;
  email: string;
};

// Detection command:
grep -r "export type" --include="*.ts"
```

### Java DTOs

```java
// Pattern: DTO class
public class UserDTO {
    private String id;
    private String name;
    private String email;
}

// Detection command:
grep -r "class.*DTO" --include="*.java"
```

---

## Repository / Data Access Layer

### TypeScript Repository Pattern

```typescript
// Pattern: Repository class
export class UserRepository {
  async findById(id: string): Promise<User> { }
  async create(data: CreateUserDTO): Promise<User> { }
}

// Detection command:
grep -r "class.*Repository" --include="*.ts"
```

### Python Repository Pattern

```python
# Pattern: Repository class
class UserRepository:
    def find_by_id(self, user_id: str) -> User:
        pass

    def create(self, data: dict) -> User:
        pass

# Detection command:
grep -r "class.*Repository" --include="*.py"
```

### Java JPA Repository

```java
// Pattern: JPA repository interface
public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findByEmail(String email);
}

// Detection command:
grep -r "interface.*Repository.*extends" --include="*.java"
```

---

## Service / Business Logic Layer

### TypeScript Service Pattern

```typescript
// Pattern: Service class
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUser(id: string): Promise<User> {
    return this.userRepository.findById(id);
  }
}

// Detection command:
grep -r "class.*Service" --include="*.ts"
```

### Python Service Pattern

```python
# Pattern: Service class
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> User:
        return self.user_repository.find_by_id(user_id)

# Detection command:
grep -r "class.*Service" --include="*.py"
```

### Dependency: Repository Injection

```typescript
// Pattern: Service depends on Repository
constructor(private userRepository: UserRepository) {}
//                  ↑
//                  Dependency on UserRepository

// Detection: Find constructor dependencies
grep -A 1 "constructor" src/services/*.ts | grep "Repository"
```

---

## API / Controller Layer

### Express.js Routes (Node.js)

```typescript
// Pattern: Route definitions
router.get('/users/:id', async (req, res) => { });
router.post('/users', async (req, res) => { });

// Detection command:
grep -r "router\.\(get\|post\|put\|delete\|patch\)" --include="*.ts" --include="*.js"
```

### NestJS Controllers

```typescript
// Pattern: Controller decorators
@Controller('users')
export class UserController {
  @Get(':id')
  async getUser(@Param('id') id: string) { }

  @Post()
  async createUser(@Body() data: CreateUserDTO) { }
}

// Detection command:
grep -r "@\(Get\|Post\|Put\|Delete\|Patch\)" --include="*.ts"
```

### Python FastAPI

```python
# Pattern: FastAPI route decorators
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> User:
    pass

@app.post("/users")
async def create_user(data: CreateUserDTO) -> User:
    pass

# Detection command:
grep -r "@app\.\(get\|post\|put\|delete\|patch\)" --include="*.py"
```

### Java Spring Controllers

```java
// Pattern: Spring controller
@RestController
@RequestMapping("/users")
public class UserController {
    @GetMapping("/{id}")
    public User getUser(@PathVariable UUID id) { }

    @PostMapping
    public User createUser(@RequestBody CreateUserDTO data) { }
}

// Detection command:
grep -r "@\(GetMapping\|PostMapping\|PutMapping\|DeleteMapping\)" --include="*.java"
```

### Dependency: Service Injection

```typescript
// Pattern: Controller depends on Service
constructor(private userService: UserService) {}
//                  ↑
//                  Dependency on UserService

// Detection: Find controller dependencies
grep -A 1 "constructor" src/controllers/*.ts | grep "Service"
```

---

## Frontend API Clients

### Fetch API (React/Vue)

```typescript
// Pattern: API client function
export async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Detection command:
grep -r "fetch(" --include="*.tsx" --include="*.jsx" --include="*.ts"
```

### Axios (React/Vue)

```typescript
// Pattern: Axios calls
export const userApi = {
  getUser: (id: string) => axios.get(`/api/users/${id}`),
  createUser: (data: CreateUserDTO) => axios.post('/api/users', data)
};

// Detection command:
grep -r "axios\.\(get\|post\|put\|delete\|patch\)" --include="*.ts" --include="*.tsx"
```

### React Query

```typescript
// Pattern: React Query hooks
export function useUser(id: string) {
  return useQuery(['user', id], () => fetchUser(id));
}

// Detection command:
grep -r "useQuery\|useMutation" --include="*.tsx" --include="*.ts"
```

### Dependency: API Endpoint Must Exist

```typescript
// Pattern: Frontend calls backend API
const response = await fetch('/api/users');
//                            ↑
//                            Must exist in backend

// Cross-reference: Check if endpoint exists
grep -r "router.get('/users'" src/routes/
```

---

## UI Components

### React Components

```tsx
// Pattern: React component
export function UserList() {
  const { data } = useUsers();  // ← Depends on API client

  return (
    <div>
      {data.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  );
}

// Detection command:
grep -r "export.*function.*(" --include="*.tsx"
```

### Vue Components

```vue
<script setup lang="ts">
import { useUsers } from '@/api/userApi';  // ← Depends on API client

const { data: users } = useUsers();
</script>

<template>
  <div v-for="user in users" :key="user.id">
    {{ user.name }}
  </div>
</template>

// Detection command:
find . -name "*.vue"
```

### Dependency: API Client Must Exist

```tsx
// Pattern: Component imports API client
import { useUsers } from '@/api/userApi';
//                       ↑
//                       Must exist as file

// Verification: Check file exists
test -f src/api/userApi.ts && echo "exists" || echo "MISSING"
```

---

## Dependency Cross-Reference Patterns

### Pattern 1: Type Definition → Repository

```typescript
// Step 1: Type defined
export interface User {
  id: string;
  name: string;
}

// Step 2: Repository uses type
export class UserRepository {
  async findById(id: string): Promise<User> { }
  //                                    ↑
  //                                    Depends on User interface
}

// Verification:
# Find type definition
grep -r "export interface User" --include="*.ts"

# Find usages
grep -r ": Promise<User>" --include="*.ts"
```

### Pattern 2: Repository → Service

```typescript
// Step 1: Repository implemented
export class UserRepository { }

// Step 2: Service uses repository
export class UserService {
  constructor(private userRepository: UserRepository) {}
  //                                  ↑
  //                                  Depends on UserRepository
}

// Verification:
# Find repository
grep -r "class UserRepository" --include="*.ts"

# Find service that uses it
grep -r "UserRepository" src/services/
```

### Pattern 3: Service → Controller/API

```typescript
// Step 1: Service implemented
export class UserService { }

// Step 2: Controller uses service
export class UserController {
  constructor(private userService: UserService) {}
  //                              ↑
  //                              Depends on UserService
}

// Verification:
# Find service
grep -r "class UserService" --include="*.ts"

# Find controllers that use it
grep -r "UserService" src/controllers/
```

### Pattern 4: API Endpoint → Frontend Client

```typescript
// Step 1: API endpoint implemented
router.get('/users', async (req, res) => { });

// Step 2: Frontend calls API
const response = await fetch('/api/users');
//                            ↑
//                            Depends on API endpoint existing

// Verification:
# Find API endpoint
grep -r "router.get('/users'" src/routes/

# Find frontend calls
grep -r "fetch('/api/users')" src/
```

### Pattern 5: API Client → UI Component

```typescript
// Step 1: API client implemented
export async function getUsers() { }

// Step 2: Component uses API client
import { getUsers } from '@/api/userApi';
//       ↑
//       Depends on getUsers function

// Verification:
# Find API client function
grep -r "export.*function getUsers" --include="*.ts"

# Find components that use it
grep -r "import.*getUsers" --include="*.tsx"
```

---

## Technology-Specific Patterns

### Node.js + TypeScript Stack

**Full Stack Dependencies**:
```
1. Database (PostgreSQL + Prisma)
   prisma/schema.prisma

2. Types
   src/types/user.ts

3. Repository
   src/repositories/userRepository.ts

4. Service
   src/services/userService.ts

5. Controller
   src/controllers/userController.ts

6. Routes
   src/routes/userRoutes.ts

7. Frontend API Client
   src/api/userApi.ts

8. Frontend Components
   src/components/UserList.tsx
```

**Detection Commands**:
```bash
# 1. Database
cat prisma/schema.prisma | grep "model User"

# 2. Types
grep -r "export interface User" src/types/

# 3. Repository
grep -r "class UserRepository" src/repositories/

# 4. Service
grep -r "class UserService" src/services/

# 5. Controller
grep -r "class UserController" src/controllers/

# 6. Routes
grep -r "router.get('/users'" src/routes/

# 7. Frontend API Client
grep -r "export.*function.*getUsers" src/api/

# 8. Frontend Components
grep -r "function UserList" src/components/
```

### Python + FastAPI Stack

**Full Stack Dependencies**:
```
1. Database (SQLAlchemy)
   app/models/user.py

2. Schemas (Pydantic)
   app/schemas/user.py

3. Repository
   app/repositories/user_repository.py

4. Service
   app/services/user_service.py

5. API Routes
   app/routes/users.py

6. Frontend API Client
   frontend/src/api/userApi.ts

7. Frontend Components
   frontend/src/components/UserList.tsx
```

**Detection Commands**:
```bash
# 1. Database models
grep -r "class User.*Base" app/models/

# 2. Schemas
grep -r "class.*Schema.*BaseModel" app/schemas/

# 3. Repository
grep -r "class.*Repository" app/repositories/

# 4. Service
grep -r "class.*Service" app/services/

# 5. API routes
grep -r "@app\.\(get\|post\)" app/routes/

# 6. Frontend API client
grep -r "export.*function" frontend/src/api/

# 7. Frontend components
grep -r "function.*Component" frontend/src/components/
```

---

## Import Analysis

### Find All Imports in a File

```bash
# TypeScript/JavaScript
grep -E "^import .* from" src/services/userService.ts

# Python
grep -E "^from .* import|^import " app/services/user_service.py

# Java
grep -E "^import " src/main/java/services/UserService.java
```

### Find All Files That Import Specific Module

```bash
# TypeScript: Find all files importing UserRepository
grep -r "import.*UserRepository" --include="*.ts"

# Python: Find all files importing UserRepository
grep -r "from.*user_repository import\|import.*user_repository" --include="*.py"
```

### Unused Imports (Potential Dead Code)

```bash
# TypeScript: Find modules not imported anywhere
for file in src/**/*.ts; do
  basename=$(basename "$file" .ts)
  grep -r "import.*$basename" --include="*.ts" || echo "UNUSED: $file"
done
```

---

## Practical Validation Scripts

### Validate Database → API Chain

```bash
#!/bin/bash
# Check if database model exists, then API uses it

MODEL_NAME="User"

# 1. Check database model exists
if grep -q "model $MODEL_NAME" prisma/schema.prisma; then
  echo "✅ Database model $MODEL_NAME exists"
else
  echo "❌ Database model $MODEL_NAME NOT FOUND"
  exit 1
fi

# 2. Check API uses model
if grep -q "$MODEL_NAME" src/controllers/*.ts; then
  echo "✅ API uses $MODEL_NAME"
else
  echo "⚠️ WARNING: API doesn't use $MODEL_NAME"
fi
```

### Validate API → Frontend Chain

```bash
#!/bin/bash
# Check if API endpoint exists, then frontend calls it

ENDPOINT="/api/users"

# 1. Check API endpoint exists
if grep -q "router.get('$ENDPOINT'" src/routes/*.ts; then
  echo "✅ API endpoint GET $ENDPOINT exists"
else
  echo "❌ API endpoint GET $ENDPOINT NOT FOUND"
  exit 1
fi

# 2. Check frontend calls endpoint
if grep -q "fetch('$ENDPOINT')" src/**/*.tsx; then
  echo "✅ Frontend calls $ENDPOINT"
else
  echo "⚠️ WARNING: Frontend doesn't call $ENDPOINT"
fi
```

---

**Last Updated**: 2025-01-30
