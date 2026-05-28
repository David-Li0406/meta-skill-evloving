# Package.json Reference - Selection Guide

This directory contains multiple package.json reference files based on different testing and state management configurations.

## Available References

### 1. jest-vuex.md (Default/Legacy)
- **Testing**: Jest 30.x
- **State Management**: Vuex 4.x
- **Use When**: Using traditional Vuex store with Jest testing
- **Config Files**: `jest.config.cjs`
- **Store Location**: `src/store/`

### 2. vitest-pinia.md (Modern/Recommended)
- **Testing**: Vitest 4.x
- **State Management**: Pinia 3.x
- **Use When**: Building new applications with modern tooling
- **Config Files**: `vitest.config.ts`
- **Store Location**: `src/stores/`
- **Benefits**: Faster tests, no Babel needed, better TypeScript support

### 3. jest-pinia.md
- **Testing**: Jest 30.x
- **State Management**: Pinia 3.x
- **Use When**: Migrating to Pinia but keeping Jest infrastructure
- **Config Files**: `jest.config.cjs`
- **Store Location**: `src/stores/`

### 4. vitest-vuex.md
- **Testing**: Vitest 4.x
- **State Management**: Vuex 4.x
- **Use When**: Migrating to Vitest but keeping existing Vuex stores
- **Config Files**: `vitest.config.ts`
- **Store Location**: `src/store/`

## Selection Matrix

| Testing Framework | State Management | Reference File     | Recommended For              |
|-------------------|------------------|--------------------|------------------------------|
| Jest              | Vuex             | jest-vuex.md       | Legacy applications          |
| Jest              | Pinia            | jest-pinia.md      | Pinia migration with Jest    |
| Vitest            | Vuex             | vitest-vuex.md     | Vitest migration with Vuex   |
| Vitest            | Pinia            | vitest-pinia.md    | New applications (Recommended)|

## How to Use

The agent should:
1. Ask the user questions 7 and 8 from copilot-instructions.md
2. Based on the answers, select the appropriate reference file:
   - `test_framework = "jest"` AND `state_management = "vuex"` → use `jest-vuex.md`
   - `test_framework = "jest"` AND `state_management = "pinia"` → use `jest-pinia.md`
   - `test_framework = "vitest"` AND `state_management = "vuex"` → use `vitest-vuex.md`
   - `test_framework = "vitest"` AND `state_management = "pinia"` → use `vitest-pinia.md`
3. Generate package.json using the selected reference

## Key Differences

### Testing Framework Differences

**Jest:**
- Requires Babel configuration
- Uses `jest.config.cjs`
- Test scripts: `jest`, `jest --watch`
- Slower execution
- Mature ecosystem

**Vitest:**
- No Babel needed (native ESM)
- Uses `vitest.config.ts`
- Test scripts: `vitest run`, `vitest`, `vitest --ui`
- Faster execution
- Better Vite integration

### State Management Differences

**Vuex:**
- Mutations + Actions pattern
- Store located in `src/store/`
- Module-based architecture
- `src/store/modules/`

**Pinia:**
- Direct state mutation
- Stores located in `src/stores/`
- Composition API style
- Better TypeScript inference
- Smaller bundle size
- `@pinia/testing` for test helpers

## Version Information

All references use the latest stable versions as of December 2024:
- Vue: `^3.5.13` (placeholder: `{{vue_version}}`)
- Vite: `^6.3.5` (placeholder: `{{vite_version}}`)
- TypeScript: `4.9` (placeholder: `{{typescript_version}}`)
- Jest: `^30.2.0`
- Vitest: `^4.0.15`
- Vuex: `^4.1.0`
- Pinia: `^3.0.4`
