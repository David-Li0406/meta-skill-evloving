# Tokenomics Design - Sharp Edges

## Token May Be Classified as Security

### **Id**
securities-classification
### **Severity**
CRITICAL
### **Description**
Howey test implications can make tokens securities
### **Symptoms**
  - SEC enforcement action
  - Exchange delistings
  - Legal liability for founders
### **Detection Pattern**
invest|profit|return|dividend
### **Solution**
  Howey Test - Investment Contract:
  1. Investment of money
  2. In a common enterprise
  3. With expectation of profits
  4. Derived from efforts of others
  
  Risk Reduction:
  - Emphasize utility over investment
  - Decentralize before token launch
  - No promises of returns or appreciation
  - Governance, not profit sharing
  - Utility discounts, not dividends
  
  Documentation:
  - Clear utility purpose
  - No investment language in marketing
  - Legal opinion before launch
  
### **References**
  - https://www.sec.gov/corpfin/framework-investment-contract-analysis-digital-assets

## High FDV with Low Float Creates Dump Risk

### **Id**
high-fdv-low-float
### **Severity**
CRITICAL
### **Description**
Large locked supply will eventually unlock and sell
### **Symptoms**
  - Price crashes at unlock events
  - Retail holders diluted
  - Token never recovers to ATH
### **Detection Pattern**
fdv|fully.*diluted|circulation
### **Solution**
  Calculate Unlock Impact:
  
  Current State:
  - Float: 100M tokens ($100M market cap)
  - FDV: 1B tokens ($1B FDV)
  - Ratio: 10x
  
  At Full Unlock (worst case):
  - If all new supply sells
  - Price impact: -90% (10x dilution)
  
  Mitigation:
  1. Gradual unlocks (not cliff dumps)
  2. Lock-up extensions for large holders
  3. Staking incentives for unlocked tokens
  4. Communicate unlock schedule clearly
  
  Healthy Ratio: FDV < 3x Market Cap
  
### **References**
  - https://tokenunlocks.app/

## Token Emissions Exceed Buy Pressure

### **Id**
emission-exceeds-demand
### **Severity**
CRITICAL
### **Description**
More tokens emitted than market can absorb
### **Symptoms**
  - Constant price decline
  - Decreasing TVL despite emissions
  - Death spiral
### **Detection Pattern**
emission|inflation|reward.*rate
### **Solution**
  Emission Sustainability Check:
  
  Weekly Emissions: 1,000,000 tokens
  Token Price: $1
  Weekly Emission Value: $1,000,000
  
  Required Weekly Buy Pressure:
  - Protocol Revenue: $200,000
  - New Investment: $500,000
  - Organic Demand: $300,000
  - Total: $1,000,000 minimum
  
  If buy pressure < emissions:
  - Price declines
  - APY drops in dollar terms
  - Farmers leave
  - TVL drops
  - Repeat (death spiral)
  
  Solution:
  - Emission = f(protocol revenue)
  - Dynamic rate reduction
  - Burn mechanisms
  
### **References**
  - https://tokenterminal.com/

## Large Cliff Unlock Causes Dump

### **Id**
vesting-cliff-dump
### **Severity**
HIGH
### **Description**
Significant supply unlocking on single date
### **Symptoms**
  - Sharp price decline on unlock date
  - Predictable selling opportunity
  - Community loses trust
### **Detection Pattern**
cliff|unlock.*date|vesting
### **Solution**
  Problematic:
  - 25% unlock after 1 year cliff
  - All investors unlock same date
  - Predictable dump
  
  Better:
  - Staggered cliffs (3, 6, 9, 12 months)
  - Different unlock dates per round
  - Linear vest after cliff (no lump sum)
  - Weekly/monthly unlocks, not quarterly
  
  Code Example:
  function vestedAmount(address beneficiary) public view returns (uint256) {
      uint256 elapsed = block.timestamp - vestingStart;
      if (elapsed < CLIFF) return 0;
  
      // Weekly unlocks after cliff
      uint256 weeksVested = (elapsed - CLIFF) / 1 weeks;
      uint256 totalWeeks = (VESTING_DURATION - CLIFF) / 1 weeks;
  
      return allocation[beneficiary] * weeksVested / totalWeeks;
  }
  
### **References**
  - https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#VestingWallet

## Governance Token Can Be Gamed

### **Id**
governance-attack
### **Severity**
HIGH
### **Description**
Flash loans or whale accumulation for malicious proposals
### **Symptoms**
  - Treasury drained via governance
  - Protocol parameters manipulated
  - Minority holders overruled
### **Detection Pattern**
governance|vote|proposal|quorum
### **Solution**
  Governance Safeguards:
  
  1. Snapshot Voting
  - Voting power from past block
  - Prevents flash loan attacks
  
  2. Time Locks
  - Proposal delay: 2-7 days
  - Execution delay: 24-48 hours
  - Allows community response
  
  3. Vote Escrow (veToken)
  - Must lock tokens to vote
  - Longer lock = more power
  - Can't quickly accumulate
  
  4. Multi-sig Override
  - Security council can veto
  - Emergency actions without vote
  
  5. Quorum Requirements
  - Minimum participation
  - Supermajority for critical changes
  
### **References**
  - https://blog.openzeppelin.com/governor-voting

## Liquidity Mining Incentives Run Out

### **Id**
liquidity-mining-exhaustion
### **Severity**
HIGH
### **Description**
Emissions end, LPs leave, liquidity collapses
### **Symptoms**
  - TVL cliff when incentives end
  - Slippage increases dramatically
  - Protocol becomes unusable
