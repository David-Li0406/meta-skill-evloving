---
title: Understanding Risk Managers and Vault Governance
impact: HIGH
impactDescription: Essential for vault governance and risk management
tags: risk, risk manager, curator, governance, roles, security
---

## Understanding Risk Managers and Vault Governance

Risk Managers (governors) are trusted entities responsible for ongoing vault configuration and risk management in Euler V2. They have full control over vault parameters through governance functions.

**Incorrect (assuming anyone can configure vaults):**

```solidity
// WRONG: Only governor can modify vault config
IEVault vault = IEVault(vaultAddress);
vault.setLTV(collateral, 8000, 9000, 0);  // Will revert with E_Unauthorized!
vault.setCaps(100, 50);                    // Will revert with E_Unauthorized!
```

**Complete list of governance functions:**

All functions below require `governorOnly` modifier (caller must be `governorAdmin`):

```solidity
import {IEVault} from "evk/EVault/IEVault.sol";

IEVault vault = IEVault(vaultAddress);

// ═══════════════════════════════════════════════════════════
// GOVERNANCE TRANSFER
// ═══════════════════════════════════════════════════════════

// Transfer governance to new address (or address(0) to renounce)
vault.setGovernorAdmin(newGovernor);

// Set fee receiver (receives governor's share of interest fees)
// If set to address(0), governor forfeits fees to protocol
vault.setFeeReceiver(newFeeReceiver);

// ═══════════════════════════════════════════════════════════
// LTV CONFIGURATION
// ═══════════════════════════════════════════════════════════

// Configure LTV for a collateral asset
// borrowLTV: max LTV for new borrows (in 1e4 scale, e.g., 0.85e4 = 85%)
// liquidationLTV: LTV at which liquidation is possible (must be >= borrowLTV)
// rampDuration: if lowering LTV, seconds to ramp down (prevents instant liquidations)
vault.setLTV(
    collateralVault,    // address of collateral vault
    0.85e4,             // 85% borrow LTV
    0.90e4,             // 90% liquidation LTV  
    0                   // ramp duration (0 for immediate, or seconds to ramp)
);

// IMPORTANT: When lowering liquidation LTV, use rampDuration to give users
// time to adjust positions. Setting rampDuration > 0 when RAISING LTV will revert.

// To disable a collateral, set LTV to 0 (with optional ramp):
vault.setLTV(collateralVault, 0, 0, 7 days); // 7-day ramp to 0

// ═══════════════════════════════════════════════════════════
// CAPS
// ═══════════════════════════════════════════════════════════

// Set supply and borrow caps (in AmountCap format - raw uint16)
// Use AmountCap library to encode/decode
// 0 = unlimited, otherwise encoded value
vault.setCaps(
    supplyCap,   // uint16 encoded supply cap
    borrowCap    // uint16 encoded borrow cap
);

// ═══════════════════════════════════════════════════════════
// INTEREST RATE MODEL
// ═══════════════════════════════════════════════════════════

// Set new interest rate model contract (must conform to the required interface)
vault.setInterestRateModel(newIRMAddress);

// Set interest fee (portion of interest that goes to fees)
// Range: 0 to 1e4 (100%)
// Guaranteed range (no protocol approval needed): 0.1e4 to 1e4 (10% to 100%)
// Outside this range requires protocolConfig approval
vault.setInterestFee(0.1e4);  // 10% interest fee

// ═══════════════════════════════════════════════════════════
// LIQUIDATION PARAMETERS
// ═══════════════════════════════════════════════════════════

// Set maximum liquidation discount
// In 1e4 scale (e.g., 0.15e4 = 15% max discount)
// Cannot be exactly 1e4 (would cause division by zero)
vault.setMaxLiquidationDiscount(0.15e4);  // 15% max discount

// Set liquidation cool-off time (seconds)
// Time that must pass after successful account status check before liquidation
vault.setLiquidationCoolOffTime(0);  // 0 = no cool-off

// ═══════════════════════════════════════════════════════════
// HOOKS AND FLAGS
// ═══════════════════════════════════════════════════════════

// Configure hook target and which operations are hooked
// hookedOps is a bitfield - see Constants.sol for operation flags
vault.setHookConfig(
    hookTargetAddress,  // contract implementing IHookTarget
    hookedOps           // bitfield of operations to hook
);

// IMPORTANT: When hookTarget is address(0) and an operation bit is set in hookedOps,
// that operation is DISABLED (will revert). This can be used for:
// - Emergency pause of specific operations (deposit, borrow, withdraw, etc.)
// - Permanently disabling certain features (e.g., no borrowing allowed)
// - Rapid response to security incidents

// Example: Emergency disable all deposits and borrows
vault.setHookConfig(address(0), (1 << 0) | (1 << 5));  // OP_DEPOSIT | OP_BORROW

// Example: Install a custom hook for deposits only
vault.setHookConfig(myHookContract, 1 << 0);  // Only hook deposits

// Set configuration flags (see Constants.sol)
vault.setConfigFlags(configFlags);

// ═══════════════════════════════════════════════════════════
// FEE CONVERSION (not governorOnly - anyone can call)
// ═══════════════════════════════════════════════════════════

// Convert accumulated fees to shares for governor and protocol
// Can be called by anyone
vault.convertFees();
```

