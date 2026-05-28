## Manual Checks

**Impact:** HIGH

Use `nix eval` and `nix build --dry-run` to validate logic before pushing. This catches option type errors and evaluation failures that linters miss.

**Incorrect:**

**Blind Push**
Pushing changes without checking if the module actually evaluates.

**Correct:**

**Dry Run**

```bash
# Check if it builds (without actually building)
nix build .#nixosConfigurations.host.config.system.build.toplevel --dry-run

# Check syntax fast
nix-instantiate --parse file.nix > /dev/null
```
