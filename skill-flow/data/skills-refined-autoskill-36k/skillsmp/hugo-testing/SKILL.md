---
name: hugo-testing
description: This skill should be used when the user mentions "test javascript", "bun test", "unit test", "happy-dom", "test client-side js", "dom mocking", "browser tests", "test theme toggle", "test scroll handlers", or any testing of JavaScript code in Hugo projects. Provides comprehensive guidance for testing client-side JavaScript using Bun's test runner with happy-dom for DOM environment simulation.
---

# Testing Client-Side JavaScript in Hugo Projects

## Overview

Hugo sites often include client-side JavaScript for interactive features like theme toggles, search functionality, scroll handlers, and dynamic content loading. Testing this code requires special consideration because it runs in a browser environment with access to the DOM, `window`, and `document` objects. This guide covers how to test both pure utility functions and DOM-dependent code using Bun's built-in test runner with happy-dom for DOM mocking.

## Test Setup with Bun Test

### Bun's Built-In Test Runner

Bun includes a fast, Jest-compatible test runner that requires zero configuration for basic tests. The runner automatically discovers test files and provides familiar assertion APIs.

```bash
# Run all tests
bun test

# Run via package.json script (PREFERRED)
bun run test

# Run specific test file
bun test tests/js/theme.test.js

# Watch mode for development
bun test --watch

# Show coverage report
bun test --coverage
```

### Why Use Bun for Testing?

- **Speed**: Bun's test runner is significantly faster than Jest or Vitest
- **Zero config**: Works out of the box with no setup files needed
- **Native TypeScript**: Runs .ts test files without transpilation
- **Jest compatibility**: Familiar `describe`, `test`, `expect` APIs
- **Built-in mocking**: Includes spies, mocks, and module mocking

## happy-dom for DOM Mocking

### Why DOM Mocking is Necessary

Client-side JavaScript in Hugo projects typically interacts with:
- `document.querySelector()` and DOM element manipulation
- `window.matchMedia()` for responsive behavior
- `localStorage` for persisting user preferences
- Event listeners on DOM elements
- `fetch()` for dynamic content loading

These APIs don't exist in a pure JavaScript runtime like Bun or Node.js. happy-dom provides a lightweight, fast implementation of the browser DOM environment.

### Installation

```bash
bun add -D happy-dom
```

### Basic Setup Pattern

Create a test setup file or include this pattern at the top of tests that need DOM access:

```javascript
import { Window } from 'happy-dom';

// Create a new browser-like environment
const window = new Window();
const document = window.document;

// Expose to global scope so code under test can access them
globalThis.document = document;
globalThis.window = window;
globalThis.HTMLElement = window.HTMLElement;
globalThis.localStorage = window.localStorage;
globalThis.matchMedia = window.matchMedia.bind(window);
```

### Reusable Test Helpers

For projects with many DOM tests, create a shared setup helper:

```javascript
// tests/helpers/dom-setup.js
import { Window } from 'happy-dom';

export function createDOMEnvironment(html = '<!DOCTYPE html><html><body></body></html>') {
  const window = new Window();
  window.document.write(html);

  globalThis.document = window.document;
  globalThis.window = window;
  globalThis.HTMLElement = window.HTMLElement;
  globalThis.localStorage = window.localStorage;
  globalThis.matchMedia = window.matchMedia.bind(window);

  return { window, document: window.document };
}

export function cleanupDOMEnvironment() {
  delete globalThis.document;
  delete globalThis.window;
  delete globalThis.HTMLElement;
  delete globalThis.localStorage;
  delete globalThis.matchMedia;
}
```

## Test File Organization

### Directory Structure

Organize tests in a dedicated `tests/` directory, separate from Hugo's source:

```
your-hugo-site/
├── assets/
│   └── js/
│       ├── theme.js
│       ├── search.js
│       └── scroll.js
├── tests/
│   ├── js/
│   │   ├── theme.test.js
│   │   ├── search.test.js
│   │   └── scroll.test.js
│   └── helpers/
│       └── dom-setup.js
├── package.json
└── bun.lock
```

