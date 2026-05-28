---
name: cardano-cli-wallets
description: "Create and manage Cardano CLI wallets: keys, addresses, UTxO checks, basic send/receive scaffolding."
---

# cardano-cli-wallets

## When to use
- Use when you need to create payment/stake keys, build addresses, or do basic wallet ops via `cardano-cli`.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Identify network
   - Ask for **mainnet** or **preprod/preview** and obtain `--testnet-magic <N>` if not mainnet.
   - Verify CLI era support: `cardano-cli --help` and `cardano-cli conway --help` (or `latest`).

2) Generate keys (payment + stake) into a new directory (never overwrite):
   - Create `payment.vkey/.skey` and `stake.vkey/.skey`.
   - Build base address (payment+stake) and enterprise address (payment only).

3) Fund address
   - Provide the address to receive ADA from faucet/exchange.
   - Confirm funds by querying UTxOs.

4) Inspect wallet state
   - UTxO query
   - Protocol parameters dump (for later fee calculation)
   - Optional: derive address from vkey and compare.

5) Output a “wallet dossier”
   - paths, address, network, magic, and command history.


## Safety / key handling
- Never paste `.skey` contents into chat.
- Prefer generating keys on an offline machine; move only `.vkey` / address online.
- If operating online, lock down filesystem permissions (`chmod 600 *.skey`) and avoid cloud sync.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
