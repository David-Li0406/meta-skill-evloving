# Error Handling

## Philosophy

**Errors are part of the contract, not exceptions to the rule.**

Good error handling:
- Makes failures informative, not mysterious
- Logs context for debugging
- Returns actionable messages to users
- Prevents cascading failures

Bad error handling:
- Swallows errors silently
- Exposes internal details to users
- Logs nothing or logs everything
- Treats errors as edge cases

## Error Categories

### Expected Errors (Business Logic)

**Examples:**
- User not found (404)
- Duplicate email (409)
- Invalid input (400)
- Unauthorized (401)
- Forbidden (403)

**Handling:** Return appropriate HTTP status, clear user message

### Unexpected Errors (System Failures)

**Examples:**
- Database connection lost
- External service timeout
- Unexpected null value
- Out of memory

**Handling:** Log with context, return generic 500, alert ops team

## Backend Error Handling

### Step 1: Define Service-Layer Exceptions

```python
# File: app/services/exceptions.py

class ServiceException(Exception):
    """Base exception for service layer errors."""
    pass

class EntityNotFoundError(ServiceException):
    """Raised when entity not found."""

    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} {entity_id} not found")

class DuplicateEntityError(ServiceException):
    """Raised when entity already exists."""

    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field}={value} already exists")

class ValidationError(ServiceException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)

class AuthorizationError(ServiceException):
    """Raised when user lacks permission."""

    def __init__(self, action: str, resource: str):
        super().__init__(f"Not authorized to {action} {resource}")
```

### Step 2: Raise in Service Layer

```python
# File: app/services/user_service.py
from app.services.exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
    ValidationError,
)

class UserService:
    async def create_user(self, request: CreateUserRequest) -> User:
        """Create user with validation."""
        # Check for duplicate
        existing = self.repository.find_by_email(request.email)
        if existing:
            raise DuplicateEntityError("User", "email", request.email)

        # Validate business rules
        if not request.email.endswith("@company.com"):
            raise ValidationError(
                "Email must be corporate address",
                field="email"
            )

        # Create user
        user = User(
            id=uuid4(),
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
        )

        return self.repository.save(user)

    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by ID."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)
        return user
```

### Step 3: Handle in API Layer

```python
# File: app/api/v1/users.py
from fastapi import APIRouter, HTTPException, status
from app.services.exceptions import (
    EntityNotFoundError,
    DuplicateEntityError,
    ValidationError,
    AuthorizationError,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Create a new user."""
    service = UserService(db)

    try:
        user = await service.create_user(request)
        return UserResponse.from_orm(user)

    except DuplicateEntityError as e:
        # Expected error - user message, no logging needed
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {e.value} is already registered"
        )

    except ValidationError as e:
        # Expected error - validation failed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

    except Exception as e:
        # Unexpected error - log with context, hide details from user
        logger.error(
            f"Unexpected error creating user: {e}",
            exc_info=True,
            extra={
                "request_email": request.email,
                "error_type": type(e).__name__
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Get user by ID."""
    service = UserService(db)

    try:
        user = await service.get_user_by_id(user_id)
        return UserResponse.from_orm(user)

    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
```

### Step 4: Consistent Error Response Format

```python
# File: app/models/error.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ErrorDetail(BaseModel):
    """Field-level error detail."""
    field: str
    message: str

class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str                          # Error code/type
    message: str                        # User-friendly message
    details: Optional[Dict[str, Any]]   # Additional context
    timestamp: datetime
    path: str                           # Request path

# Example usage
@app.exception_handler(DuplicateEntityError)
async def duplicate_entity_handler(request: Request, exc: DuplicateEntityError):
    return JSONResponse(
        status_code=409,
        content=ErrorResponse(
            error="DUPLICATE_ENTITY",
            message=f"{exc.entity_type} with {exc.field}={exc.value} already exists",
            details={"field": exc.field, "value": exc.value},
            timestamp=datetime.utcnow(),
            path=request.url.path
        ).dict()
    )
```

## Frontend Error Handling

### Step 1: Define Error Types

```typescript
// File: frontend/src/types/errors.ts

export class ApiError extends Error {
  constructor(
    public status: number,
    public message: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class NetworkError extends Error {
  constructor(message: string = 'Network connection failed') {
    super(message);
    this.name = 'NetworkError';
  }
}

export class ValidationError extends Error {
  constructor(
    public message: string,
    public fieldErrors: Record<string, string>
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### Step 2: Handle in API Client

```typescript
// File: frontend/src/api/client.ts
import axios, { AxiosError } from 'axios';
import { ApiError, NetworkError } from '@/types/errors';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (!error.response) {
      // Network error (no response from server)
      throw new NetworkError('Unable to connect to server');
    }

    const { status, data } = error.response;

    // Map HTTP status to appropriate error
    if (status === 401) {
      // Unauthorized - redirect to login
      window.location.href = '/login';
      throw new ApiError(401, 'Authentication required');
    }

    if (status === 403) {
      throw new ApiError(403, 'Access denied');
    }

    if (status === 404) {
      throw new ApiError(404, 'Resource not found');
    }

    if (status === 409) {
      throw new ApiError(
        409,
        data.message || 'Resource already exists',
        data.details
      );
    }

    if (status === 422 || status === 400) {
      // Validation error
      throw new ValidationError(
        data.message || 'Validation failed',
        data.details || {}
      );
    }

    if (status >= 500) {
      // Server error
      throw new ApiError(
        status,
        'Server error occurred. Please try again later.'
      );
    }

    // Unknown error
    throw new ApiError(status, data.message || 'An error occurred');
  }
);