**Reading governance state:**

```solidity
// All read functions are public
address governor = vault.governorAdmin();
address feeRcvr = vault.feeReceiver();
uint16 intFee = vault.interestFee();
address irm = vault.interestRateModel();
address protocolCfg = vault.protocolConfigAddress();
uint256 protocolShare = vault.protocolFeeShare();  // Max 50% (0.5e4)
address protocolRcvr = vault.protocolFeeReceiver();
(uint16 supplyCap, uint16 borrowCap) = vault.caps();
uint16 maxDiscount = vault.maxLiquidationDiscount();
uint16 coolOff = vault.liquidationCoolOffTime();
(address hookTarget, uint32 hookedOps) = vault.hookConfig();
uint32 flags = vault.configFlags();
address evc = vault.EVC();
address uoa = vault.unitOfAccount();
address orc = vault.oracle();

// LTV queries
address[] memory collaterals = vault.LTVList(); // append only list (may contain vaults that are no longer accepted as collateral)
uint16 borrowLTV = vault.LTVBorrow(collateral);
uint16 liqLTV = vault.LTVLiquidation(collateral);
(uint16 bLTV, uint16 lLTV, uint16 initLTV, uint48 targetTs, uint32 rampDur) = 
    vault.LTVFull(collateral);
```

**TypeScript: Complete governance example:**

```typescript
import { getContract, parseUnits } from 'viem';

const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: walletClient,  // Must be governor
});

// Check current state
const governor = await vault.read.governorAdmin();
console.log(`Governor: ${governor}`);

// Configure LTV for a new collateral
await vault.write.setLTV([
  collateralVaultAddress,
  8500n,   // 85% borrow LTV (0.85e4)
  9000n,   // 90% liquidation LTV (0.90e4)
  0n       // No ramp
]);

// Set caps
await vault.write.setCaps([
  supplyCap,  // uint16 AmountCap encoded
  borrowCap   // uint16 AmountCap encoded
]);

// Set interest fee (10%)
await vault.write.setInterestFee([1000n]);  // 0.1e4

// Set max liquidation discount (15%)
await vault.write.setMaxLiquidationDiscount([1500n]);  // 0.15e4

// Set new IRM
await vault.write.setInterestRateModel([newIRMAddress]);

// Read all collaterals and their LTVs
const ltvList = await vault.read.LTVList();
for (const collateral of ltvList) {
  const [borrowLTV, liqLTV, initLTV, targetTs, rampDur] = 
    await vault.read.LTVFull([collateral]);
  console.log(`${collateral}: borrow=${borrowLTV/100}%, liq=${liqLTV/100}%`);
}
```

**Important constraints from Governance.sol:**

```solidity
// Protocol fee share cannot exceed 50%
uint16 constant MAX_PROTOCOL_FEE_SHARE = 0.5e4;

// Interest fee guaranteed range (no approval needed)
uint16 constant GUARANTEED_INTEREST_FEE_MIN = 0.1e4;  // 10%
uint16 constant GUARANTEED_INTEREST_FEE_MAX = 1e4;    // 100%

// LTV constraints:
// - borrowLTV must be <= liquidationLTV
// - Cannot self-collateralize (collateral != vault address)
// - rampDuration > 0 only valid when LOWERING LTV
// - maxLiquidationDiscount cannot equal exactly 1e4 (100%)
```

**Risk Steward pattern for limited governance:**

```solidity
import {CapRiskSteward} from "evk-periphery/Governor/CapRiskSteward.sol";

// CapRiskSteward allows limited cap adjustments without full governance
CapRiskSteward steward = new CapRiskSteward(
    evc,
    admin,
    3 days,      // riskSteerCooldown: min time between adjustments
    0.1e18       // riskSteerCapLimit: max 10% change per adjustment
);

steward.setRiskSteerVault(vaultAddress, true);
steward.setSupplyCap(vaultAddress, newSupplyCap);
steward.setBorrowCap(vaultAddress, newBorrowCap);
```

When integrating with Euler, vaults verified in `GovernedPerspective` have passed an initial configuration check by Euler. However, **Euler makes no ongoing guarantees** - risk managers can change vault parameters (LTVs, caps, oracles, IRMs, etc.) at any time after initial verification. Users must perform their own due diligence, monitor governance changes, and assess risk according to their own risk appetite. 

References:
- [Governance.sol Source](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Governance.sol)
- [CapRiskSteward.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Governor/CapRiskSteward.sol)
