---
name: plutus-v3-conway
description: "Conceptual + practical notes for Plutus V3 under Conway/Chang: contexts, governance purposes, and migration gotchas."
---

# plutus-v3-conway

## When to use
- Use when you are migrating from Plutus V2 → V3, or dealing with Conway governance scripts.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Identify your target
   - Spending/Minting vs Governance (voting/proposing)

2) Understand V3 interface
   - Single context argument; datum/redeemer are inside context; datum may be optional.
   - Return type conventions (unit) and failure signaling.

3) Migration checklist
   - Datum/redeemer shape changes
   - How you compute and validate script hash/address
   - PParams fields relevant to reference scripts and fees

4) Produce actionable guidance for the user’s chosen stack
   - Aiken guidance if they’re using Aiken
   - CLI flags if they’re using `cardano-cli`
   - MeshJS patterns if they’re using TS


## Safety / key handling
- Plutus V3 governance scripts are high-stakes. Test thoroughly on testnets.
- Avoid mixing V2 mental models into V3 contexts without verifying data access patterns.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
