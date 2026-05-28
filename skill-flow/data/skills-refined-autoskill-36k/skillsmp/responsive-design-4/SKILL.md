---
name: responsive-design
description: "WHAT: Responsive layouts with useWindowDimensions, Dimensions.get, and DeviceDimensionsUtils. WHEN: adapting to screen sizes, device detection, calculating dynamic dimensions, handling fontScale. KEYWORDS: useWindowDimensions, Dimensions.get, DeviceDimensionsUtils, responsive, width, height, scale, fontScale, percentage."
---

# Responsive Design Patterns for React Native

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Use useWindowDimensions for reactive layouts and Dimensions.get for static constants.** Categorize devices with DeviceDimensionsUtils and adapt layouts with percentage-based sizing and dynamic aspect ratios.

**Why**: Responsive design ensures optimal user experience across all device sizes (iPhone SE to iPad) by dynamically adapting layouts, images, and spacing. Proper responsive patterns prevent UI breaking on edge cases and create consistent experiences.

## When to Use This Skill

Use these patterns when:

- Creating layouts that adapt to different screen sizes
- Supporting multiple device form factors (phone, phablet, tablet)
- Calculating image dimensions and aspect ratios
- Handling device orientation changes
- Supporting accessibility font scaling
- Optimizing images with device pixel ratio
- Creating responsive grids and carousels
- Testing layouts across device sizes

## useWindowDimensions Hook

### Dynamic Reactive Dimensions

Use `useWindowDimensions` for values that need to update when screen size changes:

```typescript
import { useWindowDimensions, View } from 'react-native';

export const ResponsiveHeader = ({ heroImage }: Props) => {
  const { height, width, scale } = useWindowDimensions();

  return (
    <ImageCloudinary
      width="auto"
      alt="Hero Image"
      source={{ uri: heroImage }}
      height={height * 0.2} // 20% of screen height
      dpr={scale.toFixed(1) as CloudinaryDPR} // Device Pixel Ratio
    />
  );
};
```

**Why**: `useWindowDimensions` provides reactive values that update when dimensions change. Perfect for percentage-based layouts and device pixel ratio optimization.

**Production Example**: `libs/cloudinary/ImageCloudinary.tsx:52`

### Return Values

```typescript
interface WindowDimensions {
  width: number;    // Screen width in pixels
  height: number;   // Screen height in pixels
  scale: number;    // Device pixel ratio (1, 2, 3)
  fontScale: number; // User's font scale setting
}

// Example values on iPhone 16 Pro:
// { width: 393, height: 852, scale: 3, fontScale: 1 }

// Example values on iPad Pro 12.9":
// { width: 1024, height: 1366, scale: 2, fontScale: 1 }
```

**Why**: Understanding these values helps create layouts that adapt to device characteristics. `scale` is crucial for image optimization, `fontScale` for accessibility.

### When to Use useWindowDimensions

```typescript
// ✅ Use for dynamic layouts that react to size changes
export const DynamicHeader = () => {
  const { height } = useWindowDimensions();
  return <View style={{ height: height * 0.3 }} />;
};

// ✅ Use for percentage-based dimensions
export const ResponsiveModal = () => {
  const { width } = useWindowDimensions();
  return <View style={{ width: width * 0.9 }} />;
};

// ✅ Use for device pixel ratio
export const HighResImage = () => {
  const { scale } = useWindowDimensions();
  return <Image dpr={scale.toFixed(1)} />;
};
```

**Why**: `useWindowDimensions` enables components to dynamically respond to screen size, making them work across all devices.

## Dimensions.get (Static Dimensions)

### Performance Optimization for Constants

Use `Dimensions.get()` for static dimensions that don't need to react to changes:

```typescript
import { Dimensions } from 'react-native';

/**
 * @context We're utilizing the `Dimensions` API rather than the `useWindowDimensions` hook
 * to avoid unnecessary re-renders. Since we do not support landscape mode,
 * the window dimensions will remain constant.
 *
 * This is a performance optimization to ensure that the carousel does not re-render
 * every time the window dimensions change.
 */
export const WINDOW_WIDTH = Dimensions.get('window').width;
export const WINDOW_HEIGHT = Dimensions.get('window').height;

// Constants that don't change
export const IMAGE_WIDTH_RATIO = 0.8;
export const CAROUSEL_WIDTH = WINDOW_WIDTH * IMAGE_WIDTH_RATIO;
```

**Why**: `Dimensions.get()` is a one-time calculation at import time. More performant for constants that don't need to react to dimension changes.

