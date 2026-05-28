# Cloudinary Image Transformation API Reference

**Version**: React Native 0.75.4, Cloudinary URL API v1.1

## Official Documentation

- **Transformations**: https://cloudinary.com/documentation/transformation_reference
- **Image Optimization**: https://cloudinary.com/documentation/image_optimization
- **Responsive Images**: https://cloudinary.com/documentation/responsive_images

## ImageCloudinary Component

Custom component wrapper around React Native Image with Cloudinary transformations.

```typescript
import { ImageCloudinary, ImageProxy } from '@libs/cloudinary';

<ImageCloudinary
  width={300}
  alt="Product image"
  source={{ uri: 'https://img.yourcompany.com/path/to/image.jpg' }}
  quality="auto:eco"
  fetchFormat="auto"
  proxy={ImageProxy.cloudfront}
/>
```

### Props

```typescript
interface ImageCloudinaryProps {
  // Required props
  width: 'auto' | number;           // Image width in pixels or 'auto'
  alt: string;                       // Accessibility label (required)
  source: ImageSourcePropType;       // { uri: string }

  // Optional optimization
  fallbackSource?: ImageSourcePropType; // Local fallback if load fails
  proxy?: ImageProxy;                // 'cloudfront' or 'website'

  // Cloudinary transformations
  crop?: CloudinaryCropMode;         // 'limit' | 'fill' | 'fit' | 'thumb'
  quality?: CloudinaryQuality;       // 'auto:eco' | 'auto:good' | 'auto:best'
  fetchFormat?: CloudinaryFetchFormat; // 'auto' | 'jpg' | 'png' | 'webp'
  dpr?: CloudinaryDPR;               // '1.0' | '2.0' | '3.0' | 'auto'
  gravity?: CloudinaryGravity;       // 'auto' | 'face' | 'center' | positions
  aspectRatio?: number;              // Force specific aspect ratio
  height?: number;                   // Image height in pixels

  // React Native Image props
  style?: ImageStyle;
  resizeMode?: 'cover' | 'contain' | 'stretch' | 'center';
  onLoad?: () => void;
  onError?: (error: any) => void;
}
```

## Quality Settings

### Quality Modes

```typescript
// auto:eco - Best performance, good quality (default)
<ImageCloudinary quality="auto:eco" {...props} />

// auto:good - Higher quality, slightly larger files
<ImageCloudinary quality="auto:good" {...props} />

// auto:best - Maximum quality, largest files
<ImageCloudinary quality="auto:best" {...props} />
```

**Quality Hierarchy**:
- `auto:eco`: Aggressive compression, best for thumbnails and product cards (30-50% size reduction)
- `auto:good`: Balanced quality/performance, ideal for hero images and featured content
- `auto:best`: Minimal compression, use only for brand logos and full-screen galleries

### Quality by Context

```typescript
const QUALITY_SETTINGS = {
  thumbnail: 'auto:eco',      // Small previews, quality less critical
  productCard: 'auto:eco',    // Standard product images
  heroImage: 'auto:good',     // Important header images
  brandAsset: 'auto:best',    // Logos, brand photography
  fullscreen: 'auto:best',    // Gallery lightbox views
} as const;

// Usage
<ImageCloudinary
  quality={QUALITY_SETTINGS.productCard}
  {...props}
/>
```

## Format Selection

### Auto Format

```typescript
// Recommended: Let Cloudinary select optimal format
<ImageCloudinary
  fetchFormat="auto" // WebP, AVIF, or JPEG based on device support
  {...props}
/>
```

**Format Selection Logic**:
1. Checks device support for modern formats
2. Serves AVIF if supported (best compression, ~50% smaller than JPEG)
3. Falls back to WebP if supported (~30% smaller than JPEG)
4. Falls back to JPEG for older devices

### Specific Formats

```typescript
// Force PNG for transparency
<ImageCloudinary fetchFormat="png" {...props} />

// Force WebP for modern browsers
<ImageCloudinary fetchFormat="webp" {...props} />

// Force JPEG for maximum compatibility
<ImageCloudinary fetchFormat="jpg" {...props} />
```

