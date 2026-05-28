# Vitest Configuration Examples

## ✅ RECOMMENDED FOR VUE 3 PROJECTS

**Date**: January 2026
**Status**: Current and actively maintained

Before using this example:
1. ✅ Verify Vitest is at latest stable version
2. ✅ Verify `@vitest/coverage-v8` is still recommended coverage provider
3. ✅ Verify `@vitejs/plugin-vue` version matches your Vite version
4. ✅ Check if `jsdom` is still recommended over `happy-dom`
5. ✅ Verify coverage threshold recommendations (currently 80%+)
6. ✅ Check for new Vitest features or configuration options

---

## Example: vitest.config.ts (Recommended Format)

**Configuration Date**: January 2026
**Vitest Version**: 2.x+
**Format**: TypeScript
**Status**: Officially recommended for Vue 3 + Vite

```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: false, // Explicit imports (recommended for modern projects)
    environment: 'jsdom', // DOM environment for Vue components
    setupFiles: ['./tests/unit/testSetup.ts'], // Setup file for test environment
    coverage: {
      provider: 'v8', // Fast and accurate coverage
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.spec.ts',
        '**/*.spec.js',
        '**/interfaces/**',
        '**/router/**',
        '**/services/**',
        '**/shared/constants/**',
        '**/shared/EnvConsts.ts',
        'src/store/index.ts',
        'src/App.vue',
        'src/main.ts',
        'src/shims-vue.d.ts',
        'src/**/*.d.ts',
        '**/*.config.{ts,js}',
        '**/dist/**',
        '**/coverage/**',
      ],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 80,
        statements: 80,
      },
    },
    include: [
      'src/**/*.spec.ts',
      'src/**/*.spec.js',
      'tests/**/*.spec.ts',
      'tests/**/*.spec.js',
    ],
    exclude: [
      'node_modules',
      'dist',
      'coverage',
      '.idea',
      '.git',
      '.cache',
    ],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
```

---

## Configuration Option Explanations

### Essential Options

**`plugins: [vue()]`**
- Vue plugin for transforming Vue SFC files
- **Why**: Vitest needs to understand `.vue` files
- **Verify**: Ensure `@vitejs/plugin-vue` version matches Vite version
- **Import**: `import vue from '@vitejs/plugin-vue'`

**`test.globals: false`**
- Requires explicit imports for test functions
- **Why**: Better IDE support, clearer dependencies, modern pattern
- **Recommended**: `false` for new projects
- **Usage**: Must import `describe`, `it`, `expect` from 'vitest'
```typescript
import { describe, it, expect } from 'vitest';
```

**Alternative** (`test.globals: true`):
```typescript
// No imports needed (like Jest)
describe('Component', () => {
  it('works', () => {
    expect(true).toBe(true);
  });
});
```

**`test.environment: 'jsdom'`**
- Simulates browser DOM environment for testing
- **Why**: Vue components require DOM APIs
- **Values**: `'jsdom'` (complete DOM) | `'happy-dom'` (faster, lighter) | `'node'` (no DOM)
- **Recommended**: `'jsdom'` for maximum compatibility
- **Alternative**: `'happy-dom'` if speed is priority and no compatibility issues

**`test.setupFiles`**
- Files to run before each test file
- **Why**: Configure test environment, global mocks, polyfills
- **Example**: Setup Vue test utils, mock window.matchMedia, etc.
- **Path**: `['./tests/unit/testSetup.ts']`

### Coverage Configuration

**`coverage.provider: 'v8'`**
- Uses V8's native code coverage (fast and accurate)
- **Why**: Best performance and accuracy for modern projects
- **Default**: Recommended for Vitest
- **Alternative**: `'istanbul'` (for Jest compatibility or specific tooling)
- **Install**: `npm install -D @vitest/coverage-v8`

**Coverage Reporters** (`coverage.reporter`):
```typescript
reporter: ['text', 'json', 'html', 'lcov']
```
- `'text'` - Console output
- `'json'` - JSON format for CI/CD
- `'html'` - HTML report for local viewing
- `'lcov'` - LCOV format for coverage tools (SonarQube, Codecov, etc.)

**`coverage.exclude`** - Files to exclude from coverage:
```typescript
exclude: [
  'node_modules/',              // Dependencies
  'tests/',                     // Test files themselves
  '**/*.spec.ts',              // Test files
  '**/interfaces/**',          // TypeScript interfaces (no runtime code)
  '**/router/**',              // Router config (tested via E2E)
  '**/services/**',            // Service layer (tested with mocks)
  '**/shared/constants/**',    // Static constants (no logic)
  'src/main.ts',               // App entry point (tested via E2E)
  'src/App.vue',               // Root component (tested via E2E)
  'src/**/*.d.ts',             // Type declaration files
  '**/*.config.{ts,js}',       // Config files
]
```

**Why exclude these files**:
- **Interfaces/Types**: No runtime code to test
- **Router**: Configuration files, tested through E2E tests
- **Services**: API calls are mocked in unit tests
- **Constants**: Static data with no business logic
- **main.ts**: Application bootstrap, tested through E2E
- **Declaration files**: Type definitions only

