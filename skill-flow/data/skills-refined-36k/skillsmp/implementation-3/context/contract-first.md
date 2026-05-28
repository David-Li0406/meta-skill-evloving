# Contract-First Discipline

## The Problem

**Scenario:** Frontend and backend teams implement their understanding of an API. During integration:

- Backend sends `first_name` (snake_case), frontend expects `firstName` (camelCase)
- Backend sends datetime as ISO 8601 string, frontend expects Unix timestamp
- Backend validates email with regex, frontend uses different regex
- Backend requires `user_id` field, frontend sends `userId`

**Result:** Integration becomes a debugging session. Developers waste days fixing field name mismatches, type incompatibilities, and validation differences. Each fix reveals another mismatch. Sprint goals slip.

**Root Cause:** Contract (DTO) defined ambiguously or implemented independently on each side.

## The Solution: Contract-First Discipline

**The Golden Rule:**

```
DTOs are defined in the specification,
implemented identically on frontend and backend,
and validated BEFORE any business logic is written.
```

### Why This Works

1. **Single Source of Truth** - Specification defines exact field names, types, validation
2. **Early Validation** - Contracts tested before business logic, mismatches caught immediately
3. **Parallel Development** - Frontend builds UI with correct types while backend implements logic
4. **Zero Integration Surprises** - Contracts already validated, integration is assembly not debugging

## Contract-First Workflow

### Phase 1: Specification Defines Contract (Design Phase)

Design documentation (`04-api-specification.md`) contains:

```markdown
## DTO Definitions

### CreateUserRequest

**Purpose:** Data required to create a new user

**Fields:**
- `email`: string, required, email format validation
- `first_name`: string, required, 1-255 characters (snake_case - not firstName!)
- `last_name`: string, required, 1-255 characters (snake_case - not lastName!)

**Validation Rules:**
- Email must be valid email format (RFC 5322)
- first_name must be non-empty after trimming whitespace
- last_name must be non-empty after trimming whitespace

### UserResponse

**Purpose:** User data returned from API

**Fields:**
- `id`: UUID, transmitted as string
- `email`: string, email format
- `first_name`: string (matches request field name)
- `last_name`: string (matches request field name)
- `created_at`: datetime, transmitted as ISO 8601 string (e.g., "2024-01-15T10:30:00Z")

### Contract Synchronization Table

This table is the source of truth for frontend/backend implementation:

| Field | Type (Backend) | Type (Frontend) | Format/Notes |
|-------|---------------|-----------------|--------------|
| id | UUID | string | UUID transmitted as string |
| email | EmailStr | string | Email validation on both sides |
| first_name | str | string | Snake_case on BOTH sides |
| last_name | str | string | Snake_case on BOTH sides |
| created_at | datetime | string | ISO 8601 format "YYYY-MM-DDTHH:MM:SSZ" |
```

### Phase 2: Backend Implements DTOs (Before Business Logic)

**Step 1:** Create DTO classes matching specification EXACTLY

```python
# File: app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class CreateUserRequest(BaseModel):
    """
    From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#CreateUserRequest

    CONTRACT: This DTO must match specification exactly.
    Frontend TypeScript interface must use identical field names.
    """
    email: EmailStr                                      # Spec: email format
    first_name: str = Field(min_length=1, max_length=255)  # Spec: snake_case, required
    last_name: str = Field(min_length=1, max_length=255)   # Spec: snake_case, required

class UserResponse(BaseModel):
    """
    From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#UserResponse

    CONTRACT: This DTO must match specification exactly.
    """
    id: UUID                    # Transmitted as string in JSON
    email: str
    first_name: str             # MUST match request (not firstName!)
    last_name: str              # MUST match request (not lastName!)
    created_at: datetime        # Pydantic serializes to ISO 8601 string

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Explicit ISO 8601
        }
```

**Step 2:** Create contract validation tests

```python
# File: tests/contract/test_user_contracts.py
import pytest
from app.schemas.user_schema import CreateUserRequest, UserResponse

def test_create_user_request_matches_spec():
    """Verify CreateUserRequest DTO structure matches specification."""
    # Spec: /docs/plan/.../04-api-specification.md#CreateUserRequest

    expected_fields = {'email', 'first_name', 'last_name'}
    actual_fields = set(CreateUserRequest.__fields__.keys())

    assert actual_fields == expected_fields, \
        f"DTO diverged from spec. Expected: {expected_fields}, Got: {actual_fields}"

def test_user_response_matches_spec():
    """Verify UserResponse DTO structure matches specification."""
    expected_fields = {'id', 'email', 'first_name', 'last_name', 'created_at'}
    actual_fields = set(UserResponse.__fields__.keys())

    assert actual_fields == expected_fields
```

