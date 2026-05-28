---
name: testing
description: Generates test files and testing utilities for Vue 3 applications. Ensures mandatory .spec.ts files are created alongside components, views, stores, directives, and utilities.
---

# Testing Skill

## Purpose
Generate test files and testing utilities for Vue 3 applications with proper coverage and best practices.

## Test File Generation Rules

**IMPORTANT**: Test files MUST be generated alongside UI components, views, stores, directives, and utilities.

When generating any of the following, **ALWAYS create a corresponding test file**:
- **Vue Components** (`src/components/**/*.vue`) → `{ComponentName}.spec.ts` in same directory
- **Views** (`src/views/**/*.vue`) → `{ViewName}.spec.ts` in same directory
- **Store Modules** (Vuex: `src/store/modules/*.ts`, Pinia: `src/stores/*.ts`) → `{moduleName}.spec.ts` in same directory
- **Directives** (`src/directives/*.ts`) → `{directiveName}.spec.ts` in same directory
- **Utilities** (`src/shared/utils/*.ts`) → `{utilityName}.spec.ts` in same directory
- **Mixins** (`src/shared/mixins/*.ts`) → `{mixinName}.spec.ts` in same directory
- **Services** (`src/services/*.ts`) → **OPTIONAL** - typically mocked in component tests

## Test File Location
- Test files live **co-located** with their source files (not in separate `tests/` directory)
- Naming convention: `{filename}.spec.ts` (use `.spec.ts` consistently)

## Testing Frameworks

### Jest Testing (if test_framework: jest)
- Use Jest with Vue Test Utils (`@vue/test-utils`) for component testing
- Use `@vue/vue3-jest` transformer for `.vue` files
- Use `ts-jest` for TypeScript files
- Mock external dependencies (axios, router, store)
- Target >80% coverage for services and stores
- Target >70% coverage for components
- Test file naming: `{filename}.spec.ts`
- Configuration: `jest.config.cjs` (handled by jest-config skill)

### Vitest Testing (if test_framework: vitest)
- Use Vitest with Vue Test Utils for component testing
- Native ESM support with faster execution
- Use `@vitest/ui` for interactive test UI
- Mock external dependencies (axios, router, store)
- Target >80% coverage for services and stores
- Target >70% coverage for components
- Test file naming: `{filename}.spec.ts` or `{filename}.test.ts`
- Configuration: `vitest.config.ts` (handled by vitest-config skill)

## Test Coverage Requirements

- **Components**: >70% coverage (focus on user interactions, computed properties, methods)
- **Views**: >70% coverage (lifecycle, navigation, major workflows)
- **Stores**: >80% coverage (state mutations, actions, getters)
- **Utilities**: >80% coverage (all functions and edge cases)
- **Directives**: >70% coverage (behavior and DOM manipulation)

## Test Organization Best Practices

1. **Describe blocks**: Group related tests logically
   - Component/View name as top-level describe
   - Group by: lifecycle hooks, computed properties, methods, events
2. **Test naming**: Use descriptive test names that explain expected behavior
3. **AAA Pattern**: Arrange, Act, Assert in each test
4. **Mocking**: Mock external dependencies (API calls, router, store)
5. **Cleanup**: Use `afterEach` to clear mocks and reset state
6. **Isolation**: Each test should be independent and not rely on others

## Example Files
See: `examples.md` in this directory for complete test templates:
- Component tests (Options API)
- Component tests (Composition API)
- View tests
- Store tests (Vuex)
- Store tests (Pinia)

## Notes
- Test templates vary based on `vue_api_pattern` (composition-api vs options-api)
- Test templates vary based on `state_management` (pinia vs vuex)
- All test files should use the same testing framework specified in configuration
- Co-location of tests with source files improves maintainability
