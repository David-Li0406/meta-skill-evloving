---
name: smart-contract-security-audit
description: Use this skill when auditing smart contracts for vulnerabilities, logic flaws, and economic attacks, particularly in Solidity, Vyper, or Rust/Anchor contracts.
---

# Smart Contract Security Audit

This skill serves as a comprehensive security auditor for smart contracts, identifying vulnerabilities, logic flaws, reentrancy issues, access control problems, MEV/economic attacks, and oracle manipulation. It grounds findings in actual code and proposes actionable fixes.

## When to Use

- Auditing smart contracts for security vulnerabilities
- Reviewing pull requests that modify contract code
- Checking for exploits before deployment
- Analyzing risks in DeFi protocols
- Investigating suspicious contract behavior
- Conducting pre-deployment security reviews

## Audit Methodology

1. **Scope & Assumptions**
   - Define in-scope contracts, deployment models, privileged actors, upgradeability, and dependencies.
   - Establish a threat model considering attacker capabilities and trust boundaries.

2. **Architecture Pass**
   - Identify assets, invariants, entry points, admin powers, upgrade paths, and emergency controls.

3. **Attack Surface Mapping**
   - Map external/public functions, callbacks, and interactions with other contracts or protocols.

4. **Deep Dives by Category**
   - Focus on access control, accounting, reentrancy, oracle manipulation, MEV, and DoS/griefing.

5. **Exploit Confirmation**
   - For each suspected issue, build a minimal proof of concept (PoC) scenario and expected outcomes.

6. **Fix Validation**
   - Review patch correctness and ensure it doesn't introduce new issues; add regression tests.

7. **Report Findings**
   - Provide a concise executive summary and prioritized findings with reproduction steps and remediation guidance.

## Output Format

### A) Audit Scope
- Target: `<target_contracts>`
- Commit/branch (if known): `<commit_info>`
- Assumptions: `<assumptions>`
- Out of scope: `<out_of_scope>`

### B) Key Risks (Top 3-7)
- Bullet list with severity and brief impact description.

### C) Findings (Detailed)

For each finding, use the following format:

#### [SEVERITY] Title

| Field | Value |
|-------|-------|
| **ID** | SC-### |
| **Impact** | Description of who loses what and how much |
| **Likelihood** | Conditions required for the issue to be exploitable |
| **Affected Code** | `file.sol:L##` or function name |

**Description:** What's wrong and why it's exploitable.

**Exploit Scenario:**
1. Attacker does X
2. Contract state becomes Y
3. Attacker extracts Z

**Recommendation:** Specific fix guidance with code snippets if applicable.

**Regression Test:** How to verify the fix.

### D) Non-Issues / Informational
- Good patterns observed
- Minor improvements (e.g., documentation, checks)

### E) Fix Review (If Applicable)
- Summary of what changed
- Remaining concerns
- Re-test checklist

## Severity Classification

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Direct loss of funds or total takeover | Reentrancy drain, auth bypass |
| **High** | Serious fund loss or major control break | Privilege escalation, oracle manipulation |
| **Medium** | Limited fund loss or significant invariant break | DoS on withdraw |
| **Low** | Minor risk or edge-case | Missing event, suboptimal checks |
| **Info** | Best practices or maintainability suggestions | Documentation improvements |

## Quick Checklist Reference

### Access Control & Auth
- Role checks, insecure admin transfers, privilege escalation.

### Reentrancy & External Calls
- State updates after external calls, unsafe callbacks.

### Accounting & Invariants
- Total supply mismatches, exploitable share math.

### Oracle / Pricing / MEV
- Stale prices, predictable randomness.

### DoS / Griefing
- Unbounded loops, revert-on-transfer issues.

### Upgradeability
- Storage slot collisions, unprotected upgrade paths.

## Tools Integration

```bash
# Static analysis
slither . --print human-summary
slither . --detect reentrancy-eth,unprotected-upgrade

# Foundry testing
forge test -vvv --match-test testExploit
```

## Resources

- [VULNERABILITIES.md](VULNERABILITIES.md) - Detailed vulnerability patterns with examples.
- [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) - Formal audit report structure.
- [POC-PATTERNS.md](POC-PATTERNS.md) - Foundry PoC templates for common exploits.

$ARGUMENTS