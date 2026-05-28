## optionals - Conditional List Items

**Impact:** HIGH

Use `lib.optionals` (plural) to conditionally include a list of items. It returns an empty list `[]` if the condition is false, making it safe to concatenate `++`.

**Incorrect:**

**Ternary for lists**
`pkgs = [ item1 ] ++ (if cond then [ item2 ] else []);` is verbose.

**Correct:**

**optionals**

```nix
home.packages = [ pkgs.coreutils ]
  ++ lib.optionals cfg.enableTools [ pkgs.ripgrep pkgs.fd ];
```
