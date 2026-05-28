---
name: crane-camelot
description: Use this skill when you need to interact with Camelot DEX on Arbitrum, including operations like swaps, deposits, and understanding asymmetric fees.
---

# Crane Camelot V2 Integration

Crane provides Camelot V2 integration with a service library, stubs, and test infrastructure. Camelot differs from standard Uniswap V2 forks by supporting asymmetric (directional) fees.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `CamelotV2Service` | `services/CamelotV2Service.sol` | Swap, deposit, withdraw operations |
| `CamelotV2RouterAwareRepo` | `CamelotV2RouterAwareRepo.sol` | Router dependency injection |
| `CamelotV2FactoryAwareRepo` | `CamelotV2FactoryAwareRepo.sol` | Factory dependency injection |
| `TestBase_CamelotV2` | `test/bases/TestBase_CamelotV2.sol` | Full protocol deployment |

## Key Difference: Asymmetric Fees

Camelot pools have **directional fees** - different fees for each swap direction:

```solidity
// Camelot's getReserves returns fees for each direction
(uint112 reserve0, uint112 reserve1, uint16 token0feePercent, uint16 token1FeePercent) = pool.getReserves();

// token0feePercent: Fee when swapping token0 → token1
// token1FeePercent: Fee when swapping token1 → token0
```

## Quick Start: Execute Swap

```solidity
import {CamelotV2Service} from "@crane/contracts/protocols/dexes/camelot/v2/services/CamelotV2Service.sol";
import {ICamelotV2Router} from "@crane/contracts/interfaces/protocols/dexes/camelot/v2/ICamelotV2Router.sol";
import {ICamelotPair} from "@crane/contracts/interfaces/protocols/dexes/camelot/v2/ICamelotPair.sol";

contract CamelotSwapper {
    ICamelotV2Router public router;

    function swap(
        ICamelotPair pool,
        IERC20 tokenIn,
        IERC20 tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        tokenIn.transferFrom(msg.sender, address(this), amountIn);

        amountOut = CamelotV2Service._swap(
            router,
            pool,
            amountIn,
            tokenIn,
            tokenOut,
            address(0)  // referrer (optional)
        );
    }
}
```

## Service Operations

### Deposit (Add Liquidity)

```solidity
function _deposit(
    ICamelotV2Router router,
    IERC20 tokenA,
    IERC20 tokenB,
    uint256 amountADesired,
    uint256 amountBDesired
) internal returns (uint256 amountA, uint256 amountB) {
    // Implementation for adding liquidity
}
```