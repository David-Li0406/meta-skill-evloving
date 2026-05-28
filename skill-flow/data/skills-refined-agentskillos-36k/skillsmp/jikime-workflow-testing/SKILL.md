---
name: jikime-workflow-testing
description: Comprehensive development workflow specialist combining DDD, debugging, performance optimization, code review, PR review, and quality assurance into unified development workflows
version: 1.0.0
tags: ["workflow", "testing", "quality", "coverage", "vitest", "playwright"]
triggers:
  keywords: ["test", "testing", "coverage", "vitest", "playwright", "jest", "테스트", "QA"]
  phases: ["run", "sync"]
  agents: ["test-guide", "manager-quality"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Testing Workflow for Next.js

Next.js/TypeScript 프로젝트를 위한 간결하고 실용적인 테스팅 가이드.

## Quick Reference

### Tech Stack

| 용도 | 도구 | 설명 |
|------|------|------|
| Unit/Integration | **Vitest** | 빠른 실행, ESM 지원, Jest 호환 |
| Component | **React Testing Library** | 사용자 관점 테스팅 |
| E2E | **Playwright** | 크로스 브라우저 자동화 |
| Coverage | **v8** | Vitest 내장 커버리지 |

### Testing Pyramid

```
        /   E2E   \        10% - Critical User Flows
       / Integration\      20% - API, DB 연동
      /    Unit      \     70% - Business Logic
```

### Commands

```bash
# Unit/Integration Tests
npm run test              # Watch 모드
npm run test:run          # 단일 실행
npm run test:coverage     # 커버리지 리포트

# E2E Tests
npm run test:e2e          # Playwright 실행
npm run test:e2e:ui       # UI 모드
```

---

## Setup Guide

### 1. Vitest 설치

```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
```

### 2. vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', '**/*.d.ts', '**/*.config.*'],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
  },
  resolve: {
    alias: {
      '~': path.resolve(__dirname, './src'),
    },
  },
});
```

### 3. vitest.setup.ts

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

### 4. package.json scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

---

## Test Patterns

### Unit Test (Function)

```typescript
// utils/format.test.ts
import { describe, it, expect } from 'vitest';
import { formatPrice } from './format';

describe('formatPrice', () => {
  it('formats number with currency symbol', () => {
    expect(formatPrice(1000)).toBe('$1,000');
  });

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('$0');
  });

  it('handles negative numbers', () => {
    expect(formatPrice(-500)).toBe('-$500');
  });
});
```

### Component Test

```typescript
// components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('is disabled when loading', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Hook Test

```typescript
// hooks/useCounter.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(6);
  });
});
```

### API Route Test

```typescript
// app/api/users/route.test.ts
import { describe, it, expect, vi } from 'vitest';
import { GET, POST } from './route';
import { NextRequest } from 'next/server';

describe('Users API', () => {
  it('GET returns users list', async () => {
    const request = new NextRequest('http://localhost/api/users');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(Array.isArray(data.users)).toBe(true);
  });

  it('POST creates new user', async () => {
    const request = new NextRequest('http://localhost/api/users', {
      method: 'POST',
      body: JSON.stringify({ name: 'John', email: 'john@example.com' }),
    });

    const response = await POST(request);
    expect(response.status).toBe(201);
  });
});
```

---

## Quality Gates

### Coverage Thresholds

| 레벨 | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| Minimum | 70% | 70% | 70% | 70% |
| **Target** | **80%** | **80%** | **80%** | **80%** |
| Excellent | 90%+ | 90%+ | 90%+ | 90%+ |

### PR Merge Checklist

```markdown
## Before Merge
- [ ] All tests pass (`npm run test:run`)
- [ ] Coverage meets threshold (`npm run test:coverage`)
- [ ] E2E tests pass (`npm run test:e2e`)
- [ ] No console errors in tests
- [ ] New features have tests
```

### CI Integration (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run test:run
      - run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: npm run test:e2e

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Modules

상세 가이드는 modules 디렉토리 참조:

- **vitest.md**: Unit/Integration 테스팅 상세 패턴
- **playwright.md**: E2E 테스팅 상세 패턴
- **quality-gates.md**: 품질 검증 체크리스트

---

## Works Well With

- `jikime-lang-typescript`: TypeScript 패턴
- `jikime-library-zod`: 스키마 검증 테스팅
- `jikime-workflow-tdd`: TDD 사이클

---

Last Updated: 2026-01-21
Version: 3.0.0 (Simplified for Next.js)
