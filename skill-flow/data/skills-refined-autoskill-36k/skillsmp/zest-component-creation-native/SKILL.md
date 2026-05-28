---
name: zest-component-creation-native
description: "WHAT: Create Zest design system components for React Native with StyleSheet and accessibility props. WHEN: building new Zest components from Figma, adding variants, creating reusable mobile UI. KEYWORDS: Zest, zest-react-native, StyleSheet, useTheme, TypeScript, testID, accessibilityLabel, accessibilityRole, variants, exports."
---

# Creating Zest Components for React Native

Guide for creating new components in the Zest design system for React Native applications (zest-react-native repository).

## When to Use This Skill

Use this skill when:
- Creating a new Zest component from Figma designs for mobile
- Adding a new variant to an existing Zest React Native component
- Building reusable UI components for the React Native design system
- Implementing components that will be used across multiple features/brands on mobile

## Core Principles

**Components live in `zest-react-native` repository**: All Zest components for React Native are in the standalone `zest-react-native` repository. This is the single source of truth for the Zest design system on mobile.

**Use Zest primitives (Button, Text, Icon, Card)**: Build new components using existing Zest primitives. These provide theme integration and design tokens.

**TypeScript is required**: All components must be written in TypeScript with proper type definitions, interfaces, and exports.

**StyleSheet for styling**: Use React Native StyleSheet API for styling. Access theme tokens via the theme context or props.

**Accessibility is mandatory**: All components must be accessible (accessibilityLabel, accessibilityRole, accessibilityHint, accessibilityState for screen readers like VoiceOver and TalkBack).

**Theme tokens only**: Never hardcode colors, spacing, or typography. Always use theme tokens from the design system.

**Always provide testID**: Every interactive component requires a unique testID for reliable UI testing with @testing-library/react-native.

## File Structure

### Component Directory Structure

```
zest-react-native/
└── src/
    └── components/
        └── MyComponent/
            ├── index.tsx              # Main component file (NOT MyComponent.tsx)
            ├── types.ts               # TypeScript interfaces (NOT MyComponent.types.ts)
            ├── styles.ts              # Zest styles config (NOT MyComponent.styles.ts)
            ├── index.spec.tsx         # Component tests (NOT MyComponent.test.tsx)
            └── (no separate barrel)   # index.tsx exports directly
```

**Important**: The actual Zest repo uses `index.tsx` for the main component, not `ComponentName.tsx`. This differs from typical React Native patterns.

### Example: Creating a Banner Component

**types.ts**:
```typescript
import { ViewStyle, TextStyle } from 'react-native';

export interface MyComponentProps {
  /**
   * The variant style of the component
   */
  variant?: 'primary' | 'secondary' | 'outline';

  /**
   * Size of the component
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Content to display
   */
  children: React.ReactNode;

  /**
   * Press handler
   */
  onPress?: () => void;

  /**
   * Disabled state
   */
  disabled?: boolean;

  /**
   * Test identifier for testing
   */
  testID?: string;

  /**
   * Accessibility label for screen readers
   */
  accessibilityLabel?: string;

  /**
   * Accessibility hint for screen readers
   */
  accessibilityHint?: string;

  /**
   * Additional styles
   */
  style?: ViewStyle;
}
```

**index.tsx**:
```typescript
import React from 'react';
import { TouchableOpacity, View } from 'react-native';
import { Text, useZestStyles } from '@zest/react-native';
import type { MyComponentProps } from './types';
import { stylesConfig } from './styles';

export const MyComponent: React.FC<MyComponentProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onPress,
  disabled = false,
  testID,
  accessibilityLabel,
  accessibilityHint,
  style,
}) => {
  const styles = useZestStyles(stylesConfig);

  const Wrapper = onPress ? TouchableOpacity : View;

  return (
    <Wrapper
      style={[styles.container, styles[variant], disabled && styles.disabled, style]}
      onPress={onPress}
      disabled={disabled}
      testID={testID}
      accessible={true}
      accessibilityRole={onPress ? 'button' : 'none'}
      accessibilityLabel={accessibilityLabel || (typeof children === 'string' ? children : undefined)}
      accessibilityHint={accessibilityHint}
      accessibilityState={{
        disabled: disabled,
      }}
    >
      <Text
        type="body-md-regular"
        style={styles.text}
        testID={testID ? `${testID}-text` : undefined}
      >
        {children}
      </Text>
    </Wrapper>
  );
};

// Direct export from index.tsx (no separate barrel file)
export type { MyComponentProps } from './types';
```

