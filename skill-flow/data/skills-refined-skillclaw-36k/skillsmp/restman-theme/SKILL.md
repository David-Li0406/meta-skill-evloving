---
name: restman-theme
description: Provides design tokens, color scheme, styling patterns, and theming guidelines for the RestMan TUI application. Use when working on UI components, styling, borders, focus states, or visual design consistency in RestMan.
metadata:
  author: restman
  version: "1.0"
---

## When to use this skill

Use this skill when:
- Creating or modifying UI components in RestMan
- Implementing focus states, borders, or color schemes
- Ensuring visual consistency across components
- Working with OpenTUI styling in RestMan
- Questions about RestMan's design system or theme
- Adding new visual elements to the application

## RestMan Theme Overview

RestMan uses a warm, earthy color palette with orange/brown tones as the primary colors. The design emphasizes clear focus states, consistent borders, and readable text against a dark background.

## Design Tokens

All design tokens are centralized in `src/tokens.ts`:

### Color Palette

```typescript
export const colors = {
  // Primary colors
  primary: '#CC8844',      // Warm orange - main brand color
  secondary: '#BB7733',    // Brown-orange - secondary actions

  // Text colors
  textActive: '#FFFFFF',       // White - active/editing text
  textMuted: '#999999',        // Light gray - normal/read-only text
  textPlaceholder: '#666666',  // Dark gray - placeholder text

  // Border colors
  borderDefault: '#555555',    // Gray - default borders
  borderFocused: '#CC8844',    // Primary - focused elements
  borderEdit: '#BB7733',       // Secondary - edit mode

  // Background colors
  backgroundDefault: '#1a1a1a', // Dark background
} as const;
```

### Color Usage Guidelines

#### Primary Color (`#CC8844`)
- Main brand color used throughout the app
- Focus indicators on selected fields
- Active tab labels
- Header text ("RestMan v1.0")
- Toast messages
- Emphasis elements

#### Secondary Color (`#BB7733`)
- Edit mode borders
- Secondary focus states
- Toast border
- Alternative accent color

#### Text Colors
- **Active (`#FFFFFF`)**: Text being edited or in active input fields
- **Muted (`#999999`)**: Read-only content, inactive text
- **Placeholder (`#666666`)**: Empty field hints

#### Border Colors
- **Default (`#555555`)**: Unfocused component borders
- **Focused (`#CC8844`)**: Currently selected component
- **Edit (`#BB7733`)**: Component in edit mode

#### Background
- **Default (`#1a1a1a`)**: Dark background for toast overlays and modals

## Helper Functions

The tokens file provides utility functions for common styling patterns:

### getBorderColor

```typescript
/**
 * Get the border color based on focus and edit mode states
 */
export function getBorderColor(focused: boolean, editMode: boolean): string {
  if (focused) return colors.borderFocused;
  if (editMode) return colors.borderEdit;
  return colors.borderDefault;
}
```

**Usage example:**
```typescript
const borderColor = getBorderColor(focused, editMode);
```

### getTextColor

```typescript
/**
 * Get the text color based on edit mode and whether content exists
 * @param editMode - Whether the field is in edit mode
 * @param hasValue - Whether the field has a value
 */
export function getTextColor(editMode: boolean, hasValue: boolean): string {
  if (editMode) return colors.textActive;
  return hasValue ? colors.textMuted : colors.textPlaceholder;
}
```

**Usage example:**
```typescript
const textColor = getTextColor(editMode, !!value);
```

## Component Styling Patterns

### Input Components

All input components follow this pattern:

```typescript
// Import tokens
import { colors, getBorderColor } from '../tokens';

// In component
const borderColor = getBorderColor(focused, editMode);

return (
  <box
    style={{
      border: true,
      borderColor,
      paddingLeft: 1,
      paddingRight: 1,
    }}
  >
    <text fg={editMode ? colors.textActive : colors.textMuted}>
      {value || placeholder}
    </text>
  </box>
);
```

### Tab Headers

Tab headers use specific colors for each tab type:

```typescript
const tabs = [
  { name: 'headers', label: 'Headers', color: '#CC8844' },  // Primary
  { name: 'params', label: 'Params', color: '#9988BB' },    // Purple
  { name: 'body', label: 'Body', color: '#99AA77' },        // Green
];

// Render with active/inactive states
tabs.map((tab) => (
  <text key={tab.name} fg={activeTab === tab.name ? tab.color : '#666666'}>
    {tab.label}
  </text>
))
```

### Modals and Overlays

Modals use borders and backgrounds for visual hierarchy:

```typescript
<box
  style={{
    position: 'absolute',
    top: 2,
    left: 2,
    right: 2,
    bottom: 2,
    border: true,
    borderColor: colors.primary,      // Primary border
    backgroundColor: colors.backgroundDefault,
    paddingLeft: 2,
    paddingRight: 2,
  }}
>
  {/* Modal content */}
</box>
```

### Toast Notifications

```typescript
<box
  style={{
    position: 'absolute',
    bottom: 2,
    left: 2,
    right: 2,
    border: true,
    borderColor: colors.secondary,    // Secondary border
    paddingLeft: 2,
    paddingRight: 2,
    backgroundColor: colors.backgroundDefault,
  }}
>
  <text fg={colors.primary}>{message}</text>
</box>
```

