---
name: crane-deployment
description: Use this skill when you need guidance on deploying Diamond proxies and facets using Crane's factory system, particularly for deterministic cross-chain deployments.
---

# Crane Deployment Patterns

Crane uses a two-factory system for deterministic cross-chain deployments of Diamond proxies.

## Factory Hierarchy

```
Create3Factory                    # Deploys facets, packages, and any contract
    └── DiamondPackageCallBackFactory   # Deploys Diamond proxy instances from packages
```

## Deployment Flow

### Step 1: Initialize Factories

In test `setUp()` or deployment scripts:

```solidity
(ICreate3Factory factory, IDiamondPackageCallBackFactory diamondFactory) =
    InitDevService.initEnv(address(this));
```

### Step 2: Deploy Facets

Use Create3Factory to deploy facets with deterministic addresses:

```solidity
IFacet erc20Facet = factory.deployFacet(
    type(ERC20Facet).creationCode,
    abi.encode(type(ERC20Facet).name)._hash()  // Salt from name hash
);
```

### Step 3: Deploy Package

Deploy package with facet references in constructor:

```solidity
IERC20DFPkg erc20Pkg = IERC20DFPkg(address(
    factory.deployPackageWithArgs(
        type(ERC20DFPkg).creationCode,
        abi.encode(IERC20DFPkg.PkgInit({ erc20Facet: erc20Facet })),  // Constructor args
        abi.encode(type(ERC20DFPkg).name)._hash()  // Salt
    )
));
```

### Step 4: Deploy Diamond Proxy Instances

```solidity
// Option A: Via package's deploy() helper
IERC20 token = erc20Pkg.deploy(diamondFactory, "Token", "TKN", 18, 1000e18, recipient, bytes32(0));

// Option B: Via factory directly
address proxy = diamondFactory.deploy(pkg, abi.encode(pkgArgs));
```

## Key Components

| Component | Purpose |
|-----------|---------|
| `Create3Factory` | Deploys any contract with deterministic addresses via CREATE3 |
| `DiamondPackageCallBackFactory` | Deploys Diamond proxies, calls `initAccount()` via delegatecall |
| `IDiamondFactoryPackage` | Interface for packages - bundles facets + initialization logic |
| `InitDevService` | Library to bootstrap the factory system in tests |

## Create3Factory Methods

### `deployFacet()`

Deploy a facet (no constructor args):

```solidity
IFacet facet = factory.deployFacet(
    type(MyFacet).creationCode,
    salt
);
```

### `deployPackageWithArgs()`

Deploy a package with constructor arguments.