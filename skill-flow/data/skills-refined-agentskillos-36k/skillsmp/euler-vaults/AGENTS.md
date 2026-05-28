# Euler Finance Agent Skill

**Version 1.0.0**  
Euler Labs  
January 2026

> **Note:**  
> This document is for agents and LLMs to follow when interacting with,  
> building on, or integrating Euler Finance protocol. It covers vault operations,  
> EVC batching, risk management, architecture, and security.
>
> For specialized topics, see companion skills:
> - `euler-irm-oracles` - Oracle adapters, price resolution, Interest Rate Models
> - `euler-earn` - EulerEarn yield aggregation
> - `euler-advanced` - Hooks, flash loans, fee flow, rewards
> - `euler-data` - Lens contracts, subgraphs, developer tools

---

## Abstract

Core guide for interacting with Euler Finance V2 protocol. Covers vault operations (deposit, borrow, repay), EVC orchestration (batching, sub-accounts, operators), risk management (health factors, liquidation), architecture concepts (vault types, market design), interest rate models, security practices, and developer tools. For specialized topics, see companion skills: euler-irm-oracles, euler-earn, euler-advanced.

---

## Table of Contents

1. [Vault Operations](#1-vault-operations) — **CRITICAL**
   - 1.1 [Borrow Assets from a Vault](#11-borrow-assets-from-a-vault)
   - 1.2 [Create a New Vault/Market](#12-create-a-new-vaultmarket)
   - 1.3 [Deposit Assets into a Vault](#13-deposit-assets-into-a-vault)
   - 1.4 [Get Vault APY and Interest Rates](#14-get-vault-apy-and-interest-rates)
   - 1.5 [Repay Borrowed Debt](#15-repay-borrowed-debt)
2. [EVC Operations](#2-evc-operations) — **CRITICAL**
   - 2.1 [Batch Multiple Operations Atomically](#21-batch-multiple-operations-atomically)
   - 2.2 [Delegate Control via Operators](#22-delegate-control-via-operators)
   - 2.3 [Enable Vault as Collateral](#23-enable-vault-as-collateral)
   - 2.4 [Use Sub-Accounts for Isolated Positions](#24-use-sub-accounts-for-isolated-positions)
3. [Risk Management](#3-risk-management) — **HIGH**
   - 3.1 [Check Account Health Factor](#31-check-account-health-factor)
   - 3.2 [How Liquidation Works on Euler](#32-how-liquidation-works-on-euler)
   - 3.3 [Understanding Risk Managers and Vault Governance](#33-understanding-risk-managers-and-vault-governance)
4. [Architecture](#4-architecture) — **HIGH**
   - 4.1 [Understanding Euler Market Design](#41-understanding-euler-market-design)
   - 4.2 [Understanding Vault Types (Governed, Ungoverned, Escrowed Collateral)](#42-understanding-vault-types-governed-ungoverned-escrowed-collateral)
5. [Security](#5-security) — **CRITICAL**
   - 5.1 [Security and Audits](#51-security-and-audits)

---

## 1. Vault Operations

**Impact: CRITICAL**

Core lending and borrowing operations on Euler V2 vaults. These are the fundamental building blocks for interacting with Euler - depositing collateral, borrowing assets, and managing positions. Understanding these operations is essential for any integration.

### 1.1 Borrow Assets from a Vault

**Impact: CRITICAL (Core lending operation with liquidation risk)**

Borrowing on Euler requires enabling the vault as your controller and having sufficient collateral enabled. This creates a debt position that accrues interest.

**Incorrect: borrowing without enabling controller**

```solidity
// This will revert - vault is not enabled as controller
IEVault(vault).borrow(amount, receiver);
// Error: E_ControllerDisabled
```

**Incorrect: borrowing without collateral**

```solidity
// Enable controller but forget collateral
IEVC(evc).enableController(account, vault);
IEVault(vault).borrow(amount, receiver);
// Error: E_AccountLiquidity - no collateral to back the loan
```

**Correct: full borrow flow**

```solidity
// Step 1: Deposit collateral into a collateral vault
IERC20(collateralAsset).approve(collateralVault, collateralAmount);
IEVault(collateralVault).deposit(collateralAmount, account);

// Step 2: Enable the collateral vault for your account
IEVC(evc).enableCollateral(account, collateralVault);

// Step 3: Enable the borrow vault as your controller
// This gives the vault authority to check your account status
IEVC(evc).enableController(account, borrowVault);

// Step 4: Borrow assets
// - amount: how much to borrow
// - receiver: who receives the borrowed assets
uint256 borrowed = IEVault(borrowVault).borrow(amount, receiver);
```

**Correct: batched borrow via EVC for atomicity**

```typescript
// Batch all operations for gas efficiency and atomicity
const batchItems = [
  // Deposit collateral
  {
    targetContract: collateralVault,
    onBehalfOfAccount: account,
    value: 0n,
    data: encodeFunctionData({
      abi: eVaultABI,
      functionName: 'deposit',
      args: [collateralAmount, account],
    }),
  },
  // Enable collateral (EVC call - onBehalfOfAccount must be address(0))
  {
    targetContract: evcAddress,
    onBehalfOfAccount: '0x0000000000000000000000000000000000000000',
    value: 0n,
    data: encodeFunctionData({
      abi: evcABI,
      functionName: 'enableCollateral',
      args: [account, collateralVault],
    }),
  },
  // Enable controller (EVC call - onBehalfOfAccount must be address(0))
  {
    targetContract: evcAddress,
    onBehalfOfAccount: '0x0000000000000000000000000000000000000000',
    value: 0n,
    data: encodeFunctionData({
      abi: evcABI,
      functionName: 'enableController',
      args: [account, borrowVault],
    }),
  },
  // Borrow
  {
    targetContract: borrowVault,
    onBehalfOfAccount: account,
    value: 0n,
    data: encodeFunctionData({
      abi: eVaultABI,
      functionName: 'borrow',
      args: [borrowAmount, account],
    }),
  },
];

await evc.batch(batchItems);
```

Important considerations:

- You can only have ONE controller per account (for single-liability)

- Use sub-accounts to hold multiple different borrows

- Monitor your health factor to avoid liquidation

- The borrow LTV must be satisfied at all times

Reference: [https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#controller](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#controller)

### 1.2 Create a New Vault/Market

**Impact: HIGH (Deploy new lending markets for any asset)**

Creating new Euler vaults allows you to establish lending markets for ERC-20 tokens. Use [euler-vault-scripts](https://github.com/euler-xyz/euler-vault-scripts) for deployment and management.

- [euler-vault-scripts](https://github.com/euler-xyz/euler-vault-scripts)

- [EVK Whitepaper](https://docs.euler.finance/euler-vault-kit-white-paper/)

**Using euler-vault-scripts for cluster deployment:**

```bash
# Clone euler-vault-scripts repository
git clone https://github.com/euler-xyz/euler-vault-scripts
cd euler-vault-scripts

# Install dependencies
./install.sh
forge clean && forge compile

# Edit cluster configuration (copy and modify Cluster.s.sol)
# Define assets, LTVs, oracle providers, caps, IRM parameters, etc.

# Dry run first (always!)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol --dry-run --rpc-url 1

# Deploy (initial deployment)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol --account DEPLOYER --rpc-url 1

# Management after governance transfer (via Safe + Timelock)
./script/ExecuteSolidityScript.sh ./script/clusters/Cluster.s.sol \
  --batch-via-safe --safe-address DAO --timelock-address wildcard --rpc-url 1
```

A cluster is a collection of vaults that accept each other as collateral and share a common governor. The scripts handle both initial deployment and ongoing management.

The cluster script (Cluster.s.sol) defines:

- Assets and their vaults

- LTV ratios between collateral/borrow pairs

- Oracle providers for each asset

- Supply and borrow caps

- Interest rate model parameters

- Hooks and flags

The scripts apply deltas - if vaults already exist, only the difference between configuration and current state is applied.

Key parameters to configure:

| Parameter | Description |

|-----------|-------------|

| Asset | Underlying ERC-20 token |

| Oracle | EulerRouter configured for price feeds |

| Unit of Account | Common denomination (USD, ETH, etc.) |

| LTV (borrow/liquidation) | Collateral requirements |

| Caps (supply/borrow) | Exposure limits |

| IRM | Interest rate model parameters |

| Governor | Address controlling vault parameters |

Important considerations:

- Always use `--dry-run` first to simulate transactions

- Configure appropriate LTV ratios for risk management

- Set reasonable caps to limit protocol exposure

- Consider using governance contracts (GovernorAccessControl + TimelockController + Safe)

- Governor can be set to address(0) for immutability (ungoverned vault)

### 1.3 Deposit Assets into a Vault

**Impact: CRITICAL (Fundamental operation for supplying liquidity)**

Depositing assets into an Euler vault is the first step to earning yield or using assets as collateral. Euler vaults are ERC-4626 compliant.

**Incorrect: forgetting to approve tokens first**

```solidity
// This will revert - vault cannot pull tokens without approval
IEVault(vault).deposit(amount, receiver);
```

**Correct: approve then deposit**

```solidity
// Step 1: Approve the vault to spend your tokens
IERC20(asset).approve(vault, amount);

// Step 2: Deposit assets and receive vault shares
// - amount: the amount of underlying assets to deposit
// - receiver: address that will receive the vault shares
uint256 shares = IEVault(vault).deposit(amount, receiver);
```

Euler vaults also support [Permit2](https://github.com/Uniswap/permit2) for gasless approvals.

**Correct: using mint instead of deposit**

```solidity
// Enable this vault as collateral for your account
IEVC(evc).enableCollateral(account, vault);
```

After depositing, you can enable the vault as collateral via EVC to borrow from other vaults:

Reference: [https://eips.ethereum.org/EIPS/eip-4626](https://eips.ethereum.org/EIPS/eip-4626)

### 1.4 Get Vault APY and Interest Rates

**Impact: HIGH (Essential for yield comparison and strategy decisions)**

Understanding APY is critical for comparing yield opportunities and making informed lending/borrowing decisions on Euler.

**Incorrect: reading raw interest rate without conversion**

```solidity
// The interestRate() returns the per-second interest rate (SPY)
// NOT the APY - this value will be extremely small and misleading
uint256 rate = IEVault(vault).interestRate();
// rate = 1000000000 (this is NOT 100% APY!)
```

**Correct: using VaultLens for complete APY data**

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

**Correct: calculating APY from SPY manually in Solidity**

```typescript
// UtilsLens provides a simpler API for just APY data
const [borrowAPY, supplyAPY] = await utilsLens.read.getAPYs([vaultAddress]);
console.log(`Borrow APY: ${formatUnits(borrowAPY, 25)}%`);
console.log(`Supply APY: ${formatUnits(supplyAPY, 25)}%`);
```

The VaultLens approach is preferred as it handles edge cases and provides additional useful data like collateral LTV info, oracle prices, and IRM parameters.

**Alternative: Using UtilsLens for quick APY queries**

See also: [Lens Contracts for Data Queries](tools-lens) for comprehensive Lens documentation.

Reference: [https://github.com/euler-xyz/evk-periphery/blob/master/src/Lens/VaultLens.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Lens/VaultLens.sol)

### 1.5 Repay Borrowed Debt

**Impact: HIGH (Essential for managing debt and avoiding liquidation)**

Repaying debt reduces your borrow balance and improves your health factor. Interest accrues continuously, so the debt amount increases over time.

**Incorrect: repaying exact original borrow amount**

```solidity
// Interest has accrued - this won't fully repay the debt
uint256 originalBorrow = 1000e18;
IERC20(asset).approve(vault, originalBorrow);
IEVault(vault).repay(originalBorrow, account);
// Still has dust debt remaining!
```

**Correct: partial repay - specify exact amount**

```solidity
// Get current debt to understand position
uint256 currentDebt = IEVault(vault).debtOf(account);

// Repay a specific amount (must be <= current debt, otherwise reverts)
uint256 repayAmount = currentDebt / 2; // repay half
IERC20(asset).approve(vault, repayAmount);
IEVault(vault).repay(repayAmount, account);
```

**Correct (full repay - use type(uint256).max):**

```solidity
// To repay ALL debt, use type(uint256).max
// This is the only safe way to clear debt completely (handles interest accrual)
// IMPORTANT: Repaying more than owed will REVERT - do not add buffers

// Approve enough to cover debt
uint256 currentDebt = IEVault(vault).debtOf(account);
IERC20(asset).approve(vault, currentDebt + (currentDebt / 100)); // small buffer for approval only

// Use max value to repay - pulls exactly what's owed
IEVault(vault).repay(type(uint256).max, account);
```

**Correct: repay with vault shares instead of underlying**

```typescript
const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: walletClient
});

// Check balances
const myDebt = await vault.read.debtOf([account]);
const myShares = await vault.read.balanceOf([account]);
const shareValue = await vault.read.convertToAssets([myShares]);

console.log(`Debt: ${myDebt}, Shares: ${myShares}, Share Value: ${shareValue}`);

// Repay with all shares (up to debt amount)
const [sharesBurned, assetsRepaid] = await vault.write.repayWithShares([
  MaxUint256,  // use all available shares
  account
]);

console.log(`Burned ${sharesBurned} shares, repaid ${assetsRepaid} debt`);
```

**TypeScript: repayWithShares example:**

After fully repaying:

- The controller can be released, freeing your collateral

- You can withdraw collateral or use it elsewhere

- Sub-account becomes available for new positions

Reference: [https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Borrowing.sol](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Borrowing.sol)

---

## 2. EVC Operations

**Impact: CRITICAL**

The Ethereum Vault Connector (EVC) is the central orchestration layer for Euler V2. It enables batching multiple operations atomically, managing sub-accounts for isolated positions, delegating control via operators, and handling collateral/controller relationships. Mastering EVC operations is key to efficient Euler integration.

### 2.1 Batch Multiple Operations Atomically

**Impact: CRITICAL (Gas savings and atomic execution of complex DeFi operations)**

The EVC's batch function allows executing multiple operations in a single transaction. This provides atomicity (all succeed or all fail), gas savings, and deferred liquidity checks.

**Incorrect: separate transactions for each operation**

```solidity
// Multiple transactions = higher gas, not atomic, potential for partial failure
IEVC(evc).enableCollateral(account, collateralVault);  // Tx 1
IEVault(collateralVault).deposit(amount, account);      // Tx 2
IEVC(evc).enableController(account, borrowVault);       // Tx 3
IEVault(borrowVault).borrow(borrowAmount, account);     // Tx 4
// If Tx 4 fails, Tx 1-3 already executed!
```

**Correct: batch all operations atomically**

```solidity
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](4);

// Item 1: Enable collateral
// NOTE: When target is EVC itself, onBehalfOfAccount MUST be address(0)
items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, collateralVault))
});

// Item 2: Deposit collateral (vault call - use account)
items[1] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0,
    data: abi.encodeCall(IEVault.deposit, (amount, account))
});

// Item 3: Enable controller (EVC call - use address(0))
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableController, (account, borrowVault))
});

// Item 4: Borrow (vault call - use account)
items[3] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: borrowVault,
    value: 0,
    data: abi.encodeCall(IEVault.borrow, (borrowAmount, account))
});

// Execute all atomically - liquidity check deferred to end
IEVC(evc).batch(items);
```

**Correct: TypeScript with viem**

```typescript
import { encodeFunctionData } from 'viem';

const batchItems = [
  // EVC calls: onBehalfOfAccount must be address(0)
  {
    onBehalfOfAccount: '0x0000000000000000000000000000000000000000',
    targetContract: evcAddress,
    value: 0n,
    data: encodeFunctionData({
      abi: evcABI,
      functionName: 'enableCollateral',
      args: [account, collateralVault],
    }),
  },
  // Vault calls: use the actual account
  {
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0n,
    data: encodeFunctionData({
      abi: eVaultABI,
      functionName: 'deposit',
      args: [depositAmount, account],
    }),
  },
  // ... more items
];

const tx = await evc.write.batch([batchItems]);
```

**Correct: flash loan style - borrow before collateral**

```solidity
// Deferred checks allow temporarily invalid states!
// Borrow first, deposit collateral second - works in batch
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](4);

items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),  // EVC call - must be address(0)
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableController, (account, borrowVault))
});

items[1] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: borrowVault,
    value: 0,
    data: abi.encodeCall(IEVault.borrow, (borrowAmount, account))
});

// Use borrowed funds to get collateral (e.g., swap)
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: swapRouter,
    value: 0,
    data: abi.encodeCall(ISwapRouter.swap, (/* params */))
});

// Deposit collateral - now account is healthy
items[3] = IEVC.BatchItem({
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0,
    data: abi.encodeCall(IEVault.deposit, (collateralAmount, account))
});

// Liquidity check happens AFTER all operations
IEVC(evc).batch(items);
```

Key benefits:

- Atomic execution - all or nothing

- Gas savings - single transaction overhead

- Deferred liquidity checks - temporary violations allowed

- Can interact with any contract, not just vaults

Reference: [https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#batch](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#batch)

### 2.2 Delegate Control via Operators

**Impact: HIGH (Delegate control over your accounts to other addresses for automated strategies and position management)**

Operators are addresses authorized to act on behalf of an account. They enable automated strategies like stop-loss, take-profit, and position management without giving up custody.

**Incorrect: giving full wallet access**

```solidity
// NEVER share private keys or use unlimited approvals for automation
// This is insecure and gives full control
IERC20(token).approve(automationContract, type(uint256).max);
```

**Correct: install operator for specific account**

```solidity
// Operators can only act on the specific account they're authorized for
// Account owner can revoke at any time

// Install an operator for a specific sub-account
IEVC(evc).setAccountOperator(
    account,           // The account to delegate
    operatorAddress,   // Address that can act on behalf
    true               // true = authorize, false = revoke
);

// The operator can now execute actions on this account via EVC
```

**Correct: operator executing on behalf of account**

```solidity
// Operator contract example - stop-loss implementation
contract StopLossOperator {
    IEVC public immutable evc;
    
    function executeStopLoss(
        address account,
        address vault,
        uint256 repayAmount
    ) external {
        // Verify conditions are met (price dropped below threshold)
        require(shouldTriggerStopLoss(account), "Conditions not met");
        
        // Execute via EVC on behalf of the account
        IEVC.BatchItem[] memory items = new IEVC.BatchItem[](2);
        
        // Repay debt
        items[0] = IEVC.BatchItem({
            onBehalfOfAccount: account,
            targetContract: vault,
            value: 0,
            data: abi.encodeCall(IEVault.repay, (repayAmount, account))
        });
        
        // Withdraw collateral to safety
        items[1] = IEVC.BatchItem({
            onBehalfOfAccount: account,
            targetContract: collateralVault,
            value: 0,
            data: abi.encodeCall(IEVault.withdraw, (
                type(uint256).max, 
                account, 
                account
            ))
        });
        
        evc.batch(items);
    }
}
```

**Correct: TypeScript operator management**

```typescript
// Install operator
await evc.write.setAccountOperator([
  userAccount,
  operatorContractAddress,
  true, // authorize
]);

// Check if operator is authorized
const isOperator = await evc.read.isAccountOperatorAuthorized([
  userAccount,
  operatorContractAddress,
]);

// Revoke operator access
await evc.write.setAccountOperator([
  userAccount,
  operatorContractAddress,
  false, // revoke
]);
```

**Correct: operator with limited scope via hooks**

```solidity
// Combine with hooks for fine-grained control
contract LimitedOperator {
    // Only allow specific operations
    mapping(bytes4 => bool) public allowedSelectors;
    
    function execute(
        address account,
        address target,
        bytes calldata data
    ) external {
        bytes4 selector = bytes4(data[:4]);
        require(allowedSelectors[selector], "Operation not allowed");
        
        IEVC.BatchItem[] memory items = new IEVC.BatchItem[](1);
        items[0] = IEVC.BatchItem({
            onBehalfOfAccount: account,
            targetContract: target,
            value: 0,
            data: data
        });
        
        IEVC(evc).batch(items);
    }
}
```

Key differences from controllers:

- Operators can be revoked by account owner at any time

- Controllers cannot be revoked (only by controller itself when debt is repaid)

- Operators CAN change collateral/controller sets on behalf of the account

- Operators are for delegation, controllers are for borrowing

Reference: [https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#operators](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#operators)

### 2.3 Enable Vault as Collateral

**Impact: CRITICAL (Required before collateral can back borrows)**

Before vault deposits can be used as collateral for borrowing, you must explicitly enable the vault in your account's collateral set via EVC.

**Incorrect: borrowing without enabling collateral**

```solidity
// Deposit into vault
IEVault(collateralVault).deposit(amount, account);

// Try to borrow - fails because collateral not recognized
IEVC(evc).enableController(account, borrowVault);
IEVault(borrowVault).borrow(borrowAmount, account);
// Error: E_AccountLiquidity - no recognized collateral
```

**Correct: enable collateral before borrowing**

```solidity
// Step 1: Deposit into the collateral vault
IERC20(asset).approve(collateralVault, amount);
IEVault(collateralVault).deposit(amount, account);

// Step 2: Enable this vault as collateral for your account
// This adds the vault to your account's collateral set
IEVC(evc).enableCollateral(account, collateralVault);

// Step 3: Now you can borrow against this collateral
IEVC(evc).enableController(account, borrowVault);
IEVault(borrowVault).borrow(borrowAmount, account);
```

**Correct: batch enable multiple collaterals**

```solidity
IEVC.BatchItem[] memory items = new IEVC.BatchItem[](3);

// Enable WETH vault as collateral
// NOTE: When target is EVC itself, onBehalfOfAccount MUST be address(0)
items[0] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wethVault))
});

// Enable WBTC vault as collateral
items[1] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wbtcVault))
});

// Enable wstETH vault as collateral
items[2] = IEVC.BatchItem({
    onBehalfOfAccount: address(0),
    targetContract: address(evc),
    value: 0,
    data: abi.encodeCall(IEVC.enableCollateral, (account, wstethVault))
});

IEVC(evc).batch(items);
```

**Correct: checking and disabling collateral**

```solidity
// Check if vault is enabled as collateral
bool isCollateral = IEVC(evc).isCollateralEnabled(account, vault);

// Get all enabled collaterals for an account
address[] memory collaterals = IEVC(evc).getCollaterals(account);

// Disable collateral (only works if not needed for health)
// WARNING: Will fail if removing would make account unhealthy
IEVC(evc).disableCollateral(account, vault);
```

Important considerations:

- Collateral vault must be accepted by the borrow vault's LTV configuration

- Each vault can have different LTV ratios (borrow LTV vs liquidation LTV)

- Disabling collateral fails if it would make account unhealthy

- Maximum 10 collaterals per account (SET_MAX_ELEMENTS)

Reference: [https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#collateral-validity](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#collateral-validity)

### 2.4 Use Sub-Accounts for Isolated Positions

**Impact: HIGH (Manage multiple isolated positions from one wallet)**

Sub-accounts allow a single Ethereum address to manage up to 256 isolated positions. Each sub-account can have different collateral/debt combinations with separate liquidation risk.

**Incorrect: using same account for multiple borrows**

```solidity
// ERROR: Account can only have ONE controller at a time
IEVC(evc).enableController(account, borrowVaultA);
IEVC(evc).enableController(account, borrowVaultB);
// Second call fails or overwrites first!
```

**Correct: use sub-accounts for different borrows**

```solidity
// Sub-accounts share first 19 bytes, differ in last byte (0-255)
// Account: 0x1234...5678XX where XX is the sub-account index

// Get sub-account addresses
address subAccount0 = account;  // Original address is sub-account 0
address subAccount1 = address(uint160(account) ^ 1);  // XOR with index
address subAccount2 = address(uint160(account) ^ 2);

// Each sub-account can have its own controller
IEVC(evc).enableController(subAccount0, borrowVaultA);  // ETH borrow
IEVC(evc).enableController(subAccount1, borrowVaultB);  // USDC borrow
IEVC(evc).enableController(subAccount2, borrowVaultC);  // DAI borrow

// Each position is isolated - liquidation of one doesn't affect others
```

**Correct: helper function for sub-account calculation**

```solidity
/// @notice Get sub-account address for a given index
/// @param owner The primary account address
/// @param subAccountId The sub-account index (0-255)
/// @return The sub-account address
function getSubAccount(address owner, uint8 subAccountId) 
    public 
    pure 
    returns (address) 
{
    return address(uint160(owner) ^ uint160(subAccountId));
}

// Usage
address ethPosition = getSubAccount(msg.sender, 0);
address usdcPosition = getSubAccount(msg.sender, 1);
address daiPosition = getSubAccount(msg.sender, 2);
```

**Correct: rebalancing between sub-accounts in a batch**

```typescript
// Move collateral between sub-accounts without needing approvals
const subAccount0 = getSubAccount(account, 0);
const subAccount1 = getSubAccount(account, 1);

const batchItems = [
  // Withdraw from sub-account 0
  {
    onBehalfOfAccount: subAccount0,
    targetContract: collateralVault,
    value: 0n,
    data: encodeFunctionData({
      abi: eVaultABI,
      functionName: 'withdraw',
      args: [amount, subAccount1, subAccount0], // receiver is subAccount1
    }),
  },
  // Deposit to sub-account 1 happens automatically via receiver
];

// Owner can operate on behalf of any sub-account
await evc.write.batch([batchItems]);
```

**Correct: checking sub-account ownership**

```solidity
// EVC tracks owner for sub-account groups
function getAccountOwner(address account) external view returns (address) {
    // Returns the primary address (sub-account 0) that controls this sub-account
    return IEVC(evc).getAccountOwner(account);
}

// Verify ownership
address owner = IEVC(evc).getAccountOwner(subAccount5);
require(owner == expectedOwner, "Not owned by expected address");
```

Key points:

- Sub-accounts share 19 bytes, differ in last byte (0-255)

- Owner can operate on all 256 sub-accounts without approval

- Each sub-account can have ONE controller (single liability)

- Collateral can be shared or isolated per sub-account

- Use different sub-accounts for different risk strategies

Reference: [https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#sub-accounts](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#sub-accounts)

---

## 3. Risk Management

**Impact: HIGH**

Monitoring and managing position health to avoid liquidation. Includes health factor calculations, understanding liquidation mechanics, risk curator roles, and implementing protection strategies. Critical for maintaining safe positions.

### 3.1 Check Account Health Factor

**Impact: HIGH (Critical for avoiding liquidation)**

Health factor determines how close an account is to liquidation. A health factor below 1.0 means the account can be liquidated. Monitoring health is essential for safe position management.

**Incorrect: only checking debt amount**

```solidity
// Debt amount alone doesn't indicate liquidation risk
uint256 debt = IEVault(vault).debtOf(account);
// This tells you nothing about health - need to compare against collateral value
```

**Correct: using AccountLens for health check**

```typescript
import { AccountLens } from '@eulerxyz/evk-periphery';

// Get comprehensive account health info
// accountLens.getAccountInfo(account, vault) returns AccountInfo struct
const accountInfo = await accountLens.read.getAccountInfo([account, controller]);

// Access liquidity info from vaultAccountInfo
const liquidityInfo = accountInfo.vaultAccountInfo.liquidityInfo;

// Check if query succeeded (liquidityInfo.queryFailure === false)
if (liquidityInfo.queryFailure) {
  console.error('Liquidity query failed:', liquidityInfo.queryFailureReason);
  return;
}

// For liquidation health: collateralValueLiquidation / liabilityValueLiquidation
const collateralValueLiq = liquidityInfo.collateralValueLiquidation;
const liabilityValueLiq = liquidityInfo.liabilityValueLiquidation;

// Calculate health: > 1.0 = healthy, < 1.0 = can be liquidated
const health = liabilityValueLiq > 0n 
  ? (collateralValueLiq * BigInt(1e18)) / liabilityValueLiq 
  : BigInt(2n ** 256n - 1n); // Infinite if no debt

// timeToLiquidation: estimated SECONDS until liquidation (int256)
// Computed via binary search over 0 to 400 days, assuming static prices/rates
// Binary search precision: ±1 day (exits when interval <= 1 day)
// NOTE: Only considers Euler lending/borrowing rates, NOT external yield (e.g., wstETH, DAI)
// Special int256 values:
const TTL_INFINITY = (2n ** 255n) - 1n;        // type(int256).max - no debt, zero rate, or collateral interest >= debt interest
const TTL_MORE_THAN_ONE_YEAR = (2n ** 255n) - 2n; // type(int256).max - 1 - safe for at least one year
const TTL_LIQUIDATION = -1n;                   // already liquidatable (health <= 1)
const TTL_ERROR = -2n;                         // computation overflow or failure

const ttl = liquidityInfo.timeToLiquidation;

console.log(`Health: ${Number(health) / 1e18}`);
console.log(`Liability: ${liabilityValueLiq}`);
console.log(`Collateral: ${collateralValueLiq}`);
console.log(`Time to Liquidation: ${ttl}`);
```

**Correct: on-chain health check via accountLiquidity**

```solidity
// Use accountLiquidity to check health on-chain

// Get liquidity values with liquidation LTV
(uint256 collateralValue, uint256 liabilityValue) = IEVault(controller).accountLiquidity(
    account,
    true  // liquidation = true for liquidation LTV
);

// Check if account is healthy (collateral >= liability)
bool isHealthy = collateralValue >= liabilityValue;

// Check if account is liquidatable
bool isLiquidatable = liabilityValue > 0 && collateralValue < liabilityValue;

// Calculate health factor (1e18 scale)
uint256 healthFactor = liabilityValue > 0 
    ? (collateralValue * 1e18) / liabilityValue 
    : type(uint256).max;
```

**Correct: detailed breakdown with accountLiquidityFull**

```typescript
const vault = getContract({
  address: controllerAddress,
  abi: evaultABI,
  client: publicClient
});

// Get liquidity with borrow LTV
const [collateralBorrow, liabilityBorrow] = await vault.read.accountLiquidity([
  account,
  false  // borrow LTV
]);

// Get liquidity with liquidation LTV
const [collateralLiq, liabilityLiq] = await vault.read.accountLiquidity([
  account,
  true   // liquidation LTV
]);

// Calculate both health factors
const borrowHealth = liabilityBorrow > 0n 
  ? (collateralBorrow * 10n ** 18n) / liabilityBorrow 
  : MaxUint256;

const liquidationHealth = liabilityLiq > 0n
  ? (collateralLiq * 10n ** 18n) / liabilityLiq
  : MaxUint256;

console.log(`Borrow Health: ${formatUnits(borrowHealth, 18)}`);
console.log(`Liquidation Health: ${formatUnits(liquidationHealth, 18)}`);

// Full breakdown
const [collaterals, values, liability] = await vault.read.accountLiquidityFull([
  account,
  true
]);

for (let i = 0; i < collaterals.length; i++) {
  console.log(`${collaterals[i]}: ${formatUnits(values[i], 18)} value`);
}
```

**TypeScript: Using accountLiquidity:**

**Correct: disabling controller after full repayment**

```typescript
const batchItems: BatchItem[] = [
  // Repay all debt
  {
    onBehalfOfAccount: account,
    targetContract: controllerVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'repay',
      args: [MaxUint256, account],
    }),
  },
  // Disable controller (releases collateral from health checks)
  {
    onBehalfOfAccount: account,
    targetContract: controllerVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'disableController',
      args: [],
    }),
  },
  // Withdraw collateral (no health check now that controller is disabled)
  {
    onBehalfOfAccount: account,
    targetContract: collateralVault,
    value: 0n,
    data: encodeFunctionData({
      abi: evaultABI,
      functionName: 'withdraw',
      args: [MaxUint256, account, account],
    }),
  },
];

await evc.batch(batchItems);
```

**TypeScript: Full repay and disable flow:**

**Understanding checkAccountStatus and checkVaultStatus: EVC internals**

These are EVC callback functions - **NOT meant to be called directly**. The EVC calls them automatically during deferred checks at the end of batches:

- `checkAccountStatus(account, collaterals)`: Called by EVC to verify account health. Reverts if unhealthy (collateral < liability). Returns magic selector on success.

- `checkVaultStatus()`: Called by EVC to verify vault caps aren't exceeded and triggers interest rate recalculation.

**For health checks in your code, use `accountLiquidity()` instead** (shown above).

Key concepts:

- Health > 1.0 = safe from liquidation

- Borrow LTV: max health when taking new borrows

- Liquidation LTV: health at which liquidation can occur

- Always maintain buffer above 1.0 for price volatility

- `accountLiquidity(account, false)` = borrow LTV values

- `accountLiquidity(account, true)` = liquidation LTV values

- Call `disableController()` after full repayment to release position

Time to Liquidation (TTL) - **unit: seconds**, **precision: ±1 day** (int256):

- Positive values = seconds until liquidation (binary search over 0-400 days, ±1 day precision)

- `TTL_INFINITY` = `type(int256).max`: No debt, zero borrow rate, or collateral interest >= debt interest

- `TTL_MORE_THAN_ONE_YEAR` = `type(int256).max - 1`: Safe for at least one year

- `TTL_LIQUIDATION` = `-1`: Already liquidatable (health <= 1)

- `TTL_ERROR` = `-2`: Computation overflow or failure

- ⚠️ TTL only considers **Euler lending/borrowing rates** - does NOT include external yield (wstETH, DAI etc.)

- ⚠️ TTL assumes **static prices** - real price volatility may cause liquidation sooner

See also: [Lens Contracts](tools-lens) - AccountLens provides `getAccountLiquidityInfo()` and `getTimeToLiquidation()` for comprehensive health monitoring.

Reference: [https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/RiskManager.sol](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/RiskManager.sol)

### 3.2 How Liquidation Works on Euler

**Impact: HIGH (Understanding liquidation mechanics and math)**

Liquidation protects the protocol by allowing anyone to take over an unhealthy account's debt in exchange for their collateral at a discount. The discount is dynamically calculated based on how unhealthy the position is.

**Key difference from other protocols:** Euler liquidation is a **position transfer**, not a debt repayment. The liquidator inherits the debt AND receives the collateral - no debt tokens are pulled from the liquidator upfront.

**Liquidation Math: from Liquidation.sol**

```solidity
// Health score (discountFactor) = risk-adjusted collateral / liability
// discountFactor = 1.0 means healthy, < 1.0 means liquidatable
uint256 discountFactor = collateralAdjustedValue * 1e18 / liabilityValue;

// Discount = 1 - discountFactor (i.e., 1 - health score)
// Example: health = 0.85 → discount = 15%

// Cap discount at maxLiquidationDiscount (set by governor)
uint256 minDiscountFactor = 1e18 - (1e18 * maxLiquidationDiscount / 1e4);
if (discountFactor < minDiscountFactor) {
    discountFactor = minDiscountFactor;  // Cap the discount
}

// Yield value = repay value / discountFactor (more yield at lower health)
uint256 maxYieldValue = maxRepayValue * 1e18 / discountFactor;
```

**Practical Example:**

```typescript
Position:
- Debt: 1000 USDC (value: $1000)
- Collateral: 1 ETH (value: $1200)
- Liquidation LTV: 90%
- Max Liquidation Discount: 15%

Health Score:
- Adjusted Collateral = $1200 * 90% = $1080
- Health = $1080 / $1000 = 1.08 → HEALTHY (>1.0)

After ETH drops to $1050:
- Adjusted Collateral = $1050 * 90% = $945
- Health = $945 / $1000 = 0.945 → LIQUIDATABLE (<1.0)
- Discount Factor = 0.945
- Discount = 1 - 0.945 = 5.5%

Liquidation:
- Debt inherited: $1000
- Collateral received: $1000 / 0.945 = $1058 worth of ETH
- Liquidator profit: $58 (5.5% discount)
```

**Checking liquidation opportunity:**

```solidity
// checkLiquidation returns (0, 0) if account is healthy
(uint256 maxRepay, uint256 maxYield) = IEVault(vault).checkLiquidation(
    liquidator,   // who will receive collateral
    violator,     // unhealthy account
    collateral    // which collateral to seize
);
```

**Executing liquidation:**

```solidity
// liquidate(violator, collateral, repayAssets, minYieldBalance)
// - violator: the unhealthy account
// - collateral: which collateral vault to seize from
// - repayAssets: how much debt to take over (use type(uint256).max for all)
// - minYieldBalance: minimum collateral to receive (slippage protection)

// LIQUIDATOR MUST BE PREPARED LIKE A BORROWER:
// 1. The vault must be enabled as the liquidator's controller (explicitly)
// 2. The seized collateral must be enabled for the liquidator's account

IEVC(evc).enableController(liquidator, vault);
IEVC(evc).enableCollateral(liquidator, collateral);

IEVault(vault).liquidate(violator, collateral, repayAmount, minYieldBalance);

// After: liquidator has collateral shares AND owes the debt
// Profit is realized by repaying the debt (worth less than collateral received)
```

**Liquidation Constraints:**

```solidity
// 1. Cannot self-liquidate
require(violator != liquidator, "E_SelfLiquidation");

// 2. Collateral must have LTV configured
require(isRecognizedCollateral(collateral), "E_BadCollateral");

// 3. Vault must be violator's controller
validateController(violator);

// 4. Violator must have enabled this collateral
require(isCollateralEnabled(violator, collateral), "E_CollateralDisabled");

// 5. No deferred status checks (prevents batch manipulation)
require(!isAccountStatusCheckDeferred(violator), "E_ViolatorLiquidityDeferred");

// 6. Must wait for cool-off period after last status check
require(!isInLiquidationCoolOff(violator), "E_LiquidationCoolOff");
```

**Debt Socialization: bad debt handling**

When a position has debt remaining but no collateral left, the debt is "socialized":

- Remaining debt is written off (removed from the system)

- Loss is spread across all depositors (share value decreases)

- This protects the pool from accumulating bad debt that can never be repaid

Conditions: liability >= 1e6 in unit of account, `CFG_DONT_SOCIALIZE_DEBT` flag not set.

**Key Parameters:**

| Parameter | Getter | Description |

|-----------|--------|-------------|

| maxLiquidationDiscount | `maxLiquidationDiscount()` | Max discount (e.g., 0.15e4 = 15%) |

| liquidationCoolOffTime | `liquidationCoolOffTime()` | Seconds after status check before liquidatable |

| liquidationLTV | `LTVLiquidation(collateral)` | LTV threshold for liquidation |

Reference: [https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Liquidation.sol](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Liquidation.sol)

### 3.3 Understanding Risk Managers and Vault Governance

**Impact: HIGH (Essential for vault governance and risk management)**

Risk Managers (governors) are trusted entities responsible for ongoing vault configuration and risk management in Euler V2. They have full control over vault parameters through governance functions.

- [Governance.sol Source](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/modules/Governance.sol)

- [CapRiskSteward.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Governor/CapRiskSteward.sol)

**Incorrect: assuming anyone can configure vaults**

```solidity
// WRONG: Only governor can modify vault config
IEVault vault = IEVault(vaultAddress);
vault.setLTV(collateral, 8000, 9000, 0);  // Will revert with E_Unauthorized!
vault.setCaps(100, 50);                    // Will revert with E_Unauthorized!
```

**Complete list of governance functions:**

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

All functions below require `governorOnly` modifier (caller must be `governorAdmin`):

**Reading governance state:**

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

**TypeScript: Complete governance example:**

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

---

## 4. Architecture

**Impact: HIGH**

Core market design and vault architecture concepts. Understanding Euler's modular design enables various market structures: simple collateral-debt pairs (Morpho-style), rehypothecation pairs (Silo-style), multiple collaterals (Compound-style), cross-collateralised clusters (Aave-style), or fully customisable configurations. Escrow vaults provide collateral-only functionality without borrowing. Choose based on capital efficiency vs risk isolation tradeoffs.

### 4.1 Understanding Euler Market Design

**Impact: HIGH (Fundamental knowledge for building on Euler V2)**

Euler V2 uses a modular "vault kit" architecture where each market is an independent ERC-4626 vault with its own configuration for oracle, interest rate model, and collateral relationships.

- [Euler Markets Documentation](https://docs.euler.finance/concepts/core/markets)

- [EVK Whitepaper](https://github.com/euler-xyz/euler-vault-kit/blob/master/docs/whitepaper.md)

**Incorrect: assuming monolithic pool like Compound/Aave**

```solidity
// WRONG: There's no single "Euler pool" to interact with
// Each asset has its own vault(s) with independent configuration
address eulerPool = 0x...;
IPool(eulerPool).deposit(USDC, amount); // This doesn't exist!
```

**Correct: understanding independent vault architecture**

```solidity
import {IEVault} from "evk/EVault/IEVault.sol";
import {IEVC} from "ethereum-vault-connector/interfaces/IEVC.sol";

// Each vault is independent - there can be multiple USDC vaults
// with different configurations (oracle, IRM, collaterals and risk profile)
address usdcVault = 0x...; // A specific USDC vault

// Vaults are standard ERC-4626 with extensions
IEVault vault = IEVault(usdcVault);

// Key vault properties
address asset = vault.asset();           // Underlying token
address oracle = vault.oracle();         // Price oracle (EulerRouter)
address irm = vault.interestRateModel(); // Interest rate model
address unitOfAccount = vault.unitOfAccount(); // Price denomination

// Collateral relationships are vault-to-vault
// This vault accepts another vaults' shares (not vaults' assets) as collateral
address[] memory collaterals = vault.LTVList(); // this is an append only list and may contain addresses that are no longer accepted as collateral
(uint16 borrowLTV, uint16 liquidationLTV, , ) = vault.LTVFull(collateralVault);
```

**Correct: understanding the EVC layer**

```solidity
// The EVC (Ethereum Vault Connector) orchestrates cross-vault operations
IEVC evc = IEVC(0x0C9a3dd6b8F28529d72d7f9cE918D493519EE383); // this address is different on each chain

// Accounts enable a vault as collateral for their positions
evc.enableCollateral(account, collateralVault);

// Accounts enable a vault as controller (to borrow from)
evc.enableController(account, borrowVault);

// The controller vault checks all collateral vaults to ensure solvency
// This happens automatically at the end of the operation/batch of operations
```

**Key Architecture Concepts:**

```typescript
// TypeScript example: querying vault configuration
import { getContract } from 'viem';

const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: publicClient,
});

// Get all accepted collaterals for this vault (this is an append only list and may contain addresses that are no longer accepted as collateral)
const ltvList = await vault.read.LTVList();

// For each collateral, get LTV configuration
for (const collateral of ltvList) {
  const [borrowLTV, liquidationLTV, initialLTV, targetTimestamp, rampDuration] = 
    await vault.read.LTVFull([collateral]);
  
  console.log(`Collateral ${collateral}:`);
  console.log(`  Borrow LTV: ${borrowLTV / 100}%`);
  console.log(`  Liquidation LTV: ${liquidationLTV / 100}%`);
}
```

1. **Vaults are ERC-4626**: Standard deposit/withdraw interface plus borrowing extensions

2. **Oracles per vault**: Each vault has its own EulerRouter for price resolution

3. **Unit of Account**: Common price denomination (usually USD or ETH) for LTV calculations

4. **Collateral is vault shares**: When you deposit, you get vault shares that can be accepted as collateral

5. **Controller relationship**: The vault you borrow from is your "controller". It decides if the position is healthy or requires a liquidation. It controls how much collateral user can withdraw when having an active borrow position

6. **LTV is vault-to-vault**: Each collateral-controller pair has specific LTV settings

**Market Design Patterns:**

```solidity
// Example: Simple isolated pair (Morpho-style)
// - WETH vault holds collateral in escrow only
// - USDC vault is the lending/borrowing vault
// - WETH vault has no borrowing enabled

// Example: Rehypothecation pair (Silo-style)  
// - WETH vault: accepts USDC as collateral, lends WETH
// - USDC vault: accepts WETH as collateral, lends USDC
// - Assets earn yield while backing loans

// Example: Multiple collateral vaults (Compound-style)
// - USDC vault: accepts WETH, WBTC, DAI, etc. as collateral
// - Only USDC is supplied and borrowed
// - Users can deposit various assets as collateral to borrow/supply USDC
// - Each collateral type can have different LTV and risk parameters

// Example: Cross-collateralised cluster (Aave-style)
// - WETH, WBTC, USDC, DAI vaults all interconnected
// - Each can lend and serve as collateral for others
// - Higher contagion risk if one vault defaults
```

Euler's modular architecture enables various market structures. Choose based on capital efficiency vs risk isolation tradeoffs:

| Design | Description | Similar To | Capital Efficiency | Risk Isolation |

|--------|-------------|------------|-------------------|----------------|

| Simple collateral-debt pairs | One collateral vault, one borrow vault | Morpho, FraxLend, Kashi | Low | High |

| Rehypothecation pairs | Both vaults lend and serve as collateral for each other | Silo, Fluid | Medium | Medium |

| Multiple collaterals | Many collateral vaults borrow from one lending vault | Compound | Medium-High | Medium |

| Cross-collateralised clusters | Multiple vaults all lend and collateralize each other | Aave | High | Low |

| Fully customisable | Any configuration, including vaults from existing markets | Unique to Euler | Variable | Variable |

**Creating Custom Markets:**

```solidity
// Vaults can accept collateral from ANY existing vault
// This enables composability with the broader Euler ecosystem

// Step 1: Deploy your vault
address myVault = EVaultFactory.createProxy(
    asset,
    false,  // not upgradeable
    ""      // no trailing data (only for the example; otherwise it's required)
);

// Step 2: Configure to accept existing vault shares as collateral
IEVault(myVault).setLTV(
    existingPopularVault,  // e.g., an established USDC vault
    0.85e4,                // 85% borrow LTV
    0.90e4,                // 90% liquidation LTV
    0                      // ramp duration
);

// Now users with deposits in existingPopularVault
// can borrow from your new vault without moving funds!
```

This modular design allows for permissionless market creation - anyone can deploy a vault with custom parameters while the EVC provides the security layer for cross-vault interactions.

### 4.2 Understanding Vault Types (Governed, Ungoverned, Escrowed Collateral)

**Impact: HIGH (Critical for selecting appropriate vault type for your use case)**

Euler V2 vaults fall into two main categories based on governance: **Governed** (with active governance) and **Ungoverned** (governance renounced). Escrowed Collateral vaults are a special subtype of ungoverned vaults designed for collateral-only use cases.

**Incorrect: treating all vaults the same**

```solidity
// WRONG: Not all vaults support borrowing or have the same features
IEVault vault = IEVault(anyVault);
vault.borrow(amount, receiver); // May revert for escrow vaults!
vault.setInterestRateModel(irm); // May not be configurable!
```

**Correct: understanding vault types**

```solidity
import {GenericFactory} from "evk/GenericFactory/GenericFactory.sol";
import {IEVault} from "evk/EVault/IEVault.sol";

// Governed vaults have full configuration capabilities
IEVault vault = IEVault(vaultAddress);

// Has governor for ongoing management
address governor = vault.governorAdmin();
require(governor != address(0), "This is a governed vault");

// Governor can update configuration
vault.setInterestRateModel(newIRM);
vault.setLTV(collateral, borrowLTV, liquidationLTV, rampDuration);
vault.setCaps(supplyCap, borrowCap);

// Supports all operations: deposit, withdraw, borrow, repay
vault.deposit(amount, receiver);
vault.borrow(amount, receiver);
```

Full-featured lending vaults with active governance (risk management). The governor can update parameters like LTV, caps, IRM, and oracle configuration over time.

> ⚠️ **Trust Warning:** Users must fully trust the governor address. The governor has significant power over vault parameters and could potentially act maliciously (e.g., setting dangerous LTVs, changing oracles, or extracting fees). Always verify who controls governance before depositing - whether it's an EOA, multisig, DAO, or limited governor contract.

**Limited Governor Pattern:**

```solidity
import {EscrowedCollateralPerspective} from "evk-periphery/Perspectives/deployed/EscrowedCollateralPerspective.sol";

// Escrow vaults are singletons per asset - only one per token
EscrowedCollateralPerspective perspective = EscrowedCollateralPerspective(perspectiveAddress);
address escrowVault = perspective.singletonLookup(assetAddress);

// If not deployed, deploy new escrow vault
if (escrowVault == address(0)) {
    bytes memory trailingData = abi.encodePacked(asset, address(0), address(0));
    escrowVault = GenericFactory(factory).createProxy(address(0), true, trailingData);
    
    // Escrow vaults have minimal config and renounced governance
    IEVault(escrowVault).setHookConfig(address(0), 0);
    IEVault(escrowVault).setGovernorAdmin(address(0));
    
    // Verify in perspective so that others can reuse this vault later
    perspective.perspectiveVerify(escrowVault, true);
}

// Escrow vault properties:
// - No oracle (address(0))
// - No unit of account (address(0))
// - No IRM (address(0))
// - No caps
// - No hooks
// - No LTV list (cannot be borrowed against directly)
// - Governance renounced (address(0))
```

Instead of a full EOA or multisig as governor, you can set a **limited governor contract** that only allows specific parameter changes. This provides a middle ground between full governance and complete immutability.

This pattern is useful when you want restricted, predictable governance rather than full control or complete immutability.

Vaults with governance permanently renounced (`governorAdmin == address(0)`). Configuration is fixed at deployment and cannot be changed. This provides immutability guarantees but no flexibility.

Special ungoverned vaults designed purely for holding collateral. They have no oracle, no IRM, and no borrowing capability and are neutral (can be reused by anyone). One escrow vault exists per asset (singleton pattern).

**Correct: using Perspectives to verify vault type**

```typescript
import { getContract } from 'viem';

// Perspectives verify vault properties
const governedPerspective = getContract({
  address: governedPerspectiveAddress,
  abi: perspectiveABI,
  client: publicClient,
});

const escrowPerspective = getContract({
  address: escrowPerspectiveAddress,
  abi: perspectiveABI,
  client: publicClient,
});

// Check if vault is in a perspective
const isGoverned = await governedPerspective.read.isVerified([vaultAddress]);
const isEscrow = await escrowPerspective.read.isVerified([vaultAddress]);

// Check governance status directly
const vault = getContract({
  address: vaultAddress,
  abi: evaultABI,
  client: publicClient,
});
const governor = await vault.read.governorAdmin();
const isUngoverned = governor === '0x0000000000000000000000000000000000000000';

// Perspectives provide trust guarantees:
// - GovernedPerspective: whitelisted by Euler
// - EscrowedCollateralPerspective: verified collateral-only vault
// - EVKFactoryPerspective: deployed by official factory
```

| Feature | Governed Vault | Ungoverned Vault | Escrowed Collateral |

|---------|----------------|------------------|---------------------|

| Borrowing | ✓ | ✓ (if configured) | ✗ |

| Governance | ✓ | ✗ (renounced) | ✗ (renounced) |

| Oracle | ✓ | ✓ (fixed) | ✗ |

| IRM | ✓ | ✓ (fixed) | ✗ |

| Caps | ✓ | ✓ (fixed) | ✗ |

| Can be collateral | ✓ | ✓ | ✓ |

| Config changeable | ✓ | ✗ | ✗ |

Reference: [https://github.com/euler-xyz/evk-periphery/blob/master/src/Perspectives/deployed/EscrowedCollateralPerspective.sol](https://github.com/euler-xyz/evk-periphery/blob/master/src/Perspectives/deployed/EscrowedCollateralPerspective.sol)

---

## 5. Security

**Impact: CRITICAL**

Security practices, audit reports, and safety guidelines for Euler integrations. Understanding security considerations is essential for building safe applications on Euler.

### 5.1 Security and Audits

**Impact: CRITICAL (Understanding security practices and audit coverage)**

Euler V2 has undergone extensive security audits and maintains an active bug bounty program. See [Euler Security](https://docs.euler.finance/security/audits) for full audit reports.

**Incorrect: ignoring security considerations**

```solidity
// WRONG: Using unverified vaults without checks
IEVault vault = IEVault(userProvidedVault);
vault.deposit(amount, receiver); // Could be malicious!
```

**Correct: verifying vault authenticity**

```solidity
import {GenericFactory} from "evk/GenericFactory/GenericFactory.sol";
import {IPerspective} from "evk-periphery/Perspectives/implementation/interfaces/IPerspective.sol";

// Check if deployed by official factory (confirms it's a real EVK vault)
GenericFactory factory = GenericFactory(EVAULT_FACTORY);
require(factory.isProxy(vaultAddress), "Not EVK vault");

// GovernedPerspective only confirms INITIAL configuration was checked
// It does NOT guarantee ongoing safety - governors can change parameters anytime
IPerspective governedPerspective = IPerspective(GOVERNED_PERSPECTIVE);
bool wasInitiallyVerified = governedPerspective.isVerified(vaultAddress);

// IMPORTANT: Users should only interact with vaults they trust
// - Verify the governor address and who controls it
// - Monitor for parameter changes (LTV, caps, oracle, IRM)
// - Assess the risk manager's reputation and track record
```

**Security Best Practices:**

```typescript
// 1. Validate vault is from official factory
const isEVKVault = async (vault: Address): Promise<boolean> => {
  return await evaultFactory.read.isProxy([vault]);
};

// 2. Check who controls the vault (critical!)
const checkGovernance = async (vault: Address) => {
  const governor = await evault.read.governorAdmin();
  
  if (governor === zeroAddress) {
    console.log('Ungoverned vault - parameters are immutable');
  } else {
    // IMPORTANT: Verify you trust this governor!
    // Could be EOA, multisig, DAO, or limited steward contract
    console.log('Governor:', governor);
    // Research: Who controls this address? What's their track record?
  }
};

// 3. Check current configuration matches your expectations
const verifyConfig = async (vault: Address) => {
  const oracle = await evault.read.oracle();
  const irm = await evault.read.interestRateModel();
  const [hookTarget, hookedOps] = await evault.read.hookConfig();
  const [supplyCap, borrowCap] = await evault.read.caps();
  
  // Verify these match what you expect for this vault
  console.log('Oracle:', oracle);
  console.log('IRM:', irm);
  console.log('Hooks:', hookTarget, hookedOps);
};
```

**Evaluating Collateral Quality: Critical for Lenders**

```typescript
// Check what collaterals a vault accepts and their LTVs
const collaterals = await vault.read.LTVList();
for (const collateral of collaterals) {
  const [borrowLTV, liqLTV] = await vault.read.LTVFull([collateral]);
  const collateralAsset = await IEVault(collateral).asset();
  console.log(`Collateral: ${collateralAsset}, Borrow LTV: ${borrowLTV/100}%`);
  // Research: Is this a safe, liquid asset? Do you trust it?
}
```

When depositing into a vault, you're exposed to the collateral assets that borrowers can use. Assess:

- **What collaterals are accepted?** Check `LTVList()` for all configured collaterals

- **Are these assets trustworthy?** Consider token contract risk, liquidity, price stability

- **Are the LTVs appropriate?** Higher LTV = more risk for lenders if collateral drops

- **Is the oracle reliable?** Bad price feeds can lead to undercollateralized loans

**Key Security Considerations:**

| Area | Risk | Mitigation |

|------|------|------------|

| Collateral quality | Bad debt from risky assets | Review accepted collaterals and their LTVs |

| Vault authenticity | Fake vault contracts | Verify via factory (`isProxy`) |

| Governor trust | Malicious parameter changes | Only use vaults with trusted governors |

| Oracle manipulation | Price feed attacks | Verify oracle source and configuration |

| Governance changes | Unexpected LTV/cap/IRM updates | Monitor events, verify governor identity |

| Hook exploitation | Custom logic vulnerabilities | Check hook configuration before use |

**Important:** Euler's GovernedPerspective only verifies initial configuration. Risk managers can change vault parameters at any time. Always verify you trust the vault's governor AND the accepted collateral assets before depositing funds.

Reference: [https://docs.euler.finance/security/audits](https://docs.euler.finance/security/audits), [https://github.com/euler-xyz/ethereum-vault-connector/tree/master/audits](https://github.com/euler-xyz/ethereum-vault-connector/tree/master/audits), [https://github.com/euler-xyz/euler-vault-kit/tree/master/audits](https://github.com/euler-xyz/euler-vault-kit/tree/master/audits)

---

## References

1. [https://docs.euler.finance](https://docs.euler.finance)
2. [https://github.com/euler-xyz/euler-vault-kit](https://github.com/euler-xyz/euler-vault-kit)
3. [https://github.com/euler-xyz/ethereum-vault-connector](https://github.com/euler-xyz/ethereum-vault-connector)
4. [https://github.com/euler-xyz/evk-periphery](https://github.com/euler-xyz/evk-periphery)
