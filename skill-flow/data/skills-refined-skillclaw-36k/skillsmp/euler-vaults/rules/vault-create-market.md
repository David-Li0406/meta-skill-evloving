---
title: Create a New Vault/Market
impact: HIGH
impactDescription: Deploy new lending markets for any asset
tags: vault, create, deploy, factory, market, cluster
---

## Create a New Vault/Market

Creating new Euler vaults allows you to establish lending markets for ERC-20 tokens. Use [euler-vault-scripts](https://github.com/euler-xyz/euler-vault-scripts) for deployment and management.

**Using euler-vault-scripts for cluster deployment:**

A cluster is a collection of vaults that accept each other as collateral and share a common governor. The scripts handle both initial deployment and ongoing management.

```bash
# Clone euler-vault-scripts repository
git clone https://github.com/euler-xyz/euler-vault-scripts
cd euler-vault-scripts

# Install dependencies
./install.sh
forge clean && forge compile

# Edit cluster configuration (copy and modify Cluster.s.sol)
# Define assets, LTVs, oracle providers, caps, IRM parameters, etc.

# Dry run first (always!)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol --dry-run --rpc-url 1

# Deploy (initial deployment)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol --account DEPLOYER --rpc-url 1

# Management after governance transfer (via Safe + Timelock)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol \
  --batch-via-safe --safe-address DAO --timelock-address wildcard --rpc-url 1
```

The cluster script (Cluster.s.sol) defines:
- Assets and their vaults
- LTV ratios between collateral/borrow pairs
- Oracle providers for each asset
- Supply and borrow caps
- Interest rate model parameters
- Hooks and flags

The scripts apply deltas - if vaults already exist, only the difference between configuration and current state is applied.

Key parameters to configure:

| Parameter | Description |
|-----------|-------------|
| Asset | Underlying ERC-20 token |
| Oracle | EulerRouter configured for price feeds |
| Unit of Account | Common denomination (USD, ETH, etc.) |
| LTV (borrow/liquidation) | Collateral requirements |
| Caps (supply/borrow) | Exposure limits |
| IRM | Interest rate model parameters |
| Governor | Address controlling vault parameters |

Important considerations:
- Always use `--dry-run` first to simulate transactions
- Configure appropriate LTV ratios for risk management
- Set reasonable caps to limit protocol exposure
- Consider using governance contracts (GovernorAccessControl + TimelockController + Safe)
- Governor can be set to address(0) for immutability (ungoverned vault)

References:
- [euler-vault-scripts](https://github.com/euler-xyz/euler-vault-scripts)
- [EVK Whitepaper](https://docs.euler.finance/euler-vault-kit-white-paper/)
