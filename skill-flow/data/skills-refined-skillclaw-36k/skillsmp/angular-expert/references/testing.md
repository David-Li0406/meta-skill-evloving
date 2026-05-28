# Angular Testing Strategy

Production-grade testing for Angular v21+ with Zoneless change detection, Vitest, and Sociable testing philosophy. Load when writing tests or setting up test infrastructure.

## Table of Contents
1. [Zoneless Testing Fundamentals](#zoneless-testing-fundamentals)
2. [Vitest Configuration](#vitest-configuration)
3. [Sociable Testing Deep Dive](#sociable-testing-deep-dive)
4. [MSW Network Mocking](#msw-network-mocking)
5. [Component Harnesses](#component-harnesses)
6. [Visual Regression Testing](#visual-regression-testing)

---

## Zoneless Testing Fundamentals

### The Paradigm Shift

Angular v21 is Zoneless by default. `zone.js` is removed from the build pipeline. Change Detection (CD) triggers explicitly:
- Signal updates bound in templates
- Event listeners fire
- AsyncPipe receives emission
- Explicit `markForCheck()` or `ComponentRef.setInput()`

### Obsolete Patterns

**`fakeAsync`/`tick()` are incompatible** with Zoneless. They rely on Zone.js patches that no longer exist.

```typescript
// ❌ LEGACY (Zone.js) - DO NOT USE
it('should show loader', fakeAsync(() => {
  component.initiateLoad();
  tick(100);
  fixture.detectChanges();
  expect(loader).toBeTruthy();
}));

// ✅ MODERN (Zoneless)
it('should show loader', async () => {
  await component.initiateLoad();
  await fixture.whenStable();
  fixture.detectChanges();
  expect(loader).toBeTruthy();
});
```

### Key Synchronization APIs

| Feature | Angular v16 (Zone.js) | Angular v21 (Zoneless) |
|---------|----------------------|------------------------|
| Async Handling | `fakeAsync` / `tick()` | Native `async/await` |
| Change Detection | Auto (mostly) | Explicit `detectChanges()` |
| Effect Flushing | N/A | `TestBed.tick()` |
| Stability | `whenStable()` (Zone queue) | `whenStable()` (PendingTasks) |

### TestBed.tick() for Effects

Use `TestBed.tick()` after setting signals that drive `effect()`:

```typescript
it('should trigger effect', async () => {
  component.userName.set('John');
  TestBed.tick(); // Flush effect queue
  fixture.detectChanges();
  expect(sideEffectResult).toBe('expected');
});
```

---

## Vitest Configuration

### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';
import angular from '@analogjs/vite-plugin-angular';

export default defineConfig({
  plugins: [angular()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['src/test-setup.ts'],
    include: ['**/*.spec.ts'],
    reporters: ['default'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/e2e/**'],
    pool: 'threads',
    poolOptions: {
      threads: { isolate: true },
    },
  },
});
```

### src/test-setup.ts

```typescript
import '@testing-library/jest-dom';
import { getTestBed } from '@angular/core/testing';
import {
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting,
} from '@angular/platform-browser-dynamic/testing';

// Initialize WITHOUT zone.js
getTestBed().initTestEnvironment(
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting(),
  { teardown: { destroyAfterEach: true } }
);

// Mock browser APIs not in JSDOM
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }),
});
```

---

## Sociable Testing Deep Dive

### The No-Mock Policy

Test the **Unit of Work** (Component + Services + Pipes), not the Unit of Code.

**Mock ONLY at System Boundaries:**
- ✅ Network (HTTP requests) - use MSW
- ✅ Browser APIs (`localStorage`, `window.location`)
- ✅ Time (`Date.now()`)
- ✅ Hardware (Camera, Geolocation)

**NEVER Mock:**
- ❌ `UserService` (Logic)
- ❌ `FormatPipe` (Transformation)
- ❌ `SharedUiComponent` (Presentation)

### Configuration Comparison

| Aspect | Mockist (BANNED) | Sociable (REQUIRED) |
|--------|------------------|---------------------|
| Service Provision | `{ provide: ApiService, useValue: spyObj }` | `providers: [provideHttpClient()]` |
| Verification | `expect(spy.getUsers).toHaveBeenCalled()` | `expect(screen.getByText('John')).toBeVisible()` |
| Network | `spy.getUsers.and.returnValue(of(data))` | `msw.use(rest.get('/users',...))` |
| Refactoring Safety | Low (implementation leaked) | High (behavior tested) |

### Why Sociable?

Mockist tests break when:
- Service method signature changes → mock becomes a lie
- Internal refactoring extracts logic to helper → spies break
- Test passes but app crashes in production

Sociable tests verify **observable behavior** (DOM state, network interactions) - the same things users see.

---

## MSW Network Mocking

### The Zero-Drift Pipeline

Use OpenAPI as single source of truth:

1. Backend publishes `openapi.yaml`
2. Frontend runs Orval
3. Orval generates:
   - TypeScript interfaces
   - Angular HttpClient services
   - MSW Request Handlers
   - Zod validation schemas

### Orval Configuration

```typescript
// orval.config.ts
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: './src/api/openapi.yaml',
    output: {
      mode: 'tags-split',
      target: './src/api/endpoints',
      schemas: './src/api/models',
      client: 'angular',
      mock: true, // Generates MSW handlers with Faker.js
    },
  },
  zod: {
    input: './src/api/openapi.yaml',
    output: {
      mode: 'tags-split',
      client: 'zod',
      target: './src/api/schemas',
      fileExtension: '.zod.ts',
    },
  },
});
```

### Using MSW in Tests

```typescript
import { setupServer } from 'msw/node';
import { getUserMockHandler } from './api/endpoints/user/user.msw';
import { render, screen } from '@testing-library/angular';
import { provideHttpClient } from '@angular/common/http';

const server = setupServer(getUserMockHandler());

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('should display user data', async () => {
  // Override for specific test
  server.use(
    getUserMockHandler((req, res, ctx) =>
      res(ctx.json({ id: '123', name: 'Test User' }))
    )
  );

  await render(UserComponent, {
    providers: [provideHttpClient()]
  });

  expect(await screen.findByText('Test User')).toBeVisible();
});
```

### Zod Validator Bridge

Ensure frontend validation matches backend schema:

```typescript
// util/zod-validator.ts
import { Validator } from '@angular/forms/signals';
import { z } from 'zod';

export function zodValidator<T>(schema: z.ZodSchema<T>): Validator<T> {
  return (control) => {
    const result = schema.safeParse(control.value());
    if (result.success) return null;
    return result.error.errors.map(e => e.message);
  };
}
```

---

## Component Harnesses

### Why Harnesses?

Harnesses act as Page Object Model for components. Tests become resilient to DOM changes.

```typescript
// ❌ FRAGILE: Breaks if class name changes
const button = fixture.debugElement.query(By.css('.save-btn'));

// ✅ RESILIENT: Abstracted via harness
const isSaveDisabled = await harness.isSaveDisabled();
```

### Custom Harness Example

```typescript
// user-profile.harness.ts
import { ComponentHarness } from '@angular/cdk/testing';

export class UserProfileHarness extends ComponentHarness {
  static hostSelector = 'user-profile';

  protected getSubmitButton = this.locatorFor('button[type="submit"]');
  protected getEmailInput = this.locatorFor('input[type="email"]');
  protected getErrorMessages = this.locatorForAll('.error');

  async enterEmail(email: string) {
    const input = await this.getEmailInput();
    await input.setInputValue(email);
    await input.blur();
  }

  async save() {
    const button = await this.getSubmitButton();
    await button.click();
  }

  async isSaveDisabled(): Promise<boolean> {
    const button = await this.getSubmitButton();
    return button.isDisabled();
  }

  async getErrors(): Promise<string[]> {
    const errors = await this.getErrorMessages();
    return Promise.all(errors.map(e => e.text()));
  }
}
```

### Using Harness in Tests

```typescript
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { UserProfileHarness } from './user-profile.harness';

let harness: UserProfileHarness;

beforeEach(async () => {
  fixture = TestBed.createComponent(UserProfileComponent);
  await fixture.whenStable();

  const loader = TestbedHarnessEnvironment.loader(fixture);
  harness = await loader.getHarness(UserProfileHarness);
});

it('should validate email', async () => {
  await harness.enterEmail('invalid');
  expect(await harness.isSaveDisabled()).toBe(true);
  expect(await harness.getErrors()).toContain('Invalid email format');
});
```

---

## Visual Regression Testing

### The Font Rendering Problem

Browser rendering varies by OS (CoreText on macOS vs FreeType on Linux). Solution: containerized Linux with pinned fonts.

### Dockerized Playwright

```dockerfile
# Dockerfile.vrt
FROM mcr.microsoft.com/playwright:v1.49.0-jammy

RUN apt-get update && apt-get install -y \
    fonts-liberation \
    fonts-noto-color-emoji \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./.devcontainer/fonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build-storybook

CMD ["npx", "playwright", "test", "--config=playwright.vrt.config.ts"]
```

### Playwright VRT Configuration

```typescript
// playwright.vrt.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './vrt',
  updateSnapshots: process.env.CI ? 'none' : 'missing',
  use: {
    trace: 'on-first-retry',
    viewport: { width: 1280, height: 720 },
  },
  webServer: {
    command: 'npx http-server ./storybook-static -p 6006',
    port: 6006,
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### Workflow

```bash
# Run VRT in Docker (consistent results)
npm run vrt:docker

# Update baselines in Docker
npm run vrt:update
```

**Never run VRT directly on host machine** - results will differ between developers.

---

## Test Layer Definitions

| Layer | Responsibility | Test Strategy |
|-------|----------------|---------------|
| Logic (Services/Stores) | Business rules, API, State | Unit tests with MSW. No DOM. |
| Interaction (Components) | Binding, event handling | Sociable tests via Testing Library + Harnesses |
| Presentation (Templates/CSS) | Layout, styling | Visual Regression via Playwright |
