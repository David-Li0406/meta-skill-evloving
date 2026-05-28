# Test Patterns

## Registering Assertions
- `cl.assertion({ adopter, createData, fnSelector });` runs on the next transaction only.
- Register again for each test action.
- Only one assertion function can be registered at a time; test functions in isolation.
- Put all setup before `cl.assertion()`; the very next call consumes it.
- The next call must match a trigger registered for `fnSelector`, or the assertion will not execute.
- Passing assertions persist state changes; failing assertions revert and roll back state.

## Profiles
- Use `FOUNDRY_PROFILE=assertions` (or unit/fuzz/backtest profiles) to isolate assertion builds.

## Constructor Args
- Use `abi.encodePacked(type(MyAssertion).creationCode, abi.encode(arg1, arg2))`.

## Batch Operations
- Use a helper contract that performs multiple operations in one call.
- Avoid low-level fallback calls when possible; revert reasons are cleaner.
- If you must use fallback, call `address(batch).call("")` and assert on the `success` flag.
- Internal calls do not trigger assertions; register on external entrypoints.

## Time Windows and Modes
- Use `vm.warp` to test just-before and just-after window expiration.
- Cover mode switches (sync/async, paused/unpaused) on both sides.

## Failure Path Checks
- When a call should fail, assert state is unchanged (balances, debts, indexes).
- For gatekeeping invariants (borrowable/frozen/paused), test both revert and state‑no‑change.
- Use `assertApproxEqAbs(..., 1)` for scaled balance rounding.
- For liveness invariants, assert full repay/withdraw succeeds under the expected preconditions.
- For flashloans, test both repayment success and insufficient repayment failure.
- Include sentinel max values for "full repay/withdraw" to exercise normalization logic.

## Prank Consumption
- Do not inline view calls after `vm.prank()`: the inner call consumes the prank.
- Store values before `vm.prank()` and before `cl.assertion()`.

## Protocol Mocking
Well-implemented protocols prevent invalid states, making it impossible to test assertion failure paths against the real contract. Use mocks to verify assertions catch violations:
- Build minimal mock contracts that can be forced into invalid states (e.g., a mock vault that allows unauthorized fee changes).
- Use harness contracts that expose internal setters for testing.
- This is expected behavior: if you cannot trigger an assertion failure against the real protocol, that's a sign the protocol is secure—but you still need to verify the assertion logic works.

## Fuzzing
- Fuzz amounts and sequence length to stress loops and rounding paths.
- Include `vm.assume` guards to avoid invalid setups.
- Consider a dedicated fuzz profile (e.g., `FOUNDRY_PROFILE=fuzz-assertions`) to keep local runs fast.

## Property-Based Testing
- Use roundtrip properties for encode/decode pairs.
- Use idempotence for normalization or formatting logic.
- Use invariants for state transitions (pre/post).

## Backtesting
- Use `CredibleTestWithBacktesting` and `executeBacktest` with a real RPC.
- Run with `--ffi` or a profile that sets `ffi = true`.
- Prefer `useTraceFilter = true` to capture internal calls; use `forkByTxHash` for exact state debugging.
- Expect result buckets like PASS, NEEDS_REVIEW (selector mismatch / prestate issues), ASSERTION_FAIL, UNKNOWN_ERROR.
- Skip or early-return if RPC env vars are missing.
- Use one backtest per assertion selector to isolate failures.

## PCL Test Parity
- `pcl test` is a fork of `forge test` with largely identical flags and behavior, but it adds `cl.addAssertion` for assertion tests.
- Use `pcl test` for assertions and reserve `forge test` for regular protocol tests.
- Use `forge-std/Test` for available helpers and cheatcodes.
- Refer to the Forge Book for detailed cheatcode behavior and test flags.
- Use `vm.expectRevert` for negative cases instead of `testFail` (deprecated in Foundry v1.0).
