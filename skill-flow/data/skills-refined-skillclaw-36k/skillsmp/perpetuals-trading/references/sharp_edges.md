# Perpetuals Trading - Sharp Edges

## Oracle Deviation Exploit

### **Id**
oracle-deviation-exploit
### **Summary**
Small oracle deviations enable profitable exploits
### **Severity**
critical
### **Situation**
  Your perp uses Chainlink for pricing. Chainlink updates on
  0.5% deviation. An attacker exploits the 0.5% gap between
  Chainlink and actual market price repeatedly.
  
### **Why**
  Chainlink and similar oracles update on threshold deviations
  to save gas. This creates small windows where the oracle
  price doesn't match the market, enabling MEV extraction.
  
### **Solution**
  # MULTI-ORACLE WITH DEVIATION CHECKS
  
  contract PerpOracle {
      IChainlinkAggregator public primaryOracle;
      IChainlinkAggregator public secondaryOracle;
      uint256 public constant MAX_DEVIATION = 0.005e18; // 0.5%
  
      function getPrice() public view returns (uint256) {
          uint256 primary = _getChainlinkPrice(primaryOracle);
          uint256 secondary = _getChainlinkPrice(secondaryOracle);
  
          // Check deviation between oracles
          uint256 deviation = _calculateDeviation(primary, secondary);
          require(deviation <= MAX_DEVIATION, "Price deviation too high");
  
          // Use median or average
          return (primary + secondary) / 2;
      }
  
      // Additional protections
      function validatePriceMovement(
          uint256 oldPrice,
          uint256 newPrice,
          uint256 maxMovementBps
      ) internal pure {
          uint256 movement = _calculateDeviation(oldPrice, newPrice);
          require(movement <= maxMovementBps, "Price moved too fast");
      }
  }
  
  GMX V2 Approach:
  - Primary: Chainlink price feeds
  - Secondary: Signed prices from off-chain oracles
  - Real-time signed prices for execution
  - Chainlink as fallback/validation
  
### **Symptoms**
  - Consistent small profits by sophisticated traders
  - Price differences vs CEX at trade time
  - MEV bots extracting value
### **Detection Pattern**
getLatestPrice(?!.*deviation|.*secondary)

## Funding Manipulation

### **Id**
funding-manipulation
### **Summary**
Open interest manipulation to farm funding
### **Severity**
high
### **Situation**
  Large trader opens massive long position, pushing funding
  rate negative. They hold offsetting short on another platform,
  collecting funding as the "minority side."
  
### **Why**
  Funding rates are designed to balance longs and shorts.
  But if one party can dominate open interest, they control
  the funding rate and can farm it from the other side.
  
### **Solution**
  # CAP POSITION SIZE AND RATE
  
  contract FundingProtection {
      uint256 public constant MAX_POSITION_SHARE = 0.1e18; // 10% of OI
  
      function openPosition(int256 size) external {
          int256 totalOI = longOI + shortOI;
          int256 newPositionShare = (abs(size) * 1e18) / totalOI;
  
          require(
              newPositionShare <= MAX_POSITION_SHARE,
              "Position too large"
          );
  
          // Also cap funding rate
          require(
              abs(currentFundingRate) <= MAX_FUNDING_RATE,
              "Funding rate capped"
          );
      }
  
      // Time-weighted funding to prevent gaming
      function calculateFunding() public view returns (int256) {
          // Use TWAP of OI imbalance, not instant
          return fundingRateTWAP;
      }
  }
  
  Additional Measures:
  - Delay funding rate changes
  - Use time-weighted average OI
  - Cap maximum funding rate
  - Monitor for correlated positions across platforms
  
### **Symptoms**
  - Extreme funding rates (>0.5% per 8h)
  - Single address dominating one side
  - Coordinated positions across venues
### **Detection Pattern**


## Liquidation Cascade

### **Id**
liquidation-cascade
### **Summary**
Mass liquidations cause cascading price impact
### **Severity**
critical
### **Situation**
  Price drops 10%. Leveraged longs get liquidated. Liquidations
  push price down further. More liquidations trigger. Cascade
  continues until pool is drained.
  
### **Why**
  Liquidations sell into the market. In thin liquidity or AMM
  pools, this creates price impact. Price impact triggers more
  liquidations. This feedback loop is the "cascade."
  
### **Solution**
  # GRADUAL LIQUIDATION AND BACKSTOPS
  
  contract GradualLiquidation {
      uint256 public constant PARTIAL_LIQ_RATIO = 0.25e18; // 25%
      uint256 public constant CIRCUIT_BREAKER = 0.05e18;   // 5% drop
      uint256 public priceAtIntervalStart;
      bool public circuitBreakerActive;
  
      function liquidate(address trader) external {
          require(!circuitBreakerActive, "Market halted");
  
          Position storage pos = positions[trader];
  
          // Partial liquidation - only close 25%
          uint256 closeSize = (pos.size * PARTIAL_LIQ_RATIO) / 1e18;
  
          // Check price impact
          uint256 impact = calculatePriceImpact(closeSize);
          require(impact <= MAX_IMPACT, "Impact too high");
  
          // Close partial position
          _closePosition(trader, closeSize);
  
          // If still underwater, schedule next partial
          if (isLiquidatable(trader)) {
              scheduledLiquidations[trader] = block.timestamp + 1 minutes;
          }
      }
  
      // Circuit breaker for extreme moves
      function checkCircuitBreaker() internal {
          if (block.timestamp >= intervalEnd) {
              priceAtIntervalStart = currentPrice;
              intervalEnd = block.timestamp + 1 hours;
          }
  
          uint256 movement = _deviation(currentPrice, priceAtIntervalStart);
          if (movement >= CIRCUIT_BREAKER) {
              circuitBreakerActive = true;
              emit CircuitBreaker(currentPrice, movement);
          }
      }
  }
  
  Additional Protections:
  - ADL (Auto-Deleveraging) before insurance fund
  - Reduce max leverage during high volatility
  - Dynamic maintenance margin
  - Cross-margin to share collateral
  
