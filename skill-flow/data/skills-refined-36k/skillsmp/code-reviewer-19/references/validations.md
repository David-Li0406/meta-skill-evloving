# Code Reviewer - Validations

## TODO Without Issue Reference

### **Id**
todo-without-issue
### **Severity**
info
### **Type**
regex
### **Pattern**
  - TODO(?!.*#[0-9]+|.*issue|.*JIRA)
  - FIXME(?!.*#[0-9]+|.*issue)
  - HACK(?!.*#[0-9]+|.*issue)
### **Message**
TODO/FIXME without issue reference. May be forgotten.
### **Fix Action**
Link to issue: TODO(#123): description
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Magic Number in Code

### **Id**
magic-number
### **Severity**
info
### **Type**
regex
### **Pattern**
  - if.*[=<>].*\b(100|1000|60|3600|86400)\b
  - sleep\(\d{2,}\)
  - limit.*=.*\d{2,}(?!.*#)
### **Message**
Magic number without explanation. Consider named constant.
### **Fix Action**
Extract to constant: RETRY_TIMEOUT_SECONDS = 60
### **Applies To**
  - **/*.py
  - **/*.ts

## Class With Too Many Methods

### **Id**
god-class
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*:.*def.*def.*def.*def.*def.*def.*def.*def.*def.*def
### **Message**
Class has many methods. May have too many responsibilities.
### **Fix Action**
Consider splitting into focused classes (Single Responsibility)
### **Applies To**
  - **/*.py

## Deeply Nested Code

### **Id**
deep-nesting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*:\s+if.*:\s+if.*:\s+if
  - for.*:\s+for.*:\s+for.*:
### **Message**
Deep nesting makes code hard to follow.
### **Fix Action**
Use guard clauses, extract methods, or invert conditions
### **Applies To**
  - **/*.py
  - **/*.ts

## Catching All Exceptions

### **Id**
catch-all-exception
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - except\s*:
  - except Exception:
  - catch\s*\(\s*\)
  - catch\s*\(.*Error\s*\)
### **Message**
Catching all exceptions hides bugs and unexpected errors.
### **Fix Action**
Catch specific exceptions: except ValueError, KeyError:
### **Applies To**
  - **/*.py
  - **/*.ts

## Commented Out Code

### **Id**
commented-code
### **Severity**
info
### **Type**
regex
### **Pattern**
  - #\s*(def|class|if|for|while|return)\s
  - //\s*(function|const|let|var|if|for)\s
### **Message**
Commented code clutters codebase. Delete or restore.
### **Fix Action**
Remove commented code. Use git history if needed later.
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Function Too Long

### **Id**
long-function
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def.*:(\n.*){50,}
  - function.*\{(\n.*){50,}
### **Message**
Function is very long. May have multiple responsibilities.
### **Fix Action**
Extract logical chunks into well-named helper functions
### **Applies To**
  - **/*.py
  - **/*.ts

## Hardcoded Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\s*=\s*["'][^"']+["']
  - api_key\s*=\s*["'][^"']+["']
  - secret\s*=\s*["'][^"']+["']
  - token\s*=\s*["'][A-Za-z0-9]{20,}["']
### **Message**
Hardcoded credentials. Security vulnerability.
### **Fix Action**
Use environment variables or secrets manager
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Print Debugging Left In

### **Id**
print-debugging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - print\(["']debug
  - console\.log\(["']debug
  - print\(f["'].*=
### **Message**
Debug print statement. Use proper logging instead.
### **Fix Action**
Use logger.debug() or remove before merge
### **Applies To**
  - **/*.py
  - **/*.ts

## Duplicated Code Block

### **Id**
duplicate-code
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (\b\w+\s*=\s*\w+\.\w+\(\).*\n){3,}
### **Message**
Possible code duplication. Consider extracting common logic.
### **Fix Action**
Extract to function or use loop/map
### **Applies To**
  - **/*.py
  - **/*.ts

## Direct Mutation of Class State

### **Id**
public-field-mutation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - self\.\w+\s*=.*(?!__init__|__new__)
  - this\.\w+\s*=.*(?!constructor)
### **Message**
Direct state mutation outside initializer. Consider encapsulation.
### **Fix Action**
Use setter methods or make field private
### **Applies To**
  - **/*.py
  - **/*.ts

## Public Function Without Docstring

### **Id**
missing-docstring
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def [^_].*\):\s*\n\s+[^"']
  - async def [^_].*\):\s*\n\s+[^"']
### **Message**
Public function without docstring. Add description.
### **Fix Action**
Add docstring explaining purpose, params, and return
### **Applies To**
  - **/*.py