---
name: images
description: "WHAT: ImageCloudinary component with Cloudinary CDN for automatic optimization, quality, and responsive sizing. WHEN: displaying product images, optimizing quality/format, supporting Retina displays, implementing fallbacks. KEYWORDS: ImageCloudinary, Cloudinary, CDN, quality, auto:eco, DPR, crop, gravity, fallbackSource, alt."
---

# Image Handling with Cloudinary

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**NEVER use `require()` for images.** Using `require()` bundles images into the app, increasing APK/IPA size, preventing CDN optimization, and requiring app redeployment for updates. Always use ImageCloudinary with Cloudinary URLs.

**Always use ImageCloudinary for Cloudinary-hosted images.** The ImageCloudinary component automatically applies Cloudinary transformations for format selection (WebP, AVIF), quality optimization, responsive sizing, and Device Pixel Ratio handling.

**Always provide alt text for accessibility.** The `alt` prop is required for screen readers. Descriptive alt text improves accessibility and enables visually impaired users to understand image content.

**Use auto format and quality for automatic optimization.** Setting `fetchFormat="auto"` and `quality="auto:eco"` enables Cloudinary to serve the most efficient format and quality based on device capabilities and image content.

**Why**: Proper image handling ensures fast loading times, optimal quality, responsive designs, and accessibility. Cloudinary provides automatic format selection, quality optimization, and responsive transformations that reduce bandwidth by 30-50% and improve user experience.

## When to Use This Skill

Use these patterns when:

- Displaying product images, hero images, or thumbnails
- Loading images from Cloudinary CDN
- Optimizing image quality and format automatically
- Supporting high-resolution (Retina) displays
- Creating responsive images that adapt to screen size
- Implementing fallback images for error handling
- Ensuring accessibility with alt text
- Cropping or resizing images dynamically
- Preloading critical above-the-fold images
- Supporting multi-brand image CDNs

## ImageCloudinary Component

### Basic Usage

```typescript
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

export const ProductImage = ({ imageUrl, alt }) => {
  return (
    <ImageCloudinary
      width={300}
      alt={alt}
      source={{ uri: imageUrl }}
      quality="auto:eco"
      fetchFormat="auto"
      proxy={ImageProxy.cloudfront}
    />
  );
};
```

**Why**: ImageCloudinary automatically applies Cloudinary transformations. Format selection (WebP, AVIF, JPEG), quality adjustment, and responsive sizing happen automatically.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/cart/components/product-item/ProductItem.tsx:122`

### ImageCloudinary Props

```typescript
interface ImageCloudinaryProps {
  // Required
  width: 'auto' | number;        // Image width in pixels or 'auto' for responsive
  alt: string;                    // Accessibility label (REQUIRED)
  source: ImageSourcePropType;    // Image source: { uri: string }

  // Optional optimization
  fallbackSource?: ImageSourcePropType; // Fallback if main image fails
  proxy?: ImageProxy;             // 'cloudfront' or 'website'

  // Cloudinary transformations
  crop?: CloudinaryCropMode;      // Default: 'limit'
  quality?: CloudinaryQuality;    // Default: 'auto:eco'
  fetchFormat?: CloudinaryFetchFormat; // Default: 'auto'
  dpr?: CloudinaryDPR;            // Device pixel ratio
  gravity?: CloudinaryGravity;    // Crop focus point
  aspectRatio?: number;           // Force specific aspect ratio

  // Standard React Native Image props
  style?: ImageStyle;
  resizeMode?: 'cover' | 'contain' | 'stretch' | 'center';
}
```

**Why**: Type-safe props ensure correct usage of Cloudinary transformations and React Native Image properties.

## DO NOT Use require() for Images

### ❌ NEVER Do This

```typescript
// ❌ NEVER use require() for images - bundles into app
const image = require('./assets/images/my-image.png');

<Image source={image} />
```

**Why Not**: Bundling images directly increases APK/IPA size, prevents CDN optimization, and requires app redeployment for updates.

### ✅ ALWAYS Use ImageCloudinary

```typescript
// ✅ ALWAYS use ImageCloudinary with Cloudinary URLs
import { ImageCloudinary } from '@libs/cloudinary';

<ImageCloudinary
  source={{ uri: 'https://img.yourcompany.com/path/to/image.jpg' }}
  alt="Product description"
  width={300}
  quality="auto:eco"
  fetchFormat="auto"
/>
```

**Why**: ImageCloudinary serves images from Cloudinary CDN, enabling:
- Smaller app bundles (images not bundled)
- Dynamic optimization (format, quality, size optimized per device)
- Instant updates (change images without app redeployment)
- Better performance (global CDN delivery)
- Responsive images (automatic device-specific sizing)

### Exceptions (When require() IS Allowed)

Only use `require()` for:

1. **System icons** - Very small UI icons that need immediate availability
2. **Splash screen** - Must be available before network connection
3. **Critical fallback images** - Local placeholders for error states

```typescript
// ✅ Acceptable use of require() for fallback
import placeholderImage from '@assets/images/placeholder.png';

<ImageCloudinary
  source={{ uri: cloudinaryUrl }}
  fallbackSource={placeholderImage} // Local fallback
  alt="Product"
/>
```

**Why**: These exceptional cases require images before network availability or for graceful error handling.

**Production Example**: `git-resources/shared-mobile-modules/src/features/shoppable-product-sections/ingredients/Ingredients.tsx:4`

## Quality Settings

### Quality Hierarchy

```typescript
// ✅ Use auto:eco for standard images (best performance)
<ImageCloudinary
  quality="auto:eco" // Cloudinary automatically optimizes quality
  {...props}
/>

// ✅ Use auto:good for important hero images
<ImageCloudinary
  quality="auto:good" // Higher quality, slightly larger file
  {...props}
/>

// ✅ Use auto:best for critical brand images
<ImageCloudinary
  quality="auto:best" // Maximum quality
  {...props}
/>
```

**Why**: `auto:eco` provides the best balance of quality and performance for most images. Cloudinary analyzes image content and adjusts compression accordingly. Use higher quality only for critical images.

### Quality by Context

```typescript
const QUALITY_BY_CONTEXT = {
  thumbnail: 'auto:eco',    // Small images, quality less critical
  productCard: 'auto:eco',  // Standard product images
  hero: 'auto:good',        // Important header images
  brand: 'auto:best',       // Logo, brand assets
  fullscreen: 'auto:best',  // Full-screen galleries
} as const;
```

**Why**: Different contexts require different quality-performance tradeoffs. Thumbnails benefit from aggressive compression, while brand assets need pristine quality.

## Format Selection

### Auto Format (Recommended)

```typescript
// ✅ Use 'auto' for automatic format selection (recommended)
<ImageCloudinary
  fetchFormat="auto" // Cloudinary serves WebP, AVIF, or JPEG based on device support
  {...props}
/>
```

**Why**: `fetchFormat="auto"` enables Cloudinary to serve the most efficient format supported by the device (WebP on most modern devices, AVIF on newer ones, JPEG as fallback). This reduces file size by 30-50% without quality loss.

### Specific Formats When Needed

```typescript
// ✅ Force PNG for transparency
<ImageCloudinary
  fetchFormat="png"
  {...props}
/>

// ✅ Force WebP for modern browsers
<ImageCloudinary
  fetchFormat="webp"
  {...props}
/>
```

**Why**: Different image types benefit from different formats. Photos compress well in JPEG/WebP, logos need PNG transparency, icons should be SVG for scalability.

## Device Pixel Ratio (DPR)

### Responsive DPR with useWindowDimensions

```typescript
import { useWindowDimensions } from 'react-native';

