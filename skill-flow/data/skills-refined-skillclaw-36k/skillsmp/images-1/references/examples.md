# Image Handling - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating Cloudinary image handling patterns with ImageCloudinary.

## Example 1: ImageCloudinary Implementation

**File**: `libs/cloudinary/ImageCloudinary.tsx:1`

This example shows the complete ImageCloudinary component implementation with automatic optimization.

```typescript
import React, { useState } from 'react';
import {
  useWindowDimensions,
  type ImageProps,
  type ImageSourcePropType,
} from 'react-native';
import Animated from 'react-native-reanimated';

import { Brand } from '@libs/system-country';
import { DeviceDimensionsUtils } from '@libs/utils';

import type {
  CloudinaryDPR,
  CloudinaryParams,
  ImageProxy,
} from './config/cloudinary';
import {
  ASPECT_RATIO_SMALL,
  ASPECT_RATIO_MEDIUM,
  ASPECT_RATIO_LARGE,
} from './constants';
import { getCloudinaryParams } from './getCloudinaryParams';
import { getRoot, getSource } from './utils';

// Define width type for Cloudinary images
export type CloudinaryImageWidth = 'auto' | number;

interface ImagePropsWithProxy extends Omit<ImageProps, 'width'> {
  width: CloudinaryImageWidth;
  alt: string;
  source: ImageSourcePropType;
  fallbackSource?: ImageSourcePropType;
  proxy?: ImageProxy;
}

type Props = ImagePropsWithProxy & CloudinaryParams;

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

  const { scale: screenScale } = useWindowDimensions();

  const cloudinaryParams = getCloudinaryParams({
    ...rest,
    width,
    quality: props.quality || 'auto:eco',
    fetchFormat: props.fetchFormat || 'auto',
    crop: props.crop || 'limit',
    // using the screen scale to set the dpr https://reactnative.dev/docs/usewindowdimensions#scale
    dpr: props.dpr || (screenScale.toFixed(1) as CloudinaryDPR),
  });

  // Use fallback source if there was an error, otherwise use the original source
  const currentSource = hasErrored && fallbackSource ? fallbackSource : source;

  return (
    <Animated.Image
      source={getSource(
        currentSource,
        getRoot(Brand.yourcompany), // Considering yourcompany as default brand
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
      onError={() => {
        setHasErrored(true);
      }}
      {...rest}
    />
  );
};
```

**Key patterns demonstrated:**
- useState for error state tracking (hasErrored)
- useWindowDimensions for screen scale (DPR)
- DeviceDimensionsUtils.getDeviceValue for device-specific aspect ratios
- Default values for quality ('auto:eco'), fetchFormat ('auto'), crop ('limit')
- Automatic DPR calculation from screenScale.toFixed(1)
- Fallback source on error (hasErrored && fallbackSource)
- Animated.Image component
- accessibilityLabel and accessibilityHint from alt prop
- Dynamic height calculation (width / ASPECT_RATIO)
- onError handler to set hasErrored state
- getCloudinaryParams for transformation parameters
- getSource and getRoot utilities for URL construction
- Brand-specific image roots

## Example 2: Product Image with Cloudinary Proxy

**File**: `modules/store/screens/cart/components/product-item/ProductItem.tsx:122`

This example shows ImageCloudinary used for product thumbnails with CloudFront proxy.

```typescript
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

const CLOUDINARY_THUMBNAIL_SIZE = 80;

export const ProductItem = ({
  enrichedProduct: { price, product, selection, actionOverride, mainItemId },
  hideServingCount = false,
}: Props) => {
  const {
    id,
    product: { image, name },
  } = product;

  return (
    <Pressable
      accessibilityRole="button"
      testID={`product-item-${id}`}
      style={({ pressed }) => [styles.container, pressed && styles.pressed]}
      onPress={navigateToProductDetails}
    >
      <View style={styles.innerContainer}>
        <ImageCloudinary
          width={CLOUDINARY_THUMBNAIL_SIZE}
          height={CLOUDINARY_THUMBNAIL_SIZE}
          source={{
            uri: image,
          }}
          alt={name}
          proxy={ImageProxy.cloudfront}
          style={styles.thumbnail}
        />
        {shouldShowNumberOfServings && (
          <Servings servings={numberOfServings * selection.quantity} />
        )}
      </View>
      {/* ... rest of component */}
    </Pressable>
  );
};
```

**Key patterns demonstrated:**
- Fixed width and height (CLOUDINARY_THUMBNAIL_SIZE constant)
- source prop with uri object ({ uri: image })
- alt text from product name
- ImageProxy.cloudfront for CDN delivery
- style prop for additional styling
- Thumbnail sizing (80x80 pixels)
- Product name as descriptive alt text
- testID for testing

