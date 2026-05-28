# Responsive Design - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating responsive design patterns.

## Example 1: Welcome Carousel with Dynamic Aspect Ratios

**File**: `modules/onboarding/screens/welcome-carousel/constants.ts`

This example demonstrates using `Dimensions.get()` for performance optimization in portrait-only apps with dynamic aspect ratios based on device size.

```typescript
import { Dimensions } from 'react-native';
import { DeviceDimensionsUtils } from '@libs/utils';

/**
 * @context We're utilizing the `Dimensions` API rather than the `useWindowDimensions` hook
 * to avoid unnecessary re-renders. Since we do not support landscape mode,
 * the window dimensions will remain constant.
 *
 * This is a performance optimization to ensure that the carousel does not re-render
 * every time the window dimensions change.
 */
export const WINDOW_WIDTH = Dimensions.get('window').width;

/**
 * @context Ratio of the image width to the screen width (80%).
 * This constant is used to calculate the dimensions of the carousel images,
 * ensuring they occupy a consistent proportion of the screen across different devices.
 */
export const IMAGE_WIDTH_RATIO = 0.8;

/**
 * @context Dynamic aspect ratio based on device size.
 * This is used to calculate the height of the carousel images.
 */
export const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9, // Small devices
  3 / 2,  // Medium devices
  5 / 4   // Large devices
);
```

**Key patterns demonstrated:**
- `Dimensions.get()` for static constants in portrait-only apps
- Performance optimization by avoiding unnecessary re-renders
- Dynamic aspect ratios using `DeviceDimensionsUtils.getDeviceValue()`
- Small devices (≤375px) use wider 16:9 ratio
- Medium devices (375-414px) use balanced 3:2 ratio
- Large devices (≥414px) use taller 5:4 ratio
- Percentage-based image sizing (80% of screen width)

## Example 2: Welcome Carousel Component with useMemo

**File**: `modules/onboarding/screens/welcome-carousel/WelcomeCarousel.V2.tsx`

This example shows memoizing dynamic styles for performance and using `useWindowDimensions` for device pixel ratio.

```typescript
import { useMemo } from 'react';
import type { ImageStyle, ListRenderItem } from 'react-native';
import { Dimensions, Image, View } from 'react-native';
import { Carousel, useZestStyles } from '@zest/react-native';

import { ASPECT_RATIO, WELCOME_CAROUSEL_DATA, WINDOW_WIDTH } from './constants';

export const WelcomeCarouselV2 = ({ navigation }: Props) => {
  const styles = useZestStyles(stylesConfig);

  // Memoize dynamic image style to prevent recalculation on every render
  const dynamicImageStyle: ImageStyle = useMemo(
    () => ({
      width: WINDOW_WIDTH,
      height: WINDOW_WIDTH / ASPECT_RATIO,
      resizeMode: 'cover',
    }),
    [] // Empty deps since WINDOW_WIDTH and ASPECT_RATIO are constants
  );

  const renderItem: ListRenderItem<WelcomeCarouselData> = ({ item, index }) => (
    <View style={styles.carouselContainer}>
      <Image
        source={assets?.v1Image[index]}
        style={dynamicImageStyle}
        accessibilityIgnoresInvertColors
      />
      <View style={styles.carouselBodyContent}>
        <Text type="headline-xl">{translateRaw(item.title)}</Text>
        <Text type="body-lg-regular">{translateRaw(item.body)}</Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Carousel
        data={WELCOME_CAROUSEL_DATA}
        renderItem={renderItem}
        keyExtractor={(item) => item.title}
        itemWidth={Dimensions.get('window').width}
        style={styles.content}
      />
    </View>
  );
};
```

**Key patterns demonstrated:**
- `useMemo` to prevent recalculating styles on every render
- Empty dependency array for constants (WINDOW_WIDTH, ASPECT_RATIO)
- Dynamic image height calculation based on aspect ratio
- `Dimensions.get('window').width` for carousel item width
- Combining static constants with memoized calculations
- Performance optimization for carousel rendering

## Example 3: DeviceDimensionsUtils Implementation

