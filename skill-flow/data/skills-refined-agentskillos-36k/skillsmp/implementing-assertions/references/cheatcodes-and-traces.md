# Cheatcodes and Traces

## Forking
- `forkPreTx()` and `forkPostTx()` switch global pre/post state.
- `forkPreCall(id)` and `forkPostCall(id)` switch state around a specific call.
- If you do not call a fork function, assertions run against post-state by default.

## Call Inputs
- `getCallInputs(target, selector)` returns only CALLs.
- `getDelegateCallInputs` isolates delegate calls (useful for proxies).
- `getStaticCallInputs` and `getCallCodeInputs` target other call types.
- `getAllCallInputs` includes CALL/STATICCALL/DELEGATECALL/CALLCODE and may duplicate proxy paths.
- Filter proxy duplicates by comparing `bytecode_address` and `target_address`; keep the entry that represents the intended code path (often the one where they are equal).
- Call inputs include `caller`, `value`, `gas_limit`, `bytecode_address`, `target_address`, and `id` for per-call forking.
- Call input arrays can be large; test worst-case sizes to stay under the 300k gas cap.
- For router wrappers (batch/call entrypoints), decode nested calldata to extract the real target and account.
- For delegatecall batches, `getAllCallInputs` is the only way to see nested items; dedupe targets/accounts.
- For packed calldata protocols, decode inputs using the protocol's bit layout before applying invariants.
- If a protocol uses sentinel values (e.g., max uint for "full repay"), replace with the pre-state balance/debt.

## Logs
- `getLogs()` returns all logs for the triggering transaction.
- Filter by `emitter` and `topics[0]` (event signature).

## State Changes
- `getStateChanges(target, slot)` returns the initial value plus subsequent changes for that slot.
- Use `getStateChangesUint/Address/Bool` helpers when possible.
- If no changes occurred, the array is empty; reverted changes are not included.
- Ordering is per-slot only; do not assume cross-slot timing alignment.

## Helpers
- `getAssertionAdopter()` returns the protected contract for the current run.
- `load(target, slot)` reads a storage slot directly.

## Console Logging (Debugging)
`console.log` accepts only strings. Use `string.concat` and `Strings.toString` for numbers:
```solidity
import {console} from "forge-std/console.sol";
import {Strings} from "openzeppelin-contracts/contracts/utils/Strings.sol";

function assertionDebug() external {
    uint256 value = 123;
    console.log(string.concat("Value: ", Strings.toString(value)));
}
```

## Triggers
- `registerBalanceChangeTrigger` fires on ETH balance changes for the adopter.
- `registerCallTrigger(fn)` and `registerStorageChangeTrigger(fn)` fire on any call/slot change; avoid unless you truly need global coverage.

## External Call Verification
- To ensure a downstream call occurred (e.g., bridge send), query `getCallInputs` on the callee after `forkPostCall`.

## Notes
- Internal Solidity calls are not traced unless they are externalized via `this.`.
- For nested batches, use `forkPreCall(id)` to detect whether you are inside a batch.
- `getAssertionAdopter()` is only available in `triggers()` and assertion functions (not constructors).
- Use `ph.load` in assertions; `vm.load` is unavailable.
- Use `staticcall` to probe optional interfaces; skip checks when unsupported.
- Enumerating modified mapping keys is not supported; derive keys from call inputs or logs.
- For intra‑tx stability checks, use `forkPreTx()` as a baseline and `forkPostCall(id)` per call.

## Intra-Transaction Monitoring Example
Check intermediate states after each call within a transaction:
```solidity
function assertionIntraTxPriceDeviation() external {
    IOracle oracle = IOracle(ph.getAssertionAdopter());

    // Get baseline before transaction
    ph.forkPreTx();
    uint256 initialPrice = oracle.price();
    uint256 maxPrice = (initialPrice * 110) / 100; // +10%
    uint256 minPrice = (initialPrice * 90) / 100;  // -10%

    // Check final state
    ph.forkPostTx();
    uint256 finalPrice = oracle.price();
    require(finalPrice >= minPrice && finalPrice <= maxPrice, "Final price deviation");

    // Check each intermediate state
    PhEvm.CallInputs[] memory updates = ph.getCallInputs(
        address(oracle),
        oracle.updatePrice.selector
    );

    for (uint256 i = 0; i < updates.length; i++) {
        ph.forkPostCall(updates[i].id);
        uint256 intermediatePrice = oracle.price();
        require(
            intermediatePrice >= minPrice && intermediatePrice <= maxPrice,
            "Intra-tx price deviation"
        );
    }
}
```
