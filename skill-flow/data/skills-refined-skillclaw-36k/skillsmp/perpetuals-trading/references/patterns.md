# Perpetuals Trading Engineer

## Patterns


---
  #### **Id**
funding-rate-mechanism
  #### **Name**
Funding Rate Calculation
  #### **Description**
    Mechanism to keep perpetual price aligned with spot price
    by transferring payments between longs and shorts
    
  #### **When To Use**
    - Building perpetual DEX protocol
    - Integrating with perps for hedging
    - Funding rate arbitrage strategies
  #### **Implementation**
    Funding Rate Components:
    
    ┌─────────────────────────────────────────────────────────────┐
    │ FUNDING RATE = Interest Rate + Premium Index                │
    ├─────────────────────────────────────────────────────────────┤
    │ Interest Rate: Cost of holding position (typically ~0.03%) │
    │ Premium Index: (Mark Price - Index Price) / Index Price     │
    └─────────────────────────────────────────────────────────────┘
    
    // Simplified funding rate calculation
    contract FundingRate {
        int256 public constant FUNDING_INTERVAL = 8 hours;
        int256 public constant MAX_FUNDING_RATE = 0.01e18; // 1% per interval
    
        struct Market {
            int256 longOpenInterest;
            int256 shortOpenInterest;
            int256 lastFundingRate;
            uint256 lastFundingTime;
        }
    
        function calculateFundingRate(
            int256 markPrice,
            int256 indexPrice,
            Market memory market
        ) public pure returns (int256) {
            // Premium = (Mark - Index) / Index
            int256 premium = ((markPrice - indexPrice) * 1e18) / indexPrice;
    
            // Clamp to max funding rate
            if (premium > MAX_FUNDING_RATE) {
                return MAX_FUNDING_RATE;
            } else if (premium < -MAX_FUNDING_RATE) {
                return -MAX_FUNDING_RATE;
            }
    
            // Adjust for open interest imbalance
            int256 imbalance = market.longOpenInterest - market.shortOpenInterest;
            int256 totalOI = market.longOpenInterest + market.shortOpenInterest;
    
            if (totalOI > 0) {
                int256 imbalanceFactor = (imbalance * 1e18) / totalOI;
                premium = (premium + imbalanceFactor) / 2;
            }
    
            return premium;
        }
    }
    
    Funding Payment:
    - If rate positive: Longs pay shorts
    - If rate negative: Shorts pay longs
    - Payment = Position Size × Funding Rate
    - Typically every 8 hours
    
  #### **Security Notes**
    - Oracle manipulation can exploit funding
    - Cap funding rates to prevent extremes
    - Time-weight to prevent gaming

---
  #### **Id**
liquidation-engine
  #### **Name**
Liquidation Engine Design
  #### **Description**
    System to close undercollateralized positions before
    protocol takes losses from bad debt
    
  #### **When To Use**
    - Building leverage trading protocol
    - Risk management systems
    - Liquidator bot development
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    contract LiquidationEngine {
        uint256 public constant MAINTENANCE_MARGIN = 0.05e18; // 5%
        uint256 public constant LIQUIDATION_FEE = 0.005e18;   // 0.5%
        uint256 public constant LIQUIDATOR_REWARD = 0.0025e18; // 0.25%
    
        struct Position {
            int256 size;       // Positive = long, negative = short
            uint256 collateral;
            uint256 entryPrice;
            uint256 lastFundingIndex;
        }
    
        mapping(address => mapping(bytes32 => Position)) public positions;
    
        function isLiquidatable(
            address trader,
            bytes32 market,
            uint256 markPrice
        ) public view returns (bool) {
            Position memory pos = positions[trader][market];
            if (pos.size == 0) return false;
    
            int256 pnl = calculatePnL(pos, markPrice);
            int256 equity = int256(pos.collateral) + pnl;
            uint256 positionValue = abs(pos.size) * markPrice / 1e18;
            uint256 maintenanceRequired = positionValue * MAINTENANCE_MARGIN / 1e18;
    
            return equity < int256(maintenanceRequired);
        }
    
        function liquidate(
            address trader,
            bytes32 market,
            uint256 markPrice
        ) external {
            require(isLiquidatable(trader, market, markPrice), "Not liquidatable");
    
            Position storage pos = positions[trader][market];
            uint256 positionValue = abs(pos.size) * markPrice / 1e18;
    
            // Calculate fees
            uint256 liquidationFee = positionValue * LIQUIDATION_FEE / 1e18;
            uint256 liquidatorReward = positionValue * LIQUIDATOR_REWARD / 1e18;
    
            // Close position
            int256 pnl = calculatePnL(pos, markPrice);
            int256 remainingCollateral = int256(pos.collateral) + pnl
                - int256(liquidationFee);
    
            // Pay liquidator
            if (remainingCollateral > int256(liquidatorReward)) {
                _transferReward(msg.sender, liquidatorReward);
                remainingCollateral -= int256(liquidatorReward);
            }
    
            // Handle any remaining collateral or bad debt
            if (remainingCollateral > 0) {
                _transferCollateral(trader, uint256(remainingCollateral));
            } else {
                // Bad debt absorbed by insurance fund
                _absorbBadDebt(uint256(-remainingCollateral));
            }
    
            delete positions[trader][market];
        }
    
        function calculatePnL(Position memory pos, uint256 markPrice)
            internal pure returns (int256)
        {
            int256 priceDelta = int256(markPrice) - int256(pos.entryPrice);
            return (pos.size * priceDelta) / int256(pos.entryPrice);
        }
    
        function abs(int256 x) internal pure returns (uint256) {
            return x >= 0 ? uint256(x) : uint256(-x);
        }
    }
    
    Liquidation Parameters by Market:
    ┌─────────────────┬──────────────────┬──────────────────┐
    │ Market          │ Maint. Margin    │ Liq. Threshold   │
    ├─────────────────┼──────────────────┼──────────────────┤
    │ BTC/USD         │ 0.5%             │ 0.4%             │
    │ ETH/USD         │ 0.5%             │ 0.4%             │
    │ Altcoins        │ 2.5%             │ 2.0%             │
    │ Memecoins       │ 5.0%             │ 4.0%             │
    └─────────────────┴──────────────────┴──────────────────┘
    
  #### **Security Notes**
    - Use reliable oracle with manipulation resistance
    - Insurance fund for bad debt scenarios
    - Incremental liquidation for large positions

