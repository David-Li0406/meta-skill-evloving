# Testing Strategies - Validations

## Using sleep/setTimeout in tests

### **Id**
arbitrary-sleep
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sleep\s*\(\s*\d+
  - waitForTimeout\s*\(\s*\d+
  - setTimeout.*expect
### **Message**
Arbitrary waits cause flaky tests
### **Fix Action**
Use waitFor, findBy, or wait for specific conditions
### **Applies To**
  - *.test.ts
  - *.test.tsx
  - *.spec.ts
  - *.test.js

## Focused or skipped tests

### **Id**
only-skip-in-tests
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.only\s*\\(
  - it\\.skip
  - test\\.skip
  - describe\\.skip
  - fdescribe
  - fit\\(
### **Message**
Remove .only/.skip before committing
### **Fix Action**
Remove focus/skip to run all tests
### **Applies To**
  - *.test.ts
  - *.test.tsx
  - *.spec.ts

## Mocking internal modules

### **Id**
mocking-internal-modules
### **Severity**
info
### **Type**
regex
### **Pattern**
  - jest\.mock\(['"]\.\.?/
  - vi\.mock\(['"]\.\.?/
### **Message**
Consider if you're mocking too much internal code
### **Fix Action**
Mock boundaries (external APIs) not internal code
### **Applies To**
  - *.test.ts
  - *.test.tsx

## Testing implementation details

### **Id**
test-implementation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - toHaveBeenCalledTimes\\(\\d+\\)
  - \\.mock\\.calls\\[
  - getByTestId.*container
### **Message**
May be testing implementation rather than behavior
### **Fix Action**
Test observable behavior, not internal calls
### **Applies To**
  - *.test.ts
  - *.test.tsx

## Large snapshot test

### **Id**
large-snapshot
### **Severity**
info
### **Type**
regex
### **Pattern**
  - toMatchSnapshot\\(\\)$
### **Message**
Full component snapshots are hard to review
### **Fix Action**
Use toMatchInlineSnapshot or targeted assertions
### **Applies To**
  - *.test.ts
  - *.test.tsx

## Missing act() wrapper

### **Id**
missing-act
### **Severity**
info
### **Type**
regex
### **Pattern**
  - fireEvent\\..*\\nawait\\s+expect
### **Message**
State updates may need act() wrapper
### **Fix Action**
Use userEvent or wrap updates in act()
### **Applies To**
  - *.test.tsx

## Missing cleanup in beforeEach/afterEach

### **Id**
no-cleanup
### **Severity**
info
### **Type**
regex
### **Pattern**
  - beforeAll.*\\{(?![\\s\\S]*afterAll)
### **Message**
Consider adding cleanup in afterAll/afterEach
### **Fix Action**
Add cleanup to prevent test pollution
### **Applies To**
  - *.test.ts
  - *.test.tsx

## Console statements in tests

### **Id**
console-in-tests
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\\.(log|warn|error)\\(
### **Message**
Remove console statements from tests
### **Fix Action**
Use debug() from Testing Library or remove
### **Applies To**
  - *.test.ts
  - *.test.tsx

## Happy path only testing

### **Id**
no-error-test
### **Severity**
info
### **Type**
regex
### **Pattern**
  - describe.*\\{(?![\\s\\S]*(error|fail|invalid|reject))
### **Message**
Consider adding error case tests
### **Fix Action**
Add tests for error states and edge cases
### **Applies To**
  - *.test.ts
  - *.test.tsx