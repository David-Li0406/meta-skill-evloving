---
name: crane-utilities
description: Use this skill when you need utility libraries for collections, math, cryptography, or common operations in Crane Diamond development.
---

# Crane Utility Libraries

Crane provides utility libraries for collections, math, cryptography, and common operations.

## Collections (Sets)

Diamond storage-compatible set implementations for unique value collections.

### Available Set Types

| Type | File | Use Case |
|------|------|----------|
| `AddressSet` | `AddressSetRepo.sol` | Unique addresses (operators, whitelist) |
| `Bytes32Set` | `Bytes32SetRepo.sol` | Unique hashes, identifiers |
| `Bytes4Set` | `Bytes4SetRepo.sol` | Function selectors, interface IDs |
| `StringSet` | `StringSetRepo.sol` | Unique strings |
| `UInt256Set` | `UInt256SetRepo.sol` | Unique numeric IDs |

### Set Operations

```solidity
import {AddressSet, AddressSetRepo} from "@crane/contracts/utils/collections/sets/AddressSetRepo.sol";

// In your Repo
struct Storage {
    AddressSet operators;
}

// Operations
AddressSetRepo._add(set, value);        // Add value, idempotent
AddressSetRepo._remove(set, value);     // Remove value, idempotent
AddressSetRepo._contains(set, value);   // Check presence
AddressSetRepo._length(set);            // Get count
AddressSetRepo._index(set, idx);        // Get value at index
AddressSetRepo._indexOf(set, value);    // Get index of value
AddressSetRepo._asArray(set);           // Get all values as array
```

### Pagination

For large sets, use pagination:

```solidity
// Get page of results
(address[] memory page, bool hasMore) = AddressSetRepo._getPage(
    set,
    pageIndex,   // 0-based page number
    pageSize     // Items per page
);
```

## Math Utilities

### ConstProdUtils

Core AMM math for constant product pools (xy=k):

```solidity
import {ConstProdUtils} from "@crane/contracts/utils/math/ConstProdUtils.sol";

using ConstProdUtils for uint256;

// Calculate output for swap
uint256 amountOut = ConstProdUtils._purchaseQuote(
    amountIn,         // Amount being sold
    reserveIn,        // Reserve of input token
    reserveOut,       // Reserve of output token
    feeNumerator      // Fee (e.g., 9970 for 0.3%)
);

// Calculate input needed for desired output
uint256 amountIn = ConstProdUtils._saleQuote(
    amountOut,
    reserveIn,
    reserveOut,
    feeNumerator
);
```