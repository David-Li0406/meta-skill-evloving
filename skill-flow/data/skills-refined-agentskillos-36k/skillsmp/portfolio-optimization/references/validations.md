# Portfolio Optimization - Validations

## Raw Covariance Without Shrinkage

### **Id**
no-covariance-shrinkage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.cov\(\)(?!.*ledoit|.*shrink|.*regulariz)
  - np\.cov(?!.*shrink)
### **Message**
Raw sample covariance leads to unstable optimization.
### **Fix Action**
Use Ledoit-Wolf shrinkage: LedoitWolf().fit(returns)
### **Applies To**
  - **/*portfolio*.py
  - **/*optim*.py

## Historical Returns as Expected Returns

### **Id**
historical-returns-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.mean\(\).*expected|expected.*\.mean\(\)
  - mu.*=.*returns\.mean
### **Message**
Historical mean returns have huge estimation error.
### **Fix Action**
Shrink returns toward global mean or use Black-Litterman
### **Applies To**
  - **/*portfolio*.py

## Optimization Without Weight Constraints

### **Id**
unconstrained-optimization
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - minimize.*(?!bounds|constraint)
  - optimize.*(?!max_weight|min_weight)
### **Message**
Unconstrained optimization leads to extreme positions.
### **Fix Action**
Add bounds: [(0, 0.2) for _ in range(n_assets)]
### **Applies To**
  - **/*optim*.py

## No Equal Weight Benchmark

### **Id**
no-equal-weight-comparison
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Portfolio(?!.*equal|.*benchmark|.*1_n)
### **Message**
Consider comparing to 1/N equal weight benchmark.
### **Fix Action**
Add: equal_weight = np.ones(n) / n as baseline
### **Applies To**
  - **/*portfolio*.py

## Optimization Without Turnover Consideration

### **Id**
no-turnover-constraint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - rebalance(?!.*turnover|.*cost|.*threshold)
### **Message**
Consider turnover costs in rebalancing decisions.
### **Fix Action**
Add turnover constraint or threshold-based rebalancing
### **Applies To**
  - **/*rebalance*.py
  - **/*portfolio*.py

## No Walk-Forward Validation

### **Id**
no-walk-forward
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backtest.*(?!walk.?forward|TimeSeriesSplit|rolling)
### **Message**
In-sample backtesting overstates performance.
### **Fix Action**
Use TimeSeriesSplit for walk-forward validation
### **Applies To**
  - **/*backtest*.py
  - **/*portfolio*.py