### Naming Conventions

Bun automatically discovers test files matching these patterns:
- `*.test.js` or `*.test.ts`
- `*.spec.js` or `*.spec.ts`
- Files in `__tests__/` directories

**Recommendation**: Use `*.test.js` for consistency and place in `tests/js/` directory.

## package.json Configuration

### Minimal Setup

```json
{
  "name": "your-hugo-site",
  "private": true,
  "scripts": {
    "test": "bun test",
    "test:watch": "bun test --watch",
    "test:coverage": "bun test --coverage"
  },
  "devDependencies": {
    "happy-dom": "^15.0.0"
  }
}
```

### With Additional Test Utilities

```json
{
  "name": "your-hugo-site",
  "private": true,
  "scripts": {
    "test": "bun test",
    "test:watch": "bun test --watch",
    "test:coverage": "bun test --coverage",
    "test:js": "bun test tests/js/"
  },
  "devDependencies": {
    "happy-dom": "^15.0.0"
  }
}
```

## Testing Strategies for Client-Side JavaScript

### Strategy 1: Pure Functions (No DOM Needed)

Many utility functions don't require DOM access and can be tested directly. These are the easiest to test and should be extracted from DOM-dependent code when possible.

**Examples of pure functions in Hugo sites:**
- Theme color hashing algorithms
- Data transformations for search indexes
- URL parsing utilities
- Date formatting functions
- Slug generation

```javascript
// assets/js/utils.js
export function hashStringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash % 360);
  return `hsl(${hue}, 70%, 50%)`;
}

export function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');
}
```

```javascript
// tests/js/utils.test.js
import { describe, test, expect } from 'bun:test';
import { hashStringToColor, slugify } from '../../assets/js/utils.js';

describe('hashStringToColor', () => {
  test('returns consistent color for same input', () => {
    const color1 = hashStringToColor('test');
    const color2 = hashStringToColor('test');
    expect(color1).toBe(color2);
  });

  test('returns different colors for different inputs', () => {
    const color1 = hashStringToColor('hello');
    const color2 = hashStringToColor('world');
    expect(color1).not.toBe(color2);
  });

  test('returns valid HSL color format', () => {
    const color = hashStringToColor('example');
    expect(color).toMatch(/^hsl\(\d+, 70%, 50%\)$/);
  });
});

describe('slugify', () => {
  test('converts to lowercase', () => {
    expect(slugify('Hello World')).toBe('hello-world');
  });

  test('replaces spaces with hyphens', () => {
    expect(slugify('foo bar baz')).toBe('foo-bar-baz');
  });

  test('removes special characters', () => {
    expect(slugify('Hello! World?')).toBe('hello-world');
  });
});
```

### Strategy 2: DOM-Dependent Code with happy-dom

Code that manipulates the DOM, handles events, or accesses browser APIs requires the happy-dom environment.

```javascript
// assets/js/theme.js
export function initThemeToggle() {
  const toggle = document.querySelector('[data-theme-toggle]');
  if (!toggle) return;

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  toggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
}
```

```javascript
// tests/js/theme.test.js
import { describe, test, expect, beforeEach, afterEach } from 'bun:test';
import { Window } from 'happy-dom';

describe('Theme Toggle', () => {
  let window;
  let document;

  beforeEach(() => {
    window = new Window();
    document = window.document;

    // Set up globals
    globalThis.document = document;
    globalThis.window = window;
    globalThis.localStorage = window.localStorage;

    // Create test DOM structure
    document.body.innerHTML = `
      <button data-theme-toggle>Toggle Theme</button>
    `;
  });

  afterEach(() => {
    window.close();
    delete globalThis.document;
    delete globalThis.window;
    delete globalThis.localStorage;
  });

  test('applies saved theme from localStorage on init', async () => {
    localStorage.setItem('theme', 'dark');

    const { initThemeToggle } = await import('../../assets/js/theme.js');
    initThemeToggle();

    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });

  test('toggles theme on button click', async () => {
    document.documentElement.setAttribute('data-theme', 'light');

    const { initThemeToggle } = await import('../../assets/js/theme.js');
    initThemeToggle();

    const toggle = document.querySelector('[data-theme-toggle]');
    toggle.click();

    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
```

