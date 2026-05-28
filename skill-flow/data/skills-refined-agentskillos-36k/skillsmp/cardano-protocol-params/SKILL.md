---
name: cardano-protocol-params
description: "Fetch protocol parameters, understand fee inputs, and keep pparams aligned with the target era/network."
---

# cardano-protocol-params

## When to use
- Use when you need to fetch `pparams.json`, compute min-UTxO/fees, or debug fee/script budgeting issues.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Fetch fresh params with `cardano-cli query protocol-parameters` for the target network.

2) Validate params fields used by your workflow:
   - min fee coefficients, coins per UTxO byte, execution unit prices, ref-script pricing, etc.

3) For script txs:
   - ensure you use params consistent with the era (Conway) and script version (V2/V3).

4) Capture params alongside tx artifacts for reproducibility.


## Safety / key handling
- Never assume params from mainnet apply to testnets.
- Always keep the pparams file that was used to build a tx (it matters for audit/debug).


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
