## mkMerge - Combine Conditionals

**Impact:** HIGH

Use `lib.mkMerge` to combine multiple conditional blocks into a single definition. This is clearer than repeating `config = ...` multiple times or nesting if-else structures deeply.

**Incorrect:**

**Nested spaghetti**
Deeply nested `mkIf` calls or split config definitions that are hard to read.

**Correct:**

**Clean Merge**

```nix
config = lib.mkMerge [
  # Always applied
  { programs.bash.enable = true; }

  # Conditional A
  (lib.mkIf cfg.enableGit { programs.git.enable = true; })

  # Conditional B
  (lib.mkIf cfg.enableVim { programs.vim.enable = true; })
];
```
