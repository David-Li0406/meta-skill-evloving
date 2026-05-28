---
name: ssh-server-admin
description: Use this skill when you need to securely connect to and manage remote Linux/Unix servers via SSH, including executing commands, transferring files, and setting up port forwarding.
---

# SSH Server Administration

A comprehensive skill for secure remote server management via SSH. Supports command execution, file transfers, port forwarding, and tunneling. **Cross-platform compatible: Windows, macOS, and Linux.**

## Platform Detection

**CRITICAL: Detect the operating system first to use the correct SSH approach.**

Before executing SSH commands, check the platform:
- **Windows**: Use PowerShell or Windows OpenSSH (built into Windows 10+)
- **macOS/Linux**: Use standard bash SSH commands

## Authentication Methods (In Order of Preference)

### 1. SSH Key Authentication (RECOMMENDED - Works Everywhere)

SSH keys are the most secure and reliable method. They work identically on all platforms.

**Check for existing keys:**
```bash
# Windows (PowerShell)
Get-ChildItem ~/.ssh/id_*.pub

# macOS/Linux
ls -la ~/.ssh/id_*.pub
```

**If keys exist, use them:**
```bash
# All platforms - key auth is automatic if keys are set up
ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**If no keys exist, help user create them:**
```bash
# All platforms (works in PowerShell, bash, zsh)
ssh-keygen -t ed25519 -C "user@example.com"

# Copy public key to server (if ssh-copy-id available)
ssh-copy-id -i ~/.ssh/id_ed25519.pub [username]@[host]

# Or manually append to server's authorized_keys
cat ~/.ssh/id_ed25519.pub | ssh [username]@[host] "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 2. Password Authentication

**IMPORTANT: Password auth handling differs by platform.**

#### Windows Approach

Windows OpenSSH doesn't support `sshpass`. Use one of these methods:

**Option A: Use the included Python SSH helper (RECOMMENDED)**
```powershell
# Uses paramiko library for cross-platform SSH
python scripts/ssh_helper.py --host [host] --user [username] --password [password] --command "[command]"
```

**Option B: Interactive SSH (user types password)**
```powershell
# This will prompt for password interactively
ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**Option C: Use PuTTY's plink (if installed)**
```powershell
# Example command using plink
plink.exe -ssh [username]@[host] -pw [password] "[command]"
```