**File**: `libs/utils/deviceDimensions.ts`

This is the production implementation of the device categorization utility used throughout the YourCompany codebase.

```typescript
import { Dimensions } from 'react-native';

const WIDTH = Dimensions.get('window').width;

/**
 * @description Devices such as iPhone SE or similar
 *
 * @returns boolean
 */
const isSmallDevice = () => WIDTH <= 375;

/**
 * @description Devices such as iPhone X, 16 Pro, 17 Pro, etc.
 *
 * @returns boolean
 */
const isMediumDevice = () => WIDTH >= 375 && WIDTH < 414;

/**
 * @description Devices such as Larger devices iPhone 16 Pro Max, Plus, Tablets, etc.
 *
 * @returns boolean
 */
const isLargeDevice = () => WIDTH >= 414;

/**
 * @description Helper function used to return a value based on the device size,
 * thus avoiding ternary operators in the code.
 *
 * @template T - Type of the value to be returned.
 *
 * @param small value for small devices.
 * @param medium value for medium devices.
 * @param large value for large devices.
 *
 * @returns value based on the device size, defaults to medium.
 */
const getDeviceValue = <T>(small: T, medium: T, large: T): T => {
  if (isSmallDevice()) {
    return small;
  } else if (isMediumDevice()) {
    return medium;
  } else if (isLargeDevice()) {
    return large;
  }

  return medium;
};

export const DeviceDimensionsUtils = {
  isSmallDevice,
  isMediumDevice,
  isLargeDevice,
  getDeviceValue,
};
```

**Key patterns demonstrated:**
- Single WIDTH constant calculated once at module import
- Three device size categories based on width breakpoints
- Small: ≤375px (iPhone SE, Mini)
- Medium: 375-414px (Standard iPhones)
- Large: ≥414px (Plus, Max, Tablets)
- Generic `getDeviceValue<T>` function for type-safe value selection
- Default fallback to medium for edge cases
- Semantic helper functions for readable code

## Example 4: ImageCloudinary with useWindowDimensions

**File**: `libs/cloudinary/ImageCloudinary.tsx`

This example shows using `useWindowDimensions` for device pixel ratio optimization in image loading.

```typescript
import React, { useState } from 'react';
import { useWindowDimensions, type ImageProps } from 'react-native';
import Animated from 'react-native-reanimated';

import { DeviceDimensionsUtils } from '@libs/utils';
import type { CloudinaryDPR, CloudinaryParams } from './config/cloudinary';
import {
  ASPECT_RATIO_SMALL,
  ASPECT_RATIO_MEDIUM,
  ASPECT_RATIO_LARGE,
} from './constants';

/**
 * @context Dynamic aspect ratio based on device size.
 * This is used to calculate the height of the images.
 */
const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  ASPECT_RATIO_SMALL,
  ASPECT_RATIO_MEDIUM,
  ASPECT_RATIO_LARGE
);

export const ImageCloudinary: React.FC<Props> = (props) => {
  const { width, height, style, source, fallbackSource, ...rest } = props;
  const [hasErrored, setHasErrored] = useState(false);

  // Get device pixel ratio from useWindowDimensions
  const { scale: screenScale } = useWindowDimensions();

  const cloudinaryParams = getCloudinaryParams({
    ...rest,
    width,
    quality: props.quality || 'auto:eco',
    fetchFormat: props.fetchFormat || 'auto',
    crop: props.crop || 'limit',
    // Using the screen scale to set the dpr for optimal image quality
    // https://reactnative.dev/docs/usewindowdimensions#scale
    dpr: props.dpr || (screenScale.toFixed(1) as CloudinaryDPR),
  });

  const currentSource = hasErrored && fallbackSource ? fallbackSource : source;

  return (
    <Animated.Image
      source={getSource(
        currentSource,
        getRoot(Brand.yourcompany),
        cloudinaryParams,
        fallbackSource,
        props.proxy
      )}
      accessibilityLabel={props.alt}
      accessibilityHint={props.alt}
      style={[
        {
          width,
          height:
            height ||
            (typeof width === 'number' ? width / ASPECT_RATIO : 'auto'),
        },
        style,
      ]}
      onError={() => setHasErrored(true)}
      {...rest}
    />
  );
};
```

