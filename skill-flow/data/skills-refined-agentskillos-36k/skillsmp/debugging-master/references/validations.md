# Debugging Master - Validations

## Empty Catch Block

### **Id**
empty-catch-block
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{\s*\}
  - catch\s*\{\s*\}
### **Message**
Empty catch block silently swallows errors. When something goes wrong, you'll have no idea what.
### **Fix Action**
Log the error, rethrow, or handle explicitly. Never swallow silently.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.java
  - **/*.py

## Catch Block Ignores Error

### **Id**
catch-swallows-error
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch\s*\(\s*(?:e|err|error|ex|exception)\s*\)\s*\{[^}]*\}(?!.*\1)
### **Message**
Catch block doesn't use the caught error. Log or rethrow it.
### **Fix Action**
At minimum, log the error with context for debugging.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Commented Debug Code Left Behind

### **Id**
commented-debug-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //.*console\.log
  - //.*print\(
  - //.*debugger
  - #.*print\(
  - #.*pdb
### **Message**
Commented debug code left in file. Remove or make it proper logging.
### **Fix Action**
Remove debug code or convert to proper structured logging.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Debug Print Statements

### **Id**
debug-print-in-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.log\(['"]here
  - console\.log\(['"]test
  - console\.log\(['"]debug
  - console\.log\(['"]>>>
  - print\(['"]here
  - print\(['"]test
  - print\(['"]debug
### **Message**
Debug print statement likely left from debugging session.
### **Fix Action**
Remove debug prints or convert to proper logging.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Generic Error Message

### **Id**
generic-error-message
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - throw new Error\(['"]Error['"]\)
  - throw new Error\(['"]Something went wrong['"]\)
  - throw new Error\(['"]An error occurred['"]\)
  - raise Exception\(['"]Error['"]\)
### **Message**
Generic error message provides no debugging information.
### **Fix Action**
Include specific context: what operation failed, why, with what inputs.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Error Logged Without Context

### **Id**
error-without-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.error\(\s*(?:e|err|error)\s*\)
  - logger\.error\(\s*(?:e|err|error)\s*\)
### **Message**
Error logged without context. Include what operation was attempted.
### **Fix Action**
Log: what was attempted, with what inputs, and the error.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Catch, Log, and Rethrow Unchanged

### **Id**
catch-log-rethrow
### **Severity**
info
### **Type**
regex
### **Pattern**
  - catch.*\{[^}]*(?:console|log).*throw\s+(?:e|err|error)
### **Message**
Catching, logging, and rethrowing adds noise without value.
### **Fix Action**
Either handle the error or let it propagate. Don't log at every level.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Async Operation Without Correlation

### **Id**
no-correlation-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - async function.*\{(?!.*(?:requestId|correlationId|traceId))
### **Message**
Async operation without correlation ID. Hard to trace in logs.
### **Fix Action**
Pass correlation ID through async operations for log tracing.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Magic Number in Condition

### **Id**
magic-number-condition
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if\s*\([^)]*(?:===?|!==?|[<>]=?)\s*\d{2,}[^\d]
  - status\s*(?:===?|!==?)\s*\d{3}
### **Message**
Magic number in condition. When debugging, you won't know what 86400 means.
### **Fix Action**
Use named constants: SECONDS_PER_DAY = 86400
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Silent Fallback to Default

### **Id**
silent-fallback
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \|\|\s*\[\]
  - \|\|\s*\{\}
  - \|\|\s*['"]['"]
  - \?\..*\|\|
### **Message**
Silent fallback hides errors. When data is missing, you want to know, not get empty defaults.
### **Fix Action**
Consider if missing data is actually an error that should be logged/thrown.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## TODO/FIXME Left in Code

### **Id**
todo-fix-comment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*TODO.*fix
  - //\s*FIXME
  - //\s*HACK
  - //\s*XXX
  - #\s*TODO.*fix
  - #\s*FIXME
### **Message**
TODO/FIXME comment indicates known issue. Track in issue tracker instead.
### **Fix Action**
Create issue ticket and reference it, or fix the issue.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Hardcoded Timeout Value

### **Id**
hardcoded-timeout
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setTimeout\([^,]+,\s*\d{4,}\)
  - timeout:\s*\d{4,}
  - delay:\s*\d{4,}
### **Message**
Hardcoded timeout makes debugging timing issues difficult.
### **Fix Action**
Extract to named constant with comment explaining the value.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## JSON Parse Without Try/Catch

### **Id**
unsafe-json-parse
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - JSON\.parse\([^)]+\)(?![^;]*catch)
### **Message**
JSON.parse can throw on invalid input. Unhandled, this becomes hard to debug.
### **Fix Action**
Wrap in try/catch with helpful error message about the source of the JSON.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Boolean Parameter Without Name

### **Id**
boolean-trap
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \(\s*(?:true|false)\s*\)
  - ,\s*(?:true|false)\s*[,)]
### **Message**
Boolean parameter without name. Debugging 'process(data, true, false)' is confusing.
### **Fix Action**
Use named parameters or options object: { strict: true, validate: false }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx