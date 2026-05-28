# Security Audit Report Template

Use this template for formal audit deliverables.

---

# Security Audit Report

## [Protocol Name]

**Audit Date:** [YYYY-MM-DD]
**Commit:** [hash]
**Auditor:** [Name/Team]

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Scope](#scope)
3. [Findings Summary](#findings-summary)
4. [Detailed Findings](#detailed-findings)
5. [Informational & Best Practices](#informational--best-practices)
6. [Appendix](#appendix)

---

## Executive Summary

### Overview

[1-2 paragraphs describing:
- What the protocol does
- Key mechanisms audited
- Overall security posture]

### Key Statistics

| Metric | Value |
|--------|-------|
| Total Findings | X |
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| Informational | X |

### Risk Assessment

| Risk Area | Assessment |
|-----------|------------|
| Access Control | [Good/Moderate/Needs Improvement] |
| Arithmetic Safety | [Good/Moderate/Needs Improvement] |
| Reentrancy Protection | [Good/Moderate/Needs Improvement] |
| Oracle Integration | [Good/Moderate/Needs Improvement] |
| Upgradeability | [Good/Moderate/Needs Improvement] |

### Recommendations Summary

1. [Top priority fix]
2. [Second priority]
3. [Third priority]

---

## Scope

### Contracts in Scope

| Contract | SLOC | Purpose |
|----------|------|---------|
| `src/Vault.sol` | 250 | Main vault logic |
| `src/Strategy.sol` | 180 | Yield strategy |
| `src/Oracle.sol` | 75 | Price feed wrapper |

### Out of Scope

- External dependencies (OpenZeppelin, Chainlink)
- Frontend/off-chain components
- [Other exclusions]

### Methodology

1. Manual code review
2. Static analysis (Slither)
3. Unit test review
4. Invariant/fuzz testing
5. Economic attack modeling

### Assumptions

- [List trust assumptions, e.g., "Admin is trusted and uses multisig"]
- [External dependency assumptions]

---

## Findings Summary

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| SC-01 | [Title] | Critical | [Open/Fixed/Acknowledged] |
| SC-02 | [Title] | High | [Open/Fixed/Acknowledged] |
| SC-03 | [Title] | Medium | [Open/Fixed/Acknowledged] |
| SC-04 | [Title] | Low | [Open/Fixed/Acknowledged] |

---

## Detailed Findings

---

### SC-01: [Finding Title]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Status** | Open |
| **Affected Code** | `Vault.sol:L125-140` |

#### Description

[Clear explanation of the vulnerability. What's wrong and why.]

#### Impact

[Who loses what, how much, under what conditions.]

#### Proof of Concept

```solidity
// Step-by-step attack
function testExploit_SC01() public {
    // 1. Setup
    vm.deal(attacker, 1 ether);

    // 2. Attack
    vm.prank(attacker);
    vault.exploitableFunction();

    // 3. Verify impact
    assertGt(attacker.balance, 1 ether);
}
```

Or narrative form:
1. Attacker deposits minimal amount
2. Attacker calls `vulnerableFunction()`
3. Due to [flaw], attacker can [impact]

#### Recommendation

```solidity
// Before (vulnerable)
function withdraw(uint256 amount) external {
    (bool success, ) = msg.sender.call{value: amount}("");
    balances[msg.sender] -= amount;
}

// After (fixed)
function withdraw(uint256 amount) external nonReentrant {
    balances[msg.sender] -= amount;
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

#### Team Response

> [Quote team's response or mitigation plan]

#### Auditor Notes

[Any follow-up observations or concerns about the fix]

---

### SC-02: [Finding Title]

| Attribute | Value |
|-----------|-------|
| **Severity** | High |
| **Status** | Fixed |
| **Affected Code** | `Strategy.sol:L45` |

#### Description

[Description]

#### Impact

[Impact]

#### Proof of Concept

[PoC or attack scenario]

#### Recommendation

[Fix]

#### Fix Review

Verified in commit [hash]:
- [x] Vulnerability addressed
- [x] No new issues introduced
- [x] Regression test added

---

## Informational & Best Practices

### I-01: Missing Events for State Changes

**Affected:** `Vault.sol:L50-55`

**Description:** Admin functions don't emit events, making off-chain monitoring difficult.

**Recommendation:** Add events:
```solidity
event FeeUpdated(uint256 oldFee, uint256 newFee);

function setFee(uint256 newFee) external onlyOwner {
    emit FeeUpdated(fee, newFee);
    fee = newFee;
}
```

---

### I-02: Inconsistent NatSpec

**Affected:** Multiple files

**Description:** Some functions lack documentation.

**Recommendation:** Add NatSpec for all external/public functions.

---

### I-03: Consider Using Custom Errors

**Affected:** Throughout codebase

**Description:** Revert strings consume more gas than custom errors.

**Recommendation:**
```solidity
// Before
require(amount > 0, "Amount must be positive");

// After
error InvalidAmount();
if (amount == 0) revert InvalidAmount();
```

---

## Appendix

### A. Static Analysis Results

```
Slither Summary:
- Detectors run: 93
- Issues found: [X]
- False positives filtered: [Y]
```

### B. Test Coverage

| File | Line Coverage | Branch Coverage |
|------|---------------|-----------------|
| Vault.sol | 95% | 88% |
| Strategy.sol | 87% | 75% |

### C. Gas Optimization Notes

| Optimization | Estimated Savings |
|--------------|-------------------|
| Pack storage variables | ~2100 gas/tx |
| Use `calldata` instead of `memory` | ~300 gas/call |

### D. References

- [Relevant EIPs]
- [Prior audits]
- [Protocol documentation]

---

## Disclaimer

This audit is not a guarantee of security. Smart contracts are experimental technology. This report represents a point-in-time review based on the code provided. Changes after the audit may introduce new vulnerabilities. Users should exercise caution and perform their own due diligence.

---

*Report generated [DATE]*
