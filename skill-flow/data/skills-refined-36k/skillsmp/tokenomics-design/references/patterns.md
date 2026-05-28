# Tokenomics Design

## Patterns


---
  #### **Name**
Progressive Decentralization Vesting
  #### **Description**
Longer vesting for insiders, faster for community
  #### **When**
VC-backed projects seeking decentralization
  #### **Example**
    Token Distribution Example:
    - Total Supply: 1,000,000,000 tokens
    
    Community (60%):
    - Airdrop: 5% - No vesting, immediate claim
    - Ecosystem Grants: 25% - Milestone-based, 4 years
    - Liquidity Mining: 20% - Emission schedule, 4 years
    - Treasury: 10% - Governance-controlled
    
    Insiders (40%):
    - Team: 20% - 1 year cliff, 4 year linear vest
    - Investors: 15% - 1 year cliff, 3 year linear vest
    - Advisors: 5% - 6 month cliff, 2 year linear vest
    
    TGE Circulating: ~5-10%
    Year 1: ~25%
    Year 4: 100%
    

---
  #### **Name**
ve-Token Model
  #### **Description**
Vote-escrowed tokens for governance and rewards
  #### **When**
Need strong holder alignment and reduced sell pressure
  #### **Example**
    // Curve-style vote escrow
    contract VeToken {
        struct Lock {
            uint256 amount;
            uint256 unlockTime;
        }
    
        mapping(address => Lock) public locks;
    
        // Lock tokens for voting power
        function lock(uint256 amount, uint256 duration) external {
            require(duration >= MIN_LOCK && duration <= MAX_LOCK);
    
            locks[msg.sender] = Lock({
                amount: amount,
                unlockTime: block.timestamp + duration
            });
    
            // Voting power = amount * (duration / MAX_LOCK)
            // 4 year lock = 100% voting power
            // 1 year lock = 25% voting power
        }
    
        function votingPower(address user) public view returns (uint256) {
            Lock memory userLock = locks[user];
            uint256 remaining = userLock.unlockTime - block.timestamp;
            return userLock.amount * remaining / MAX_LOCK;
        }
    }
    

---
  #### **Name**
Dual Token Model
  #### **Description**
Separate governance and utility tokens
  #### **When**
Need stable utility pricing with speculative governance
  #### **Example**
    Dual Token Structure:
    
    GOV Token (Governance):
    - Fixed supply: 100M
    - Used for: Protocol votes, parameter changes
    - Vesting: Standard insider vesting
    - Value: Speculative, tied to protocol success
    
    UTIL Token (Utility):
    - Dynamic supply (mint/burn)
    - Used for: Transaction fees, staking
    - Stable value target: $1 (algorithmic or backed)
    - No vesting: Available on demand
    
    Interaction:
    - Stake GOV to earn UTIL emissions
    - Burn UTIL for protocol services
    - GOV holders vote on UTIL monetary policy
    

---
  #### **Name**
Bonding Curve Distribution
  #### **Description**
Price increases with supply for fair launch
  #### **When**
No VC, community-first distribution
  #### **Example**
    contract BondingCurve {
        uint256 public supply;
        uint256 public reserveBalance;
    
        // Price = k * supply^n
        // Linear: n = 1
        // Quadratic: n = 2
    
        function calculatePrice(uint256 amount) public view returns (uint256) {
            // Integral of price curve
            uint256 newSupply = supply + amount;
            return (newSupply ** 2 - supply ** 2) * PRICE_FACTOR / 2;
        }
    
        function buy(uint256 amount) external payable {
            uint256 cost = calculatePrice(amount);
            require(msg.value >= cost, "Insufficient payment");
    
            supply += amount;
            reserveBalance += cost;
    
            _mint(msg.sender, amount);
        }
    
        function sell(uint256 amount) external {
            uint256 refund = calculateSellReturn(amount);
    
            supply -= amount;
            reserveBalance -= refund;
    
            _burn(msg.sender, amount);
            payable(msg.sender).transfer(refund);
        }
    }
    

---
  #### **Name**
Emissions Halving Schedule
  #### **Description**
Bitcoin-style periodic emission reduction
  #### **When**
