# Intent-to-Metric Routing

Route natural language questions to correct CryptoQuant metrics.

---

## How to Use This Map

1. Identify keywords in user question
2. Match to intent category
3. Select primary metric (check plan access)
4. Query endpoint and interpret using INTERPRETATION.md

---

## BTC Intent Categories

### VALUATION
**Triggers**: overvalued, undervalued, fair value, price outlook, worth buying, bubble, cheap, expensive, market cap, realized cap

**Primary Metric**: mvrv
**Endpoint**: `/v1/btc/market-indicator/mvrv`
**Plan**: Free

**Definition**: Market Value to Realized Value - compares market cap to average acquisition cost.

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| nupl | /v1/btc/market-indicator/nupl | Professional | Net unrealized profit/loss |
| nvt | /v1/btc/market-indicator/nvt | Free | Network value vs utility |
| realized-price | /v1/btc/market-indicator/realized-price | Free | Average cost basis |

---

### NETWORK_VALUATION
**Triggers**: nvt, network value, P/E ratio, utility, transaction value, on-chain activity

**Primary Metric**: nvt
**Endpoint**: `/v1/btc/market-indicator/nvt`
**Plan**: Free

**Definition**: Market cap / Transaction volume. Like a P/E ratio for Bitcoin.

**Interpretation**:
- NVT < 50: Undervalued relative to network utility
- NVT > 90: Overvalued, network value exceeds utility
- Compare to 6-month MA for context

---

### PROFIT_BEHAVIOR
**Triggers**: profit taking, selling at loss, realized profit, capitulation, SOPR, breakeven

**Primary Metric**: sopr
**Endpoint**: `/v1/btc/market-indicator/sopr`
**Plan**: Free

**Definition**: Spent Output Profit Ratio - evaluates if coins moved are in profit or loss.

**Interpretation**:
- SOPR < 1: Selling at loss (capitulation in bear, support test in bull)
- SOPR > 1: Selling at profit (healthy in bull, distribution in top)

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| asopr | /v1/btc/market-indicator/asopr | Professional | Adjusted (excludes <1hr) |
| sth-sopr | /v1/btc/market-indicator/sth-sopr | Professional | Short-term holders (<155d) |
| lth-sopr | /v1/btc/market-indicator/lth-sopr | Professional | Long-term holders (>155d) |

---

### EXCHANGE_FLOWS
**Triggers**: exchange inflow, outflow, accumulation, selling pressure, exchange reserve, deposits, withdrawals

**Primary Metric**: netflow
**Endpoint**: `/v1/btc/exchange-flows/netflow`
**Required Param**: `exchange` (default: all_exchange)
**Plan**: Free

**Definition**: Exchange Inflow - Outflow. Measures net coin movement.

**Interpretation**:
- Negative netflow = accumulation (coins leaving exchanges)
- Positive netflow = distribution (coins entering exchanges)
- Rapid changes signal shifting sentiment

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| reserve | /v1/btc/exchange-flows/reserve | Free | Total coins on exchanges |
| inflow | /v1/btc/exchange-flows/inflow | Free | Deposits to exchanges |
| outflow | /v1/btc/exchange-flows/outflow | Free | Withdrawals from exchanges |

---

### EXCHANGE_RESERVE
**Triggers**: exchange reserve, coins on exchange, supply on exchange, exchange balance

**Primary Metric**: reserve
**Endpoint**: `/v1/btc/exchange-flows/reserve`
**Plan**: Free

**Definition**: Total amount of coins held in exchange addresses.

**Interpretation**:
- Declining reserve: Holders withdrawing, supply squeeze developing (bullish)
- Rising reserve: Holders depositing, potential sell pressure (bearish)

---

### WHALE_ACTIVITY
**Triggers**: whale, large holder, institutional, smart money, big players, top 10 transactions

**Primary Metric**: exchange-whale-ratio
**Endpoint**: `/v1/btc/exchange-flows/exchange-whale-ratio`
**Plan**: Professional

**Definition**: Top 10 transaction volume / Total inflow. Measures large player dominance.

**Interpretation**:
- > 0.5: Whale dominated (watch for large moves)
- > 0.85: Extreme whale activity (manipulation risk)
- < 0.3: Retail dominated

**Free Alternative**: Use netflow + inflow analysis for context

---

### FUND_FLOW
**Triggers**: fund flow ratio, exchange vs network, trading activity ratio

**Primary Metric**: fund-flow-ratio
**Endpoint**: `/v1/btc/exchange-flows/fund-flow-ratio`
**Plan**: Professional

**Definition**: Exchange flow / Total network transfer. Contextualizes exchange activity.

**Interpretation**:
- < 0.05: Most activity is transfers, not trading
- > 0.15: Unusual exchange-focused activity

---

### LEVERAGE_SENTIMENT
**Triggers**: funding rate, leverage, derivatives, futures, perpetual, long, short, sentiment

**Primary Metric**: funding-rates
**Endpoint**: `/v1/btc/market-data/funding-rates`
**Required Param**: `symbol` (e.g., btc_usd)
**Plan**: Professional

