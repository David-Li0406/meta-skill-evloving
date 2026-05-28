---
name: cardano-cli-plutus-scripts
description: "Build and submit Plutus script transactions via cardano-cli: datums, redeemers, collateral, reference scripts, and script spends."
---

# cardano-cli-plutus-scripts

## When to use
- Use when you are spending from a script address or creating outputs with inline datum / reference scripts via CLI.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Confirm script type and era
   - V2 vs V3 matters. Conway era introduces V3 and governance contexts.
   - Verify CLI has script flags you need (`--tx-in-script-file`, inline datum, redeemer, collateral).

2) Prepare artifacts
   - script file (.plutus), datum.json, redeemer.json (or value form), and pparams.json.
   - identify collateral UTxO at a payment address (ADA-only recommended).

3) Build tx
   - Include:
     - `--tx-in` (script UTxO)
     - script flags (script file, datum present, redeemer)
     - `--tx-in-collateral`
     - outputs + change address
   - Keep tx body and all artifacts together.

4) Sign and submit
   - Use required keys (payment key; script spends do not use script keys but do require collateral signer).
   - Submit and verify UTxO movement.

5) Debug
   - If script fails, inspect execution units, datum/redeemer shape, and pparams alignment.


## Safety / key handling
- Always include collateral for Plutus script spends.
- Keep datum/redeemer free of secrets; these are on-chain visible.
- Prefer preprod/preview rehearsals before mainnet.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