## Example 3: Image with Local Fallback

**File**: `features/shoppable-product-sections/ingredients/Ingredients.tsx:100`

This example shows ImageCloudinary with a local fallback image using require().

```typescript
import { View } from 'react-native';

import recipeFallbackImageSmall from '@assets/images/shoppable-product/recipe-image-fallback-small.webp';

import { ImageCloudinary } from '@libs/cloudinary';
import { Text } from '@zest/react-native';

export const Ingredients = ({
  showIngredientsImages,
}: {
  showIngredientsImages: boolean;
}) => {
  return (
    <View>
      {ingredients.map((ingredient) => {
        const a11yLabel = quantityText
          ? `${ingredient.name}, ${quantityText}`
          : `${ingredient.name}`;

        return (
          <View
            key={ingredient.name}
            style={styles.ingredientItem}
            accessible
            accessibilityRole="text"
            accessibilityLabel={a11yLabel}
            accessibilityHint={a11yLabel}
          >
            {showIngredientsImages && (
              <ImageCloudinary
                width={40}
                height={40}
                alt={ingredient.name || ''}
                aria-hidden={true}
                source={{ uri: ingredient.image || '' }}
                fallbackSource={recipeFallbackImageSmall}
              />
            )}
            <View style={styles.ingredientTextContainer}>
              <Text type="body-md-bold">{ingredient.name}</Text>
              {/* ... ingredient details */}
            </View>
          </View>
        );
      })}
    </View>
  );
};
```

**Key patterns demonstrated:**
- require() for local fallback image (recipeFallbackImageSmall)
- fallbackSource prop with imported image
- Small thumbnail size (40x40 pixels)
- alt text from ingredient.name
- aria-hidden={true} for decorative images
- Empty string fallback for alt (alt={ingredient.name || ''})
- Conditional rendering (showIngredientsImages)
- source with uri fallback (source={{ uri: ingredient.image || '' }})
- Graceful degradation when network fails

## Example 4: Responsive Hero Image

This example demonstrates responsive hero image with auto width and percentage-based height (composite example from patterns).

```typescript
import { useWindowDimensions } from 'react-native';
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

export const ResponsiveHeroImage = ({ imageUrl }) => {
  const { height, scale } = useWindowDimensions();

  return (
    <ImageCloudinary
      width="auto" // Full width
      alt="Hero image"
      source={{ uri: imageUrl }}
      height={height * 0.25} // 25% of screen height
      crop="fill"
      gravity="auto"
      quality="auto:good"
      fetchFormat="auto"
      dpr={scale.toFixed(1) as CloudinaryDPR}
      proxy={ImageProxy.cloudfront}
    />
  );
};
```

**Key patterns demonstrated:**
- width="auto" for responsive full-width images
- height as percentage of screen height (height * 0.25)
- useWindowDimensions for height and scale
- crop="fill" for exact dimensions with cropping
- gravity="auto" for smart content-aware cropping
- quality="auto:good" for hero images (higher quality)
- fetchFormat="auto" for automatic format selection
- dpr from scale with toFixed(1) conversion
- ImageProxy.cloudfront for CDN delivery

## Example 5: Device-Specific Aspect Ratios

This example shows device-specific aspect ratio calculation from ImageCloudinary implementation.

```typescript
import { DeviceDimensionsUtils } from '@libs/utils';

// Constants from cloudinary/constants.ts
const ASPECT_RATIO_SMALL = 16 / 9;  // Small devices - wider ratio
const ASPECT_RATIO_MEDIUM = 3 / 2;  // Medium devices - balanced
const ASPECT_RATIO_LARGE = 5 / 4;   // Large devices - taller ratio

/**
 * @context Dynamic aspect ratio based on device size.
 * This is used to calculate the height of the images.
 */
const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  ASPECT_RATIO_SMALL,
  ASPECT_RATIO_MEDIUM,
  ASPECT_RATIO_LARGE
);

// Used in ImageCloudinary component for automatic height calculation
const imageHeight =
  height ||
  (typeof width === 'number' ? width / ASPECT_RATIO : 'auto');
```

**Key patterns demonstrated:**
- DeviceDimensionsUtils.getDeviceValue for device-specific values
- Three breakpoints: small, medium, large
- Wider ratio (16/9) for small devices (landscape-friendly)
- Balanced ratio (3/2) for medium devices
- Taller ratio (5/4) for large devices (more vertical content)
- Automatic height calculation (width / ASPECT_RATIO)
- Fallback to 'auto' when width is not a number
- Height prop override if provided

