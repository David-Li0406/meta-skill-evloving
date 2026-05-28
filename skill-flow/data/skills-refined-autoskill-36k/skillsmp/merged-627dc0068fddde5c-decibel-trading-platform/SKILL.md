---
name: decibel-trading-platform
description: Use this skill when integrating with the Decibel on-chain perpetual futures trading platform on Aptos for trading, market data, and position management.
---

# Decibel Trading Platform

Decibel is a fully on-chain perpetual futures trading platform built on the Aptos blockchain.

## When to Use

- Integrating with Decibel trading APIs
- Building trading bots or applications
- Understanding on-chain orderbook mechanics
- Market data queries (prices, orderbook, trades)
- Position and order management

## Platform Overview

**Base URLs:**
- REST API: `https://api.netna.aptoslabs.com/decibel`
- WebSocket: `wss://api.netna.aptoslabs.com/decibel`

**Core Features:**
- Perpetual futures trading
- Fully on-chain orderbook
- TWAP (Time-Weighted Average Price) orders
- Real-time WebSocket streams
- Subaccount support
- Vault strategies

## TypeScript SDK

### Installation

```bash
npm install @decibel/sdk
```

### Client Setup

```typescript
import { DecibelClient } from "@decibel/sdk";

const client = new DecibelClient({
  apiKey: process.env.DECIBEL_API_KEY,
  network: "mainnet",
});
```

### Market Data

```typescript
// Get available markets
const markets = await client.getMarkets();

// Get current prices
const prices = await client.getPrices();

// Get orderbook depth
const orderbook = await client.getOrderbook("<market>", { depth: <depth> });

// Get recent trades
const trades = await client.getRecentTrades("<market>", { limit: <limit> });

// Get OHLC/candlesticks
const candles = await client.getCandles("<market>", {
  interval: "<interval>",
  limit: <limit>,
});
```

### Order Management

```typescript
// Place limit order
const order = await client.placeOrder({
  market: "<market>",
  side: "<side>",
  type: "limit",
  price: <price>,
  size: <size>,
});

// Place market order
const marketOrder = await client.placeOrder({
  market: "<market>",
  side: "<side>",
  type: "market",
  size: <size>,
});

// Cancel order
await client.cancelOrder("<orderId>");

// Cancel all orders
await client.cancelAllOrders({ market: "<market>" });
```

### Position Management

```typescript
// Get open positions
const positions = await client.getPositions();

// Get specific position
const position = await client.getPosition("<market>");

// Close position
await client.closePosition("<market>");

// Set take-profit/stop-loss
await client.setTPSL("<market>", {
  takeProfit: <takeProfit>,
  stopLoss: <stopLoss>,
});
```

### TWAP Orders

```typescript
// Place TWAP order (reduces slippage)
const twapOrder = await client.placeTWAPOrder({
  market: "<market>",
  side: "<side>",
  size: <size>,
  duration: <duration>, // in seconds
  intervals: <intervals>, // number of intervals
});

// Get active TWAP orders
const activeTWAPs = await client.getActiveTWAPOrders();

// Cancel TWAP order
await client.cancelTWAPOrder("<twapOrderId>");
```

## REST API

### Market Data (Unauthenticated)

```bash
# Get markets
GET /market-data/markets

# Get prices
GET /market-data/prices

# Get orderbook
GET /market-data/orderbook?market=<market>&depth=<depth>

# Get recent trades
GET /market-data/trades?market=<market>&limit=<limit>

# Get candlesticks
GET /market-data/candles?market=<market>&interval=<interval>&limit=<limit>
```

### User Endpoints (Authenticated)

```bash
# Get account overview
GET /user/account
Headers: Authorization: Bearer {token}

# Get positions
GET /user/positions

# Get open orders
GET /user/orders

# Get order history
GET /user/orders/history

# Get trade history
GET /user/trades

# Get funding rate history
GET /user/funding-history
```

### Transaction Endpoints

```bash
# Place order
POST /transactions/place-order
Body: { market, side, type, price?, size }

# Cancel order
POST /transactions/cancel-order
Body: { orderId }

# Deposit to subaccount
POST /transactions/deposit
Body: { amount, subaccountId? }

# Withdraw from subaccount
POST /transactions/withdraw
Body: { amount, subaccountId? }
```

## WebSocket Streams

### Connection

```javascript
const ws = new WebSocket("wss://api.netna.aptoslabs.com/decibel");

ws.onopen = () => {
  // Subscribe to channels
  ws.send(JSON.stringify({
    type: "subscribe",
    channels: ["trades:<market>", "orderbook:<market>"],
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

### Available Channels

| Channel | Description |
|---------|-------------|
| `trades:{market}` | Real-time trades |
| `orderbook:{market}` | Orderbook updates |
| `ticker:{market}` | Price ticker |
| `account` | Account updates (authenticated) |
| `orders` | Order updates (authenticated) |
| `positions` | Position updates (authenticated) |
| `fills` | Fill notifications (authenticated) |

### Authenticated Subscription

```javascript
ws.send(JSON.stringify({
  type: "auth",
  token: "<your-api-token>",
}));

ws.send(JSON.stringify({
  type: "subscribe",
  channels: ["account", "orders", "positions", "fills"],
}));
```

## Account Management

### Subaccounts

```typescript
// Create subaccount
const subaccount = await client.createSubaccount({
  name: "<subaccount_name>",
});

// List subaccounts
const subaccounts = await client.getSubaccounts();

// Deposit to subaccount
await client.deposit({
  amount: <amount>,
  subaccountId: subaccount.id,
});

// Withdraw from subaccount
await client.withdraw({
  amount: <amount>,
  subaccountId: subaccount.id,
});
```

### Delegations

```typescript
// Delegate trading authority
await client.createDelegation({
  delegatee: "<delegatee_address>",
  permissions: ["trade", "cancel"],
  expiry: Date.now() + 30 * 24 * 60 * 60 * 1000,
});

// Revoke delegation
await client.revokeDelegation("<delegationId>");
```

## Error Handling

```typescript
try {
  const order = await client.placeOrder({...});
} catch (error) {
  if (error.code === "INSUFFICIENT_MARGIN") {
    console.log("Not enough margin for this order");
  } else if (error.code === "INVALID_PRICE") {
    console.log("Price outside allowed range");
  } else if (error.code === "RATE_LIMITED") {
    await sleep(1000);
    // Retry
  }
}
```

## Best Practices

**DO:**
- Use WebSocket for real-time data
- Implement proper error handling
- Use TWAP for large orders
- Monitor positions and margin
- Set TP/SL for risk management

**DON'T:**
- Poll REST API for real-time data
- Ignore rate limits
- Trade without sufficient margin
- Skip order confirmation

## Resources

- **API Docs:** https://docs.decibel.trade
- **SDK:** `@decibel/sdk`
- **Package Address:** `0xb8a5788314451ce4d2fbbad32e1bad88d4184b73943b7fe5166eab93cf1a5a95`