**`coverage.thresholds`** - Minimum coverage requirements:
```typescript
thresholds: {
  lines: 80,       // 80% of lines must be covered
  branches: 80,    // 80% of branches (if/else) must be covered
  functions: 80,   // 80% of functions must be covered
  statements: 80,  // 80% of statements must be covered
}
```

**Recommended Thresholds**:
- **80%**: Industry standard for production applications
- **90%**: High-quality, critical systems
- **70%**: Acceptable for legacy codebases
- **60%**: Minimum viable (not recommended)

**Enforcement**: Tests will fail if coverage falls below thresholds

### Test File Matching

**`test.include`** - Test file patterns to run:
```typescript
include: [
  'src/**/*.spec.ts',      // Component co-located tests
  'src/**/*.spec.js',      // JavaScript test files
  'tests/**/*.spec.ts',    // Centralized test directory
  'tests/**/*.spec.js',    // JavaScript tests in tests/
]
```

**Why co-located tests**:
- ✅ Tests live next to source code
- ✅ Easier to find and maintain
- ✅ Modern pattern for component-based architectures

**`test.exclude`** - Directories to ignore:
```typescript
exclude: [
  'node_modules',
  'dist',
  'coverage',
  '.idea',
  '.git',
  '.cache',
]
```

### Path Alias Resolution

**`resolve.alias`** - Import path aliases:
```typescript
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url)),
  },
}
```

**Why needed**:
- Resolves `@/` imports to `src/` directory
- Consistent with vite.config.ts aliases
- Enables absolute imports in tests

**Import example**:
```typescript
import { MyComponent } from '@/components/MyComponent.vue';
import { myService } from '@/services/myService';
```

**Note**: If you already have path aliases in `vite.config.ts`, Vitest will inherit them automatically. This configuration is redundant but explicit for clarity.

---

## Common Configuration Patterns

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import MyComponent from '@/components/MyComponent.vue';

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent);
    expect(wrapper.text()).toContain('Hello');
  });
});
```

**Note**: If `globals: true`, no need to import `describe`, `it`, `expect`

---

## Setup File Example

**File**: `tests/unit/testSetup.ts`

```typescript
import { vi } from 'vitest';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
} as any;

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
} as any;
```

---

## Troubleshooting

### Issue: "Cannot find module 'vitest'"
**Solution**: Install Vitest and its types
```bash
npm install -D vitest @vitest/ui @types/node
```

### Issue: "Cannot find module '@vitejs/plugin-vue'"
**Solution**: Install Vue plugin
```bash
npm install -D @vitejs/plugin-vue
```

### Issue: "Coverage provider 'v8' not found"
**Solution**: Install v8 coverage provider
```bash
npm install -D @vitest/coverage-v8
```

### Issue: Test environment 'jsdom' not found
**Solution**: Install jsdom
```bash
npm install -D jsdom
```

### Issue: Path aliases not resolving (@/ imports fail)
**Solution**: Verify `resolve.alias` in vitest.config.ts
```typescript
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url)),
  },
}
```

### Issue: Vue components not transforming
**Solution**: Ensure Vue plugin is included
```typescript
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  // ...
});
```

### Issue: "describe is not defined" when globals: false
**Solution**: Import test functions explicitly
```typescript
import { describe, it, expect } from 'vitest';
```

---

## Best Practices

### ✅ DO
- Use `globals: false` for better IDE support
- Set coverage thresholds (80%+ recommended)
- Co-locate test files with source code (`Component.spec.ts` next to `Component.vue`)
- Use `@vitest/coverage-v8` for best performance
- Import test utilities explicitly when globals disabled
- Configure path aliases for cleaner imports
- Use setup files for global test configuration
- Exclude infrastructure files from coverage

### ❌ DON'T
- Mix Jest and Vitest in the same project
- Set coverage thresholds below 70%
- Include test files in coverage reports
- Use `happy-dom` without testing compatibility first
- Forget to install coverage provider package
- Hardcode absolute paths (use path aliases)
- Test configuration files or type definitions

---

## Important Reminders

1. **Vitest is Recommended**: Official recommendation for Vue 3 + Vite projects
2. **No Transformers Needed**: Vitest uses Vite's built-in transformation (no ts-jest)
3. **ESM Native**: Handles ESM packages automatically (no transformIgnorePatterns)
4. **Coverage Provider**: v8 is default and recommended
5. **Globals Disabled**: Better IDE support with explicit imports
6. **TypeScript Format**: Use `.ts` config files for type safety
7. **Coverage Thresholds**: Set minimum 80% for production quality
8. **Test Environment**: jsdom for maximum compatibility
9. **Path Aliases**: Automatically resolved from Vite config
10. **Setup Files**: Use for global test configuration and mocks
11. **Performance**: Significantly faster than Jest for Vite projects
12. **HMR Support**: Tests hot reload during development