**When to Use Specific Formats**:
- `png`: Images requiring transparency (logos, icons with alpha channel)
- `webp`: Modern devices where you need guaranteed WebP support
- `jpg`: Maximum compatibility for older devices or email templates
- `auto`: **Recommended default** - Let Cloudinary choose optimal format

## Device Pixel Ratio (DPR)

### Responsive DPR

```typescript
import { useWindowDimensions } from 'react-native';

const ResponsiveImage = ({ source, alt }) => {
  const { scale } = useWindowDimensions();

  return (
    <ImageCloudinary
      width={300}
      alt={alt}
      source={source}
      dpr={scale.toFixed(1) as CloudinaryDPR} // '1.0', '2.0', or '3.0'
    />
  );
};
```

**DPR Values**:
- `1.0`: Standard displays (non-Retina) - serves 300px image for 300px width
- `2.0`: Retina displays (most modern devices) - serves 600px image for 300px width
- `3.0`: High-resolution displays (iPhone 12+, Pixel 6+) - serves 900px image for 300px width
- `auto`: Cloudinary detects device capabilities automatically

### DPR Performance Impact

```typescript
// ❌ Fixed 1x DPR - Blurry on Retina displays
<ImageCloudinary width={300} dpr="1.0" />

// ❌ Fixed 3x DPR - Wastes bandwidth on standard displays
<ImageCloudinary width={300} dpr="3.0" />

// ✅ Responsive DPR - Sharp on all devices, optimal bandwidth
const { scale } = useWindowDimensions();
<ImageCloudinary
  width={300}
  dpr={scale.toFixed(1) as CloudinaryDPR}
/>
```

**Bandwidth Impact**:
- 1x DPR: 100% bandwidth (baseline)
- 2x DPR: 400% bandwidth (4x pixels)
- 3x DPR: 900% bandwidth (9x pixels)

**Best Practice**: Always match DPR to device scale to avoid wasting bandwidth or serving blurry images.

## Crop Modes

### Crop Mode Options

```typescript
// 'limit' - Resize within boundaries, maintain aspect ratio (default)
<ImageCloudinary
  width={300}
  height={200}
  crop="limit" // Never exceeds 300x200, preserves original ratio
/>

// 'fill' - Fill exact dimensions, crops excess
<ImageCloudinary
  width={300}
  height={200}
  crop="fill" // Exactly 300x200, crops to fill
  gravity="auto" // Smart crop to keep important content
/>

// 'fit' - Fit within boundaries, add padding
<ImageCloudinary
  width={300}
  height={200}
  crop="fit" // Fits within 300x200, adds padding if needed
/>

// 'thumb' - Smart thumbnail generation
<ImageCloudinary
  width={150}
  height={150}
  crop="thumb" // Smart crop for square thumbnail
  gravity="face" // Focus on faces
/>
```

### Crop Mode Use Cases

```typescript
const CROP_MODES = {
  // Product images - preserve proportions
  productCard: { crop: 'limit' },

  // Avatar images - exact dimensions for circular crops
  avatar: { crop: 'fill', gravity: 'face' },

  // Thumbnails - smart crop focusing on important content
  thumbnail: { crop: 'thumb', gravity: 'auto' },

  // Hero images - fill container completely
  hero: { crop: 'fill', gravity: 'auto' },

  // Logos - no distortion, add padding
  logo: { crop: 'fit' },
} as const;
```

**Crop Mode Behavior**:

| Mode | Aspect Ratio | May Crop | Adds Padding |
|------|--------------|----------|--------------|
| `limit` | Preserved | No | No |
| `fill` | Forced | Yes | No |
| `fit` | Preserved | No | Yes |
| `thumb` | Forced | Yes (smart) | No |

## Gravity (Crop Focus)

### Gravity Options

```typescript
// 'auto' - AI-powered smart crop
<ImageCloudinary
  crop="fill"
  gravity="auto" // Cloudinary detects important content
/>

// 'face' - Focus on detected faces
<ImageCloudinary
  crop="thumb"
  gravity="face" // Crops to include faces
/>

// 'center' - Center crop (default)
<ImageCloudinary
  crop="fill"
  gravity="center"
/>

// Position-based gravity
<ImageCloudinary
  crop="fill"
  gravity="north" // north, south, east, west, north_east, etc.
/>
```

