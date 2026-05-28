# Portfolio Optimization

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
1/N often wins
    ##### **Reason**
Simple allocation beats complex models out-of-sample
  
---
    ##### **Rule**
Shrink covariance
    ##### **Reason**
Raw sample covariance is unstable
  
---
    ##### **Rule**
Constrain weights
    ##### **Reason**
Unconstrained = concentrated bets
  
---
    ##### **Rule**
Regularize
    ##### **Reason**
Prevents corner solutions
  
---
    ##### **Rule**
Backtest carefully
    ##### **Reason**
In-sample optimal ≠ out-of-sample optimal
### **Method Selection**
  #### **Strong Return Views**
Black-Litterman
  #### **Want Diversification**
Risk Parity / HRP
  #### **Trust Estimates**
Mean-Variance (with shrinkage)
  #### **Want Simplicity**
1/N Equal Weight
  #### **Have Factor Exposures**
Factor Model
### **Markowitz Optimization**
  Maximize: w'μ - (λ/2)*w'Σw
  Subject to: w'1 = 1, w >= 0
  
  Where:
  - w = weights
  - μ = expected returns
  - Σ = covariance matrix
  - λ = risk aversion
  
### **Risk Parity Concept**
  Equal risk contribution from each asset:
  RC_i = w_i * (Σw)_i / σ_p
  Target: RC_1 = RC_2 = ... = RC_n
  
### **Hrp Steps**
  - Tree clustering on correlation distance
  - Quasi-diagonalize correlation matrix
  - Recursive bisection allocation
### **Black Litterman**
  Prior: π = δΣw_mkt (equilibrium returns)
  Views: P*μ = Q + ε
  Posterior: μ_bl = [(τΣ)^-1 + P'Ω^-1P]^-1 * [(τΣ)^-1π + P'Ω^-1Q]
  

## Anti-Patterns


---
  #### **Pattern**
No shrinkage
  #### **Problem**
Unstable covariance estimates
  #### **Solution**
Ledoit-Wolf or similar

---
  #### **Pattern**
Unconstrained optimization
  #### **Problem**
Extreme positions
  #### **Solution**
Max weight constraints

---
  #### **Pattern**
Single optimization
  #### **Problem**
Ignores estimation error
  #### **Solution**
Resampling or robust methods

---
  #### **Pattern**
In-sample only
  #### **Problem**
Overfits to historical data
  #### **Solution**
Walk-forward validation

---
  #### **Pattern**
Ignoring turnover
  #### **Problem**
High transaction costs
  #### **Solution**
Turnover constraints

---
  #### **Pattern**
No rebalancing rules
  #### **Problem**
Drift from target
  #### **Solution**
Regular or threshold-based