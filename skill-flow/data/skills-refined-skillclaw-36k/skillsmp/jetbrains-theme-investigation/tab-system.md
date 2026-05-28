# Tab System

## Key Source Files

```text
platform/platform-api/src/com/intellij/ui/tabs/
├── JBTabsBorder.kt              # Border/thickness
├── JBTabPainter.kt              # Tab painting
├── impl/
│   ├── JBTabsImpl.kt            # Main implementation (tabHGap defined here!)
│   ├── JBEditorTabs.kt          # Editor-specific tabs
│   ├── TabLabel.kt              # Individual tab labels
│   ├── singleRow/
│   │   ├── SingleRowLayout.java       # Layout algorithm
│   │   └── SingleRowLayoutStrategy.java # H/V strategies
│   └── themes/
│       └── TabTheme.kt          # Theme colors
```

## Themeable Properties

| Property                               | Description                 | Format                  |
|----------------------------------------|-----------------------------|-------------------------|
| `EditorTabs.tabInsets`                 | Horizontal tab padding      | "top,right,bottom,left" |
| `EditorTabs.tabInsets.compact`         | Compact mode padding        | "top,right,bottom,left" |
| `EditorTabs.verticalTabInsets`         | Vertical tab padding        | "top,right,bottom,left" |
| `EditorTabs.verticalTabInsets.compact` | Vertical compact padding    | "top,right,bottom,left" |
| `EditorTabs.underlineHeight`           | Active tab underline height | integer                 |
| `EditorTabs.underlineArc`              | Underline corner radius     | integer                 |
| `EditorTabs.background`                | Tab bar background          | color                   |
| `EditorTabs.underlineColor`            | Active tab underline color  | color                   |

**Insets format**: `"top,right,bottom,left"` (CSS order)

- Negative values = tabs extend beyond bounds (taller/wider)
- Positive values = padding inside tabs

## NOT Themeable (Hardcoded)

### Gap Between Tabs

```kotlin
// JBTabsImpl.kt:3284-3285
val tabHGap: Int
  get() = -tabBorder.thickness
```

The gap is calculated as negative border thickness. Same `tabHGap` used for both horizontal AND vertical tabs.

### Border Thickness

```kotlin
// JBTabsBorder.kt:13-14
val thickness: Int
  get() = tabs.tabPainter.getTabTheme().topBorderThickness

// TabTheme.kt:14
topBorderThickness = JBUI.scale(1)  // Hardcoded!
```

## Key Insight

`verticalTabInsets` controls padding **INSIDE** each tab, NOT the gap **BETWEEN** tabs.

To reduce vertical spacing between stacked tabs:

- **Cannot be done via theme JSON**
- Gap is hardcoded as `-topBorderThickness`
- Requires source code modification

## Search Commands

```bash
# Find tab gap implementation
grep -rn "tabHGap\|tabVGap" $INTELLIJ_COMMUNITY/platform/platform-api/src/com/intellij/ui/tabs --include="*.kt"

# Find thickness definition
grep -rn "topBorderThickness" $INTELLIJ_COMMUNITY/platform/platform-api/src/com/intellij/ui/tabs --include="*.kt"

# Find all tab-related theme properties
grep -i '"EditorTabs\.' $INTELLIJ_COMMUNITY/platform/platform-resources/src/themes/metadata/*.json
```
