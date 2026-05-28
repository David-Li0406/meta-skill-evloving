---
name: solidity-test-writer
description: Use this skill when you need to write comprehensive unit and integration tests for EigenLayer Solidity contracts, following established conventions for both types of tests.
---

# Skill body

## Overview

This skill encompasses the creation of both unit and integration tests for EigenLayer Solidity contracts. It provides guidelines for structuring tests, naming conventions, and best practices to ensure thorough coverage and maintainability.

## Unit Tests

### Test File Structure

Each unit test file should follow this structure:

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
/// @notice Base contract for all ContractUnderTest unit tests
contract ContractUnderTestUnitTests is EigenLayerUnitTestSetup, IContractErrors, IContractEvents, IContractTypes {
    // Test state variables
    ContractUnderTest contractUnderTest;

    function setUp() public virtual override {
        EigenLayerUnitTestSetup.setUp();
        // Deploy and initialize contract under test
        // Set up default test values
        // Configure mocks
    }

    // Helper functions
}

/// @title ContractUnderTestUnitTests_functionName
/// @notice Unit tests for ContractUnderTest.functionName
contract ContractUnderTestUnitTests_functionName is ContractUnderTestUnitTests {
    function setUp() public override {
        super.setUp();
        // Function-specific setup
    }

    // Revert tests
    function test_Revert_Paused() public { }
    function test_Revert_NotPermissioned() public { }
    function test_Revert_InvalidInput() public { }

    // Success tests
    function test_functionName_Success() public { }

    // Fuzz tests
    function testFuzz_functionName_VariableName(uint256 value) public { }
}
```

### Test Contract Naming Convention

- **Base contract**: `{ContractName}UnitTests`
- **Per-function contracts**: `{ContractName}UnitTests_{functionName}`

### Test Function Naming Convention

| Pattern | Purpose |
|---------|---------|
| `test_Revert_Paused` | Test function reverts when paused |
| `test_Revert_NotPermissioned` | Test function reverts for unauthorized callers |
| `test_Revert_NotOwner` | Test function reverts for non-owner |
| `test_Revert_Invalid{Thing}` | Test function reverts for invalid inputs |

## Integration Tests

### Overview

Integration tests orchestrate the deployment of all EigenLayer core contracts to test high-level user flows across multiple contracts. There are three test modes:

1. **Local Integration Tests** - Deploy fresh contracts and test user flows.
2. **Fork Tests** - Fork mainnet, upgrade all contracts to latest implementations, then run the integration test suite.
3. **Upgrade Tests** - Fork mainnet, perform actions on OLD contracts, then upgrade and verify compatibility.

### Test Function Signature

**All integration test functions MUST:**
1. Be named `testFuzz_action1_action2_...` describing the flow.
2. Take `uint24 _random` (or `_r`) as the only parameter - this seeds randomness.
3. Use the `rand(_random)` modifier to initialize the random seed.

```solidity
function testFuzz_deposit_delegate_queue_complete(uint24 _random) public rand(_random) {
    // Test implementation
}
```

The `rand()` modifier initializes the test's random seed, which is used by helper functions to generate deterministic random values for reproducible tests.

### Test File Locations

| Type | Location |
|------|----------|
| Normal integration tests | `src/test/integration/tests/` |
| Upgrade tests | `src/test/integration/tests/upgrade/` |
| Check functions | `src/test/integration/IntegrationChecks.t.sol` |
| Multichain checks | `src/test/integration/MultichainIntegrationChecks.t.sol` |

### Core Principles

1. **All Actions Must Be Called Through User Contracts**: Never call contracts directly. Use the `User` or `AVS` actor contracts.
2. **Every Action Must Be Followed By a Check**: After each numbered action, verify state changes using `check_*` functions.

By following these guidelines, you can ensure that your Solidity tests are well-structured, maintainable, and effective in verifying the functionality of EigenLayer contracts.