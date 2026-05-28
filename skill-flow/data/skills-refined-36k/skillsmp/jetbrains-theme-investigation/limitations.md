# Known Limitations (NOT Themeable)

Properties that cannot be changed via theme JSON - require source code modification.

## Tab System

| What                        | Why                                 | Source               |
|-----------------------------|-------------------------------------|----------------------|
| Gap between vertical tabs   | Hardcoded as `-tabBorder.thickness` | `JBTabsImpl.kt:3284` |
| Gap between horizontal tabs | Same as vertical - uses `tabHGap`   | `JBTabsImpl.kt:3284` |
| Border thickness            | `JBUI.scale(1)` hardcoded           | `TabTheme.kt:14`     |

**Workaround**: None. File feature request on [YouTrack](https://youtrack.jetbrains.com/issue/IJPL-174976).

## Icon Colors on Buttons

| What                      | Why                                    | Source      |
|---------------------------|----------------------------------------|-------------|
| Default button icon color | Requires `toStrokeIcon()` call in code | `stroke.kt` |

**Workaround**: Use `icons.ColorPalette` to remap the specific hex color globally. This affects ALL icons using that color.

## Useful Links

- [YouTrack: Tab Height Request](https://youtrack.jetbrains.com/issue/IJPL-174976)
- [Material Theme UI Plugin](https://plugins.jetbrains.com/plugin/8006-material-theme-ui) - has more customization options

## How to Check if Themeable

1. Search theme metadata:

   ```bash
   grep -i "property" $INTELLIJ_COMMUNITY/platform/platform-resources/src/themes/metadata/*.json
   ```

2. If not in metadata, search JBUI.java for `namedColor`:

   ```bash
   grep "namedColor.*Property" $INTELLIJ_COMMUNITY/platform/util/ui/src/com/intellij/util/ui/JBUI.java
   ```

3. If not found, search source for hardcoded values:

   ```bash
   grep -rn "PropertyName\|scale(" $INTELLIJ_COMMUNITY/platform/platform-*/src --include="*.kt"
   ```

If value is computed or hardcoded in source → **NOT themeable**
