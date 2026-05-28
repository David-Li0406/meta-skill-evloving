# Solana Development - Validations

## Account Ownership Verification

### **Id**
check-account-ownership
### **Description**
Ensure accounts verify ownership before access
### **Pattern**
Account<'info
### **File Glob**
**/*.rs
### **Match**
absent_in_context
### **Context Pattern**
constraint.*owner|has_one
### **Message**
Account should verify ownership with constraint or has_one
### **Severity**
error
### **Autofix**


## Signer Type for Authority

### **Id**
check-signer-required
### **Description**
Authority accounts should use Signer type
### **Pattern**
pub.*authority.*AccountInfo
### **File Glob**
**/lib.rs
### **Match**
present
### **Message**
Use Signer<'info> instead of AccountInfo for authority accounts
### **Severity**
error
### **Autofix**


## Checked Arithmetic Operations

### **Id**
check-checked-math
### **Description**
Use checked_add/sub/mul/div for arithmetic
### **Pattern**
\b(balance|amount|quantity|total|sum)\s*[+\-*/]=?\s*\w+
### **File Glob**
**/*.rs
### **Match**
present
### **Message**
Use checked arithmetic (checked_add, checked_sub) for token amounts
### **Severity**
warning
### **Autofix**


## PDA Seeds Include User Context

### **Id**
check-pda-seeds
### **Description**
PDA seeds should include user-specific data
### **Pattern**
seeds\s*=\s*\[b"\w+"\]\s*,?\s*bump
### **File Glob**
**/*.rs
### **Match**
present
### **Message**
PDA seeds should include user pubkey or unique identifier
### **Severity**
warning
### **Autofix**


## Rent Exemption Calculation

### **Id**
check-rent-exemption
### **Description**
New accounts should calculate rent exemption
### **Pattern**
init\s*,
### **File Glob**
**/*.rs
### **Match**
present
### **Context Pattern**
space\s*=
### **Message**
init accounts must specify space for rent calculation
### **Severity**
error
### **Autofix**


## Zero Data Before Close

### **Id**
check-close-zero-data
### **Description**
Accounts should be zeroed before closing
### **Pattern**
close\s*=
### **File Glob**
**/*.rs
### **Match**
present
### **Message**
Consider zeroing account data before closing to prevent resurrection
### **Severity**
warning
### **Autofix**


## CPI Program ID Verification

### **Id**
check-cpi-program-id
### **Description**
Verify program ID before cross-program invocation
### **Pattern**
CpiContext::new
### **File Glob**
**/*.rs
### **Match**
present
### **Context Pattern**
Program<'info|key\(\).*==.*ID
### **Message**
Verify target program ID before CPI
### **Severity**
warning
### **Autofix**


## Compute Budget Instructions

### **Id**
check-compute-budget
### **Description**
Complex transactions should set compute budget
### **Pattern**
ComputeBudgetProgram
### **File Glob**
**/*.ts
### **Match**
absent
### **Context Pattern**
transaction|sendTransaction
### **Message**
Consider setting compute budget for complex transactions
### **Severity**
info
### **Autofix**


## Custom Error Codes

### **Id**
check-error-codes
### **Description**
Programs should define custom error codes
### **Pattern**
#\[error_code\]
### **File Glob**
**/lib.rs
### **Match**
absent
### **Message**
Define custom error codes for better debugging
### **Severity**
warning
### **Autofix**


## Event Emission for State Changes

### **Id**
check-event-emission
### **Description**
State changes should emit events for indexing
### **Pattern**
emit!
### **File Glob**
**/*.rs
### **Match**
absent_in_context
### **Context Pattern**
pub fn.*->.*Result
### **Message**
Consider emitting events for off-chain indexing
### **Severity**
info
### **Autofix**
