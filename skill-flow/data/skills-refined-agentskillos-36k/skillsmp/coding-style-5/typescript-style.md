# TypeScript Style Guide

## Project Structure

### SvelteKit Application
```
project/
├── src/
│   ├── lib/
│   │   ├── apis/           # API endpoint wrappers
│   │   │   ├── index.ts
│   │   │   ├── auth.ts
│   │   │   └── models.ts
│   │   ├── components/     # Reusable components
│   │   ├── stores/         # Svelte stores
│   │   ├── types/          # Type definitions
│   │   └── utils/          # Utility functions
│   ├── routes/             # SvelteKit routes
│   └── app.html
├── static/
├── package.json
├── tsconfig.json
├── svelte.config.js
└── vite.config.ts
```

---

## Configuration

### tsconfig.json
```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true
  }
}
```

### ESLint Configuration
```javascript
// .eslintrc.cjs
module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:svelte/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    extraFileExtensions: ['.svelte']
  },
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    'no-console': ['warn', { allow: ['warn', 'error'] }]
  },
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser'
      }
    }
  ]
};
```

### Prettier Configuration
```json
{
  "useTabs": true,
  "singleQuote": true,
  "trailingComma": "none",
  "printWidth": 100,
  "plugins": ["prettier-plugin-svelte"],
  "overrides": [
    {
      "files": "*.svelte",
      "options": { "parser": "svelte" }
    }
  ]
}
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files (components) | PascalCase | `UserProfile.svelte` |
| Files (utilities) | camelCase | `fetchUtils.ts` |
| Functions | camelCase | `getModels()` |
| Classes | PascalCase | `ApiClient` |
| Interfaces/Types | PascalCase | `ModelConfig` |
| Constants | SCREAMING_SNAKE or camelCase | `API_BASE_URL` or `defaultTimeout` |
| Enums | PascalCase | `ResponseStatus` |

---

## Type Definitions

### Interface vs Type
```typescript
// Use interface for object shapes that may be extended
interface User {
  id: string;
  name: string;
  email: string;
}

interface AdminUser extends User {
  permissions: string[];
}

// Use type for unions, intersections, and aliases
type UserId = string;
type ApiResponse<T> = { data: T; error: null } | { data: null; error: string };
type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
```

### Form Types
```typescript
// Name forms with suffix
interface LoginForm {
  email: string;
  password: string;
}

interface ChatCompletedForm {
  model: string;
  messages: Message[];
  chat_id: string;
}
```

### Config Types
```typescript
interface ModelConfig {
  readonly id: string;
  name: string;
  params: Record<string, unknown>;
}

interface GlobalModelConfig {
  models: ModelConfig[];
  defaultModel: string;
}
```

---

## Error Handling

### Standard API Fetch Pattern
```typescript
export const fetchData = async <T>(
  url: string,
  token: string,
  options: RequestInit = {}
): Promise<T | null> => {
  let error = null;

  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err;
      return null;
    });

  if (error) {
    throw error;
  }

  return res as T;
};
```

### API Wrapper Functions
```typescript
// src/lib/apis/models.ts
import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getModels = async (token: string = ''): Promise<ModelConfig[]> => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/models`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err.detail ?? 'Server connection failed';
      return null;
    });

  if (error) {
    throw error;
  }

  return res?.data ?? [];
};

export const updateModelConfig = async (
  token: string,
  config: GlobalModelConfig
): Promise<GlobalModelConfig | null> => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/models/config`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(config)
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err.detail ?? 'Failed to update config';
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};
```

---

## Svelte Patterns

### Component Structure
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import type { User } from '$lib/types';

  // Props
  export let user: User;
  export let onSave: (user: User) => void;

  // Local state
  let loading = false;
  let error: string | null = null;

  // Reactive statements
  $: displayName = user.name || 'Anonymous';

  // Functions
  async function handleSave() {
    loading = true;
    try {
      await onSave(user);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unknown error';
    } finally {
      loading = false;
    }
  }

  // Lifecycle
  onMount(() => {
    // Setup code
    return () => {
      // Cleanup code
    };
  });
</script>

<div class="user-profile">
  <h1>{displayName}</h1>
  {#if error}
    <p class="error">{error}</p>
  {/if}
  <button on:click={handleSave} disabled={loading}>
    {loading ? 'Saving...' : 'Save'}
  </button>
</div>

<style>
  .user-profile {
    padding: 1rem;
  }

  .error {
    color: red;
  }
</style>
```

### Store Pattern
```typescript
// src/lib/stores/user.ts
import { writable, derived } from 'svelte/store';
import type { User } from '$lib/types';

function createUserStore() {
  const { subscribe, set, update } = writable<User | null>(null);

  return {
    subscribe,
    set,
    login: (user: User) => set(user),
    logout: () => set(null),
    updateName: (name: string) => update((u) => (u ? { ...u, name } : null))
  };
}

export const user = createUserStore();

// Derived store
export const isLoggedIn = derived(user, ($user) => $user !== null);
```

---

## Utility Functions

### Type Guards
```typescript
export function isError(value: unknown): value is Error {
  return value instanceof Error;
}

export function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

export function hasProperty<K extends string>(
  obj: unknown,
  key: K
): obj is Record<K, unknown> {
  return typeof obj === 'object' && obj !== null && key in obj;
}
```

### Async Utilities
```typescript
export async function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function retry<T>(
  fn: () => Promise<T>,
  attempts: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < attempts; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === attempts - 1) throw error;
      await sleep(delay);
    }
  }
  throw new Error('Unreachable');
}
```

---

## Constants

```typescript
// src/lib/constants.ts
export const WEBUI_API_BASE_URL = '/api/v1';
export const DEFAULT_TIMEOUT = 30000;

export const RESPONSE_STATUS = {
  SUCCESS: 'success',
  ERROR: 'error',
  PENDING: 'pending'
} as const;

export type ResponseStatus = (typeof RESPONSE_STATUS)[keyof typeof RESPONSE_STATUS];
```

---

## Testing

### Vitest Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}'],
    globals: true,
    environment: 'jsdom'
  }
});
```

### Unit Test Pattern
```typescript
// src/lib/utils/format.test.ts
import { describe, it, expect } from 'vitest';
import { formatDate, truncate } from './format';

describe('formatDate', () => {
  it('formats ISO date string', () => {
    const result = formatDate('2024-01-15T10:30:00Z');
    expect(result).toBe('Jan 15, 2024');
  });

  it('returns empty string for invalid date', () => {
    const result = formatDate('invalid');
    expect(result).toBe('');
  });
});

describe('truncate', () => {
  it('truncates long strings', () => {
    const result = truncate('Hello World', 5);
    expect(result).toBe('Hello...');
  });

  it('returns original if under limit', () => {
    const result = truncate('Hi', 10);
    expect(result).toBe('Hi');
  });
});
```

---

## Common Dependencies

| Purpose | Package |
|---------|---------|
| Framework | `svelte`, `@sveltejs/kit` |
| Build | `vite` |
| Testing | `vitest`, `@testing-library/svelte` |
| E2E Testing | `cypress`, `playwright` |
| Linting | `eslint`, `@typescript-eslint/*` |
| Formatting | `prettier`, `prettier-plugin-svelte` |
| State | Svelte stores (built-in) |
| Icons | `lucide-svelte` |
| Styling | `tailwindcss` |
