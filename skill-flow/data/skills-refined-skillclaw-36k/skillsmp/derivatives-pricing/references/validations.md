# Derivatives Pricing - Validations

## Using Historical Vol for Pricing

### **Id**
historical-vol-pricing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - returns\.std\(\).*black_scholes
  - historical.*vol.*price
### **Message**
Using historical volatility for option pricing ignores market expectations.
### **Fix Action**
Extract implied volatility from market prices
### **Applies To**
  - **/*option*.py
  - **/*pricing*.py

## Same Vol for All Strikes

### **Id**
single-vol-all-strikes
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*strike.*in.*:\s*.*black_scholes.*(?!vol_surface|get_vol)
### **Message**
Using same volatility for all strikes ignores smile/skew.
### **Fix Action**
Build volatility surface, use strike-specific vol
### **Applies To**
  - **/*option*.py

## Black-Scholes for American Options

### **Id**
black-scholes-american
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - american.*black.?scholes
  - black.?scholes.*american
### **Message**
Black-Scholes doesn't price American early exercise correctly.
### **Fix Action**
Use binomial trees or LSM for American options
### **Applies To**
  - **/*.py

## No Put-Call Parity Verification

### **Id**
no-put-call-parity-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def.*price.*option(?!.*put_call_parity|.*parity_check)
### **Message**
Consider verifying put-call parity as consistency check.
### **Fix Action**
Add: C - P = S*exp(-qT) - K*exp(-rT)
### **Applies To**
  - **/*pricing*.py

## Greeks Without Numerical Verification

### **Id**
no-numerical-greek-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def.*delta|def.*gamma|def.*vega(?!.*bump|.*numerical)
### **Message**
Consider numerical verification of analytical Greeks.
### **Fix Action**
Add bump-and-reprice check for Greek formulas
### **Applies To**
  - **/*greeks*.py
  - **/*option*.py

## Barrier Options Without Brownian Bridge

### **Id**
barrier-no-bridge
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - barrier.*monte.?carlo(?!.*bridge|.*continuous)
### **Message**
Discrete monitoring misses barrier crossings between steps.
### **Fix Action**
Use Brownian bridge correction for barrier options
### **Applies To**
  - **/*exotic*.py
  - **/*barrier*.py