**styles.ts** (using createStylesConfig - not StyleSheet.create):
```typescript
import { createStylesConfig } from '@zest/react-native';

// Extract stylesConfig outside component for performance
export const stylesConfig = createStylesConfig({
  container: {
    borderRadius: 'global.borderRadius.md',
    alignItems: 'center',
    justifyContent: 'center',
  },
  // Variant styles
  primary: {
    backgroundColor: 'alias.color.brand.background.default',
    padding: 'global.spacing.md',
  },
  secondary: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
    borderWidth: 1,
    borderColor: 'alias.color.neutral.border.default',
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: 'alias.color.brand.border.default',
    padding: 'global.spacing.md',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: 'alias.color.neutral.foreground.default',
  },
  // Callback pattern for computed/negative values
  negativeMargin: {
    marginHorizontal: (theme) => -theme.global.spacing.xs,
  },
});
```

**Note**: No separate barrel file needed - `index.tsx` exports directly.

**index.spec.tsx**:
```typescript
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { MyComponent } from './MyComponent';
import { ThemeProvider } from '../../theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider>
      {component}
    </ThemeProvider>
  );
};

describe('MyComponent', () => {
  it('renders children correctly', () => {
    const { getByText } = renderWithTheme(
      <MyComponent>Test Content</MyComponent>
    );
    expect(getByText('Test Content')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const handlePress = jest.fn();
    const { getByTestID } = renderWithTheme(
      <MyComponent onPress={handlePress} testID="my-component">
        Press me
      </MyComponent>
    );

    fireEvent.press(getByTestID('my-component'));
    expect(handlePress).toHaveBeenCalledTimes(1);
  });

  it('does not call onPress when disabled', () => {
    const handlePress = jest.fn();
    const { getByTestID } = renderWithTheme(
      <MyComponent onPress={handlePress} disabled testID="my-component">
        Press me
      </MyComponent>
    );

    fireEvent.press(getByTestID('my-component'));
    expect(handlePress).not.toHaveBeenCalled();
  });

  it('has proper accessibility attributes', () => {
    const { getByTestID } = renderWithTheme(
      <MyComponent
        onPress={() => {}}
        testID="my-component"
        accessibilityLabel="Test button"
        accessibilityHint="Tap to perform action"
      >
        Press me
      </MyComponent>
    );

    const component = getByTestID('my-component');
    expect(component.props.accessible).toBe(true);
    expect(component.props.accessibilityRole).toBe('button');
    expect(component.props.accessibilityLabel).toBe('Test button');
    expect(component.props.accessibilityHint).toBe('Tap to perform action');
  });

  it('renders different variants correctly', () => {
    const { getByTestID, rerender } = renderWithTheme(
      <MyComponent variant="primary" testID="my-component">
        Primary
      </MyComponent>
    );

    let component = getByTestID('my-component');
    expect(component.props.style).toMatchObject({
      backgroundColor: expect.any(String),
    });

    rerender(
      <ThemeProvider>
        <MyComponent variant="secondary" testID="my-component">
          Secondary
        </MyComponent>
      </ThemeProvider>
    );

    component = getByTestID('my-component');
    expect(component.props.style).toMatchObject({
      backgroundColor: expect.any(String),
    });
  });
});
```

## Advanced Patterns

### createStylesConfigFor - Typed Component Styles

Use `createStylesConfigFor<'componentName'>()` for type-safe component-specific styles:

```typescript
import { createStylesConfigFor } from '@zest/react-native';

// Type-safe styles for specific component type
export const stylesConfig = createStylesConfigFor<'button'>()({
  root: {
    // Button-specific styles with type safety
    backgroundColor: 'alias.color.brand.background.default',
    borderRadius: 'global.borderRadius.md',
  },
  label: {
    color: 'alias.color.neutral.foreground.inverse',
  },
});
```

**Why**: `createStylesConfigFor` provides component-specific type safety, ensuring only valid style properties for that component type.

### createZestStyledComponent - HOC Pattern

Use `createZestStyledComponent` for components with conditional state styling:

```typescript
import { createZestStyledComponent, View } from '@zest/react-native';

// Create styled component with state-based styling
export const StyledContainer = createZestStyledComponent(View, {
  default: {
    backgroundColor: 'alias.color.neutral.background.default',
    padding: 'global.spacing.md',
  },
  pressed: {
    backgroundColor: 'alias.color.neutral.background.subtle',
  },
  disabled: {
    opacity: 0.5,
  },
});

// Usage
<StyledContainer pressed={isPressed} disabled={isDisabled}>
  {children}
</StyledContainer>
```

**Why**: `createZestStyledComponent` handles state-based style variants (pressed, disabled, focused) automatically with proper token resolution.

## Theme Tokens

### Accessing Theme Tokens

**Using useZestStyles (preferred)**:
```typescript
import { useZestStyles, createStylesConfig } from '@zest/react-native';

const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',
    backgroundColor: 'alias.color.neutral.background.default',
    borderRadius: 'global.borderRadius.md',
  },
});

const MyComponent = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.container}>{/* Content */}</View>;
};
```

