# Testing with Environment Variables

## Mocking in Tests

### Vitest Setup

```typescript
// tests/unit/vitest.setup.ts
import { vi } from "vitest";

// Mock environment variables before imports
vi.stubEnv("NODE_ENV", "test");
vi.stubEnv("LOG_LEVEL", "error");
vi.stubEnv("SKIP_ENV_VALIDATION", "true");

// Mock server env vars
vi.stubEnv("CLERK_SECRET_KEY", "sk_test_mock_key");
vi.stubEnv("FIREBASE_PROJECT_ID", "test-project");
vi.stubEnv("FIREBASE_CLIENT_EMAIL", "test@test.iam.gserviceaccount.com");
vi.stubEnv("FIREBASE_PRIVATE_KEY", "mock-private-key");

// Mock client env vars
vi.stubEnv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY", "pk_test_mock_key");
vi.stubEnv("NEXT_PUBLIC_CLERK_SIGN_IN_URL", "/sign-in");
vi.stubEnv("NEXT_PUBLIC_CLERK_SIGN_UP_URL", "/sign-up");
```

### Per-Test Mocking

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

describe("feature with env dependency", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    vi.resetModules();
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("should use custom log level", async () => {
    process.env.LOG_LEVEL = "debug";
    process.env.SKIP_ENV_VALIDATION = "true";

    // Re-import module to pick up new env
    const { env } = await import("~/data/env/server");

    expect(env.LOG_LEVEL).toBe("debug");
  });
});
```

### Using vi.stubEnv

```typescript
import { describe, it, expect, vi } from "vitest";

describe("environment-dependent feature", () => {
  it("should behave differently in production", () => {
    vi.stubEnv("NODE_ENV", "production");

    // Test production behavior
    expect(process.env.NODE_ENV).toBe("production");

    vi.unstubAllEnvs();
  });

  it("should use default log level", () => {
    vi.stubEnv("LOG_LEVEL", undefined);
    vi.stubEnv("SKIP_ENV_VALIDATION", "true");

    // Module uses default "info"
  });
});
```

## Test Environment File

Create `.env.test` for consistent test values:

```bash
# .env.test
NODE_ENV=test
LOG_LEVEL=error
SKIP_ENV_VALIDATION=true

# Clerk test keys
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxx
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxx
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/onboarding

# Firebase test config
FIREBASE_PROJECT_ID=test-project-id
FIREBASE_CLIENT_EMAIL=test@test.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMOCK_KEY\n-----END PRIVATE KEY-----"
```

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig, loadEnv } from "vitest/config";

export default defineConfig({
  test: {
    env: loadEnv("test", process.cwd(), ""),
    setupFiles: ["./tests/unit/vitest.setup.ts"],
  },
});
```

## Testing Validation Logic

### Test Valid Configuration

```typescript
import { describe, it, expect, vi } from "vitest";
import { z } from "zod";

describe("environment validation", () => {
  it("should validate correct LOG_LEVEL", () => {
    const schema = z.enum(["fatal", "error", "warn", "info", "debug", "trace"]);

    expect(schema.parse("info")).toBe("info");
    expect(schema.parse("debug")).toBe("debug");
  });

  it("should reject invalid LOG_LEVEL", () => {
    const schema = z.enum(["fatal", "error", "warn", "info", "debug", "trace"]);

    expect(() => schema.parse("invalid")).toThrow();
  });

  it("should transform boolean strings", () => {
    const schema = z
      .enum(["true", "false"])
      .transform((val) => val === "true");

    expect(schema.parse("true")).toBe(true);
    expect(schema.parse("false")).toBe(false);
  });
});
```

### Test Default Values

```typescript
import { describe, it, expect } from "vitest";
import { z } from "zod";

describe("default values", () => {
  it("should use default when undefined", () => {
    const schema = z.string().optional().default("default-value");

    expect(schema.parse(undefined)).toBe("default-value");
  });

  it("should not use default when value provided", () => {
    const schema = z.string().optional().default("default-value");

    expect(schema.parse("custom")).toBe("custom");
  });
});
```

## Mocking for Integration Tests

### Database Connection String

```typescript
import { describe, it, vi, beforeAll } from "vitest";

describe("database integration", () => {
  beforeAll(() => {
    // Use test database
    vi.stubEnv("DATABASE_URL", "postgresql://localhost:5432/test_db");
    vi.stubEnv("SKIP_ENV_VALIDATION", "true");
  });

  it("should connect to test database", async () => {
    // Integration test using test database
  });
});
```

### External Service Mocking

```typescript
import { describe, it, vi } from "vitest";

describe("external service", () => {
  it("should use mock API endpoint", () => {
    vi.stubEnv("EXTERNAL_API_URL", "http://localhost:3001/mock-api");

    // Test with mock API
  });
});
```

## E2E Testing

For Playwright E2E tests, set environment in `playwright.config.ts`:

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  use: {
    baseURL: "http://localhost:3000",
  },
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    env: {
      NODE_ENV: "test",
      LOG_LEVEL: "error",
      // ... other env vars
    },
  },
});
```

## CI/CD Environment

### GitHub Actions

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: test
      SKIP_ENV_VALIDATION: true
      CLERK_SECRET_KEY: ${{ secrets.CLERK_SECRET_KEY_TEST }}
      NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY_TEST }}
      # ... other vars

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test
```

### Docker Testing

```dockerfile
# Dockerfile.test
FROM node:20-alpine

WORKDIR /app
COPY . .

ENV NODE_ENV=test
ENV SKIP_ENV_VALIDATION=true
ENV LOG_LEVEL=error

RUN npm ci
RUN npm test
```

## Troubleshooting

### Module Not Picking Up New Env

```typescript
// Reset module cache before re-importing
vi.resetModules();
const { env } = await import("~/data/env/server");
```

### Validation Failing in Tests

```typescript
// Always set SKIP_ENV_VALIDATION in test setup
vi.stubEnv("SKIP_ENV_VALIDATION", "true");
```

### TypeScript Errors with Mocked Env

```typescript
// Use type assertion if needed
const mockEnv = {
  NODE_ENV: "test" as const,
  LOG_LEVEL: "error" as const,
};
```
