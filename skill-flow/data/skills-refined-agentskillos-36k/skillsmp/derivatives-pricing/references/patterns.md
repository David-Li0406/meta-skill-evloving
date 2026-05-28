# Derivatives Pricing

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Calibrate to market
    ##### **Reason**
Model parameters from liquid options
  
---
    ##### **Rule**
Hedge, don't speculate on models
    ##### **Reason**
Greeks show exposure, not truth
  
---
    ##### **Rule**
Check put-call parity
    ##### **Reason**
Arbitrage check for consistency
  
---
    ##### **Rule**
Use implied vol, not historical
    ##### **Reason**
Market prices embed forward-looking info
  
---
    ##### **Rule**
Validate Greeks numerically
    ##### **Reason**
Analytical Greeks can have errors
### **Method Selection**
  #### **European Vanilla**
Black-Scholes (Analytical)
  #### **American Vanilla**
Binomial/Trinomial Trees
  #### **Barrier Asian**
Monte Carlo + Variance Reduction
  #### **Exotic Path Dependent**
Monte Carlo or PDE Methods
  #### **Volatility Smile**
Heston or Local Vol Models
### **Black Scholes Formula**
  d1 = (ln(S/K) + (r - q + 0.5*σ²)*T) / (σ*sqrt(T))
  d2 = d1 - σ*sqrt(T)
  Call = S*e^(-qT)*N(d1) - K*e^(-rT)*N(d2)
  Put = K*e^(-rT)*N(-d2) - S*e^(-qT)*N(-d1)
  
### **Greeks**
  #### **Delta**
Price sensitivity to spot
  #### **Gamma**
Delta sensitivity to spot
  #### **Theta**
Time decay (daily P&L)
  #### **Vega**
Sensitivity to volatility
  #### **Rho**
Sensitivity to rates
  #### **Vanna**
Delta sensitivity to vol
  #### **Volga**
Vega sensitivity to vol
### **Binomial Parameters**
  u = exp(σ*sqrt(dt))  # Up factor
  d = 1/u              # Down factor
  p = (exp((r-q)*dt) - d) / (u - d)  # Risk-neutral probability
  
### **Monte Carlo Exotics**
  #### **Asian**
Average price options with control variate
  #### **Barrier**
Brownian bridge for barrier crossing
  #### **Lookback**
Maximum/minimum over path
  #### **Basket**
Correlated asset simulation

## Anti-Patterns


---
  #### **Pattern**
Using historical vol
  #### **Problem**
Ignores market expectations
  #### **Solution**
Calibrate to implied vol

---
  #### **Pattern**
Ignoring dividends
  #### **Problem**
Misprices options near ex-dates
  #### **Solution**
Use dividend yield or discrete dividends

---
  #### **Pattern**
Single model
  #### **Problem**
Misses skew/smile
  #### **Solution**
Compare multiple models

---
  #### **Pattern**
Analytical Greeks only
  #### **Problem**
Can have errors in exotics
  #### **Solution**
Verify with bump-and-reprice

---
  #### **Pattern**
Ignoring early exercise
  #### **Problem**
Underprices American options
  #### **Solution**
Use trees or LSM