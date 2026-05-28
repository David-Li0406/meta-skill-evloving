---
name: cli-tools
description: "WHAT: Yarn scripts for React Native monorepo development. WHEN: running dev builds, testing, linting, code generation. KEYWORDS: yarn, dev:ios, dev:android, test, lint, typecheck, generate, turbo, build, clean."
---

# CLI Tools

## Core Principles

**Always use yarn scripts, never run tools directly.** Run `yarn dev:ios` not `npx react-native run-ios`. Yarn scripts include necessary environment variables, flags, and configurations. Direct tool invocation skips project-specific setup.

**Always use yarn, never npm.** The project uses Yarn 4.5.0 with workspace configuration. Running `npm install` or `npm run` breaks workspace resolution and dependency management.

**Always check package.json or this document for exact script names.** Don't assume conventions. The project uses `yarn dev:ios` not `yarn ios`. Custom naming prevents conflicts with React Native CLI.

**Always use code generation scripts for scaffolding.** Run `yarn generate:module` for modules, `yarn graphql:generate` for GraphQL types. Plop templates follow project conventions for file structure and naming.

**Why**: Consistent CLI usage ensures reproducible builds, prevents environment-specific issues, automates complex setup sequences, and maintains code quality through pre-commit hooks.

## When to Use This Skill

Use these commands when:

- Running the app locally on iOS or Android
- Building the library for distribution
- Running tests with Jest
- Linting code with ESLint
- Type checking with TypeScript
- Generating new modules or components
- Scaffolding GraphQL types from schema
- Cleaning build artifacts
- Setting up development environment
- Running accessibility checks
- Opening Xcode or Android Studio
- Managing git hooks with Husky
- Orchestrating monorepo builds with Turbo

## Development Commands

### Running the App

Start Metro bundler and run app on iOS or Android.

```bash
# Start Metro bundler (terminal 1)
yarn start

# Run iOS app (terminal 2)
yarn dev:ios

# Run Android app (terminal 2)
yarn dev:android
```

**What dev:ios and dev:android do:**
1. Prompt for local path to YourCompany iOS/Android repositories (cached in `.env.local_dev_paths`)
2. **iOS**: Build debug XCFramework if needed, symlink to local iOS repo, run metro bundler
3. **Android**: Configure AAR symlink to local Android repo, run metro bundler
4. Enable live development with local changes reflected in consumer apps

**Why**: These commands handle environment configuration, native builds, and symlink setup automatically. Live development without publishing to npm or Maven.

### Shell App

Test modules in isolation using the shell app.

```bash
# Run shell app on iOS
yarn app ios

# Run shell app on Android
yarn app android

# Generic command syntax
yarn app <command>
```

**Why**: The shell app (`app/*` workspace) allows developing modules without full YourCompany consumer apps. Faster iteration for module development.

### Building

Compile library for distribution with TypeScript definitions.

```bash
# Build library (CommonJS, ES modules, TypeScript definitions)
yarn build

# Type checking without emitting files
yarn typecheck
```

**Why**: `yarn build` uses react-native-builder-bob with correct configuration for multiple module formats. `yarn typecheck` runs TypeScript compiler with project-specific tsconfig.

## Code Quality

### Linting

Run ESLint with accessibility checks.

```bash
# Run ESLint on all source files
yarn lint

# Accessibility baseline checks (runs on staged files)
yarn a11y:check

# Accessibility check with verbose output
yarn a11y:check:verbose

# Check all files for accessibility issues
yarn a11y:check:all

# Generate new accessibility baseline
yarn a11y:baseline:gen

# Update existing accessibility baseline
yarn a11y:baseline:update

# Generate accessibility report
yarn a11y:report
```

**Why**: `yarn lint` includes custom ESLint rules and React Native plugins. Accessibility commands track baseline and flag regressions. Pre-commit hooks run these automatically.

### Testing

Run Jest tests with React Native preset.

```bash
# Run all tests
yarn test

# Run specific test file
yarn jest <path-to-test>

# Run tests in watch mode
yarn jest --watch

# Run tests with coverage
yarn jest --coverage

# Update snapshots
yarn jest -u
```

**Why**: `yarn test` runs with project-specific Jest configuration, React Native transformers, and module resolution. Direct `jest` usage provides more control for debugging.

### Maestro E2E Tests

Run end-to-end tests on iOS simulator or Android emulator.

```bash
# Run Maestro tests on iOS simulator
./scripts/maestro-test.sh ios

# Run Maestro tests on Android emulator
./scripts/maestro-test.sh android

# Run specific test directory
./scripts/maestro-test.sh ios ./MaestroTests/onboarding/
```

**Why**: Maestro tests validate complete user journeys on actual devices/simulators. Script automatically detects running emulators and executes YAML test flows.

## Code Generation

### Module Scaffolding

Generate modules and components with Plop templates.

```bash
# Generate new module (follows project conventions)
yarn generate:module

# Extend existing module
yarn extend:module

# Generate brand assets
yarn generate:brand-assets
```

**Why**: Plop templates follow project conventions for file structure, naming, and boilerplate. Consistent module organization across features.