### Strategy 3: Testing Event Handlers

```javascript
// tests/js/scroll.test.js
import { describe, test, expect, beforeEach, afterEach, mock } from 'bun:test';
import { Window } from 'happy-dom';

describe('Scroll Handler', () => {
  let window;
  let document;

  beforeEach(() => {
    window = new Window();
    document = window.document;
    globalThis.document = document;
    globalThis.window = window;

    document.body.innerHTML = `
      <nav class="navbar">Navigation</nav>
      <main>Content</main>
    `;
  });

  afterEach(() => {
    window.close();
  });

  test('adds scrolled class when page is scrolled', async () => {
    const { initScrollHandler } = await import('../../assets/js/scroll.js');
    initScrollHandler();

    // Simulate scroll
    Object.defineProperty(window, 'scrollY', { value: 100, writable: true });
    window.dispatchEvent(new window.Event('scroll'));

    const navbar = document.querySelector('.navbar');
    expect(navbar.classList.contains('scrolled')).toBe(true);
  });
});
```

### Strategy 4: Mocking Fetch and Network Calls

```javascript
// tests/js/search.test.js
import { describe, test, expect, beforeEach, afterEach, mock } from 'bun:test';
import { Window } from 'happy-dom';

describe('Search', () => {
  let window;
  let originalFetch;

  beforeEach(() => {
    window = new Window();
    globalThis.document = window.document;
    globalThis.window = window;

    // Mock fetch
    originalFetch = globalThis.fetch;
    globalThis.fetch = mock(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([
          { title: 'First Post', url: '/posts/first/' },
          { title: 'Second Post', url: '/posts/second/' }
        ])
      })
    );
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    window.close();
  });

  test('fetches and displays search results', async () => {
    const { performSearch } = await import('../../assets/js/search.js');

    const results = await performSearch('post');

    expect(fetch).toHaveBeenCalledWith('/index.json');
    expect(results).toHaveLength(2);
    expect(results[0].title).toBe('First Post');
  });
});
```

## Running Tests

### Command Reference

```bash
# Run all tests (using package.json script - PREFERRED)
bun run test

# Run all tests directly
bun test

# Run specific test file
bun test tests/js/theme.test.js

# Run tests matching pattern
bun test --test-name-pattern "theme"

# Watch mode - re-runs on file changes
bun test --watch

# Coverage report
bun test --coverage

# Bail on first failure
bun test --bail

# Run tests in specific directory
bun test tests/js/
```

### CI/CD Integration

For GitHub Actions or similar CI systems:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run test
```

## Best Practices

### 1. Separate Pure Logic from DOM Code

Extract testable pure functions from DOM-manipulating code. This makes testing easier and code more maintainable.

### 2. Clean Up After Each Test

Always clean up global state and close happy-dom windows in `afterEach` to prevent test pollution.

### 3. Use Dynamic Imports for Module Isolation

Use `await import()` inside tests to ensure fresh module state and proper global setup timing.

### 4. Test Behavior, Not Implementation

Focus on what the code does (theme changes, elements appear) rather than how it does it internally.

### 5. Prefer bun run test Over bun test

Using the package.json script ensures consistent configuration and makes it easier to add options later.

## Troubleshooting

### "document is not defined"

Ensure happy-dom is set up before importing the module under test. Use dynamic imports or set up globals in a `beforeEach` block.

### Tests Pass Individually but Fail Together

Add proper cleanup in `afterEach` to reset global state between tests.

### Async Event Handler Issues

Use `window.happyDOM.waitUntilComplete()` or explicit promises when testing async DOM operations.
