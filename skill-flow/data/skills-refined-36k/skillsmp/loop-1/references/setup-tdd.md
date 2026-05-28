# setup-tdd

TDD framework establishment patterns for different project types.

## philosophy

> "no tests, no confidence, no autonomy"

autonomous loops require test coverage. establish TDD before feature work.

## detection

| signal | framework | action |
|--------|-----------|--------|
| vitest.config.ts | vitest | ready |
| jest.config.js | jest | ready |
| playwright.config.ts | playwright | ready |
| convex/ + no tests | convex-test | setup needed |
| none | - | setup needed |

## setup by type

### convex stack (arbor pattern)

```bash
# install testing deps
pnpm add -D vitest convex-test @testing-library/react @testing-library/jest-dom msw

# create vitest config
cat > vitest.config.ts << 'EOF'
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
  },
});
EOF

# create convex vitest config
cat > convex/vitest.config.ts << 'EOF'
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "edge-runtime",
    server: { deps: { inline: ["convex-test"] } },
  },
});
EOF

# create test setup
mkdir -p tests
cat > tests/setup.ts << 'EOF'
import "@testing-library/jest-dom";
import { server } from "./mocks/server";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
EOF
```

### next.js

```bash
# install
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react

# config
cat > vitest.config.ts << 'EOF'
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
  },
});
EOF
```

### playwright E2E

```bash
# install
pnpm add -D @playwright/test
npx playwright install

# config
cat > playwright.config.ts << 'EOF'
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
EOF

mkdir -p tests/e2e
```

### xcode

```bash
# XCTest is built-in
# ensure test target exists in project

# check for test target
xcodebuild -list | grep -i test

# if missing, add via Xcode UI or:
# File > New > Target > Unit Testing Bundle
```

## verify CLI

```bash
# unified verify command
verify --format=summary

# or direct
pnpm vitest --run
pnpm playwright test
xcodebuild test -scheme AppScheme
```

## gold standard: turborepo structure

personal projects use turborepo monorepos:

```
project-xyz/
├── apps/
│   └── app/
│       ├── vitest.config.mts      # frontend unit tests
│       ├── playwright.config.ts   # E2E tests
│       ├── src/__tests__/
│       │   ├── setup.ts           # mock setup (convex, jotai, next)
│       │   └── *.test.tsx         # component tests
│       └── e2e/                   # playwright tests
├── packages/
│   └── backend/
│       ├── vitest.config.mts      # backend unit tests
│       ├── __tests__/
│       │   ├── setup.ts           # test helpers (createTestContext, withTestUser)
│       │   └── *.test.ts          # function tests
│       ├── test-setup/
│       │   └── convex.setup.ts    # modules export for convex-test
│       └── convex/
│           └── ...                # convex functions
└── turbo.json                     # monorepo tasks
```

### backend test setup (packages/backend)

```typescript
// __tests__/setup.ts
import { convexTest } from 'convex-test';
import schema from '../convex/schema';
import { modules } from '../test-setup/convex.setup';

export type TestContext = ReturnType<typeof convexTest<typeof schema>>;

export function createTestContext(): TestContext {
  return convexTest(schema, modules);
}

// add withTest* helpers for each table
export async function withTestUser(t: TestContext, overrides = {}) {...}
export async function withTestArtwork(t: TestContext, userId, overrides = {}) {...}
```

### frontend test setup (apps/app)

```typescript
// src/__tests__/setup.ts
import * as matchers from '@testing-library/jest-dom/matchers';
import { cleanup } from '@testing-library/react';
import { afterEach, expect, vi } from 'vitest';

expect.extend(matchers);

// mock convex
export const mockUseQuery = vi.fn();
export const mockUseMutation = vi.fn(() => vi.fn());

vi.mock('convex/react', () => ({
  useQuery: mockUseQuery,
  useMutation: mockUseMutation,
  ConvexProvider: ({ children }) => children,
}));

// mock jotai
export const mockUseAtom = vi.fn(() => [null, vi.fn()]);
vi.mock('jotai', async () => ({
  ...(await vi.importActual('jotai')),
  useAtom: mockUseAtom,
}));

// mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  usePathname: () => '/',
}));

afterEach(() => cleanup());
```

## coverage targets

| area | minimum | ideal |
|------|---------|-------|
| convex functions | 80% | 95% |
| react components | 60% | 80% |
| E2E critical paths | 100% | 100% |
| utilities | 90% | 100% |

## anti-patterns

- **skipping setup**: no tests = no autonomous work
- **partial coverage**: cover critical paths first
- **slow tests**: keep unit tests fast (<5s total)
- **flaky E2E**: fix or skip, don't ignore