### Data Layer

Generate types and code from schemas.

```bash
# Generate GraphQL types and operations
yarn graphql:generate

# Generate native data access layer
yarn generate:data-access:native

# Generate Swift types from TypeScript
yarn generate:swift-types
```

**Why**: Code generation ensures type safety between TypeScript, GraphQL schemas, and native Swift code. Prevents runtime type errors.

## Platform-Specific Commands

### iOS

Manage iOS dependencies and build artifacts.

```bash
# Install iOS dependencies (CocoaPods)
yarn install:ios

# Clean iOS build artifacts
yarn clean:ios

# Open Xcode workspace
yarn open:xcode
```

**Why**: These scripts handle CocoaPods installation and Xcode workspace management. `clean:ios` removes derived data and build caches.

### Android

Manage Android build artifacts and tools.

```bash
# Clean Android build artifacts and Gradle caches
yarn clean:android

# Open Android Studio
yarn open:androidstudio
```

**Why**: `clean:android` runs Gradle tasks that properly clear all build caches. Opens Android Studio with correct project structure.

## Building Native Artifacts

### iOS XCFramework

Build React Shared Modules as XCFramework for iOS.

```bash
# Build for both device and simulator (for distribution)
./scripts/build_spm_frameworks.sh --target both

# Build for device only
./scripts/build_spm_frameworks.sh --target device

# Build for simulator only (for local testing)
./scripts/build_spm_frameworks.sh --target simulator
```

**Why**: XCFramework consumed by YourCompany iOS app via Swift Package Manager. Simulator-only builds are faster for local iteration.

### Android AAR

Build Android Archive for YourCompany Android app.

```bash
# Build AAR locally
cd app/android && ./gradlew :modules:bundleReleaseAar

# Publish to local Maven repository
cd app/android && ./gradlew :modules:publishToMavenLocal
```

**Why**: AAR contains compiled code, resources, and JavaScript bundle. Publishing to local Maven allows testing AAR changes before release.

## Environment Setup

Configure development environment and git hooks.

```bash
# Set up development environment
yarn setup:env

# Install git hooks (runs automatically after install)
yarn prepare
```

**Why**: `setup:env` configures environment variables and dependencies. `prepare` installs Husky git hooks for pre-commit checks (lint-staged, a11y).

## Localization

Manage translation files and synchronization.

```bash
# Run localization helper utilities
yarn localization:helpers
```

**Why**: Manages translation file validation and synchronization with Lokalise translation management system.

## Developer Tools

Open toolbox UI for common development tasks.

```bash
# Open toolbox UI (new version)
yarn toolbox

# Open toolbox UI (deprecated version)
yarn toolbox:deprecated
```

**Why**: Toolbox provides UI for feature flag management, environment switching, and other development utilities.

## Workspace Commands

Run commands in specific workspaces within monorepo.

```bash
# Run command in app workspace
yarn app <command>

# Run command in specific workspace
yarn workspace @repo/toolbox <command>
```

**Why**: Yarn workspaces enable monorepo management. Workspace commands ensure dependencies and scripts run in correct package context.

## Pre-Commit Hooks

### lint-staged

Runs automatically on `git commit` via Husky. Manually run:

```bash
# Run lint-staged on staged files
yarn lint-staged
```

**Checks on staged files:**
- **TypeScript/TSX files** (`.ts`, `.tsx`):
  - ESLint with auto-fix (`--fix`)
  - Prettier formatting
  - Accessibility baseline check (non-test files in `src/`)

- **JavaScript files** (`.js`):
  - ESLint with auto-fix
  - Prettier formatting

- **JSON, Markdown, YAML files**:
  - Prettier formatting

- **Team governance files** (`.teams/*.json`, `**/.claim.json`):
  - JSON schema validation with ajv
  - Claims validation check

**Why**: Lint-staged ensures only valid, formatted code is committed. Faster than running checks on all files (only processes staged changes).

### Prettier

Format code with Prettier.

```bash
# Format specific files
yarn prettier --write <file>

# Check formatting without fixing
yarn prettier --check <file>

# Format all files (use with caution)
yarn prettier --write .
```

**Why**: Direct prettier invocation for formatting files outside git workflows. Prefer lint-staged for pre-commit formatting.

### ESLint

Lint code with ESLint.

```bash
# Lint specific files with auto-fix
yarn eslint <file> --fix

# Lint without a11y checks (matches lint-staged behavior)
ESLINT_DISABLE_A11Y=1 yarn eslint <file> --fix
```

**Why**: Direct ESLint usage for debugging linting issues. Use `yarn lint` for full project lint run.

## Monorepo Orchestration

### Turbo

Run scripts across workspaces with caching.

```bash
# Run turbo commands across workspaces
yarn turbo run <script-name>

# Examples
yarn turbo run build
yarn turbo run lint
yarn turbo run check-types
```

**Why**: Turbo 2.5.6 orchestrates script execution across monorepo. Creates dependency graph, runs scripts in parallel, caches results to avoid redundant work.

**Note**: Turbo expects consistent script names across packages (`build`, `lint`, `check-types`, `dev`).

