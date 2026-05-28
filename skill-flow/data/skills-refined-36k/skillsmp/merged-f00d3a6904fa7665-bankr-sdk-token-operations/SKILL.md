---
name: bankr-sdk-token-operations
description: Use this skill when you need to perform token operations such as trading, swapping, transferring, or bridging tokens across multiple blockchains.
---

# Bankr SDK Token Operations

Execute various token operations including transfers, swaps, and NFT transactions across multiple blockchains.

## Transaction Types

| Type | Description | Example Prompt |
|------|-------------|----------------|
| `transfer_erc20` | Send ERC20 tokens | "Send 100 USDC to 0x..." |
| `transfer_eth` | Send native ETH | "Send 0.1 ETH to 0x..." |
| `convert_eth_to_weth` | Wrap ETH | "Wrap 0.5 ETH" |
| `convert_weth_to_eth` | Unwrap WETH | "Unwrap 1 WETH" |
| `transfer_nft` | Send NFT | "Transfer my NFT #123 to 0x..." |
| `buy_nft` | Purchase NFT | "Buy the cheapest Pudgy Penguin" |
| `mint_nft` | Mint an NFT | "Mint NFT from Manifold contract 0x..." |
| `swap_tokens` | Exchange tokens | "Swap 0.1 ETH to USDC" |
| `bridge_tokens` | Move tokens across chains | "Bridge 100 USDC from Ethereum to Base" |

## Prompt Patterns

### Transfers
```
"Send 100 USDC to 0x742d35..."
"Transfer 0.5 ETH to vitalik.eth"
```

### ETH/WETH
```
"Wrap 0.5 ETH to WETH"
"Unwrap 1 WETH to ETH"
```

### NFTs
```
"Transfer my Pudgy Penguin #1234 to 0x..."
"Buy the cheapest Pudgy Penguin on OpenSea"
```

### Token Swaps
```
"Swap 0.1 ETH to USDC"
"Buy $100 worth of DEGEN"
"Sell all my DEGEN"
```

### Cross-Chain
```
"Bridge 0.5 ETH from Ethereum to Base"
"Move 100 USDC from Polygon to Solana"
```

## Usage

```typescript
import { BankrClient } from "@bankr/sdk";

const client = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
});

// Example: Transfer tokens
const result = await client.promptAndWait({
  prompt: "Send 100 USDC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
});

if (result.status === "completed" && result.transactions) {
  const tx = result.transactions[0].metadata.transaction;
  await wallet.sendTransaction(tx);
}
```

## Supported Chains

| Chain | Native Token |
|-------|--------------|
| Base | ETH |
| Polygon | MATIC |
| Ethereum | ETH |
| Solana | SOL |

## Common Issues

| Issue | Resolution |
|-------|------------|
| Insufficient balance | Reduce amount or add funds |
| Token not found | Check token symbol/address |
| High slippage | Try smaller amounts |
| Network congestion | Wait and retry |

## Timing Guidelines

| Operation | Typical Time |
|-----------|--------------|
| ERC20/ETH transfer | 2-5s |
| Wrap/Unwrap | 2-5s |
| NFT transfer | 3-5s |
| NFT purchase | 5-10s |
| Cross-chain bridge | 10-30s |

## Related Skills

- **sdk-capabilities**: Full list of supported operations
- **sdk-wallet-operations**: Client setup and configuration