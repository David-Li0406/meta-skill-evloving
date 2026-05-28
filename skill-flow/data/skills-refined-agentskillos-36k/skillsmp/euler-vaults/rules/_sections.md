# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

> **Note:** Specialized topics have been moved to companion skills:
> - `euler-irm-oracles` - Oracle adapters, price resolution, Interest Rate Models
> - `euler-earn` - EulerEarn yield aggregation
> - `euler-advanced` - Hooks, flash loans, fee flow, rewards
> - `euler-data` - Lens contracts, subgraphs, developer tools

---

## 1. Vault Operations (vault)

**Impact:** CRITICAL

**Description:** Core lending and borrowing operations on Euler V2 vaults. These are the fundamental building blocks for interacting with Euler - depositing collateral, borrowing assets, and managing positions. Understanding these operations is essential for any integration.

## 2. EVC Operations (evc)

**Impact:** CRITICAL

**Description:** The Ethereum Vault Connector (EVC) is the central orchestration layer for Euler V2. It enables batching multiple operations atomically, managing sub-accounts for isolated positions, delegating control via operators, and handling collateral/controller relationships. Mastering EVC operations is key to efficient Euler integration.

## 3. Risk Management (risk)

**Impact:** HIGH

**Description:** Monitoring and managing position health to avoid liquidation. Includes health factor calculations, understanding liquidation mechanics, risk curator roles, and implementing protection strategies. Critical for maintaining safe positions.

## 4. Architecture (arch)

**Impact:** HIGH

**Description:** Core market design and vault architecture concepts. Understanding Euler's modular design enables various market structures: simple collateral-debt pairs (Morpho-style), rehypothecation pairs (Silo-style), multiple collaterals (Compound-style), cross-collateralised clusters (Aave-style), or fully customisable configurations. Escrow vaults provide collateral-only functionality without borrowing. Choose based on capital efficiency vs risk isolation tradeoffs.

## 5. Security (sec)

**Impact:** CRITICAL

**Description:** Security practices, audit reports, and safety guidelines for Euler integrations. Understanding security considerations is essential for building safe applications on Euler.