Long-term sustainability with predictable supply
  #### **Example**
    Halving Schedule Example:
    
    Initial Emission: 1,000,000 tokens/year
    Halving Period: Every 2 years
    
    Year 1-2:  1,000,000/year  (2M total)
    Year 3-4:    500,000/year  (3M total)
    Year 5-6:    250,000/year  (3.5M total)
    Year 7-8:    125,000/year  (3.75M total)
    ...
    Asymptotic Max: 4,000,000 tokens
    
    Benefits:
    - Predictable supply schedule
    - Decreasing inflation over time
    - Strong early incentives
    - Long-term sustainability
    

---
  #### **Name**
Protocol-Owned Liquidity
  #### **Description**
Protocol owns LP positions instead of renting
  #### **When**
Reducing dependency on mercenary LPs
  #### **Example**
    // Olympus-style bonding
    contract Treasury {
        function bond(
            address lpToken,
            uint256 amount,
            uint256 maxPrice
        ) external returns (uint256 payout) {
            // User deposits LP tokens
            IERC20(lpToken).transferFrom(msg.sender, address(this), amount);
    
            // Calculate bond price (discounted token)
            uint256 price = bondPrice(lpToken);
            require(price <= maxPrice, "Slippage");
    
            // Payout vests over 5 days
            payout = amount * price / 1e18;
            vestingInfo[msg.sender] = VestInfo({
                payout: payout,
                vestingEnd: block.timestamp + 5 days
            });
        }
    
        // Protocol now owns LP forever
        // No ongoing emissions to LPs
    }
    

## Anti-Patterns


---
  #### **Name**
High TGE Unlock
  #### **Description**
Large percentage unlocked at token generation
  #### **Why**
VCs and early holders dump immediately, killing momentum
  #### **Instead**
    // Bad: 25% TGE unlock
    TGE: 25% unlocked
    Result: Immediate dump, -80% from launch
    
    // Good: Minimal TGE
    TGE: 5% or less for investors
    Community airdrop: Can be higher if broad distribution
    Vesting: Start immediately after TGE
    

---
  #### **Name**
Linear Vesting Without Cliff
  #### **Description**
Tokens unlock from day 1 linearly
  #### **Why**
Allows constant selling, no commitment period
  #### **Instead**
    // Bad: No cliff
    Month 1: 2.5% unlocked
    Month 2: 5% unlocked
    // Allows selling from day 1
    
    // Good: 1 year cliff
    Month 1-12: 0% unlocked (cliff)
    Month 13: 25% unlocked (12 months accrued)
    Month 14-48: Linear vest remaining 75%
    

---
  #### **Name**
Unsustainable APY
  #### **Description**
Promising 1000%+ APY through emissions
  #### **Why**
Emissions dilute holders, APY drops, yield farmers leave
  #### **Instead**
    // Bad: 10,000% APY
    - Requires massive emissions
    - Dilutes non-stakers
    - Mercenary capital leaves when APY drops
    
    // Good: Sustainable yields
    - Real yield from protocol fees: 5-15%
    - Token emissions add 10-20%
    - Total: 15-35% APY
    - Emissions decrease over time
    

---
  #### **Name**
Complex Utility Without Demand
  #### **Description**
Designing elaborate token utility without real usage
  #### **Why**
Utility is meaningless if no one uses the protocol
  #### **Instead**
    // Bad: Complex utility
    - Stake to boost
    - Lock for governance
    - Burn for premium
    - Pay for features
    // But no users actually doing any of this
    
    // Good: Simple, essential utility
    - Token required to use protocol (fees)
    - Start with one clear use case
    - Add utility as demand grows
    

---
  #### **Name**
No Value Accrual Mechanism
  #### **Description**
Token captures no value from protocol success
  #### **Why**
Price has no fundamental support
  #### **Instead**
    // Bad: Governance only
    - Token only votes on proposals
    - No fees to holders
    - Value is pure speculation
    
    // Good: Value accrual
    Option 1: Fee sharing
    - 50% of fees to stakers
    Option 2: Buyback
    - Protocol buys tokens with revenue
    Option 3: Burn
    - Fees partially burned
    Option 4: Treasury growth
    - Revenue grows DAO treasury
    

---
  #### **Name**
Short Team Vesting
  #### **Description**
Team fully vested before protocol matures
  #### **Why**
Team can leave once vested, no long-term alignment
  #### **Instead**
    // Bad: 2 year vest
    - Team fully liquid after 2 years
    - Protocol still developing
    - Team incentives misaligned
    
    // Good: 4+ year vest with extensions
    - 1 year cliff
    - 4 year linear vest
    - Option to extend for additional allocation
    - Performance-based unlocks
    