### Gravity Use Cases

```typescript
const GRAVITY_SETTINGS = {
  // User avatars - focus on faces
  avatar: { crop: 'thumb', gravity: 'face' },

  // Product photos - AI detects product
  product: { crop: 'fill', gravity: 'auto' },

  // Food photography - focus on center
  food: { crop: 'fill', gravity: 'center' },

  // Landscape photos - keep top portion
  landscape: { crop: 'fill', gravity: 'north' },

  // Text overlays - keep specific region
  withText: { crop: 'fill', gravity: 'south' },
} as const;
```

**Gravity Modes**:
- `auto`: Uses AI to detect and preserve important content (faces, objects, text)
- `face`: Specifically detects and centers faces
- `center`: Simple center crop (fastest, no AI)
- Positional (`north`, `south`, `east`, `west`, etc.): Fixed position crops

## Responsive Image Sizing

### Auto Width Pattern

```typescript
import { useWindowDimensions } from 'react-native';

const ResponsiveHeroImage = ({ imageUrl }) => {
  const { height, scale } = useWindowDimensions();

  return (
    <ImageCloudinary
      width="auto" // Full container width
      height={height * 0.25} // 25% of screen height
      alt="Hero image"
      source={{ uri: imageUrl }}
      crop="fill"
      gravity="auto"
      quality="auto:good"
      dpr={scale.toFixed(1) as CloudinaryDPR}
    />
  );
};
```

### Fixed Width with Aspect Ratio

```typescript
import { DeviceDimensionsUtils } from '@libs/utils';

// Device-specific aspect ratios
const ASPECT_RATIO = DeviceDimensionsUtils.getDeviceValue<number>(
  16 / 9,  // Small screens - wider
  3 / 2,   // Medium screens - balanced
  5 / 4    // Large screens - taller
);

const ProductImage = ({ imageUrl }) => {
  const IMAGE_WIDTH = 300;
  const IMAGE_HEIGHT = IMAGE_WIDTH / ASPECT_RATIO;

  return (
    <ImageCloudinary
      width={IMAGE_WIDTH}
      height={IMAGE_HEIGHT}
      alt="Product"
      source={{ uri: imageUrl }}
      crop="limit"
      quality="auto:eco"
    />
  );
};
```

### Percentage-Based Sizing

```typescript
const FlexibleImage = ({ imageUrl, aspectRatio = 16 / 9 }) => {
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
    />
  );
};
```

### Grid Layout Pattern

```typescript
const GridImage = ({ imageUrl, columns = 2 }) => {
  const { width } = useWindowDimensions();

  const GRID_PADDING = 16;
  const GRID_GAP = 8;

  const imageWidth = (width - (GRID_PADDING * 2) - (GRID_GAP * (columns - 1))) / columns;
  const imageHeight = imageWidth; // Square images

  return (
    <ImageCloudinary
      width={Math.round(imageWidth)}
      height={Math.round(imageHeight)}
      alt="Grid item"
      source={{ uri: imageUrl }}
      crop="fill"
      gravity="auto"
      quality="auto:eco"
    />
  );
};
```

## Image Proxies

### Proxy Types

```typescript
export enum ImageProxy {
  cloudfront = 'cloudfront', // CloudFront CDN (faster global delivery)
  website = 'website',       // Direct website URL
}

// Production assets - use CloudFront
<ImageCloudinary
  source={{ uri: productImageUrl }}
  proxy={ImageProxy.cloudfront}
  {...props}
/>

// User-generated content - use website proxy
<ImageCloudinary
  source={{ uri: userUploadedUrl }}
  proxy={ImageProxy.website}
  {...props}
/>
```

**Proxy Selection Guidelines**:
- `cloudfront`: Static product images, brand assets, marketing content (better caching, global CDN)
- `website`: User uploads, dynamic content, frequently changing images (faster invalidation)

## Fallback Images

