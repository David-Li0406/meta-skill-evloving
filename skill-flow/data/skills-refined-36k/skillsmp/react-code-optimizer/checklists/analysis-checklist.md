# React Code Optimization Analysis Checklist

Use this checklist when analyzing a React project for optimization opportunities.

## 📋 Pre-Analysis Setup

- [ ] Identify project root directory
- [ ] Locate `package.json`
- [ ] Identify main source directory (usually `src/`)
- [ ] Note React version and other key dependencies
- [ ] Check if TypeScript is used

## 🔍 Project Structure Analysis

### File Discovery
- [ ] List all `.tsx` and `.ts` files
- [ ] Count total number of components
- [ ] Identify directory structure pattern
- [ ] Find configuration files (eslint, tsconfig, etc.)

### Size Analysis
- [ ] Identify files >500 lines (flag for potential splitting)
- [ ] Identify files >1000 lines (high priority for splitting)
- [ ] Identify files >2000 lines (critical - must split)
- [ ] Calculate average component size

## ⚡ Performance Analysis

### React.memo Usage
- [ ] Search for `React.memo` usage across project
- [ ] Identify components that should use React.memo:
  - Components with expensive render logic
  - Components receiving stable props
  - List components (e.g., rendering 50+ items)
  - Components in frequently updated contexts

### Hook Optimization
- [ ] Check `useCallback` usage for event handlers
- [ ] Check `useMemo` usage for computed values
- [ ] Identify missing `useCallback` on event handlers
- [ ] Identify missing `useMemo` on expensive calculations
- [ ] Review dependency arrays for correctness

### Context Performance
- [ ] Locate all Context providers
- [ ] Check if Context value is properly memoized
- [ ] Count dependencies in Context value useMemo
- [ ] Identify if Context triggers too many re-renders
- [ ] Consider if Context should be split

### Re-render Analysis
- [ ] Search for inline object creation in render (e.g., `style={{}}`)
- [ ] Search for inline array creation
- [ ] Search for inline function creation (not in useCallback)
- [ ] Check for proper `key` usage in lists

### Code Splitting
- [ ] Check for `React.lazy` usage
- [ ] Identify large components that could be lazy-loaded
- [ ] Check for route-based code splitting
- [ ] Identify heavy dependencies that could be lazy-loaded

## 🏗️ Architecture Analysis

### State Management
- [ ] Identify state management approach (Context, Redux, Zustand, etc.)
- [ ] Check for proper state organization
- [ ] Identify unnecessary global state
- [ ] Check for proper state updates (immutability)

### Side Effects
- [ ] Review all `useEffect` hooks
- [ ] Check for proper cleanup functions
- [ ] Verify dependency arrays are correct
- [ ] Identify potential infinite loops
- [ ] Check for race conditions in async effects

### Data Fetching
- [ ] Identify data fetching patterns
- [ ] Check for loading states
- [ ] Check for error handling
- [ ] Identify duplicate API calls
- [ ] Check for proper caching

### Event Handling
- [ ] Check if event handlers are properly memoized
- [ ] Identify event listener memory leaks
- [ ] Check for proper event delegation
- [ ] Verify cleanup of global event listeners

## 📝 Code Quality Analysis

### Component Organization
- [ ] Check if components follow Single Responsibility Principle
- [ ] Identify components doing too much
- [ ] Check for proper component composition
- [ ] Identify opportunities to extract reusable components

### Code Duplication
- [ ] Identify repeated code blocks
- [ ] Identify similar patterns across components
- [ ] Check for opportunities to create custom hooks
- [ ] Check for opportunities to create utility functions

### Type Safety (TypeScript)
- [ ] Search for `any` types
- [ ] Search for `@ts-ignore` comments
- [ ] Check if props have proper types/interfaces
- [ ] Verify return types on functions
- [ ] Check for proper null/undefined handling

### Error Handling
- [ ] Check for Error Boundaries
- [ ] Verify try-catch in async operations
- [ ] Check for proper error messages
- [ ] Identify silent failures

## 🎨 Code Style & Patterns

### Import Organization
- [ ] Check for unused imports
- [ ] Check for circular dependencies
- [ ] Verify consistent import ordering
- [ ] Check for relative vs absolute imports consistency

### Naming Conventions
- [ ] Verify consistent component naming (PascalCase)
- [ ] Verify consistent hook naming (use prefix)
- [ ] Verify consistent file naming
- [ ] Check for meaningful variable names

### File Organization
- [ ] Check if related files are grouped
- [ ] Verify consistent folder structure
- [ ] Check for proper separation of concerns
- [ ] Identify files in wrong locations

## 🛠️ Tooling & Configuration

### ESLint
- [ ] Check if ESLint is configured
- [ ] Review ESLint rules
- [ ] Check for React-specific rules
- [ ] Check for TypeScript-specific rules

### Testing
- [ ] Check for test files
- [ ] Verify test coverage
- [ ] Identify untested critical paths
- [ ] Check for integration tests

### Build Configuration
- [ ] Check build tool configuration
- [ ] Verify optimization settings
- [ ] Check for source maps configuration
- [ ] Check for proper environment variables

## 📊 Metrics to Collect

### Size Metrics
- [ ] Total lines of code
- [ ] Average component size
- [ ] Number of components >500 lines
- [ ] Number of components >1000 lines

### Performance Metrics
- [ ] Number of components without React.memo
- [ ] Number of inline object/array creations
- [ ] Number of useEffect without cleanup
- [ ] Number of missing useCallback/useMemo

### Quality Metrics
- [ ] Number of `any` types
- [ ] Number of `@ts-ignore` comments
- [ ] Number of code duplication instances
- [ ] Cyclomatic complexity of large components

## 📝 Issue Categorization

For each issue found, categorize as:

### 🔴 Critical (Fix Immediately)
- Major performance bottlenecks
- Memory leaks
- Security issues
- Critical type errors

### 🟡 Important (Fix Soon)
- Large components (>1000 lines)
- Missing React.memo on frequently rendered components
- Poor error handling
- Significant code duplication

### 🟢 Optional (Nice to Have)
- Code style improvements
- Minor refactoring opportunities
- Documentation improvements
- Test coverage improvements

## ✅ Final Checklist

- [ ] All issues documented with file path and line numbers
- [ ] Issues categorized by priority
- [ ] Metrics collected and summarized
- [ ] Quick wins identified
- [ ] Long-term improvements identified
- [ ] Verification plan created