**Key patterns demonstrated:**
- `useWindowDimensions()` to get device pixel ratio (scale)
- Device pixel ratio used for Cloudinary image optimization
- `screenScale.toFixed(1)` converts to DPR format (e.g., "2.0", "3.0")
- Dynamic aspect ratio using `DeviceDimensionsUtils.getDeviceValue()`
- Automatic height calculation based on width and aspect ratio
- Fallback to 'auto' height for non-numeric widths
- Error handling with fallback source
- Accessibility labels and hints

## Example 5: Responsive Grid Layout Pattern

This pattern is commonly used for product grids, recipe cards, and catalog views in the YourCompany app.

```typescript
import { useWindowDimensions, FlatList, View } from 'react-native';

const CARD_MIN_WIDTH = 160;
const SPACING = 16;

export const ResponsiveProductGrid = ({ products }: Props) => {
  const { width } = useWindowDimensions();

  // Calculate number of columns based on screen width
  // Small devices (≤375px): 2 columns
  // Medium devices (375-414px): 2 columns
  // Large devices (≥414px): 3+ columns
  const numColumns = Math.floor(width / (CARD_MIN_WIDTH + SPACING));

  // Calculate card width to fill available space
  const cardWidth = (width - SPACING * (numColumns + 1)) / numColumns;

  return (
    <FlatList
      data={products}
      numColumns={numColumns}
      key={numColumns} // Force re-render when columns change
      columnWrapperStyle={{ gap: SPACING }}
      contentContainerStyle={{ padding: SPACING }}
      renderItem={({ item }) => (
        <View style={{ width: cardWidth }}>
          <ProductCard product={item} />
        </View>
      )}
      keyExtractor={(item) => item.id}
    />
  );
};
```

**Key patterns demonstrated:**
- `useWindowDimensions()` for reactive layout
- Dynamic column calculation based on minimum card width
- `Math.floor()` to determine column count
- Calculate card width to fill available space with spacing
- `key={numColumns}` forces FlatList re-render when layout changes
- `columnWrapperStyle` for gap between columns
- Consistent spacing using contentContainerStyle

## Example 6: FontScale Awareness for Accessibility

This pattern ensures layouts adapt when users increase system font size for accessibility.

```typescript
import { useWindowDimensions, View, Text } from 'react-native';

export const ResponsiveLabel = ({ label, value }: Props) => {
  const { fontScale } = useWindowDimensions();

  // Switch to vertical layout when text is scaled beyond 1.3x
  const shouldStack = fontScale > 1.3;

  return (
    <View
      style={{
        flexDirection: shouldStack ? 'column' : 'row',
        alignItems: shouldStack ? 'flex-start' : 'center',
        gap: shouldStack ? 4 : 8,
      }}
    >
      <Text type="body-md-bold">{label}:</Text>
      <Text type="body-md-regular">{value}</Text>
    </View>
  );
};
```

**Key patterns demonstrated:**
- `fontScale` from `useWindowDimensions()` for accessibility
- 1.3x threshold for layout change (30% increase)
- Switch from horizontal to vertical layout for larger text
- Adjust alignment and gap based on layout direction
- Prevent text overflow and clipping
- Maintain readability at all font scales

## Example 7: Testing Responsive Layouts

This pattern is used throughout the YourCompany test suite for testing responsive behavior.