### Basic Fallback

```typescript
import placeholderImage from '@assets/images/placeholder.png';

<ImageCloudinary
  width={300}
  alt="Product"
  source={{ uri: imageUrl }}
  fallbackSource={placeholderImage}
  quality="auto:eco"
/>
```

### Error Handling with State

```typescript
import { useState } from 'react';

const ImageWithFallback = ({ imageUrl, fallbackUrl, alt }) => {
  const [hasError, setHasError] = useState(false);

  const currentSource = hasError && fallbackUrl
    ? { uri: fallbackUrl }
    : { uri: imageUrl };

  return (
    <ImageCloudinary
      source={currentSource}
      alt={alt}
      onError={() => setHasError(true)}
      width={300}
    />
  );
};
```

### Multiple Fallback Attempts

```typescript
const ImageWithCascadingFallbacks = ({ primaryUrl, fallbackUrl, placeholderUrl, alt }) => {
  const [attemptedUrls, setAttemptedUrls] = useState<string[]>([]);

  const currentUrl = attemptedUrls.includes(primaryUrl)
    ? attemptedUrls.includes(fallbackUrl)
      ? placeholderUrl
      : fallbackUrl
    : primaryUrl;

  return (
    <ImageCloudinary
      source={{ uri: currentUrl }}
      alt={alt}
      onError={() => setAttemptedUrls([...attemptedUrls, currentUrl])}
      width={300}
    />
  );
};
```

## URL Construction

### Manual URL Building

```typescript
const buildCloudinaryUrl = ({
  baseUrl,
  transformations,
  filename,
}: {
  baseUrl: string;
  transformations: string[];
  filename: string;
}) => {
  return `${baseUrl}/${transformations.join(',')}/${filename}`;
};

// Usage
const imageUrl = buildCloudinaryUrl({
  baseUrl: 'https://res.cloudinary.com/demo/image/upload',
  transformations: [
    'w_300',           // width: 300
    'h_200',           // height: 200
    'c_fill',          // crop: fill
    'g_auto',          // gravity: auto
    'q_auto:eco',      // quality: auto:eco
    'f_auto',          // format: auto
    'dpr_2.0',         // dpr: 2x
  ],
  filename: 'sample.jpg',
});
// Result: https://res.cloudinary.com/demo/image/upload/w_300,h_200,c_fill,g_auto,q_auto:eco,f_auto,dpr_2.0/sample.jpg
```

### Transformation Parameters

```typescript
const CLOUDINARY_PARAMS = {
  // Dimensions
  width: (w: number) => `w_${w}`,
  height: (h: number) => `h_${h}`,

  // Crop
  crop: (mode: string) => `c_${mode}`,      // c_fill, c_limit, c_fit, c_thumb

  // Quality
  quality: (q: string) => `q_${q}`,         // q_auto:eco, q_auto:good, q_auto:best

  // Format
  format: (f: string) => `f_${f}`,          // f_auto, f_webp, f_jpg, f_png

  // DPR
  dpr: (dpr: string) => `dpr_${dpr}`,       // dpr_1.0, dpr_2.0, dpr_3.0, dpr_auto

  // Gravity
  gravity: (g: string) => `g_${g}`,         // g_auto, g_face, g_center

  // Aspect ratio
  aspectRatio: (ar: string) => `ar_${ar}`,  // ar_16:9, ar_4:3
} as const;
```

## Performance Optimization

### Calculate Exact Size Needed

```typescript
// ✅ Good - exact size
const { width } = useWindowDimensions();
const cardWidth = (width - 48) / 2; // 2 columns with padding

<ImageCloudinary
  width={Math.round(cardWidth)}
  height={Math.round(cardWidth / 1.5)}
  quality="auto:eco"
/>

// ❌ Bad - oversized
<ImageCloudinary
  width={1000} // Requesting 1000px
  style={{ width: 150, height: 150 }} // Displaying 150px - waste 95% bandwidth
/>
```

**Bandwidth Waste Calculation**:
- Requesting 1000px image: ~200 KB
- Displaying at 150px: ~30 KB needed
- **Wasted**: 170 KB (85% waste) per image

