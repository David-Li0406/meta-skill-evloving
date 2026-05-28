# Smart Contract Engineer - Validations

## External Call Before State Update

### **Id**
reentrancy-risk
### **Severity**
error
### **Type**
regex
### **Pattern**
  - call\{value.*balances\[.*\].*=
  - transfer\(.*amount.*balances.*=
  - send\(.*balance.*=
### **Message**
External call before state update - reentrancy risk.
### **Fix Action**
Update state BEFORE external calls (checks-effects-interactions)
### **Applies To**
  - **/*.sol

## Using tx.origin for Auth

### **Id**
tx-origin
### **Severity**
error
### **Type**
regex
### **Pattern**
  - tx\.origin
  - require.*tx\.origin
### **Message**
tx.origin is vulnerable to phishing attacks.
### **Fix Action**
Use msg.sender for authentication
### **Applies To**
  - **/*.sol

## Floating Pragma Version

### **Id**
floating-pragma
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pragma solidity \^
  - pragma solidity >=
### **Message**
Floating pragma may compile with different versions.
### **Fix Action**
Lock to specific version: pragma solidity 0.8.20
### **Applies To**
  - **/*.sol

## Unchecked External Call Return

### **Id**
unchecked-return
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.call\{.*\}\([^)]*\);(?!\s*if)
  - \.send\(.*\);(?!\s*require)
### **Message**
External call return value not checked.
### **Fix Action**
Check return: (bool success, ) = ...; require(success);
### **Applies To**
  - **/*.sol

## Unsafe Math Operations (Pre-0.8)

### **Id**
unsafe-math
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pragma solidity.*0\.[0-7]
### **Message**
Solidity < 0.8 has no overflow protection.
### **Fix Action**
Use Solidity 0.8+ or SafeMath library
### **Applies To**
  - **/*.sol

## Missing Access Control

### **Id**
missing-access-control
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function.*external(?!.*onlyOwner|.*onlyRole|.*require\(msg\.sender)
  - function.*public(?!.*onlyOwner|.*view|.*pure)
### **Message**
State-changing function may be missing access control.
### **Fix Action**
Add onlyOwner or role-based access control
### **Applies To**
  - **/*.sol

## Unbounded Loop

### **Id**
unbounded-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*\.length
  - while.*true
### **Message**
Unbounded loop may exceed gas limit.
### **Fix Action**
Add iteration limits or use pagination
### **Applies To**
  - **/*.sol

## Block Timestamp Manipulation

### **Id**
block-timestamp-dependence
### **Severity**
info
### **Type**
regex
### **Pattern**
  - block\.timestamp.*<
  - block\.timestamp.*>
  - now.*[<>]
### **Message**
block.timestamp can be manipulated by miners (~15 seconds).
### **Fix Action**
Don't use for critical timing within short windows
### **Applies To**
  - **/*.sol

## Private Variable Assumption

### **Id**
private-not-hidden
### **Severity**
info
### **Type**
regex
### **Pattern**
  - private.*password
  - private.*secret
  - private.*key
### **Message**
Private variables are readable from blockchain storage.
### **Fix Action**
Never store secrets on-chain - use hashes or off-chain
### **Applies To**
  - **/*.sol

## Selfdestruct Usage

### **Id**
selfdestruct-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - selfdestruct
  - suicide
### **Message**
selfdestruct is deprecated and may be removed.
### **Fix Action**
Use alternative patterns for contract cleanup
### **Applies To**
  - **/*.sol

## State Change Without Event

### **Id**
no-events
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function.*external(?!.*emit)
### **Message**
State changes should emit events for indexing.
### **Fix Action**
Emit event for important state changes
### **Applies To**
  - **/*.sol

## Hardcoded Contract Address

### **Id**
hardcoded-addresses
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - 0x[a-fA-F0-9]{40}
### **Message**
Hardcoded address can't be updated if dependency changes.
### **Fix Action**
Use constructor parameter or admin-settable address
### **Applies To**
  - **/*.sol