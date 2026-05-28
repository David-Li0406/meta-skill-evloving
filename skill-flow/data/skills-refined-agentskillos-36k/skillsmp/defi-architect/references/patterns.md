# DeFi Architect

## Patterns


---
  #### **Name**
AMM Design
  #### **Description**
Automated market maker mechanics
  #### **When**
Building DEX or liquidity pools
  #### **Example**
    // Constant Product AMM (Uniswap v2 style)
    // x * y = k
    
    interface IAMM {
        function swap(
            address tokenIn,
            address tokenOut,
            uint256 amountIn,
            uint256 minAmountOut
        ) external returns (uint256 amountOut);
    }
    
    contract ConstantProductAMM {
        IERC20 public immutable token0;
        IERC20 public immutable token1;
    
        uint256 public reserve0;
        uint256 public reserve1;
    
        uint256 public constant FEE_BPS = 30;  // 0.3%
    
        function getAmountOut(
            uint256 amountIn,
            uint256 reserveIn,
            uint256 reserveOut
        ) public pure returns (uint256) {
            // Fee applied to input
            uint256 amountInWithFee = amountIn * (10000 - FEE_BPS);
    
            // Constant product formula
            // (reserveIn + amountIn) * (reserveOut - amountOut) = k
            // amountOut = reserveOut - k / (reserveIn + amountIn)
            // amountOut = (amountIn * reserveOut) / (reserveIn + amountIn)
    
            uint256 numerator = amountInWithFee * reserveOut;
            uint256 denominator = (reserveIn * 10000) + amountInWithFee;
    
            return numerator / denominator;
        }
    
        // Impermanent Loss Calculation
        // If price ratio changes from P0 to P1:
        // IL = 2 * sqrt(P1/P0) / (1 + P1/P0) - 1
        //
        // Example: 2x price increase
        // IL = 2 * sqrt(2) / (1 + 2) - 1 = 2 * 1.414 / 3 - 1 = -5.7%
        //
        // LPs lose 5.7% compared to just holding
    }
    

---
  #### **Name**
Lending Protocol Design
  #### **Description**
Over-collateralized lending mechanics
  #### **When**
Building lending/borrowing protocols
  #### **Example**
    // Core lending mechanics
    
    struct Market {
        IERC20 asset;
        uint256 totalDeposits;
        uint256 totalBorrows;
        uint256 collateralFactor;  // e.g., 75% = 7500
        uint256 liquidationThreshold;  // e.g., 80% = 8000
        uint256 liquidationBonus;  // e.g., 5% = 500
    }
    
    // Interest Rate Model (Compound style)
    function getBorrowRate(
        uint256 utilization  // totalBorrows / totalDeposits
    ) public pure returns (uint256) {
        uint256 kink = 8000;  // 80% utilization
        uint256 baseRate = 200;  // 2% base
        uint256 multiplierPerYear = 1000;  // 10% at kink
        uint256 jumpMultiplier = 10000;  // 100% above kink
    
        if (utilization <= kink) {
            return baseRate + (utilization * multiplierPerYear / 10000);
        } else {
            uint256 normalRate = baseRate + (kink * multiplierPerYear / 10000);
            uint256 excessUtil = utilization - kink;
            return normalRate + (excessUtil * jumpMultiplier / 10000);
        }
    }
    
    // Health Factor Calculation
    // healthFactor = (collateralValue * liquidationThreshold) / borrowValue
    // liquidatable if healthFactor < 1
    
    function isLiquidatable(address user) public view returns (bool) {
        uint256 collateralValue = getCollateralValue(user);
        uint256 borrowValue = getBorrowValue(user);
    
        // Health factor with 18 decimals
        uint256 healthFactor = (collateralValue * liquidationThreshold * 1e18)
            / (borrowValue * 10000);
    
        return healthFactor < 1e18;
    }
    

---
  #### **Name**
Oracle Integration
  #### **Description**
Secure price feed integration
  #### **When**
