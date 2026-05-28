## Submodule Pattern

**Impact:** HIGH

Use `types.submodule` for complex nested configurations (like creating a list of accounts or services with their own options).

**Incorrect:**

**Attrs of attrs**
`type = types.attrsOf types.attrs;` allows invalid configuration structure.

**Correct:**

**Submodule**

```nix
users = lib.mkOption {
  type = lib.types.attrsOf (lib.types.submodule {
    options = {
      uid = lib.mkOption { type = lib.types.int; };
      shell = lib.mkOption { type = lib.types.path; };
    };
  });
};
```
