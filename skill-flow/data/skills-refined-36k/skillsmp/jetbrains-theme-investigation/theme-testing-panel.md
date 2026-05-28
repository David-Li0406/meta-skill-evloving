# Theme Testing Panel

## Overview

Dev-mode-only UI panel for visually testing theme changes in real-time. Displays various JetBrains Platform UI components to verify theme rendering, particularly useful for testing color changes, contrast fixes, and visual consistency.

## Location

Settings → Appearance & Behavior → Appearance → **Theme Testing** (dev mode only)

**Dev Mode Detection**: Panel only appears when `idea.is.internal=true` (automatically set when running via `./gradlew runIde -PdevMode`)

## UI Components

The testing panel displays the following categories:

### Buttons

**Interactive Icon Grid** - Dynamic grid of icon buttons with real-time column resizing:

- **Icon Selection**: Click any icon button to preview it on Normal, Disabled, and Default (cyan) buttons
- **Text Input**: Modify button text via text field to test different label lengths
- **Dynamic Grid**: Automatically adjusts column count when panel resizes
  - Width detection: Calculates optimal columns based on available width
  - Preserves selection: Selected icon remains highlighted during grid rebuild
  - Info label: Displays current width, usable width, and column count
- **Preview Buttons**:
  - **Normal Button** - Standard button state with selected icon
  - **Disabled Button** - Inactive state with selected icon
  - **Default Button** - Cyan accent button with checkmark and selected icon (tests checkmark contrast)

### Input Elements

- **Text Field** - JBTextField with sample text
- **Combo Box** - Dropdown with multiple options
- **Checkboxes** - Enabled and disabled states

### Selection Elements

- **Radio Buttons** - Button group with selected state
- **Slider** - Range selector for testing accent colors

### Lists & Trees

- **List** - JBList with selection state
- **Tree** - Tree component with expanded/collapsed nodes

### Borders & Separators

- **Titled Border** - Panel with titled border
- **Separator** - Horizontal separator line

### Status Indicators

- **Info/Warning/Error Messages** - Labels with emoji indicators
- **Progress Bar** - Progress indicator at 65%

## Adding Test Elements

### Step 1: Locate the Category

Edit `src/main/kotlin/com/github/smykla/monokaiislands/settings/ThemeTestingComponent.kt`

The panel uses **Kotlin UI DSL V2** with the following groups:

- `group("Buttons")` - Icon grid with preview buttons
- `group("Input Elements")` - Text fields, combo boxes, checkboxes
- `group("Selection Elements")` - Radio buttons, sliders
- `group("Lists & Trees")` - Lists and trees
- `group("Borders & Separators")` - Borders and separators
- `group("Status Indicators")` - Status messages and progress bars

### Step 2: Add Component to Category

Example - Adding a new test element:

```kotlin
val panel = panel {
    // ... existing groups ...

    separator()

    group("Input Elements") {
        row("Text Field:") {
            textField()
                .text("Sample text")
        }
        row("Combo Box:") {
            comboBox(listOf("Option 1", "Option 2", "Option 3"))
        }
        row {
            checkBox("Enabled Checkbox")
                .selected(true)
            checkBox("Disabled Checkbox")
                .selected(false)
                .enabled(false)
        }
        // NEW: Add password field
        row("Password:") {
            textField()
                .text("password")
        }
    }
}
```

### Step 3: Test in Sandbox

```bash
./gradlew runIde -PdevMode
```

Wait for IDE to open, then:

1. Navigate to Settings → Appearance & Behavior → Appearance → Theme Testing
2. Verify new component appears
3. Test visual appearance with current theme

## Common Test Scenarios

### Testing Button Contrast (Checkmark Issue Example)

**Problem**: Cyan button checkmark has poor contrast

**Test Workflow**:

