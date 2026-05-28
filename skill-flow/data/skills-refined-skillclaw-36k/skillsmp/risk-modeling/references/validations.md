# Risk Modeling - Validations

## Monte Carlo with Few Simulations

### **Id**
too-few-simulations
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - random.*\((\d{1,4})\)
  - n_sim.*=.*\d{1,4}$
  - num_paths.*=.*\d{1,4}$
### **Message**
Monte Carlo with < 10,000 simulations gives high variance VaR estimates.
### **Fix Action**
Use minimum 100,000 simulations for VaR, apply variance reduction
### **Applies To**
  - **/*monte*.py
  - **/*simulation*.py

## VaR Using Only Normal Distribution

### **Id**
normal-var-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - norm\.ppf.*var
  - stats\.norm.*ppf(?!.*t\.ppf)
### **Message**
Parametric VaR with normal distribution underestimates fat tails.
### **Fix Action**
Use t-distribution, historical simulation, or EVT for tail estimation
### **Applies To**
  - **/*var*.py
  - **/*risk*.py

## VaR Without Expected Shortfall

### **Id**
no-expected-shortfall
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*VaR(?!.*ES|.*CVaR|.*expected_shortfall)
  - def.*var(?!.*cvar|.*expected)
### **Message**
VaR alone doesn't capture tail severity. Consider adding ES/CVaR.
### **Fix Action**
Implement Expected Shortfall alongside VaR
### **Applies To**
  - **/*risk*.py

## Using Static Correlation Matrix

### **Id**
static-correlation-matrix
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.corr\(\)(?!.*stress|.*crisis|.*rolling)
### **Message**
Static correlation may underestimate risk during market stress.
### **Fix Action**
Add stressed correlation scenarios from crisis periods
### **Applies To**
  - **/*risk*.py
  - **/*portfolio*.py

## Monte Carlo Without Variance Reduction

### **Id**
no-variance-reduction
### **Severity**
info
### **Type**
regex
### **Pattern**
  - random\.normal.*for.*in.*range(?!.*antithetic)
### **Message**
Consider variance reduction techniques for Monte Carlo.
### **Fix Action**
Add antithetic variates, control variates, or stratified sampling
### **Applies To**
  - **/*monte*.py
  - **/*simulation*.py

## Risk Model Without Backtesting

### **Id**
no-backtest
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*RiskModel(?!.*backtest|.*validate|.*kupiec)
### **Message**
Risk models should include backtesting validation.
### **Fix Action**
Implement Kupiec POF test and exception monitoring
### **Applies To**
  - **/*risk*.py
  - **/*var*.py