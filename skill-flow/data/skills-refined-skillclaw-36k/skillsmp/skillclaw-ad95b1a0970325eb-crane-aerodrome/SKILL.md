---
name: crane-aerodrome
description: Use this skill when you need to integrate with Aerodrome DEX on Base, perform swaps, manage liquidity in volatile or stable pools, or utilize Slipstream and concentrated liquidity features.
---

# Crane Aerodrome Integration

Crane provides comprehensive Aerodrome v1 and Slipstream integration with services, stubs, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `AerodromServiceVolatile` | `services/AerodromServiceVolatile.sol` | Volatile pool operations (xy=k) |
| `AerodromServiceStable` | `services/AerodromServiceStable.sol` | Stable pool operations (x³y + xy³ = k) |
| `AerodromeRouterAwareRepo` | `aware/AerodromeRouterAwareRepo.sol` | Router dependency injection |
| `AerodromePoolMetadataRepo` | `aware/AerodromePoolMetadataRepo.sol` | Pool metadata storage |
| `TestBase_Aerodrome` | `test/bases/TestBase_Aerodrome.sol` | Full protocol deployment |
| `TestBase_Aerodrome_Pools` | `test/bases/TestBase_Aerodrome_Pools.sol` | Pool creation helpers |
| `SlipstreamRewardUtils` | `slipstream/SlipstreamRewardUtils.sol` | Concentrated liquidity reward calculations |

## Pool Types

Aerodrome has two pool types with different AMM curves:

| Type | Curve | Use Case | Service |
|------|-------|----------|---------|
| Volatile | xy = k | ETH/USDC, volatile pairs | `AerodromServiceVolatile` |
| Stable | x³y + xy³ = k | USDC/USDT, stablecoin pairs | `AerodromServiceStable` |

## Quick Start: Volatile Pool Swap

```solidity
import {AerodromServiceVolatile} from "@crane/contracts/protocols/dexes/aerodrome/v1/services/AerodromServiceVolatile.sol";
import {AerodromeRouterAwareRepo} from "@crane/contracts/protocols/dexes/aerodrome/v1/aware/AerodromeRouterAwareRepo.sol";

contract MyVault {
    function swap(IERC20 tokenIn, IERC20 tokenOut, uint256 amount) external {
        IRouter router = AerodromeRouterAwareRepo._router();
        IPoolFactory factory = router.defaultFactory();
        IPool pool = IPool(factory.getPool(address(tokenIn), address(tokenOut), false));

        AerodromServiceVolatile._swapVolatile(
            AerodromServiceVolatile.SwapVolatileParams({
                router: router,
                factory: factory,
                pool: pool,
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                amountIn: amount,
                recipient: address(this)
            })
        );
    }
}
```