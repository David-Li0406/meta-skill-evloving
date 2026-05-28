---
name: dojo-deploy
description: Use this skill when deploying your Dojo worlds to local Katana, Sepolia testnet, or Starknet mainnet, and managing your deployment configurations.
---

# Dojo Deployment

Deploy your Dojo world to local Katana sequencer, Sepolia testnet, or Starknet mainnet.

## When to Use This Skill

- "Deploy my world to Katana"
- "Start Katana sequencer"
- "Deploy to Sepolia testnet"
- "Deploy to mainnet"

## What This Skill Does

Handles deployment workflows:
- Start and configure Katana sequencer
- Deploy worlds with `sozo migrate`
- Verify deployments
- Manage world addresses
- Configure network settings

## Quick Start

**Local development:**
```bash
katana --dev --dev.no-fee
sozo build && sozo migrate
```

**Testnet deployment:**
```bash
sozo build --profile sepolia
sozo migrate --profile sepolia
```

**Mainnet deployment:**
```bash
sozo build --profile mainnet
sozo migrate --profile mainnet
```

## Deployment Workflow

### 1. Local Development (Katana)

**Start Katana:**
```bash
katana --dev --dev.no-fee
```
This launches Katana with:
- RPC server at `http://localhost:5050`
- 10 pre-funded accounts
- Instant block mining
- Gas fees disabled

**Verify:**
```bash
# Preview deployment
sozo inspect

# Execute a system
sozo execute dojo_starter-actions spawn
```

### 2. Testnet Deployment (Sepolia)

**Configure profile:**
```toml
# dojo_sepolia.toml
[world]
name = "My Game"
seed = "my-game-sepolia"

[env]
rpc_url = "https://api.cartridge.gg/x/starknet/sepolia"
account_address = "YOUR_ACCOUNT"
private_key = "YOUR_KEY"

[namespace]
default = "my_game"

[writers]
"my_game" = ["my_game-actions"]
```

**Deploy:**
```bash
sozo build --profile sepolia
sozo migrate --profile sepolia
```

### 3. Mainnet Deployment

**Configure profile:**
```toml
# dojo_mainnet.toml
[world]
name = "My Game"
seed = "my-game-mainnet"

[env]
rpc_url = "https://api.cartridge.gg/x/starknet/mainnet"
account_address = "YOUR_ACCOUNT"
keystore_path = "~/.starknet_accounts/mainnet.json"

[namespace]
default = "my_game"

[writers]
"my_game" = ["my_game-actions"]
```

**Deploy:**
```bash
sozo build --profile mainnet
sozo migrate --profile mainnet
```

## Katana Configuration

### Mining Modes

**Instant (default):**
```bash
katana --dev --dev.no-fee
```
Mines block immediately on transaction.

**Interval:**
```bash
katana --block-time 10000
```
Mines block every 10 seconds.

**On-demand:**
```bash
katana --dev --no-mining
```
Manual block production.

### Account Configuration

**Default accounts:**
```bash
katana --dev --dev.accounts 10
```
Generates 10 pre-funded accounts.

**Custom seed:**
```bash
katana --dev --seed 0x123
```
Deterministic account generation.

### Network Forking

**Fork Sepolia:**
```bash
katana --dev --fork https://api.cartridge.gg/x/starknet/sepolia
```

**Fork at block:**
```bash
katana --dev --fork https://... --fork-block-number 100000
```