export const ResponsiveImage = ({ source, alt }) => {
  const { scale } = useWindowDimensions();

  return (
    <ImageCloudinary
      width={300}
      alt={alt}
      source={source}
      // Convert scale (number) to DPR string
      dpr={scale.toFixed(1) as CloudinaryDPR}
      // Device with scale=3 gets 900px image (300 * 3)
      // Device with scale=2 gets 600px image (300 * 2)
    />
  );
};
```

**Why**: `useWindowDimensions().scale` provides the device pixel ratio (1x for standard, 2x for Retina, 3x for high-res). Cloudinary multiplies image dimensions by DPR to serve appropriately sized images for each display.

### DPR Values

```typescript
// Common device pixel ratios:
// - Standard displays: 1.0
// - Retina displays: 2.0
// - High-resolution displays: 3.0

type CloudinaryDPR = '1.0' | '1.5' | '2.0' | '3.0' | 'auto';

// Example usage:
const { scale } = useWindowDimensions();

// Manual DPR based on device
<ImageCloudinary dpr={scale.toFixed(1) as CloudinaryDPR} />

// Automatic DPR (Cloudinary detects)
<ImageCloudinary dpr="auto" />
```

**Why**: Matching DPR to device capabilities ensures sharp images without wasting bandwidth. A 2x display needs 2x resolution, but serving 3x images wastes 50% of bandwidth.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/cloudinary/ImageCloudinary.tsx:61`

## Crop Modes

### Common Crop Modes

```typescript
// 'limit' - Resize within boundaries, maintain aspect ratio (default)
<ImageCloudinary
  width={300}
  height={200}
  crop="limit" // Never exceeds 300x200, maintains original aspect ratio
/>

// 'fill' - Fill exact dimensions, may crop
<ImageCloudinary
  width={300}
  height={200}
  crop="fill" // Exactly 300x200, crops excess content
  gravity="auto" // Smart crop to keep important content
/>

// 'fit' - Fit within boundaries, add padding if needed
<ImageCloudinary
  width={300}
  height={200}
  crop="fit" // Fits within 300x200, adds padding to maintain aspect ratio
/>

// 'thumb' - Generate thumbnail with smart cropping
<ImageCloudinary
  width={150}
  height={150}
  crop="thumb"
  gravity="face" // Focus on faces in thumbnail
/>
```

**Why**: Different crop modes serve different use cases. `limit` preserves quality, `fill` ensures consistent dimensions, `thumb` creates smart thumbnails focusing on important content.

### Crop Mode by Context

```typescript
const CROP_BY_CONTEXT = {
  productCard: 'limit',   // Preserve product proportions
  avatar: 'fill',         // Circular avatars need exact dimensions
  thumbnail: 'thumb',     // Smart crop for small previews
  hero: 'fill',           // Hero images fill container
  logo: 'fit',            // Logos need padding, no distortion
} as const;
```

**Why**: Selecting the right crop mode prevents unwanted distortion and ensures images display correctly in different contexts.

## Gravity (Crop Focus)

### Smart Cropping with Gravity

```typescript
// 'auto' - Smart crop focusing on important content
<ImageCloudinary
  crop="fill"
  gravity="auto" // Cloudinary AI detects important content
/>

// 'face' - Focus on faces
<ImageCloudinary
  crop="thumb"
  gravity="face" // Crops to include detected faces
/>

// 'center' - Center crop (default)
<ImageCloudinary
  crop="fill"
  gravity="center" // Crop from center
/>

// Position-based gravity
<ImageCloudinary
  crop="fill"
  gravity="north" // Crop from top
/>
```

**Why**: Gravity controls which part of the image to preserve during cropping. `auto` uses AI to detect important content (faces, objects), ensuring smart crops that don't cut off critical elements.

## Responsive Image Sizing

### Auto Width with Responsive Height

```typescript
import { useWindowDimensions } from 'react-native';

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
    />
  );
};
```

**Why**: Setting `width="auto"` makes images responsive to container width, while calculating `height` as a percentage of screen height ensures consistent proportions across devices.

### Fixed Width with Dynamic Aspect Ratio

