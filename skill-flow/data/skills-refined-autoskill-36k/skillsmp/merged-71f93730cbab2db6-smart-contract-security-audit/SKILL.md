---
name: smart-contract-security-audit
description: Use this skill when auditing smart contracts for security vulnerabilities, logic flaws, and economic risks, particularly in Solidity, Vyper, or Rust/Anchor contracts.
---

# Smart Contract Security Audit

This skill serves as a comprehensive security auditor for smart contracts, identifying vulnerabilities, logic flaws, reentrancy, access control issues, MEV/economic attacks, and oracle manipulation. It grounds findings in actual code and proposes minimal safe fixes with tests.

## When to Use

- Auditing smart contracts for security vulnerabilities
- Reviewing PRs that modify contract code
- Checking for exploits before deployment
- Analyzing DeFi protocol risks
- Investigating suspicious contract behavior
- Pre-deployment security review

## Audit Methodology

1. **Scope & Assumptions**
   - Define in-scope contracts, deployment model, privileged actors, upgradeability, and dependencies.
   - Establish a threat model: attacker capabilities, trust boundaries, and external integrations (oracles, bridges, tokens).

2. **Architecture Pass**
   - Identify assets, invariants, entry points, admin powers, upgrade paths, pausing, and emergency controls.

3. **Attack Surface Mapping**
   - Identify external/public functions, callbacks, `receive/fallback`, delegate calls, and external protocols.

4. **Deep Dives by Category**
   - Focus on access control, accounting, reentrancy, oracle manipulation, MEV, and DoS/griefing.

5. **Exploit Confirmation**
   - For each suspected issue, build a minimal proof of concept (PoC) scenario, transaction sequence, and expected outcome.

6. **Fix Validation**
   - Review patch correctness; ensure it doesn't introduce new issues; add regression tests.

7. **Report**
   - Provide a concise executive summary and prioritized findings with reproduction and remediation steps.

## Output Format

### A) Audit Scope
- Target:
- Commit/branch (if known):
- Assumptions:
- Out of scope:

### B) Key Risks (Top 3-7)
- Bullet list with severity and 1-line impact

### C) Findings (Detailed)

For each finding, use:

#### [SEVERITY] Title

| Field | Value |
|-------|-------|
| **ID** | SC-### |
| **Impact** | Who loses what, how much |
| **Likelihood** | Conditions required |
| **Affected Code** | `file.sol:L##` or function name |

**Description:** What's wrong + why it's exploitable

**Exploit Scenario:**
1. Attacker does X
2. Contract state becomes Y
3. Attacker extracts Z

**Recommendation:** Exact fix guidance with code snippet if helpful

**Regression Test:** How to verify the fix

### D) Non-Issues / Informational
- Good patterns observed
- Minor improvements (NatSpec, events, checks)

### E) Fix Review (If Applicable)
- What changed
- Remaining concerns
- Re-test checklist

## Severity Classification

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Direct loss of funds, permanent lock, total takeover with realistic path | Reentrancy drain, auth bypass, infinite mint |
| **High** | Serious fund loss or major control break under plausible conditions | Privilege escalation, oracle manipulation |
| **Medium** | Limited fund loss, griefing, significant invariant break with constraints | Share inflation, DoS on withdraw |
| **Low** | Minor risk, edge-case, defense-in-depth | Missing event, suboptimal check order |
| **Info** | Best practice, clarity, maintainability | NatSpec, naming, gas optimization |

## Quick Checklist Reference

### Access Control & Auth
- Missing/incorrect role checks, insecure admin transfer, privilege escalation
- Initializer exposure (unprotected `initialize()`)
- Signature issues: replay, nonce reuse, wrong domain separator

### Reentrancy & External Calls
- State updated after external calls
- Unsafe callbacks and cross-function reentrancy

### Accounting & Invariants
- `totalSupply != sum(balances)`
- Integer truncation exploitable over many transactions

### Oracle / Pricing / MEV
- Stale prices, predictable randomness, and sandwichable swaps

### DoS / Griefing
- Unbounded loops over user-controlled arrays and storage bloat vectors

### Upgradeability
- Storage slot collision and missing `__gap` for future variables

## Tools Integration

```bash
# Static analysis
slither . --print human-summary
slither . --detect reentrancy-eth,unprotected-upgrade

# Foundry testing
forge test -vvv --match-test testExploit
```

## PoC Development

When writing exploit PoCs:

1. **Minimal setup**: Only deploy what's needed
2. **Clear state transitions**: Log balances before/after
3. **Assertion-based**: `assertGt(attackerBalance, initialBalance)`

## Resources

- [VULNERABILITIES.md](VULNERABILITIES.md) - Detailed vulnerability patterns with code examples
- [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) - Formal audit report structure
- [POC-PATTERNS.md](POC-PATTERNS.md) - Foundry PoC templates for common exploits

$ARGUMENTS