**Production Example**: `modules/onboarding/screens/welcome-carousel/constants.ts:35`

### window vs screen

```typescript
// 'window' - Visible viewport (excludes status bar, navigation)
const windowDims = Dimensions.get('window');
// Use for: Layout calculations, component sizing

// 'screen' - Full device screen (includes system UI)
const screenDims = Dimensions.get('screen');
// Use for: Full-screen modals, splash screens
```

**Why**: `window` dimensions are typically more useful for layouts, while `screen` dimensions are for full-screen experiences.

### When to Use Dimensions.get

```typescript
// ✅ Use for constants calculated once
export const WINDOW_WIDTH = Dimensions.get('window').width;
export const IMAGE_WIDTH_RATIO = 0.8;
export const CAROUSEL_WIDTH = WINDOW_WIDTH * IMAGE_WIDTH_RATIO;

// ❌ Don't use in component render for dynamic values
export const BadComponent = () => {
  const width = Dimensions.get('window').width; // Use useWindowDimensions instead
  return <View style={{ width }} />;
};
```

**Why**: `Dimensions.get()` won't update if screen size changes (e.g., iPad split view, window resize).

## Device Size Detection (DeviceDimensionsUtils)

### Semantic Device Categorization

Use `DeviceDimensionsUtils` helper for readable device size checks:

```typescript
import { DeviceDimensionsUtils } from '@libs/utils';

// Check device category
const isSmall = DeviceDimensionsUtils.isSmallDevice();  // <= 375px (iPhone SE)
const isMedium = DeviceDimensionsUtils.isMediumDevice(); // 375-414px (iPhone 16 Pro)
const isLarge = DeviceDimensionsUtils.isLargeDevice();   // >= 414px (Plus, Max, iPad)

// Get value based on device size
const spacing = DeviceDimensionsUtils.getDeviceValue<number>(
  12, // Small devices
  16, // Medium devices
  20  // Large devices
);

const aspectRatio = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9, // Small devices - wider ratio
  3 / 2,  // Medium devices - balanced
  5 / 4   // Large devices - taller ratio
);
```

**Why**: `DeviceDimensionsUtils` provides semantic device categorization, making code more readable than magic numbers. The `getDeviceValue` helper prevents ternary chains.

**Production Example**: `libs/utils/deviceDimensions.ts:1`

### Implementation Reference

```typescript
// libs/utils/deviceDimensions.ts
import { Dimensions } from 'react-native';

const WIDTH = Dimensions.get('window').width;

/**
 * @description Devices such as iPhone SE or similar
 */
const isSmallDevice = () => WIDTH <= 375;

/**
 * @description Devices such as iPhone X, 16 Pro, 17 Pro, etc.
 */
const isMediumDevice = () => WIDTH >= 375 && WIDTH < 414;

/**
 * @description Devices such as iPhone 16 Pro Max, Plus, Tablets, etc.
 */
const isLargeDevice = () => WIDTH >= 414;

/**
 * @description Helper function to return a value based on device size,
 * avoiding ternary operators in the code.
 */
const getDeviceValue = <T>(small: T, medium: T, large: T): T => {
  if (isSmallDevice()) return small;
  if (isMediumDevice()) return medium;
  if (isLargeDevice()) return large;
  return medium; // Default fallback
};

export const DeviceDimensionsUtils = {
  isSmallDevice,
  isMediumDevice,
  isLargeDevice,
  getDeviceValue,
};
```

**Why**: Centralized device detection prevents duplicate logic and ensures consistent device categorization across the app.

### Usage in Components

```typescript
import { DeviceDimensionsUtils } from '@libs/utils';

// Dynamic aspect ratio for images
const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9, // Small: Wider ratio fits better
  3 / 2,  // Medium: Balanced
  5 / 4   // Large: More square for larger screens
);

// Dynamic spacing
const PADDING = DeviceDimensionsUtils.getDeviceValue<number>(
  12, // Small: Less padding
  16, // Medium: Default padding
  24  // Large: More padding for larger screens
);

// Component usage
export const ResponsiveCard = () => {
  const imageHeight = 200 / ASPECT_RATIO;

  return (
    <View style={{ padding: PADDING }}>
      <Image style={{ width: 200, height: imageHeight }} />
    </View>
  );
};
```

**Why**: Device-specific values create better visual hierarchy and spacing on different screen sizes.

## Responsive Layouts

### Percentage-Based Sizing

