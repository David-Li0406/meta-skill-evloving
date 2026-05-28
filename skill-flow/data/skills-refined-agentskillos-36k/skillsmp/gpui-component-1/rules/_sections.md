# gpui-component Best Practices - Rule Sections

## Section Overview

| Priority | Prefix | Section | Description |
|----------|--------|---------|-------------|
| 1 | `comp-` | Component Architecture | RenderOnce, structure, stateful patterns |
| 2 | `trait-` | Trait System | Styled, Sizable, Disableable, etc. |
| 3 | `theme-` | Theme System | Colors, variants, ActiveTheme |
| 4 | `dialog-` | Dialog & Overlay | Root, WindowExt, popup comparison |
| 5 | `form-` | Form Components | Input state, validation |
| 6 | `anim-` | Animation | Transitions, keyed state |

## Rules by Section

### Component Architecture (CRITICAL)
- `comp-renderonce` - Use RenderOnce with #[derive(IntoElement)]
- `comp-structure` - Standard component structure template
- `comp-stateful` - Entity + RenderOnce for stateful components
- `comp-callbacks` - Use Rc<dyn Fn> for event callbacks
- `comp-builder` - Fluent builder pattern

### Trait System (CRITICAL)
- `trait-styled` - Implement Styled for style customization
- `trait-sizable` - Implement Sizable with Size enum
- `trait-disableable` - Implement Disableable for disabled state
- `trait-selectable` - Implement Selectable for selection state
- `trait-parent-element` - Implement ParentElement for children
- `trait-interactive` - Implement InteractiveElement for events

### Theme System (HIGH)
- `theme-colors` - Use ThemeColor for consistent colors
- `theme-variants` - Implement variant enums (ButtonVariant)
- `theme-active` - Use ActiveTheme trait for theme access
- `theme-size-system` - Use StyleSized for size-based styling

### Dialog & Overlay (HIGH)
- `dialog-root` - Use Root component as window root
- `dialog-window-ext` - Use WindowExt for dialog management
- `dialog-confirm` - Implement confirm/alert dialogs
- `dialog-comparison` - Dialog vs Popover vs PopupMenu vs Sheet

### Form Components (MEDIUM)
- `form-input-state` - Entity-based input state management
- `form-focus` - Focus management with keyed state
- `form-validation` - Input validation patterns

### Animation (MEDIUM)
- `anim-with-animation` - Use with_animation for transitions
- `anim-keyed-state` - Persist animation state
- `anim-easing` - Use cubic_bezier for smooth animations

## Key Patterns Summary

### Component Structure
```rust
#[derive(IntoElement)]
pub struct MyComponent {
    id: ElementId,
    style: StyleRefinement,
    // ... fields
}

impl RenderOnce for MyComponent { ... }
impl Styled for MyComponent { ... }
impl Sizable for MyComponent { ... }
impl Disableable for MyComponent { ... }
```

### Overlay Usage
```rust
// Dialog
window.open_dialog(cx, |d, _, _| d.title("Title"));

// Sheet
window.open_sheet(cx, |s, _, _| s.title("Panel"));

// Notification
window.push_notification("Message", cx);
```

### Theme Access
```rust
let colors = cx.theme().colors;
div().bg(colors.primary).text_color(colors.primary_foreground)
```
