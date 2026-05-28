# Code Quality - Validations

## Single Letter Variable Name

### **Id**
single-letter-variable
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - const\s+[a-z]\s*=
  - let\s+[a-z]\s*=
  - var\s+[a-z]\s*=
### **Message**
Single-letter variable name provides no context. Use descriptive names.
### **Fix Action**
Rename to describe what the variable represents: 'u' → 'user', 'i' → 'index'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - for\s*\(.*[ijk]\s*=
  - \(\s*[a-z]\s*\)\s*=>

## Boolean Without is/has/can Prefix

### **Id**
unclear-boolean-name
### **Severity**
info
### **Type**
regex
### **Pattern**
  - const\s+(?!is|has|can|should|will|did)[a-z]+\s*=\s*(?:true|false)
  - let\s+(?!is|has|can|should|will|did)[a-z]+\s*=\s*(?:true|false)
### **Message**
Boolean variable should read like a question. Use is/has/can prefix.
### **Fix Action**
Rename: 'active' → 'isActive', 'permission' → 'hasPermission'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Deeply Nested Code

### **Id**
deep-nesting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{\s*\{\s*\{\s*\{
  - if\s*\([^)]+\)\s*\{[^}]*if\s*\([^)]+\)\s*\{[^}]*if\s*\([^)]+\)\s*\{
### **Message**
More than 3 levels of nesting. Consider guard clauses or extracting functions.
### **Fix Action**
Use early returns: if (!condition) return; instead of if (condition) { ... }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Magic Number

### **Id**
magic-number
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ===\s*\d{2,}(?!px|em|rem|%)
  - !==\s*\d{2,}(?!px|em|rem|%)
  - setTimeout\([^,]+,\s*\d{4,}\)
  - setInterval\([^,]+,\s*\d{4,}\)
### **Message**
Magic number without explanation. Extract to named constant.
### **Fix Action**
Create constant: const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000;
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Boolean Function Parameter

### **Id**
boolean-parameter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ,\s*(?:true|false)\s*[,)]
### **Message**
Boolean parameter hides meaning. Consider named options object.
### **Fix Action**
Use options: doThing({ verbose: true }) instead of doThing(true)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Generic Function Name

### **Id**
generic-function-name
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+(?:process|handle|manage|do|execute|run)\s*\(
  - const\s+(?:process|handle|manage|do|execute|run)\w*\s*=
### **Message**
Generic function name provides no information. Use specific verbs.
### **Fix Action**
Be specific: 'processData' → 'validateOrderItems' or 'calculateTotals'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Commented Out Code

### **Id**
commented-out-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*(?:const|let|var|function|if|for|while|return)\s+
  - //\s*\w+\s*\([^)]*\);
  - /\*[\s\S]*?(?:const|let|function)[\s\S]*?\*/
### **Message**
Commented-out code is clutter. Delete it - version control has the history.
### **Fix Action**
Delete commented code. If needed later, retrieve from git history.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Empty Function Body

### **Id**
empty-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+\w+\s*\([^)]*\)\s*\{\s*\}
  - \([^)]*\)\s*=>\s*\{\s*\}
### **Message**
Empty function body. Add implementation or document why it's intentionally empty.
### **Fix Action**
Implement the function or add comment: '// Intentionally empty: placeholder for future'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Function Exceeds 50 Lines

### **Id**
long-function
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function\s+\w+\s*\([^)]*\)\s*\{[\s\S]{2000,}?\}
### **Message**
Long function (50+ lines). Consider extracting smaller, focused functions.
### **Fix Action**
Extract distinct responsibilities into separate functions.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Console.log in Production Code

### **Id**
console-log-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.debug\(
  - console\.info\(
### **Message**
Console statements in production code. Use proper logging or remove.
### **Fix Action**
Use structured logger: logger.info() or remove debug statements.
### **Applies To**
  - **/src/**/*.ts
  - **/src/**/*.tsx
  - **/src/**/*.js
### **Exceptions**
  - **/test/**
  - **/*.test.*
  - **/*.spec.*

## TypeScript Any Type

### **Id**
any-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - :\s*any(?:\s|;|,|\)|\])
  - as\s+any
### **Message**
Using 'any' defeats TypeScript's type checking. Use specific types or 'unknown'.
### **Fix Action**
Define proper type, use 'unknown' if truly dynamic, or use type assertion.
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Catch Block Ignores Error

### **Id**
catch-and-ignore
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{\s*\}
  - catch\s*\{\s*\}
### **Message**
Empty catch block silently swallows errors. Handle or rethrow.
### **Fix Action**
Log the error, handle it, or rethrow. Never swallow silently.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Nested Ternary Operator

### **Id**
nested-ternary
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \?[^?:]*\?[^?:]*:
### **Message**
Nested ternary is hard to read. Use if/else or extract to function.
### **Fix Action**
Replace with if/else block or extract logic to named function.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## String Concatenation Instead of Template

### **Id**
string-concatenation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \+\s*['"][^'"]*['"]\s*\+
  - ['"][^'"]*['"]\s*\+\s*\w+\s*\+\s*['"]
### **Message**
String concatenation is harder to read. Use template literals.
### **Fix Action**
Use template: `Hello ${name}` instead of 'Hello ' + name
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Else After Return

### **Id**
unnecessary-else
### **Severity**
info
### **Type**
regex
### **Pattern**
  - return[^;]*;\s*\}\s*else\s*\{
### **Message**
Else after return is unnecessary. Remove else block.
### **Fix Action**
Remove else: if (x) { return y; } doOther(); instead of else { doOther(); }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx