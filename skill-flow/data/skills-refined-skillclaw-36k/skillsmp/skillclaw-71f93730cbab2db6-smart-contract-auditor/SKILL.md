---
name: smart-contract-auditor
description: Use this skill when auditing smart contracts for security vulnerabilities, reviewing code changes, or analyzing DeFi protocols to ensure safe deployment and operation.
---

# Smart Contract Auditor

As a Smart Contract Auditor, you will identify vulnerabilities, logic flaws, and economic risks in smart contracts. This skill grounds findings in actual code and proposes minimal safe fixes with tests.

## When to Use

- Auditing smart contracts for security vulnerabilities
- Reviewing pull requests that modify contract code
- Checking for exploits before deployment
- Analyzing risks in DeFi protocols
- Investigating suspicious contract behavior
- Conducting pre-deployment security reviews

## On Every Invocation

### 1. Define Scope & Assumptions

- Identify in-scope contracts, deployment model, privileged actors, upgradeability, and dependencies.
- Establish a threat model: attacker capabilities, trust boundaries, and external integrations (oracles, bridges, tokens).

### 2. Detect Stack & Layout

Identify the smart contract framework and structure:

| Framework | Indicators |
|-----------|------------|
| Foundry | `foundry.toml`, `src/`, `forge` |
| Hardhat | `hardhat.config.js/ts`, `contracts/` |
| Truffle | `truffle-config.js`, `migrations/` |
| Anchor (Rust) | `Anchor.toml`, `programs/` |
| Vyper | `.vy` files |

Map contract directories, core contracts, libraries, test folders, and deployment scripts.

### 3. Scan Recent Changes

```bash
# Check current state
git status

# View uncommitted changes in contracts
git diff -- "**/contracts/**" "**/src/**" "**/*.sol" "**/*.vy"

# Last 20 commits affecting contracts
git log --oneline -20 -- "**/contracts/**" "**/src/**" "**/*.sol"
```

Summarize security-relevant changes (new external calls, authorization changes, token handling).

### 4. Build Contract Map

For each contract document:
- **Purpose**: What it does
- **Trust boundaries**: Owner/admin roles, upgrade authority
- **External interactions**: Calls to other contracts, oracles, DEXs
- **Value flows**: Token transfers, ETH handling

### 5. Structured Audit Pass

Run the audit checklist on:
- All touched contracts (from git diff)
- High-risk contracts (upgradeable, handles funds, external calls)

### 6. Deep Dives by Category

- Access control, accounting, authorization/signatures, reentrancy, oracle manipulation, MEV, denial of service (DoS), upgrade safety.

### 7. Exploit Confirmation

For each suspected issue, build a minimal proof of concept (PoC) scenario, transaction sequence, and expected outcome.

### 8. Fix Validation

Review patch correctness; ensure it doesn't introduce new issues; add regression tests.

### 9. Report Findings

Structure findings as:

```
## A) Audit Scope
- Target:
- Commit/branch (if known):
- Assumptions:
- Out of scope:

## B) Key Risks (Top 3-7)
- Bullet list with severity and 1-line impact

## C) Findings (Detailed)

For each finding use:

#### [SEVERITY] Title

| Field | Value |
|-------|-------|
| **ID** | SC-### |
| **Impact** | Who loses what, how much |
| **Likelihood** | Conditions required |
| **Affected Code** | `file.sol:L##` or function name |

**Description:** What's wrong + proposed fix.
```