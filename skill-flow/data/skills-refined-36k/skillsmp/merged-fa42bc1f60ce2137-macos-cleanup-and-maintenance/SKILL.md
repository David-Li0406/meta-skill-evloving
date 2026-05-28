---
name: macos-cleanup-and-maintenance
description: Use this skill for comprehensive macOS system cleanup and maintenance, including cache clearing, application uninstallation, disk space analysis, and development environment cleanup.
---

# macOS Cleanup and Maintenance

## Overview

This skill provides a complete workflow for cleaning and maintaining macOS systems, utilizing the Mole tool for cache clearing, application uninstallation, disk space analysis, and development environment cleanup. It supports interactive menu selection, intelligent diagnostics, and safe operations (default dry-run + user confirmation).

## Core Principles

1. **Safety First**: Default to `--dry-run` previews, and require user confirmation before executing dangerous operations.
2. **Detailed Logging**: Record all operations for auditing and traceability.
3. **Gradual Execution**: Progress from preview to confirmation to execution.
4. **User Autonomy**: Provide clear guidance, allowing users to choose manual execution or AI-assisted execution.

## Workflow Decision Tree

```
User Request
   │
   ├─ Uncertain about what to clean?
   │  └─→ Run Intelligent Diagnostic Cleanup
   │
   ├─ Specific Cleanup Needs
   │  │
   │  ├─ Quick Cleanup / Regular Maintenance
   │  │  └─→ Daily Cleanup
   │  │
   │  ├─ Low Disk Space / Thorough Cleanup
   │  │  └─→ Deep Cleanup
   │  │
   │  └─ Development Environment / Build Artifacts
   │     └─→ Developer Cleanup
   │
   └─ Specific Operations
      ├─ System Cache → mo clean --dry-run
      ├─ Application Uninstallation → mo uninstall
      ├─ Disk Analysis → mo analyze
      ├─ System Optimization → mo optimize --dry-run
      ├─ Project Cleanup → mo purge
      └─ Installation Files → mo installer
```

## Cleanup Scenarios

### Scenario 1: Daily Cleanup

**Goal**: Quickly clean system caches, logs, and temporary files for regular maintenance.

**Workflow**:

1. **System Diagnostics** (optional)
   ```bash
   mo status
   ```
   Displays system health status: CPU, memory, disk usage, etc.

2. **Preview Cleanup Plan**
   ```bash
   mo clean --dry-run
   ```
   Lists caches and files to be cleaned along with their sizes.

3. **User Confirmation**
   Use AskUser to confirm whether to proceed with the cleanup:
   - Show preview results.
   - Ask if they want to continue.
   - Provide options for "clean specific categories only."

4. **Execute Cleanup**
   ```bash
   # Based on user confirmation
   mo clean                    # Full cleanup
   # or
   mo clean --whitelist        # Selective cleanup
   ```

5. **Log Results**
   Display a comparison of disk space before and after cleanup.

**User Interaction Example**:
```
Found the following items to clean:
- User application cache: 45.2GB
- Browser cache: 10.5GB
- Developer tools: 23.3GB
- System logs and temporary files: 3.8GB
- Trash: 12.3GB

Estimated space to be freed: 95.5GB

Would you like to proceed with the cleanup?
1. Full cleanup
2. Selective cleanup (skip browser cache)
3. Show detailed operation plan only
4. Cancel
```

### Scenario 2: Deep Cleanup

**Goal**: Thoroughly clean the system, including application uninstallation, large file analysis, and system optimization.

**Workflow**:

1. **Disk Space Analysis**
   ```bash
   mo analyze
   ```
   Visualizes disk usage, identifying large files and directories.

2. **Application Uninstallation** (if needed)
   ```bash
   mo uninstall
   ```
   Interactively select applications to uninstall, thoroughly removing them and their residual files.

3. **Deep Cache Cleanup**
   ```bash
   mo clean --dry-run --debug
   ```
   Displays a detailed cleanup plan, including risk levels and file information.

4. **Installation File Cleanup**
   ```bash
   mo installer
   ```
   Finds and deletes downloaded installation files (.dmg, .pkg, etc.).

5. **System Optimization**
   ```bash
   mo optimize --dry-run
   ```
   Previews optimization operations: rebuilding system caches, refreshing services, etc.

6. **Step-by-Step Confirmation and Execution**
   Each step requires user confirmation via AskUser.

**User Interaction Example**:
```
Deep cleanup includes the following steps:
1. Disk space analysis ✓
2. Application uninstallation (found 3 rarely used apps)
3. Deep cache cleanup (estimated to free 95.5GB)
4. Installation file cleanup (found 3.8GB of installation files)
5. System optimization (rebuild caches and refresh services)

Which step would you like to start with?
- Execute step-by-step (confirm each step)
- Execute all (final confirmation)
- Skip certain steps
```

### Scenario 3: Developer Cleanup

**Goal**: Clean the development environment by removing node_modules, build artifacts, and other development-related files.

**Workflow**:

1. **Scan Project Build Artifacts**
   ```bash
   mo purge
   ```
   Scans default project directories (~/Projects, ~/GitHub, ~/dev, etc.).

2. **Display Cleanup Options**
   Lists all projects and their build artifact sizes:
   - Mark recent projects (<7 days) as unchecked by default.
   - Show the type of build for each project (node_modules, target, venv, etc.).

3. **Custom Scan Paths** (optional)
   ```bash
   mo purge --paths
   ```
   Configure directories to scan.

4. **Confirm and Clean**
   Use AskUser to confirm which projects to clean.

5. **Log Cleanup Results**
   Display the freed space and list of cleaned projects.

**User Interaction Example**:
```
Found the following project build artifacts (total 18.5GB):

➤ ● my-react-app       3.2GB | node_modules  >6mo
  ● old-project        2.8GB | node_modules  >6mo
  ● rust-app           4.1GB | target        >6mo
  ○ current-work       856MB | node_modules  | Recent (2 days)
  ● django-api         2.3GB | venv          >6mo

Which projects would you like to clean?
- Clean all (keep recent projects)
- Selective cleanup
- View detailed information
- Cancel
```

### Scenario 4: Intelligent Diagnostic Cleanup

**Goal**: Automatically determine what cleanup operations are needed based on system status.

**Workflow**:

1. **System Health Check**
   ```bash
   mo status
   ```
   Retrieves system status: CPU, memory, disk, network, etc.

2. **Disk Space Analysis**
   ```bash
   mo analyze ~/Downloads ~/Documents
   ```
   Analyzes disk usage in user directories.

3. **Intelligent Assessment**
   Based on system status, suggest cleanup actions:
   - Disk usage >80% → Recommend deep cleanup.
   - Disk usage 60-80% → Recommend daily cleanup.
   - Large number of development projects → Recommend developer cleanup.
   - System performance decline → Recommend system optimization.

4. **Provide Cleanup Plan**
   List recommended cleanup operations and expected effects.

5. **User Selection**
   Use AskUser to let the user choose which cleanup plan to execute.

**User Interaction Example**:
```
System diagnostic results:
- Disk usage: 78.3% (333/460 GB)
- Memory usage: 58.4% (14.2/24 GB)
- CPU load: Normal
- Found: 8 old projects, 12.3GB in Trash, 3.8GB in installation files

Recommended cleanup plans:
Plan A: Daily cleanup + Developer cleanup (estimated to free 30GB)
Plan B: Deep cleanup (estimated to free 110GB)
Plan C: Only clean Trash and installation files (estimated to free 16GB)

Choose a plan or customize cleanup operations?
```

## Safety Policies

### 1. Default Dry-Run

All cleanup operations default to `--dry-run` previews, not executing deletions:

```bash
# Incorrect example (direct execution)
mo clean

# Correct example (preview first)
mo clean --dry-run
```

### 2. User Confirmation

Before executing any dangerous operations, AskUser must obtain explicit user consent:

**Confirmation Template**:
```
About to execute the following operations:
- Clean system cache (45.2GB)
- Clean browser cache (10.5GB)
- Clean Trash (12.3GB)

Estimated space to be freed: 67.7GB

Confirm execution?
- Yes, execute cleanup
- Only execute certain operations
- Cancel
```

### 3. Detailed Operation Logging

Record all operations, including:
- Executed commands
- Timestamps
- Files cleaned and their sizes
- System status before and after cleanup

### 4. Gradual Disclosure

For advanced options, use `--debug` and `--whitelist` to provide more detailed information:

```bash
mo clean --dry-run --debug    # Detailed preview, including risk levels
mo clean --whitelist          # Manage protected cache paths
```

## Interactive Menu

### Main Menu Structure

```
macOS Maintenance Cleanup Assistant
══════════════════════════════

Please select a cleanup mode:

1. 💨 Daily Cleanup (quickly clean caches and temporary files)
2. 🔍 Deep Cleanup (thoroughly clean system and applications)
3. 💻 Developer Cleanup (clean project build artifacts)
4. 🩺 Intelligent Diagnostics (automatically determine cleanup plan)
5. ⚙️  Individual Operations

Select mode (1-5) or describe your needs:
```

### Individual Operations Menu

```
Individual Operations
══════════════════════════════

1. 🧹 System Cache Cleanup (mo clean)
2. 🗑️  Application Uninstallation (mo uninstall)
3. 📊 Disk Space Analysis (mo analyze)
4. ⚡ System Optimization (mo optimize)
5. 📦 Project Build Cleanup (mo purge)
6. 💿 Installation File Cleanup (mo installer)
7. 📈 System Status Monitoring (mo status)

Select operation (1-7):
```

## References

### Mole Command Reference

For detailed command descriptions, refer to: [references/mole-commands.md](references/mole-commands.md)

Includes:
- Detailed usage for all Mole commands
- Common parameters and options
- Output format descriptions
- Best practices and considerations

### Cleanup Best Practices

For detailed guidelines, refer to: [references/cleanup-best-practices.md](references/cleanup-best-practices.md)

Includes:
- Recommended cleanup frequency
- Safety considerations
- Common issues and solutions
- Performance optimization tips

## Platform Compatibility

This skill is primarily based on the Mole tool and is designed specifically for macOS. For cross-platform needs:

- **macOS**: Use the Mole tool (full functionality)
- **Windows/Linux**: Provide equivalent native commands and alternative tools

For non-macOS platforms, refer to [references/cross-platform-alternatives.md](references/cross-platform-alternatives.md)

## Usage Examples

### Example 1: Quick Daily Cleanup

**User Request**:
```
Help me clean my Mac system.
```

**AI Response**:
```
I'll help you clean your Mac system. First, let me check the system status:

[Execute mo status]

Found the following items to clean:
- User application cache: 45.2GB
- Browser cache: 10.5GB
- System logs: 3.8GB

Estimated space to be freed: 59.5GB

[Use AskUser]
Would you like to proceed with the daily cleanup?
1. Execute cleanup (preview then confirm)
2. Show detailed cleanup plan only
3. Customize cleanup options
```

### Example 2: Deep Cleanup

**User Request**:
```
My disk space is running low, I need a deep cleanup.
```

**AI Response**:
```
I'll assist you with a deep cleanup. Let me analyze the disk usage first:

[Execute mo analyze]

Found the following issues:
- Disk usage: 82% (377/460 GB)
- Large folders: Library (75.4GB), Downloads (34.6GB)
- Cleanable items: caches 95.5GB, installation files 3.8GB

Recommended deep cleanup plan:
1. Clean system caches (95.5GB)
2. Clean installation files (3.8GB)
3. Uninstall rarely used applications (found 3, totaling 12.8GB)

[Use AskUser]
Which cleanup operations would you like to execute?
```

### Example 3: Developer Cleanup

**User Request**:
```
Clean my development environment, remove old node_modules.
```

**AI Response**:
```
I'll help you clean the build artifacts in your development environment:

[Execute mo purge]

Found the following project build artifacts (total 18.5GB):
- my-react-app (3.2GB, node_modules)
- old-project (2.8GB, node_modules)
- current-work (856MB, node_modules, Recent)

[Use AskUser]
Which projects would you like to clean?
- Clean all (keep recent projects)
- Selective cleanup
- View detailed information
```

## Considerations

1. **Data Safety**: While Mole is designed to be safe, file deletions are permanent; please review operations carefully.
2. **Terminal Compatibility**: iTerm2 has known compatibility issues; recommend using Alacritty, kitty, WezTerm, Ghostty, or Warp.
3. **Regular Cleanup**: It is advisable to perform daily or monthly cleanups to maintain system health.
4. **Backup Important Data**: Before executing any cleanup over 10GB, it is recommended to back up important data.