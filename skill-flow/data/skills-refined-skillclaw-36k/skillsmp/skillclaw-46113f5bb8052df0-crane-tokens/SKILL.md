---
name: crane-tokens
description: Use this skill when you need to deploy ERC20 tokens, create tokens, implement token standards, or require guidance on using Crane's Diamond Factory Packages.
---

# Crane Token Components

Crane provides pre-built Diamond Factory Packages (DFPkg) for deploying ERC20, ERC20Permit, and ERC4626 tokens as Diamond proxies.

## Token Package Selection

| Need                | Package                                      | Features                             |
|---------------------|----------------------------------------------|--------------------------------------|
| Basic ERC20         | `ERC20DFPkg`                                | Transfer, approve, metadata          |
| ERC20 + Permit      | `ERC20PermitDFPkg`                          | + EIP-2612 gasless approvals         |
| Full-featured token | `ERC20PermitMintBurnLockedOwnableDFPkg`    | + Mint/burn with owner control      |

## Quick Start: Deploy ERC20 with Permit

```solidity
import {ERC20PermitDFPkg, IERC20PermitDFPkg} from "@crane/contracts/tokens/ERC20/ERC20PermitDFPkg.sol";
import {IERC20} from "@crane/contracts/interfaces/IERC20.sol";

// 1. Deploy facets (typically done once via FactoryService)
IFacet erc20Facet = factory.deployFacet(type(ERC20Facet).creationCode, salt);
IFacet erc5267Facet = factory.deployFacet(type(ERC5267Facet).creationCode, salt);
IFacet erc2612Facet = factory.deployFacet(type(ERC2612Facet).creationCode, salt);

// 2. Deploy package with facet references
ERC20PermitDFPkg pkg = new ERC20PermitDFPkg(IERC20PermitDFPkg.PkgInit({
    erc20Facet: erc20Facet,
    erc5267Facet: erc5267Facet,
    erc2612Facet: erc2612Facet
}));

// 3. Deploy token instance via Diamond factory
IERC20 token = IERC20(diamondFactory.deploy(
    pkg,
    abi.encode(IERC20PermitDFPkg.PkgArgs({
        name: "My Token",
        symbol: "MTK",
        decimals: 18,
        totalSupply: 1_000_000e18,
        recipient: msg.sender,
        optionalSalt: bytes32(0)
    }))
));
```

## Available Packages

### ERC20DFPkg

Basic ERC20 token with metadata.

**PkgInit** (constructor):
```solidity
struct PkgInit {
    IFacet erc20Facet;
}
```

**PkgArgs** (deployment):
```solidity
struct PkgArgs {
    string name;
    string symbol;
    uint8 decimals;      // Defaults to 18 if 0
    uint256 totalSupply; // Initial mint amount
    address recipient;   // Required if totalSupply > 0
    bytes32 optionalSalt;
}
```

**Interfaces**: `IERC20`, `IERC20Metadata`

### ERC20PermitDFPkg

ERC20 with EIP-2612 permit (gasless approvals).

**PkgInit**:
```solidity
struct PkgInit {
    IFacet erc20Facet;
}
```