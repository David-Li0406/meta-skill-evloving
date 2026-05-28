---
name: entry-point-analyzer
description: Use this skill when auditing smart contracts to identify state-changing entry points, categorize them by access level, and generate structured audit reports.
---

# Entry Point Analyzer

Systematically identify all **state-changing** entry points in a smart contract codebase to guide security audits.

## When to Use

Use this skill when:
- Starting a smart contract security audit to map the attack surface.
- Asked to find entry points, external functions, or audit flows.
- Analyzing access control patterns across a codebase.
- Identifying privileged operations and role-restricted functions.
- Building an understanding of which functions can modify contract state.

## When NOT to Use

Do NOT use this skill for:
- Vulnerability detection (use audit-context-building or domain-specific-audits).
- Writing exploit POCs (use solidity-poc-builder).
- Code quality or gas optimization analysis.
- Non-smart-contract codebases.
- Analyzing read-only functions (this skill excludes them).

## Scope: State-Changing Functions Only

This skill focuses exclusively on functions that can modify state. **Excluded:**

| Language | Excluded Patterns |
|----------|-------------------|
| Solidity | `view`, `pure` functions |
| Vyper | `@view`, `@pure` functions |
| Solana | Functions without `mut` account references |
| Move | Non-entry `public fun` (module-callable only) |
| TON | `get` methods (FunC), read-only receivers (Tact) |
| CosmWasm | `query` entry point and its handlers |

**Why exclude read-only functions?** They cannot directly cause loss of funds or state corruption. While they may leak information, the primary audit focus is on functions that can change state.

## Workflow

1. **Detect Language** - Identify contract language(s) from file extensions and syntax.
2. **Use Tooling (if available)** - For Solidity, check if Slither is available and use it.
3. **Locate Contracts** - Find all contract/module files (apply directory filter if specified).
4. **Extract Entry Points** - Parse each file for externally callable, state-changing functions.