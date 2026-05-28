---
name: helius-solana-infrastructure
description: Use this skill when you need to interact with Helius, Solana's high-performance RPC and API infrastructure for querying NFTs, tokens, and real-time blockchain data.
---

# Helius Solana Infrastructure Guide

Helius provides high-performance Solana RPC, real-time data streaming, and developer APIs for building applications on the Solana blockchain.

## Overview

Helius offers:
- **RPC Infrastructure**: Ultra-low latency globally distributed nodes.
- **Digital Asset Standard (DAS) API**: Unified access to NFT and token data.
- **Enhanced Transactions API**: Human-readable transaction data.
- **Priority Fee API**: Real-time fee recommendations for transactions.
- **Webhooks**: Event-driven notifications for blockchain activity.
- **LaserStream**: Real-time gRPC streaming service for low-latency data.
- **ZK Compression**: Reduced on-chain storage costs.

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

### Basic Setup

```typescript
import { createHelius } from "helius-sdk";

const helius = createHelius({
  apiKey: process.env.HELIUS_API_KEY!,
});
```

## Core Services

### RPC Endpoints

| Network | HTTP Endpoint |
|---------|---------------|
| Mainnet | `https://mainnet.helius-rpc.com/?api-key=<KEY>` |
| Devnet | `https://devnet.helius-rpc.com/?api-key=<KEY>` |

### Digital Asset Standard (DAS) API

Query NFT and token metadata.

**Get Single Asset:**
```javascript
const asset = await helius.getAsset({ id: "asset_id_here" });
```

**Get Assets by Owner:**
```javascript
const assets = await helius.getAssetsByOwner({ ownerAddress: "wallet_address", page: 1, limit: 100 });
```

### Enhanced Transactions API

Get parsed, human-readable transaction data.

```javascript
const parsed = await helius.enhanced.getTransactions({ transactions: ["sig1", "sig2", "sig3"] });
```

### Priority Fee API

Get optimal priority fees for fast transaction landing.

```javascript
const feeEstimate = await helius.getPriorityFeeEstimate({
  accountKeys: ["account1", "account2"],
  options: { priorityLevel: "HIGH" },
});
```

### LaserStream (Real-Time gRPC)

Ultra-low latency blockchain streaming.

```typescript
import { LaserStream } from '@helius-labs/laserstream';

const stream = new LaserStream({ apiKey: 'YOUR_API_KEY', region: 'fra' });
stream.subscribeAccount('ACCOUNT_ADDRESS', (update) => {
  console.log('Account updated:', update);
});
```

### Webhooks

Event-driven notifications for blockchain activity.

```javascript
const webhook = await helius.webhooks.createWebhook({
  webhookURL: "https://your-server.com/webhook",
  transactionTypes: ["NFT_SALE", "TOKEN_TRANSFER"],
  accountAddresses: ["ADDRESS_TO_WATCH"],
});
```

### ZK Compression

Reduce on-chain storage costs.

```javascript
const compressedAccount = await helius.zk.getCompressedAccount({ address: "compressed_account_address" });
```

## Pricing & Rate Limits

| Plan | Price | Credits | Rate Limit |
|------|-------|---------|------------|
| Free | $0/mo | 1M | 10 RPS |
| Developer | $49/mo | 10M | 50 RPS |
| Business | $499/mo | 100M | 200 RPS |
| Professional | $999/mo | 200M | 500 RPS |

## Best Practices

- Use environment variables for API keys.
- Implement retry logic with exponential backoff.
- Use DAS API for NFT queries instead of raw account info.
- Monitor webhook delivery and handle retries.

## Resources

- [Helius Documentation](https://www.helius.dev/docs)
- [Helius Dashboard](https://dashboard.helius.dev)
- [Helius Discord](https://discord.gg/helius)