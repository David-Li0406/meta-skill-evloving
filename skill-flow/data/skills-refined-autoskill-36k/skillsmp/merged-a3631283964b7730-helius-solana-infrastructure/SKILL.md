---
name: helius-solana-infrastructure
description: Use this skill when you need to set up and interact with Helius, Solana's high-performance RPC and API infrastructure for NFTs, tokens, and real-time data streaming.
---

# Helius Solana Infrastructure Guide

Helius provides high-performance Solana RPC, real-time data streaming, and developer APIs for building applications on the Solana blockchain.

## Overview

Helius offers:
- **RPC Infrastructure**: Globally distributed nodes with ultra-low latency.
- **Digital Asset Standard (DAS) API**: Unified access to NFT and token data.
- **Enhanced Transactions API**: Parsed, human-readable transaction data.
- **Priority Fee API**: Real-time fee recommendations for transactions.
- **Webhooks**: Event-driven notifications for blockchain activity.
- **LaserStream**: Real-time gRPC streaming service for low-latency data.
- **ZK Compression**: Reduced on-chain storage costs for accounts and tokens.

## Quick Start

### Installation

```bash
# Install Helius SDK
npm install helius-sdk
```

### Get Your API Key

1. Visit [dashboard.helius.dev](https://dashboard.helius.dev)
2. Create an account or sign in
3. Generate an API key
4. Store it securely (never commit to git)

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

Query NFT and token metadata.

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

Get parsed, human-readable transaction data.

```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getTransactionsForAddress',
    params: [
      'WALLET_ADDRESS',
      {
        transactionDetails: 'full',
        sortOrder: 'desc',
        limit: 10
      }
    ]
  })
});
```

### Priority Fee API

Get optimal priority fees for fast transaction landing.

```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getPriorityFeeEstimate',
    params: [{
      accountKeys: ['PROGRAM_ID', 'ACCOUNT_1', 'ACCOUNT_2']
    }]
  })
});
```

### LaserStream (Real-Time gRPC)

Ultra-low latency blockchain streaming.

```typescript
import { LaserStream } from '@helius-labs/laserstream';

const stream = new LaserStream({
  apiKey: 'YOUR_API_KEY',
  region: 'fra'  // fra, ams, tyo, sg, ewr, pitt, slc, lax, lon
});

// Subscribe to account changes
stream.subscribeAccount('ACCOUNT_ADDRESS', (update) => {
  console.log('Account updated:', update);
});
```

### Webhooks

Event-driven notifications for blockchain activity.

```javascript
const webhook = await fetch('https://api.helius.xyz/v0/webhooks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  },
  body: JSON.stringify({
    webhookURL: 'https://your-server.com/webhook',
    transactionTypes: ['NFT_SALE', 'TOKEN_TRANSFER'],
    accountAddresses: ['ADDRESS_TO_WATCH']
  })
});
```

### ZK Compression

Reduce on-chain storage costs by up to 98%.

```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getCompressedAccount',
    params: { address: 'COMPRESSED_ACCOUNT' }
  })
});
```

## Error Handling

```javascript
try {
  const response = await fetch(RPC_URL, { method: 'POST', ... });
  if (response.status === 429) {
    // Rate limited - wait and retry
  }
} catch (err) {
  // Handle network error
}
```

## Best Practices

- Use `confirmed` commitment for faster responses.
- Simulate transactions before sending.
- Check rate limit headers.

## Resources

- [Helius Documentation](https://www.helius.dev/docs)
- [Helius Dashboard](https://dashboard.helius.dev)
- [Helius Discord](https://discord.gg/helius)