**Using useZestTheme (for dynamic values)**:
```typescript
import { useZestTheme } from '@zest/react-native';
import { useMemo } from 'react';

const MyComponent = ({ isActive }) => {
  const theme = useZestTheme();

  const dynamicStyle = useMemo(() => ({
    backgroundColor: isActive
      ? theme.alias.color.brand.background.default
      : theme.alias.color.neutral.background.default,
  }), [theme, isActive]);

  return <View style={dynamicStyle}>{/* Content */}</View>;
};
```

### Common Theme Token Categories

**Spacing** (`theme.spacing`):
- `sm-1`, `sm-2`, `md-1`, `md-2`, `lg-1`, `lg-2`

**Colors** (`theme.colors`):
- Brand: `brand.primary`, `brand.secondary`
- Neutral: `neutral['100']`, `neutral['200']`, `neutral['800']`
- Semantic: `semantic.success`, `semantic.error`, `semantic.warning`

**Border Radius** (`theme.borderRadius`):
- `sm`, `md`, `lg`

**Typography** (`theme.typography`):
- Use Text component instead of accessing directly

## Accessibility Requirements

### Required Accessibility Props

All interactive components must have:

```typescript
<TouchableOpacity
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Close dialog"
  accessibilityHint="Tap to close the dialog"
  accessibilityState={{
    disabled: isDisabled,
    selected: isSelected,
  }}
  testID="close-button"
>
```

### Accessibility Roles

Common roles:
- `button` - Interactive buttons
- `link` - Navigation links
- `header` - Section headers
- `text` - Static text content
- `none` - Non-interactive decorative elements
- `image` - Images (also provide alt text via accessibilityLabel)
- `checkbox` - Checkboxes
- `switch` - Toggle switches
- `radio` - Radio buttons

### Icons Must Have Alt Text

```typescript
import { Icon } from '@zest/react-native';

// Meaningful icon
<Icon icon="HeartOutline24" altText="Favorite" />

// Decorative icon
<Icon icon="ImageOutline24" altText="" />
```

### Testing Accessibility

```typescript
it('has proper accessibility setup', () => {
  const { getByTestID } = render(
    <MyComponent
      onPress={() => {}}
      testID="component"
      accessibilityLabel="Action button"
      accessibilityHint="Tap to perform action"
    >
      Press me
    </MyComponent>
  );

  const component = getByTestID('component');
  expect(component.props.accessible).toBe(true);
  expect(component.props.accessibilityRole).toBe('button');
  expect(component.props.accessibilityLabel).toBe('Action button');
});
```

## Component Export Pattern

### Update Main Index File

After creating a component, export it from `src/index.ts`:

```typescript
// src/index.ts
export { MyComponent } from './components/MyComponent';
export type { MyComponentProps } from './components/MyComponent';
```

### Barrel Exports

Each component directory should have an `index.ts`:

```typescript
// src/components/MyComponent/index.ts
export { MyComponent } from './MyComponent';
export type { MyComponentProps } from './MyComponent.types';
```

## Testing Patterns

### Basic Component Tests

```typescript
import { render } from '@testing-library/react-native';
import { ThemeProvider } from '../../theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider>
      {component}
    </ThemeProvider>
  );
};

describe('MyComponent', () => {
  it('renders correctly', () => {
    const { getByText } = renderWithTheme(
      <MyComponent>Test</MyComponent>
    );
    expect(getByText('Test')).toBeTruthy();
  });
});
```

### Testing Interactions

```typescript
import { fireEvent } from '@testing-library/react-native';

it('handles press events', () => {
  const handlePress = jest.fn();
  const { getByTestID } = renderWithTheme(
    <MyComponent onPress={handlePress} testID="my-component">
      Press me
    </MyComponent>
  );

  fireEvent.press(getByTestID('my-component'));
  expect(handlePress).toHaveBeenCalledTimes(1);
});
```

### Testing Variants

```typescript
it('renders different variants', () => {
  const { getByTestID, rerender } = renderWithTheme(
    <MyComponent variant="primary" testID="test">
      Primary
    </MyComponent>
  );

  let component = getByTestID('test');
  expect(component.props.style).toMatchObject({
    backgroundColor: expect.any(String),
  });

  rerender(
    <ThemeProvider>
      <MyComponent variant="secondary" testID="test">
        Secondary
      </MyComponent>
    </ThemeProvider>
  );

  component = getByTestID('test');
  expect(component.props.style).toMatchObject({
    backgroundColor: expect.any(String),
  });
});
```

## Common Patterns

### Compound Components

For components with variants:

```typescript
// Button.tsx
const ButtonPrimary: React.FC<ButtonProps> = (props) => (
  <BaseButton {...props} variant="primary" />
);

const ButtonSecondary: React.FC<ButtonProps> = (props) => (
  <BaseButton {...props} variant="secondary" />
);

export const Button = {
  Primary: ButtonPrimary,
  Secondary: ButtonSecondary,
};

// Usage
<Button
  variant="primary"
  size="lg"
  onPress={handleSubmit}
  testID="submit-button"
>
  Submit
</Button>
```