```typescript
import { useWindowDimensions, View } from 'react-native';

export const ResponsiveContainer = ({ children }) => {
  const { width } = useWindowDimensions();

  return (
    <View
      style={{
        width: width * 0.9, // 90% of screen width
        maxWidth: 600,      // Cap at 600px for large screens
        alignSelf: 'center',
      }}
    >
      {children}
    </View>
  );
};
```

**Why**: Percentage-based sizing ensures content scales appropriately across devices while max-width prevents overly wide layouts on tablets.

### Dynamic Aspect Ratios

```typescript
import { Dimensions } from 'react-native';
import { DeviceDimensionsUtils } from '@libs/utils';

export const WINDOW_WIDTH = Dimensions.get('window').width;

/**
 * @context Ratio of the image width to the screen width (80%).
 * Ensures images occupy consistent proportion across devices.
 */
export const IMAGE_WIDTH_RATIO = 0.8;
export const IMAGE_WIDTH = WINDOW_WIDTH * IMAGE_WIDTH_RATIO;

/**
 * @context Dynamic aspect ratio based on device size.
 * Used to calculate image heights.
 */
export const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9, // Small devices
  3 / 2,  // Medium devices
  5 / 4   // Large devices
);

export const IMAGE_HEIGHT = IMAGE_WIDTH / ASPECT_RATIO;
```

**Why**: Dynamic ratios maintain visual consistency while adapting content to different screen shapes. Small devices use wider ratios (landscape-friendly), large devices use taller ratios (more content visible).

**Production Example**: `modules/onboarding/screens/welcome-carousel/constants.ts:42`

### Memoized Dynamic Styles

```typescript
import { useMemo } from 'react';
import { useWindowDimensions, type ImageStyle } from 'react-native';

export const WelcomeCarousel = () => {
  const dynamicImageStyle: ImageStyle = useMemo(
    () => ({
      width: WINDOW_WIDTH,
      height: WINDOW_WIDTH / ASPECT_RATIO,
      resizeMode: 'cover',
    }),
    [] // Empty deps since WINDOW_WIDTH and ASPECT_RATIO are constants
  );

  return <Image source={heroImage} style={dynamicImageStyle} />;
};
```

**Why**: `useMemo` prevents recalculating style objects on every render, improving performance.

**Production Example**: `modules/onboarding/screens/welcome-carousel/WelcomeCarousel.V2.tsx:35`

### Responsive Grid Layouts

```typescript
import { useWindowDimensions, FlatList } from 'react-native';

const CARD_MIN_WIDTH = 160;
const SPACING = 16;

export const ResponsiveGrid = ({ items }: Props) => {
  const { width } = useWindowDimensions();

  // Calculate number of columns based on screen width
  const numColumns = Math.floor(width / (CARD_MIN_WIDTH + SPACING));

  // Calculate card width to fill available space
  const cardWidth = (width - SPACING * (numColumns + 1)) / numColumns;

  return (
    <FlatList
      data={items}
      numColumns={numColumns}
      key={numColumns} // Force re-render when columns change
      columnWrapperStyle={{ gap: SPACING }}
      renderItem={({ item }) => (
        <View style={{ width: cardWidth }}>
          <ProductCard {...item} />
        </View>
      )}
    />
  );
};
```

**Why**: Dynamic column calculation ensures optimal space usage across devices. Small phones show 2 columns, tablets show 4-6 columns.

### Flex-Based Responsive Layouts

```typescript
import { View } from 'react-native';
import { useZestStyles } from '@zest/react-native';

const stylesConfig = {
  container: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 'global.spacing.md',
  },
  item: {
    // Flex-basis creates responsive columns
    flexBasis: '45%', // ~2 columns on small screens
    flexGrow: 1,
    minWidth: 150,
    maxWidth: 300,
  },
};

export const FlexGrid = ({ items }: Props) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      {items.map((item) => (
        <View key={item.id} style={styles.item}>
          <ProductCard {...item} />
        </View>
      ))}
    </View>
  );
};
```

**Why**: Flex-based layouts automatically adjust to available space without calculating columns, making them simpler for basic responsive grids.

## Orientation Handling

### Portrait-Only Applications

```typescript
/**
 * @context We do not support landscape mode.
 * The window dimensions remain constant, so we use Dimensions.get()
 * instead of useWindowDimensions for performance.
 */
export const WINDOW_WIDTH = Dimensions.get('window').width;
export const WINDOW_HEIGHT = Dimensions.get('window').height;
```

**Why**: Many mobile apps lock to portrait orientation. Using `Dimensions.get()` avoids unnecessary re-renders from orientation changes that won't occur.

