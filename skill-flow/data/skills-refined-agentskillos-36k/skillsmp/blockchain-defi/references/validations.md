# Blockchain Defi - Validations

## State Change Without Reentrancy Guard

### **Id**
no-reentrancy-guard
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function.*external(?!.*nonReentrant).*\{[^}]*\.call\{
  - \.call\{value:.*balances\[.*\].*-=
### **Message**
External calls with state changes need reentrancy protection.
### **Fix Action**
Add ReentrancyGuard modifier from OpenZeppelin
### **Applies To**
  - **/*.sol

## Using Spot Price Instead of TWAP

### **Id**
spot-price-oracle
### **Severity**
error
### **Type**
regex
### **Pattern**
  - reserve[01].*\/.*reserve[10](?!.*twap|.*observe)
  - getReserves.*price.*(?!.*twap)
### **Message**
Spot price is manipulable via flash loans. Use TWAP.
### **Fix Action**
Use pool.observe() for TWAP or Chainlink oracle
### **Applies To**
  - **/*.sol

## Swap Without Slippage Protection

### **Id**
no-slippage-protection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - swapExact.*\(.*,.*0,.*\)
  - swap.*amountOutMin.*=.*0
### **Message**
Zero slippage tolerance guarantees sandwich attacks.
### **Fix Action**
Set minAmountOut to at least 99% of expected output
### **Applies To**
  - **/*.sol
  - **/*swap*.py

## Unlimited Token Approval

### **Id**
max-approval
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - approve.*type\(uint256\)\.max
  - approve.*MaxUint256
  - approve.*2\*\*256
### **Message**
Unlimited approvals create long-term risk if contract is compromised.
### **Fix Action**
Approve only exact amount needed, or use permit
### **Applies To**
  - **/*.sol
  - **/*.js
  - **/*.ts

## Transaction Without Deadline

### **Id**
no-deadline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - swap.*deadline.*=.*0
  - addLiquidity(?!.*deadline)
### **Message**
Transactions without deadline can be held and executed at bad prices.
### **Fix Action**
Set deadline to block.timestamp + reasonable duration
### **Applies To**
  - **/*.sol

## Hardcoded Contract Addresses

### **Id**
hardcoded-addresses
### **Severity**
info
### **Type**
regex
### **Pattern**
  - address.*=.*0x[a-fA-F0-9]{40}[^;]*;
### **Message**
Consider using registry pattern for upgradeability.
### **Fix Action**
Use address registry or constructor parameters
### **Applies To**
  - **/*.sol