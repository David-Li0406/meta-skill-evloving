# Frontend Implementation Workflow

## Purpose

This workflow guides systematic implementation of frontend components following contract-first discipline and validation gates.

Use this workflow when implementing:
- Vue/React components
- State management (Pinia/Redux stores)
- API integration
- Form handling and validation
- Frontend routing

## Prerequisites

1. **Design Documentation**
   - Frontend design specification (`05-frontend-design.md`)
   - API specification (`04-api-specification.md`)
   - UX mockups or wireframes (if available)

2. **Contract Requirements**
   - Backend API DTOs defined
   - TypeScript interfaces needed
   - Component props/emits specified

3. **Dependencies**
   - Component library available (if using one)
   - API client configured
   - State management setup

## Phase 0: Start Task Tracking

Before beginning implementation, start task tracking:

```bash
# Start the task to update status and track progress
shark task start <task-id>

# Example:
shark task start T-E04-F05-001
```

This:
- Updates task status to "in-progress" in the database
- Tracks when implementation began
- Provides visibility to the team
- Enables accurate progress reporting

## Phase 1: Contract-First Implementation (CRITICAL)

**Time: 30-45 minutes | Prevents: Days of integration debugging**

### Step 1.1: Extract DTO Requirements from Backend Spec (5 minutes)

```bash
# Open API specification
Read: /docs/plan/{epic-key}/{feature-key}/04-api-specification.md
```

Find:
- Backend DTO field names (EXACT - snake_case vs camelCase matters!)
- Backend DTO types (string, UUID, datetime format)
- Validation rules (required, optional, constraints)
- Contract Synchronization Table

**Critical:** Frontend types must match backend DTOs EXACTLY. No "improving" field names.

### Step 1.2: Create TypeScript Interfaces Matching Backend (10 minutes)

```typescript
// File: frontend/src/types/api/{feature}.ts

/**
 * From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#CreateUserRequest
 *
 * Contract: This interface must match backend DTO EXACTLY
 * Backend field: first_name (snake_case) - DO NOT change to firstName!
 */
export interface CreateUserRequest {
  email: string;           // Backend: EmailStr (transmitted as string)
  first_name: string;      // MUST match backend field name (snake_case)
  last_name: string;       // MUST match backend field name (snake_case)
}

/**
 * From: /docs/plan/E09-identity/E09-F01-user-mgmt/04-api-specification.md#UserResponse
 *
 * Contract: This interface must match backend DTO EXACTLY
 */
export interface UserResponse {
  id: string;              // Backend: UUID (transmitted as string)
  email: string;
  first_name: string;      // MUST match backend (not firstName!)
  last_name: string;       // MUST match backend (not lastName!)
  created_at: string;      // Backend: datetime (transmitted as ISO 8601 string)
}
```

**Anti-Patterns (DO NOT DO):**
```typescript
// ❌ WRONG - Different field names than backend
export interface CreateUserRequest {
  email: string;
  firstName: string;   // Backend has first_name - MISMATCH!
  lastName: string;    // Backend has last_name - MISMATCH!
}

// ❌ WRONG - Different types than backend
export interface UserResponse {
  id: string;
  created_at: number;  // Backend sends ISO string, not timestamp!
  status: string;      // Backend has enum, not any string!
}

// ❌ WRONG - Using 'any' defeats contract validation
export interface UserResponse {
  id: string;
  data: any;           // Type safety lost!
}
```

### Step 1.3: Create Mock API Layer with Correct Shapes (15 minutes)

Create mock that uses exact DTO types (enables frontend development before backend ready):

```typescript
// File: frontend/src/api/mock/{feature}.ts
import type { CreateUserRequest, UserResponse } from '@/types/api/users';

export const mockUserApi = {
  createUser: async (request: CreateUserRequest): Promise<UserResponse> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Response must match UserResponse interface exactly
    return {
      id: '550e8400-e29b-41d4-a716-446655440000',  // UUID as string
      email: request.email,
      first_name: request.first_name,  // Must use backend field name
      last_name: request.last_name,    // Must use backend field name
      created_at: new Date().toISOString(),  // ISO 8601 format
    };
  },

  getUser: async (userId: string): Promise<UserResponse> => {
    await new Promise(resolve => setTimeout(resolve, 300));

    return {
      id: userId,
      email: 'john@example.com',
      first_name: 'John',
      last_name: 'Doe',
      created_at: '2024-01-15T10:30:00Z',
    };
  },
};
```

