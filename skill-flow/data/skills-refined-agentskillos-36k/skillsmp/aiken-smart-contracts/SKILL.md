---
name: aiken-smart-contracts
description: "Aiken workflows: project structure, writing validators, building, generating blueprints, and producing .plutus scripts for CLI/MeshJS."
---

# aiken-smart-contracts

## When to use
- Use when you are writing or auditing Aiken validators, or need the build → script artifact pipeline.

## Operating rules (must follow)
- Confirm the user's network (mainnet vs preprod/preview) and **magic** before generating commands.
- Print commands in **copy/paste blocks**. Keep secrets out of logs.
- For any `cardano-cli` command: verify syntax with `cardano-cli --help` (and era help) and adjust if needed.
- Use fresh protocol parameters from the target network when calculating fees or script execution units.

## Workflow
1) Initialize / inspect project
   - Confirm Aiken version and project dependencies.
   - Identify validators and parameters.

2) Write validator
   - Keep types explicit and minimize implicit assumptions.
   - For V3 contexts, ensure you match the expected interface.

3) Build and test
   - `aiken build`
   - `aiken check` / unit tests if present

4) Produce artifacts for chain usage
   - Generate blueprint and convert to `.plutus` as needed for `cardano-cli`.
   - Record script hash and address derivation steps.

5) Provide integration snippets
   - CLI script spend template
   - MeshJS script usage pointers


## Safety / key handling
- Treat datum/redeemer schemas as public APIs—version them.
- Verify script hashes after rebuilds; never assume unchanged binaries.


## References used by this skill
- `shared/PRINCIPLES.md` (repo)
