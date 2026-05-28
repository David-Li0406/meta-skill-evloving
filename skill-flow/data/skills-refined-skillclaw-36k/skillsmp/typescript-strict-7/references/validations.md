# Typescript Strict - Validations

## Using 'any' Type

### **Id**
ts-any-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - : any(?!\w)
  - as any
  - <any>
### **Message**
Using 'any' defeats type safety. Use 'unknown' or define a proper type.
### **Fix Action**
Replace 'any' with 'unknown' and add type guards, or define specific type
### **Applies To**
  - *.ts
  - *.tsx

## Non-Null Assertion Operator

### **Id**
ts-non-null-assertion
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \w+!\.
  - \w+!\[
  - \)!\.
### **Message**
Non-null assertion (!) can cause runtime errors. Use optional chaining or proper checks.
### **Fix Action**
Use optional chaining (?.) or add explicit null/undefined check
### **Applies To**
  - *.ts
  - *.tsx

## Using @ts-ignore

### **Id**
ts-ignore-comment
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @ts-ignore
  - @ts-nocheck
### **Message**
Suppressing TypeScript errors hides bugs. Fix the type error properly.
### **Fix Action**
Remove @ts-ignore and fix the underlying type issue
### **Applies To**
  - *.ts
  - *.tsx

## @ts-expect-error Without Description

### **Id**
ts-expect-error-no-description
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @ts-expect-error(?!\s+\w)
### **Message**
@ts-expect-error should have a description explaining why it's needed.
### **Fix Action**
Add explanation: // @ts-expect-error - reason why this is expected
### **Applies To**
  - *.ts
  - *.tsx

## Type Assertion to Complex Type

### **Id**
ts-type-assertion-danger
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - as (?!const)[A-Z][a-zA-Z]+(?:<|\[|\{)
### **Message**
Type assertion to complex type may hide type mismatches. Consider type guards.
### **Fix Action**
Use type guard function or Zod schema for runtime validation
### **Applies To**
  - *.ts
  - *.tsx

## Strict Mode Disabled

### **Id**
ts-strict-disabled
### **Severity**
error
### **Type**
regex
### **Pattern**
  - "strict":\s*false
  - "noImplicitAny":\s*false
  - "strictNullChecks":\s*false
### **Message**
TypeScript strict mode flags are disabled. Enable for better type safety.
### **Fix Action**
Set 'strict': true in tsconfig.json
### **Applies To**
  - tsconfig.json
  - tsconfig.*.json

## Using object or Object Type

### **Id**
ts-object-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - : object(?!\w)
  - : Object(?!\w)
### **Message**
Using 'object' type is too broad. Define a specific interface or use Record.
### **Fix Action**
Replace with specific interface, Record<string, T>, or unknown
### **Applies To**
  - *.ts
  - *.tsx

## Using Function Type

### **Id**
ts-function-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - : Function(?!\w)
### **Message**
Using 'Function' type loses parameter and return type information.
### **Fix Action**
Define specific function signature: (arg: Type) => ReturnType
### **Applies To**
  - *.ts
  - *.tsx