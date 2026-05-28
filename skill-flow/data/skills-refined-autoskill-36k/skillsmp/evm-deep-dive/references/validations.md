# Evm Deep Dive - Validations

## Unchecked Arithmetic Safety

### **Id**
check-unchecked-arithmetic
### **Description**
Verify unchecked blocks are used safely
### **Pattern**
unchecked\s*\{[^}]*\+[^}]*\}
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Verify unchecked arithmetic cannot overflow in context
### **Severity**
warning
### **Autofix**


## Storage Variable Caching

### **Id**
check-storage-caching
### **Description**
Storage variables should be cached for multiple reads
### **Pattern**
storage\w+\s*[^=]*storage\w+
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Consider caching storage variable in memory for multiple reads
### **Severity**
info
### **Autofix**


## Calldata for External Functions

### **Id**
check-calldata-params
### **Description**
External functions should use calldata for arrays/structs
### **Pattern**
function.*external.*\(.*memory.*\[\]
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Use calldata instead of memory for external function array parameters
### **Severity**
warning
### **Autofix**


## Loop Length Caching

### **Id**
check-loop-optimization
### **Description**
Array length should be cached outside loop
### **Pattern**
for.*<.*\.length
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Cache array length before loop: uint256 len = arr.length
### **Severity**
warning
### **Autofix**


## Unchecked Increment

### **Id**
check-increment-style
### **Description**
Loop increments should be unchecked
### **Pattern**
for.*\+\+\s*\)
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
unchecked
### **Message**
Use unchecked { ++i } for loop increment
### **Severity**
info
### **Autofix**


## Redundant Zero Initialization

### **Id**
check-zero-initialization
### **Description**
Variables don't need explicit zero initialization
### **Pattern**
(uint|int)\d*\s+\w+\s*=\s*0\s*;
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Remove explicit zero initialization - variables are zero by default
### **Severity**
info
### **Autofix**


## Custom Error Usage

### **Id**
check-custom-errors
### **Description**
Use custom errors instead of require strings
### **Pattern**
require\([^,]+,\s*"[^"]+"\)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Consider custom error instead of require with string
### **Severity**
info
### **Autofix**


## Storage Packing Analysis

### **Id**
check-packed-storage
### **Description**
Check for suboptimal storage variable ordering
### **Pattern**
(uint256|bytes32|address).*;\s*(uint\d+|bool|bytes\d+).*;
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Review storage layout - smaller types after uint256 waste a slot
### **Severity**
info
### **Autofix**


## Delegatecall Safety

### **Id**
check-delegatecall-safety
### **Description**
Delegatecall to untrusted contracts is dangerous
### **Pattern**
delegatecall\(
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Verify delegatecall target is trusted - storage collision risk
### **Severity**
warning
### **Autofix**


## Selfdestruct Deprecation

### **Id**
check-selfdestruct-usage
### **Description**
Selfdestruct behavior changed post-Cancun
### **Pattern**
selfdestruct\(
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
selfdestruct only sends ETH post-Cancun, doesn't delete contract
### **Severity**
warning
### **Autofix**


## Assembly Block Review

### **Id**
check-assembly-safety
### **Description**
Assembly blocks need careful review
### **Pattern**
assembly\s*\{
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Assembly block requires careful security review
### **Severity**
info
### **Autofix**


## Immutable Variable Usage

### **Id**
check-immutable-usage
### **Description**
Frequently read constants should be immutable
### **Pattern**
constant.*SLOAD|view.*return.*storage
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Consider immutable for frequently accessed values
### **Severity**
info
### **Autofix**