```typescript
import { DeviceDimensionsUtils } from '@libs/utils';

// Device-specific aspect ratio
const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9, // Small devices - wider ratio
  3 / 2,  // Medium devices - balanced
  5 / 4   // Large devices - taller ratio
);

export const ProductImage = ({ imageUrl }) => {
  const IMAGE_WIDTH = 300;
  const IMAGE_HEIGHT = IMAGE_WIDTH / ASPECT_RATIO;

  return (
    <ImageCloudinary
      width={IMAGE_WIDTH}
      height={IMAGE_HEIGHT}
      alt="Product image"
      source={{ uri: imageUrl }}
      crop="limit"
      quality="auto:eco"
      fetchFormat="auto"
    />
  );
};
```

**Why**: Device-specific aspect ratios ensure images look proportional on different screen sizes. Small devices use wider ratios (landscape-friendly), large devices use taller ratios (more vertical content visible).

**Production Example**: `git-resources/shared-mobile-modules/src/libs/cloudinary/ImageCloudinary.tsx:42`

### Percentage-Based Sizing

```typescript
import { useWindowDimensions } from 'react-native';

export const FlexibleImage = ({ imageUrl, aspectRatio = 16 / 9 }) => {
  const { width } = useWindowDimensions();

  const imageWidth = width * 0.9; // 90% of screen width
  const imageHeight = imageWidth / aspectRatio;

  return (
    <ImageCloudinary
      width={imageWidth}
      height={imageHeight}
      alt="Flexible image"
      source={{ uri: imageUrl }}
      crop="limit"
      quality="auto:eco"
      fetchFormat="auto"
    />
  );
};
```

**Why**: Percentage-based sizing adapts images to any screen size. 90% width leaves comfortable margins, while maintaining aspect ratio prevents distortion.

## Image Proxies

### Image Proxy Types

```typescript
export enum ImageProxy {
  cloudfront = 'cloudfront', // CloudFront CDN (faster delivery)
  website = 'website',       // Direct website URL
}

// Use CloudFront for production assets
<ImageCloudinary
  source={{ uri: productImageUrl }}
  proxy={ImageProxy.cloudfront}
  {...props}
/>

// Use website proxy for user-uploaded content
<ImageCloudinary
  source={{ uri: userAvatarUrl }}
  proxy={ImageProxy.website}
  {...props}
/>
```

**Why**: Image proxies determine how Cloudinary fetches the original image. CloudFront provides global CDN distribution for faster loading. Website proxy fetches directly from origin URLs.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/cart/components/product-item/ProductItem.tsx:129`

## Fallback Images

### Error Handling with Fallbacks

```typescript
import placeholderImage from '@assets/images/placeholder.png';

export const ProductImageWithFallback = ({ imageUrl, productName }) => {
  return (
    <ImageCloudinary
      width={300}
      alt={productName}
      source={{ uri: imageUrl }}
      fallbackSource={placeholderImage} // Local fallback image
      quality="auto:eco"
      fetchFormat="auto"
    />
  );
};
```

**Why**: Fallback images prevent broken image icons when network requests fail or URLs are invalid. Provides graceful degradation experience.

**Production Example**: `git-resources/shared-mobile-modules/src/features/shoppable-product-sections/ingredients/Ingredients.tsx:106`

### Implementing Error Handling

```typescript
import { useState } from 'react';

export const ImageWithFallback = ({ imageUrl, fallbackUrl, alt }) => {
  const [hasError, setHasError] = useState(false);

  const currentSource = hasError && fallbackUrl
    ? { uri: fallbackUrl }
    : { uri: imageUrl };

  return (
    <ImageCloudinary
      source={currentSource}
      alt={alt}
      onError={() => setHasError(true)}
      {...props}
    />
  );
};
```

**Why**: Tracking error state enables multiple fallback attempts or displaying custom error UI instead of broken images.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/cloudinary/ImageCloudinary.tsx:50`

## Accessibility

### Alt Text Requirements

