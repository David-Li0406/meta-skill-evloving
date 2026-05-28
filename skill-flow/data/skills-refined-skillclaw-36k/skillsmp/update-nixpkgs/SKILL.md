---
name: update-nixpkgs
description: Update nixpkgs flake input in home-manager configuration. Use when the user requests to update nixpkgs, update the Nix package repository, or refresh system packages to their latest versions.
---

# Update Nixpkgs

Updates the nixpkgs flake input to the latest version from the nixos-unstable branch.

## Workflow

When the user requests to update nixpkgs:

1. **Update the nixpkgs flake input**
   ```bash
   nix flake update nixpkgs
   ```

   This command:
   - Fetches the latest commit from github:nixos/nixpkgs/nixos-unstable
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

   Review the nixpkgs revision change to confirm the update.

## Package Details

The flake.nix contains:
- **nixpkgs**: Main package repository (github:nixos/nixpkgs/nixos-unstable)
- Used by home-manager and all package definitions
- Updates bring in latest package versions and security fixes

## Prerequisites

- Nix with flakes enabled
- Write access to the flake.lock file
- Internet connection to fetch latest nixpkgs

## Example Usage

User: "Update nixpkgs to the latest version"

Response workflow:
1. Navigate to the home-manager config directory
2. Run `nix flake update nixpkgs`
3. Verify with `nix flake check` or `nix build`
4. Show the user what revision was updated to
5. Do NOT apply automatically
