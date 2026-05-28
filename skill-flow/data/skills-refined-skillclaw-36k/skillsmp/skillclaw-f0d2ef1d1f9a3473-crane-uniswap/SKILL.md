---
name: crane-uniswap
description: Use this skill when you need to integrate with Uniswap DEX, including operations for Uniswap V2, V3, and V4, such as swaps and liquidity management using Crane's service libraries.
---

# Crane Uniswap Integration

Crane provides integration with Uniswap V2, V3, and V4 through services, stubs, libraries, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `UniswapV2Service` | `v2/services/UniswapV2Service.sol` | V2 swap, deposit, withdraw operations |
| `UniswapV2RouterAwareRepo` | `v2/aware/UniswapV2RouterAwareRepo.sol` | Router dependency injection |
| `UniswapV2FactoryAwareRepo` | `v2/aware/UniswapV2FactoryAwareRepo.sol` | Factory dependency injection |
| `TestBase_UniswapV2` | `v2/test/bases/TestBase_UniswapV2.sol` | Full protocol deployment |
| `TestBase_UniswapV2_Pools` | `v2/test/bases/TestBase_UniswapV2_Pools.sol` | Pool creation helpers |
| `UniswapV3Factory` | `v3/UniswapV3Factory.sol` | V3 factory stub |
| `UniswapV3Pool` | `v3/UniswapV3Pool.sol` | V3 pool implementation |
| `UniswapV4Utils` | `v4/utils/UniswapV4Utils.sol` | V4 utility functions |
| `UniswapV4Quoter` | `v4/utils/UniswapV4Quoter.sol` | V4 quote calculations |

## Uniswap V2 (Standard 0.3% Fee)

Uniswap V2 uses a fixed 0.3% fee for transactions:

```solidity
// UniswapV2Service always uses 300 (0.3%) for fee calculations
feePercent = 300;
```

## Quick Start: Execute V2 Swap

```solidity
import {UniswapV2Service} from "@crane/contracts/protocols/dexes/uniswap/v2/services/UniswapV2Service.sol";
import {IUniswapV2Router} from "@crane/contracts/interfaces/protocols/dexes/uniswap/v2/IUniswapV2Router.sol";
import {IUniswapV2Pair} from "@crane/contracts/interfaces/protocols/dexes/uniswap/v2/IUniswapV2Pair.sol";

contract UniswapSwapper {
    IUniswapV2Router public router;

    function swap(
        IUniswapV2Pair pool,
        IERC20 tokenIn,
        IERC20 tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        tokenIn.transferFrom(msg.sender, address(this), amountIn);

        amountOut = UniswapV2Service._swap(
            router,
            pool,
            amountIn,
            tokenIn,
            tokenOut
        );
    }
}
```

## V2 Service Operations

### Deposit (Add Liquidity)

```solidity
function _deposit(
    IUniswapV2Router router,
    IERC20 tokenA,
    IERC20 tokenB,
    uint256 amountA,
    uint256 amountB
) external {
    // Implementation for adding liquidity
}
```