# Token Launch Engineer

## Patterns


---
  #### **Id**
standard-vesting-contract
  #### **Name**
Linear Vesting with Cliff
  #### **Description**
    Industry-standard vesting pattern with initial cliff period followed
    by linear token release
    
  #### **When To Use**
    - Team token allocations (4-year vesting, 1-year cliff)
    - Investor allocations (2-3 year vesting, 6-12 month cliff)
    - Advisor tokens (2-year vesting, 6-month cliff)
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
    import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
    import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
    import "@openzeppelin/contracts/access/Ownable.sol";
    
    contract TokenVesting is ReentrancyGuard, Ownable {
        using SafeERC20 for IERC20;
    
        struct VestingSchedule {
            uint256 totalAmount;
            uint256 released;
            uint256 startTime;
            uint256 cliffDuration;
            uint256 vestingDuration;
            bool revocable;
            bool revoked;
        }
    
        IERC20 public immutable token;
        mapping(address => VestingSchedule) public vestingSchedules;
    
        event TokensReleased(address indexed beneficiary, uint256 amount);
        event VestingRevoked(address indexed beneficiary, uint256 returnedAmount);
    
        constructor(address _token) Ownable(msg.sender) {
            require(_token != address(0), "Invalid token address");
            token = IERC20(_token);
        }
    
        function createVestingSchedule(
            address beneficiary,
            uint256 totalAmount,
            uint256 startTime,
            uint256 cliffDuration,
            uint256 vestingDuration,
            bool revocable
        ) external onlyOwner {
            require(vestingSchedules[beneficiary].totalAmount == 0, "Schedule exists");
            require(totalAmount > 0, "Amount must be > 0");
            require(vestingDuration > cliffDuration, "Vesting must exceed cliff");
    
            token.safeTransferFrom(msg.sender, address(this), totalAmount);
    
            vestingSchedules[beneficiary] = VestingSchedule({
                totalAmount: totalAmount,
                released: 0,
                startTime: startTime,
                cliffDuration: cliffDuration,
                vestingDuration: vestingDuration,
                revocable: revocable,
                revoked: false
            });
        }
    
        function release() external nonReentrant {
            VestingSchedule storage schedule = vestingSchedules[msg.sender];
            require(schedule.totalAmount > 0, "No vesting schedule");
            require(!schedule.revoked, "Vesting revoked");
    
            uint256 releasable = _computeReleasableAmount(schedule);
            require(releasable > 0, "No tokens to release");
    
            schedule.released += releasable;
            token.safeTransfer(msg.sender, releasable);
    
            emit TokensReleased(msg.sender, releasable);
        }
    
        function _computeReleasableAmount(VestingSchedule memory schedule)
            internal view returns (uint256)
        {
            if (block.timestamp < schedule.startTime + schedule.cliffDuration) {
                return 0;
            }
    
            uint256 elapsed = block.timestamp - schedule.startTime;
            if (elapsed >= schedule.vestingDuration) {
                return schedule.totalAmount - schedule.released;
            }
    
            uint256 vested = (schedule.totalAmount * elapsed) / schedule.vestingDuration;
            return vested - schedule.released;
        }
    }
    
  #### **Security Notes**
    - Use SafeERC20 for all token transfers
    - Implement ReentrancyGuard on release functions
    - Validate all time parameters
    - Consider emergency pause functionality

---
  #### **Id**
fair-launch-anti-bot
  #### **Name**
Fair Launch with Anti-Bot Protection
  #### **Description**
    Launch mechanism that prevents bot frontrunning and ensures fair
    distribution to real participants
    
  #### **When To Use**
    - Public token sales
    - DEX liquidity provision
    - Community-focused launches
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    contract FairLaunch {
        uint256 public constant MAX_TX_AMOUNT = 1 ether; // Per-tx limit
        uint256 public constant COOLDOWN_BLOCKS = 3;
        uint256 public launchBlock;
        bool public tradingEnabled;
    
        mapping(address => uint256) public lastBuyBlock;
        mapping(address => bool) public isWhitelisted;
        mapping(address => bool) public isBlacklisted;
    
        modifier antiBot(address from, address to, uint256 amount) {
            if (!isWhitelisted[from] && !isWhitelisted[to]) {
                require(!isBlacklisted[from] && !isBlacklisted[to], "Blacklisted");
    
                // Block 0-2: Only whitelisted (prevents sandwich attacks at launch)
                if (block.number <= launchBlock + 2) {
                    revert("Trading not yet enabled");
                }
    
                // Block 3-10: Per-transaction limits
                if (block.number <= launchBlock + 10) {
                    require(amount <= MAX_TX_AMOUNT, "Exceeds max tx");
                }
    
                // Cooldown between buys (prevents rapid accumulation)
                require(
                    block.number >= lastBuyBlock[to] + COOLDOWN_BLOCKS,
                    "Cooldown active"
                );
                lastBuyBlock[to] = block.number;
            }
            _;
        }
    
        function enableTrading() external onlyOwner {
            require(!tradingEnabled, "Already enabled");
            tradingEnabled = true;
            launchBlock = block.number;
        }
    }
    
  #### **Security Notes**
    - Deploy and add liquidity in same transaction to prevent sniping
    - Consider using private mempool (Flashbots) for launch tx
    - Set reasonable per-wallet limits during initial period