### Forwarding Refs

For components that need ref forwarding:

```typescript
export const MyComponent = React.forwardRef<View, MyComponentProps>(
  ({ children, ...props }, ref) => {
    return (
      <View ref={ref} {...props}>
        {children}
      </View>
    );
  }
);

MyComponent.displayName = 'MyComponent';
```

### Theme-aware Styling

```typescript
const createStyles = (theme: Theme, variant: string) => {
  const colors = {
    primary: theme.colors.brand.primary,
    secondary: theme.colors.neutral['100'],
  };

  return StyleSheet.create({
    container: {
      backgroundColor: colors[variant],
      padding: theme.spacing['md-1'],
      borderRadius: theme.borderRadius.md,
    },
  });
};
```

## Common Mistakes

❌ **Don't hardcode colors**:
```typescript
// Wrong
<View style={{ backgroundColor: '#ffffff', borderColor: '#333333' }}>
```

✅ **Do use theme tokens**:
```typescript
// Correct
<View style={{
  backgroundColor: theme.colors.neutral['100'],
  borderColor: theme.colors.neutral['800'],
}}>
```

❌ **Don't hardcode spacing**:
```typescript
// Wrong
<View style={{ padding: 16, margin: 24 }}>
```

✅ **Do use spacing tokens**:
```typescript
// Correct
<View style={{
  padding: theme.spacing['md-1'],
  margin: theme.spacing['lg-1'],
}}>
```

❌ **Don't skip accessibility**:
```typescript
// Wrong
<TouchableOpacity onPress={handlePress}>
  <Text>Press me</Text>
</TouchableOpacity>
```

✅ **Do add proper accessibility**:
```typescript
// Correct
<TouchableOpacity
  onPress={handlePress}
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Close dialog"
  accessibilityHint="Tap to close"
  testID="close-button"
>
  <Text>Press me</Text>
</TouchableOpacity>
```

❌ **Don't forget testID**:
```typescript
// Wrong
<Button onPress={handlePress}>Submit</Button>
```

✅ **Do always provide testID**:
```typescript
// Correct
<Button onPress={handlePress} testID="submit-button">
  Submit
</Button>
```

❌ **Don't skip icon alt text**:
```typescript
// Wrong
<Icon icon="HeartOutline24" />
```

✅ **Do provide alt text**:
```typescript
// Correct
<Icon icon="HeartOutline24" altText="Favorite" />

// Decorative icon
<Icon icon="ImageOutline24" altText="" />
```

## Quick Reference

**Component file structure**:
```
MyComponent/
├── index.tsx           # Main component + exports
├── types.ts            # TypeScript interfaces
├── styles.ts           # createStylesConfig
└── index.spec.tsx      # Tests
```

**Basic component template (index.tsx)**:
```typescript
import React from 'react';
import { TouchableOpacity, View } from 'react-native';
import { Text, useZestStyles } from '@zest/react-native';
import type { MyComponentProps } from './types';
import { stylesConfig } from './styles';

export const MyComponent: React.FC<MyComponentProps> = ({
  children,
  variant = 'default',
  onPress,
  disabled = false,
  testID,
  accessibilityLabel,
  accessibilityHint,
}) => {
  const styles = useZestStyles(stylesConfig);
  const Wrapper = onPress ? TouchableOpacity : View;

  return (
    <Wrapper
      style={[styles.container, disabled && styles.disabled]}
      onPress={onPress}
      disabled={disabled}
      testID={testID}
      accessible={true}
      accessibilityRole={onPress ? 'button' : 'none'}
      accessibilityLabel={accessibilityLabel}
      accessibilityHint={accessibilityHint}
      accessibilityState={{ disabled }}
    >
      <Text type="body-md-regular">{children}</Text>
    </Wrapper>
  );
};

export type { MyComponentProps } from './types';
```

**Styles template (styles.ts)**:
```typescript
import { createStylesConfig } from '@zest/react-native';

export const stylesConfig = createStylesConfig({
  container: {
    padding: 'global.spacing.md',
    backgroundColor: 'alias.color.neutral.background.default',
    borderRadius: 'global.borderRadius.md',
  },
  disabled: {
    opacity: 0.5,
  },
  // Callback pattern for computed values
  negativeMargin: {
    marginHorizontal: (theme) => -theme.global.spacing.xs,
  },
});
```

**Export from main index.ts**:
```typescript
// src/index.ts
export { MyComponent } from './components/MyComponent';
export type { MyComponentProps } from './components/MyComponent';
```

**Key Libraries:**
- @zest/react-native 1.5.3
- React Native 0.76+
