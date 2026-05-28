# Defi Architect - Sharp Edges

## Impermanent Loss

### **Id**
impermanent-loss
### **Summary**
LP positions lose value compared to holding
### **Severity**
high
### **Situation**
Providing liquidity to AMMs
### **Why**
  Deposit 1 ETH + 2000 USDC when ETH = $2000.
  ETH goes to $4000. Pool rebalances to 0.707 ETH + 2828 USDC.
  Value: $5656. If you just held: $6000.
  Lost $344 (5.7%) to impermanent loss.
  It's only "impermanent" if price returns. Usually it doesn't.
  
### **Solution**
  1. Calculate IL before providing:
     // IL = 2 * sqrt(priceRatio) / (1 + priceRatio) - 1
     // 2x price move = -5.7%
     // 5x price move = -25.5%
  
  2. Only LP when fees compensate:
     // Daily fees * 365 > Expected IL
     // High volume, stable pairs = good
     // Low volume, volatile pairs = bad
  
  3. Use concentrated liquidity wisely:
     // Uniswap V3: Higher capital efficiency
     // But IL is amplified if price moves out of range
  
  4. Consider single-sided staking:
     // Many protocols offer staking without IL
     // Lower yield but no IL risk
  
  5. Hedge with options if available
  
### **Symptoms**
  - LP position worth less than initial deposit
  - I would have made more just holding
  - Losses during volatile periods
### **Detection Pattern**
addLiquidity|deposit.*pair|LP.*token

## Oracle Latency Exploit

### **Id**
oracle-latency-exploit
### **Summary**
Stale oracle prices enable arbitrage
### **Severity**
critical
### **Situation**
Protocols depending on price feeds
### **Why**
  Chainlink updates every X% price movement or heartbeat.
  During volatile moves, on-chain price lags real price.
  Attacker sees real price moved 10%, oracle shows old price.
  Borrows at old (favorable) price, sells at real price, profits.
  
### **Solution**
  1. Check oracle freshness:
     (, , , uint256 updatedAt, ) = priceFeed.latestRoundData();
     require(block.timestamp - updatedAt < MAX_DELAY, "Stale price");
  
  2. Use circuit breakers:
     uint256 lastPrice = previousPrices[token];
     require(
         newPrice > lastPrice * 95 / 100 &&
         newPrice < lastPrice * 105 / 100,
         "Price deviation too large"
     );
  
  3. Multiple oracle sources:
     // Only proceed if sources agree within tolerance
  
  4. Pause protocol during extreme volatility:
     if (volatility > threshold) {
         _pause();
     }
  
  5. Use TWAP for large operations
  
### **Symptoms**
  - Arbitrageurs profiting from protocol
  - Bad debt accumulating
  - Unexpected liquidations/mints
### **Detection Pattern**
latestRoundData|getPrice(?!.*staleness|.*freshness)

## Flash Loan Attack

### **Id**
flash-loan-attack
### **Summary**
Attacker uses flash loan to manipulate protocol
### **Severity**
critical
### **Situation**
Any protocol with external price dependencies
### **Why**
  Flash loan $100M → Manipulate DEX price → Exploit your protocol
  at manipulated price → Repay loan → Profit.
  All in one transaction. Zero capital required.
  Hundreds of millions stolen via flash loans.
  
### **Solution**
  1. Use TWAP instead of spot price:
     // 30-minute TWAP can't be manipulated in one block
     uint256 price = twapOracle.consult(token, 1800);
  
  2. Block same-transaction dependencies:
     mapping(address => uint256) lastInteraction;
  
     modifier noFlashLoan() {
         require(lastInteraction[msg.sender] < block.number);
         lastInteraction[msg.sender] = block.number;
         _;
     }
  
  3. Use external oracles (Chainlink):
     // Decentralized, not manipulable by on-chain activity
  
  4. Delay sensitive operations:
     // Commit-reveal or time delays
  
  5. Limit single-transaction impact:
     require(amount < maxPerTransaction);
  
### **Symptoms**
  - Massive loss in single transaction
  - Protocol drained
  - Price spike then immediate reversal
### **Detection Pattern**
getReserves|balanceOf.*this.*price

## Governance Attack

### **Id**
governance-attack
### **Summary**
Attacker accumulates votes to pass malicious proposal
### **Severity**
critical
### **Situation**
On-chain governance
### **Why**
  Flash loan governance tokens → Vote for malicious proposal →
  Execute (drain treasury) → Repay tokens.
  Or: Buy tokens, pass proposal, sell tokens.
  Beanstalk lost $180M this way.
  
### **Solution**
  1. Time-lock all proposals:
     uint256 public constant TIMELOCK = 2 days;
     require(block.timestamp > proposal.createdAt + TIMELOCK);
  
  2. Snapshot voting at proposal creation:
     // Votes counted from snapshot BEFORE proposal
     // Flash loans don't help
  
  3. Quorum requirements:
     require(votes > totalSupply * 4 / 100);  // 4% quorum
  
  4. Vote delegation requirements:
     // Must delegate before proposal
     // Prevents buying votes
  
  5. Emergency pause capability:
     // Multisig can pause malicious proposals
  
### **Symptoms**
  - Large token movements before vote
  - Unusual proposals passing
  - Treasury/parameter changes
