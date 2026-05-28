# Perpetuals Trading - Validations

## Single oracle dependency

### **Id**
single-oracle
### **Severity**
error
### **Type**
regex
### **Pattern**
  - oracle\.getPrice(?!.*secondary|.*deviation)
### **Message**
Perpetuals should use multiple oracles with deviation checks
### **Fix Action**
Implement secondary oracle and validate deviation
### **Applies To**
  - *.sol

## No oracle freshness check

### **Id**
no-oracle-freshness
### **Severity**
error
### **Type**
regex
### **Pattern**
  - latestRoundData(?!.*timestamp|.*updatedAt)
### **Message**
Oracle prices should be validated for freshness
### **Fix Action**
Check updatedAt timestamp and reject stale prices
### **Applies To**
  - *.sol

## No maximum leverage limit

### **Id**
no-max-leverage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+openPosition(?!.*maxLeverage|.*MAX_LEVERAGE)
### **Message**
Positions must have maximum leverage limits
### **Fix Action**
Implement MAX_LEVERAGE check before opening position
### **Applies To**
  - *.sol

## No individual position size cap

### **Id**
no-position-cap
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+openPosition(?!.*maxPosition|.*positionCap)
### **Message**
Large positions create outsized risk
### **Fix Action**
Cap individual position size as percentage of pool
### **Applies To**
  - *.sol

## No open interest limit

### **Id**
no-oi-limit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - openInterest\s*\+=
### **Message**
Open interest should be capped relative to liquidity
### **Fix Action**
Check totalOI <= maxOI before increasing
### **Applies To**
  - *.sol

## No partial liquidation mechanism

### **Id**
instant-liquidation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+liquidate(?!.*partial|.*gradual)
### **Message**
Large positions should be partially liquidated
### **Fix Action**
Implement partial liquidation for positions above threshold
### **Applies To**
  - *.sol

## Missing liquidator reward

### **Id**
no-liquidation-incentive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+liquidate(?!.*reward|.*fee.*liquidator)
### **Message**
Liquidators need incentive to participate
### **Fix Action**
Add liquidation reward from position collateral
### **Applies To**
  - *.sol

## No insurance fund for bad debt

### **Id**
no-insurance-fund
### **Severity**
error
### **Type**
regex
### **Pattern**
  - contract.*Perp(?!.*insurance|.*insuranceFund)
### **Message**
Perpetual protocols need insurance fund for bad debt
### **Fix Action**
Implement insurance fund funded by trading fees
### **Applies To**
  - *.sol

## No circuit breaker for extreme moves

### **Id**
no-circuit-breaker
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - markPrice(?!.*circuitBreaker|.*pause)
### **Message**
Consider circuit breaker for extreme price movements
### **Fix Action**
Pause trading if price moves >10% in short period
### **Applies To**
  - *.sol

## Uncapped funding rate

### **Id**
uncapped-funding
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fundingRate(?!.*MAX_FUNDING|.*cap)
### **Message**
Funding rates should be capped to prevent manipulation
### **Fix Action**
Cap funding rate to reasonable maximum (e.g., 0.1% per hour)
### **Applies To**
  - *.sol