---
  #### **Id**
gmx-style-amm
  #### **Name**
GMX-Style Liquidity Pool
  #### **Description**
    Zero-slippage perpetuals AMM using liquidity pool as
    counterparty to all trades
    
  #### **When To Use**
    - Building perpetuals without orderbook
    - Seeking zero-slippage execution
    - Pool-based leverage trading
  #### **Implementation**
    GMX Architecture:
    
    ┌─────────────────────────────────────────────────────────────┐
    │                      GLP/GM Pool                            │
    │  ┌─────────────────────────────────────────────────────────┐│
    │  │ Assets: ETH, BTC, USDC, USDT, DAI, etc.                ││
    │  │ Value: ~$500M+ (varies by chain)                       ││
    │  └─────────────────────────────────────────────────────────┘│
    │                          │                                  │
    │              ┌───────────┴───────────┐                      │
    │              ▼                       ▼                      │
    │    [Traders open positions]    [LPs earn fees]              │
    │    - Zero slippage at oracle   - 70% of trading fees       │
    │    - Pool is counterparty      - Bear PnL risk             │
    │    - Funding to LPs            - Funding payments          │
    └─────────────────────────────────────────────────────────────┘
    
    Key Components:
    - Oracle-based pricing (Chainlink + secondary)
    - Position fees: 0.1% open/close
    - Borrow fee: Hourly rate based on utilization
    - Funding: Paid to LPs when open interest imbalanced
    
    // Simplified position opening
    function openPosition(
        address collateralToken,
        uint256 collateralAmount,
        address indexToken,    // Token being traded
        uint256 sizeDelta,     // Position size increase
        bool isLong
    ) external {
        // Oracle price for execution
        uint256 price = oracle.getPrice(indexToken, isLong);
    
        // Validate leverage
        uint256 leverage = (sizeDelta * 1e18) / collateralAmount;
        require(leverage <= MAX_LEVERAGE, "Leverage too high");
    
        // Update pool reserved amounts
        if (isLong) {
            reservedAmounts[indexToken] += sizeDelta;
        } else {
            reservedAmounts[collateralToken] += sizeDelta;
        }
    
        // Collect fees
        uint256 fee = (sizeDelta * POSITION_FEE) / 1e18;
        _collectFees(fee);
    
        // Create/update position
        positions[msg.sender].size += sizeDelta;
        // ...
    }
    
  #### **Security Notes**
    - Oracle manipulation is primary risk
    - Cap open interest relative to pool size
    - Dynamic fees based on utilization

## Anti-Patterns


---
  #### **Id**
single-oracle
  #### **Name**
Single Oracle Dependency
  #### **Severity**
critical
  #### **Description**
    Relying on single oracle for mark price allows manipulation
    leading to unfair liquidations or exploits
    
  #### **Detection**
    - Only Chainlink, no secondary
    - No deviation checks
    - No circuit breakers
    
  #### **Consequence**
    Oracle manipulation causes mass liquidations or
    allows attackers to exploit price discrepancies
    

---
  #### **Id**
no-oi-caps
  #### **Name**
No Open Interest Caps
  #### **Severity**
high
  #### **Description**
    Unlimited open interest relative to liquidity creates
    situations where pool cannot cover payouts
    
  #### **Detection**
    - reservedAmounts can exceed pool value
    - No utilization limits
    
  #### **Consequence**
    Winning traders cannot withdraw, protocol insolvency
    

---
  #### **Id**
instant-liquidation
  #### **Name**
Immediate Liquidation Without Buffer
  #### **Severity**
medium
  #### **Description**
    Liquidating at exact maintenance margin allows
    MEV bots to sandwich-attack near-threshold positions
    
  #### **Detection**
    - Liquidation threshold equals maintenance margin
    - No partial liquidation
    
  #### **Consequence**
    Traders unfairly liquidated by MEV manipulation
    