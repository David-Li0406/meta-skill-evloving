---
name: crane-testing
description: Use this skill when you need guidance on Crane's testing infrastructure for writing comprehensive smart contract tests, including topics like "testbase", "behavior library", "invariant test", and "fuzz test".
---

# Crane Testing Patterns

Crane uses structured testing patterns with TestBase contracts, Behavior libraries, and Handler contracts for comprehensive coverage.

## Test Directory Structure

Test infrastructure lives in `contracts/`, while test specs are located in `test/`:

```
contracts/                              # Test infrastructure WITH the code
├── access/ERC8023/
│   ├── MultiStepOwnableRepo.sol
│   ├── MultiStepOwnableFacet.sol
│   └── TestBase_IMultiStepOwnable.sol  # TestBase next to implementation
├── introspection/ERC165/
│   ├── ERC165Facet.sol
│   ├── TestBase_IERC165.sol            # Behavior testing
│   └── Behavior_IERC165.sol            # Validation library
└── test/
    ├── stubs/                          # Example implementations
    ├── comparators/                    # Assertion helpers
    └── behaviors/                      # Shared behavior utilities

test/foundry/spec/                      # Actual test specs mirror contracts/
├── access/ERC8023/
│   └── MultiStepOwnable.t.sol
└── introspection/ERC165/
    └── ERC165Facet.t.sol
```

## TestBase Pattern

Two types of TestBase contracts exist:

### Protocol Setup TestBase

Sets up protocol infrastructure with inheritance chains:

```solidity
abstract contract TestBase_CamelotV2 is TestBase_Weth9 {
    ICamelotFactory internal camelotV2Factory;
    ICamelotV2Router internal camelotV2Router;

    function setUp() public virtual override {
        TestBase_Weth9.setUp();  // Call parent setUp
        if (address(camelotV2Factory) == address(0)) {
            camelotV2Factory = new CamelotFactory(feeToSetter);
        }
        if (address(camelotV2Router) == address(0)) {
            camelotV2Router = new CamelotRouter(address(camelotV2Factory), address(weth));
        }
    }
}
```

### Behavior TestBase

Defines expected behavior via virtual functions:

```solidity
abstract contract TestBase_IFacet is Test {
    IFacet internal testFacet;

    function setUp() public virtual {
        testFacet = facetTestInstance();
    }

    // Virtual functions - inheritors return expected values
    function facetTestInstance() public virtual returns (IFacet);
    function controlFacetInstance() public virtual returns (IFacet);
}
```