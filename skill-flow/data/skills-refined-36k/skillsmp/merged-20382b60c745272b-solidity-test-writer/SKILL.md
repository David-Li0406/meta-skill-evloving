---
name: solidity-test-writer
description: Use this skill when you need to write comprehensive integration or unit tests for EigenLayer Solidity contracts, covering user flows, function behaviors, and edge cases.
---

# Solidity Test Writer

Write comprehensive integration and unit tests for EigenLayer Solidity contracts following the project's established conventions.

## Overview

This skill encompasses two types of tests:

1. **Integration Tests** - Test high-level user flows across multiple contracts.
2. **Unit Tests** - Test individual functions and their behaviors.

### Integration Tests

Integration tests orchestrate the deployment of all EigenLayer core contracts to test user flows, cross-contract interactions, and upgrade scenarios. There are three test modes:

- **Local Integration Tests** - Deploy fresh contracts and test user flows.
- **Fork Tests** - Fork mainnet, upgrade all contracts to the latest implementations, then run the integration test suite.
- **Upgrade Tests** - Fork mainnet, perform actions on old contracts, then upgrade and verify compatibility.

#### Test Function Signature

All integration test functions must:
- Be named `testFuzz_action1_action2_...` describing the flow.
- Take `uint24 _random` as the only parameter to seed randomness.
- Use the `rand(_random)` modifier to initialize the random seed.

```solidity
function testFuzz_deposit_delegate_queue_complete(uint24 _random) public rand(_random) {
    // Test implementation
}
```

#### Core Principles

1. **All Actions Must Be Called Through User Contracts** - Use the `User` or `AVS` actor contracts.
2. **Every Action Must Be Followed By a Check** - Verify state changes using `check_*` functions.
3. **Actions Must Be Numbered** - Use comments to number each action step for clarity.

### Unit Tests

Unit tests focus on individual functions within contracts, ensuring they behave as expected under various conditions.

#### Test File Structure

Each test file follows this structure:

```solidity
// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.27;

// Import the contract under test
import "src/contracts/path/to/ContractUnderTest.sol";
// Import the appropriate test setup
import "src/test/utils/EigenLayerUnitTestSetup.sol";
// Import any required mocks
import "src/test/mocks/SomeMock.sol";

/// @title ContractUnderTestUnitTests
contract ContractUnderTestUnitTests is EigenLayerUnitTestSetup {
    ContractUnderTest contractUnderTest;

    function setUp() public virtual override {
        EigenLayerUnitTestSetup.setUp();
        // Deploy and initialize contract under test
    }

    // Helper functions
}

/// @title ContractUnderTestUnitTests_functionName
contract ContractUnderTestUnitTests_functionName is ContractUnderTestUnitTests {
    function setUp() public override {
        super.setUp();
        // Function-specific setup
    }

    // Revert tests
    function test_Revert_Paused() public { }
    function test_functionName_Success() public { }
}
```

#### Coverage Requirements

For each function, ensure:
1. **Revert Cases** - Test all revert conditions.
2. **Happy Path** - Test successful execution and verify emitted events.
3. **Fuzz Tests** - Use bounded inputs to test edge cases.

### Running Tests

To run tests, use the following commands:

```bash
# Run all integration tests
forge t --mc Integration

# Run all unit tests
forge test --no-match-contract Integration

# Run specific test
forge test --match-test test_functionName_Success
```

### Naming Conventions

- **Integration Test Contracts**: `Integration_FlowName_Base`, `Integration_FlowName_Variant`
- **Unit Test Contracts**: `{ContractName}UnitTests`, `{ContractName}UnitTests_{functionName}`
- **Test Function Names**: `testFuzz_action1_action2_...`, `test_Revert_{Condition}`, `test_{functionName}_Success`

## Example: Complete Integration Test

Reference: `src/test/integration/tests/DualSlashing.t.sol`

This file demonstrates:
- Base contract with `_init()` for shared setup.
- Multiple test contracts inheriting from base.
- Numbered action steps.
- `check_*` after every action.

## Example: Complete Unit Test Contract

Reference: `src/test/unit/ContractUnit.t.sol`

This file demonstrates:
- Base test contract with setUp and helpers.
- Per-function test contracts.
- Comprehensive revert testing.

## Checklist Before Writing Tests

1. Identify the user flow or function to test.
2. Determine if it's a normal test or upgrade test.
3. Identify all actors needed (stakers, operators, AVSs).
4. Plan the numbered action steps for integration tests.
5. Identify which `check_*` functions to use after each action.
6. For unit tests, identify all revert conditions, emitted events, and state changes.