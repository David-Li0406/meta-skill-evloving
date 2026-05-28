# Code Review - Validations

## TODO Without Ticket Reference

### **Id**
review-todo-without-ticket
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\\s*TODO(?!.*JIRA|.*#\\d+|.*[A-Z]+-\\d+)
  - //\\s*FIXME(?!.*JIRA|.*#\\d+|.*[A-Z]+-\\d+)
  - //\\s*HACK(?!.*JIRA|.*#\\d+|.*[A-Z]+-\\d+)
### **Message**
TODO/FIXME without ticket reference. Add tracking ticket.
### **Fix Action**
Add ticket reference: // TODO: JIRA-123 - description
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Commented Out Code

### **Id**
review-commented-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\\s*(const|let|var|function|class|if|for|while|return)\\s+\\w+
  - /\\*[\\s\\S]*?(function|class|const|let|var)[\\s\\S]*?\\*/
### **Message**
Commented out code should be removed, not committed.
### **Fix Action**
Delete commented code. Use git history for recovery.
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Console Log in Production Code

### **Id**
review-console-log
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\\.log\\(
  - console\\.debug\\(
  - console\\.info\\(
### **Message**
Console statements should not be in production code.
### **Fix Action**
Remove or replace with proper logging
### **Applies To**
  - src/**/*.ts
  - src/**/*.js
  - src/**/*.tsx
  - src/**/*.jsx

## Debugger Statement

### **Id**
review-debugger
### **Severity**
error
### **Type**
regex
### **Pattern**
  - debugger;
  - debugger$
### **Message**
Debugger statement must be removed before merge.
### **Fix Action**
Remove debugger statement
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## TypeScript 'any' Type

### **Id**
review-any-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - :\\s*any\\b
  - as\\s+any\\b
  - <any>
### **Message**
Avoid 'any' type. Use specific types or 'unknown'.
### **Fix Action**
Replace with specific type or 'unknown'
### **Applies To**
  - *.ts
  - *.tsx

## Hardcoded Secret

### **Id**
review-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\\s*=\\s*["'][^"']{8,}["']
  - secret\\s*=\\s*["'][^"']{8,}["']
  - apiKey\\s*=\\s*["'][^"']{16,}["']
  - api_key\\s*=\\s*["'][^"']{16,}["']
  - AKIA[A-Z0-9]{16}
### **Message**
Possible hardcoded secret. Use environment variables.
### **Fix Action**
Move to environment variable: process.env.SECRET_NAME
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.json

## Large File

### **Id**
review-large-file
### **Severity**
warning
### **Type**
file_size
### **Max Lines**

### **Message**
File exceeds 500 lines. Consider splitting into modules.
### **Fix Action**
Split into smaller, focused modules
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Deep Nesting

### **Id**
review-deep-nesting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\{[^}]*\\{[^}]*\\{[^}]*\\{[^}]*\\{
### **Message**
Deep nesting detected. Consider early returns or extraction.
### **Fix Action**
Use early returns or extract nested logic to functions
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Magic Number

### **Id**
review-magic-number
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - [^\\d\\.](86400|3600|60000|1000|100|50)(?!\\d)
### **Message**
Magic number detected. Use named constant for clarity.
### **Fix Action**
Define constant: const SECONDS_PER_DAY = 86400
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Empty Catch Block

### **Id**
review-empty-catch
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\\s*\\([^)]*\\)\\s*\\{\\s*\\}
  - catch\\s*\\{\\s*\\}
### **Message**
Empty catch block swallows errors. Handle or rethrow.
### **Fix Action**
Log the error or rethrow: catch (e) { logger.error(e); throw e; }
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## ESLint Disable Without Explanation

### **Id**
review-eslint-disable
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - eslint-disable(?!.*--.*)
  - eslint-disable-next-line(?!.*--.*)
  - @ts-ignore(?!.*--.*)
  - @ts-expect-error(?!.*--.*)
### **Message**
Lint disable without explanation. Add reason comment.
### **Fix Action**
Add reason: // eslint-disable-next-line -- reason here
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Force Type Cast

### **Id**
review-force-cast
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - as\\s+[A-Z][a-zA-Z]+(?!\\s*\\|)
  - !\\.
  - !\\[
### **Message**
Force cast may hide type errors. Validate or use type guard.
### **Fix Action**
Add runtime validation or use type guard function
### **Applies To**
  - *.ts
  - *.tsx

## Deprecated API Usage

### **Id**
review-deprecated-api
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @deprecated
  - componentWillMount
  - componentWillReceiveProps
  - UNSAFE_
### **Message**
Deprecated API detected. Update to current API.
### **Fix Action**
Replace with current API equivalent
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Long Function

### **Id**
review-long-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (function|=>)\\s*\\{[\\s\\S]{2000,}?\\}
### **Message**
Function exceeds recommended length. Consider splitting.
### **Fix Action**
Extract logic into smaller, focused functions
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx