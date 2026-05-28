---
name: systems-manager-management
description: Use this skill for managing system operations across Linux and Windows environments.
---

### Overview
This skill provides access to system management operations for both Linux and Windows platforms.

### Capabilities
- **install_applications**: Installs applications using the native package manager with Snap fallback.
- **update**: Updates the system and applications.
- **clean**: Cleans system resources (e.g., trash/recycle bin).
- **optimize**: Optimizes system resources (e.g., autoremove, defrag).
- **install_python_modules**: Installs Python modules via pip.
- **install_fonts**: Installs specified Nerd Fonts or all available fonts if 'all' is specified.
- **get_os_statistics**: Retrieves operating system statistics.
- **get_hardware_statistics**: Retrieves hardware statistics.
- **list_windows_features**: Lists all Windows features and their status.
- **enable_windows_features**: Enables specified Windows features.
- **disable_windows_features**: Disables specified Windows features.
- **add_repository**: Adds an upstream repository to the package manager repository list (Linux only).
- **install_local_package**: Installs a local Linux package file using the appropriate tool (dpkg/rpm/dnf/zypper/pacman).
- **run_command**: Runs a command on the host. Can run elevated for administrator or root privileges.

### Common Tools
- `install_applications`
- `update`
- `clean`
- `optimize`
- `install_python_modules`
- `install_fonts`
- `get_os_statistics`
- `get_hardware_statistics`
- `list_windows_features`
- `enable_windows_features`
- `disable_windows_features`
- `add_repository`
- `install_local_package`
- `run_command`

### Usage Rules
- Use these tools when the user requests actions related to **system management** for either Linux or Windows.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please optimize"
- "Please install applications"
- "Please install python modules"
- "Please disable windows features"
- "Please add repository"
- "Please install local package"
- "Please run command"
- "Please list windows features"