### Step 1.4: Run Contract Validation (10 minutes)

**Type Check:**
```bash
cd frontend
npm run type-check -- --strict
# TypeScript compiler must pass with no errors
```

**Create Contract Validation Test:**
```typescript
// File: frontend/src/types/api/__tests__/users.test.ts
import { describe, it, expect } from 'vitest';
import type { CreateUserRequest, UserResponse } from '../users';

describe('User API Contracts', () => {
  it('CreateUserRequest has required fields matching backend', () => {
    const request: CreateUserRequest = {
      email: 'test@example.com',
      first_name: 'John',  // Must be snake_case like backend
      last_name: 'Doe',
    };

    // TypeScript enforces this at compile time
    expect(request.email).toBeDefined();
    expect(request.first_name).toBeDefined();
    expect(request.last_name).toBeDefined();
  });

  it('UserResponse has required fields matching backend', () => {
    const response: UserResponse = {
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'test@example.com',
      first_name: 'John',      // Must match backend
      last_name: 'Doe',        // Must match backend
      created_at: '2024-01-15T10:30:00Z',
    };

    expect(response.id).toBeDefined();
    expect(response.created_at).toMatch(/^\d{4}-\d{2}-\d{2}T/); // ISO 8601
  });

  // These should NOT compile (uncomment to verify contract):
  // it('catches field name mismatches', () => {
  //   const bad: UserResponse = {
  //     id: '123',
  //     firstName: 'John',  // ❌ Compiler error - field doesn't exist
  //   };
  // });
});
```

Run tests:
```bash
npm run test -- users.test.ts
```

### Step 1.5: Synchronize with Backend Team

**Communication Required:**

Share with backend developer:
```
TypeScript interfaces implemented for {feature}:
- CreateUserRequest: email, first_name, last_name
- UserResponse: id, email, first_name, last_name, created_at

Location: frontend/src/types/api/{feature}.ts
Type checking passing: ✓
Contract tests passing: ✓

Confirmation received that backend DTOs match:
✓ Field names identical (first_name, last_name in snake_case)
✓ Types compatible (UUID as string, datetime as ISO 8601)
✓ Contract synchronized

Proceeding to component implementation.
```

**STOP if not synchronized.** Align before Phase 2.

## Phase 2: Component Implementation

With validated contracts, implement components.

### Step 2.1: Create Component Shell with Typed Props

**Vue 3 Example:**
```vue
<!-- File: frontend/src/components/users/CreateUserForm.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import type { CreateUserRequest, UserResponse } from '@/types/api/users';

// Props with explicit types
interface Props {
  initialData?: Partial<CreateUserRequest>;
}

const props = defineProps<Props>();

// Emits with explicit types
const emit = defineEmits<{
  submit: [payload: CreateUserRequest];
  cancel: [];
}>();

// Form data matching DTO exactly
const formData = ref<CreateUserRequest>({
  email: props.initialData?.email ?? '',
  first_name: props.initialData?.first_name ?? '',  // Snake_case matches backend
  last_name: props.initialData?.last_name ?? '',
});

// Validation state
const errors = ref<Partial<Record<keyof CreateUserRequest, string>>>({});

const handleSubmit = () => {
  // Validation
  errors.value = {};

  if (!formData.value.email) {
    errors.value.email = 'Email is required';
  }
  if (!formData.value.first_name) {
    errors.value.first_name = 'First name is required';
  }
  if (!formData.value.last_name) {
    errors.value.last_name = 'Last name is required';
  }

  if (Object.keys(errors.value).length > 0) {
    return;
  }

  // Emit with exact DTO type
  emit('submit', formData.value);
};
</script>

<template>
  <form @submit.prevent="handleSubmit" class="create-user-form">
    <div class="form-field">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="formData.email"
        type="email"
        :class="{ error: errors.email }"
      />
      <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
    </div>

    <div class="form-field">
      <label for="first_name">First Name</label>
      <input
        id="first_name"
        v-model="formData.first_name"
        type="text"
        :class="{ error: errors.first_name }"
      />
      <span v-if="errors.first_name" class="error-message">{{ errors.first_name }}</span>
    </div>

    <div class="form-field">
      <label for="last_name">Last Name</label>
      <input
        id="last_name"
        v-model="formData.last_name"
        type="text"
        :class="{ error: errors.last_name }"
      />
      <span v-if="errors.last_name" class="error-message">{{ errors.last_name }}</span>
    </div>

    <div class="form-actions">
      <button type="button" @click="emit('cancel')">Cancel</button>
      <button type="submit">Create User</button>
    </div>
  </form>
</template>

<style scoped>
/* Follow frontend-design skill for aesthetics */
</style>
```