### Handling Orientation Changes

```typescript
import { useEffect } from 'react';
import { useWindowDimensions } from 'react-native';

export const OrientationAwareComponent = () => {
  const { width, height } = useWindowDimensions();

  const isLandscape = width > height;
  const isPortrait = height > width;

  useEffect(() => {
    // Handle orientation change
    console.log('Orientation:', isLandscape ? 'Landscape' : 'Portrait');
  }, [isLandscape]);

  return (
    <View style={{ flexDirection: isLandscape ? 'row' : 'column' }}>
      <Content />
    </View>
  );
};
```

**Why**: `useWindowDimensions` reactively updates when orientation changes, enabling dynamic layout adjustments.

## Responsive Typography

### FontScale Awareness

```typescript
import { useWindowDimensions } from 'react-native';

export const AccessibleText = () => {
  const { fontScale } = useWindowDimensions();

  // Adjust layout when text is scaled
  const shouldWrapText = fontScale > 1.3;

  return (
    <View style={{ flexDirection: shouldWrapText ? 'column' : 'row' }}>
      <Text>Label:</Text>
      <Text>Value</Text>
    </View>
  );
};
```

**Why**: Users can adjust system font size for accessibility. Layouts should adapt when text becomes larger to prevent clipping or overflow.

### Maximum Font Size

```typescript
import { PixelRatio, Text, StyleSheet } from 'react-native';

const MAX_FONT_SIZE = 24;

const styles = StyleSheet.create({
  text: {
    fontSize: 16,
    maxFontSizeMultiplier: MAX_FONT_SIZE / 16, // 1.5x max scale
  },
});

export const LimitedScaleText = () => (
  <Text style={styles.text} maxFontSizeMultiplier={1.5}>
    This text won't scale beyond 24px
  </Text>
);
```

**Why**: Some UI elements (buttons, headers) shouldn't scale infinitely as it breaks layouts. Set reasonable maximums for critical text.

## Platform-Specific Responsive Patterns

### iOS vs Android Sizing

```typescript
import { Platform } from 'react-native';

const HEADER_HEIGHT = Platform.select({
  ios: 44,     // iOS standard navigation bar
  android: 56, // Android standard app bar
  default: 50,
});

const BOTTOM_TAB_HEIGHT = Platform.select({
  ios: 49,     // iOS tab bar height
  android: 56, // Android navigation bar height
  default: 50,
});
```

**Why**: Platform-specific heights ensure UI elements match platform conventions and don't look out of place.

### Safe Area Responsive Layouts

```typescript
import { useWindowDimensions } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export const ResponsiveSafeLayout = () => {
  const { height } = useWindowDimensions();
  const insets = useSafeAreaInsets();

  // Calculate available height excluding safe areas
  const availableHeight = height - insets.top - insets.bottom;

  return (
    <SafeAreaView edges={['top', 'bottom']}>
      <View style={{ height: availableHeight * 0.3 }}>
        <Header />
      </View>
      <View style={{ height: availableHeight * 0.7 }}>
        <Content />
      </View>
    </SafeAreaView>
  );
};
```

**Why**: Combining window dimensions with safe area insets ensures layouts use all available space without being obscured by notches or system UI.

## Testing Responsive Layouts

### Mock useWindowDimensions

```typescript
import { useWindowDimensions } from 'react-native';

jest.mock('react-native', () => ({
  ...jest.requireActual('react-native'),
  useWindowDimensions: jest.fn(),
}));

describe('ResponsiveComponent', () => {
  it('should render mobile layout', () => {
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 375,
      height: 667,
      scale: 2,
      fontScale: 1,
    });

    const { getByTestId } = render(<ResponsiveComponent />);
    expect(getByTestId('mobile-layout')).toBeDefined();
  });

  it('should render tablet layout', () => {
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 1024,
      height: 768,
      scale: 2,
      fontScale: 1,
    });

    const { getByTestId } = render(<ResponsiveComponent />);
    expect(getByTestId('tablet-layout')).toBeDefined();
  });
});
```

**Why**: Mocking `useWindowDimensions` enables testing responsive behavior for different device sizes without physical devices.

### Mock DeviceDimensionsUtils

