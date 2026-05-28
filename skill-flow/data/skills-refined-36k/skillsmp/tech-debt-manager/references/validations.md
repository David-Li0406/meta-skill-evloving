# Tech Debt Manager - Validations

## TODO Without Issue Reference

### **Id**
todo-without-issue
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*TODO(?!.*#\d|.*JIRA|.*ISSUE)
  - #\s*TODO(?!.*#\d|.*JIRA|.*ISSUE)
### **Message**
TODO without issue reference is invisible debt. Link to tracking system.
### **Fix Action**
Add issue reference: // TODO(#123): Description
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## FIXME Comment Found

### **Id**
fixme-in-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*FIXME
  - #\s*FIXME
  - /\*\s*FIXME
### **Message**
FIXME indicates known problem. Either fix now or create tracked issue.
### **Fix Action**
Fix the issue or create ticket with context and remove FIXME
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## HACK Comment Found

### **Id**
hack-comment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*HACK
  - #\s*HACK
  - //\s*XXX
### **Message**
HACK/XXX indicates deliberate shortcut. Document context and create issue.
### **Fix Action**
Add explanation of why this hack exists and link to tracking issue
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Deprecated API Usage

### **Id**
deprecated-usage
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @deprecated
  - DEPRECATED
  - \.deprecated\(
### **Message**
Using deprecated API. Consider migrating to replacement.
### **Fix Action**
Check for recommended replacement and plan migration
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Temporary Solution Marker

### **Id**
temporary-solution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*[Tt]emp
  - //\s*[Ww]orkaround
  - //\s*[Pp]laceholder
  - //\s*[Ss]tub
### **Message**
Temporary solution found. Track when permanent solution is needed.
### **Fix Action**
Either implement permanent solution or document why temporary is acceptable
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Hardcoded Configuration Value

### **Id**
hardcoded-config
### **Severity**
info
### **Type**
regex
### **Pattern**
  - localhost:\d{4}
  - 127\.0\.0\.1
  - api\..*\.com
  - password.*=.*['"]\w+
### **Message**
Hardcoded configuration is debt. Move to environment or config file.
### **Fix Action**
Extract to environment variable or configuration file
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - test
  - spec
  - mock
  - \.env

## Possible Copy-Paste Code

### **Id**
copy-paste-code
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // copied from
  - // same as
  - // duplicate of
### **Message**
Copy-paste indicated. Consider extracting shared code.
### **Fix Action**
Extract common functionality to shared module
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Missing Error Handling

### **Id**
no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{\s*\}
  - catch\s*\{\s*\}
  - \.catch\(\(\)\s*=>\s*\{\}\)
### **Message**
Empty catch block hides errors. This is hidden debt.
### **Fix Action**
Add proper error handling or at minimum logging
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Validation Bypass

### **Id**
skipped-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - // skip validation
  - // no validation
  - // trust input
  - @ts-ignore
  - @ts-nocheck
### **Message**
Skipped validation is security debt. Document why or add validation.
### **Fix Action**
Add proper validation or document why it's safe to skip
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Unpinned Dependency Version

### **Id**
version-pinning-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - "\*"
  - "latest"
  - "\^\d
  - "~\d
### **Message**
Unpinned dependency can break unexpectedly. Pin to specific version.
### **Fix Action**
Pin to specific version: 1.2.3 instead of ^1.2.3
### **Applies To**
  - **/package.json
  - **/requirements.txt
### **Exceptions**
  - devDependencies

## Unexplained Magic Number

### **Id**
magic-number-debt
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ===\s*\d{3,}[^;]*$
  - \?\s*\d{3,}\s*:
  - if\s*\(.*>\s*\d{3,}
### **Message**
Magic number without explanation is maintenance debt. Add constant or comment.
### **Fix Action**
Extract to named constant: const MAX_RETRIES = 300
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Retry Without Exponential Backoff

### **Id**
retry-without-backoff
### **Severity**
info
### **Type**
regex
### **Pattern**
  - retry.*\d\s*times
  - for.*retry
  - while.*retry
### **Message**
Retry without backoff can cause cascading failures. Add exponential backoff.
### **Fix Action**
Add exponential backoff: delay = baseDelay * Math.pow(2, attempt)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - backoff
  - exponential

## Potentially Outdated Comment

### **Id**
outdated-comment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // old:
  - // was:
  - // previously:
  - // before:
### **Message**
Comment referencing old state may be outdated. Verify accuracy.
### **Fix Action**
Update or remove comment if no longer accurate
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Raw SQL in Application Code

### **Id**
direct-database-query
### **Severity**
info
### **Type**
regex
### **Pattern**
  - query\(['"]SELECT
  - query\(['"]INSERT
  - query\(['"]UPDATE
  - query\(['"]DELETE
### **Message**
Raw SQL scattered in code is maintenance debt. Consider repository pattern.
### **Fix Action**
Move queries to dedicated data access layer or use ORM
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - repository
  - dao
  - migration

## Console Log in Production Code

### **Id**
console-log-forgotten
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.debug\(
  - print\(
### **Message**
Console/print statements suggest debug code left in. Use proper logging.
### **Fix Action**
Remove debug statements or replace with structured logging
### **Applies To**
  - **/src/**/*.ts
  - **/src/**/*.tsx
  - **/src/**/*.js
### **Exceptions**
  - test
  - spec
  - cli