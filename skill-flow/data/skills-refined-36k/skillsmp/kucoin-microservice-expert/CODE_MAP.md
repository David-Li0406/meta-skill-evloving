# KuCoin Integration Code Map

Complete file-by-file breakdown of the KuCoin microservice integration.

## Core API Clients

### Primary Client
**`src/services/kucoinApi/KuCoinApiClient.ts`** (5000+ lines)

Main KuCoin API client with 100+ methods:

| Category | Methods |
|----------|---------|
| **Orders** | `createOrder()`, `createUSDFirstBuyOrder()`, `cancelOrder()`, `getOrder()` |
| **Market Data** | `getOrderBook()`, `getTicker()`, `getMarketData()`, `getSymbolInfo()` |
| **Account** | `getBalances()`, `getTradingBalance()`, `getAccountInfo()` |
| **WebSocket** | `subscribeToMarketData()`, `subscribeToExecutionReports()` |
| **Withdrawals** | `requestWithdrawal()`, `getWithdrawals()`, `getWithdrawalQuotas()` |
| **Futures** | `getFuturesSymbols()`, `createFuturesOrder()` |
| **Time Sync** | `getEnhancedSynchronizedTimestamp()` |

Key private methods:
- `createSignature()` - HMAC-SHA256 signing
- `encryptPassphrase()` - Passphrase encryption
- `makeRequest()` - HTTP request wrapper

### Enhanced Wrapper
**`src/services/enhancedKuCoinApiClient.ts`** (477 lines)

Adds operational resilience:
- `getOrderBook()` with smart caching (3s TTL)
- `getTicker()` with 2s caching
- `batchGetOrderBooks()` - 5 symbols per batch
- `prefetchOrderBooks()` - Cache warming
- `healthCheck()` - Client status
- `emergencySlowdown()` - Rate limit recovery

### Backward Compatibility
**`src/services/kucoinApiClient.ts`**

Simple re-export for legacy code:
```typescript
export { KuCoinApiClient as KucoinApiClient };
```

## Infrastructure Services

### Rate Limit Manager
**`src/services/rateLimitManager.ts`** (250+ lines)

KuCoin Rate Limit 2.0 implementation:

```typescript
// VIP0 Limits
const RATE_LIMITS = {
  spot: { requests: 4000, window: 30000 },
  public: { requests: 2000, window: 30000 },
  futures: { requests: 2000, window: 30000 }
};
```

Features:
- Request deduplication (concurrent duplicate prevention)
- Exponential backoff with jitter
- Circuit breaker (open/half-open/closed states)
- Priority queuing (high/medium/low)
- Metrics tracking (requests, latency, errors)

### Timestamp Manager
**`src/services/timestampManager.ts`** (150+ lines)

Server time synchronization:
- 10-minute caching of synchronized timestamps
- 1-second safety buffer (fallback)
- Batch request queue
- Network latency tolerance (2s max)

### WebSocket Data Manager
**`src/services/webSocketDataManager.ts`** (200+ lines)

Real-time data management:
- Public WebSocket: market data, order books
- Private WebSocket: execution reports, balance updates
- 30-second health monitoring
- Auto-reconnection with exponential backoff
- Subscription management

## Functional Modules

**Location**: `src/services/kucoinApi/modules/`

| Module | File | Key Functions |
|--------|------|---------------|
| **Core** | `core.ts` | `generateWebSocketAuthHeaders()`, `attemptConnection()` |
| **Orders** | `orders.ts` | `createOrderMessage()`, `validateOrderParameters()`, `roundQuantity()` |
| **Basket** | `basket.ts` | `getBasketTokens()`, `processBasketPriceCalculation()` |
| **Market Data** | `marketData.ts` | `formatSymbol()`, `processMarketData()` |
| **Health** | `health.ts` | `pingWebSocket()`, `trackPerformance()` |
| **Logger** | `logger.ts` | `log()`, `warn()`, `wsLog()`, `pxApiLog()` |

## Type Definitions

### Main Types
**`src/types/kucoinApi.ts`**