```typescript
jest.mock('@libs/utils', () => ({
  DeviceDimensionsUtils: {
    isSmallDevice: jest.fn(),
    isMediumDevice: jest.fn(),
    isLargeDevice: jest.fn(),
    getDeviceValue: jest.fn(),
  },
}));

import { DeviceDimensionsUtils } from '@libs/utils';

describe('Device-specific layout', () => {
  it('should use small device values', () => {
    (DeviceDimensionsUtils.isSmallDevice as jest.Mock).mockReturnValue(true);
    (DeviceDimensionsUtils.getDeviceValue as jest.Mock).mockReturnValue(12);

    const { getByTestId } = render(<Component />);
    const element = getByTestId('container');

    expect(element.props.style.padding).toBe(12);
  });
});
```

**Why**: Mocking device utilities ensures components adapt correctly to different device categories.

## Common Mistakes to Avoid

❌ **Don't use Dimensions.get in render for dynamic values**:

```typescript
// ❌ Won't update if dimensions change
export const BadComponent = () => {
  const { width } = Dimensions.get('window'); // Static value!
  return <View style={{ width: width * 0.9 }} />;
};
```

❌ **Don't hardcode device-specific values**:

```typescript
// ❌ Breaks on different devices
export const BadLayout = () => (
  <View style={{ width: 375 }}> // Hardcoded iPhone width
    <Content />
  </View>
);
```

❌ **Don't forget to handle fontScale**:

```typescript
// ❌ Layout breaks when user scales font
export const BadText = () => (
  <View style={{ flexDirection: 'row', alignItems: 'center' }}>
    <Text style={{ fontSize: 16 }}>Long label text:</Text>
    <Text style={{ fontSize: 16 }}>Value</Text>
  </View>
);
```

❌ **Don't calculate dimensions in component body**:

```typescript
// ❌ Recalculates on every render
export const BadComponent = () => {
  const { width } = useWindowDimensions();
  const cardWidth = (width - 32) / 2; // Expensive calculation every render
  return <View style={{ width: cardWidth }} />;
};
```

✅ **Do use useWindowDimensions for reactive layouts**:

```typescript
// ✅ Updates when dimensions change
export const GoodComponent = () => {
  const { width } = useWindowDimensions();
  return <View style={{ width: width * 0.9 }} />;
};
```

✅ **Do use percentage or device utilities**:

```typescript
// ✅ Works on all devices
export const GoodLayout = () => {
  const { width } = useWindowDimensions();
  return <View style={{ width: width * 0.9 }}><Content /></View>;
};

// ✅ Or use device utilities
const PADDING = DeviceDimensionsUtils.getDeviceValue(12, 16, 24);
```

✅ **Do adapt layout based on fontScale**:

```typescript
// ✅ Layout adapts to font scaling
export const GoodText = () => {
  const { fontScale } = useWindowDimensions();
  const shouldStack = fontScale > 1.3;

  return (
    <View style={{
      flexDirection: shouldStack ? 'column' : 'row',
      alignItems: shouldStack ? 'flex-start' : 'center',
    }}>
      <Text style={{ fontSize: 16 }}>Long label text:</Text>
      <Text style={{ fontSize: 16 }}>Value</Text>
    </View>
  );
};
```

✅ **Do memoize expensive calculations**:

```typescript
// ✅ Calculates only when width changes
export const GoodComponent = () => {
  const { width } = useWindowDimensions();
  const cardWidth = useMemo(() => (width - 32) / 2, [width]);
  return <View style={{ width: cardWidth }} />;
};
```

## Quick Reference

**useWindowDimensions:**
- Reactive values that update when dimensions change
- Use for: Dynamic layouts, percentage sizing, DPR
- Returns: { width, height, scale, fontScale }

**Dimensions.get:**
- Static one-time calculation
- Use for: Constants, portrait-only apps
- Better performance for non-reactive values

**DeviceDimensionsUtils:**
- Device categorization: Small (≤375px), Medium (375-414px), Large (≥414px)
- `getDeviceValue(small, medium, large)` - Avoid ternary chains
- Semantic device checks: `isSmallDevice()`, `isMediumDevice()`, `isLargeDevice()`

**Best Practices:**
- Use percentage-based sizing (width * 0.9)
- Set max-width for large screens
- Calculate dynamic aspect ratios per device size
- Handle fontScale for accessibility
- Memoize expensive calculations
- Use Platform.select for platform-specific values
- Combine with safe area insets

**Device Size Reference:**
- iPhone SE: 320px
- iPhone 12/13/14 Mini: 375px
- iPhone 16 Pro: 393px
- iPhone 16 Pro Max: 430px
- iPad: 768px
- iPad Pro 12.9": 1024px

**Key Libraries:**
- React Native 0.76+
- @zest/react-native 1.5.3
- react-native-safe-area-context

For production examples, see [references/examples.md](references/examples.md).
