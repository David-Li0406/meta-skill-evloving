# Offline Updates

For air-gapped or isolated systems, THOR supports offline update workflows.

## Overview

Offline updates require two steps:
1. **Download** on internet-connected machine
2. **Install** on offline/target machine

## Step 1: Download on Connected Machine

Use a machine with internet access and thor-util:

```bash
# Download Windows package
thor-util download -t thor10-win

# Download Linux package
thor-util download -t thor10-linux

# Download macOS package
thor-util download -t thor10-macos
```

### TechPreview Packages

```bash
thor-util download -t thor10-win --techpreview
thor-util download -t thor10-linux --techpreview
```

### What Gets Downloaded

The download creates a complete package including:
- THOR binaries
- All signatures
- Default configuration files
- Documentation

**Note**: This is equivalent to a fresh installation package.

## Step 2: Transfer Package

Transfer the downloaded package to the offline system via:
- USB drive
- Network share (if available)
- Secure file transfer
- Physical media

The package is typically a ZIP or directory structure.

## Step 3: Install on Offline Machine

On the offline/target machine:

```bash
thor-util install
```

This extracts and installs the previously downloaded package.

## Signature-Only Updates

For signature updates without program file changes:

### On Connected Machine

```bash
# Download just signatures
thor-util update

# Package the signatures directory
# (Manual: zip ./signatures folder)
```

### On Offline Machine

1. Extract signatures to `./signatures/`
2. Verify with a quick scan

## Preserving Custom Configuration

When using `download` + `install`, default configs are installed.

**To preserve customizations:**

1. Backup before install:
   ```bash
   cp ./config/thor.yml ./config/thor.yml.backup
   cp ./config/false_positive_filters.cfg ./config/false_positive_filters.cfg.backup
   ```

2. Run install:
   ```bash
   thor-util install
   ```

3. Restore customizations:
   ```bash
   cp ./config/thor.yml.backup ./config/thor.yml
   cp ./config/false_positive_filters.cfg.backup ./config/false_positive_filters.cfg
   ```

## Offline YARA-Forge

YARA-Forge rules can also be transferred offline:

### On Connected Machine

```bash
thor-util yara-forge download --ruleset extended
```

### Transfer

Copy `./custom-signatures/yara-forge/` directory.

### On Offline Machine

Place in `./custom-signatures/yara-forge/`

## License Considerations

- Offline machines still require valid `.lic` files
- License files don't need internet once installed
- License expiration checked locally
- Cannot fetch new licenses offline (must be pre-deployed)

## Automation Script Example

For regular offline updates, create a script on the connected machine:

```bash
#!/bin/bash
# offline-update-prep.sh

DATE=$(date +%Y%m%d)
OUTPUT_DIR="/path/to/usb/thor-update-${DATE}"

mkdir -p "$OUTPUT_DIR"

# Download packages
thor-util download -t thor10-win -o "$OUTPUT_DIR/thor10-win"
thor-util download -t thor10-linux -o "$OUTPUT_DIR/thor10-linux"

# Get YARA-Forge
thor-util yara-forge download --ruleset extended

# Copy YARA-Forge rules
cp -r ./custom-signatures/yara-forge "$OUTPUT_DIR/"

echo "Update package ready at: $OUTPUT_DIR"
```

## Verification

After offline installation, verify:

```bash
# Check version
thor64.exe --version

# Check signatures loaded
thor64.exe --print-signatures | head -20

# Quick test scan
thor64.exe --quick -a Filescan -p /tmp -e /tmp/test-output
```

## Troubleshooting

### "No package to install"

Ensure download was completed on the connected machine and transferred completely.

### License errors after install

Re-copy the `.lic` file(s) to the THOR directory.

### Missing signatures

Verify `./signatures/` directory transferred completely.

### Old version still running

Ensure you're running the newly installed binary, not a cached/old copy.
