## Polarity Logic

**Impact:** MEDIUM

When you explicitly need to know if the theme is light or dark (e.g. for boolean flags), use `config.aytordev.theme.isLight`. This handles edge cases (like "lotus" variant implying light mode even if polarity wasn't explicitly set).

**Incorrect:**

**Fragile Checks**
Checking `config.aytordev.theme.polarity == "light"` directly, which misses the case where variant="lotus" forces light mode.

**Correct:**

**Computed Boolean**
Use the robust computed value.

```nix
programs.bat.config = {
  # Some apps need a boolean flag for light mode
  "--light" = lib.mkIf config.aytordev.theme.isLight;
};
```
