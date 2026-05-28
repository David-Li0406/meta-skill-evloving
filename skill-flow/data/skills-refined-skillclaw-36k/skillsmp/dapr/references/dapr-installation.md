# DAPR Installation Guide

## Overview
This guide provides instructions for installing the DAPR CLI on different platforms. The DAPR CLI is the main tool for various DAPR-related tasks such as running applications with a DAPR sidecar, reviewing sidecar logs, listing running services, and running the DAPR dashboard.

## Prerequisites
- Docker Desktop with the default Docker socket enabled (for Linux/macOS)
- Administrative rights (for Windows installations)

## Installing the DAPR CLI

### Linux Installation

#### Install from Terminal
Install the latest Linux DAPR CLI to `/usr/local/bin`:
```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

#### Installing a specific CLI version
To install a specific version (replace `<VERSION>` with the desired version number):
```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash -s <VERSION>
```

#### Install without `sudo`
If you do not have access to the `sudo` command or your username is not in the `sudoers` file, you can install DAPR to an alternate directory via the `DAPR_INSTALL_DIR` environment variable:
```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | DAPR_INSTALL_DIR="$HOME/dapr" /bin/bash
```

To install a specific version without `sudo`:
```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | DAPR_INSTALL_DIR="$HOME/dapr" /bin/bash -s <VERSION>
```

### Windows Installation

#### Install from Command Prompt
Install the latest Windows DAPR CLI to `$Env:SystemDrive\dapr` and add this directory to the User PATH environment variable:
```powershell
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
```

#### Installing a specific CLI version
To install a specific version:
```powershell
powershell -Command "$script=iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1; $block=[ScriptBlock]::Create($script); invoke-command -ScriptBlock $block -ArgumentList <VERSION>"
```

#### Install without administrative rights
If you do not have admin rights, you can install DAPR to an alternate directory:
```powershell
$Env:DAPR_INSTALL_DIR = "<your_alt_install_dir_path>"
$script=iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1; $block=[ScriptBlock]::Create($script); invoke-command -ScriptBlock $block -ArgumentList "", "$Env:DAPR_INSTALL_DIR"
```

#### Install using winget
Install the latest Windows DAPR CLI using winget:
```powershell
winget install Dapr.CLI
```

For preview releases:
```powershell
winget install Dapr.CLI.Preview
```

#### Install using MSI installer
1. Download the MSI package `dapr.msi` from the latest [DAPR release](https://github.com/dapr/cli/releases)
2. Navigate to the downloaded MSI file and double-click the file to run it
3. Follow the installation prompts to accept the license and the installation directory
4. The selected folder is added to the user PATH environment variable (default: `$Env:SystemDrive\dapr`)
5. Click `Install` to start the installation

### macOS Installation

#### Install from Terminal
Install the latest Darwin DAPR CLI to `/usr/local/bin`:
```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
```

To install a specific version:
```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash -s <VERSION>
```

#### Install from Homebrew
Install via [Homebrew](https://brew.sh):
```bash
brew install dapr/tap/dapr-cli
```

For ARM64 Macs:
```bash
arch -arm64 brew install dapr/tap/dapr-cli
```

#### Install without `sudo`
If you do not have access to the `sudo` command, install to an alternate directory:
```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | DAPR_INSTALL_DIR="$HOME/dapr" /bin/bash
```

To install a specific version without `sudo`:
```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | DAPR_INSTALL_DIR="$HOME/dapr" /bin/bash -s <VERSION>
```

### Manual Binary Installation

Each release of DAPR CLI includes binaries for various OSes and architectures. You can manually download and install these binary versions:

1. Download the desired DAPR CLI from the latest [DAPR Release](https://github.com/dapr/cli/releases)
2. Unpack it (e.g. `dapr_linux_amd64.tar.gz`, `dapr_windows_amd64.zip`)
3. Move it to your desired location
   - For Linux/macOS, we recommend `/usr/local/bin`
   - For Windows, create a directory and add this to your System PATH (e.g., `C:\dapr`)

## Verify Installation

Verify the CLI is installed by restarting your terminal/command prompt and running:
```bash
dapr -h
```

Expected output should show the DAPR CLI help with available commands such as:
- `init` - Install DAPR on supported hosting platforms
- `run` - Run DAPR and (optionally) your application side by side
- `list` - List all DAPR instances
- `dashboard` - Start DAPR dashboard
- `version` - Print the DAPR runtime and CLI version
- And more commands...

## Next Steps

After successful installation, you can:
1. Initialize DAPR in self-hosted mode: `dapr init`
2. Initialize DAPR in Kubernetes mode: `dapr init -k`
3. Run your first application with DAPR: `dapr run --app-id myapp --app-port 3000 node app.js`

## Troubleshooting

### Common Installation Issues
- **Permission Denied**: Ensure you have proper permissions or use the alternate directory installation method
- **Network Issues**: Check your internet connection and firewall settings
- **PATH Issues**: Restart your terminal after installation to refresh the PATH environment variable
- **Docker Not Found**: Ensure Docker is installed and running before initializing DAPR