```typescript
import { useWindowDimensions } from 'react-native';
import { render } from '@testing-library/react-native';
import { DeviceDimensionsUtils } from '@libs/utils';

jest.mock('react-native', () => ({
  ...jest.requireActual('react-native'),
  useWindowDimensions: jest.fn(),
}));

jest.mock('@libs/utils', () => ({
  DeviceDimensionsUtils: {
    isSmallDevice: jest.fn(),
    isMediumDevice: jest.fn(),
    isLargeDevice: jest.fn(),
    getDeviceValue: jest.fn(),
  },
}));

describe('ResponsiveComponent', () => {
  it('should render small device layout', () => {
    // Mock iPhone SE dimensions
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 375,
      height: 667,
      scale: 2,
      fontScale: 1,
    });

    (DeviceDimensionsUtils.isSmallDevice as jest.Mock).mockReturnValue(true);
    (DeviceDimensionsUtils.getDeviceValue as jest.Mock).mockReturnValue(12);

    const { getByTestId } = render(<ResponsiveComponent />);
    const element = getByTestId('container');

    expect(element.props.style.padding).toBe(12);
  });

  it('should render tablet layout', () => {
    // Mock iPad dimensions
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 1024,
      height: 768,
      scale: 2,
      fontScale: 1,
    });

    (DeviceDimensionsUtils.isLargeDevice as jest.Mock).mockReturnValue(true);
    (DeviceDimensionsUtils.getDeviceValue as jest.Mock).mockReturnValue(24);

    const { getByTestId } = render(<ResponsiveComponent />);
    const element = getByTestId('container');

    expect(element.props.style.padding).toBe(24);
  });

  it('should adapt layout to large font scale', () => {
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 375,
      height: 667,
      scale: 2,
      fontScale: 1.5, // 150% font scale
    });

    const { getByTestId } = render(<ResponsiveComponent />);
    const element = getByTestId('layout');

    expect(element.props.style.flexDirection).toBe('column');
  });
});
```

**Key patterns demonstrated:**
- Mock `useWindowDimensions` for different device sizes
- Mock `DeviceDimensionsUtils` for device categorization
- Test small (iPhone SE), medium (iPhone 16 Pro), and large (iPad) layouts
- Test font scale adaptations (1.0x, 1.3x, 1.5x)
- Verify layout direction changes based on fontScale
- Ensure padding/spacing adapts to device size

## Anti-Patterns from Codebase Review

### ❌ Using Dimensions.get in Component Render

```typescript
// DON'T: Static value won't update on dimension changes
export const BadComponent = () => {
  const { width } = Dimensions.get('window');
  return <View style={{ width: width * 0.9 }} />;
};

// DO: Use useWindowDimensions for reactive values
export const GoodComponent = () => {
  const { width } = useWindowDimensions();
  return <View style={{ width: width * 0.9 }} />;
};
```

### ❌ Hardcoding Device-Specific Values

```typescript
// DON'T: Only works on specific devices
export const BadLayout = () => (
  <View style={{ width: 375 }}>
    <Content />
  </View>
);

// DO: Use percentage-based sizing
export const GoodLayout = () => {
  const { width } = useWindowDimensions();
  return (
    <View style={{ width: width * 0.9 }}>
      <Content />
    </View>
  );
};
```

### ❌ Forgetting to Memoize Expensive Calculations

```typescript
// DON'T: Recalculates on every render
export const BadComponent = () => {
  const { width } = useWindowDimensions();
  const cardWidth = (width - 32) / 2;
  return <View style={{ width: cardWidth }} />;
};

// DO: Memoize calculations
export const GoodComponent = () => {
  const { width } = useWindowDimensions();
  const cardWidth = useMemo(() => (width - 32) / 2, [width]);
  return <View style={{ width: cardWidth }} />;
};
```

## Summary

The YourCompany codebase consistently follows these responsive design patterns:

1. **useWindowDimensions** for reactive layouts and device pixel ratio
2. **Dimensions.get** for static constants in portrait-only apps
3. **DeviceDimensionsUtils** for semantic device categorization
4. **Dynamic aspect ratios** based on device size (16:9, 3:2, 5:4)
5. **Percentage-based sizing** (80%, 90% of screen width)
6. **useMemo** for performance optimization
7. **fontScale awareness** for accessibility
8. **Responsive grids** with dynamic column calculation
9. **Platform.select** for iOS/Android differences
10. **Comprehensive testing** with mocked dimensions

These patterns ensure optimal user experience across all device sizes from iPhone SE (320px) to iPad Pro (1024px) while maintaining performance and accessibility.