```typescript
// ✅ Always provide descriptive alt text
<ImageCloudinary
  alt="Fresh salmon fillet with lemon and herbs on white plate"
  source={{ uri: productImage }}
  {...props}
/>

// ✅ Alt text for decorative images can be empty
<ImageCloudinary
  alt="" // Decorative image, screen reader will skip
  source={{ uri: decorativePattern }}
  {...props}
/>

// ❌ Never omit alt prop
<ImageCloudinary
  // Missing alt - accessibility error!
  source={{ uri: productImage }}
  {...props}
/>
```

**Why**: Alt text is required for screen readers to describe images to visually impaired users. Descriptive alt text improves accessibility. Empty alt (`alt=""`) marks decorative images that should be skipped by screen readers.

### Writing Good Alt Text

```typescript
// ✅ Good alt text: Descriptive and concise
<ImageCloudinary
  alt="Grilled chicken breast with roasted vegetables"
  {...props}
/>

// ❌ Bad alt text: Too vague
<ImageCloudinary
  alt="Food"
  {...props}
/>

// ❌ Bad alt text: Redundant words
<ImageCloudinary
  alt="Image of grilled chicken breast with roasted vegetables"
  {...props}
/>

// ✅ Good alt text for functional images
<ImageCloudinary
  alt="Close menu" // Describes button action
  {...props}
/>
```

**Why**: Good alt text describes image content concisely without redundant phrases like "image of" or "picture of". For functional images (buttons, icons), describe the action, not the visual.

## Performance Best Practices

### Calculate Exact Size Needed

```typescript
// ✅ Calculate exact size needed
const { width } = useWindowDimensions();
const cardWidth = (width - 48) / 2; // 2 columns with padding

<ImageCloudinary
  width={cardWidth} // Exact width needed
  height={cardWidth / 1.5} // Maintain aspect ratio
  quality="auto:eco"
  crop="limit"
/>

// ❌ Don't request oversized images
<ImageCloudinary
  width={1000} // Too large for 150px display
  style={{ width: 150, height: 150 }}
/>
```

**Why**: Requesting images at the exact size needed reduces bandwidth usage and loading time. Downloading 1000px images to display at 150px wastes 95% of bandwidth.

### Preloading Critical Images

```typescript
import { Image } from 'react-native';
import { useEffect } from 'react';

export const usePreloadImages = (imageUrls: string[]) => {
  useEffect(() => {
    // Preload images into cache
    imageUrls.forEach((url) => {
      Image.prefetch(url);
    });
  }, [imageUrls]);
};

// Usage
export const ProductScreen = () => {
  usePreloadImages([
    heroImageUrl,
    productImage1Url,
    productImage2Url,
  ]);

  return <ProductView />;
};
```

**Why**: Preloading critical images prevents loading spinners for important above-the-fold content, improving perceived performance.

## Common Mistakes to Avoid

❌ **Don't use require() for images**:

```typescript
// ❌ Bundles into app, increases size
const image = require('./assets/images/product.png');
<Image source={image} />
```

**Why**: Bundling images directly increases APK/IPA size, prevents CDN optimization, and requires app redeployment for updates.

✅ **Do use ImageCloudinary with Cloudinary URLs**:

```typescript
// ✅ CDN delivery, automatic optimization
<ImageCloudinary
  source={{ uri: 'https://img.yourcompany.com/product.jpg' }}
  alt="Product"
  width={300}
/>
```

**Why**: Cloudinary CDN provides automatic optimization, format selection, and responsive sizing without increasing app bundle size.

❌ **Don't omit alt text**:

```typescript
// ❌ Accessibility violation
<ImageCloudinary
  source={{ uri: imageUrl }}
  width={300}
  // Missing alt!
/>
```

**Why**: Screen readers cannot describe images without alt text, creating accessibility barriers for visually impaired users.

✅ **Do always provide alt text**:

```typescript
// ✅ Accessible image
<ImageCloudinary
  source={{ uri: imageUrl }}
  alt="Product name and description"
  width={300}
/>
```

**Why**: Alt text enables screen readers to describe images, improving accessibility for all users.

❌ **Don't request oversized images**:

