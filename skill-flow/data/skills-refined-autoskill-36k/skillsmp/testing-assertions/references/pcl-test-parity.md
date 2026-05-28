# PCL Test Parity

`pcl test` is a fork of `forge test` with largely identical flags and behavior, but it adds the `cl.addAssertion` cheatcode required for assertion tests. Use `pcl test` for assertions and reserve `forge test` for regular protocol tests; note `pcl` can lag Forge versions so newer flags may be missing.

## Test Discovery
- Any Solidity function starting with `test` is a test.
- Tests can live anywhere in the source tree; convention is `test/*.t.sol`.

## Common Filters
- `--match-test <regex>` / `--no-match-test <regex>`
- `--match-contract <regex>` / `--no-match-contract <regex>`
- `--match-path <glob>` / `--no-match-path <glob>`

## Verbosity
- `-vv` logs emitted during tests.
- `-vvv` execution traces for failing tests.
- `-vvvv` traces for all tests + setup traces for failures.
- `-vvvvv` traces for all tests with storage changes and line-number backtraces.

## Useful Flags
- `--watch` (re-run on changes), `--run-all` to re-run all tests in watch mode.
- `--fork-url <URL>` and `--fork-block-number <N>` for forked testing.
- `--gas-report` to print a gas report.

## Forge Std
- Use `forge-std/Test.sol` to get `vm`, std assertions, and cheat wrappers.
- `Vm.sol` defines the cheatcode interface used by `vm`.
- `Test.sol` also brings `StdAssertions`, `StdCheats`, `StdInvariant`, `StdUtils`, `stdError`, `stdMath`, and `stdstore`.
- Use `console2` for logging that decodes cleanly in Foundry traces.
