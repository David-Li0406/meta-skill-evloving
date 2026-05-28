---
name: assertions-testing-and-backtesting
description: Use this skill when you need to validate and backtest assertions in the Phylax Credible Layer against both unit tests and historical transactions.
---

# Assertions Testing and Backtesting

This skill encompasses both testing and backtesting of assertions in the Phylax Credible Layer, ensuring that invalid transactions are blocked while valid ones are allowed.

## Meta-Cognitive Protocol

Adopt the role of a Meta-Cognitive Reasoning Expert.

For every complex problem:
1. **DECOMPOSE**: Break into sub-problems.
2. **SOLVE**: Address each with explicit confidence (0.0-1.0).
3. **VERIFY**: Check logic, facts, completeness, bias.
4. **SYNTHESIZE**: Combine using weighted confidence.
5. **REFLECT**: If confidence <0.8, identify weakness and retry.

For simple questions, skip to direct answer.

Always output:
- Clear answer
- Confidence level
- Key caveats

## When to Use

- Writing unit, fuzz, or backtesting tests for assertions.
- Validating assertions against real mainnet transactions or known exploits.
- Investigating false positives or gas-limit risks.
- Confirming triggers match real protocol entrypoints.

## When NOT to Use

- You need help designing invariants or triggers. Use `designing-assertions`.
- You only need implementation details. Use `implementing-assertions`.

## Test Directory Structure

```
assertions/test/
├── unit/           # Unit tests (.t.sol)
├── fuzz/           # Fuzz tests (.t.sol)
└── backtest/       # Backtest tests (.t.sol)
```

- **Test files**: `{ContractOrFeature}Assertion.t.sol` (e.g., `VaultOwnerAssertion.t.sol`)
- **Test functions**: start with `test` (e.g., `testAssertionSetFeePasses`, `testAssertionSetFeeFails`)

## Running Tests

Run tests by type using Foundry profiles:

- All tests: `FOUNDRY_PROFILE=assertions pcl test`
- Unit only: `FOUNDRY_PROFILE=assertions-unit pcl test`
- Fuzz only: `FOUNDRY_PROFILE=assertions-fuzz pcl test`
- Backtests only: `FOUNDRY_PROFILE=assertions-backtest pcl test`

## Quick Start for Testing Assertions

- Use `CredibleTest` and `cl.assertion(...)` to register a single assertion function for the next transaction.
- **One assertion per test**: `cl.assertion(...)` registers exactly one assertion function. Create separate test functions for each assertion you want to verify.
- Register full assertion contracts with `cl.addAssertion(...)` (usually in `setUp`) so `cl.validate(...)` can find them.

## Quick Start for Backtesting Assertions

1. Place backtest files in `assertions/test/backtest/` (e.g., `VaultAssertion.backtest.t.sol`).
2. Create a test that inherits `CredibleTestWithBacktesting`.
3. Configure `BacktestingConfig` with target contract, block range, and assertion selector.
4. Call `executeBacktest` and assert failures are zero.
5. Run with the backtest profile: `FOUNDRY_PROFILE=assertions-backtest pcl test` (or use `--ffi` flag).

## Core Test Patterns

- **Positive path**: expected to pass and keep state consistent.
- **Negative path**: expected to revert with the assertion message.
- **Edge cases**: zero supply, empty vaults, proxy upgrades, nested batches.

## Gas Limit Checks

- Assertions are capped at 300k gas.
- The happy path is often the most expensive. Test with max sizes.

## Rationalizations to Reject

- "One passing test is enough." Assertions must also fail on violations.
- "The protocol already reverts, so negative tests are pointless." Assertions still need a failing path.
- "Backtesting catches real-world call patterns." It is essential for validating assertions against historical data.

## References

- [Test Patterns](references/test-patterns.md)
- [Backtesting Template](references/backtesting-template.md)
- [PCL Test Parity](references/pcl-test-parity.md)