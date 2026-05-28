# Vitest Configuration

Each app/package has its own `vitest.config.mts` - no root config needed. This follows the next-forge pattern where apps are independent.

## App Config (Next.js Frontend)

```typescript
// apps/app/vitest.config.mts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    name: 'app',
    globals: true,
    environment: 'jsdom',  // jsdom: more mature, better compatibility

    // Performance
    pool: 'threads',
    maxWorkers: '75%',
    isolate: true,
    fileParallelism: true,

    // Test files
    include: [
      'src/**/*.{test,spec}.{ts,tsx}',
      '__tests__/**/*.{test,spec}.{ts,tsx}',
    ],
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/.next/**',
      '**/e2e/**',
    ],

    // Setup
    setupFiles: ['./__tests__/setup.ts'],
    testTimeout: 10000,

    // V8 coverage
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}', 'app/**/*.{ts,tsx}'],
      exclude: [
        '**/node_modules/**',
        '**/*.d.ts',
        '**/__tests__/**',
        '**/*.test.{ts,tsx}',
        '**/*.spec.{ts,tsx}',
        '**/*.config.*',
        '**/types/**',
      ],
      reporter: ['text', 'html', 'json', 'lcov'],
      reportsDirectory: './coverage',
      thresholds: {
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80,
      },
    },
  },
})
```

## App Setup File

```typescript
// apps/app/__tests__/setup.ts
import { afterEach, beforeEach, vi, expect } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// IMPORTANT: Vitest 4.x requires explicit expect.extend for jest-dom matchers
expect.extend(matchers)

// Cleanup after each test
afterEach(() => cleanup())

// Reset mocks between tests
beforeEach(() => vi.clearAllMocks())

// Mock ResizeObserver (not available in jsdom)
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock IntersectionObserver (not available in jsdom)
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
  root: null,
  rootMargin: '',
  thresholds: [],
  takeRecords: () => [],
}))

// Mock matchMedia for responsive components
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock scrollTo (not available in jsdom)
window.scrollTo = vi.fn()
Element.prototype.scrollTo = vi.fn()
Element.prototype.scrollIntoView = vi.fn()
```

## Backend Config (Convex)

```typescript
// packages/backend/vitest.config.mts
import { defineConfig } from 'vitest/config'
import path from 'node:path'

export default defineConfig({
  test: {
    name: 'backend',
    globals: true,
    environment: 'edge-runtime',

    // Convex-test requires these settings
    server: {
      deps: {
        inline: ['convex-test', 'convex'],
      },
    },

    // Use forks for Convex isolation
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true,  // Convex tests need isolation
      },
    },

    // Test files
    include: ['convex/**/*.test.ts', 'convex/__tests__/**/*.test.ts'],
    exclude: ['**/node_modules/**', '**/convex/_generated/**'],

    // Timeout for Convex operations
    testTimeout: 30000,
    hookTimeout: 30000,

    // V8 coverage
    coverage: {
      provider: 'v8',
      include: ['convex/**/*.ts'],
      exclude: [
        '**/node_modules/**',
        '**/convex/_generated/**',
        '**/*.test.ts',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      reporter: ['text', 'html', 'json', 'lcov'],
      reportsDirectory: './coverage',
      thresholds: {
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './convex'),
    },
  },
})
```

## UI Package Config

```typescript
// packages/design/vitest.config.mts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    name: 'design',
    globals: true,
    environment: 'jsdom',

    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**'],

    setupFiles: ['./__tests__/setup.ts'],
    testTimeout: 10000,

    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        '**/node_modules/**',
        '**/*.d.ts',
        '**/__tests__/**',
        '**/*.test.{ts,tsx}',
      ],
      reporter: ['text', 'html', 'json', 'lcov'],
      reportsDirectory: './coverage',
    },
  },
})
```

## Coverage Thresholds

### Greenfield Projects
```typescript
thresholds: {
  statements: 80,
  branches: 75,
  functions: 80,
  lines: 80,
}
```

### Legacy Projects (Adopting TDD)
```typescript
thresholds: {
  statements: 60,
  branches: 50,
  functions: 60,
  lines: 60,
}
```

## Codecov Configuration

```yaml
# codecov.yml
coverage:
  precision: 2
  round: down
  range: "50...100"

status:
  project:
    default:
      target: auto
      threshold: 2%
    critical:
      target: 90%
      paths:
        - "packages/backend/convex/core/**"
        - "apps/app/src/core/**"
  patch:
    default:
      target: 60%

flag_management:
  individual_flags:
    - name: frontend
      paths:
        - "apps/app/**"
        - "packages/design/**"
      carryforward: true
    - name: backend
      paths:
        - "packages/backend/**"
      carryforward: true
```
