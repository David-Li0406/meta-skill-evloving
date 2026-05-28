---
name: helius
description: Use this skill when you need to set up and utilize Helius, the leading RPC and API infrastructure for building high-performance Solana applications.
---

# Helius Development Guide

Helius provides high-performance infrastructure for Solana applications, including RPC nodes, DAS API for NFTs and tokens, real-time data streaming, and more.

## Overview

Helius offers:
- **RPC Infrastructure**: Globally distributed nodes with ultra-low latency.
- **DAS API**: Unified NFT and token data (compressed & standard).
- **Enhanced Transactions**: Parsed, human-readable transaction data.
- **Priority Fee API**: Real-time fee recommendations.
- **Webhooks**: Event-driven blockchain monitoring.
- **ZK Compression**: Compressed account and token APIs.
- **LaserStream**: gRPC-based real-time data streaming.

## Quick Start

### Installation

```bash
# Install Helius SDK
npm install helius-sdk

# Or with pnpm (recommended)
pnpm add helius-sdk
```

### Get Your API Key

1. Visit [dashboard.helius.dev](https://dashboard.helius.dev).
2. Create an account or sign in.
3. Generate an API key.
4. Store it securely (never commit to git).

### Environment Setup

```bash
# .env file
HELIUS_API_KEY=your_api_key_here
```

### Basic Setup

```typescript
import { createHelius } from "helius-sdk";

const helius = createHelius({
  apiKey: process.env.HELIUS_API_KEY!,
});

// RPC endpoint URLs
const MAINNET_RPC = `https://mainnet.helius-rpc.com/?api-key=${process.env.HELIUS_API_KEY}`;
const DEVNET_RPC = `https://devnet.helius-rpc.com/?api-key=${process.env.HELIUS_API_KEY}`;
```

## Core Services

### RPC Endpoints

| Network | HTTP Endpoint | WebSocket Endpoint |
|---------|--------------|-------------------|
| Mainnet | `https://mainnet.helius-rpc.com/?api-key=<KEY>` | `wss://mainnet.helius-rpc.com/?api-key=<KEY>` |
| Devnet | `https://devnet.helius-rpc.com/?api-key=<KEY>` | `wss://devnet.helius-rpc.com/?api-key=<KEY>` |

### Digital Asset Standard (DAS) API

Query NFT and token metadata, handling both regular and compressed NFTs.

**Get Single Asset:**
```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getAsset',
    params: { id: 'ASSET_MINT_ADDRESS' }
  })
});
```

**Get Assets by Owner:**
```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getAssetsByOwner',
    params: {
      ownerAddress: 'WALLET_ADDRESS',
      page: 1,
      limit: 100
    }
  })
});
```

### Enhanced Transactions API

Pre-parsed transaction data for easier integration and analysis.

### Real-time Data Streaming

Utilize LaserStream and webhooks for real-time blockchain data monitoring and event handling.

## Conclusion

Use Helius to build scalable and efficient Solana applications with ease, leveraging its powerful APIs and infrastructure.