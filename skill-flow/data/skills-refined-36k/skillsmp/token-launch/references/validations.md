# Token Launch - Validations

## Missing ReentrancyGuard on claim functions

### **Id**
no-reentrancy-guard
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+(claim|withdraw|release).*\{(?!.*nonReentrant)
### **Message**
Claim functions should use ReentrancyGuard
### **Fix Action**
Add nonReentrant modifier to all claim/withdraw functions
### **Applies To**
  - *.sol

## Hardcoded 18 decimals assumption

### **Id**
hardcoded-decimals
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - 10\s*\*\*\s*18|1e18
  - decimals\s*=\s*18
### **Message**
Token decimals should not be hardcoded - query from contract
### **Fix Action**
Use IERC20Metadata(token).decimals() instead
### **Applies To**
  - *.sol

## Using transfer instead of safeTransfer

### **Id**
unsafe-transfer
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.transfer\s*\(
  - \.transferFrom\s*\(
### **Message**
Use SafeERC20 safeTransfer/safeTransferFrom for compatibility
### **Fix Action**
Import SafeERC20 and use safeTransfer
### **Applies To**
  - *.sol

## Missing zero address validation

### **Id**
no-zero-address-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - address\s+\w+\s*\).*\{(?!.*require.*!=\s*address\(0\))
### **Message**
Address parameters should be validated for zero address
### **Fix Action**
Add require(_addr != address(0), 'Zero address')
### **Applies To**
  - *.sol

## Missing cliff period in vesting

### **Id**
no-cliff-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - vestingSchedule(?!.*cliff)
  - struct\s+Vesting.*\{(?!.*cliff)
### **Message**
Vesting should include cliff period
### **Fix Action**
Add cliffDuration to vesting schedule
### **Applies To**
  - *.sol

## Short timeframes using block.timestamp

### **Id**
timestamp-manipulation-risk
### **Severity**
info
### **Type**
regex
### **Pattern**
  - block\.timestamp.*<\s*\d{1,6}[^0-9]
### **Message**
Short durations with timestamp may be manipulable
### **Fix Action**
Consider using block numbers for short critical periods
### **Applies To**
  - *.sol

## Missing maximum allocation cap

### **Id**
no-allocation-cap
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+allocate(?!.*maxAllocation|.*<=.*cap)
### **Message**
Token allocations should have maximum caps
### **Fix Action**
Add per-user and total allocation limits
### **Applies To**
  - *.sol

## Allocations may exceed total supply

### **Id**
no-total-supply-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - totalAllocated\s*\+=
### **Message**
Ensure allocations cannot exceed token total supply
### **Fix Action**
Add require(totalAllocated + amount <= maxSupply)
### **Applies To**
  - *.sol

## Administrative function without access control

### **Id**
missing-owner-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+(allocate|setVesting|revoke|pause).*public(?!.*onlyOwner|.*onlyRole)
### **Message**
Administrative functions need access control
### **Fix Action**
Add onlyOwner or onlyRole modifier
### **Applies To**
  - *.sol

## Single owner without multi-sig

### **Id**
no-multisig
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Ownable\s*\(
### **Message**
Consider using multi-sig for owner functions
### **Fix Action**
Deploy owner as Gnosis Safe or similar multi-sig
### **Applies To**
  - *.sol

## No anti-bot protection at launch

### **Id**
no-launch-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+enableTrading(?!.*launchBlock|.*cooldown)
### **Message**
Consider adding anti-bot protection for launch
### **Fix Action**
Add cooldown blocks and max transaction limits
### **Applies To**
  - *.sol

## No maximum wallet limit

### **Id**
no-max-wallet
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function\s+_transfer(?!.*maxWallet|.*maxBalance)
### **Message**
Consider max wallet limits to prevent whale accumulation
### **Fix Action**
Add maxWalletAmount check in transfer
### **Applies To**
  - *.sol