1. Open Settings → Appearance → Theme Testing
2. Locate "Default Button" (cyan accent with checkmark)
3. Edit `palettes/monokai-dark.json` to change `accent5` color
4. Manually regenerate the theme by running `python3 scripts/generate-themes.py && ./gradlew buildPlugin -PdevMode`
5. Restart IDE (Cmd+Q, then re-run `./gradlew runIde -PdevMode`)
6. Verify checkmark contrast in testing panel

### Testing Selection Colors

**Components**: Tree selection, List selection

**Properties to Test**:

- `Tree.selectionBackground` - Tree node selection background
- `List.selectionBackground` - List item selection background
- Focus indicators on selected items

**Workflow**:

1. Modify selection colors in `scripts/generate-themes.py`
2. Run `python3 scripts/generate-themes.py`
3. Rebuild with `./gradlew buildPlugin`
4. Restart IDE
5. Check "Lists & Trees" section in testing panel

### Testing Focus States

**Components**: Buttons, text fields, combo boxes

**Properties to Test**:

- `Button.default.focusedBorderColor`
- `Component.focusedBorderColor`
- Focus ring visibility and color

**Workflow**:

1. Tab through components in testing panel
2. Verify focus indicators are visible
3. Check contrast against component backgrounds

## Dev Mode Detection

**Runtime Detection**: `ApplicationManager.getApplication().isInternal`

**When `true`** (dev mode):

- Running via `./gradlew runIde -PdevMode`
- `idea.is.internal=true` set in sandbox config (see `idea.properties` or build script)

**When `false`** (production):

- Plugin installed in real IDE
- Production build from Marketplace
- `ThemeTestingConfigurableProvider` returns `null` (panel hidden)

## Architecture

**Files**:

- `DevModeDetector.kt` - Runtime dev mode detection utility
- `ThemeTestingComponent.kt` - UI component with test elements
- `MonokaiIslandsConfigurable.kt` - Integrates the theme testing panel directly into the existing configurable
- `plugin.xml` - Registers the configurable as usual

**Pattern**: Direct integration with runtime dev mode check

- The theme testing panel is part of the main configurable UI
- `DevModeDetector.isDevMode()` is used to conditionally show the testing panel only in dev mode
- In production, the panel is not shown and has zero overhead

### Dynamic Icon Grid Implementation

**File**: `InteractiveIconPanel.kt`

**Mechanism**: Uses `WrapLayout` custom layout manager for automatic grid wrapping without manual resize handling.

**Architecture**:

1. **WrapLayout** (`ui/components/WrapLayout.kt`):
   - Extends `FlowLayout` with preferred size calculation that accounts for wrapped rows
   - Overrides `preferredLayoutSize()` to simulate layout and calculate actual wrapped dimensions
   - Handles wrapping automatically based on available container width
   - No ComponentListener needed - layout manager recalculates on every layout pass

2. **Grid Panel Structure**:
   - Single `JPanel(WrapLayout(FlowLayout.LEFT, 5, 5))`
   - No manual grid rebuilding or resize detection
   - Icon buttons added once during initialization
   - Layout manager handles all wrapping automatically

3. **Selection State Management**:
   - `allButtons` - Mutable list of all icon buttons
   - Selection tracked via border style (cyan rounded border for selected button)
   - Button click handlers update borders directly (reset all, set selected)
   - No index tracking needed - selection state lives on button components

4. **Button Configuration**:
   - Fixed button size: `JBUI.size(40, 40)` (preferred, minimum, and maximum)
   - Layout gaps: horizontal 5px, vertical 5px
   - "None" button (no icon) + all icon buttons in single flat list
   - Selection border: custom `AbstractBorder` with rounded rectangle and cyan color

**Why WrapLayout vs JetBrains APIs**:

- **Kotlin UI DSL V2** (`com.intellij.ui.dsl.builder`): Form-oriented, row/cell paradigm doesn't fit icon grid pattern
- **ActionToolbar** with `WRAP_LAYOUT_POLICY`: Experimental, designed for toolbars not button grids, requires converting icons to Actions
- **WrapLayout**: Simple, proven Swing pattern (based on 2008 WrapLayout), solves exact problem (FlowLayout's preferred size doesn't account for wrapping)

