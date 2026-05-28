# Onchain Analytics Engineer

## Patterns


---
  #### **Id**
dune-decoded-tables
  #### **Name**
Using Dune Decoded Tables
  #### **Description**
    Query decoded smart contract events and function calls
    for human-readable blockchain data
    
  #### **When To Use**
    - Analyzing specific protocol activity
    - Tracking token transfers
    - Monitoring contract interactions
  #### **Implementation**
    -- Dune SQL (Trino-based)
    
    -- Find all Uniswap V3 swaps for a token
    SELECT
      block_time,
      tx_hash,
      "from" as swapper,
      amount0 / 1e18 as token0_amount,
      amount1 / 1e6 as token1_amount,
      sqrt_price_x96
    FROM uniswap_v3_ethereum.Pair_evt_Swap
    WHERE contract_address = 0x... -- Pool address
      AND block_time >= NOW() - INTERVAL '7' DAY
    ORDER BY block_time DESC
    LIMIT 100
    
    -- Track protocol TVL over time
    SELECT
      date_trunc('day', block_time) as day,
      SUM(amount_usd) as daily_deposits,
      SUM(SUM(amount_usd)) OVER (ORDER BY date_trunc('day', block_time)) as cumulative_tvl
    FROM protocol_ethereum.Pool_evt_Deposit
    WHERE block_time >= NOW() - INTERVAL '30' DAY
    GROUP BY 1
    ORDER BY 1
    
    -- Cross-chain analysis
    SELECT
      blockchain,
      COUNT(*) as tx_count,
      SUM(amount_usd) as volume_usd
    FROM (
      SELECT 'ethereum' as blockchain, amount_usd FROM protocol_ethereum.swaps
      UNION ALL
      SELECT 'arbitrum' as blockchain, amount_usd FROM protocol_arbitrum.swaps
      UNION ALL
      SELECT 'polygon' as blockchain, amount_usd FROM protocol_polygon.swaps
    )
    GROUP BY 1
    ORDER BY 3 DESC
    
    Key Dune Tables:
    - tokens.erc20: Token metadata
    - prices.usd: Historical token prices
    - ethereum.transactions: Raw transactions
    - ethereum.logs: Raw event logs
    - [protocol]_[chain].[Contract]_evt_[Event]: Decoded events
    - [protocol]_[chain].[Contract]_call_[Function]: Decoded calls
    
  #### **Security Notes**
    - Validate data freshness (check max block)
    - Handle token decimals correctly
    - Account for price oracle delays

---
  #### **Id**
wallet-profiling
  #### **Name**
Wallet Behavior Analysis
  #### **Description**
    Analyze wallet activity patterns to identify traders,
    smart money, or protocol users
    
  #### **When To Use**
    - Finding alpha wallets
    - User segmentation
    - Fraud detection
  #### **Implementation**
    -- Wallet PnL analysis
    WITH wallet_trades AS (
      SELECT
        trader as wallet,
        token_bought_address,
        token_bought_amount_raw / POWER(10, decimals) as amount_bought,
        amount_usd
      FROM dex.trades
      WHERE trader = 0x... -- Target wallet
        AND block_time >= NOW() - INTERVAL '90' DAY
    ),
    token_performance AS (
      SELECT
        wallet,
        token_bought_address,
        SUM(amount_bought) as total_bought,
        SUM(amount_usd) as total_cost,
        -- Get current value
        SUM(amount_bought) * (
          SELECT price FROM prices.usd
          WHERE contract_address = token_bought_address
          ORDER BY minute DESC LIMIT 1
        ) as current_value
      FROM wallet_trades
      GROUP BY 1, 2
    )
    SELECT
      wallet,
      SUM(current_value - total_cost) as total_pnl,
      SUM(current_value) / SUM(total_cost) - 1 as pnl_pct
    FROM token_performance
    GROUP BY 1
    
    -- Smart money identification
    SELECT
      trader,
      COUNT(DISTINCT token_bought_address) as tokens_traded,
      AVG(CASE
        WHEN current_value > amount_usd * 2 THEN 1
        ELSE 0
      END) as win_rate_2x,
      SUM(current_value - amount_usd) as total_pnl
    FROM dex.trades t
    JOIN token_metrics m ON t.token_bought_address = m.token
    WHERE block_time >= NOW() - INTERVAL '30' DAY
    GROUP BY 1
    HAVING COUNT(*) >= 10
    ORDER BY win_rate_2x DESC
    LIMIT 100
    
  #### **Security Notes**
    - PnL calculations are estimates
    - Consider gas costs
    - Account for unsold holdings

---
  #### **Id**
protocol-health
  #### **Name**
Protocol Health Dashboard
  #### **Description**
    Key metrics for monitoring DeFi protocol health
    
  #### **When To Use**
    - Protocol monitoring
    - Risk assessment
    - Investor due diligence
  #### **Implementation**
    Protocol Health Metrics:
    
    -- 1. TVL and TVL Growth
    SELECT
      date_trunc('day', block_time) as day,
      SUM(amount_usd) FILTER (WHERE type = 'deposit') as deposits,
      SUM(amount_usd) FILTER (WHERE type = 'withdraw') as withdrawals,
      SUM(amount_usd) FILTER (WHERE type = 'deposit') -
        SUM(amount_usd) FILTER (WHERE type = 'withdraw') as net_flow
    FROM protocol_events
    GROUP BY 1
    
    -- 2. User Retention (DAU/MAU ratio)
    WITH daily_users AS (
      SELECT date_trunc('day', block_time) as day, "from" as user
      FROM protocol_transactions
      GROUP BY 1, 2
    ),
    monthly_users AS (
      SELECT date_trunc('month', day) as month, COUNT(DISTINCT user) as mau
      FROM daily_users
      GROUP BY 1
    ),
    avg_daily AS (
      SELECT
        date_trunc('month', day) as month,
        AVG(daily_count) as avg_dau
      FROM (
        SELECT day, COUNT(DISTINCT user) as daily_count FROM daily_users GROUP BY 1
      )
      GROUP BY 1
    )
    SELECT
      m.month,
      avg_dau,
      mau,
      avg_dau / mau as stickiness
    FROM monthly_users m
    JOIN avg_daily d ON m.month = d.month
    
    -- 3. Revenue and Fee Generation
    SELECT
      date_trunc('week', block_time) as week,
      SUM(fee_amount_usd) as protocol_fees,
      SUM(volume_usd) * 0.003 as lp_fees, -- 0.3% fee example
      COUNT(DISTINCT tx_hash) as transactions
    FROM protocol_trades
    GROUP BY 1
    
    -- 4. Concentration Risk (top holder %)
    SELECT
      holder,
      balance / total_supply as pct_ownership
    FROM token_balances
    CROSS JOIN (SELECT SUM(balance) as total_supply FROM token_balances)
    ORDER BY balance DESC
    LIMIT 10
    