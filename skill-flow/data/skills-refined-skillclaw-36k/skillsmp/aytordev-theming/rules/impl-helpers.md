## Library Helpers

**Impact:** MEDIUM

Use `config.aytordev.theme.lib` for common transformations, such as converting hex colors to Sketchybar format (`0xff...`) or extracting subsets of the palette.

**Incorrect:**

**Regex Magic**
Manually replacing `#` with `0xff` using string manipulation functions in every module.

**Correct:**

**Standard Functions**
Use the provided helpers for consistency.

```nix
let
  themeLib = config.aytordev.theme.lib;
  accent = config.aytordev.theme.palette.accent.hex;
in
{
  # Correctly formats as 0xffRRGGBB
  color = themeLib.hexToSketchybar accent;
}
```