**React Example:**
```typescript
// File: frontend/src/components/users/CreateUserForm.tsx
import React, { useState } from 'react';
import type { CreateUserRequest } from '@/types/api/users';

interface CreateUserFormProps {
  initialData?: Partial<CreateUserRequest>;
  onSubmit: (data: CreateUserRequest) => void;
  onCancel: () => void;
}

export const CreateUserForm: React.FC<CreateUserFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
}) => {
  const [formData, setFormData] = useState<CreateUserRequest>({
    email: initialData?.email ?? '',
    first_name: initialData?.first_name ?? '',  // Snake_case matches backend
    last_name: initialData?.last_name ?? '',
  });

  const [errors, setErrors] = useState<Partial<Record<keyof CreateUserRequest, string>>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors: typeof errors = {};

    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="create-user-form">
      {/* Form fields similar to Vue example */}
    </form>
  );
};
```

### Step 2.2: Implement State Management (Pinia/Redux)

**Pinia Store Example:**
```typescript
// File: frontend/src/stores/userStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { CreateUserRequest, UserResponse } from '@/types/api/users';
import { mockUserApi } from '@/api/mock/users';

export const useUserStore = defineStore('user', () => {
  const users = ref<UserResponse[]>([]);
  const currentUser = ref<UserResponse | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const createUser = async (request: CreateUserRequest): Promise<UserResponse> => {
    loading.value = true;
    error.value = null;

    try {
      const user = await mockUserApi.createUser(request);
      users.value.push(user);
      return user;
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  const getUser = async (userId: string): Promise<UserResponse> => {
    loading.value = true;
    error.value = null;

    try {
      const user = await mockUserApi.getUser(userId);
      currentUser.value = user;
      return user;
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    currentUser,
    loading,
    error,
    createUser,
    getUser,
  };
});
```

### Step 2.3: Wire Component to Store

```vue
<!-- File: frontend/src/views/CreateUserView.vue -->
<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import CreateUserForm from '@/components/users/CreateUserForm.vue';
import type { CreateUserRequest } from '@/types/api/users';

const router = useRouter();
const userStore = useUserStore();

const handleSubmit = async (data: CreateUserRequest) => {
  try {
    await userStore.createUser(data);
    router.push('/users');  // Navigate on success
  } catch (e) {
    console.error('Failed to create user:', e);
    // Error displayed via store.error
  }
};

const handleCancel = () => {
  router.back();
};
</script>

<template>
  <div class="create-user-view">
    <h1>Create New User</h1>

    <div v-if="userStore.error" class="error-banner">
      {{ userStore.error }}
    </div>

    <CreateUserForm
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>
```

## Phase 3: Testing

### Step 3.1: Component Unit Tests

```typescript
// File: frontend/src/components/users/__tests__/CreateUserForm.test.ts
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import CreateUserForm from '../CreateUserForm.vue';

describe('CreateUserForm', () => {
  it('renders form fields', () => {
    const wrapper = mount(CreateUserForm);

    expect(wrapper.find('input#email').exists()).toBe(true);
    expect(wrapper.find('input#first_name').exists()).toBe(true);
    expect(wrapper.find('input#last_name').exists()).toBe(true);
  });

  it('validates required fields', async () => {
    const wrapper = mount(CreateUserForm);

    await wrapper.find('form').trigger('submit');

    expect(wrapper.text()).toContain('Email is required');
    expect(wrapper.text()).toContain('First name is required');
  });

  it('emits submit with correct data structure', async () => {
    const wrapper = mount(CreateUserForm);

    await wrapper.find('input#email').setValue('test@example.com');
    await wrapper.find('input#first_name').setValue('John');
    await wrapper.find('input#last_name').setValue('Doe');
    await wrapper.find('form').trigger('submit');

    expect(wrapper.emitted('submit')).toBeTruthy();
    expect(wrapper.emitted('submit')![0]).toEqual([
      {
        email: 'test@example.com',
        first_name: 'John',  // Verify snake_case preserved
        last_name: 'Doe',
      },
    ]);
  });
});
```

