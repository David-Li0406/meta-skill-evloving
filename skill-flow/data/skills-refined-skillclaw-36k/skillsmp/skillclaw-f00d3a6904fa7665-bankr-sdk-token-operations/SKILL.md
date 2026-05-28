---
name: bankr-sdk-token-operations
description: Use this skill when you need to perform token operations such as sending, swapping, or trading tokens across various blockchains using the Bankr SDK.
---

# Bankr SDK Token Operations

This skill allows you to build and execute transactions for sending, swapping, and trading tokens across multiple blockchains.

## Transaction Types

| Type | Description | Example Prompt |
|------|-------------|----------------|
| `transfer_erc20` | Send ERC20 tokens | "Send 100 USDC to 0x..." |
| `transfer_eth` | Send native ETH | "Send 0.1 ETH to 0x..." |
| `convert_eth_to_weth` | Wrap ETH | "Wrap 0.5 ETH" |
| `convert_weth_to_eth` | Unwrap WETH | "Unwrap 1 WETH" |
| `transfer_nft` | Send NFT | "Transfer my NFT #123 to 0x..." |
| `buy_nft` | Purchase NFT | "Buy the cheapest Pudgy Penguin" |
| `bridge_tokens` | Move tokens across chains | "Bridge 100 USDC from Ethereum to Base" |
| `swap_tokens` | Exchange tokens | "Swap 0.1 ETH to USDC" |

## Prompt Patterns

### Transfers
```
"Send 100 USDC to 0x742d35..."
"Transfer 0.5 ETH to vitalik.eth"
```

### ETH/WETH Operations
```
"Wrap 0.5 ETH to WETH"
"Unwrap 1 WETH to ETH"
```

### NFT Operations
```
"Transfer my Pudgy Penguin #1234 to 0x..."
"Buy the cheapest Pudgy Penguin on OpenSea"
```

### Cross-Chain Operations
```
"Bridge 100 USDC from Ethereum to Base"
"Move 0.5 ETH from Base to Ethereum"
```

### Token Swaps
```
"Swap 0.1 ETH to USDC"
"Exchange 100 USDC for WETH"
"Buy $100 worth of DEGEN"
```

## Usage

```typescript
import { BankrClient } from "@bankr/sdk";

const client = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
});

// Example: Transfer tokens
const transferResult = await client.promptAndWait({
  prompt: "Send 100 USDC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
});

// Example: Swap tokens
const swapResult = await client.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC",
});

// Handle transfer result
if (transferResult.status === "completed" && transferResult.transactions) {
  const tx = transferResult.transactions[0].metadata.transaction;
  await wallet.sendTransaction(tx);
}

// Handle swap result
if (swapResult.status === "completed" && swapResult.transactions) {
  const swapTx = swapResult.transactions[0].metadata.transaction;
  await wallet.sendTransaction(swapTx);
}
```

## Common Issues

| Issue | Resolution |
|-------|------------|
| Insufficient balance | Reduce amount or add funds |
| Token not found | Check token symbol/address |
| High slippage | Try smaller amounts |
| Network congestion | Wait and retry |

## Supported Chains

| Chain | Native Token |
|-------|--------------|
| Base | ETH |
| Polygon | MATIC |
| Ethereum | ETH |
| Unichain | ETH |
| Solana | SOL |