### **Detection Pattern**
liquidity.*mining|lp.*reward|farming
### **Solution**
  Liquidity Sustainability:
  
  Phase 1: Bootstrap (Month 1-6)
  - High emissions: 500K tokens/month
  - Goal: Attract initial liquidity
  
  Phase 2: Transition (Month 7-12)
  - Reduce emissions: 250K/month
  - Introduce POL (protocol-owned liquidity)
  - Start fee sharing to LPs
  
  Phase 3: Sustainable (Year 2+)
  - Minimal emissions: 50K/month
  - POL provides base liquidity
  - Trading fees incentivize remaining LPs
  
  Never go from high to zero emissions.
  Always have a sustainability plan.
  
### **References**
  - https://olympusdao.medium.com/

## Airdrop Recipients Immediately Dump

### **Id**
airdrop-dump
### **Severity**
HIGH
### **Description**
Free tokens sold instantly, price collapses
### **Symptoms**
  - Price drops 50%+ at airdrop claim
  - Farmers claim and sell
  - Real users get worse price
### **Detection Pattern**
airdrop|claim|distribution
### **Solution**
  Anti-Dump Airdrop Design:
  
  1. Vested Airdrop
  - 10% immediate
  - 90% over 6-12 months
  
  2. Lock Boost
  - Claim now: 100 tokens
  - Lock 3 months: 150 tokens
  - Lock 6 months: 200 tokens
  
  3. Usage Requirements
  - Must use protocol to claim
  - Partial claim per transaction
  - Ongoing engagement rewards
  
  4. Smaller Allocations
  - Cap per address
  - Wider distribution
  - Reduces whale dumps
  
### **References**
  - https://dune.com/queries/airdrop-analysis

## High Token Velocity Reduces Value

### **Id**
token-velocity-problem
### **Severity**
MEDIUM
### **Description**
Tokens immediately sold after receiving, no holding
### **Symptoms**
  - Buy pressure doesn't sustain price
  - Constant sell pressure from users
  - Token acts as pass-through
### **Detection Pattern**
velocity|hold|stake|utility
### **Solution**
  Reduce Velocity:
  
  1. Staking Requirements
  - Lock to access features
  - Higher lock = better rates
  
  2. Fee Discounts
  - Pay in token: 50% off
  - Hold threshold for discount
  
  3. Time-Weighted Benefits
  - Longer hold = more rewards
  - Loyalty multipliers
  
  4. Utility Sinks
  - Burn for premium features
  - Consume for upgrades
  
  Equation:
  Token Value = Transaction Volume / Velocity
  Lower velocity = higher value
  
### **References**
  - https://multicoin.capital/2017/12/velocity-of-tokens/

## Token Concentrated in Few Addresses

### **Id**
whale-concentration
### **Severity**
MEDIUM
### **Description**
Top holders control majority of supply
### **Symptoms**
  - Single wallet can crash price
  - Governance centralized
  - Retail hesitant to buy
### **Detection Pattern**
distribution|holder|whale|concentration
### **Solution**
  Healthy Distribution Targets:
  
  Top 10 holders: < 40% of supply
  Top 100 holders: < 70% of supply
  Gini coefficient: < 0.8
  
  Achieving Distribution:
  1. Broad airdrop (many small recipients)
  2. Cap per-address allocations
  3. Community sale with limits
  4. Liquidity mining (gradual distribution)
  
  Monitoring:
  - Track concentration metrics
  - Etherscan/Solscan holder analysis
  - Dune dashboard for distribution
  
### **References**
  - https://dune.com/queries/token-distribution

## Token Price Oracle Can Be Manipulated

### **Id**
oracle-manipulation
### **Severity**
MEDIUM
### **Description**
Low liquidity tokens vulnerable to price manipulation
### **Symptoms**
  - Flash loan attacks on DeFi integrations
  - Incorrect liquidations
  - Arbitrage exploits
### **Detection Pattern**
oracle|price.*feed|twap
### **Solution**
  Oracle Security:
  
  1. Use TWAP (Time-Weighted Average Price)
  - 30 minute minimum window
  - Resists single-block manipulation
  
  2. Multiple Sources
  - Aggregate Chainlink, Uniswap, etc.
  - Median or weighted average
  
  3. Liquidity Requirements
  - Minimum liquidity depth
  - Circuit breakers on low liquidity
  
  4. Price Deviation Checks
  - Compare to external sources
  - Pause on large deviations
  
  Code:
  require(
      deviation(oraclePrice, backupPrice) < 5%,
      "Price deviation too high"
  );
  
### **References**
  - https://docs.chain.link/data-feeds/using-data-feeds

## Forced Token Utility Creates Friction

### **Id**
token-utility-forcing
### **Severity**
MEDIUM
### **Description**
Requiring token for everything annoys users
### **Symptoms**
  - Users leave for competitors
  - Complaints about token requirement
  - Lower adoption than tokenless alternatives
### **Detection Pattern**
required|must.*hold|token.*gate
### **Solution**
  Good Utility:
  - Discounts for using token (not requirements)
  - Governance participation (optional)
  - Premium features (with free tier)
  - Staking rewards (opt-in)
  
  Bad Utility:
  - Token required for basic access
  - Can't use without buying token
  - Artificial friction
  
  Rule: Users should be able to use the
  protocol without tokens, but benefit
  from holding tokens.
  
### **References**
  - https://www.placeholder.vc/blog/tokens