**Step 3:** Run contract tests

```bash
pytest tests/contract/test_user_contracts.py -v
# Must pass before proceeding to business logic
```

### Phase 3: Frontend Implements Interfaces (Before Component Code)

**Step 1:** Create TypeScript interfaces matching backend DTOs EXACTLY

```typescript
// File: frontend/src/types/api/users.ts

/**
 * From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#CreateUserRequest
 *
 * CONTRACT: This interface must match backend DTO exactly.
 * Field names MUST be snake_case to match backend (first_name, not firstName).
 */
export interface CreateUserRequest {
  email: string;           // Backend: EmailStr (string with email validation)
  first_name: string;      // MUST be snake_case to match backend
  last_name: string;       // MUST be snake_case to match backend
}

/**
 * From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#UserResponse
 *
 * CONTRACT: This interface must match backend DTO exactly.
 */
export interface UserResponse {
  id: string;              // Backend: UUID (transmitted as string)
  email: string;
  first_name: string;      // MUST match backend field name
  last_name: string;       // MUST match backend field name
  created_at: string;      // Backend: datetime (transmitted as ISO 8601 string)
}
```

**Step 2:** Create contract validation tests

```typescript
// File: frontend/src/types/api/__tests__/users.contract.test.ts
import { describe, it, expect } from 'vitest';
import type { CreateUserRequest, UserResponse } from '../users';

describe('User API Contracts', () => {
  it('CreateUserRequest has required fields matching backend', () => {
    const request: CreateUserRequest = {
      email: 'test@example.com',
      first_name: 'Test',  // Snake_case matches backend
      last_name: 'User',
    };

    expect(Object.keys(request).sort()).toEqual(
      ['email', 'first_name', 'last_name'].sort()
    );
  });

  it('UserResponse has required fields matching backend', () => {
    const response: UserResponse = {
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      created_at: '2024-01-15T10:30:00Z',
    };

    expect(Object.keys(response).sort()).toEqual(
      ['id', 'email', 'first_name', 'last_name', 'created_at'].sort()
    );

    // Verify ISO 8601 datetime format
    expect(response.created_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
  });
});
```

**Step 3:** Run type checking and contract tests

```bash
npm run type-check -- --strict
npm run test -- users.contract.test.ts
# Must pass before proceeding to component implementation
```

### Phase 4: Synchronization Checkpoint (CRITICAL)

**Backend to Frontend:**

```
Backend developer to frontend developer:

"DTOs implemented for user management:
- CreateUserRequest: email, first_name, last_name
- UserResponse: id, email, first_name, last_name, created_at

Contract tests passing: ✓
Location: app/schemas/user_schema.py

Please confirm your TypeScript interfaces match:
- Field names (first_name, not firstName)
- Types (created_at is ISO 8601 string, not number)
- Validation (email format on both sides)

Contract Synchronization Table verified: ✓"
```

**Frontend to Backend:**

```
Frontend developer to backend developer:

"TypeScript interfaces implemented:
- CreateUserRequest: email, first_name, last_name
- UserResponse: id, email, first_name, last_name, created_at

Type checking passing (strict mode): ✓
Contract tests passing: ✓
Location: frontend/src/types/api/users.ts

Confirmed:
✓ Field names match (first_name, last_name in snake_case)
✓ Types compatible (UUID as string, datetime as ISO 8601)
✓ Ready for parallel development

Contract synchronized."
```

**If NOT synchronized:** STOP. Fix discrepancies before proceeding to Phase 5.

### Phase 5: Implementation (With Validated Contracts)

**Backend:** Implement business logic knowing DTOs are correct

```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,  # Contract validated ✓
    db: Session = Depends(get_db)
) -> UserResponse:
    """Create user - contract already validated."""
    service = UserService(db)
    user = await service.create_user(request)

    # Response DTO matches frontend expectation ✓
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at
    )
```

**Frontend:** Implement components knowing types are correct

```vue
<script setup lang="ts">
import type { CreateUserRequest, UserResponse } from '@/types/api/users';

// Contract validated ✓
const formData = ref<CreateUserRequest>({
  email: '',
  first_name: '',  // Snake_case matches backend ✓
  last_name: '',
});

const handleSubmit = async () => {
  // TypeScript enforces correct structure ✓
  const user: UserResponse = await api.createUser(formData.value);
  console.log(user.created_at);  // ISO 8601 string ✓
};
</script>
```

