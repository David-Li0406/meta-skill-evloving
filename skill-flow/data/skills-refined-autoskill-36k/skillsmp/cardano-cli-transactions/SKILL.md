---
name: cardano-cli-transactions
description: "Build, sign, and submit standard (non-script) transactions with cardano-cli, including change, fees, and TTL/validity."
---

# cardano-cli-transactions

## When to use
- Use when you need to send ADA or native assets, manage UTxOs, or do offline/online signing workflows.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Gather inputs
   - Sender address + signing key path
   - Recipient address
   - Amount (lovelace) and optional asset bundle
   - Target network flags

2) Query UTxOs and choose inputs
   - Prefer consolidating inputs intentionally (avoid accidental dust).
   - Calculate change output.

3) Fetch protocol parameters
   - Dump pparams to file (fresh from network).

4) Build tx body
   - Use `transaction build` (online) when possible.
   - Use `build-raw` only for offline/cold-key workflows.

5) Sign + submit
   - Create witness set (or full signed tx) and submit.
   - Verify by querying UTxO for recipient and checking tx hash.

6) Produce a reproducible “tx bundle” folder
   - tx.raw / tx.body, pparams.json, witnesses, and a command log.


## Safety / key handling
- Never expose signing keys.
- Confirm the destination address (checksum mindset).
- On mainnet: recommend a small test transfer first.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
