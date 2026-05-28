---
name: ethereum-wingman
description: Use this skill when you need guidance on building Ethereum projects, creating smart contracts, or navigating DeFi protocols using Scaffold-ETH 2.
---

# Ethereum Wingman

Comprehensive Ethereum development guide for AI agents. Covers smart contract development, DeFi protocols, security best practices, and the SpeedRun Ethereum curriculum.

## 🚨 THE MOST CRITICAL CONCEPT 🚨

**NOTHING IS AUTOMATIC ON ETHEREUM.**

Smart contracts cannot execute themselves. There is no cron job, no scheduler, no background process. For EVERY function that "needs to happen":

1. Make it callable by **ANYONE** (not just admin).
2. Give callers a **REASON** (profit, reward, their own interest).
3. Make the incentive **SUFFICIENT** to cover gas + profit.

**Always ask: "Who calls this function? Why would they pay gas?"**

If you can't answer this, your function won't get called.

### Examples of Proper Incentive Design

```solidity
// LIQUIDATIONS: Caller gets bonus collateral
function liquidate(address user) external {
    require(getHealthFactor(user) < 1e18, "Healthy");
    uint256 bonus = collateral * 5 / 100; // 5% bonus
    collateralToken.transfer(msg.sender, collateral + bonus);
}

// YIELD HARVESTING: Caller gets % of harvest
function harvest() external {
    uint256 yield = protocol.claimRewards();
    uint256 callerReward = yield / 100; // 1%
    token.transfer(msg.sender, callerReward);
}

// CLAIMS: User wants their own tokens
function claimRewards() external {
    uint256 reward = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    token.transfer(msg.sender, reward);
}
```

## AI AGENT INSTRUCTIONS - READ THIS FIRST

### Default Stack: Scaffold-ETH 2 with Fork Mode

When a user wants to BUILD any Ethereum project, follow these steps:

**Step 1: Create Project**

```bash
npx create-eth@latest
# Select: foundry (recommended), target chain, project name
```

**Step 2: Install & Fork a Live Network**

```bash
cd <project-name>
yarn install
yarn fork --network base  # or mainnet, arbitrum, optimism, polygon
```

**Step 3: Deploy to Local Fork (FREE!)**

```bash
yarn deploy
```

**Step 4: Start Frontend**

```bash
yarn start
```

### DO NOT:

- Run `yarn chain` (use `yarn fork --network <chain>` instead!)
- Manually run `forge init` or set up Foundry from scratch
- Manually create Next.js projects  
- Set up wallet connection manually (SE2 has RainbowKit pre-configured)

### Why Fork Mode?

```
yarn chain (WRONG)              yarn fork --network base (CORRECT)
└─ Empty local chain            └─ Fork of real Base mainnet
└─ No protocols                 └─ Uniswap, Aave, etc. available
└─ No tokens                    └─ Real USDC, WETH exist
└─ Testing in isolation         └─ Test against REAL state
```

### Auto Block Mining (Prevent Timestamp Drift)

When you fork a chain, block timestamps are FROZEN at the fork point. New blocks only mine when transactions happen, breaking time-dependent logic.

**Solution**: After starting the fork, enable interval mining:

```bash
# Enable auto block mining (1 block/second)
cast rpc anvil_setIntervalMining 1
```

### Address Data Available

Token, protocol, and whale addresses are in `data/addresses/`:
- `tokens.json` - WETH, USDC, DAI, etc. per chain
- `protocols.json` - Uniswap, Aave, Chainlink per chain  
- `whales.json` - Large token holders for test funding