---
  #### **Id**
tokenomics-allocation
  #### **Name**
Sustainable Tokenomics Template
  #### **Description**
    Battle-tested token allocation framework based on successful launches
    
  #### **When To Use**
    - Designing new token economics
    - Reviewing existing allocations
    - Planning token distribution
  #### **Implementation**
    Recommended Token Allocation (1B total supply):
    
    ┌─────────────────────────┬─────────┬────────────────────────────────┐
    │ Category                │ %       │ Vesting                        │
    ├─────────────────────────┼─────────┼────────────────────────────────┤
    │ Community/Ecosystem     │ 35-45%  │ Ongoing distribution           │
    │ Treasury/DAO            │ 20-25%  │ Governance controlled          │
    │ Team                    │ 15-20%  │ 4yr vest, 1yr cliff            │
    │ Investors (Seed+Private)│ 12-18%  │ 2-3yr vest, 6-12mo cliff       │
    │ Public Sale             │ 5-10%   │ 0-25% TGE, rest 6-12mo vest    │
    │ Advisors                │ 2-5%    │ 2yr vest, 6mo cliff            │
    │ Liquidity               │ 5-10%   │ Locked in DEX                  │
    └─────────────────────────┴─────────┴────────────────────────────────┘
    
    TGE Unlock Best Practices:
    - Public sale: 10-25% at TGE (higher for smaller allocations)
    - Private investors: 0-10% at TGE
    - Team: 0% at TGE (never unlock team tokens at launch)
    - Ecosystem: Release as needed for growth
    
    Red Flags to Avoid:
    ❌ Team allocation > 25%
    ❌ No cliff for investors/team
    ❌ > 50% TGE unlock for any group
    ❌ Concentrated whale wallets > 5% each
    ❌ Unlocks creating > 10% supply increase at once
    
  #### **Security Notes**
    - Ensure all allocations are verifiable on-chain
    - Use multi-sig for team/treasury wallets
    - Consider token lockup transparency dashboards

---
  #### **Id**
liquidity-bootstrapping
  #### **Name**
Liquidity Bootstrapping Pool (LBP)
  #### **Description**
    Fair price discovery mechanism using Balancer-style weighted pools
    that shift weights over time
    
  #### **When To Use**
    - Projects wanting fair price discovery
    - Avoiding large initial dumps
    - When seeking wide token distribution
  #### **Implementation**
    LBP Configuration (Balancer V2):
    
    // Initial weights: 96% PROJECT / 4% USDC
    // Final weights: 50% PROJECT / 50% USDC
    // Duration: 24-72 hours
    
    Key Parameters:
    - Start weight: 90-96% project token
    - End weight: 50% project token
    - Duration: 24-72 hours (longer = more gradual)
    - Swap fee: 0.5-2%
    
    Price Dynamics:
    - Price starts HIGH (discourages immediate dumps)
    - Price decreases as weights shift
    - Buyers wait for acceptable entry
    - Natural price discovery occurs
    
    Anti-Gaming Measures:
    - No withdrawals during LBP
    - Swap fee accumulates to project
    - Random end time (not publicized)
    - Rate limiting on swaps
    
  #### **Security Notes**
    - Lock all project tokens for LBP duration
    - Use Balancer's official LBP factory
    - Consider pausing capability for emergencies

## Anti-Patterns


---
  #### **Id**
unlock-cliff-too-short
  #### **Name**
Insufficient Vesting Cliff
  #### **Severity**
high
  #### **Description**
    Team or investor tokens with cliffs under 6 months create immediate
    sell pressure and signal lack of commitment
    
  #### **Detection**
    Watch for:
    - Team cliff < 12 months
    - Investor cliff < 6 months
    - "TGE unlock" > 20% for non-public rounds
    
  #### **Consequence**
    Early unlocks lead to price dumps, community distrust, and
    potential securities law violations
    

---
  #### **Id**
whale-concentration
  #### **Name**
Excessive Wallet Concentration
  #### **Severity**
high
  #### **Description**
    Single wallets holding > 5% of supply create manipulation risk
    and governance centralization
    
  #### **Detection**
    Check token distribution:
    - Any non-contract wallet > 5% supply
    - Top 10 wallets > 50% combined
    - Hidden multi-wallet concentration
    
  #### **Consequence**
    Price manipulation, governance attacks, rug pull risk
    

---
  #### **Id**
no-liquidity-lock
  #### **Name**
Unlocked DEX Liquidity
  #### **Severity**
critical
  #### **Description**
    DEX liquidity not locked can be pulled, rugging all holders
    
  #### **Detection**
    Verify on lock services:
    - Unicrypt, Team Finance, PinkSale locks
    - Minimum 6-12 month lock period
    - Multi-sig for early unlock
    
  #### **Consequence**
    Complete loss of trading liquidity, price collapse to zero
    