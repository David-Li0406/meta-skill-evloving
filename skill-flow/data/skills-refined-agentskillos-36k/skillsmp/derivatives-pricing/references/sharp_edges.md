# Derivatives Pricing - Sharp Edges

## Historical Vol ≠ Implied Vol

### **Id**
historical-vs-implied-vol
### **Severity**
critical
### **Summary**
Using historical volatility for pricing ignores market expectations
### **Symptoms**
  - Pricing doesn't match market quotes
  - Hedges consistently lose money
  - Model prices diverge from dealers
### **Why**
  Implied volatility is extracted from market prices and reflects
  collective expectations. Historical volatility is backward-looking.
  Using historical vol for pricing ignores information in option prices.
  
### **Gotcha**
  # Using historical volatility
  historical_vol = returns.std() * np.sqrt(252)
  option_price = black_scholes(S, K, T, r, historical_vol)
  
  # This ignores market expectations embedded in prices!
  
### **Solution**
  # Extract implied vol from market prices
  market_price = get_option_price(ticker, strike, expiry)
  implied_vol = implied_volatility(
      market_price, S, K, T, r, option_type
  )
  
  # Use implied vol for consistent pricing
  # Build vol surface for all strikes/expiries
  

## Ignoring Volatility Smile/Skew

### **Id**
ignoring-smile-skew
### **Severity**
high
### **Summary**
Flat vol assumption misprices OTM options
### **Symptoms**
  - OTM puts underpriced relative to market
  - Hedges perform poorly in tail events
  - Risk metrics understate downside
### **Why**
  Black-Scholes assumes constant volatility across strikes.
  Markets show higher implied vol for OTM puts (skew) and
  higher vol for both OTM puts and calls (smile). Using
  ATM vol for all strikes misprices wings.
  
### **Gotcha**
  # Single vol for all strikes
  vol = get_atm_vol(ticker, expiry)
  for strike in strikes:
      price = black_scholes(S, strike, T, r, vol)  # Wrong for OTM!
  
### **Solution**
  # Build volatility surface
  vol_surface = build_vol_surface(market_data, S, r)
  
  for strike in strikes:
      vol = vol_surface.get_vol(strike, expiry)  # Strike-specific
      price = black_scholes(S, strike, T, r, vol)
  
  # Or use Heston, SABR, or local vol models
  

## European Model for American Options

### **Id**
american-vs-european
### **Severity**
high
### **Summary**
Black-Scholes underprices options with early exercise value
### **Symptoms**
  - Model prices below market for ITM puts
  - Dividend-paying stocks show large errors
  - Early exercise never considered
### **Why**
  American options can be exercised early, which has value.
  ITM puts on non-dividend stocks and ITM calls before
  dividends have early exercise premium. Black-Scholes
  can't capture this.
  
### **Gotcha**
  # Black-Scholes for American put
  price = black_scholes(S, K, T, r, sigma, 'put')
  
  # This ignores early exercise premium!
  # Deep ITM put might be worth more exercised now
  
### **Solution**
  # Use binomial tree for American options
  price = binomial_american(S, K, T, r, sigma, n_steps=500, 'put')
  
  # Or use Longstaff-Schwartz for path-dependent Americans
  price = lsm_american(S, K, T, r, sigma, n_paths=100000)
  
  # Compare to European to see early exercise premium
  

## Continuous Dividend Yield for Discrete Dividends

### **Id**
discrete-dividend-miss
### **Severity**
medium
### **Summary**
Misprices options around ex-dividend dates
### **Symptoms**
  - Large pricing errors around ex-dates
  - Call prices jump unexpectedly
  - Dividend arbitrage opportunities appear
### **Why**
  Discrete dividends cause stock price to drop by dividend
  amount on ex-date. Using continuous yield doesn't capture
  this discrete jump, leading to mispricing for short-dated
  options near ex-dates.
  
### **Gotcha**
  # Continuous dividend yield
  option_price = black_scholes(S, K, T, r, sigma, q=0.02)
  
  # Misses the discrete $0.50 dividend in 2 weeks!
  
### **Solution**
  # For short-dated options, use discrete dividends
  dividend_dates = [(0.038, 0.50), (0.288, 0.50)]  # (time, amount)
  
  # Adjust spot for present value of dividends
  S_adj = S - sum(d * np.exp(-r * t) for t, d in dividend_dates if t < T)
  
  # Price with adjusted spot
  option_price = black_scholes(S_adj, K, T, r, sigma)
  

## Analytical Greeks Can Have Errors

### **Id**
greeks-bump-vs-analytical
### **Severity**
medium
### **Summary**
Formula errors in Greeks go undetected
### **Symptoms**
  - Delta hedges don't neutralize as expected
  - P&L attribution doesn't match Greek decomposition
  - Vega hedges underperform
### **Why**
  Analytical Greek formulas are complex and easy to get wrong.
  Sign errors, missing discount factors, or wrong derivatives
  are common. Without numerical validation, errors persist.
  
### **Gotcha**
  # Analytical delta (might have bug)
  delta = np.exp(-q * T) * norm.cdf(d1)
  
  # No verification this is correct!
  
### **Solution**
  # Always verify Greeks numerically
  def verify_delta(S, K, T, r, sigma, q):
      bump = 0.01  # 1% bump
      price_up = black_scholes(S * 1.01, K, T, r, sigma, q)
      price_down = black_scholes(S * 0.99, K, T, r, sigma, q)
      numerical_delta = (price_up - price_down) / (2 * S * bump)
  
      analytical_delta = calculate_delta(S, K, T, r, sigma, q)
  
      assert abs(numerical_delta - analytical_delta) < 0.001
  