## Example 6: Quality Settings by Context

This example demonstrates quality settings for different image contexts (composite example from patterns).

```typescript
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

// Thumbnail - low quality, small size
export const ProductThumbnail = ({ imageUrl, productName }) => (
  <ImageCloudinary
    width={150}
    height={150}
    alt={productName}
    source={{ uri: imageUrl }}
    crop="thumb"
    gravity="auto"
    quality="auto:eco" // Aggressive compression for thumbnails
    fetchFormat="auto"
    proxy={ImageProxy.cloudfront}
  />
);

// Product card - standard quality
export const ProductCard = ({ imageUrl, productName }) => (
  <ImageCloudinary
    width={300}
    height={300}
    alt={productName}
    source={{ uri: imageUrl }}
    crop="limit"
    quality="auto:eco" // Standard compression
    fetchFormat="auto"
    proxy={ImageProxy.cloudfront}
  />
);

// Hero image - higher quality
export const HeroImage = ({ imageUrl }) => (
  <ImageCloudinary
    width="auto"
    height={400}
    alt="Featured promotion"
    source={{ uri: imageUrl }}
    crop="fill"
    gravity="auto"
    quality="auto:good" // Higher quality for hero images
    fetchFormat="auto"
    proxy={ImageProxy.cloudfront}
  />
);

// Brand logo - maximum quality
export const BrandLogo = ({ logoUrl }) => (
  <ImageCloudinary
    width={200}
    alt="Brand logo"
    source={{ uri: logoUrl }}
    crop="fit"
    quality="auto:best" // Maximum quality for brand assets
    fetchFormat="png" // Force PNG for transparency
    proxy={ImageProxy.cloudfront}
  />
);
```

**Key patterns demonstrated:**
- quality="auto:eco" for thumbnails and product cards
- quality="auto:good" for hero images
- quality="auto:best" for brand logos
- crop="thumb" for smart thumbnail generation
- crop="limit" for maintaining aspect ratio
- crop="fill" for exact dimensions
- crop="fit" for logos (adds padding, no distortion)
- fetchFormat="png" for logos with transparency
- gravity="auto" for smart content detection
- Different sizes for different contexts

## Example 7: Error Handling with State

This example shows error state management and fallback logic from ImageCloudinary implementation.

```typescript
import { useState } from 'react';
import { ImageCloudinary } from '@libs/cloudinary';
import placeholderImage from '@assets/images/placeholder.png';

export const ImageWithErrorHandling = ({ imageUrl, alt }) => {
  const [hasErrored, setHasErrored] = useState(false);

  // Use fallback source if there was an error, otherwise use the original source
  const currentSource = hasErrored && placeholderImage
    ? placeholderImage
    : { uri: imageUrl };

  return (
    <ImageCloudinary
      width={300}
      alt={alt}
      source={currentSource}
      fallbackSource={placeholderImage}
      onError={() => {
        setHasErrored(true);
      }}
      quality="auto:eco"
      fetchFormat="auto"
    />
  );
};
```

**Key patterns demonstrated:**
- useState for error state tracking
- hasErrored boolean state
- Conditional source selection (hasErrored && placeholderImage)
- onError handler to update state
- fallbackSource prop for automatic fallback
- currentSource calculation before render
- Local placeholder image with require()
- Graceful degradation on network errors

## Summary

The YourCompany codebase consistently follows these image handling patterns:

1. **ImageCloudinary component** - Always use for Cloudinary-hosted images
2. **NEVER use require()** - Except for fallback images, icons, splash screens
3. **Always provide alt text** - Required for accessibility (alt prop)
4. **Quality by context** - auto:eco for thumbnails, auto:good for hero, auto:best for brand
5. **fetchFormat="auto"** - Automatic format selection (WebP, AVIF, JPEG)
6. **DPR from scale** - useWindowDimensions().scale.toFixed(1)
7. **ImageProxy.cloudfront** - CloudFront CDN for faster delivery
8. **fallbackSource** - Local placeholder for error handling
9. **Error state tracking** - useState with onError handler
10. **Device-specific aspect ratios** - DeviceDimensionsUtils.getDeviceValue
11. **Responsive sizing** - width="auto" for full width, percentage-based height
12. **Crop modes by context** - limit for products, fill for hero, thumb for thumbnails
13. **Gravity for smart cropping** - gravity="auto" for AI-powered content detection

These patterns ensure optimal image loading, automatic format selection, responsive sizing, and graceful error handling throughout the app with 30-50% bandwidth savings.
