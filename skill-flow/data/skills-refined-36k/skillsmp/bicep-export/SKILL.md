---
name: bicep-export
description: Generates a set of .bicep files to replicate existing Azure infrastructure
---

# Skill Instructions

## Goal

Generate a new, human-maintainable set of `.bicep` files plus a `.bicepparam` file that can redeploy the *current live state* of a target Azure resource group as a **no-op** (i.e., deploying should produce no changes).

## Guiding Principles

- Optimize for maintainability and clarity: split into sensible modules, use descriptive names, and factor repeated patterns.
- Prefer templates that look like they were written by a human, not a direct export dump.
- If there is a trade-off between “prettier” and “no-op correctness,” correctness wins.

## Inputs

Ensure you have the subscriptionId and resourceGroup of the resource group to export from the user before starting.

## Required Tools / Commands

Strongly prefer the following tools/commands as part of the workflow, instead of finding other tools or CLI commands to call:

- `get_bicep_best_practices` MCP tool: learn current best practices before refactoring.
- `get_bicep_file_diagnostics` MCP tool: compile/validate Bicep and address errors/warnings during edits.
- `get_deployment_snapshot` MCP tool: predict deployment output; take “before” and “after” snapshots and compare.
- `what_if_deployment` MCP tool: run a live diff against Azure using a `.bicepparam` file.
- `az group export ...` CLI command: export the live resource group to bootstrap the initial template.

## Workflow

### 1) Bootstrap from Live State (Export)

- Run `az group export ...` against the target resource group to get an initial baseline. This will give you a very rough machine-generated output.
- Use the `--export-format bicep` and `--output tsv` arguments to obtain a `.bicep` file output.
- Use the `--skip-all-params` argument to avoid generating parameter statements.
- Only pipe stdout, don't use `2>&1` to pipe stderr to file.
- Treat export output as input material only; plan to refactor heavily for readability and long-term maintenance.
- Generate an empty `.bicepparam` file, pointing to the exported `.bicep` file - for example, assuming it is named `.main.bicep`:
    ```bicep
    using 'main.bicep'
    ```
- Clearly differentiate the fact that these files are raw exports by naming them `exported_raw.bicepparam` and `exported_raw.bicep`

### 2) Capture snapshot file

- Capture a snapshot for the “before” state (initial exported structure + parameters) using the `get_deployment_snapshot` MCP tool.
- Ensure you pass it all the inputs (subscription id, resource group name) that you have values for.
- Save the MCP tool output to `exported_raw.snapshot.json`, bearing in mind it is a large file.

### 3) Refactor for maintainability

Refactor the exported output into a clean structure:

- Do not modify the raw exported files, create a new file structure instead.
- Use a main entrypoint (for example `main.bicep`) and split resources into modules by domain (for example: network, compute, storage, identity, monitoring).
- Use parameters and variables judiciously: avoid abstraction for its own sake; prefer clarity. Examples where you might want to use parameters are valuse that the user may want to vary between deploymens to different environments - e.g. locations, resource base names, subscription Ids, application Ids.
- Declare parameter values in the `.bicepparam` file, rather than using default values in the `.bicep` file parameter declarations.
- Prefer stable, explicit resource names and scopes.
- Preserve drift-sensitive configuration needed for a no-op (examples: identity blocks, SKU/tier, role assignments, locks, private endpoints/DNS, diagnostics settings).
- Use snapshots when embarking on complex refactors to verify that the before+after produce the same desired state.

### 4) Keep the Template Healthy (Diagnostics)

- After each significant change, run `get_bicep_file_diagnostics` on the edited `.bicep` files.
- Fix compilation errors immediately.
- Review warnings and fix anything that could affect correctness, deployment behavior, or maintainability.

### 5) Predict Deployment Output (Snapshots)

This provides confidence that the code has been succesfully refactored without altering the outcome of the deployment.

- Capture a new snapshot of the “after” state (refactored modules + parameters) using the `get_deployment_snapshot` MCP tool.
- Ensure you pass it all the inputs (subscription id, resource group name) that you have values for.
- Save the MCP tool output to `main.snapshot.json`, bearing in mind it is a large file.
- Diff the new snapshot against the original snapshot, to ensure that all of the refactors have succesfully preserved semantics.
- If there are any semantic differences, iterate until snapshots are equivalent (or any differences are explicitly intentional and justified).

### 6) Validate Against Live Azure (What-If)

- Once snapshots look equivalent, use the `what_if_deployment` MCP tool, using the `.bicepparam` file.
- Review the **full** What-If output.
- The target outcome is a **no-op**: no creates, no deletes, no updates.
- If What-If reports changes, adjust templates/parameters until What-If is clean.

### 7) Cleanup

- Remove the temporary files (exported raw .bicep and .bicepparam files, and snapshots)

## Acceptance Criteria

- A coherent set of `.bicep` files + a `.bicepparam` file exists for the target resource group.
- The Bicep compiles cleanly (diagnostics show no errors; warnings are understood/acceptable).
- “Before vs after” snapshots are equivalent (or differences are explicitly intentional and justified).
- `what_if_deployment` indicates the deployment would have **no impact** on live resources.