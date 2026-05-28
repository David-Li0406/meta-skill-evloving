---
name: credible-layer-assertions-testing
description: Use this skill when you need to validate assertions in the Phylax Credible Layer through unit tests, fuzz tests, or backtesting against historical transactions.
---

# Skill body

## Overview

Build confidence that assertions block invalid transactions and allow valid ones by testing them through various methods.

## Meta-Cognitive Protocol

Adopt the role of a Meta-Cognitive Reasoning Expert.

For every complex problem:
1. **DECOMPOSE**: Break into sub-problems.
2. **SOLVE**: Address each with explicit confidence (0.0-1.0).
3. **VERIFY**: Check logic, facts, completeness, bias.
4. **SYNTHESIZE**: Combine using weighted confidence.
5. **REFLECT**: If confidence < 0.8, identify weakness and retry.

Always output:
- Clear answer
- Confidence level
- Key caveats

## When to Use

- Writing unit, fuzz, or backtesting tests for assertions.
- Investigating false positives or gas-limit risks.
- Validating assertions against real mainnet transactions or known exploits.
- Adding regression tests after protocol or assertion changes.

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

## Quick Start

### For Unit and Fuzz Tests
- Use `CredibleTest` and `cl.assertion(...)` to register a single assertion function for the next transaction.
- **One assertion per test**: `cl.assertion(...)` registers exactly one assertion function. Create separate test functions for each assertion you want to verify.
- Register full assertion contracts with `cl.addAssertion(...)` (usually in `setUp`) so `cl.validate(...)` can find them.

### For Backtesting
1. Place backtest files in `assertions/test/backtest/` (e.g., `VaultAssertion.backtest.t.sol`).
2. Create a test that inherits `CredibleTestWithBacktesting`.
3. Configure `BacktestingConfig` with target contract, block range, and assertion selector.
4. Call `executeBacktest` and assert failures are zero.
5. Run with the backtest profile: `FOUNDRY_PROFILE=assertions-backtest pcl test` (or use `--ffi` flag).

## Workflow for Backtesting
- Pick a target contract (the assertion adopter address).
- Choose `endBlock` and `blockRange`.
- Verify RPC env vars; skip or fallback when missing.
- Prefer `useTraceFilter = true` to detect internal calls; fall back to block scanning if your RPC lacks `trace_filter`.
- For large ranges, use a paid RPC to avoid rate limits; `useTraceFilter` reduces calls.
- Use `forkByTxHash = true` only when debugging state-dependent failures.
- Interpret results: `PASS`, `NEEDS_REVIEW` (selector mismatch or replay failure).