```typescript
interface OrderBook {
  asks: Array<[string, string]>;
  bids: Array<[string, string]>;
  timestamp: number;
}

interface KuCoinOrder {
  orderId: string;
  symbol: string;
  side: 'buy' | 'sell';
  type: 'market' | 'limit';
  price?: string;
  size: string;
  dealFunds: string;
  dealSize: string;
  fee: string;
  feeCurrency: string;
  status: string;
  // ... more fields
}

interface KuCoinSymbol {
  symbol: string;
  baseCurrency: string;
  quoteCurrency: string;
  baseMinSize: string;
  baseMaxSize: string;
  baseIncrement: string;  // lot size
  quoteMinSize: string;
  quoteMaxSize: string;
  quoteIncrement: string; // tick size
  priceIncrement: string;
  // ... more fields
}
```

### Module Types
**`src/services/kucoinApi/types.ts`**

```typescript
interface ProcessingStats {
  requestCount: number;
  avgLatency: number;
  errorRate: number;
}

interface BasketToken {
  symbol: string;
  weight: number;
  // ... more fields
}
```

## Configuration

### Main Config
**`src/config/index.ts`**

```typescript
export const config = {
  api: {
    kucoin: {
      key: process.env.KUCOIN_API_KEY,
      secret: process.env.KUCOIN_API_SECRET,
      passphrase: process.env.KUCOIN_API_PASSPHRASE,
      baseUrl: KUCOIN_USE_SANDBOX
        ? 'https://openapi-sandbox.kucoin.com'
        : 'https://api.kucoin.com',
    }
  },
  buffers: {
    buy: 0.026,  // 2.6% buy buffer
    sell: 0.026, // 2.6% sell buffer
    dynamic: {
      smallOrder: 0.015, // 1.5% for small orders
      normal: 0.010      // 1.0% for normal orders
    }
  },
  trading: {
    minUsdtPerToken: 10,
    maxSlippage: 0.05
  },
  strategyRebalanceWindow: {
    start: '23:00',
    end: '01:20',
    timezone: 'CET'
  }
};
```

### Cache Config
**`src/config/cacheConfig.ts`**

```typescript
export const CACHE_TTL = {
  orderBook: 3000,      // 3 seconds
  ticker: 2000,         // 2 seconds
  symbols: 3600000,     // 1 hour
  balances: 5000,       // 5 seconds
  timestamp: 600000     // 10 minutes
};
```

## Trading Services

Higher-level services that consume KuCoin API:

| Service | File | Purpose |
|---------|------|---------|
| Buy Basket | `src/services/buyBasket.ts` | Execute basket purchases |
| Sell Basket | `src/services/sellBasket.ts` | Execute basket sales |
| Buy Strategy | `src/services/buyStrategy.ts` | Strategy position entry |
| Sell Strategy | `src/services/sellStrategy.ts` | Strategy position exit |
| Rebalancing | `src/services/rebalancingService.ts` | 3-phase rebalancing |
| Strategy Rebalancing | `src/services/strategyRebalancingService.ts` | Weight adjustments |
| Basket Pricing | `src/services/basketPricingService.ts` | Price with buffers |
| Dynamic Buffer | `src/services/dynamicBufferService.ts` | Token-level buffers |

## Caching Layer

| Cache | File | Purpose |
|-------|------|---------|
| Order Book | `src/utils/cache/orderBookCache.ts` | Real-time order book data |
| Request | `src/utils/cache/requestCache.ts` | API response caching |
| Deduplication | `src/utils/cache/requestDeduplication.ts` | Prevent duplicate calls |
| Smart Cache | `src/services/smartCacheManager.ts` | Intelligent invalidation |
| Basket Price | `src/services/basketPriceCache.ts` | Computed price caching |

## Dependency Chain

```
Routes (tradingRoutes.ts, accountRoutes.ts)
    ↓
Trading Services (buyBasket.ts, sellBasket.ts)
    ↓
Pricing Services (basketPricingService.ts)
    ↓
EnhancedKuCoinApiClient (rate limiting, caching)
    ↓
KuCoinApiClient (core API implementation)
    ├─→ RateLimitManager (request queuing)
    ├─→ TimestampManager (time sync)
    ├─→ WebSocketDataManager (real-time data)
    └─→ Modules (core, orders, basket, marketData, health, logger)
```

## Environment Variables

**Required:**
```bash
KUCOIN_API_KEY=your_key
KUCOIN_API_SECRET=your_secret
KUCOIN_API_PASSPHRASE=your_passphrase
```

**Optional:**
```bash
KUCOIN_USE_SANDBOX=true    # Use sandbox environment
PORT=8080                   # Server port
ENVIRONMENT=development     # or production
```
