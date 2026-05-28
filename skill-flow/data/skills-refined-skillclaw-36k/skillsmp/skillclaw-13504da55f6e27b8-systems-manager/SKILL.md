---
name: systems-manager
description: Use this skill when you need to manage system operations on both Linux and Windows platforms.
---

# Skill body

### Overview
This skill provides access to system management operations for both Linux and Windows environments.

### Capabilities
- **install_applications**: Installs applications using the native package manager with Snap fallback (Linux).
- **update**: Updates the system and applications (Linux).
- **clean**: Cleans system resources (e.g., trash/recycle bin) (Linux).
- **optimize**: Optimizes system resources (e.g., autoremove, defrag) (Linux).
- **install_python_modules**: Installs Python modules via pip (Linux).
- **install_fonts**: Installs specified Nerd Fonts or all available fonts if 'all' is specified (Linux).
- **get_os_statistics**: Retrieves operating system statistics (Linux).
- **get_hardware_statistics**: Retrieves hardware statistics (Linux).
- **add_repository**: Adds an upstream repository to the package manager repository list (Linux).
- **install_local_package**: Installs a local Linux package file using the appropriate tool (dpkg/rpm/dnf/zypper/pacman) (Linux).
- **run_command**: Runs a command on the host. Can run elevated for administrator or root privileges (Linux).
- **list_windows_features**: Lists all Windows features and their status (Windows).
- **enable_windows_features**: Enables specified Windows features (Windows).
- **disable_windows_features**: Disables specified Windows features (Windows).

### Usage Rules
- Use these tools when the user requests actions related to system management on either Linux or Windows.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please install an application"
- "Please update the system"
- "Please list windows features"
- "Please enable a windows feature"