### Phase 6: Integration (Assembly, Not Debugging)

Connect frontend to real backend:

```typescript
// File: frontend/src/api/users.ts
import type { CreateUserRequest, UserResponse } from '@/types/api/users';
import { apiClient } from './client';

export const userApi = {
  createUser: async (request: CreateUserRequest): Promise<UserResponse> => {
    const response = await apiClient.post('/api/v1/users', request);
    return response.data;  // TypeScript validates structure ✓
  },
};
```

**Expected result:** Integration works immediately because contracts were validated before implementation.

## Anti-Patterns (DO NOT DO)

### Anti-Pattern 1: Different Field Names

```python
# ❌ Backend
class CreateUserRequest(BaseModel):
    email: str
    first_name: str  # Snake_case

# ❌ Frontend (MISMATCH!)
interface CreateUserRequest {
  email: string;
  firstName: string;  // CamelCase - DIVERGED!
}
```

**Why it fails:** Backend rejects requests with `firstName` field. Frontend receives responses with `first_name` field but expects `firstName`.

**Fix:** Use EXACT same field names on both sides (follow specification).

### Anti-Pattern 2: Different Types

```python
# ❌ Backend sends datetime as ISO 8601 string
class UserResponse(BaseModel):
    created_at: datetime  # Serializes to "2024-01-15T10:30:00Z"

# ❌ Frontend expects Unix timestamp (MISMATCH!)
interface UserResponse {
  created_at: number;  // Expects 1705318200
}
```

**Why it fails:** Frontend tries to parse string as number, gets NaN.

**Fix:** Agree on format in specification (ISO 8601), implement identically.

### Anti-Pattern 3: Skip Contract Validation

```python
# ❌ Implement business logic immediately without validating contracts
@router.post("/users")
async def create_user(request: dict):  # Untyped!
    user = User(email=request['email'], ...)
    # No contract validation - hope frontend sends correct shape
```

**Why it fails:** Runtime errors when frontend sends different field structure.

**Fix:** Validate contracts first (Phase 2), then implement logic (Phase 5).

### Anti-Pattern 4: "We'll Figure It Out During Integration"

**❌ Approach:** Backend and frontend implement independently, plan integration session to "work out the details."

**Why it fails:** Integration becomes multi-day debugging session finding field name mismatches, type incompatibilities, validation differences.

**Fix:** Contract-first discipline. Synchronize contracts (Phase 4) BEFORE implementation (Phase 5).

## Benefits

### Prevents Integration Failures

| Without Contract-First | With Contract-First |
|----------------------|-------------------|
| "Why is first_name undefined?" | Contracts validated before implementation |
| "Backend sends string, I expected number" | Types synchronized via specification |
| "Email validation different on each side" | Validation rules documented, implemented identically |
| Integration takes 3 days | Integration takes 30 minutes |

### Enables Parallel Development

- **Backend:** Implements business logic with validated DTOs
- **Frontend:** Builds UI with mocked APIs using correct types
- **Integration:** Swap mock for real API, works immediately

### Builds Confidence

- Contract tests prove structure matches specification
- Type checking proves no `any` types or implicit conversions
- Integration is assembly (connecting validated parts), not debugging (finding what's wrong)

## Measurement

**Contract-First is working when:**

- Integration sessions are < 1 hour (not multi-day)
- Zero field name mismatch bugs in production
- Zero type conversion errors during integration
- Frontend/backend can develop in parallel without blockers

**Contract-First is failing when:**

- "Integration week" on project schedule
- Bug tracker has "field name mismatch" tickets
- Developers say "let's just try it and see what breaks"

## Checklist

Before claiming "contracts synchronized":

- [ ] Specification defines exact field names (case-sensitive)
- [ ] Specification defines exact types with transmission format
- [ ] Backend DTOs implemented matching specification
- [ ] Frontend interfaces implemented matching specification
- [ ] Backend contract tests passing
- [ ] Frontend contract tests passing
- [ ] Backend/frontend developers confirmed synchronization
- [ ] No `any` types in frontend code
- [ ] No `dict` types in backend code (use DTOs)

---

**Remember:** 45 minutes validating contracts prevents 3 days debugging integration. The contract is the source of truth, not "what I thought it should be."
