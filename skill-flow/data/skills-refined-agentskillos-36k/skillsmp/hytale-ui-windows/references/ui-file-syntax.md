# Hytale UI File (.ui) Syntax Reference

Complete reference for creating custom UI files in Hytale. UI files define the visual layout and styling of windows, pages, and HUD elements.

## File Structure Overview

UI files use a declarative, hierarchical syntax similar to CSS/JSON hybrid. The structure consists of:
- **Variable definitions** (`@` prefix)
- **File imports** (`$` prefix)
- **Element definitions** (widget types with properties)
- **Nested children** (elements within `{}` blocks)

```
// Comment (single line)
$Import = "path/to/other.ui";  // Import another UI file

@VariableName = value;          // Define reusable variable

WidgetType {                    // Root element
  Property: value;              // Element property
  
  ChildWidget {                 // Nested child element
    Property: value;
  }
}
```

## Imports and References

### File Imports
Import other UI files to reuse their variables and templates:

```
$C = "../Common.ui";           // Import Common.ui, reference as $C
$Sounds = "../../Sounds.ui";   // Import Sounds.ui, reference as $Sounds
```

### Using Imported Variables
Reference imported variables with `$Alias.@VariableName`:

```
$C = "../Common.ui";

Group {
  Style: $C.@DefaultLabelStyle;     // Use variable from Common.ui
  Background: $C.@InputBoxBackground;
  ScrollbarStyle: $C.@DefaultScrollbarStyle;
}
```

### Using Imported Templates
Instantiate imported templates (parameterized elements):

```
$C = "../Common.ui";

$C.@Container {                    // Instantiate @Container template from Common.ui
  Anchor: (Width: 600, Height: 400);
  
  #Title {                         // Override named slot #Title
    Label { Text: "My Window"; }
  }
  
  #Content {                       // Override named slot #Content
    // Custom content here
  }
}
```

## Variable Definitions

### Simple Variables
```
@FontSize = 15;                    // Number
@DisabledColor = #797b7c;          // Color
@ButtonBorder = 12;                // Number
@DefaultButtonHeight = 44;         // Number
```

### Style Variables
```
@TitleStyle = LabelStyle(
  FontSize: 15,
  VerticalAlignment: Center,
  RenderUppercase: true,
  TextColor: #b4c8c9,
  FontName: "Secondary",
  RenderBold: true,
  LetterSpacing: 0.5
);
```

### Template Variables (Parameterized Elements)
Templates allow reusable elements with customizable parameters:

```
@TextButton = TextButton {
  @Anchor = Anchor();              // Parameter with default value
  @Sounds = ();                    // Empty tuple default
  @Text = "";                      // String parameter
  
  Style: (
    ...@DefaultTextButtonStyle,    // Spread existing style
    Sounds: (
      ...$Sounds.@ButtonsLight,    // Spread imported sounds
      ...@Sounds                   // Spread parameter
    )
  );
  Anchor: (...@Anchor, Height: @DefaultButtonHeight);
  Padding: (Horizontal: @DefaultButtonPadding);
  Text: @Text;
};
```

### Using Template Parameters
```
$C.@TextButton #SubmitButton {
  @Anchor = (Width: 200);          // Override parameter
  @Text = %ui.buttons.submit;      // Override parameter
}
```

## Colors

### Hex Colors
```
Background: #ffffff;               // RGB (white)
Background: #000000;               // RGB (black)
Background: #96a9be;               // RGB (custom)
TextColor: #ffffff(0.8);           // RGBA with alpha (0.0-1.0)
Background: #000000(0.45);         // Semi-transparent black
```

## Anchor System

Anchors define element positioning and sizing:

### Basic Positioning
```
Anchor: (Width: 200, Height: 100);           // Fixed size
Anchor: (Top: 10, Left: 20);                 // Position from edges
Anchor: (Right: 0, Bottom: 0);               // Position from opposite edges
Anchor: (Full: 0);                           // Fill parent (all edges at 0)
```

### Combined Anchors
```
Anchor: (Width: 600, Height: 700);           // Fixed size, centered
Anchor: (Top: 20, Left: 50, Right: 50);      // Horizontal stretch with margins
Anchor: (Height: 38, Horizontal: 10);        // Fixed height, horizontal padding
Anchor: (Vertical: 16);                      // Vertical padding only
```

### Anchor Properties
| Property | Description |
|----------|-------------|
| `Width` | Fixed width in pixels |
| `Height` | Fixed height in pixels |
| `Top` | Distance from top edge |
| `Bottom` | Distance from bottom edge |
| `Left` | Distance from left edge |
| `Right` | Distance from right edge |
| `Full` | Distance from all edges (shorthand) |
| `Horizontal` | Distance from left and right edges |
| `Vertical` | Distance from top and bottom edges |

