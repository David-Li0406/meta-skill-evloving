---
name: crane-balancer
description: Use this skill when you need to create or interact with Balancer V3 pools using Crane's DFPkg and service libraries, including weighted and constant product pools.
---

# Crane Balancer V3 Integration

Crane provides comprehensive Balancer V3 integration including pool DFPkgs, vault awareness, authentication, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `BalancerV3WeightedPoolDFPkg` | `pool-weighted/BalancerV3WeightedPoolDFPkg.sol` | Deploy weighted pools (80/20, custom weights) |
| `BalancerV3ConstantProductPoolDFPkg` | `pool-constProd/BalancerV3ConstantProductPoolDFPkg.sol` | Deploy 50/50 constant product pools |
| `BalancerV3VaultAwareRepo` | `vault/BalancerV3VaultAwareRepo.sol` | Vault dependency injection |
| `BalancerV3PoolRepo` | `vault/BalancerV3PoolRepo.sol` | Pool metadata storage |
| `BalancerV3WeightedPoolRepo` | `pool-weighted/BalancerV3WeightedPoolRepo.sol` | Weight storage |
| `BalancerV3AuthenticationRepo` | `vault/BalancerV3AuthenticationRepo.sol` | Pool authentication |
| `TestBase_BalancerV3Vault` | `test/bases/TestBase_BalancerV3Vault.sol` | Full vault deployment |
| `ERC4626RateProviderFacetDFPkg` | `rateProviders/ERC4626RateProviderFacetDFPkg.sol` | Rate provider for yield tokens |

## Pool Types

Crane supports two Balancer V3 pool types:

| Type | DFPkg | Use Case |
|------|-------|----------|
| Weighted | `BalancerV3WeightedPoolDFPkg` | Custom weight pools (80/20 ETH/TOKEN) |
| Constant Product | `BalancerV3ConstantProductPoolDFPkg` | 50/50 pools (x*y=k) |

## Quick Start: Deploy Weighted Pool

```solidity
import {IBalancerV3WeightedPoolDFPkg, BalancerV3WeightedPoolDFPkg} from "@crane/contracts/protocols/dexes/balancer/v3/pool-weighted/BalancerV3WeightedPoolDFPkg.sol";
import {TokenConfig, TokenType} from "@balancer-labs/v3-interfaces/contracts/vault/VaultTypes.sol";

contract MyFactory {
    BalancerV3WeightedPoolDFPkg public poolDFPkg;

    function deployPool(
        IERC20 tokenA,
        IERC20 tokenB
    ) external returns (address pool) {
        TokenConfig[] memory tokenConfigs = new TokenConfig[](2);
        tokenConfigs[0] = TokenConfig({
            token: tokenA,
            tokenType: TokenType.STANDARD,
            rateProvider: IRateProvider(address(0)),
            paysYieldFees: false
        });
        // Additional implementation...
    }
}
```