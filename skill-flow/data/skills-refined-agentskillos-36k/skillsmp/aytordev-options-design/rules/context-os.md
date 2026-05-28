## osConfig Access

**Impact:** MEDIUM

When a Home Manager module needs to read the system configuration (NixOS/Darwin), use `osConfig`. Always guard access with `or` to prevent eval errors in standalone Home Manager usage.

**Incorrect:**

**Unsafe Access**
Creating a dependency on `osConfig` without a fallback, crashing the build if `osConfig` is missing.

**Correct:**

**Guarded Access**

```nix
{ osConfig ? {}, ... }:

# Safely check if system-level sops is enabled
mkIf (osConfig.aytordev.security.sops.enable or false) {
  # ...
}
```
