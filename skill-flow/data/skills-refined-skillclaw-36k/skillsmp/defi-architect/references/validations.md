# Defi Architect - Validations

## Using Spot Price

### **Id**
spot-price-usage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - getReserves\(\)
  - reserve0.*reserve1
  - spotPrice
### **Message**
Spot prices can be manipulated via flash loans.
### **Fix Action**
Use TWAP oracles or Chainlink price feeds
### **Applies To**
  - **/*.sol

## Single Oracle Source

### **Id**
single-oracle
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - latestRoundData\(\)(?!.*backup|.*secondary)
  - getPrice\((?!.*aggregate)
### **Message**
Single oracle source is risky - can fail or be stale.
### **Fix Action**
Use multiple oracle sources with deviation checks
### **Applies To**
  - **/*.sol

## Oracle Without Staleness Check

### **Id**
no-staleness-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - latestRoundData\(\)(?!.*updatedAt)
  - getPrice\((?!.*timestamp)
### **Message**
Oracle price may be stale without timestamp check.
### **Fix Action**
Check updatedAt and reject stale prices
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
  - swap\((?!.*minAmount)
  - exchange\((?!.*minimum)
### **Message**
Swap without slippage protection allows sandwich attacks.
### **Fix Action**
Add minAmountOut parameter and check
### **Applies To**
  - **/*.sol

## Flash Loan Vulnerable Pattern

### **Id**
flash-loan-vulnerable
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - balanceOf\(.*\).*price
  - getReserves.*mint
### **Message**
Pattern may be vulnerable to flash loan manipulation.
### **Fix Action**
Use TWAP, commit-reveal, or block-based checks
### **Applies To**
  - **/*.sol

## Missing Circuit Breaker

### **Id**
no-circuit-breaker
### **Severity**
info
### **Type**
regex
### **Pattern**
  - liquidate(?!.*paused)
  - withdraw(?!.*circuit)
### **Message**
Critical function without pause/circuit breaker.
### **Fix Action**
Add Pausable or circuit breaker for emergencies
### **Applies To**
  - **/*.sol

## Unlimited Token Approval

### **Id**
unlimited-approval
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - approve.*type\(uint256\)\.max
  - approve.*2\*\*256
  - approve.*MAX_UINT
### **Message**
Unlimited approval is risky if approved contract is compromised.
### **Fix Action**
Use exact approval amounts or approval management
### **Applies To**
  - **/*.sol
  - **/*.ts
  - **/*.js

## No Withdrawal Rate Limit

### **Id**
no-withdrawal-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - withdraw(?!.*limit|.*cooldown)
### **Message**
Large withdrawals without limits can drain protocol.
### **Fix Action**
Add withdrawal limits or cooldown periods
### **Applies To**
  - **/*.sol

## Governance Without Timelock

### **Id**
governance-no-timelock
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - execute.*proposal(?!.*timelock)
  - vote.*execute(?!.*delay)
### **Message**
Governance without timelock allows immediate malicious changes.
### **Fix Action**
Add timelock delay between voting and execution
### **Applies To**
  - **/*.sol

## Missing Reentrancy Guard

### **Id**
no-reentrancy-guard
### **Severity**
error
### **Type**
regex
### **Pattern**
  - call\{value(?!.*nonReentrant)
  - transfer\((?!.*nonReentrant)
### **Message**
External call without reentrancy protection.
### **Fix Action**
Use ReentrancyGuard modifier or checks-effects-interactions
### **Applies To**
  - **/*.sol

## Unsafe Downcast

### **Id**
unsafe-cast
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - uint128\(uint256
  - uint96\(uint256
  - int128\(int256
### **Message**
Downcast may truncate value silently.
### **Fix Action**
Use SafeCast or check bounds before casting
### **Applies To**
  - **/*.sol