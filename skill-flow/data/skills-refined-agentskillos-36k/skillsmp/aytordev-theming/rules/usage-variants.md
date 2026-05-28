## App Themes & Variants

**Impact:** HIGH

For applications that need a named theme (e.g., "Kanagawa Wave" vs "kanagawa-wave"), use the convenience accessors in `config.aytordev.theme.appTheme`. This avoids string formatting errors.

**Incorrect:**

**String Interpolation**
Manually constructing theme names like `"Kanagawa ${config.aytordev.theme.variant}"`.

**Correct:**

**Standardized Names**
Use the pre-calculated formats provided by the module.

```nix
# Returns "Kanagawa Wave" or "Kanagawa Lotus"
theme = config.aytordev.theme.appTheme.capitalized;

# Returns "kanagawa-wave" or "kanagawa-lotus"
theme = config.aytordev.theme.appTheme.kebab;
```
