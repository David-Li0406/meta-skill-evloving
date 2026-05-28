---
title: Get Vault APY and Interest Rates
impact: HIGH
impactDescription: Essential for yield comparison and strategy decisions
tags: vault, apy, interest-rate, lens, query
---

## Get Vault APY and Interest Rates

Understanding APY is critical for comparing yield opportunities and making informed lending/borrowing decisions on Euler.

**Incorrect (reading raw interest rate without conversion):**

```solidity
// The interestRate() returns the per-second interest rate (SPY)
// NOT the APY - this value will be extremely small and misleading
uint256 rate = IEVault(vault).interestRate();
// rate = 1000000000 (this is NOT 100% APY!)
```

**Correct (using VaultLens for complete APY data):**

```typescript
import { VaultLens } from '@eulerxyz/evk-periphery';

// VaultLens provides pre-calculated APY values
const vaultInfo = await vaultLens.getVaultInfoDynamic(vaultAddress);

// Access the IRM info which contains calculated APYs
const irmInfo = vaultInfo.irmInfo;
const interestRateInfo = irmInfo.interestRateInfo[0];

// borrowAPY - what borrowers pay (already converted to annual %)
const borrowAPY = interestRateInfo.borrowAPY;

// supplyAPY - what suppliers earn (accounts for utilization and fees)
const supplyAPY = interestRateInfo.supplyAPY;

// borrowSPY - raw per-second rate if you need it
const borrowSPY = interestRateInfo.borrowSPY;

console.log(`Supply APY: ${supplyAPY / 1e25}%`);
console.log(`Borrow APY: ${borrowAPY / 1e25}%`);
```

**Correct (calculating APY from SPY manually in Solidity):**

```solidity
// Constants for APY calculation
uint256 constant SECONDS_PER_YEAR = 365.2425 days;
uint256 constant ONE = 1e27; // RAY precision

// Convert per-second rate to APY using compound interest formula
// APY = (1 + SPY)^SECONDS_PER_YEAR - 1
function calculateAPY(uint256 borrowSPY) public pure returns (uint256) {
    // Use RPow for precise exponentiation
    uint256 compounded = RPow.rpow(ONE + borrowSPY, SECONDS_PER_YEAR, ONE);
    return compounded - ONE;
}

// For supply APY, account for utilization and interest fee
function calculateSupplyAPY(
    uint256 borrowSPY,
    uint256 totalCash,
    uint256 totalBorrows,
    uint256 interestFee
) public pure returns (uint256) {
    uint256 borrowAPY = calculateAPY(borrowSPY);
    uint256 totalAssets = totalCash + totalBorrows;
    if (totalAssets == 0) return 0;
    
    uint256 utilization = (totalBorrows * ONE) / totalAssets;
    uint256 feeAdjusted = borrowAPY * (1e4 - interestFee) / 1e4;
    return (feeAdjusted * utilization) / ONE;
}
```

The VaultLens approach is preferred as it handles edge cases and provides additional useful data like collateral LTV info, oracle prices, and IRM parameters.

**Alternative: Using UtilsLens for quick APY queries**

```typescript
// UtilsLens provides a simpler API for just APY data
const [borrowAPY, supplyAPY] = await utilsLens.read.getAPYs([vaultAddress]);
console.log(`Borrow APY: ${formatUnits(borrowAPY, 25)}%`);
console.log(`Supply APY: ${formatUnits(supplyAPY, 25)}%`);
```

See also: [Lens Contracts for Data Queries](tools-lens) for comprehensive Lens documentation.

Reference: [VaultLens.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Lens/VaultLens.sol)
