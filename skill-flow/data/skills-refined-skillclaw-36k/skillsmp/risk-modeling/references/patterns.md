# Risk Modeling

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Know your assumptions
    ##### **Reason**
All models have hidden assumptions that break
  
---
    ##### **Rule**
Backtest regularly
    ##### **Reason**
Model validity degrades over time
  
---
    ##### **Rule**
Use multiple measures
    ##### **Reason**
VaR alone misses tail risk
  
---
    ##### **Rule**
Stress test extremes
    ##### **Reason**
Normal conditions don't reveal fragility
  
---
    ##### **Rule**
N >= 10^5 simulations
    ##### **Reason**
Fewer simulations understate tail risk
### **Risk Measure Spectrum**
  #### **Description**
From less conservative to more conservative
  #### **Measures**
    
---
      ###### **Name**
Sensitivity
      ###### **Type**
Greeks
      ###### **Description**
First-order risk exposure
    
---
      ###### **Name**
Volatility
      ###### **Type**
Std Dev
      ###### **Description**
Dispersion measure
    
---
      ###### **Name**
VaR
      ###### **Type**
Quantile
      ###### **Description**
Loss threshold at confidence
    
---
      ###### **Name**
ES/CVaR
      ###### **Type**
Tail Average
      ###### **Description**
Expected loss beyond VaR
### **Var Methods**
  #### **Historical**
No distribution assumptions, uses actual return distribution
  #### **Parametric**
Faster but assumes returns follow specified distribution
  #### **Monte Carlo**
Most flexible, handles complex portfolios
### **Monte Carlo Techniques**
  #### **Antithetic Variates**
Generate z and -z for variance reduction
  #### **Control Variates**
Use correlated variable with known expectation
  #### **Importance Sampling**
Sample more from important regions
  #### **Stratified Sampling**
Ensure coverage across strata
### **Stress Test Types**
  #### **Historical**
Replay historical crisis scenarios
  #### **Hypothetical**
Model potential future scenarios
  #### **Reverse**
Find scenarios that cause target loss
### **Garch Model**
  sigma_t^2 = omega + alpha * r_{t-1}^2 + beta * sigma_{t-1}^2
  - alpha: reaction to market news
  - beta: persistence of volatility
  - alpha + beta: volatility persistence (should be < 1)
  

## Anti-Patterns


---
  #### **Pattern**
VaR only risk measure
  #### **Problem**
Ignores tail severity
  #### **Solution**
Add ES/CVaR for tail risk

---
  #### **Pattern**
Normal distribution assumption
  #### **Problem**
Underestimates fat tails
  #### **Solution**
Use t-distribution or historical

---
  #### **Pattern**
Static correlation
  #### **Problem**
Correlations spike in crisis
  #### **Solution**
Stressed correlation scenarios

---
  #### **Pattern**
Too few simulations
  #### **Problem**
High variance in estimates
  #### **Solution**
N >= 100,000 for VaR

---
  #### **Pattern**
No backtesting
  #### **Problem**
Model degrades silently
  #### **Solution**
Regular validation tests (Kupiec)

---
  #### **Pattern**
Single horizon
  #### **Problem**
Misses liquidity risk
  #### **Solution**
Multiple holding periods