### Preloading Critical Images

```typescript
import { Image } from 'react-native';
import { useEffect } from 'react';

const usePreloadImages = (imageUrls: string[]) => {
  useEffect(() => {
    imageUrls.forEach((url) => {
      Image.prefetch(url);
    });
  }, [imageUrls]);
};

// Usage
const ProductScreen = ({ heroUrl, thumbnailUrls }) => {
  usePreloadImages([
    heroUrl,
    ...thumbnailUrls.slice(0, 3), // Preload first 3 thumbnails
  ]);

  return <ProductView />;
};
```

### Lazy Loading Pattern

```typescript
import { useState, useRef, useEffect } from 'react';
import { View } from 'react-native';

const LazyImage = ({ imageUrl, ...props }) => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const viewRef = useRef<View>(null);

  useEffect(() => {
    // Implement intersection observer logic
    // Load image when entering viewport
  }, []);

  if (!shouldLoad) {
    return <View ref={viewRef} style={props.style} />;
  }

  return (
    <ImageCloudinary
      source={{ uri: imageUrl }}
      {...props}
    />
  );
};
```

## Accessibility

### Alt Text Requirements

```typescript
// ✅ Descriptive alt text
<ImageCloudinary
  alt="Fresh salmon fillet with lemon and herbs on white plate"
  source={{ uri: imageUrl }}
  width={300}
/>

// ✅ Empty alt for decorative images
<ImageCloudinary
  alt="" // Screen reader will skip
  source={{ uri: decorativePattern }}
  width={300}
/>

// ❌ Missing alt - accessibility violation
<ImageCloudinary
  source={{ uri: imageUrl }}
  width={300}
  // Missing alt prop!
/>
```

### Writing Good Alt Text

```typescript
// ✅ Good - Concise and descriptive
alt="Grilled chicken breast with roasted vegetables"

// ❌ Bad - Too vague
alt="Food"

// ❌ Bad - Redundant phrases
alt="Image of grilled chicken breast with roasted vegetables"

// ✅ Good - Action for functional images
alt="Close menu" // For close button icon

// ✅ Good - Empty for decorative
alt="" // For decorative background patterns
```

**Alt Text Guidelines**:
1. Describe image content, not visual details
2. Be concise (aim for <150 characters)
3. Avoid "image of" or "picture of"
4. For functional images (buttons), describe action
5. Use empty alt (`alt=""`) for purely decorative images
6. Include text visible in image

## Testing Patterns

### Mock ImageCloudinary

```typescript
jest.mock('@libs/cloudinary', () => ({
  ImageCloudinary: 'ImageCloudinary',
  ImageProxy: {
    cloudfront: 'cloudfront',
    website: 'website',
  },
}));

// In test
import { render } from '@testing-library/react-native';

it('renders product image', () => {
  const { getByLabelText } = render(
    <ProductImage imageUrl="https://example.com/image.jpg" alt="Product" />
  );

  const image = getByLabelText('Product');
  expect(image).toBeTruthy();
  expect(image.props.source).toEqual({ uri: 'https://example.com/image.jpg' });
});
```

### Test Fallback Behavior

```typescript
it('shows fallback on error', () => {
  const { getByLabelText } = render(
    <ImageWithFallback
      imageUrl="https://example.com/invalid.jpg"
      fallbackUrl="https://example.com/fallback.jpg"
      alt="Product"
    />
  );

  const image = getByLabelText('Product');

  // Trigger error
  fireEvent(image, 'error');

  // Should switch to fallback
  expect(image.props.source.uri).toBe('https://example.com/fallback.jpg');
});
```

### Test Responsive Sizing

```typescript
import { useWindowDimensions } from 'react-native';

jest.mock('react-native/Libraries/Utilities/useWindowDimensions', () => ({
  default: jest.fn(),
}));

it('calculates correct size for device', () => {
  (useWindowDimensions as jest.Mock).mockReturnValue({
    width: 375,
    height: 667,
    scale: 2,
  });

  const { getByLabelText } = render(<ResponsiveImage imageUrl="test.jpg" alt="Test" />);

  const image = getByLabelText('Test');
  expect(image.props.width).toBe(375); // Full width
  expect(image.props.dpr).toBe('2.0'); // 2x display
});
```