### Husky

Manage git hooks.

```bash
# Manually reinstall git hooks
yarn husky install

# Test pre-commit hook manually
yarn husky run pre-commit
```

**Why**: Husky 9.1.7 manages git hooks. Hooks install automatically via `yarn prepare` but can be manually reinstalled if needed.

## TypeScript Compiler

Type check and build type definitions.

```bash
# Type check without emitting files (use yarn typecheck instead)
yarn tsc --noEmit

# Build type definitions
yarn tsc --project tsconfig.build.json
```

**Why**: Direct `tsc` usage rarely needed since `yarn typecheck` and `yarn build` handle this. Useful for debugging type errors with specific compiler flags.

## Common Mistakes to Avoid

❌ **Don't run underlying tools directly**:

```bash
# ❌ Wrong - missing environment config
npx react-native run-ios
./gradlew clean
eslint src
jest
```

**Why**: Direct tool invocation skips project-specific environment variables, flags, and configurations. May work differently on different machines.

✅ **Do use yarn scripts**:

```bash
# ✅ Correct - includes all necessary config
yarn dev:ios
yarn clean:android
yarn lint
yarn test
```

**Why**: Yarn scripts abstract complex command sequences, handle environment setup, and ensure consistent behavior across team.

❌ **Don't use npm commands**:

```bash
# ❌ Wrong - breaks workspace resolution
npm run test
npm install
npm run dev:ios
```

**Why**: Project uses Yarn 4.5.0 with workspace configuration and custom resolutions. npm breaks workspace dependency management.

✅ **Do use yarn commands**:

```bash
# ✅ Correct - uses Yarn workspace resolution
yarn test
yarn install
yarn dev:ios
```

**Why**: Yarn 4.5.0 manages monorepo with workspace dependencies. Consistent package manager across team.

❌ **Don't assume standard script names**:

```bash
# ❌ Wrong - these scripts don't exist
yarn ios
yarn android
yarn run
```

**Why**: Project uses custom naming conventions. Script names may differ from common React Native conventions.

✅ **Do check package.json for exact names**:

```bash
# ✅ Correct - use actual script names
yarn dev:ios
yarn dev:android
yarn start
```

**Why**: Custom naming prevents conflicts with React Native CLI. Check `package.json` or this document for exact script names.

❌ **Don't manually create modules**:

```bash
# ❌ Wrong - manual file creation
mkdir src/modules/new-feature
touch src/modules/new-feature/index.ts
```

**Why**: Manual creation skips project conventions for file structure, naming, and boilerplate.

✅ **Do use code generation scripts**:

```bash
# ✅ Correct - uses Plop templates
yarn generate:module

# Follow prompts for module name, type, etc.
```

**Why**: Plop templates follow project conventions automatically. Consistent module organization, imports, exports, and tests.

## Quick Reference

**Development:**
- `yarn start` - Start Metro bundler
- `yarn dev:ios` - Run iOS app with local symlinks
- `yarn dev:android` - Run Android app with local symlinks
- `yarn app <command>` - Run shell app commands

**Building:**
- `yarn build` - Compile library for distribution
- `yarn typecheck` - Type check without emitting

**Code Quality:**
- `yarn lint` - Run ESLint
- `yarn a11y:check` - Accessibility baseline check
- `yarn test` - Run Jest tests

**Code Generation:**
- `yarn generate:module` - Scaffold new module
- `yarn graphql:generate` - Generate GraphQL types
- `yarn generate:swift-types` - Generate Swift types

**Platform:**
- `yarn install:ios` - Install CocoaPods
- `yarn clean:ios` - Clean iOS artifacts
- `yarn clean:android` - Clean Android artifacts
- `yarn open:xcode` - Open Xcode workspace
- `yarn open:androidstudio` - Open Android Studio

**Native Builds:**
- `./scripts/build_spm_frameworks.sh --target simulator` - Build iOS XCFramework
- `cd app/android && ./gradlew :modules:bundleReleaseAar` - Build Android AAR

**Setup:**
- `yarn setup:env` - Configure environment
- `yarn prepare` - Install git hooks

**Utilities:**
- `yarn localization:helpers` - Translation utilities
- `yarn toolbox` - Developer toolbox UI

**Monorepo:**
- `yarn turbo run <script>` - Run across workspaces
- `yarn workspace <name> <command>` - Run in specific workspace

**Pre-Commit:**
- `yarn lint-staged` - Run pre-commit checks
- `yarn prettier --write <file>` - Format code
- `yarn eslint <file> --fix` - Lint and fix

**Testing:**
- `yarn jest <path>` - Run specific test
- `yarn jest --watch` - Watch mode
- `yarn jest --coverage` - Coverage report
- `./scripts/maestro-test.sh ios` - E2E tests

**Never use:**
- ❌ `npm install` - Use `yarn install`
- ❌ `npm run <script>` - Use `yarn <script>`
- ❌ `npx react-native run-ios` - Use `yarn dev:ios`
- ❌ `./gradlew clean` - Use `yarn clean:android`

**Full CLI reference**: `previous-standards/global/cli-tools.md`
