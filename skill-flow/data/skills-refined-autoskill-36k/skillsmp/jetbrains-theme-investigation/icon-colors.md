# Icon Color System

## Key Source Files

```text
platform/util/ui/src/com/intellij/ui/icons/stroke.kt       # toStrokeIcon function
platform/icons/src/expui/actions/                          # New UI action icons
platform/icons/src/actions/                                # Classic action icons
```

## ColorPalette in Theme JSON

Remap icon colors globally via `icons.ColorPalette`:

```json
"icons": {
  "ColorPalette": {
    "#3592C4": "#19181a",
    "Actions.Grey": "#19181a"
  }
}
```

## Named Color Keys (Targeted)

From HighContrast.theme.json:

**Actions (toolbar icons):**

- `Actions.Grey`, `Actions.Red`, `Actions.Yellow`, `Actions.Green`, `Actions.Blue`
- `Actions.GreyInline`, `Actions.GreyInline.Dark`

**Objects (list/tree icons):**

- `Objects.Grey`, `Objects.Red`, `Objects.Blue`, `Objects.Purple`, etc.
- `Objects.BlackText`, `Objects.YellowDark`, `Objects.GreenAndroid`

**Checkboxes:**

**IMPORTANT:** For new UI themes (Islands, expUI), use base keys WITHOUT `.Dark` suffix:

- `Checkbox.Foreground.Selected` - checkmark color (NOT `.Dark` for Islands/expUI)
- `Checkbox.Background.Selected` - background when selected
- `Checkbox.Border.Selected` - border when selected
- `Checkbox.Focus.Wide` - focus ring color

Old-style dark themes used `.Dark` suffix, but this is deprecated for Islands/expUI themes.
Build warnings will indicate: "Checkbox.Foreground.Selected.Dark is deprecated for new UI themes"

## Standard Stroke Colors (from stroke.kt)

These hex colors can be remapped in ColorPalette:

```text
#818594, #6c707e, #3574f0, #5fb865, #e35252,
#eb7171, #e3ae4d, #fcc75b, #f28c35, #955ae0,
#a8adbd, #ced0d6
```

## How Icon Recoloring Works

1. SVG icons have hardcoded colors (e.g., `#CED0D6`)
2. `ColorPalette` in theme JSON remaps globally
3. Named keys (e.g., `Actions.Grey`) are more targeted but require icon support
4. `toStrokeIcon(icon, color)` recolors programmatically at runtime (code must call it)

## Button Icon Issue

Button icons don't auto-recolor. The `toStrokeIcon` function must be called explicitly:

```kotlin
icon = toStrokeIcon(icon, JBUI.CurrentTheme.Button.defaultButtonForeground())
```

Dialog buttons don't use this - icons display with original colors. Fix via ColorPalette hex mapping.

## SVG Icon Structure

SVG icons use `id` attributes that map to ColorPalette keys:

```xml
<!-- Example: checkBoxSelected.svg -->
<svg>
  <rect id="Checkbox.Background.Selected_Checkbox.Border.Selected"
        fill="#3574F0" stroke="#3574F0"/>
  <path id="Checkbox.Foreground.Selected"
        stroke="white" stroke-width="2"/>
</svg>
```

The `id` attribute determines which ColorPalette key controls the color. Default colors in SVG
(e.g., `stroke="white"`) get replaced by ColorPalette values when defined in theme JSON.

## Finding Icon Colors

```bash
# Find what color an icon uses
cat ../../JetBrains/intellij-community/platform/icons/src/expui/actions/checked_dark.svg | grep -o 'stroke="[^"]*"\|fill="[^"]*"'

# View checkbox icon structure
cat ../../JetBrains/intellij-community/platform/platform-resources/src/themes/expUI/icons/dark/checkBoxSelected.svg

# Find all icons using a specific color
find ../../JetBrains/intellij-community/platform/icons -name "*.svg" | xargs grep -l "#CED0D6"
```

## Debugging Icon Color Issues

1. **Check the SVG source** - view the icon file to see what `id` attributes and default colors it uses
2. **Look at build warnings** - `buildSearchableOptions` task shows deprecated ColorPalette keys
3. **Test in reference themes** - check HighContrast or expUI themes for working examples
4. **Verify key names** - Islands/expUI use base keys (no `.Dark` suffix), older themes use `.Dark`

## Common Issue: Checkmark on Colored Button Backgrounds

**Problem:** Checkmark icon on default button (light/colored background) has poor contrast.

**Cause:** Checkbox icons default to white checkmark, designed for dark backgrounds. When button
has light/colored background (e.g., cyan `#78dce8`), white checkmark is barely visible.

**Solution:** Set `Checkbox.Foreground.Selected` to a dark color in ColorPalette:

```python
# In generate-themes.py
theme["icons"] = {
    "ColorPalette": {
        # Dark checkmark for contrast on light colored buttons
        "Checkbox.Foreground.Selected": palette["dark1"],  # e.g., #19181a
        "Checkbox.Background.Selected": palette["accent5"],  # Match button background
        "Checkbox.Border.Selected": palette["accent5"],
    }
}
```

**Testing:** Look for dialogs with Apply/OK buttons, Settings changes requiring confirmation, etc.
