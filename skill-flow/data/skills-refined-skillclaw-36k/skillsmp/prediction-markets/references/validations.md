# Prediction Markets - Validations

## Single address can resolve market

### **Id**
single-oracle-resolver
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+resolve.*onlyOwner|resolve.*onlyOracle(?!.*dispute)
### **Message**
Markets should have dispute mechanism, not single resolver
### **Fix Action**
Implement UMA or multi-sig resolution with dispute period
### **Applies To**
  - *.sol

## No dispute period for resolution

### **Id**
no-dispute-period
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+resolve(?!.*liveness|.*dispute|.*challenge)
### **Message**
Resolution should have dispute/challenge period
### **Fix Action**
Add liveness period where disputes can be raised
### **Applies To**
  - *.sol

## Outcome tokens not properly backed

### **Id**
unbalanced-tokens
### **Severity**
error
### **Type**
regex
### **Pattern**
  - _mint.*outcomeToken(?!.*collateral)
### **Message**
Outcome tokens must be backed 1:1 by collateral
### **Fix Action**
Lock collateral equal to minted outcome tokens
### **Applies To**
  - *.sol

## No redemption function for winning tokens

### **Id**
missing-redemption
### **Severity**
error
### **Type**
regex
### **Pattern**
  - contract.*Prediction(?!.*redeem|.*claim)
### **Message**
Winners must be able to redeem tokens for collateral
### **Fix Action**
Implement redeem() for winning outcome tokens
### **Applies To**
  - *.sol

## Trading continues until resolution

### **Id**
no-trading-cutoff
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+(buy|trade|swap)(?!.*cutoff|.*deadline)
### **Message**
Consider trading cutoff before resolution to prevent front-running
### **Fix Action**
Add tradingCutoff before resolution time
### **Applies To**
  - *.sol

## No slippage protection for trades

### **Id**
no-slippage-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+buy(?!.*minOut|.*slippage)
### **Message**
Traders should be protected from excessive slippage
### **Fix Action**
Add minAmountOut parameter for slippage protection
### **Applies To**
  - *.sol

## Resolution without proof

### **Id**
no-resolution-proof
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+resolve.*bool\s+outcome(?!.*proof|.*data)
### **Message**
Resolution should include verifiable proof
### **Fix Action**
Require proof/data parameter for verification
### **Applies To**
  - *.sol

## No INVALID resolution option

### **Id**
no-invalid-outcome
### **Severity**
info
### **Type**
regex
### **Pattern**
  - function\s+resolve.*bool\s+outcome
### **Message**
Consider INVALID outcome for ambiguous/cancelled markets
### **Fix Action**
Add third outcome option for market invalidation
### **Applies To**
  - *.sol