### Step 3.2: Store Tests

```typescript
// File: frontend/src/stores/__tests__/userStore.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '../userStore';

describe('userStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('creates user successfully', async () => {
    const store = useUserStore();

    const user = await store.createUser({
      email: 'test@example.com',
      first_name: 'John',
      last_name: 'Doe',
    });

    expect(user.email).toBe('test@example.com');
    expect(user.first_name).toBe('John');  // Verify snake_case
    expect(store.users).toHaveLength(1);
    expect(store.loading).toBe(false);
  });

  it('handles errors gracefully', async () => {
    const store = useUserStore();

    // Mock API to throw error
    vi.spyOn(mockUserApi, 'createUser').mockRejectedValue(new Error('Network error'));

    await expect(store.createUser({
      email: 'test@example.com',
      first_name: 'John',
      last_name: 'Doe',
    })).rejects.toThrow('Network error');

    expect(store.error).toBe('Network error');
    expect(store.loading).toBe(false);
  });
});
```

## Phase 4: Validation Gates

### Gate 1: Linting & Formatting
```bash
cd frontend
npm run lint
npm run format -- --check
```

### Gate 2: Type Checking
```bash
npm run type-check
```

### Gate 3: Unit Tests
```bash
npm run test
```

### Gate 4: E2E Tests (if applicable)
```bash
npm run test:e2e:headless
```

### Gate 5: Build
```bash
npm run build
# Must complete without errors
```

**All gates must pass.**

## Phase 5: Documentation

```markdown
# File: /docs/plan/{epic}/{feature}/IMPLEMENTATION.md

## Frontend Implementation

### Components
- CreateUserForm.vue - User creation form with validation
- UserList.vue - Display users with pagination

### Stores
- userStore - User state management (Pinia)

### API Integration
- Mock API: frontend/src/api/mock/users.ts
- Types: frontend/src/types/api/users.ts

### Contract Synchronization
- ✓ TypeScript interfaces match backend DTOs exactly
- ✓ Field names preserved (first_name, last_name in snake_case)
- ✓ Types compatible (UUID strings, ISO 8601 datetimes)
- ✓ Backend team confirmed synchronization

### Validation Gates
- ✓ Linting passed
- ✓ Type checking passed (strict mode)
- ✓ Unit tests: 24/24 passed
- ✓ Build successful
```

## UI Design Integration

For visual design, consult `frontend-design` skill:

```
Reference: ~/.claude/skills/frontend-design/SKILL.md

- Choose bold aesthetic direction
- Typography: distinctive fonts, not generic
- Color: cohesive theme with CSS variables
- Motion: CSS animations for micro-interactions
- Spatial composition: unexpected layouts
```

## Completion Checklist

- [ ] TypeScript interfaces match backend DTOs exactly
- [ ] Contract validation tests passing
- [ ] Backend synchronization confirmed
- [ ] Components implemented with typed props/emits
- [ ] State management wired (Pinia/Redux)
- [ ] Unit tests passing
- [ ] E2E tests passing (if applicable)
- [ ] All validation gates passed
- [ ] UI design follows frontend-design skill
- [ ] Documentation updated
- [ ] **Task completed:** `shark task complete <task-id>`

**Final Step:** Mark the task as complete:
```bash
shark task complete T-E04-F05-001
```

This updates the task status to "completed" and records completion time in the database.

## Common Issues

| Issue | Solution |
|-------|----------|
| Type errors on API responses | Check DTO interfaces match backend exactly |
| Form fields not updating | Verify v-model bindings, use reactive refs |
| Store state not persisting | Check if createPinia() called in main.ts |
| Tests failing | Mock API responses, check async/await |
| Build errors | Run type-check, fix TypeScript errors |

## Reference

- Contract-first discipline: `../context/contract-first.md`
- Validation gates: `../context/validation-gates.md`
- Frontend design: `../../frontend-design/SKILL.md`
- Testing requirements: `../context/testing-requirements.md`

---

**Remember:** Contract-first prevents integration pain. Match backend DTOs exactly, synchronize early, validate types.
