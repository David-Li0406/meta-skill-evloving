# Theme & Component Reference

Complete reference for theme tokens, z-index layers, and component APIs.

## Theme Tokens

### Colors (`theme.colors.*`)

#### Primary/Secondary/Tertiary
```
primary.{main, dark, light, contrast}
secondary.{main, dark, light, contrast}
tertiary.{main, dark, light, contrast}
```

#### Backgrounds
```
background.{default, paper, elevated, overlay}
```

#### Surfaces
```
surface.{base, raised, sunken, interactive, hover, pressed}
```

#### Text
```
text.{primary, secondary, tertiary, disabled, inverse, link, linkHover}
```

#### Borders
```
border.{subtle, default, strong, interactive, focus}
```

#### Semantic Colors
```
semantic.{success, warning, error, info}.{main, light, dark, contrast}
```

#### Effects
```
effects.{shimmer, glow, shadow, highlight}
```

### Typography (`theme.typography.*`)

#### Font Sizes
| Token | Value | Pixels |
|-------|-------|--------|
| `fontSize.xs` | 0.75rem | 12px |
| `fontSize.sm` | 0.875rem | 14px |
| `fontSize.base` | 1rem | 16px |
| `fontSize.lg` | 1.125rem | 18px |
| `fontSize.xl` | 1.25rem | 20px |
| `fontSize.2xl` | 1.5rem | 24px |
| `fontSize.3xl` | 1.875rem | 30px |
| `fontSize.4xl` | 2.25rem | 36px |
| `fontSize.5xl` | 3rem | 48px |

#### Font Weights
| Token | Value |
|-------|-------|
| `fontWeight.light` | 300 |
| `fontWeight.regular` | 400 |
| `fontWeight.medium` | 500 |
| `fontWeight.semibold` | 600 |
| `fontWeight.bold` | 700 |
| `fontWeight.extrabold` | 800 |

#### Line Heights
```
lineHeight.{tight, normal, relaxed, loose}
```

#### Letter Spacing
```
letterSpacing.{tight, normal, wide}
```

#### Font Families
```
fontFamily.{primary, secondary, monospace}
```

### Spacing (`theme.spacing.*`)

| Token | Value | Pixels |
|-------|-------|--------|
| `xs` | 0.25rem | 4px |
| `sm` | 0.5rem | 8px |
| `md` | 1rem | 16px |
| `lg` | 1.5rem | 24px |
| `xl` | 2rem | 32px |
| `2xl` | 3rem | 48px |
| `3xl` | 4rem | 64px |
| `4xl` | 6rem | 96px |

### Borders (`theme.borders.*`)

#### Radius
```
radius.{none, sm, md, lg, xl, full}
```

#### Width
```
width.{thin, default, thick}
```

### Shadows (`theme.shadows.*`)
```
sm, md, lg, xl, inner, glow, primary
```

### Gradients (`theme.gradients.*`)
```
primary, secondary, sunset, dusk, radial, shimmer
```

## Z-Index Layers

Import from `@src/styles/style`:

```tsx
import { zIndexes } from '@src/styles/style';
```

| Layer | Value | Usage |
|-------|-------|-------|
| `content` | 0 | Base content |
| `header` | 100 | Header bar |
| `sidebar` | 150 | Side navigation |
| `modal` | 200 | Modal dialogs |
| `dropdown` | 300 | Dropdown menus |
| `tooltip` | 400 | Tooltips |
| `loader` | 500 | Loading overlays |
| `toast` | 600 | Toast notifications |

## Layout Dimensions

Import from `@src/styles/style`:

```tsx
import { dimensions } from '@src/styles/style';
```

Key values:
- `sidebarWidth` - Sidebar width
- `headerHeight` - Header height
- `mobileWidth` - Mobile breakpoint (768px)

## Three.js Render Layers

```tsx
import { layers } from '@src/styles/style';
```

| Layer | Value | Usage |
|-------|-------|-------|
| `default` | 0 | Default render layer |
| `raycast` | 7 | Interactive objects |

## Legacy Constants (DEPRECATED)

**DO NOT USE in new code:**
- `fontSizes` from `@src/styles/style.ts` → use `theme.typography.fontSize`
- `fontWeights` from `@src/styles/style.ts` → use `theme.typography.fontWeight`
- `colors` from `@src/styles/style.ts` → use `theme.colors`

**Still valid:**
- `zIndexes` - Z-index layering values
- `dimensions` - Layout dimensions
- `layers` - Three.js render layers

## Component APIs

### Button

```tsx
import { Button } from '@src/component/atoms/Button';

<Button
  scheme="primary"    // primary | surface | warning | error | secondary | tertiary | none
  fontSize="base"     // xs | sm | base | lg | xl | 2xl | 3xl | 4xl | 5xl
  width="fit-content" // fit-content | full
  radius="default"    // default | small
  onClick={handleClick}
>
  Click me
</Button>
```

### Text

```tsx
import { Text } from '@src/component/atoms/Text';
import { useSharedTheme } from '@src/hooks/useSharedTheme';

const MyComponent = () => {
  const { theme } = useSharedTheme();

  return (
    <Text
      text="Hello World"
      fontSize={theme.typography.fontSize.lg}
      fontWeight={theme.typography.fontWeight.bold}
      color={theme.colors.text.primary}
    />
  );
};
```

### Flex Layout

```tsx
import { FlexRow, FlexColumn, InlineFlexRow } from '@src/component/atoms/Flex';

// Row layout
<FlexRow gap={16} align="center">
  <Button />
  <Button />
</FlexRow>

// Column layout
<FlexColumn gap={8} align="flex-start">
  <Text />
  <Text />
</FlexColumn>
```

### Modal

```tsx
import { Modal } from '@src/component/molecules/Modal';

<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="My Modal"
  closeOutside={true}
>
  <Content />
</Modal>
```

### TextField

```tsx
import { TextField } from '@src/component/molecules/TextField';

<TextField
  value={value}
  onChange={setValue}
  label="Username"
  placeholder="Enter username"
  type="text"
/>
```

### Icons

```tsx
import { IoCloseOutline } from 'react-icons/io5';
import { IconContext } from 'react-icons';

<IconContext.Provider value={{ size: '24px' }}>
  <IoCloseOutline />
</IconContext.Provider>
```

Common icon libraries:
- `io5` (Ionicons 5)
- `fa` (Font Awesome)

## Responsive Design

```tsx
import { useIsDesktop } from '@src/hooks/useIsDesktop';

const MyComponent = () => {
  const isDesktop = useIsDesktop();

  return isDesktop ? <DesktopView /> : <MobileView />;
};
```

Mobile breakpoint: 768px (from `dimensions.mobileWidth`)