## Layout Modes

LayoutMode controls how children are arranged:

```
LayoutMode: Top;              // Stack children from top to bottom
LayoutMode: Left;             // Stack children from left to right
LayoutMode: Right;            // Stack children from right to left
LayoutMode: Middle;           // Center single child
LayoutMode: Center;           // Center children horizontally
LayoutMode: CenterMiddle;     // Center children both horizontally and vertically
LayoutMode: TopScrolling;     // Vertical scrollable list
LayoutMode: LeftCenterWrap;   // Wrap from left, center vertically
```

### Examples

#### Vertical Stack (Top)
```
Group {
  LayoutMode: Top;
  
  Label { Text: "First"; }
  Label { Text: "Second"; }
  Label { Text: "Third"; }
}
```

#### Horizontal Stack (Left)
```
Group {
  LayoutMode: Left;
  
  Button { Text: "A"; }
  Button { Text: "B"; }
  Button { Text: "C"; }
}
```

#### Scrollable List
```
Group {
  LayoutMode: TopScrolling;
  ScrollbarStyle: $C.@DefaultScrollbarStyle;
  
  Group #ItemList {
    LayoutMode: Top;
    // Dynamic children added here
  }
}
```

#### Grid with Wrapping
```
Group #TradeGrid {
  LayoutMode: LeftCenterWrap;
  // Cards wrap to next row when space runs out
}
```

## Flex Layout

FlexWeight distributes remaining space among siblings:

```
Group {
  LayoutMode: Left;
  
  Group { Anchor: (Width: 100); }  // Fixed 100px
  Group { FlexWeight: 1; }          // Takes 1/3 of remaining space
  Group { FlexWeight: 2; }          // Takes 2/3 of remaining space
}
```

### Spacer Pattern
```
Group {
  LayoutMode: Left;
  
  Label { Text: "Left"; }
  Group { FlexWeight: 1; }          // Flexible spacer
  Label { Text: "Right"; }
}
```

## Padding

```
Padding: (Full: 16);                           // All sides
Padding: (Horizontal: 10, Vertical: 5);        // Left/right and top/bottom
Padding: (Top: 10, Bottom: 20, Left: 5, Right: 5);
Padding: (Left: 20, Right: 5, Vertical: 16);   // Mixed
```

## Backgrounds

### Solid Color
```
Background: #000000(0.45);
Background: (Color: #2b3542);
```

### Simple Image
```
Background: "Common/Tab.png";
Background: (TexturePath: "FrameTop.png");
```

### 9-Slice (Patch) Image
```
Background: (TexturePath: "Common/ContainerPatch.png", Border: 23);
Background: (TexturePath: "Common/Buttons/Primary.png", VerticalBorder: 12, HorizontalBorder: 80);
```

### PatchStyle Function
```
@DefaultButtonDefaultBackground = PatchStyle(
  TexturePath: "Common/Buttons/Primary.png",
  VerticalBorder: @ButtonBorder,
  HorizontalBorder: 80
);
```

## Widget Types

### Group
Container element for organizing children:
```
Group {
  Anchor: (Width: 200, Height: 100);
  LayoutMode: Top;
  Padding: (Full: 10);
  Background: #000000(0.5);
  
  // Children here
}
```

### Label
Text display element:
```
Label {
  Text: "Hello World";
  Style: (FontSize: 16, TextColor: #ffffff);
}

Label #DynamicLabel {
  Text: "";                        // Set dynamically
  Style: LabelStyle(
    FontSize: 15,
    VerticalAlignment: Center,
    HorizontalAlignment: Center,
    RenderUppercase: true,
    RenderBold: true,
    Wrap: true
  );
}
```

### Button
Clickable button without text:
```
Button #CloseButton {
  Anchor: (Width: 32, Height: 32);
  Style: (
    Default: (Background: "CloseButton.png"),
    Hovered: (Background: "CloseButtonHovered.png"),
    Pressed: (Background: "CloseButtonPressed.png"),
    Disabled: (Background: "CloseButtonDisabled.png"),
    Sounds: $Sounds.@ButtonsLight
  );
}
```

### TextButton
Button with text label:
```
TextButton #SubmitButton {
  Text: "Submit";
  Anchor: (Width: 150, Height: 44);
  Padding: (Horizontal: 24);
  Style: TextButtonStyle(
    Default: (Background: @ButtonBg, LabelStyle: @ButtonLabel),
    Hovered: (Background: @ButtonHoverBg, LabelStyle: @ButtonLabel),
    Pressed: (Background: @ButtonPressBg, LabelStyle: @ButtonLabel),
    Disabled: (Background: @ButtonDisabledBg, LabelStyle: @DisabledLabel),
    Sounds: $Sounds.@ButtonsLight
  );
}
```

