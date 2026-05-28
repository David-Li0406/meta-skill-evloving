# macOS Fixes & Platform-Specific Issues

**Purpose**: Document macOS-specific issues and workarounds for Qara system.

**Platform Note**: This system appears to be running on Linux. This file documents macOS-specific fixes if Qara is used on macOS in the future.

**Last Updated**: 2025-11-19

---

## Current Platform

**Detected OS**: Linux

If you're running Qara on Linux, you likely don't need this file. Platform-specific Linux issues should be documented here as they arise.

---

## macOS-Specific Issues (If Applicable)

### Issue 1: File System Case Sensitivity

**Problem**: macOS file system is case-insensitive by default, which can cause git issues.

**Solution**:
```bash
# Check if using case-sensitive filesystem
diskutil info / | grep "File System"

# If needed, create case-sensitive volume for development
# (Requires APFS or HFS+)
```

### Issue 2: Command Line Tools

**Problem**: Some commands require Xcode Command Line Tools.

**Solution**:
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Verify installation
xcode-select -p
```

### Issue 3: Homebrew Path Issues

**Problem**: Homebrew installs to different locations on Intel vs Apple Silicon.

**Solution**:
```bash
# Intel Macs
export PATH="/usr/local/bin:$PATH"

# Apple Silicon Macs (M1/M2/M3)
export PATH="/opt/homebrew/bin:$PATH"

# Add to ~/.zshrc or ~/.bashrc
```

### Issue 4: File Permissions

**Problem**: macOS may restrict access to certain directories.

**Solution**:
```bash
# Grant Full Disk Access to Terminal/IDE
# System Preferences → Security & Privacy → Full Disk Access
# Add Terminal.app or VS Code
```

---

## Linux-Specific Issues

### Issue 1: Missing Dependencies

**Problem**: Some packages may not be installed by default.

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git curl build-essential

# Fedora/RHEL
sudo dnf install git curl gcc make

# Arch
sudo pacman -S git curl base-devel
```

### Issue 2: Permissions

**Problem**: Need permissions for ~/.claude directory.

**Solution**:
```bash
# Ensure proper ownership
chown -R $USER:$USER ~/.claude

# Ensure executability for scripts
chmod +x ~/.claude/bin/**/*.ts
```

---

## Cross-Platform Considerations

### Path Separators
```typescript
// ✅ Good: Use path module
import { join } from 'path';
const filePath = join(dir, file);

// ❌ Bad: Hardcoded separators
const filePath = dir + '/' + file;  // Breaks on Windows
```

### Line Endings
```bash
# Configure git to handle line endings
git config --global core.autocrlf input  # Linux/macOS
git config --global core.autocrlf true   # Windows
```

### Shell Scripts
```bash
#!/usr/bin/env bash
# ✅ Portable shebang

#!/bin/bash
# ❌ May not work if bash is elsewhere
```

---

## Future Additions

**As issues arise, document them here with:**
1. Problem description
2. Platform affected
3. Solution/workaround
4. Related commands or configuration

---

## Related Documentation

- **stack-preferences.md** - Development tools and preferences
- **cli-first-guide.md** - CLI tool best practices and implementation
- **testing-guide.md** - Cross-platform testing considerations

---

**Key Takeaways:**
1. This system is currently on Linux
2. Document platform-specific issues as they arise
3. Prefer cross-platform solutions when possible
4. Use path modules and portable shebangs
5. Test on target platforms before deploying
