# Onchain Analytics - Sharp Edges

## Decimal Handling

### **Id**
decimal-handling
### **Summary**
Token decimals vary and cause calculation errors
### **Severity**
high
### **Situation**
  You divide raw token amounts by 1e18 assuming all tokens have
  18 decimals. USDC (6 decimals) values are off by 10^12.
  
### **Why**
  ERC20 tokens have varying decimals: USDC/USDT (6), WBTC (8),
  most others (18). Using wrong decimals completely breaks analysis.
  
### **Solution**
  -- Always join to get correct decimals
  SELECT
    t.token_bought_amount_raw / POWER(10, tk.decimals) as amount,
    t.amount_usd
  FROM dex.trades t
  LEFT JOIN tokens.erc20 tk
    ON t.token_bought_address = tk.contract_address
    AND t.blockchain = tk.blockchain
  

## Price Timing

### **Id**
price-timing
### **Summary**
Price data timing mismatch with transactions
### **Severity**
medium
### **Situation**
  You join transaction data with prices.usd. Transaction is at
  10:31:45, nearest price is 10:30:00. For volatile tokens,
  price may be 5% different.
  
### **Why**
  Price oracles update periodically (usually every minute).
  High volatility means significant gaps between actual and
  recorded prices.
  
### **Solution**
  -- Use closest price, not exact match
  SELECT t.*, p.price
  FROM transactions t
  ASOF JOIN prices.usd p
    ON t.token_address = p.contract_address
    AND t.block_time >= p.minute
  -- ASOF join gets most recent price before transaction
  

## Internal Transactions

### **Id**
internal-transactions
### **Summary**
Missing internal transactions in analysis
### **Severity**
high
### **Situation**
  You track ETH transfers using ethereum.transactions. Contract
  interactions that move ETH internally are invisible, missing
  significant value flow.
  
### **Why**
  Internal transactions (contract-to-contract ETH transfers)
  aren't in the main transactions table. They require traces.
  
### **Solution**
  -- Include internal transactions
  SELECT * FROM ethereum.transactions WHERE value > 0
  UNION ALL
  SELECT * FROM ethereum.traces
  WHERE type = 'call' AND value > 0
  