Using external price data
  #### **Example**
    // NEVER trust a single oracle source
    
    interface IPriceOracle {
        function getPrice(address token) external view returns (uint256);
    }
    
    contract SecureOracleAggregator {
        IPriceOracle public immutable chainlink;
        IPriceOracle public immutable uniswapTWAP;
        IPriceOracle public immutable backup;
    
        uint256 public constant MAX_DEVIATION = 500;  // 5%
        uint256 public constant STALE_THRESHOLD = 1 hours;
    
        error StalePrice();
        error PriceDeviation();
    
        function getPrice(address token) external view returns (uint256) {
            // Primary: Chainlink
            (uint256 chainlinkPrice, uint256 timestamp) =
                getChainlinkPrice(token);
    
            // Check staleness
            if (block.timestamp - timestamp > STALE_THRESHOLD) {
                revert StalePrice();
            }
    
            // Secondary: TWAP for validation
            uint256 twapPrice = uniswapTWAP.getPrice(token);
    
            // Check deviation between sources
            uint256 deviation = chainlinkPrice > twapPrice
                ? (chainlinkPrice - twapPrice) * 10000 / chainlinkPrice
                : (twapPrice - chainlinkPrice) * 10000 / twapPrice;
    
            if (deviation > MAX_DEVIATION) {
                // Use more conservative price when sources disagree
                return chainlinkPrice < twapPrice ? chainlinkPrice : twapPrice;
            }
    
            return chainlinkPrice;
        }
    
        // TWAP implementation for manipulation resistance
        // Price = sum(price_i * time_i) / sum(time_i)
        // Longer time windows = harder to manipulate
    }
    

---
  #### **Name**
Yield Optimization
  #### **Description**
Sustainable yield generation
  #### **When**
Designing yield products
  #### **Example**
    // Yield sources (most to least sustainable):
    
    // 1. Trading fees (sustainable)
    // - DEX LPs earn from swap fees
    // - 0.3% per trade, distributed pro-rata
    
    // 2. Interest from borrowers (sustainable)
    // - Lenders earn from borrower interest
    // - Market-driven rates
    
    // 3. Protocol revenue share (sustainable if protocol profitable)
    // - Share of actual protocol revenue
    
    // 4. Token emissions (NOT sustainable long-term)
    // - Protocol pays in own token
    // - Requires constant buy pressure
    
    // Yield calculation example
    contract YieldVault {
        uint256 public totalAssets;
        uint256 public totalShares;
    
        // Real yield from strategy
        function harvest() external returns (uint256 profit) {
            uint256 before = underlying.balanceOf(address(this));
    
            // Collect trading fees, interest, etc.
            strategy.harvest();
    
            uint256 after = underlying.balanceOf(address(this));
            profit = after - before;
    
            // Performance fee to protocol
            uint256 fee = profit * performanceFee / 10000;
            _mint(treasury, fee * totalShares / totalAssets);
    
            totalAssets = after - fee;
        }
    
        // APY = (endValue / startValue) ^ (365 / days) - 1
        function getAPY() external view returns (uint256) {
            // Calculate based on historical performance
            // NOT projected token emissions
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Single Oracle Source
  #### **Description**
Relying on one price feed
  #### **Why**
Oracle manipulation, downtime, stale prices
  #### **Instead**
Multiple sources with deviation checks

---
  #### **Name**
Unsustainable Yields
  #### **Description**
Promising yields from token emissions only
  #### **Why**
Ponzi dynamics, death spiral when emissions reduce
  #### **Instead**
Real yield from protocol revenue

---
  #### **Name**
Unbounded Liquidations
  #### **Description**
No limits on liquidation during crisis
  #### **Why**
Can cascade, drain protocol, create bad debt
  #### **Instead**
Partial liquidations, caps, circuit breakers

---
  #### **Name**
Flash Loan Vulnerable Design
  #### **Description**
State that can be manipulated atomically
  #### **Why**
Governance attacks, price manipulation, drains
  #### **Instead**
Time locks, TWAP oracles, snapshot voting

---
  #### **Name**
Hardcoded Parameters
  #### **Description**
Fixed rates, thresholds in code
  #### **Why**
Can't adapt to market conditions
  #### **Instead**
Governance-controlled parameters with bounds