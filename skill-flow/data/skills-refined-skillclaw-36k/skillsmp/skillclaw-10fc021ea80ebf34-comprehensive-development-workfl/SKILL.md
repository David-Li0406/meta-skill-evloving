---
name: comprehensive-development-workflow
description: Use this skill when you need to manage the complete development lifecycle, integrating testing, debugging, performance optimization, code review, and quality assurance into a unified workflow.
---

# Skill body

## Overview

This skill provides a comprehensive approach to managing the development lifecycle, combining Test-Driven Development (TDD), debugging, performance optimization, code review, and quality assurance into integrated workflows.

## Core Capabilities

- **Test-Driven Development (TDD)**: Follow the RED-GREEN-REFACTOR cycle with best practice patterns.
- **Debugging**: Utilize intelligent error analysis and solution recommendations.
- **Performance Optimization**: Get guidance on profiling and detecting bottlenecks.
- **Automated Code Review**: Implement a validation framework for quality analysis.
- **Pull Request (PR) Review**: Use a multi-agent pattern for thorough code review.
- **Quality Assurance**: Integrate comprehensive testing and CI/CD patterns.
- **Workflow Orchestration**: Navigate through the development process with clear stages.

## Workflow Stages

1. **Debug**: Identify and resolve issues in the code.
2. **Refactor**: Improve the code structure without changing its behavior.
3. **Optimize**: Enhance performance and efficiency.
4. **Review**: Conduct thorough code reviews.
5. **Test**: Execute tests to ensure code quality.
6. **Profile**: Analyze performance metrics.

## Setup Guide

### 1. Install Required Tools

```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
```

### 2. Configure Testing Environment

Create a `vitest.config.ts` file with the following content:

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

### 3. Setup Testing Environment

Create a `vitest.setup.ts` file with the following content:

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';

// Additional setup can be added here
```

## Commands

### Running Tests

- **Unit/Integration Tests**: 
  ```bash
  npm run test              # Watch mode
  npm run test:run          # Single run
  npm run test:coverage     # Coverage report
  ```

- **E2E Tests**: 
  ```bash
  npm run test:e2e          # Playwright execution
  npm run test:e2e:ui       # UI mode
  ```

## When to Use

- For complete development lifecycle management.
- In enterprise-grade quality assurance implementations.
- For multi-language development projects.
- When working on performance-critical applications.
- To reduce technical debt through automated testing and CI/CD integration.
- For automating pull request code reviews.