### TextField
Text input field:
```
TextField #NameInput {
  Anchor: (Height: 38);
  Padding: (Horizontal: 10);
  Style: @DefaultInputFieldStyle;
  PlaceholderStyle: @DefaultInputFieldPlaceholderStyle;
  Background: @InputBoxBackground;
  PlaceholderText: %ui.placeholder.enterName;
}
```

### NumberField
Numeric input field:
```
NumberField #AmountInput {
  Anchor: (Width: 60, Height: 38);
  Padding: (Horizontal: 10);
  Value: 5;
  Format: (
    MinValue: 0,
    MaxValue: 100
  );
}
```

### CheckBox
Toggleable checkbox:
```
CheckBox #EnableOption {
  Anchor: (Width: 22, Height: 22);
  Background: (TexturePath: "CheckBoxFrame.png", Border: 7);
  Padding: (Full: 4);
  Value: false;
  Style: CheckBoxStyle(
    Unchecked: (
      DefaultBackground: (Color: #00000000),
      HoveredBackground: (Color: #00000000),
      ChangedSound: (SoundPath: @UntickSound, Volume: 6)
    ),
    Checked: (
      DefaultBackground: (TexturePath: "Checkmark.png"),
      HoveredBackground: (TexturePath: "Checkmark.png"),
      ChangedSound: (SoundPath: @TickSound, Volume: 6)
    )
  );
}
```

### DropdownBox
Dropdown selection:
```
DropdownBox #CategorySelect {
  Anchor: (Width: 330, Height: 32);
  Style: @DefaultDropdownBoxStyle;
}
```

### ColorPicker
Color selection widget:
```
ColorPicker #ColorPicker {
  Anchor: (Width: 310, Height: 290);
  Format: Rgb;
  Style: @DefaultColorPickerStyle;
}
```

### Slider
Value slider:
```
Slider #VolumeSlider {
  Anchor: (Height: 20);
  Style: SliderStyle(
    Background: (TexturePath: "SliderBackground.png", Border: 2),
    Handle: "SliderHandle.png",
    HandleWidth: 16,
    HandleHeight: 16
  );
}
```

### Sprite
Animated sprite:
```
Sprite #LoadingSpinner {
  Anchor: (Width: 32, Height: 32);
  TexturePath: "Common/Spinner.png";
  Frame: (Width: 32, Height: 32, PerRow: 8, Count: 72);
  FramesPerSecond: 30;
}
```

### AssetImage
Dynamic image (set from code):
```
AssetImage #ItemIcon {
  Anchor: (Width: 64, Height: 64);
}
```

### TimerLabel
Countdown timer display:
```
TimerLabel #GameTimer {
  Style: (FontSize: 32, Alignment: Center);
  Seconds: 15 * 60;                // 15 minutes
}
```

### BackButton
Pre-built back navigation button:
```
BackButton {}
```

## Element IDs

Elements can have IDs for programmatic access:

```
Group #MyContainer {               // ID: MyContainer
  Label #TitleLabel {              // ID: TitleLabel
    Text: "Hello";
  }
  
  Group #ContentArea {             // ID: ContentArea
    // Content
  }
}
```

IDs are used in Java code to find and manipulate elements.

## Translation Keys

Use `%` prefix for localized text:

```
Label {
  Text: %server.customUI.shopPage.title;
}

TextButton {
  Text: %client.general.button.back;
}
```

## Style System

### LabelStyle
```
LabelStyle(
  FontSize: 16,
  FontName: "Default",             // or "Secondary"
  TextColor: #ffffff,
  HorizontalAlignment: Center,     // Start, Center, End
  VerticalAlignment: Center,       // Start, Center, End
  RenderUppercase: true,
  RenderBold: true,
  LetterSpacing: 0.5,
  Wrap: true,
  OutlineColor: #000000(0.2)
)
```

### ButtonStyle
```
ButtonStyle(
  Default: (Background: @DefaultBg),
  Hovered: (Background: @HoveredBg),
  Pressed: (Background: @PressedBg),
  Disabled: (Background: @DisabledBg),
  Sounds: @ButtonSounds
)
```

### TextButtonStyle
```
TextButtonStyle(
  Default: (Background: @DefaultBg, LabelStyle: @DefaultLabel),
  Hovered: (Background: @HoveredBg, LabelStyle: @HoveredLabel),
  Pressed: (Background: @PressedBg, LabelStyle: @PressedLabel),
  Disabled: (Background: @DisabledBg, LabelStyle: @DisabledLabel),
  Sounds: @ButtonSounds
)
```

### ScrollbarStyle
```
ScrollbarStyle(
  Spacing: 6,
  Size: 6,
  Background: (TexturePath: "Scrollbar.png", Border: 3),
  Handle: (TexturePath: "ScrollbarHandle.png", Border: 3),
  HoveredHandle: (TexturePath: "ScrollbarHandleHovered.png", Border: 3),
  DraggedHandle: (TexturePath: "ScrollbarHandleDragged.png", Border: 3),
  OnlyVisibleWhenHovered: false
)
```

