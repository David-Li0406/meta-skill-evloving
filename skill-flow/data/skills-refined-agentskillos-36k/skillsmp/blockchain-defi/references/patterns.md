# Blockchain DeFi

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Audit before deploy
    ##### **Reason**
Bugs are permanent and exploitable
  
---
    ##### **Rule**
Use battle-tested code
    ##### **Reason**
Don't reinvent OpenZeppelin
  
---
    ##### **Rule**
Check-Effects-Interactions
    ##### **Reason**
Prevents reentrancy attacks
  
---
    ##### **Rule**
Never trust external calls
    ##### **Reason**
Any callback can be malicious
  
---
    ##### **Rule**
Assume oracles can fail
    ##### **Reason**
Use multiple sources, circuit breakers
### **Defi Stack**
  #### **Applications**
Yield Aggregators, Dashboards, Wallets
  #### **Protocols**
Uniswap, Aave, Compound, Curve, MakerDAO
  #### **Primitives**
AMMs, Lending, Stablecoins, Oracles
  #### **L2 Scaling**
Arbitrum, Optimism, Base, zkSync
  #### **L1 Blockchain**
Ethereum, Solana, Avalanche
### **Amm Formula**
  Constant Product: x * y = k
  Price impact: dy = y - k/(x + dx)
  LP tokens: sqrt(x * y)
  Fee: 0.3% on swaps (Uniswap)
  
### **Impermanent Loss**
  IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
  
  Examples:
  - 2x price change: -5.7% IL
  - 5x price change: -25.5% IL
  - 0.5x price change: -5.7% IL
  
### **Security Patterns**
  #### **Reentrancy Guard**
Lock state during external calls
  #### **Check Effects Interactions**
Update state before external calls
  #### **Access Control**
onlyOwner, role-based permissions
  #### **Emergency Pause**
Circuit breaker for exploits
  #### **Slippage Protection**
minAmountOut on swaps
  #### **Deadline**
Prevent stale transactions

## Anti-Patterns


---
  #### **Pattern**
Spot price oracle
  #### **Problem**
Flash loan manipulation
  #### **Solution**
Use TWAP

---
  #### **Pattern**
No slippage protection
  #### **Problem**
Sandwich attacks
  #### **Solution**
Set minAmountOut

---
  #### **Pattern**
Unlimited approvals
  #### **Problem**
Token theft if contract compromised
  #### **Solution**
Approve exact amounts

---
  #### **Pattern**
Hardcoded addresses
  #### **Problem**
No upgradeability
  #### **Solution**
Use registry pattern

---
  #### **Pattern**
No deadline
  #### **Problem**
Stale transactions execute
  #### **Solution**
Always set deadline

---
  #### **Pattern**
Single oracle
  #### **Problem**
Oracle failure
  #### **Solution**
Multiple sources + circuit breaker