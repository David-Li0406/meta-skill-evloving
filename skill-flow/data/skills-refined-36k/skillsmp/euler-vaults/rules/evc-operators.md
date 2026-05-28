---
title: Delegate Control via Operators
impact: HIGH
impactDescription: Delegate control over your accounts to other addresses for automated strategies and position management
tags: evc, operators, delegation, automation, permissions
---

## Delegate Control via Operators

Operators are addresses authorized to act on behalf of an account. They enable automated strategies like stop-loss, take-profit, and position management without giving up custody.

**Incorrect (giving full wallet access):**

```solidity
// NEVER share private keys or use unlimited approvals for automation
// This is insecure and gives full control
IERC20(token).approve(automationContract, type(uint256).max);
```

**Correct (install operator for specific account):**

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

**Correct (operator executing on behalf of account):**

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

**Correct (TypeScript operator management):**

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

**Correct (operator with limited scope via hooks):**

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

Reference: [EVC Whitepaper - Operators](https://github.com/euler-xyz/ethereum-vault-connector/blob/master/docs/whitepaper.md#operators)
