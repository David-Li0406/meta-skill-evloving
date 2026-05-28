---
name: update-llm-agents
description: Update llm-agents.nix flake input in home-manager configuration. Use when the user requests to update llm-agents, update the LLM agents package, or refresh the numtide/llm-agents.nix dependency.
---

# Update LLM Agents

Updates the llm-agents flake input to the latest version from the numtide/llm-agents.nix repository.

## Workflow

When the user requests to update llm-agents:

1. **Update the llm-agents flake input**
   ```bash
   nix flake update llm-agents
   ```

   This command:
   - Fetches the latest commit from github:numtide/llm-agents.nix
   - Updates the flake.lock file with the new revision and hash
   - Preserves all other flake inputs unchanged

2. **Verify the changes**
   ```bash
   nix flake check
   ```

   Or build without applying:
   ```bash
   nix build .#homeConfigurations.company-mbp.activationPackage
   ```

   This verifies the flake is valid and all packages build correctly without activating the configuration.

3. **Show what changed**
   ```bash
   git diff flake.lock
   ```

   Review the llm-agents revision change to confirm the update.

## Package Details

The flake.nix contains:
- **llm-agents**: LLM agents framework (github:numtide/llm-agents.nix)
- Passed to home-manager modules via extraSpecialArgs
- Updates bring in latest agent features and improvements

## Prerequisites

- Nix with flakes enabled
- Write access to the flake.lock file
- Internet connection to fetch latest llm-agents

## Example Usage

User: "Update llm-agents to the latest version"

Response workflow:
1. Navigate to the home-manager config directory
2. Run `nix flake update llm-agents`
3. Verify with `nix flake check` or `nix build`
4. Show the user what revision was updated to
5. Do NOT apply automatically
