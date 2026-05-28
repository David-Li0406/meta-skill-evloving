---
name: meshjs-cardano
description: "MeshJS usage patterns: building txs, UTxO selection, datums/redeemers, script interactions, and wallet connectors."
---

# meshjs-cardano

## When to use
- Use when you are building Cardano dApps in TS/JS with MeshJS and want best-practice patterns and pitfalls.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Confirm environment
   - Node version, bundler (Next.js/Vite), and MeshJS package versions.
   - Wallet connector expectations (Eternl, Nami, Lace, etc.)

2) Transaction building
   - UTxO selection strategy
   - Change address discipline
   - Asset bundles and metadata

3) Script interactions
   - Inline datums, reference scripts, redeemers
   - Collateral selection in browser wallets
   - Submit + confirmation UX

4) Provide a minimal working example aligned with the user’s stack.


## Safety / key handling
- Never request users to paste seed phrases.
- Validate CIP-30 wallet API availability and handle disconnects gracefully.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
