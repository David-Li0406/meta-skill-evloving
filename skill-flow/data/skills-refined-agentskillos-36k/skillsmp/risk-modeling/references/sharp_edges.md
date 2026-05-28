# Risk Modeling - Sharp Edges

## Normal Distribution Underestimates Tail Risk

### **Id**
normal-distribution-tails
### **Severity**
critical
### **Summary**
VaR based on normal assumption misses extreme events
### **Symptoms**
  - VaR breaches much more frequent than expected
  - Actual losses exceed VaR by large multiples
  - Model performs well in calm markets, fails in stress
### **Why**
  Financial returns have fat tails - extreme events occur more
  frequently than normal distribution predicts. Using normal
  assumptions can understate 99% VaR by 30-50%.
  
### **Gotcha**
  # Parametric VaR with normal assumption
  z_score = stats.norm.ppf(0.01)  # -2.33
  var_99 = mean + z_score * std
  
  # This assumes tails follow normal distribution - they don't!
  
### **Solution**
  # Use t-distribution for fat tails
  params = stats.t.fit(returns)  # Fit degrees of freedom
  z_score = stats.t.ppf(0.01, *params)
  
  # Or use historical simulation
  var_99 = np.percentile(returns, 1)
  
  # Or use Extreme Value Theory for tail estimation
  

## Monte Carlo Has High Variance

### **Id**
too-few-simulations
### **Severity**
high
### **Summary**
Small N gives unreliable VaR estimates
### **Symptoms**
  - VaR fluctuates significantly between runs
  - Tail percentiles very unstable
  - Can't reproduce results
### **Why**
  For 99% VaR with 1,000 simulations, you only have ~10 observations
  in the tail. The standard error of the percentile estimate is huge.
  Need N >= 100,000 for stable tail estimates.
  
### **Gotcha**
  # Too few simulations
  simulations = np.random.normal(0, 1, 1000)
  var_99 = np.percentile(simulations, 1)  # ~10 tail observations!
  
### **Solution**
  # Minimum 100,000 for VaR
  n_simulations = 100_000
  
  # Use antithetic variates to reduce variance
  z1 = np.random.standard_normal(n_simulations // 2)
  z2 = -z1  # Antithetic
  simulations = np.concatenate([z1, z2])
  
  # Bootstrap to estimate standard error
  bootstrap_vars = [np.percentile(np.random.choice(simulations, len(simulations)), 1) for _ in range(1000)]
  se = np.std(bootstrap_vars)
  

## Correlations Spike in Crisis

### **Id**
static-correlation
### **Severity**
high
### **Summary**
Using average correlation underestimates portfolio risk
### **Symptoms**
  - Diversification benefit evaporates in drawdowns
  - Portfolio VaR exceeded by actual losses in crisis
  - Hedges fail when most needed
### **Why**
  Correlations increase dramatically during market stress.
  Using historical average correlation understates risk
  precisely when it matters most.
  
### **Gotcha**
  # Using full-period correlation
  corr_matrix = returns.corr()  # Average correlation
  
  # Portfolio VaR assumes this holds in stress
  portfolio_var = np.sqrt(weights @ corr_matrix @ weights) * asset_vols
  
### **Solution**
  # Use stressed correlation scenarios
  def stressed_correlation(base_corr, stress_factor=0.3):
      """Move correlations toward 1 under stress."""
      return base_corr + (1 - base_corr) * stress_factor
  
  # Or use rolling correlation from crisis periods
  crisis_periods = ['2008-09':'2009-03', '2020-02':'2020-04']
  stress_corr = returns[crisis_periods].corr()
  
  # Run VaR with both normal and stressed correlations
  

## VaR Fails Subadditivity

### **Id**
var-not-coherent
### **Severity**
medium
### **Summary**
Diversified portfolio can have higher VaR than sum of parts
### **Symptoms**
  - Portfolio VaR exceeds sum of component VaRs
  - Diversification appears harmful (mathematically)
  - Risk limits create perverse incentives
### **Why**
  VaR is not a coherent risk measure - it can violate subadditivity.
  This means combining positions can appear to increase risk,
  even when diversification should reduce it.
  
### **Gotcha**
  # Two positions with different tail shapes
  var_A = np.percentile(returns_A, 1)
  var_B = np.percentile(returns_B, 1)
  var_portfolio = np.percentile(returns_A + returns_B, 1)
  
  # Can happen: var_portfolio > var_A + var_B
  
### **Solution**
  # Use Expected Shortfall (CVaR) - it's coherent
  def expected_shortfall(returns, confidence=0.99):
      var = np.percentile(returns, (1 - confidence) * 100)
      return returns[returns <= var].mean()
  
  # ES satisfies subadditivity:
  # ES(A + B) <= ES(A) + ES(B)
  

## Backtesting Can Overfit to History

### **Id**
backtest-overfitting
### **Severity**
medium
### **Summary**
Model passes backtest but fails on new data
### **Symptoms**
  - Perfect Kupiec test results
  - Model calibrated to specific historical period
  - Fails on out-of-sample data
### **Why**
  If you tune model parameters to pass backtests on historical
  data, you've essentially fit to that specific history.
  The model won't generalize to new market regimes.
  
### **Gotcha**
  # Tune parameters until backtest passes
  for alpha in [0.01, 0.02, 0.05, 0.1]:
      for beta in [0.85, 0.9, 0.95]:
          model = fit_garch(returns, alpha, beta)
          if kupiec_test(model).p_value > 0.05:
              best_params = (alpha, beta)  # Overfitting!
  
### **Solution**
  # Use walk-forward backtesting
  from sklearn.model_selection import TimeSeriesSplit
  
  tscv = TimeSeriesSplit(n_splits=5)
  results = []
  
  for train_idx, test_idx in tscv.split(returns):
      # Fit on train
      model = fit_garch(returns.iloc[train_idx])
      # Test on out-of-sample
      var_estimates = model.forecast(len(test_idx))
      results.append(kupiec_test(returns.iloc[test_idx], var_estimates))
  