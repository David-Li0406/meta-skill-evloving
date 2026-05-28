## mkIf - Conditional Config Blocks

**Impact:** CRITICAL

Use `lib.mkIf` for conditional configuration blocks. It pushes the condition down to the leaves of the configuration, allowing accurate merging. Avoid Python-style `if condition then { ... } else { ... }` for top-level config blocks, as it breaks module merging.

**Incorrect:**

**Top-level if-else**
Wraps the entire config set in a conditional, preventing other modules from merging into it unless the condition matches perfectly for everyone.

**Correct:**

**mkIf**
Use `lib.mkIf` to guard the configuration.

```nix
config = lib.mkIf cfg.enable {
  programs.git.enable = true;
};
```