**Definition**: Periodic payments to keep perpetual futures near index price.

**Interpretation**:
- > 0.05%: Extreme bullish leverage (correction risk)
- < -0.03%: Extreme bearish sentiment (squeeze risk)
- Extremes often precede reversal

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| open-interest | /v1/btc/market-data/open-interest | Professional | Total positions |
| long-short-ratio | /v1/btc/market-data/long-short-ratio | Professional | Directional bias |

---

### OPEN_INTEREST
**Triggers**: open interest, OI, positions, derivatives volume, futures positions

**Primary Metric**: open-interest
**Endpoint**: `/v1/btc/market-data/open-interest`
**Plan**: Professional

**Definition**: Total open long and short positions on derivative exchanges.

**Interpretation**:
- Rising OI + Rising price = Strong trend confirmation
- Rising OI + Falling price = Shorts building
- Falling OI + Rising price = Weak rally (short covering)
- Falling OI + Falling price = Capitulation

---

### COIN_AGE
**Triggers**: CDD, coin days destroyed, old coins, dormant coins, long-term holder movement, hodl

**Primary Metric**: cdd
**Endpoint**: `/v1/btc/network-indicator/cdd`
**Plan**: Free

**Definition**: Days held × Amount moved. Measures old coin activity.

**Interpretation**:
- CDD spike + falling price = Capitulation (bullish contrarian)
- CDD spike + rising price = Distribution (bearish)
- Baseline = Normal activity

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| mean-coin-age | /v1/btc/network-indicator/mean-coin-age | Free | Average holding time |
| dormancy | /v1/btc/network-indicator/dormancy | Professional | Coin age per volume |

---

### HODL_BEHAVIOR
**Triggers**: HODL, holding, mean coin age, aging coins, accumulation phase

**Primary Metric**: mean-coin-age
**Endpoint**: `/v1/btc/network-indicator/mean-coin-age`
**Plan**: Free

**Definition**: Average age of unspent coins weighted by value.

**Interpretation**:
- Rising MCA = Coins aging, strong HODL behavior (bullish)
- Declining MCA = Old coins moving, potential distribution

---

### STABLECOIN_LIQUIDITY
**Triggers**: stablecoin, SSR, USDT, USDC, buying power, dry powder, liquidity

**Primary Metric**: ssr
**Endpoint**: `/v1/btc/market-indicator/ssr`
**Plan**: Professional

**Definition**: BTC Market Cap / Stablecoin Market Cap.

**Interpretation**:
- Low SSR (<10): High buying power available (bullish)
- High SSR (>20): Reduced stablecoin liquidity
- Low SSR + bear market = Accumulation opportunity

---

### MINER_ACTIVITY
**Triggers**: miner, mining, hash rate, miner selling, miner revenue, MPI, Puell

**Primary Metric**: mpi
**Endpoint**: `/v1/btc/miner-flows/mpi`
**Plan**: Professional

**Definition**: Miners' Position Index - miner outflows vs 365d MA.

**Interpretation**:
- MPI > 2: Miners selling aggressively (bearish)
- MPI < 0.5: Miners accumulating (bullish)

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| puell-multiple | /v1/btc/miner-flows/puell-multiple | Free | Miner profitability |
| miner-netflow | /v1/btc/miner-flows/miner-netflow | Professional | Direct flow tracking |
| miner-to-exchange | /v1/btc/miner-flows/miner-to-exchange | Professional | Direct exchange deposits |

---

### MINER_PROFITABILITY
**Triggers**: Puell multiple, miner profit, mining profitability, issuance, block rewards

**Primary Metric**: puell-multiple
**Endpoint**: `/v1/btc/miner-flows/puell-multiple`
**Plan**: Free

**Definition**: Daily issuance value / 365-day MA.

**Interpretation**:
- < 0.5: Miners under stress (accumulation zone)
- > 2.0: Miners extremely profitable (potential top signal)
- Historical extremes mark cycle tops and bottoms

---

### MARKET_CYCLE
**Triggers**: bull market, bear market, cycle phase, market top, bottom, accumulation, distribution

**Primary Metrics**: mvrv + sopr + netflow (combined analysis)

**Workflow**:
1. Query mvrv: `/v1/btc/market-indicator/mvrv`
2. Query sopr: `/v1/btc/market-indicator/sopr`
3. Query netflow: `/v1/btc/exchange-flows/netflow`
4. Apply combined analysis from INTERPRETATION.md

**Cycle Phase Detection**:
| Phase | MVRV | SOPR | Netflow |
|-------|------|------|---------|
| Accumulation | < 1.5 | ≈ 1.0 | Negative |
| Markup | 1.5 - 2.5 | > 1.0 | Negative |
| Distribution | 2.5 - 3.5 | > 1.05 | Positive |
| Markdown | Falling | < 1.0 | Positive |

---

### COINBASE_PREMIUM
**Triggers**: coinbase premium, US institutional, american buyers, US demand, coinbase price

**Primary Metric**: coinbase-premium-index
**Endpoint**: `/v1/btc/market-data/coinbase-premium-index`
**Plan**: Professional

**Definition**: Price gap between Coinbase (USD) and other exchanges (USDT).