### **Detection Pattern**
propose|vote|execute|governance

## Insufficient Liquidity

### **Id**
insufficient-liquidity
### **Summary**
Liquidations fail during market stress
### **Severity**
critical
### **Situation**
Lending protocol liquidations
### **Why**
  Normal times: Liquidators compete, bad debt cleared.
  Market crash: Everyone underwater, DEXs drained, no liquidity.
  Liquidators can't sell collateral → Don't liquidate.
  Bad debt accumulates, protocol becomes insolvent.
  
### **Solution**
  1. Over-collateralization buffer:
     // 150% collateral ratio with 125% liquidation threshold
     // 25% buffer for price moves during liquidation
  
  2. Partial liquidations:
     // Liquidate 50% at a time
     // Reduces market impact
  
  3. Liquidation incentives:
     // Higher bonus during stress
     uint256 bonus = baseBonus + stressMultiplier;
  
  4. Protocol-owned liquidity:
     // Treasury can liquidate as backstop
  
  5. Insurance fund:
     // Cover bad debt from reserves
  
  6. Circuit breakers:
     // Pause new borrows in extreme conditions
  
### **Symptoms**
  - Bad debt accumulating
  - Liquidations not happening
  - Protocol token price crashing
### **Detection Pattern**
liquidate|collateral|healthFactor

## Reward Gaming

### **Id**
reward-gaming
### **Summary**
Users game reward mechanics for outsized returns
### **Severity**
high
### **Situation**
Liquidity mining, yield farming
### **Why**
  Protocol: "Earn 100% APY for providing liquidity!"
  Whale: Deposit $100M right before snapshot, collect rewards,
  withdraw after. Dilutes rewards for real users.
  Or: Create many wallets to maximize per-wallet rewards.
  
### **Solution**
  1. Time-weighted rewards:
     // reward = balance * time_held / total_weighted
     uint256 timeWeight = block.timestamp - depositTime;
     uint256 reward = balance * timeWeight * rewardRate;
  
  2. Vesting periods:
     // Rewards vest over 90 days
     // Early exit = forfeit unvested
  
  3. Lock-up requirements:
     // Must lock for X days to earn rewards
     require(block.timestamp > depositTime + lockPeriod);
  
  4. Decay function:
     // Rewards decrease over time
     // Early LPs rewarded more
  
  5. Merkle drops based on historical behavior:
     // Reward past genuine usage, not new gaming
  
### **Symptoms**
  - Whale deposits/withdrawals around snapshots
  - Many small identical wallets
  - APY much lower than advertised
### **Detection Pattern**
claimReward|harvest|pendingReward

## Cross Chain Bridge Exploit

### **Id**
cross-chain-bridge-exploit
### **Summary**
Bridge verification flaws allow fake deposits
### **Severity**
critical
### **Situation**
Multi-chain protocols with bridges
### **Why**
  Bridge verifies deposits on Chain A to mint on Chain B.
  Flaw in verification: Attacker fakes deposit proof.
  Mints unlimited tokens on Chain B. Sells, drains liquidity.
  Billions lost in bridge hacks (Ronin, Wormhole, Nomad).
  
### **Solution**
  1. Multi-sig verification:
     // Require N of M validators to confirm deposit
     require(confirmations >= threshold);
  
  2. Finality requirements:
     // Wait for source chain finality
     require(sourceBlocksConfirmed >= finalityBlocks);
  
  3. Amount limits:
     // Max transfer per transaction
     // Max transfer per hour/day
     require(dailyTransferred + amount <= dailyLimit);
  
  4. Delay for large transfers:
     // Large transfers have 24h delay
     if (amount > largeThreshold) {
         require(block.timestamp > submitTime + delay);
     }
  
  5. Emergency pause:
     // Guardian can freeze bridge
  
  6. Proof verification:
     // Multiple independent verifiers
     // Formal verification of bridge logic
  
### **Symptoms**
  - Tokens minted without deposits
  - Imbalance between chains
  - Large unexplained mints
### **Detection Pattern**
bridge|crossChain|mint.*verify

## Composability Risk

### **Id**
composability-risk
### **Summary**
Integrating protocols creates unexpected attack vectors
### **Severity**
high
### **Situation**
DeFi protocols integrated with other protocols
### **Why**
  Your protocol integrates Aave, Compound, Uniswap.
  Aave upgrades: Your integration breaks.
  Uniswap pool manipulated: Your collateral valuation wrong.
  Each integration adds risk surface. Composition multiplies risks.
  
### **Solution**
  1. Interface abstraction:
     // Don't hardcode external protocol logic
     interface ILending {
         function deposit(uint256 amount) external;
     }
  
  2. Integration circuit breakers:
     // Pause specific integrations if issues
     mapping(address => bool) public pausedIntegrations;
  
  3. Conservative assumptions:
     // Assume external protocols can be manipulated
     // Don't trust their spot prices
  
  4. Regular integration audits:
     // Check for upstream changes
  
  5. Graceful degradation:
     // Protocol works (reduced functionality) if integration fails
  
  6. Position limits:
     // Max exposure to any single integration
  
### **Symptoms**
  - Unexpected behavior after external upgrades
  - Losses from external protocol exploits
  - Integration timeouts/failures
### **Detection Pattern**
external.*contract|integration|compound|aave|uniswap