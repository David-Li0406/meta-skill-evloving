---
name: cardano-cli-staking
description: "Stake key registration, delegation, rewards withdrawal, and stake address operations with cardano-cli."
---

# cardano-cli-staking

## When to use
- Use when you need to register stake keys, delegate to a pool, or withdraw rewards via CLI.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Verify stake keys exist (stake.vkey/stake.skey) and you have a base address.

2) Query stake address info
   - Confirm stake key status (registered/unregistered) and rewards.

3) Register stake key (if needed)
   - Build and submit a tx that includes stake key registration certificate.

4) Delegate
   - Create delegation certificate to target pool id.
   - Build and submit tx with certificate.

5) Withdraw rewards (optional)
   - Include withdrawal plus change and ensure correct signing keys.


## Safety / key handling
- Stake operations require both payment and stake signing keys depending on action.
- Confirm pool id / bech32 correctness before delegating.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