## Common Mistakes to Avoid

### ❌ Using require() for Images

```typescript
// ❌ NEVER - Bundles images into app
const image = require('./assets/images/product.png');
<Image source={image} />
```

**Impact**: Each image increases APK/IPA size, no CDN benefits, requires app redeployment for updates.

### ✅ Using ImageCloudinary

```typescript
// ✅ ALWAYS - CDN delivery, automatic optimization
<ImageCloudinary
  source={{ uri: 'https://img.yourcompany.com/product.jpg' }}
  alt="Product"
  width={300}
/>
```

### ❌ Omitting Alt Text

```typescript
// ❌ Accessibility violation
<ImageCloudinary source={{ uri: url }} width={300} />
```

**Impact**: Screen readers cannot describe images, violates WCAG 2.1 Level A.

### ✅ Always Provide Alt Text

```typescript
// ✅ Accessible
<ImageCloudinary
  source={{ uri: url }}
  alt="Product name and description"
  width={300}
/>
```

### ❌ Requesting Oversized Images

```typescript
// ❌ Wastes 85% bandwidth
<ImageCloudinary
  width={1000}
  style={{ width: 150, height: 150 }}
/>
```

**Impact**: 150px display needs ~30 KB, 1000px image is ~200 KB = 170 KB waste per image.

### ✅ Request Exact Size

```typescript
// ✅ Optimal bandwidth usage
<ImageCloudinary
  width={150}
  height={150}
  crop="fill"
/>
```

### ❌ Ignoring Device Pixel Ratio

```typescript
// ❌ Blurry on Retina displays
<ImageCloudinary width={300} dpr="1.0" />
```

**Impact**: 2x and 3x displays show blurry images.

### ✅ Match DPR to Device

```typescript
// ✅ Sharp on all displays
const { scale } = useWindowDimensions();
<ImageCloudinary
  width={300}
  dpr={scale.toFixed(1) as CloudinaryDPR}
/>
```

## Quick Reference

### Basic Usage

```typescript
<ImageCloudinary
  width={300}
  alt="Description"
  source={{ uri: imageUrl }}
  quality="auto:eco"
  fetchFormat="auto"
  proxy={ImageProxy.cloudfront}
/>
```

### Responsive with DPR

```typescript
const { scale } = useWindowDimensions();

<ImageCloudinary
  width={300}
  dpr={scale.toFixed(1) as CloudinaryDPR}
  alt="Description"
  source={{ uri: imageUrl }}
/>
```

### With Fallback

```typescript
<ImageCloudinary
  source={{ uri: imageUrl }}
  fallbackSource={require('@assets/placeholder.png')}
  alt="Description"
  width={300}
/>
```

### Hero Image

```typescript
const { height, scale } = useWindowDimensions();

<ImageCloudinary
  width="auto"
  height={height * 0.3}
  crop="fill"
  gravity="auto"
  quality="auto:good"
  dpr={scale.toFixed(1) as CloudinaryDPR}
  alt="Hero"
  source={{ uri: imageUrl }}
/>
```

### Thumbnail

```typescript
<ImageCloudinary
  width={150}
  height={150}
  crop="thumb"
  gravity="auto"
  quality="auto:eco"
  alt="Thumbnail"
  source={{ uri: imageUrl }}
/>
```

## Key Considerations

- Always use ImageCloudinary with CDN URLs, never `require()` for images
- Always provide descriptive alt text for accessibility
- Use `quality="auto:eco"` for most images, `auto:good` for heroes, `auto:best` for brand assets
- Use `fetchFormat="auto"` to enable WebP/AVIF automatic selection
- Match DPR to device scale for sharp images without wasting bandwidth
- Request exact dimensions needed, avoid oversized images
- Use `crop="fill"` with `gravity="auto"` for smart responsive crops
- Provide fallback images for graceful error handling
- Preload critical above-the-fold images
- Calculate responsive sizes based on `useWindowDimensions()`