```typescript
// ❌ Wastes bandwidth - displaying 150px but loading 1000px
<ImageCloudinary
  width={1000}
  style={{ width: 150, height: 150 }}
/>
```

**Why**: Loading large images and scaling them down wastes bandwidth (95% waste) and slows loading times.

✅ **Do request exact size needed**:

```typescript
// ✅ Efficient - loads exact size
<ImageCloudinary
  width={150}
  height={150}
  crop="fill"
/>
```

**Why**: Requesting exact dimensions reduces file size and improves performance dramatically.

❌ **Don't ignore device pixel ratio**:

```typescript
// ❌ Blurry on high-resolution displays
<ImageCloudinary
  width={300}
  dpr="1.0" // Always 1x resolution
/>
```

**Why**: Fixed 1x DPR creates blurry images on Retina and high-resolution displays.

✅ **Do use device scale for DPR**:

```typescript
// ✅ Sharp on all displays
const { scale } = useWindowDimensions();

<ImageCloudinary
  width={300}
  dpr={scale.toFixed(1) as CloudinaryDPR}
/>
```

**Why**: Matching DPR to device scale ensures sharp images on all display types (standard, Retina, high-res).

❌ **Don't forget fallback images**:

```typescript
// ❌ Shows broken image icon on error
<ImageCloudinary
  source={{ uri: mayFailUrl }}
  alt="Product"
/>
```

**Why**: Network errors or invalid URLs show broken image icons, degrading user experience.

✅ **Do provide fallback images**:

```typescript
// ✅ Graceful degradation
<ImageCloudinary
  source={{ uri: imageUrl }}
  fallbackSource={placeholderImage}
  alt="Product"
/>
```

**Why**: Fallback images provide graceful degradation when primary images fail to load.

## Quick Reference

**Basic ImageCloudinary**:
```typescript
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

<ImageCloudinary
  width={300}
  alt="Description"
  source={{ uri: imageUrl }}
  quality="auto:eco"
  fetchFormat="auto"
  proxy={ImageProxy.cloudfront}
/>
```

**Responsive image with DPR**:
```typescript
const { scale } = useWindowDimensions();

<ImageCloudinary
  width={300}
  alt="Description"
  source={{ uri: imageUrl }}
  dpr={scale.toFixed(1) as CloudinaryDPR}
  quality="auto:eco"
  fetchFormat="auto"
/>
```

**Image with fallback**:
```typescript
import placeholderImage from '@assets/images/placeholder.png';

<ImageCloudinary
  source={{ uri: imageUrl }}
  fallbackSource={placeholderImage}
  alt="Description"
  width={300}
/>
```

**Auto-width hero image**:
```typescript
const { height, scale } = useWindowDimensions();

<ImageCloudinary
  width="auto"
  height={height * 0.3}
  alt="Hero"
  source={{ uri: imageUrl }}
  crop="fill"
  gravity="auto"
  quality="auto:good"
  dpr={scale.toFixed(1) as CloudinaryDPR}
/>
```

**Thumbnail with smart crop**:
```typescript
<ImageCloudinary
  width={150}
  height={150}
  alt="Thumbnail"
  source={{ uri: imageUrl }}
  crop="thumb"
  gravity="auto"
  quality="auto:eco"
/>
```

**Quality by context**:
```typescript
// Thumbnails: auto:eco
// Product cards: auto:eco
// Hero images: auto:good
// Brand assets: auto:best
```

**Crop modes**:
```typescript
crop="limit"  // Preserve aspect ratio (default)
crop="fill"   // Fill exact dimensions (crops)
crop="fit"    // Fit with padding
crop="thumb"  // Smart thumbnail
```

**Key Libraries:**
- react-native 0.76+
- @zest/react-native 1.5.3
- Cloudinary CDN with multi-brand support

**Brand-Specific CDN URLs:**
- yourcompany → https://media.yourcompany.com
- greenchef → https://media.greenchef.com
- everyplate → https://media.everyplate.com
- factor → https://media.factor75.com

For production examples, see [references/examples.md](references/examples.md).
