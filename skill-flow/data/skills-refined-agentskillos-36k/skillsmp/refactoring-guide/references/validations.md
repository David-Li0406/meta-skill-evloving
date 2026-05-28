# Refactoring Guide - Validations

## Long Method (50+ Lines)

### **Id**
long-method
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function\s+\w+\s*\([^)]*\)\s*\{[\s\S]{2000,}?\}
  - \w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{[\s\S]{2000,}?\}
### **Message**
Long method is a code smell. Consider extracting smaller functions.
### **Fix Action**
Apply Extract Method refactoring. Each function should do one thing.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Long Parameter List

### **Id**
long-parameter-list
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function\s+\w+\s*\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,
  - \w+\s*=\s*(?:async\s*)?\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,
### **Message**
Many parameters (5+) is a code smell. Consider parameter object.
### **Fix Action**
Replace with options object: fn({ name, age, ... }) instead of fn(name, age, ...)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Feature Envy Pattern

### **Id**
feature-envy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \w+\.\w+\.\w+\.\w+
### **Message**
Deep property access suggests Feature Envy. Method might belong in different class.
### **Fix Action**
Consider Move Method refactoring. Method should be where data lives.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - this\.
  - process\.env
  - window\.location

## Unused Function Declaration

### **Id**
dead-code-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+unused\w*\s*\(
  - const\s+unused\w*\s*=\s*\(
  - //\s*function\s+\w+\s*\(
### **Message**
Possibly unused code. Dead code should be deleted, not commented.
### **Fix Action**
Delete dead code. Git has the history if you ever need it.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Primitive Obsession - ID as String

### **Id**
primitive-obsession-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - userId:\s*string
  - orderId:\s*string
  - productId:\s*string
  - customerId:\s*string
### **Message**
IDs as bare strings lose type safety. Consider branded types.
### **Fix Action**
Use branded type: type UserId = string & { readonly brand: unique symbol }
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Data Clump - Repeated Parameter Group

### **Id**
data-clump
### **Severity**
info
### **Type**
regex
### **Pattern**
  - street.*city.*zip
  - firstName.*lastName.*email
  - latitude.*longitude
### **Message**
These parameters often appear together. Consider grouping into object.
### **Fix Action**
Extract class/type for grouped data: Address { street, city, zip }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Switch Statement on Type

### **Id**
switch-on-type
### **Severity**
info
### **Type**
regex
### **Pattern**
  - switch\s*\(\s*\w+\.type\s*\)
  - switch\s*\(\s*typeof\s+
  - if\s*\([^)]*\.type\s*===.*\).*else\s+if\s*\([^)]*\.type\s*===
### **Message**
Switch on type often indicates polymorphism opportunity.
### **Fix Action**
Consider Replace Conditional with Polymorphism refactoring.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Duplicate Conditional Logic

### **Id**
duplicate-conditional
### **Severity**
info
### **Type**
regex
### **Pattern**
  - if\s*\([^)]+\)[\s\S]*if\s*\(\1\)
### **Message**
Same condition checked multiple times. Consider consolidating.
### **Fix Action**
Consolidate Conditional Expression refactoring.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Refactoring TODO Comment

### **Id**
todo-refactor-comment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*TODO:?\s*refactor
  - //\s*FIXME:?\s*refactor
  - //\s*HACK
  - //\s*XXX
### **Message**
Refactoring TODO found. Consider addressing or creating a ticket.
### **Fix Action**
Either refactor now or create a tracked issue with context.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Commented Out Code Block

### **Id**
commented-out-code-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - /\*[\s\S]*(?:function|class|const|let|var|import)[\s\S]*\*/
  - ^\s*//.*(?:function|class|const|let).*;\s*$
### **Message**
Commented code is dead code. Delete it; use version control for history.
### **Fix Action**
Delete commented code. If needed, retrieve from git history.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## God Class - Too Many Methods

### **Id**
god-class
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class\s+\w+[\s\S]{5000,}
### **Message**
Very large class. May have too many responsibilities.
### **Fix Action**
Consider Extract Class refactoring. Each class should have one responsibility.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Speculative Generality - Unused Abstraction

### **Id**
speculative-generality
### **Severity**
info
### **Type**
regex
### **Pattern**
  - interface\s+I\w+\s*\{[\s\S]{0,100}\}
  - abstract\s+class\s+\w+\s*\{[\s\S]{0,200}\}
### **Message**
Small interface or abstract class may be speculative. Verify it's used.
### **Fix Action**
If only one implementation exists, inline the abstraction.
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Middle Man - Delegation Without Value

### **Id**
middleman-class
### **Severity**
info
### **Type**
regex
### **Pattern**
  - return\s+this\.\w+\.\w+\(
  - return\s+this\.delegate\.\w+\(
### **Message**
Method just delegates to another object. Consider removing middle man.
### **Fix Action**
If class just delegates, consider Remove Middle Man refactoring.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Temporary Field Pattern

### **Id**
temporary-field
### **Severity**
info
### **Type**
regex
### **Pattern**
  - this\.temp\w+\s*=
  - this\._temp\w*\s*=
### **Message**
Temporary field suggests object is being used inconsistently.
### **Fix Action**
Consider Extract Class for the temporary state.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Refused Bequest - Overriding to Throw

### **Id**
refused-bequest
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - throw\s+new\s+(?:Error|NotImplementedError)\(['"].*not\s+(?:supported|implemented)
### **Message**
Throwing 'not implemented' in override suggests wrong inheritance.
### **Fix Action**
Consider Replace Inheritance with Delegation.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Inappropriate Intimacy - Accessing Private Details

### **Id**
inappropriate-intimacy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \[\s*['"]_\w+['"]\s*\]
  - \.\s*_private
### **Message**
Accessing another object's private details breaks encapsulation.
### **Fix Action**
Move Method or add proper public interface.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Lazy Class - Too Small to Justify

### **Id**
lazy-class
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class\s+\w+\s*\{\s*\w+\s*\([^)]*\)\s*\{[^}]{1,100}\}\s*\}
### **Message**
Very small class with only one method. May not justify its existence.
### **Fix Action**
Consider Inline Class refactoring if class doesn't pull its weight.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx