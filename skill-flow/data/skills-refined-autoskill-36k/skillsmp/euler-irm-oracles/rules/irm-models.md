---
title: Interest Rate Model Types and Configuration
impact: HIGH
impactDescription: Critical for selecting and configuring appropriate interest rates
tags: irm, interest-rate, kink, adaptive, configuration
---

## Interest Rate Model Types and Configuration

Euler V2 supports multiple Interest Rate Model (IRM) types, each suited for different market dynamics and risk profiles. Governors can also bring their own custom IRM as long as it conforms to the `IIRM` interface, though custom IRMs may not be supported by the Euler UI.

**Incorrect (misconfigured IRM parameters):**

```solidity
// WRONG: Poorly configured IRM parameters
// This can lead to suboptimal utilization and poor lender returns
address irm = kinkIRMFactory.deploy(
    0,           // baseRate
    4e27,        // slope1: way too high - discourages borrowing
    300e27,      // slope2: extreme spike after kink
    3865470566   // kink: 90%
);
// Result: rates too high → low utilization → poor capital efficiency
```

**Correct (choosing appropriate IRM type):**

### 1. Linear Kink IRM (IRMLinearKink)

Traditional two-slope model. Rate increases linearly up to kink, then accelerates.

```solidity
import {EulerKinkIRMFactory} from "evk-periphery/IRMFactory/EulerKinkIRMFactory.sol";

// Good for stable assets with predictable utilization
// kink parameter is uint32, representing utilization on type(uint32).max scale
// 90% utilization = type(uint32).max * 9 / 10 = 3865470566
address kinkIRM = EulerKinkIRMFactory(kinkIRMFactory).deploy(
    0,            // baseRate: 0% at 0 utilization
    1406417851,   // slope1: ~10% APY at 50% kink (in SPY)
    19050045013,  // slope2: ~100% APY at 100% utilization (in SPY)
    3865470566    // kink: 90% utilization (type(uint32).max * 9 / 10)
);

// Rate formula:
// if utilization <= kink: rate = baseRate + utilization * slope1
// else: rate = baseRate + kink * slope1 + (utilization - kink) * slope2
//
// Common kink values (type(uint32).max scale):
// - 50%: 2147483648  (type(uint32).max / 2)
// - 80%: 3435973837  (type(uint32).max * 8 / 10)
// - 90%: 3865470566  (type(uint32).max * 9 / 10)
```

Use the helper script to calculate parameters from human-readable APY values:

```bash
# Usage: node calculate-irm-linear-kink.js borrow <baseIr> <kinkIr> <maxIr> <kink>
# Example: Base=0%, Kink(90%)=4% APY, Max=100% APY
node calculate-irm-linear-kink.js borrow 0 4 100 90
# Output: 0, 1406417851, 19050045013, 3865470566
```

See: [calculate-irm-linear-kink.js](https://github.com/euler-xyz/evk-periphery/blob/development/script/utils/calculate-irm-linear-kink.js)

### 2. Adaptive Curve IRM (IRMAdaptiveCurve)

Self-adjusting model that targets specific utilization. Rate at target adjusts based on time spent above/below target.

```solidity
import {EulerIRMAdaptiveCurveFactory} from "evk-periphery/IRMFactory/EulerIRMAdaptiveCurveFactory.sol";

// Good for volatile assets or when optimal utilization is uncertain
address adaptiveIRM = EulerIRMAdaptiveCurveFactory(adaptiveCurveFactory).deploy(
    0.9e18,       // TARGET_UTILIZATION: 90%
    0.04e18 / int256(365.2425 days),  // INITIAL_RATE_AT_TARGET: 4% APY
    0.001e18 / int256(365.2425 days), // MIN_RATE_AT_TARGET: 0.1% APY
    2e18 / int256(365.2425 days),     // MAX_RATE_AT_TARGET: 200% APY
    4e18,         // CURVE_STEEPNESS: 4x steeper above target
    2e18 / int256(24 hours)  // ADJUSTMENT_SPEED: 2x per day
);

// Rate adjusts automatically:
// - Utilization above target → rate increases
// - Utilization below target → rate decreases
// - Bounded by MIN and MAX rates at target
```

Use the helper script to calculate parameters from human-readable APY values:

```bash
# Usage: node calculate-irm-adaptive-curve.js <targetUtilization> <initialIrAtTarget> <minIrAtTarget> <maxIrAtTarget> [curveSteepness] [adjustmentSpeedDays]
# Example: Target=90%, Initial=4% APY, Min=0.1% APY, Max=200% APY
node calculate-irm-adaptive-curve.js 90 4 0.1 200
# Default: curveSteepness=4.0, adjustmentSpeedDays=7
```

See: [calculate-irm-adaptive-curve.js](https://github.com/euler-xyz/evk-periphery/blob/development/script/utils/calculate-irm-adaptive-curve.js)

### 3. Linear Kinky IRM (IRMLinearKinky)

Similar to kink IRM but with non-linear acceleration after kink using shape parameter.

```solidity
import {EulerKinkyIRMFactory} from "evk-periphery/IRMFactory/EulerKinkyIRMFactory.sol";

// Good for markets that need smoother rate transitions
// Example: Base=0%, Kink(50%)=10% APY, Max=300% APY, Shape=10
address kinkyIRM = EulerKinkyIRMFactory(kinkyIRMFactory).deploy(
    0,             // baseRate: 0% at 0 utilization
    1406417851,    // slope: rate growth factor (in SPY)
    10,            // shape: 0-100, controls non-linear acceleration
    2147483648,    // kink: 50% utilization (type(uint32).max / 2)
    43929920467914357205  // cutoff: ~1000% APY max (caps extreme rates)
);

// Shape parameter controls how aggressively rates spike after kink
// shape = 0: similar to linear kink
// shape = 100: very aggressive spike
```

### 4. Fixed Cyclical Binary IRM (IRMFixedCyclicalBinary)

Alternates between two fixed rates on a schedule. Useful for special mechanisms.

```solidity
import {EulerFixedCyclicalBinaryIRMFactory} from "evk-periphery/IRMFactory/EulerFixedCyclicalBinaryIRMFactory.sol";

// Useful for synthetic assets or special vault types
address cyclicalIRM = EulerFixedCyclicalBinaryIRMFactory(factory).deploy(
    1e27,         // primaryRate: 100% SPY during primary phase
    0,            // secondaryRate: 0% during secondary phase
    7 days,       // primaryDuration: 1 week at primary rate
    7 days,       // secondaryDuration: 1 week at secondary rate
    block.timestamp  // startTimestamp: when first cycle begins
);
```

Reference: [IRM Contracts](https://github.com/euler-xyz/evk-periphery/tree/master/src/IRM)