## OpenTUI Style Properties

RestMan uses kebab-case for style properties:

```typescript
style={{
  flexDirection: 'column',
  gap: 1,
  paddingLeft: 1,
  paddingRight: 1,
  paddingTop: 1,
  paddingBottom: 1,
  backgroundColor: 'black',
  border: true,
  borderColor: '#555555',
  flexGrow: 1,
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
}}
```

## State-Based Styling

Components use three primary states:

### 1. Default State
- Border: `colors.borderDefault` (`#555555`)
- Text: `colors.textMuted` (`#999999`)
- No special indicators

### 2. Focused State
- Border: `colors.borderFocused` (`#CC8844`)
- Text: `colors.textMuted` (`#999999`)
- Indicates current selection

### 3. Edit Mode State
- Border: `colors.borderEdit` (`#BB7733`)
- Text: `colors.textActive` (`#FFFFFF`)
- Indicates active editing

## Component Examples

### Basic Input Component

```typescript
import { colors, getBorderColor } from '../tokens';

interface InputProps {
  value: string;
  onChange: (value: string) => void;
  focused: boolean;
  editMode: boolean;
  placeholder?: string;
}

export function Input({ value, onChange, focused, editMode, placeholder }: InputProps) {
  const borderColor = getBorderColor(focused, editMode);
  const textColor = getTextColor(editMode, !!value);

  return (
    <box
      style={{
        border: true,
        borderColor,
        paddingLeft: 1,
        paddingRight: 1,
      }}
    >
      <text fg={textColor}>{value || placeholder}</text>
    </box>
  );
}
```

### Tabbed Panel

```typescript
import { colors } from '../tokens';

interface TabbedPanelProps {
  focused: boolean;
  editMode: boolean;
  activeTab: string;
  tabs: Array<{ name: string; label: string; color: string }>;
}

export function TabbedPanel({ focused, editMode, activeTab, tabs }: TabbedPanelProps) {
  const borderColor = getBorderColor(focused, editMode);

  return (
    <box
      style={{
        flexDirection: 'column',
        border: true,
        borderColor,
        paddingLeft: 1,
        paddingRight: 1,
      }}
    >
      {/* Tab header */}
      <box style={{ flexDirection: 'row', gap: 1 }}>
        {tabs.map((tab) => (
          <text key={tab.name} fg={activeTab === tab.name ? tab.color : colors.textPlaceholder}>
            {tab.label}
          </text>
        ))}
      </box>
      
      {/* Tab content */}
      <box style={{ flexGrow: 1 }}>
        {/* Content here */}
      </box>
    </box>
  );
}
```

## Best Practices

1. **Always import from tokens**: Never hardcode colors directly
   ```typescript
   // Good
   import { colors } from '../tokens';
   const color = colors.primary;
   
   // Bad
   const color = '#CC8844';
   ```

2. **Use helper functions**: Leverage `getBorderColor` and `getTextColor`
   ```typescript
   // Good
   const borderColor = getBorderColor(focused, editMode);
   
   // Bad
   const borderColor = focused ? '#CC8844' : editMode ? '#BB7733' : '#555555';
   ```

3. **Consistent padding**: Use padding values of 1 or 2 for consistency
   ```typescript
   paddingLeft: 1,
   paddingRight: 1,
   ```

4. **Gap for spacing**: Use `gap: 1` for spacing between flex children
   ```typescript
   style={{ flexDirection: 'row', gap: 1 }}
   ```

5. **Black background for root**: Main app container uses `black` background
   ```typescript
   backgroundColor: 'black'
   ```

6. **Focus indication**: Always show clear focus states with primary color border

7. **Edit mode distinction**: Edit mode uses secondary color to differentiate from focus

## Color Accessibility

The RestMan color scheme follows these principles:

- **High contrast**: White text (`#FFFFFF`) on dark backgrounds
- **Muted for read-only**: Gray text (`#999999`) reduces visual weight
- **Clear focus**: Orange borders (`#CC8844`) stand out against gray defaults
- **Distinct edit state**: Brown-orange (`#BB7733`) distinguishes edit from focus

## Testing Theme Changes

When modifying the theme:

1. Check `src/tokens.ts` for color definitions
2. Update helper functions if adding new states
3. Test across all component types:
   - Input fields (TextInput, URLInput, MethodInput)
   - Panels (RequestEditor, ResponseViewer)
   - Modals (all modal components)
   - Toast notifications
4. Verify focus states with keyboard navigation (Tab, Shift+Tab)
5. Test edit mode activation (press 'e' on focused fields)
6. Ensure consistent appearance across light/dark terminals

## Common Pitfalls

1. **Hardcoding colors**: Always import from tokens
2. **Inconsistent borders**: Use `getBorderColor` helper
3. **Wrong text colors**: Use `getTextColor` helper
4. **Missing focus indicators**: Always show visual feedback for focused elements
5. **Confusing states**: Edit and focus states should be visually distinct

## Reference Files

- Design tokens: `src/tokens.ts`
- Example components: `src/components/TextInput.tsx`, `src/components/RequestEditor.tsx`
- Main app styling: `src/App.tsx`
