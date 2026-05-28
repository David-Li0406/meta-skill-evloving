---
name: unified-development-workflow-testing
description: Use this skill for comprehensive development lifecycle management, integrating testing, debugging, performance optimization, code review, and quality assurance into unified workflows.
---

# Unified Development Workflow Testing

This skill provides a comprehensive guide for managing the development lifecycle, focusing on testing, debugging, performance optimization, code review, and quality assurance.

## Quick Reference

### Core Capabilities

- **Test-Driven Development (TDD)**: Implement the RED-GREEN-REFACTOR cycle with best practice patterns.
- **AI-Powered Debugging**: Intelligent error analysis and solution recommendations.
- **Performance Optimization**: Profiling and bottleneck detection guidance.
- **Automated Code Review**: Quality analysis using the TRUST 5 validation framework.
- **Quality Assurance**: Comprehensive testing and CI/CD integration patterns.
- **Workflow Orchestration**: End-to-end development process guidance.

### Tech Stack

| Purpose | Tool | Description |
|---------|------|-------------|
| Unit/Integration | **Vitest** | Fast execution, ESM support, Jest compatible |
| Component | **React Testing Library** | User-centric testing |
| E2E | **Playwright** | Cross-browser automation |
| Coverage | **v8** | Built-in coverage for Vitest |

### Testing Pyramid

```
        /   E2E   \        10% - Critical User Flows
       / Integration\      20% - API, DB integration
      /    Unit      \     70% - Business Logic
```

### Commands

```bash
# Unit/Integration Tests
npm run test              # Watch mode
npm run test:run          # Single run
npm run test:coverage     # Coverage report

# E2E Tests
npm run test:e2e          # Playwright execution
npm run test:e2e:ui       # UI mode
```

## Implementation Guide

### Setup Guide

1. **Install Vitest and Dependencies**:
   ```bash
   npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
   ```

2. **Configure vitest.config.ts**:
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

3. **Setup vitest.setup.ts**:
   ```typescript
   import '@testing-library/jest-dom/vitest';
   import { cleanup } from '@testing-library/react';
   import { afterEach } from 'vitest';

   afterEach(() => {
     cleanup();
   });
   ```

4. **Configure package.json scripts**:
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

### Quality Gates

#### Coverage Thresholds

| Level | Statements | Branches | Functions | Lines |
|-------|------------|----------|-----------|-------|
| Minimum | 70% | 70% | 70% | 70% |
| **Target** | **80%** | **80%** | **80%** | **80%** |
| Excellent | 90%+ | 90%+ | 90%+ | 90%+ |

#### PR Merge Checklist

```markdown
## Before Merge
- [ ] All tests pass (`npm run test:run`)
- [ ] Coverage meets threshold (`npm run test:coverage`)
- [ ] E2E tests pass (`npm run test:e2e`)
- [ ] No console errors in tests
- [ ] New features have tests
```

### Workflow Integration Patterns

#### CI/CD Integration

Integrate with CI/CD pipelines through a multi-stage validation process:

1. **Code Quality Validation**: Run automated code review and verify results meet quality standards.
2. **Testing Validation**: Execute the full test suite including unit, integration, and end-to-end tests.
3. **Performance Validation**: Run performance tests and compare results against defined thresholds.
4. **Security Validation**: Execute security analysis including static analysis and dependency scanning.

### Common Use Cases

- **Enterprise Development Workflow**: Integrate quality gates at each stage for enterprise applications.
- **Performance-Critical Applications**: Emphasize profiling and optimization stages for performance-sensitive systems.
- **Automated Testing and CI/CD Integration**: Streamline testing and deployment processes.

---

## Works Well With

- `jikime-lang-typescript`: TypeScript patterns
- `jikime-library-zod`: Schema validation testing
- `moai-domain-backend`: Backend development workflows
- `moai-domain-frontend`: Frontend development workflows

---

Last Updated: 2026-01-21
Version: 3.0.0