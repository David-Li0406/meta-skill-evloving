---
name: decibel-trading-expert
description: Use this skill when you need to integrate with the Decibel on-chain perpetual futures trading platform on Aptos, including API interactions, market data retrieval, and order management.
---

# Skill body

## Overview

Decibel is a fully on-chain perpetual futures trading platform built on the Aptos blockchain. It provides a comprehensive set of features for trading, including a trading engine, orderbook, and various APIs.

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
const orderbook = await client.getOrderbook("BTC-PERP", { depth: 10 });

// Get recent trades
const trades = await client.getRecentTrades("BTC-PERP", { limit: 50 });

// Get OHLC/candlesticks
const candles = await client.getCandles("BTC-PERP", {
  interval: "1h",
  limit: 100,
});
```

### Order Management

```typescript
// Place limit order
const order = await client.placeOrder({
  market: "BTC-PERP",
  side: "buy",
  type: "limit",
  price: 50000,
  size: 0.1,
});

// Place market order
const marketOrder = await client.placeOrder({
  market: "BTC-PERP",
  side: "sell",
  type: "market",
  size: 0.1,
});

// Cancel order
await client.cancelOrder(orderId);

// Cancel all orders
await client.cancelAllOrders({ market: "BTC-PERP" });
```

### Position Management

```typescript
// Get open positions
const positions = await client.getPositions();

// Get specific position details
const positionDetails = await client.getPosition("BTC-PERP");
```