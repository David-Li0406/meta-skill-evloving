---
name: upgrade-agent-shell
description: Update agent-shell, shell-maker, and acp Emacs packages in home-manager flake.nix to their latest GitHub releases. Use when the user requests to upgrade agent-shell or its dependencies (shell-maker, acp) in the Nix flake configuration.
---

# Upgrade Agent Shell

Automates upgrading agent-shell and its dependencies (shell-maker and acp) in a home-manager flake.nix configuration.

## Workflow

When the user requests to upgrade agent-shell:

1. **Fetch latest versions**
   ```bash
   python scripts/fetch_latest_versions.py > versions.json
   ```

   This script:
   - Queries GitHub API for latest releases of agent-shell, shell-maker, and acp.el
   - Computes SHA256 hashes using `nix-prefetch-url`
   - Outputs JSON with version and hash information

2. **Update flake.nix**
   ```bash
   python scripts/update_flake.py flake.nix versions.json
   ```

   This script:
   - Reads the versions.json file
   - Updates version, rev, and sha256 fields for all three packages
   - Writes the updated flake.nix back to disk

3. **Verify the changes**
   ```bash
   nix flake check
   ```

   Or build without applying:
   ```bash
   nix build .#homeConfigurations.company-mbp.activationPackage
   ```

   This verifies the flake is valid and all packages build correctly without activating the configuration.

## Package Details

The flake.nix contains Emacs package overlays for:

- **agent-shell**: Main LLM-powered shell interface for Emacs
- **shell-maker**: Dependency providing shell creation framework
- **acp**: Dependency providing AI completion functionality

All three are maintained by xenodium on GitHub and must be updated together to maintain compatibility.

## Prerequisites

- `curl` (for fetching GitHub API data)
- `nix-prefetch-url` available (comes with Nix)
- Python 3.x
- Write access to the flake.nix file

## Example Usage

User: "Upgrade agent-shell to the latest version"

Response workflow:
1. Navigate to the home-manager config directory
2. Run fetch_latest_versions.py to get current releases
3. Run update_flake.py to update the flake.nix
4. Verify with `nix flake check` or `nix build`
5. Show the user what versions were updated
6. Do NOT apply automatically
