## Using the Palette

**Impact:** HIGH

The palette is exposed at `config.aytordev.theme.palette`. It provides semantic colors relative to the active variant (Wave/Dragon/Lotus) and polarity (Dark/Light). Do not switch on variants inside modules; rely on the palette to provide the correct color for the current state.

**Incorrect:**

**Manual Variant Switching**
Using `if variant == "lotus"` inside a module configuration to select colors.

**Correct:**

**Semantic Access**
Trust `theme.palette` to provide the correct color.

```nix
# BAD
color = if config.aytordev.theme.variant == "lotus" then "#..." else "#...";

# GOOD
color = config.aytordev.theme.palette.bg.main.hex;
```