export default apiClient;
```

### Step 3: Handle in Store

```typescript
// File: frontend/src/stores/userStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { CreateUserRequest, UserResponse } from '@/types/api/users';
import { userApi } from '@/api/users';
import { ApiError, NetworkError, ValidationError } from '@/types/errors';

export const useUserStore = defineStore('user', () => {
  const users = ref<UserResponse[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const fieldErrors = ref<Record<string, string>>({});

  const createUser = async (request: CreateUserRequest): Promise<UserResponse | null> => {
    loading.value = true;
    error.value = null;
    fieldErrors.value = {};

    try {
      const user = await userApi.createUser(request);
      users.value.push(user);
      return user;

    } catch (e) {
      if (e instanceof ValidationError) {
        // Field-level validation errors
        error.value = e.message;
        fieldErrors.value = e.fieldErrors;

      } else if (e instanceof ApiError) {
        // API errors (409, 404, etc.)
        error.value = e.message;

        if (e.status === 409) {
          // Duplicate email - highlight email field
          fieldErrors.value = { email: 'Email already registered' };
        }

      } else if (e instanceof NetworkError) {
        // Network errors
        error.value = 'Unable to connect. Please check your internet connection.';

      } else {
        // Unknown error
        error.value = 'An unexpected error occurred. Please try again.';
        console.error('Unexpected error:', e);
      }

      return null;

    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    loading,
    error,
    fieldErrors,
    createUser,
  };
});
```

### Step 4: Display in Component

```vue
<!-- File: frontend/src/components/users/CreateUserForm.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import type { CreateUserRequest } from '@/types/api/users';

const userStore = useUserStore();

const formData = ref<CreateUserRequest>({
  email: '',
  first_name: '',
  last_name: '',
});

const hasError = computed(() => userStore.error !== null);
const fieldErrors = computed(() => userStore.fieldErrors);

const handleSubmit = async () => {
  const user = await userStore.createUser(formData.value);

  if (user) {
    // Success - navigate or show success message
    router.push('/users');
  }
  // Errors already set in store, displayed in template
};
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <!-- Global error banner -->
    <div v-if="hasError" class="error-banner" role="alert">
      {{ userStore.error }}
    </div>

    <!-- Email field with error -->
    <div class="form-field">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="formData.email"
        type="email"
        :class="{ error: fieldErrors.email }"
        :aria-invalid="!!fieldErrors.email"
        :aria-describedby="fieldErrors.email ? 'email-error' : undefined"
      />
      <span v-if="fieldErrors.email" id="email-error" class="error-message">
        {{ fieldErrors.email }}
      </span>
    </div>

    <!-- Other fields... -->

    <button type="submit" :disabled="userStore.loading">
      {{ userStore.loading ? 'Creating...' : 'Create User' }}
    </button>
  </form>
</template>

<style scoped>
.error-banner {
  padding: 1rem;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c00;
  margin-bottom: 1rem;
}

.error-message {
  color: #c00;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

input.error {
  border-color: #c00;
}
</style>
```

## Logging Best Practices

### What to Log

**DO log:**
- Unexpected errors with stack traces
- Security events (failed auth, access denied)
- Performance issues (slow queries > 1s)
- Business events (user created, payment processed)

**DON'T log:**
- Passwords or secrets
- Personal data (in production)
- Expected errors (404s flood logs)
- Debug statements left in code

### Log Levels

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG - Development only
logger.debug(f"Processing request: {request}")

# INFO - Business events
logger.info(f"User created: user_id={user.id}, email={user.email}")

# WARNING - Concerning but handled
logger.warning(f"Slow query detected: {query_time}ms")

# ERROR - Unexpected failure
logger.error(f"Failed to create user: {e}", exc_info=True)

# CRITICAL - System failure
logger.critical(f"Database connection lost", exc_info=True)
```

### Structured Logging

```python
logger.error(
    "Failed to create user",
    exc_info=True,
    extra={
        "user_email": request.email,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.state.request_id,
        "error_type": type(e).__name__
    }
)
```

## Error Handling Checklist

- [ ] Service layer uses custom exceptions
- [ ] API layer maps exceptions to HTTP status codes
- [ ] User-facing messages are clear and actionable
- [ ] Internal errors log with context
- [ ] Sensitive data not exposed in errors
- [ ] Frontend handles network errors gracefully
- [ ] Field-level validation errors highlighted
- [ ] Error states have loading indicators
- [ ] Errors are accessible (ARIA attributes)

---

**Remember:** Errors are not failures in your code; they're part of the user experience. Handle them gracefully, log them usefully, and make failures informative.
