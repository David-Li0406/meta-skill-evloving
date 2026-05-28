# Technical Debt Strategy - Validations

## TODO Comment Without Tracking

### **Id**
td-todo-without-ticket
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TODO(?!.*#\d+)(?!.*JIRA)(?!.*ticket)(?!.*issue)
  - FIXME(?!.*#\d+)(?!.*JIRA)(?!.*ticket)
  - HACK(?!.*#\d+)(?!.*JIRA)
### **Message**
TODO/FIXME/HACK without issue reference. Untracked debt is invisible debt that never gets paid.
### **Fix Action**
Create a ticket and reference it: TODO(#123): description. Or delete if not worth tracking.
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py
  - *.go
  - *.rs

## Lint Suppression Without Reason

### **Id**
td-suppress-without-reason
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - eslint-disable(?!.*because|.*reason|.*TODO)
  - @ts-ignore(?!.*because|.*reason)
  - noqa(?!.*#)
  - nolint(?!.*reason)
### **Message**
Lint rule suppressed without explanation. Future developers will not know if this is intentional or forgotten.
### **Fix Action**
Add reason: // eslint-disable-next-line rule-name -- reason why this is acceptable
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py
  - *.go

## TypeScript Any Type Usage

### **Id**
td-any-type-spread
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - :\s*any\b
  - as\s+any\b
  - <any>
### **Message**
Using any defeats TypeScript purpose. Each any is a future runtime error waiting to happen.
### **Fix Action**
Use unknown with type guards, proper generic types, or create specific interfaces
### **Applies To**
  - *.ts
  - *.tsx

## Magic Numbers in Code

### **Id**
td-magic-number
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?<!["\047\w])(?:86400|3600|1000|60000|300000)(?!["\047\w\d])
  - \[\s*\d{2,}\s*\]
  - ===?\s*\d{2,}(?!\d)
### **Message**
Magic numbers make code harder to understand and maintain. What does 86400 mean?
### **Fix Action**
Extract to named constants: const SECONDS_PER_DAY = 86400
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Deeply Nested Code

### **Id**
td-deep-nesting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^\s{16,}(?:if|for|while|switch)
  - \{\s*\{\s*\{\s*\{
### **Message**
Deep nesting makes code hard to follow. Often a sign of missing abstraction.
### **Fix Action**
Extract to functions, use early returns, consider state machine for complex conditionals
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py

## Commented Out Code

### **Id**
td-commented-out-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*(?:const|let|var|function|class|import)\s+\w+
  - //\s*\w+\s*\([^)]*\)\s*[;{]
  - #\s*def\s+\w+
### **Message**
Commented out code is dead weight. Version control exists for a reason.
### **Fix Action**
Delete commented code. Use git history if you need it back.
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py

## Empty Catch Block

### **Id**
td-catch-ignore
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{\s*\}
  - catch\s*\([^)]*\)\s*\{\s*//.*\s*\}
  - except:\s*pass
### **Message**
Empty catch block silently swallows errors. Failures become invisible.
### **Fix Action**
Log the error, rethrow, or handle explicitly. Silent failure is the worst failure.
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py

## Console Statements in Production Code

### **Id**
td-console-in-prod
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.(log|debug|info)\s*\(
### **Message**
Console statements in production code. Clutters logs and can leak sensitive data.
### **Fix Action**
Use proper logging service with levels, or remove debug statements before commit
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Hardcoded URLs or Endpoints

### **Id**
td-hardcoded-url
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - https?://(?!example\.com|localhost|127\.0\.0\.1)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
### **Message**
Hardcoded URL found. Environment-specific values should come from configuration.
### **Fix Action**
Move to environment variable: process.env.API_URL or configuration file
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Repeated String Literals

### **Id**
td-duplicate-string-literal
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (["\047][^"\047]{10,}["\047]).*\1.*\1
### **Message**
Same string literal repeated multiple times. Changes require finding all instances.
### **Fix Action**
Extract to constant: const ERROR_MESSAGE = 'Your message here'
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Error Without Context

### **Id**
td-no-error-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - throw\s+new\s+Error\s*\(\s*\)
  - throw\s+new\s+Error\s*\(\s*["\047]["\047]\s*\)
  - raise\s+Exception\s*\(\s*\)
### **Message**
Error thrown without message. Debugging this in production will be painful.
### **Fix Action**
Include context: throw new Error('Failed to fetch user: ${userId}')
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.py

## Oversized File

### **Id**
td-god-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^.{500,}$
### **Message**
File is very large. Large files are hard to navigate and often indicate multiple responsibilities.
### **Fix Action**
Consider splitting by concern: one concept per file, one responsibility per module
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx