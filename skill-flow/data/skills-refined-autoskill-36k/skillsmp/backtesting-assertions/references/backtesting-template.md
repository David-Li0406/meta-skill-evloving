# Backtesting Template

## Example Test
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {CredibleTestWithBacktesting} from "credible-std/CredibleTestWithBacktesting.sol";
import {BacktestingTypes} from "credible-std/utils/BacktestingTypes.sol";
import {MyAssertion} from "../../assertions/src/MyAssertion.a.sol";

contract MyBacktestingTest is CredibleTestWithBacktesting {
    function testBacktest_RecentBlocks() public {
        string memory rpcUrl;
        try vm.envString("MAINNET_RPC_URL") returns (string memory url) {
            rpcUrl = url;
        } catch {
            return; // Skip if RPC not configured
        }

        BacktestingTypes.BacktestingResults memory results = executeBacktest(
            BacktestingTypes.BacktestingConfig({
                targetContract: 0x1111111111111111111111111111111111111111,
                endBlock: 20000000,
                blockRange: 50,
                assertionCreationCode: type(MyAssertion).creationCode,
                assertionSelector: MyAssertion.assertionInvariant.selector,
                rpcUrl: rpcUrl,
                detailedBlocks: false,
                useTraceFilter: true,
                forkByTxHash: false
            })
        );

        require(results.assertionFailures == 0, "Backtest failures");
    }
}
```

## Running Backtests
- `FOUNDRY_PROFILE=backtest-assertions pcl test --ffi`
- Set `ffi = true` in the backtest profile to avoid `--ffi`.
- If the script path is not found, set `CREDIBLE_STD_PATH` to the credible-std repo root.

## Config Tips
- `useTraceFilter = true` detects internal calls; requires RPC support.
- If your provider does not support `trace_filter`, set `useTraceFilter = false` (block scanning).
- `forkByTxHash = true` replays prior txs in the block for exact state (slow).
- Use `blockRange = 1` with a known exploit block to validate detection.
- For large ranges, prefer paid RPC endpoints to avoid rate limits.

## Foundry Profile Snippet
```toml
[profile.backtest-assertions]
src = "assertions/src"
test = "assertions/test/backtest"
out = "assertions/out"
libs = ["lib"]
solc = "0.8.29"
optimizer = true
optimizer_runs = 200
ffi = true
```

## Result Buckets
- `PASS`: assertion ran and passed.
- `NEEDS_REVIEW`: selector mismatch or prestate issues.
- `ASSERTION_FAIL`: assertion reverted (often false positive or gas cap).
- `UNKNOWN_ERROR`: RPC or unexpected execution error.

## Debugging
- Reduce `blockRange` around the failing block.
- Flip `forkByTxHash = true` when state dependencies are suspected.
- Use `pcl test -vvvv` for full logs and traces.
