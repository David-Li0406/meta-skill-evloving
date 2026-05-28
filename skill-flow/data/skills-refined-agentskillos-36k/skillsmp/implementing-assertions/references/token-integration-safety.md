# Token Integration Safety

## Common Non-Standard Behaviors
- Missing return values on `transfer`/`transferFrom`.
- Fee-on-transfer (amount received < amount requested).
- Rebasing (balances change outside transfers).
- Non-18 decimals (low or high decimals).
- Pausable or blacklisting tokens.

## Assertion Tactics
- Prefer balance deltas over return values when validating transfers.
- Treat amount received as authoritative for accounting.
- Do not assume fixed decimals; read `decimals()` where available.
- Expect reverts on zero-value transfers/approvals for some tokens.

## Example Pattern
```solidity
uint256 pre = token.balanceOf(vault);
// operation
uint256 post = token.balanceOf(vault);
uint256 received = post - pre;
require(received >= expectedMin, "Insufficient received");
```

## Triggers to Consider
- Mint/burn/transfer entrypoints.
- Settlement/accounting functions that rely on token balances.
