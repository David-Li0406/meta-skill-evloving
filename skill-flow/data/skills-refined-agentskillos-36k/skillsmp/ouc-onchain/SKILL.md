---
name: ouc-onchain
description: >
  Use this skill when you need to query on-chain data from EVM or ICP.
  This includes: ERC-7546 Dictionary state, OUC canister state, auditor pools,
  proposals, and upgrade status. Provides helper functions for cast and dfx calls.
allowed-tools: Bash,Read
---

# OUC On-Chain Data Retrieval Skill

This skill provides patterns for querying on-chain data from both EVM and ICP chains.

## EVM Queries (via cast)

### Query ERC-7546 Dictionary Implementation

```bash
# Get implementation address for a selector
cast call $DICTIONARY_ADDR "getImplementation(bytes4)(address)" $SELECTOR --rpc-url $RPC_URL

# Get dictionary owner
cast call $DICTIONARY_ADDR "owner()(address)" --rpc-url $RPC_URL

# Read storage slot directly
cast storage $CONTRACT_ADDR $SLOT --rpc-url $RPC_URL
```

### Query ERC-7546 Proxy

```bash
# The proxy's dictionary slot (ERC-7201 namespaced)
DICTIONARY_SLOT="0x267691be3525af8a813d30db0c9e2bad5b0d2c0f67d9e4f1c769018cff56f4"

# Get dictionary address from proxy
cast storage $PROXY_ADDR $DICTIONARY_SLOT --rpc-url $RPC_URL
```

### Block Information

```bash
# Get current block number
cast block-number --rpc-url $RPC_URL

# Get block timestamp
cast block latest --json --rpc-url $RPC_URL | jq '.timestamp'
```

## ICP Queries (via dfx)

### Query OUC Canister

```bash
# Get version
dfx canister call ouc getVersion

# Get proposal count
dfx canister call ouc getProposalCount

# Get specific proposal
dfx canister call ouc getProposal '(0)'

# Get auditor count
dfx canister call ouc getAuditorCount
```

### Canister Status

```bash
# Get canister status (cycles, memory, etc.)
dfx canister status ouc

# Get canister ID
dfx canister id ouc
```

## Common Patterns

### Compare Local vs Deployed (EVM)

1. Read local handler selectors from SPEC.toml or source code
2. Query dictionary for each selector's implementation
3. Check if implementation addresses match expected
4. Detect zombie references (impl with no code)

### Upgrade Detection

1. Take baseline snapshot (dictionary state at block N)
2. Take current snapshot (dictionary state now)
3. Compare implementations for each selector
4. Detect Added/Removed/Changed/Unchanged

### Risk Assessment for Auditor Assignment

Based on detected changes:
- **Critical**: Zombie references detected
- **High**: Multiple selector changes, core function upgrades
- **Medium**: Single selector change, non-critical function
- **Low**: Minor updates, configuration changes
- **None**: No changes detected

## Environment Variables

```bash
# EVM
export RPC_URL="https://eth.llamarpc.com"
export DICTIONARY_ADDR="0x..."
export PROXY_ADDR="0x..."

# ICP
export DFX_NETWORK="local"  # or "ic" for mainnet
```

## Helper Functions

### Parse hex address from cast output

```bash
# Remove 0x prefix and pad
parse_address() {
  echo "0x$(echo $1 | sed 's/0x//' | tail -c 41)"
}
```

### Check if address has code

```bash
has_code() {
  local size=$(cast codesize $1 --rpc-url $RPC_URL)
  [ "$size" != "0" ]
}
```
