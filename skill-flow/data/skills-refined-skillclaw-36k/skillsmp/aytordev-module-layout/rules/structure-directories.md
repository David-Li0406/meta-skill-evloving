## Directory Structure

**Impact:** CRITICAL

Adhere strictly to the top-level directory structure to ensure cross-platform compatibility and correct module loading.

**Incorrect:**

**Mixed Platforms**
Putting macOS modules in `modules/nixos/` or system services in `modules/home/`.

**Correct:**

**Strict Isolation**

- `modules/nixos/`: NixOS system-level (Linux only)
- `modules/darwin/`: macOS system-level (nix-darwin)
- `modules/home/`: Home Manager user-space (cross-platform)
- `modules/common/`: Shared functionality (imported by others)
