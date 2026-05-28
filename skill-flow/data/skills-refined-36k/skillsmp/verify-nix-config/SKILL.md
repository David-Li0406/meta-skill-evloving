---
name: verify-nix-config
description: Compile-only validation for Home Manager Nix/Emacs config changes. Use after editing any `*.nix` or `emacs.el` file to ensure the flake builds without switching profiles.
---

# Verify Nix Config (Compile Only)

Run a build-only check after changes to Nix or Emacs configuration to catch errors without activating a profile.

## Trigger

Use this workflow whenever editing:
- Any `*.nix` file (e.g., `common.nix`, `home.nix`, `osx.nix`, `flake.nix`)
- `emacs.el`

## Workflow

1. **Build activation package (no switch)**
   ```bash
   nix build .#homeConfigurations.company-mbp.activationPackage
   ```

   This compiles the Home Manager profile without applying it.

2. **If working on the Linux profile**
   ```bash
   nix build .#homeConfigurations.homelab-devbox.activationPackage
   ```

## Notes

- Do not run `home-manager switch` for verification.
- If the build fails, report the error output and stop before further edits.
