---
title: "Installing [Product Name]"
description: "[Brief description of installation process and supported platforms in 1-2 sentences]"
type: guide
difficulty: beginner
duration: "15 minutes"
prerequisites:
  - [OS requirement]
  - [Prerequisite 2]
tags:
  - installation
  - setup
  - beginner
status: published
created: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
---


[Brief introduction explaining what will be installed and why these installation steps are needed.]

## System Requirements

**Minimum requirements**:

- **Operating System**: [OS] version [X.X] or higher
- **Memory**: [X GB] RAM
- **Disk Space**: [X GB] available
- **CPU**: [Specification]
- **Software**: [Required software] version [X.X]+

**Recommended requirements**:

- **Operating System**: [OS] version [X.X]
- **Memory**: [X GB] RAM
- **Disk Space**: [X GB] available
- **CPU**: [Specification]

**Check your system**:

```bash
[command-to-check-os]
[command-to-check-memory]
[command-to-check-disk]
```

## Installation Methods

Choose the installation method that best suits your environment:

- **[Method 1]** - Recommended for most users
- **[Method 2]** - For advanced users
- **[Method 3]** - For specific use case

## Method 1: [Package Manager] (Recommended)

### Prerequisites

Ensure [package-manager] is installed:

```bash
[package-manager] --version
```

Expected output:

```
[package-manager] version X.X.X
```

### Install [Product]

Install using [package-manager]:

```bash
[package-manager-install-command]
```

**What this installs**:

- [Product] binary at `/path/to/binary`
- Configuration files in `/path/to/config`
- Documentation in `/path/to/docs`

### Verify Installation

Confirm [Product] is installed correctly:

```bash
[product] --version
```

Expected output:

```
[product] version X.X.X
```

## Method 2: [Download Binary]

### Download

Download the latest release for your platform:

**Linux (x64)**:

```bash
wget https://releases.example.com/[product]-linux-x64.tar.gz
```

**macOS (ARM64)**:

```bash
curl -O https://releases.example.com/[product]-darwin-arm64.tar.gz
```

**Windows (x64)**:

```powershell
Invoke-WebRequest -Uri https://releases.example.com/[product]-windows-x64.zip -OutFile [product].zip
```

### Extract

Extract the downloaded archive:

**Linux/macOS**:

```bash
tar -xzf [product]-*.tar.gz
cd [product]
```

**Windows**:

```powershell
Expand-Archive [product].zip -DestinationPath [product]
cd [product]
```

### Install

Move binary to system path:

**Linux/macOS**:

```bash
sudo mv [product] /usr/local/bin/
sudo chmod +x /usr/local/bin/[product]
```

**Windows**: Add to PATH environment variable

### Verify Installation

Test the installation:

```bash
[product] --version
```

## Method 3: [Build from Source]

### Prerequisites

Install build dependencies:

```bash
[install-build-deps]
```

### Clone Repository

Clone the source code:

```bash
git clone https://github.com/example/[product].git
cd [product]
```

### Build

Compile the binary:

```bash
[build-command]
```

Expected output:

```
[build-success-message]
```

### Install

Install the compiled binary:

```bash
[install-command]
```

### Verify Installation

Test the installation:

```bash
[product] --version
```

## Post-Installation Configuration

### Create Configuration File

Create the default configuration file:

```bash
[product] init
```

This creates `[config-file]` with default settings:

```[language]
[default-config-content]
```

### Set Environment Variables

Add required environment variables:

**Linux/macOS** (add to `~/.bashrc` or `~/.zshrc`):

```bash
export [PRODUCT]_HOME=/path/to/[product]
export PATH=$PATH:$[PRODUCT]_HOME/bin
```

**Windows** (System Properties > Environment Variables):

```
Variable: [PRODUCT]_HOME
Value: C:\path\to\[product]
```

### Verify Configuration

Test the configuration:

```bash
[product] config verify
```

Expected output:

```
✓ Configuration valid
✓ All required settings present
```

## Upgrading

### Upgrade via Package Manager

```bash
[package-manager-upgrade-command]
```

### Upgrade via Binary

1. Download new version
2. Stop running instances: `[product] stop`
3. Replace binary: `sudo mv [product] /usr/local/bin/`
4. Restart: `[product] start`

### Verify Upgrade

```bash
[product] --version
```

## Uninstalling

### Uninstall via Package Manager

```bash
[package-manager-uninstall-command]
```

### Manual Uninstall

Remove [Product] files:

```bash
sudo rm /usr/local/bin/[product]
rm -rf ~/.config/[product]
rm -rf ~/.cache/[product]
```

### Verify Removal

```bash
[product] --version
```

Should return: `command not found`

## Troubleshooting

### Issue: "Command not found"

**Cause**: [Product] not in PATH

**Solution**:

```bash
echo $PATH
export PATH=$PATH:/usr/local/bin
```

Make permanent by adding to shell config file.

### Issue: "Permission denied"

**Cause**: Insufficient permissions

**Solution**:

```bash
sudo chmod +x /usr/local/bin/[product]
```

Or run with sudo:

```bash
sudo [product] [command]
```

### Issue: "Version mismatch"

**Cause**: Multiple installations or old version cached

**Solution**:

```bash
which [product]
[product] --version
```

Remove old installations and reinstall.

## Next Steps

Now that [Product] is installed:

1. [[Getting Started]](/docs/getting-started) - Quick start guide
2. [[Configuration Guide]](/docs/guides/configuration) - Configure for your needs
3. [[Tutorial]](/docs/tutorials/first-app) - Build your first application

## Platform-Specific Notes

### Linux

- **Dependencies**: [List dependencies]
- **Supported distributions**: [List distributions]
- **Package manager**: [apt, yum, dnf, etc.]

### macOS

- **Dependencies**: [List dependencies]
- **Minimum version**: macOS [X.X]
- **Apple Silicon**: Native ARM64 support

### Windows

- **Dependencies**: [List dependencies]
- **Minimum version**: Windows [X]
- **PowerShell**: Version [X.X]+ required

## Additional Resources

- [[Release Notes]](/docs/changelog) - Version history
- [[System Requirements]](/docs/requirements) - Detailed requirements
- [[Migration Guide]](/docs/migration) - Upgrade from older versions
- [[Support]](mailto:support@example.com) - Installation help