**Interpretation**:
- > +$100: Strong US institutional demand (bullish)
- +$20 to +$100: Healthy US premium
- < -$100: US selling pressure (bearish)

**Key Signal**: Sustained premium during price drops = institutional accumulation.

---

### KIMCHI_PREMIUM
**Triggers**: kimchi premium, korea premium, korean demand, korean retail, KRW premium

**Primary Metric**: korea-premium-index
**Endpoint**: `/v1/btc/market-data/korea-premium-index`
**Plan**: Professional

**Definition**: Price gap between Korean exchanges (KRW) and global exchanges.

**Interpretation**:
- > +10%: Extreme FOMO (🔴 often marks local tops)
- +2% to +5%: Healthy demand
- < -2%: Korean selling (contrarian opportunity)

**Key Signal**: Kimchi premium > 10% historically marks local tops.

---

### ETF_FLOWS
**Triggers**: etf, ETF flow, spot ETF, bitcoin ETF, blackrock, fidelity, institutional flow, ETF inflow, ETF outflow

**Primary Metric**: etf-netflow
**Endpoint**: `/v1/btc/etf/netflow`
**Plan**: Professional

**Definition**: Net flow of BTC into/out of spot Bitcoin ETFs.

**Interpretation**:
- > +$500M/day: Massive institutional buying (🟢)
- +$100M to +$500M: Healthy accumulation
- -$100M to +$100M: Neutral
- < -$500M/day: Heavy institutional selling (🔴)

**Key Signal**: Multi-day positive streaks = strong conviction. Consecutive outflows = risk-off.

**Additional Metrics**:
| Metric | Endpoint | Plan | Use Case |
|--------|----------|------|----------|
| etf-holdings | /v1/btc/etf/holdings | Professional | Total BTC in ETFs |
| gbtc-premium | /v1/btc/etf/gbtc-premium | Professional | GBTC NAV discount |

---

## ETH Intent Categories

### VALUATION
**Triggers**: eth price, ethereum outlook, eth valuation, eth overvalued, eth undervalued

**Primary Metric**: mvrv
**Endpoint**: `/v1/eth/market-indicator/mvrv`
**Plan**: Free

---

### EXCHANGE_FLOWS
**Triggers**: eth exchange, eth accumulation, eth deposit, eth withdrawal

**Primary Metric**: netflow
**Endpoint**: `/v1/eth/exchange-flows/netflow`
**Plan**: Free

---

### STAKING
**Triggers**: staking, validator, staked eth, beacon chain, PoS, staking rate

**Primary Metric**: staking-rate
**Endpoint**: `/v1/eth/network-indicator/staking-rate`
**Plan**: Professional

---

### PROFIT_BEHAVIOR
**Triggers**: eth profit, eth SOPR, eth selling

**Primary Metric**: sopr
**Endpoint**: `/v1/eth/market-indicator/sopr`
**Plan**: Free

---

## Fallback Strategy

When intent doesn't match any category:

1. **Try discover_endpoints()** with keyword search
2. **Use describe_metric()** for unfamiliar metrics
3. **Ask for clarification** if still unclear

---

## Quick Reference Table

| Intent | Primary Metric | Free? | Endpoint |
|--------|---------------|-------|----------|
| VALUATION | mvrv | Yes | /v1/btc/market-indicator/mvrv |
| NETWORK_VALUATION | nvt | Yes | /v1/btc/market-indicator/nvt |
| PROFIT_BEHAVIOR | sopr | Yes | /v1/btc/market-indicator/sopr |
| EXCHANGE_FLOWS | netflow | Yes | /v1/btc/exchange-flows/netflow |
| EXCHANGE_RESERVE | reserve | Yes | /v1/btc/exchange-flows/reserve |
| WHALE_ACTIVITY | whale-ratio | No | /v1/btc/exchange-flows/exchange-whale-ratio |
| FUND_FLOW | fund-flow-ratio | No | /v1/btc/exchange-flows/fund-flow-ratio |
| LEVERAGE_SENTIMENT | funding-rates | No | /v1/btc/market-data/funding-rates |
| OPEN_INTEREST | open-interest | No | /v1/btc/market-data/open-interest |
| COIN_AGE | cdd | Yes | /v1/btc/network-indicator/cdd |
| HODL_BEHAVIOR | mean-coin-age | Yes | /v1/btc/network-indicator/mean-coin-age |
| STABLECOIN_LIQUIDITY | ssr | No | /v1/btc/market-indicator/ssr |
| MINER_ACTIVITY | mpi | No | /v1/btc/miner-flows/mpi |
| MINER_PROFITABILITY | puell-multiple | Yes | /v1/btc/miner-flows/puell-multiple |
| COINBASE_PREMIUM | coinbase-premium-index | No | /v1/btc/market-data/coinbase-premium-index |
| KIMCHI_PREMIUM | korea-premium-index | No | /v1/btc/market-data/korea-premium-index |
| ETF_FLOWS | etf-netflow | No | /v1/btc/etf/netflow |
| MARKET_CYCLE | mvrv + sopr | Partial | Combined query |
