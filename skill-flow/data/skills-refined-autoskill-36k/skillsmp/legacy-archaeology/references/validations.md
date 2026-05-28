# Legacy Archaeology - Validations

## Removing Code Without Context

### **Id**
no-context-removal
### **Severity**
high
### **Type**
conceptual
### **Check**
Should understand code before removing
### **Indicators**
  - Removing unused code
  - Cleaning up dead code
  - Deleting old code
### **Message**
Removing code without understanding why it exists.
### **Fix Action**
Git blame, find context, add logging before removing

## Unverified Assumptions

### **Id**
assumption-not-verified
### **Severity**
medium
### **Type**
conceptual
### **Check**
Understanding should be verified by running
### **Indicators**
  - I think it does
  - It should
  - It looks like
### **Message**
Assumption not verified by running code.
### **Fix Action**
Add test or logging to verify actual behavior

## Learning Not Documented

### **Id**
no-documentation
### **Severity**
medium
### **Type**
conceptual
### **Check**
Discoveries should be documented
### **Indicators**
  - Now I understand
  - Finally figured out
  - This actually does
### **Message**
Understanding not being documented.
### **Fix Action**
Write down discoveries in repo docs

## Single Person Knowledge

### **Id**
knowledge-silo
### **Severity**
high
### **Type**
conceptual
### **Check**
Knowledge should be shared
### **Indicators**
  - Only I know
  - Ask Bob
  - She wrote it
### **Message**
Knowledge siloed to one person.
### **Fix Action**
Document and share knowledge, create backup

## Fear Preventing Changes

### **Id**
fear-driven-freeze
### **Severity**
medium
### **Type**
conceptual
### **Check**
Fear should be addressed, not avoided
### **Indicators**
  - Don't touch that
  - It's scary
  - We never change
### **Message**
Fear preventing necessary changes.
### **Fix Action**
Add tests, monitoring, feature flags for safe changes

## Changing Without Tests

### **Id**
missing-characterization
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have tests before modifying legacy code
### **Indicators**
  - Modifying untested code
  - No test coverage
  - Tests don't exist
### **Message**
Changing legacy code without characterization tests.
### **Fix Action**
Write tests documenting current behavior first