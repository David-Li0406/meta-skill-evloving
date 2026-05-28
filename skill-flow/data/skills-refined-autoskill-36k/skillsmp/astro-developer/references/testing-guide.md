# Testing Guide for Astro Projects

This comprehensive guide covers testing strategies for Astro projects, including unit tests, integration tests, and end-to-end tests with modern testing frameworks.

## Table of Contents

1. [Overview](#overview)
2. [Unit Testing with Vitest](#unit-testing-with-vitest)
3. [Component Testing with Container API](#component-testing-with-container-api)
4. [End-to-End Testing with Playwright](#end-to-end-testing-with-playwright)
5. [Testing React Components](#testing-react-components)
6. [Common Testing Patterns](#common-testing-patterns)
7. [Best Practices](#best-practices)

## Overview

Astro supports multiple testing frameworks for different testing needs:

- **Vitest**: Fast unit tests with native Vite integration
- **Playwright**: End-to-end testing across browsers
- **Cypress**: Alternative E2E testing framework
- **Container API**: Test Astro components directly

## Unit Testing with Vitest

### Installation

```bash
npm install -D vitest @vitest/ui jsdom
```

### Configuration

Create `vitest.config.ts` in your project root:

```typescript
/// <reference types="vitest" />

import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    // Vitest configuration options
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    exclude: ['node_modules', 'dist', '.astro'],
  },
});
```

### Custom Astro Configuration

As of Astro 4.8, customize the Astro configuration applied in tests:

```typescript
export default getViteConfig(
  { test: { /* Vitest configuration options */ } },
  {
    site: 'https://example.com/',
    trailingSlash: 'always',
  }
);
```

### Running Tests

Add test scripts to `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run"
  }
}
```

## Component Testing with Container API

Astro 4.9+ includes the Container API for natively testing Astro components.

### Basic Component Test

```javascript
// src/components/Card.test.js
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test } from 'vitest';
import Card from '../src/components/Card.astro';

test('Card with slots', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    slots: {
      default: 'Card content',
    },
  });

  expect(result).toContain('This is a card');
  expect(result).toContain('Card content');
});
```

### Testing with Props

```javascript
test('Card with custom title', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: {
      title: 'Test Title',
      variant: 'primary'
    },
  });

  expect(result).toContain('Test Title');
  expect(result).toContain('bg-blue-500');
});
```

### Testing Conditional Rendering

```javascript
test('Card shows featured badge when featured=true', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: { featured: true }
  });

  expect(result).toContain('Featured');
});
```

## End-to-End Testing with Playwright

### Installation

```bash
npm init playwright@latest
```

### Configuration

Create `playwright.config.ts`:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4321/',
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:4321/',
  },
});
```

### Basic E2E Test

```typescript
// src/test/index.spec.ts
import { test, expect } from '@playwright/test';

test('meta is correct', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle('Astro is awesome!');
});

test('heading is visible', async ({ page }) => {
  await page.goto('/');
  const heading = page.getByRole('heading', { name: 'Hello world' });
  await expect(heading).toBeVisible();
});
```

### Testing Interactive Elements

```typescript
test('counter increments', async ({ page }) => {
  await page.goto('/counter');

  // Get initial count
  const count = page.getByTestId('count');
  await expect(count).toHaveText('0');

  // Click increment button
  const button = page.getByRole('button', { name: 'Increment' });
  await button.click();

  // Verify count updated
  await expect(count).toHaveText('1');
});
```

### Testing Navigation

```typescript
test('navigation works', async ({ page }) => {
  await page.goto('/');

  // Click navigation link
  const link = page.getByRole('link', { name: 'About' });
  await link.click();

  // Verify URL changed
  await expect(page).toHaveURL(/.*\/about/);
  await expect(page).toHaveTitle('About Us');
});
```

### Testing Forms

```typescript
test('contact form submission', async ({ page }) => {
  await page.goto('/contact');

  // Fill out form
  await page.getByLabel('Name').fill('John Doe');
  await page.getByLabel('Email').fill('john@example.com');
  await page.getByLabel('Message').fill('Test message');

  // Submit form
  await page.getByRole('button', { name: 'Send' }).click();

  // Verify success message
  await expect(page.getByText('Message sent successfully')).toBeVisible();
});
```

## Testing React Components

### Installation

```bash
npm install -D @testing-library/react @testing-library/jest-dom
```

### Vitest Setup

Update `vitest.config.ts`:

```typescript
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

### Setup File

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
```

### React Component Test

```typescript
// src/components/Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Counter from './Counter';

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={5} />);
    expect(screen.getByText('Count: 5')).toBeInTheDocument();
  });

  it('increments count', () => {
    render(<Counter initialCount={0} />);
    const button = screen.getByRole('button', { name: 'Increment' });
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('decrements count', () => {
    render(<Counter initialCount={5} />);
    const button = screen.getByRole('button', { name: 'Decrement' });
    fireEvent.click(button);
    expect(screen.getByText('Count: 4')).toBeInTheDocument();
  });
});
```

## Common Testing Patterns

### Testing API Routes

```typescript
// src/test/api/posts.test.ts
import { describe, it, expect } from 'vitest';

describe('/api/posts', () => {
  it('returns posts list', async () => {
    const response = await fetch('/api/posts');
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.posts).toBeDefined();
    expect(Array.isArray(data.posts)).toBe(true);
  });
});
```

### Testing Content Collections

```javascript
// src/test/content.test.js
import { describe, it, expect } from 'vitest';
import { getCollection } from 'astro:content';

describe('Blog collection', () => {
  it('has valid frontmatter', async () => {
    const posts = await getCollection('blog');

    for (const post of posts) {
      expect(post.data.title).toBeDefined();
      expect(post.data.pubDate).toBeInstanceOf(Date);
      expect(post.data.description).toBeDefined();
    }
  });
});
```

### Testing View Transitions

```typescript
test('view transition animation', async ({ page }) => {
  await page.goto('/');

  // Navigate to another page
  await page.getByRole('link', { name: 'About' }).click();

  // Wait for transition to complete
  await page.waitForURL('/about');

  // Verify new page content
  await expect(page.getByText('About Us')).toBeVisible();
});
```

## Best Practices

### 1. Test Structure

- **Arrange, Act, Assert**: Organize tests clearly
- **Descriptive names**: Make test names self-explanatory
- **One assertion per test**: Keep tests focused

### 2. Testing Strategy

- **Unit tests**: Test individual components and functions
- **Integration tests**: Test component interactions
- **E2E tests**: Test critical user flows

### 3. What to Test

- **Component rendering**: Verify components display correctly
- **User interactions**: Test clicks, form submissions, navigation
- **Edge cases**: Test empty states, error handling
- **Accessibility**: Verify ARIA labels, keyboard navigation

### 4. What NOT to Test

- Implementation details (private methods, internal state)
- Third-party libraries (assume they work)
- Static content that never changes

### 5. Performance Tips

- **Parallel execution**: Run tests concurrently by default
- **Selective testing**: Run only affected tests during development
- **Mock external services**: Don't make real network requests

### 6. CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test
```

### 7. Code Coverage

```typescript
// vitest.config.ts
export default getViteConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
});
```

## Sources

- [Astro Testing Documentation](https://docs.astro.build/en/guides/testing/)
- [Vitest Configuration](https://vitest.dev/config/)
- [vitest-browser-astro](https://github.com/ascorbic/vitest-browser-astro/)
- [Astro Unit Tests Guide](https://angelika.me/2025/02/01/astro-component-unit-tests/)
