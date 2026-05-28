# Blockchain Defi - Sharp Edges

## Reentrancy Allows Recursive Exploitation

### **Id**
reentrancy-attack
### **Severity**
critical
### **Summary**
External calls before state updates enable theft
### **Symptoms**
  - Funds drained in single transaction
  - Balance discrepancies after withdrawals
  - Same function called recursively
### **Why**
  When a contract sends ETH or calls another contract before
  updating its state, the receiving contract can call back
  into the original function. This was the DAO hack ($60M).
  
### **Gotcha**
  function withdraw(uint amount) external {
      require(balances[msg.sender] >= amount);
  
      // VULNERABLE: External call before state update
      (bool success, ) = msg.sender.call{value: amount}("");
      require(success);
  
      balances[msg.sender] -= amount;  // Too late!
  }
  
### **Solution**
  // Check-Effects-Interactions pattern
  function withdraw(uint amount) external nonReentrant {
      require(balances[msg.sender] >= amount);
  
      // EFFECTS: Update state first
      balances[msg.sender] -= amount;
  
      // INTERACTIONS: External call last
      (bool success, ) = msg.sender.call{value: amount}("");
      require(success);
  }
  
  // Plus use ReentrancyGuard from OpenZeppelin
  

## Spot Price Oracles Enable Flash Loan Attacks

### **Id**
flash-loan-oracle-manipulation
### **Severity**
critical
### **Summary**
Attackers manipulate price within single transaction
### **Symptoms**
  - Massive liquidations in one block
  - Protocol loses millions instantly
  - Price spikes that don't match market
### **Why**
  Flash loans give attackers unlimited capital within a transaction.
  If your protocol uses spot price (current reserves ratio),
  attackers can manipulate it, exploit your protocol, and
  return the loan - all atomically.
  
### **Gotcha**
  // Using spot price
  function getPrice() public view returns (uint) {
      return reserve1 / reserve0;  // Manipulable!
  }
  
  function liquidate(address user) external {
      if (getPrice() < collateralRatio) {
          // Attacker flash loaned to crash price
          seizeCollateral(user);
      }
  }
  
### **Solution**
  // Use TWAP (Time-Weighted Average Price)
  function getPrice() public view returns (uint) {
      // Uniswap V3 oracle - aggregates over time
      (int24 tick, ) = pool.observe([3600, 0]);  // 1 hour TWAP
      return tickToPrice(tick);
  }
  
  // Or use Chainlink with staleness checks
  function getPrice() public view returns (uint) {
      (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
      require(block.timestamp - updatedAt < 3600, "Stale price");
      return uint256(price);
  }
  

## Impermanent Loss Exceeds Fee Income

### **Id**
impermanent-loss-surprise
### **Severity**
high
### **Summary**
LPs lose money despite high APY display
### **Symptoms**
  - LP position worth less than holding
  - High APY but negative actual returns
  - Losses accelerate with price movement
### **Why**
  AMM LPs are constantly selling winners and buying losers.
  If price moves 2x, you lose 5.7% vs holding. At 5x, you
  lose 25.5%. Trading fees may not compensate, especially
  in low-volume pools.
  
### **Gotcha**
  # Deposited $10k each of ETH and USDC
  # ETH 2x'd - but LP only up 15% vs 50% for just holding ETH
  
  initial_value = 20000  # $10k each
  eth_price_change = 2.0
  
  # IL calculation
  il = 2 * sqrt(2.0) / (1 + 2.0) - 1  # -5.7%
  
  # Holding: $10k * 2 + $10k = $30k (50% gain)
  # LP: $28,284 - 5.7% IL = ~$26,700 (33% gain)
  
### **Solution**
  def should_lp(volatility, pool_fee, expected_volume):
      """Estimate if LP will be profitable."""
      # Simplified model
      daily_vol = volatility / sqrt(365)
  
      # Expected IL from volatility
      expected_price_move = 1 + daily_vol * 30  # 30-day estimate
      expected_il = 2 * sqrt(expected_price_move) / (1 + expected_price_move) - 1
  
      # Expected fees
      expected_fees = pool_fee * expected_volume * 30
  
      return expected_fees > abs(expected_il)
  
  # Also consider: concentrated liquidity, stable pairs, hedging
  

## Unlimited Token Approvals Enable Future Theft

### **Id**
unlimited-approval-risk
### **Severity**
high
### **Summary**
Compromised contract can drain tokens years later
### **Symptoms**
  - Tokens disappear from wallet
  - User didn't interact with protocol recently
  - Exploit uses old approvals
### **Why**
  Common practice is approving max uint256 for convenience.
  If that contract is ever compromised (or has hidden
  functionality), attackers can drain all your tokens
  even years later.
  
### **Gotcha**
  // Frontend approval - max approval for convenience
  await token.approve(dexRouter, ethers.MaxUint256);
  
  // Two years later, router is exploited
  // Attacker drains all user tokens
  
### **Solution**
  // Approve only exact amount needed
  const exactAmount = parseUnits("100", 18);
  await token.approve(dexRouter, exactAmount);
  
  // Or use permit for single-transaction approval
  const { v, r, s } = await signPermit(owner, spender, value, deadline);
  await token.permit(owner, spender, value, deadline, v, r, s);
  
  // Revoke unused approvals regularly
  await token.approve(oldProtocol, 0);
  

## Transactions Get Sandwiched by MEV Bots

### **Id**
sandwich-attack
### **Severity**
medium
### **Summary**
Bots front-run and back-run your swaps for profit
### **Symptoms**
  - Worse execution price than expected
  - Large trades especially affected
  - Visible front-run transactions in block
### **Why**
  MEV bots monitor mempool for pending swaps. They front-run
  with a buy to move price, let your trade execute at worse
  price, then back-run with a sell. The bot profits from
  your slippage.
  
### **Gotcha**
  // No slippage protection
  router.swapExactTokensForTokens(
      amountIn,
      0,  // Accept any output - guaranteed to be sandwiched
      path,
      recipient,
      deadline
  );
  
### **Solution**
  // Calculate minimum output with slippage tolerance
  const quote = await router.getAmountsOut(amountIn, path);
  const minOut = quote[1] * 995n / 1000n;  // 0.5% slippage
  
  router.swapExactTokensForTokens(
      amountIn,
      minOut,  // Reject if sandwich pushes price too far
      path,
      recipient,
      deadline
  );
  
  // For large trades: use private mempool (Flashbots)
  // Or split into smaller chunks
  