**Performance**:

- Layout calculation happens only during layout passes (triggered by resize, revalidate)
- No manual grid rebuilds, no ComponentListener overhead
- Swing's native layout system handles all wrapping efficiently
- ~60% code reduction vs previous ComponentListener + GridLayout approach

## Extending the Panel

### Adding a New Category

The panel uses **Kotlin UI DSL V2** (`com.intellij.ui.dsl.builder`) for layout structure.

1. For simple DSL components, add directly to the panel builder:

   ```kotlin
   val panel = panel {
       // ... existing groups ...

       separator()

       group("New Category") {
           row("Label:") {
               textField()
                   .text("Sample text")
           }
           row {
               checkBox("Option 1")
               checkBox("Option 2")
           }
       }
   }
   ```

2. For complex custom components (like icon grid), create a factory method and embed via `cell()`:

   ```kotlin
   private fun createCustomComponent(): JPanel {
       return JPanel().apply {
           layout = BoxLayout(this, BoxLayout.Y_AXIS)
           border = JBUI.Borders.empty(5)
           // Add components here
       }
   }

   // In panel builder:
   group("Custom Category") {
       row {
           cell(createCustomComponent())
               .align(AlignX.FILL)
       }
   }
   ```

3. Test in sandbox IDE

### Useful JetBrains Platform Components

- `JButton` - Standard button (use `JButton.isDefaultButton` for accent style)
- `JBCheckBox` - Checkbox with JetBrains styling
- `JBTextField` - Text input field
- `JBList` - List component
- `Tree` - Tree component with expansion
- `JBLabel` - Label (supports HTML)
- `JProgressBar` - Progress indicator
- `JSeparator` - Horizontal/vertical separator
- `ComboBox` - Dropdown selector
- `JRadioButton` - Radio button (use `ButtonGroup` for mutual exclusion)
- `JSlider` - Range slider

**Layout Helpers**:

- `panel { }` - Kotlin UI DSL V2 panel builder (modern standard, mandatory since 2025.1)
- `group("Title") { }` - Group with title separator
- `row("Label:") { }` - Row with optional label
- `cell(component)` - Embed custom Swing component
- `separator()` - Horizontal separator
- `JBUI.Panels.simplePanel()` - Simple panel with border layout (for custom components)
- `BoxLayout` - Vertical or horizontal box layout (for custom components)
- `FlowLayout` - Left-to-right flow layout (for custom components)
- `WrapLayout` - Flow layout with automatic wrapping (custom utility)

## Troubleshooting

### Panel Not Appearing in Dev Mode

**Check**:

1. `idea.is.internal` property set in build.gradle.kts:

   ```kotlin
   systemProperty("idea.is.internal", "true")
   ```

2. Running via `./gradlew runIde` (not a production build)
3. Check IDE logs for provider errors

### Panel Appearing in Production Build

**Issue**: `DevModeDetector.isDevMode()` returning `true` in production

**Fix**: Ensure production build doesn't set `idea.is.internal=true` in JVM args

### Theme Changes Not Reflected

**Issue**: Modified theme not visible after palette edit

**Workflow**:

1. Edit `palettes/monokai-dark.json`
2. Run `python3 scripts/generate-themes.py && ./gradlew buildPlugin -PdevMode` to regenerate theme
3. **Restart IDE** (theme resources cached, hot reload doesn't work)
4. Verify changes in testing panel

## References

- [SearchableConfigurable](https://plugins.jetbrains.com/docs/intellij/settings.html) - IntelliJ Platform settings API
- [ConfigurableProvider](https://plugins.jetbrains.com/docs/intellij/settings.html#configurableprovider) - Conditional registration pattern
- [IntelliJ Platform UI Components](https://plugins.jetbrains.com/docs/intellij/user-interface-components.html) - Component library
- [JBUI Utilities](https://github.com/JetBrains/intellij-community/blob/master/platform/util/ui/src/com/intellij/util/ui/JBUI.java) - Spacing and sizing helpers
