# Error Handling - Validations

## Empty catch block

### **Id**
empty-catch
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - catch.*\{\s*\}
### **Message**
Empty catch block swallows errors
### **Fix Action**
Handle, log, or rethrow the error
### **Applies To**
  - *.ts
  - *.js
  - *.tsx

## Catch with only console.log

### **Id**
console-only-catch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch.*{\s*console\.(log|error).*}
### **Message**
Console only logging may not be sufficient
### **Fix Action**
Add proper error tracking
### **Applies To**
  - *.ts
  - *.tsx

## Throwing string instead of Error

### **Id**
throw-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - throw\s+["\x27]
### **Message**
Throw Error objects, not strings
### **Fix Action**
Use throw new Error() or custom error class
### **Applies To**
  - *.ts
  - *.js

## Promise without await or catch

### **Id**
floating-promise
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^\s+\w+\([^)]*\)(?!.*await|.*\.catch|.*\.then)
### **Message**
Floating promise may lose errors
### **Fix Action**
Add await or .catch()
### **Applies To**
  - *.ts
  - *.tsx

## Raw error in response

### **Id**
error-in-response
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - res\.json.*err\.message
  - res\.send.*error\.stack
### **Message**
Do not expose internal errors to clients
### **Fix Action**
Return user-friendly message, log internal error
### **Applies To**
  - *.ts
  - *.js