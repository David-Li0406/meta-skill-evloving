---
name: smart-contract-auditor
description: Security auditor for smart contracts - identifies vulnerabilities, logic flaws, reentrancy, access control issues, MEV/economic attacks, and oracle manipulation. Use when auditing Solidity, Vyper, or Rust/Anchor contracts, reviewing PRs for security issues, checking for exploits, or analyzing DeFi protocols. Triggers on "audit", "security review", "vulnerability", "exploit", "reentrancy", "access control", "MEV", "frontrunning".
---

# Smart Contract Auditor

Security auditor for smart contracts. Grounds all findings in actual code, identifies vulnerabilities and economic risks, and proposes minimal safe fixes with tests.

## When to Use

- Auditing smart contracts for security vulnerabilities
- Reviewing PRs that modify contract code
- Checking for exploits before deployment
- Analyzing DeFi protocol risks
- Investigating suspicious contract behavior
- Pre-deployment security review

## On Every Invocation

### 1. Detect Stack & Layout

Identify the smart contract framework and structure:

| Framework | Indicators |
|-----------|------------|
| Foundry | `foundry.toml`, `src/`, `forge` |
| Hardhat | `hardhat.config.js/ts`, `contracts/` |
| Truffle | `truffle-config.js`, `migrations/` |
| Anchor (Rust) | `Anchor.toml`, `programs/` |
| Vyper | `.vy` files |

Map: contract directories, core contracts, libraries, test folders, deployment scripts.

### 2. Scan Recent Changes

```bash
# Check current state
git status

# View uncommitted changes in contracts
git diff -- "**/contracts/**" "**/src/**" "**/*.sol" "**/*.vy"

# Last 20 commits affecting contracts
git log --oneline -20 -- "**/contracts/**" "**/src/**" "**/*.sol"
```

Summarize security-relevant changes (new external calls, auth changes, token handling).

### 3. Build Contract Map

For each contract document:
- **Purpose**: What it does
- **Trust boundaries**: Owner/admin roles, upgrade authority
- **External interactions**: Calls to other contracts, oracles, DEXs
- **Value flows**: Token transfers, ETH handling

### 4. Structured Audit Pass

Run the [AUDIT_CHECKLIST.md](AUDIT_CHECKLIST.md) on:
- All touched contracts (from git diff)
- High-risk contracts (upgradeable, handles funds, external calls)

## Output Format

Structure findings as:

```
## A) Scope Scanned
- Paths and contracts reviewed
- Commit range / diff analyzed

## B) High Severity Issues
For each:
- Vulnerability description
- Exploit scenario (step-by-step attack)
- Impacted functions
- Recommended fix

## C) Medium Severity Issues
[Same format as High]

## D) Low / Informational
[Brief description + recommendation]

## E) Suggested Patches
Step-by-step code edits with before/after

## F) Test Cases
Tests to verify fixes and prevent regression
```

## Severity Classification

| Severity | Criteria |
|----------|----------|
| **High** | Direct fund loss, privilege escalation, contract bricking |
| **Medium** | Conditional fund loss, griefing, DoS, value leakage |
| **Low** | Gas inefficiency, code quality, best practice violations |
| **Info** | Suggestions, documentation, style |

## Quick Checklist Reference

See [AUDIT_CHECKLIST.md](AUDIT_CHECKLIST.md) for the complete checklist. Key categories:

- Access Control
- Reentrancy
- Arithmetic/Precision
- Oracle/Price Manipulation
- MEV/Economic Attacks
- Upgradability
- Signature Schemes
- Token Handling
- DoS/Gas
- Chain Assumptions
- Events & Monitoring
- Invariants

## Resources

- [AUDIT_CHECKLIST.md](AUDIT_CHECKLIST.md) - Detailed vulnerability checklist
- [PATTERNS.md](PATTERNS.md) - Common vulnerability patterns with examples
