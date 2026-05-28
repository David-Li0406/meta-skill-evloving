# Code Review Guide

This document provides detailed guidance on what the code quality checker looks for and how to interpret its results.

## Code Smells Detected

### 1. Complexity Issues
- **Long functions**: Functions exceeding 50 lines
- **Deep nesting**: More than 3 levels of indentation
- **Too many parameters**: Functions with more than 5 parameters

### 2. Potential Bugs
- **Missing error handling**: Try-catch blocks without proper error handling
- **Uninitialized variables**: Variables declared but not initialized
- **Console statements in production**: Console.log statements in production code
- **Direct DOM manipulation**: Direct DOM queries that could fail

### 3. Code Quality Issues
- **Magic numbers**: Hardcoded numeric values without explanation
- **Duplicate code**: Identical or very similar code blocks
- **Long parameter lists**: Functions with too many parameters
- **Poor naming**: Single-letter variables (except loop counters)

### 4. TypeScript Specific
- **Any types**: Usage of `any` type that bypasses type checking
- **Non-null assertions**: Unsafe use of `!` operator
- **Type casting**: Excessive use of type assertions (`as Type`)

## Review Severity Levels

### 🔴 Critical
Issues that could cause runtime errors or security vulnerabilities:
- Division by zero without checks
- Unhandled promise rejections
- SQL injection vulnerabilities
- XSS vulnerabilities

### 🟡 Warning
Issues that reduce code quality but don't break functionality:
- Complex functions
- Missing documentation
- Code duplication
- Use of `any` type

### 🔵 Info
Suggestions for improvement:
- Style consistency
- Better naming
- Refactoring opportunities

## How to Address Issues

### For Type Errors
1. Review the error message carefully
2. Check type definitions in the affected files
3. Add or fix type annotations
4. Consider using type guards for union types

### For Linting Issues
1. Many can be auto-fixed: `npm run lint:fix`
2. For remaining issues, review the ESLint rule documentation
3. If a rule doesn't fit your project, consider disabling it in `.eslintrc.js`

### For Code Quality Issues
1. Refactor complex functions into smaller ones
2. Extract magic numbers into named constants
3. Add error handling for risky operations
4. Remove debug console statements
5. Add unit tests for critical paths

## Example Improvements

### Before: Complex Function
```typescript
function processUser(user: any) {
  if (user) {
    if (user.age > 18) {
      if (user.verified) {
        console.log('Processing user...');
        // ... 50 more lines
      }
    }
  }
}
```

### After: Refactored
```typescript
interface User {
  age: number;
  verified: boolean;
  name: string;
}

function isEligibleUser(user: User): boolean {
  return user.age > 18 && user.verified;
}

function processUser(user: User | null): void {
  if (!user) {
    throw new Error('User is required');
  }

  if (!isEligibleUser(user)) {
    return;
  }

  performUserProcessing(user);
}

function performUserProcessing(user: User): void {
  // Focused function with single responsibility
}
```
