## Option Helpers

**Impact:** HIGH

Use `lib.aytordev` helpers to reduce boilerplate. `mkOpt` simplifies type/default/description, and `enabled`/`disabled` sets the enable flag.

**Incorrect:**

**Verbose Options**
Manually writing `mkOption { type = ...; default = ...; description = ...; }` for simple values.

**Correct:**

**Concise Helpers**

```nix
inherit (lib.aytordev) mkOpt enabled;

# Quick enable
programs.git = enabled;

# Custom option
userName = mkOpt types.str "default" "User name";
```