### **Symptoms**
  - Price drops much further than spot
  - Cascade of liquidation events
  - Insurance fund depleted
### **Detection Pattern**


## Bad Debt Socialization

### **Id**
bad-debt-socialization
### **Summary**
Bad debt distributed to winning traders
### **Severity**
high
### **Situation**
  Large position gets liquidated underwater. Insurance fund
  is empty. Protocol socializes losses by reducing winning
  traders' profits proportionally.
  
### **Why**
  When a position is liquidated with negative equity (bad debt),
  someone must absorb the loss. If insurance fund is depleted,
  protocols often socialize losses to remain solvent.
  
### **Solution**
  # TIERED LOSS ABSORPTION
  
  Loss Absorption Waterfall:
  1. Trader's remaining collateral
  2. Liquidation penalty (paid to liquidator)
  3. Insurance fund
  4. ADL (Auto-Deleveraging) most profitable positions
  5. Socialization (last resort)
  
  contract InsuranceFund {
      uint256 public fundBalance;
      uint256 public constant MIN_FUND_RATIO = 0.02e18; // 2% of OI
  
      function absorbBadDebt(uint256 debt) external onlyLiquidationEngine {
          if (fundBalance >= debt) {
              fundBalance -= debt;
              return;
          }
  
          // Partial coverage
          uint256 covered = fundBalance;
          fundBalance = 0;
          uint256 uncovered = debt - covered;
  
          // ADL before socialization
          _autoDeleverage(uncovered);
      }
  
      function _autoDeleverage(uint256 amount) internal {
          // Find most profitable positions on opposite side
          // Force-close them at current price
          // They take the loss instead of everyone
      }
  }
  
  ADL Ranking:
  - Profit ratio = PnL / Position Size
  - Higher profit ratio = first to be ADL'd
  - Fairer than random socialization
  
### **Symptoms**
  - Winning trades receive less than expected
  - Unexpected position closures
  - Insurance fund at zero
### **Detection Pattern**


## Stale Position Interest

### **Id**
stale-position-interest
### **Summary**
Abandoned positions accumulate unbounded fees
### **Severity**
medium
### **Situation**
  Trader opens small position and forgets about it. Borrow fees
  accumulate for months. When finally liquidated, the position
  owes more than the entire protocol's insurance fund.
  
### **Why**
  Borrow fees compound over time. A position can technically
  owe infinite fees if never closed or liquidated. This creates
  accounting problems and bad debt risk.
  
### **Solution**
  # CAP ACCUMULATED FEES
  
  contract FeeManagement {
      uint256 public constant MAX_FEE_RATIO = 0.95e18; // 95% of collateral
  
      function updatePosition(address trader) public {
          Position storage pos = positions[trader];
  
          uint256 accumulatedFees = calculateAccumulatedFees(pos);
  
          // Cap fees at percentage of collateral
          uint256 maxFees = (pos.collateral * MAX_FEE_RATIO) / 1e18;
          if (accumulatedFees > maxFees) {
              accumulatedFees = maxFees;
              // Auto-liquidate when fees hit cap
              _liquidate(trader);
          }
  
          pos.accruedFees = accumulatedFees;
      }
  
      // Also implement position expiry
      uint256 public constant MAX_POSITION_AGE = 365 days;
  
      function checkPositionAge(address trader) internal {
          Position storage pos = positions[trader];
          if (block.timestamp > pos.openTime + MAX_POSITION_AGE) {
              _forceClose(trader);
          }
      }
  }
  
### **Symptoms**
  - Ancient positions in system
  - Fees exceeding collateral on paper
  - Accounting discrepancies
### **Detection Pattern**


## Cross Margin Contagion

### **Id**
cross-margin-contagion
### **Summary**
One bad position drains all cross-margin collateral
### **Severity**
high
### **Situation**
  Trader has 10 positions in cross-margin mode. One position
  goes heavily underwater. The system uses collateral from
  other profitable positions, liquidating everything.
  
### **Why**
  Cross-margin shares collateral across positions. A single
  large loss can consume collateral meant for other positions,
  triggering cascading liquidations of the entire account.
  
### **Solution**
  # ISOLATED MARGIN OPTION + RISK LIMITS
  
  contract MarginModes {
      enum MarginMode { Isolated, Cross }
  
      struct Account {
          MarginMode mode;
          uint256 totalCollateral;
          mapping(bytes32 => Position) positions;
      }
  
      function openPositionIsolated(
          bytes32 market,
          uint256 collateral,
          int256 size
      ) external {
          // Collateral locked to this position only
          positions[market].isolatedCollateral = collateral;
          positions[market].size = size;
  
          // Max loss = this collateral, not entire account
      }
  
      function openPositionCross(
          bytes32 market,
          int256 size
      ) external {
          require(account.mode == MarginMode.Cross);
  
          // Uses shared collateral
          // But set individual position loss limits
          positions[market].maxLoss = account.totalCollateral / 4;
      }
  
      // Force close before one position drains everything
      function checkPositionLimit(address trader, bytes32 market) internal {
          int256 pnl = calculatePnL(trader, market);
          if (pnl < -int256(positions[market].maxLoss)) {
              _forceClose(trader, market);
          }
      }
  }
  
### **Symptoms**
  - Entire account liquidated from one position
  - Profitable positions closed unexpectedly
  - Rapid account value decline
### **Detection Pattern**
