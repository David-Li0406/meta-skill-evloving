---
name: cursor-setup
description: Cursor AI-powered editor setup and configuration on NixOS including AppImage extraction, version updates, cursor-agent patching, and troubleshooting
---

# Cursor - AI-powered Code Editor

## Overview

Cursor is an AI-powered code editor built on VSCode. On NixOS, we use a custom package that extracts and patches the AppImage to work properly with the NixOS environment.

## Installation

Cursor is installed via the NixOS system configuration:

```nix
# nixos/configuration.nix
environment.systemPackages = with pkgs; [
  (pkgs.callPackage ./packages/cursor/extracted.nix { })
];
```

## Update Procedure

### 1. Check for New Version

Visit the [Cursor Downloads page](https://cursor.com/download) or check the [changelog](https://changelog.cursor.com/) for the latest version.

### 2. Update Package Definition

Edit `nixos/packages/cursor/extracted.nix`:

```nix
let
  pname = "cursor";
  version = "1.6.45";  # Update this version number

  src = fetchurl {
    url = "https://downloads.cursor.com/production/COMMIT_HASH/linux/x64/Cursor-${version}-x86_64.AppImage";
    hash = "sha256-PLACEHOLDER";  # This will be updated in the next step
  };
```

**Finding the download URL:**
1. Go to https://cursor.com/download
2. Open browser DevTools (F12) → Network tab
3. Click the Linux download button
4. Copy the download URL from the network request
5. The URL format: `https://downloads.cursor.com/production/{commit}/linux/x64/Cursor-{version}-x86_64.AppImage`

### 3. Calculate SHA256 Hash

Use `nix-prefetch-url` to download and calculate the hash:

```bash
# Download and get SHA256 hash
nix-prefetch-url https://downloads.cursor.com/production/COMMIT_HASH/linux/x64/Cursor-1.6.45-x86_64.AppImage

# Convert to SRI format (sha256-...)
nix --extra-experimental-features 'nix-command' hash convert --hash-algo sha256 --to sri HASH_FROM_ABOVE
```

Update the `hash` field in `extracted.nix` with the SRI format hash (e.g., `sha256-ABC123...=`).

### 4. Build and Apply

```bash
# Build the new package
sudo nixos-rebuild switch --flake .#desktop

# Or for testing without system changes
nix build .#nixosConfigurations.desktop.config.environment.systemPackages -L
```

### 5. Verify Installation

```bash
cursor --version
```

## NixOS-Specific Implementation

### Automatic cursor-agent Patching

The Cursor package includes an automatic patcher for the `cursor-agent` node binaries. This is necessary because Cursor downloads its own Node.js binaries to `~/.local/share/cursor-agent/versions/`, which are dynamically linked and won't work on NixOS without patching.

**How it works:**
1. When you launch Cursor, the wrapper script checks for cursor-agent directories
2. For each version directory containing an unpatched `node` binary:
   - Sets the correct ELF interpreter for NixOS
   - Sets the runtime library path (rpath)
   - Creates a `.patched` marker file to avoid re-patching

**Location:** `nixos/packages/cursor/extracted.nix:130-161`

### Manual Patching (if needed)

If cursor-agent fails to run, you can manually patch the node binary:

```bash
# Get the NixOS dynamic linker path
INTERPRETER=$(nix --extra-experimental-features 'nix-command flakes' eval --raw 'nixpkgs#stdenv.cc.bintools.dynamicLinker')

# Get the library path
LIBPATH=$(nix --extra-experimental-features 'nix-command flakes' eval --raw 'nixpkgs#stdenv.cc.cc.lib.outPath')/lib

# Patch the binary
nix --extra-experimental-features 'nix-command flakes' run nixpkgs#patchelf -- \
  --set-interpreter "$INTERPRETER" \
  --set-rpath "$LIBPATH" \
  ~/.local/share/cursor-agent/versions/*/node
```

## Troubleshooting

### Issue: `Could not start dynamically linked executable`

**Error message:**
```
Could not start dynamically linked executable: /home/user/.local/share/cursor-agent/versions/.../node
NixOS cannot run dynamically linked executables intended for generic linux environments out of the box.
```

**Solution:**
1. The automatic patcher should handle this, but if it fails, use the manual patching steps above
2. Check if the `.patched` marker file exists in the cursor-agent version directory
3. Remove the `.patched` file and restart Cursor to trigger re-patching
4. Verify the patcher script is working: check the Cursor wrapper at `/nix/store/.../bin/cursor`

### Issue: Build fails with `makeCWrapper: Unknown argument --run`

This error occurred in older versions when using `makeWrapper --run`. The current implementation uses a simple bash script wrapper instead.

**Solution:**
Ensure you're using the latest version of `nixos/packages/cursor/extracted.nix` from this repository.

### Issue: Wayland warnings on startup

**Warning messages:**
```
Warning: 'ozone-platform-hint' is not in the list of known options
Warning: 'enable-features' is not in the list of known options
```

**Status:**
These warnings are harmless and can be ignored. They appear because we pass Wayland-specific flags to enable proper Wayland support. Cursor functions correctly despite these warnings.

### Issue: Cursor doesn't start after update

**Checklist:**
1. Check if the AppImage was extracted correctly: `ls -la /nix/store/*-cursor-*/`
2. Verify the cursor binary is executable: `file $(which cursor)`
3. Check for error messages: `cursor --verbose`
4. Try rebuilding with verbose output: `sudo nixos-rebuild switch --flake .#desktop --show-trace`
5. Check the build logs: `nix log /nix/store/...-cursor-*.drv`

### Issue: Cursor-agent updates fail

If Cursor attempts to update cursor-agent but fails:

1. Clear the cursor-agent directory:
   ```bash
   rm -rf ~/.local/share/cursor-agent
   ```
2. Restart Cursor - it will re-download and the patcher will handle the new version

## Architecture Details

### Package Structure

```
nixos/packages/cursor/
├── extracted.nix       # Main package definition (AppImage extraction approach)
└── default.nix        # Alternative package (AppImage wrapper approach - not used)
```

We use the `extracted.nix` approach because:
- Better control over the binary patching
- Can modify internal files (sudo-prompt, ripgrep, etc.)
- More predictable behavior with cursor-agent
- Full access to patch node_modules and resources

### Key Dependencies

- `autoPatchelfHook`: Automatically patches ELF binaries
- `asar`: Unpacks/repacks VSCode's asar archives
- `wrapGAppsHook`: Sets up GTK/GLib environment variables
- `patchelf`: Runtime patching of cursor-agent binaries
- `ripgrep`: Replaced with Nix version for consistency

### Build Phases

1. **Extract**: AppImage is extracted using `appimageTools.extract`
2. **Patch**: Asar archives are unpacked, files are patched (sudo-prompt, ripgrep)
3. **Install**: Files are copied to output, wrapper script is created
4. **Fixup**: `autoPatchelfHook` and `wrapGAppsHook` process the binaries
5. **PostFixup**: Additional library dependencies are added to the main binary

## References

- [Cursor Official Website](https://cursor.com/)
- [Cursor Changelog](https://changelog.cursor.com/)
- [NixOS Dynamic Linking Guide](https://nix.dev/permalink/stub-ld)
- [AppImage Tools Documentation](https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/appimage/default.nix)
