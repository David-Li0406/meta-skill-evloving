# Code Cleanup - Validations

## Unused Imports

### **Id**
cleanup-unused-imports
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - import\s+\{[^}]+\}\s+from\s+['"][^'"]+['"];?(?!.*\n.*\b\w+\b)
### **Message**
Potentially unused import. Remove or use the imported module.
### **Fix Action**
Remove unused imports or use them in code
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Commented Out Code Blocks

### **Id**
cleanup-commented-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*(const|let|var|function|class|if|for|while|return)\s+\w+
  - /\*[\s\S]{50,}?(function|class|const|let|var)[\s\S]*?\*/
### **Message**
Large block of commented code detected. Remove or document why it's kept.
### **Fix Action**
Delete commented code - use git history for recovery
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Console.log in Production Code

### **Id**
cleanup-console-log
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.debug\(
  - console\.info\(
### **Message**
Console statement in production code. Remove or replace with proper logger.
### **Fix Action**
Remove or replace with logger.debug(...)
### **Applies To**
  - src/**/*.ts
  - src/**/*.js
  - app/**/*.tsx
  - app/**/*.jsx

## TODO Without Ticket Reference

### **Id**
cleanup-todo-without-ticket
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*TODO(?!.*#\d+|.*JIRA-|.*[A-Z]+-\d+|.*http)
  - //\s*FIXME(?!.*#\d+|.*JIRA-|.*[A-Z]+-\d+)
  - //\s*HACK(?!.*#\d+|.*JIRA-|.*[A-Z]+-\d+)
### **Message**
TODO/FIXME/HACK without tracking ticket. Add ticket reference or fix it.
### **Fix Action**
Add ticket: // TODO: JIRA-123 - description or fix immediately
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Potentially Unused Function

### **Id**
cleanup-unused-function
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?:function|const)\s+(\w+)(?!.*export)(?!.*\b\1\b.*\()
### **Message**
Function defined but not exported or used. Remove if truly unused.
### **Fix Action**
Remove unused function or export if needed elsewhere
### **Applies To**
  - **/*.ts
  - **/*.js

## Empty or Near-Empty File

### **Id**
cleanup-empty-file
### **Severity**
warning
### **Type**
file_size
### **Max Lines**

### **Message**
File has fewer than 5 lines. Remove if unused.
### **Fix Action**
Delete empty/placeholder files
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Duplicate Type Definition

### **Id**
cleanup-duplicate-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - type\s+(\w+)\s*=.*\n[\s\S]{0,500}type\s+\1\s*=
  - interface\s+(\w+)\s*\{[\s\S]{0,500}interface\s+\1\s*\{
### **Message**
Duplicate type or interface definition detected.
### **Fix Action**
Consolidate into single definition or rename if different
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Skipped Tests

### **Id**
cleanup-test-skip
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - it\.skip\(
  - test\.skip\(
  - describe\.skip\(
  - xit\(
  - xdescribe\(
### **Message**
Skipped test found. Fix and unskip or remove if obsolete.
### **Fix Action**
Fix test or remove: it('test name', () => { ... })
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Debugger Statement

### **Id**
cleanup-debugger-statement
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \bdebugger;?
### **Message**
Debugger statement must be removed before commit.
### **Fix Action**
Remove debugger statement
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Outdated API Comments

### **Id**
cleanup-old-api-comment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //.*deprecated
  - //.*old version
  - /\*.*TODO.*v[0-9]+.*\*/
  - //.*legacy
### **Message**
Comment references deprecated/old code. Update or remove.
### **Fix Action**
Update comment or remove if code is updated
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Empty CSS Rules

### **Id**
cleanup-unused-css
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.[a-zA-Z_-]+\s*\{\s*\}
  - #[a-zA-Z_-]+\s*\{\s*\}
### **Message**
Empty CSS rule detected. Remove unused styles.
### **Fix Action**
Delete empty CSS rules
### **Applies To**
  - **/*.css
  - **/*.scss
  - **/*.sass

## Large Commented Block

### **Id**
cleanup-large-commented-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - /\*[\s\S]{200,}?\*/
### **Message**
Large commented block (200+ chars). Remove or move to docs.
### **Fix Action**
Delete or move explanation to docs/README
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx