## optionalString - Conditional Strings

**Impact:** MEDIUM

Use `lib.optionalString` to generate a string only if a condition is true. Returns `""` otherwise. Ideal for shell scripts or config files.

**Incorrect:**

**If-then-else null**
`str = if cond then "text" else null;` usually throws a type error because you can't concatenate null strings.

**Correct:**

**optionalString**

```nix
shellInit = ''
  export EDITOR=vim
'' + lib.optionalString cfg.enableAliases ''
  alias ll='ls -la'
'';
```