## Spread Operator

Use `...` to merge/extend styles and objects:

```
@BaseStyle = LabelStyle(FontSize: 16, TextColor: #ffffff);

@ExtendedStyle = LabelStyle(
  ...@BaseStyle,                   // Include all from BaseStyle
  RenderBold: true                 // Add/override properties
);

@ButtonStyle = (
  ...@DefaultButtonStyle,
  Sounds: (
    ...$Sounds.@ButtonsLight,
    ...@CustomSounds
  )
);
```

## Visibility

Control element visibility:

```
Group #OptionalSection {
  Visible: false;                  // Hidden by default
}

Button #CloseButton {
  Visible: @CloseButton;           // Controlled by parameter
}
```

## Tooltips

Add hover tooltips:

```
Group #InfoIcon {
  TooltipText: %ui.tooltip.moreInfo;
  TextTooltipStyle: $C.@DefaultTextTooltipStyle;
}

TextButton #ActionButton {
  TooltipText: "Click to perform action";
  TextTooltipStyle: TextTooltipStyle(
    Background: (TexturePath: "TooltipBg.png", Border: 24),
    MaxWidth: 400,
    LabelStyle: (Wrap: true, FontSize: 16),
    Padding: 24
  );
}
```

## Sound Definitions

Define UI sounds:

```
@ButtonsLight = (
  Activate: (
    SoundPath: "Sounds/ButtonsLightActivate.ogg",
    MinPitch: -0.4,
    MaxPitch: 0.4,
    Volume: 4
  ),
  MouseHover: (
    SoundPath: "Sounds/ButtonsLightHover.ogg",
    Volume: 6
  )
);
```

## Common Page Structure

### Modal Window Page
```
$C = "../Common.ui";

$C.@PageOverlay {}                 // Dark background overlay

$C.@Container {
  Anchor: (Width: 600, Height: 400);
  
  #Title {
    $C.@Title {
      @Text = %page.title;
    }
  }
  
  #Content {
    LayoutMode: Top;
    Padding: (Full: 16);
    
    // Page content here
  }
}

$C.@BackButton {}                  // Back button in corner
```

### Decorated Container Page
```
$C = "../Common.ui";

$C.@PageOverlay {
  LayoutMode: Middle;
  
  $C.@DecoratedContainer {
    Anchor: (Width: 800, Height: 600);
    
    #Title {
      Label {
        Text: %page.decoratedTitle;
        Style: $C.@TitleStyle;
      }
    }
    
    #Content {
      // Content with decorative frame
    }
  }
}
```

### HUD Element
```
Group {
  LayoutMode: Left;
  Anchor: (Top: 20, Height: 60);
  
  Group #StatusDisplay {
    Background: #000000(0.2);
    Anchor: (Left: 20);
    Padding: (Horizontal: 20, Vertical: 10);
    
    Label #ValueLabel {
      Style: (FontSize: 24);
    }
  }
}
```

### Reusable Component
```
$C = "../Common.ui";
$Sounds = "../Sounds.ui";

// Self-contained component - no page overlay
Group {
  Anchor: (Width: 144, Height: 176, Right: 16, Bottom: 16);
  
  TextButton #ActionButton {
    Style: (Sounds: $Sounds.@ButtonsLight);
    FlexWeight: 1;
  }
  
  Group {
    LayoutMode: Middle;
    AssetImage #Icon {
      Anchor: (Width: 128, Height: 128);
    }
  }
}
```

## File Organization

```
UI/
  Custom/
    Common.ui              # Shared styles, templates, variables
    Sounds.ui              # Sound definitions
    Common/                # Shared component .ui files
      TextButton.ui
      ActionButton.ui
    Pages/                 # Full-page UI files
      ShopPage.ui
      SettingsPage.ui
      Memories/            # Related pages grouped
        MemoriesPanel.ui
        Memory.ui
    Hud/                   # HUD overlay elements
      TimeLeft.ui
      StatusBar.ui
```

## Best Practices

1. **Import Common.ui** - Always import the shared common file for consistent styling
2. **Use Templates** - Create parameterized templates for reusable components
3. **ID Important Elements** - Use `#ElementId` for elements accessed from code
4. **Use Translation Keys** - Use `%key` format for all user-visible text
5. **Spread Existing Styles** - Use `...@ExistingStyle` to extend rather than duplicate
6. **Group Related Elements** - Use nested Groups for logical organization
7. **Use FlexWeight** - For flexible layouts instead of fixed sizes where possible
8. **Define Variables** - Extract common values (colors, sizes) into variables
