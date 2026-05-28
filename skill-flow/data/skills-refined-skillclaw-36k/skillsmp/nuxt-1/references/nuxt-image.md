# Nuxt Image Reference

**Last Updated:** 2025-11

**Check:** `@nuxt/image` in package.json

Nuxt Image is an image optimization module that provides automatic image optimization, lazy loading, responsive images, and support for multiple image providers.

## Installation & Setup

```bash
pnpm add @nuxt/image
```

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  modules: ["@nuxt/image"],

  image: {
    // Optional configuration
    quality: 80,
    formats: ["webp", "avif"],

    // Image providers
    providers: {
      cloudinary: {
        baseURL: "https://res.cloudinary.com/{your-cloud-name}/image/upload/",
      },
    },
  },
})
```

## Core Components

### NuxtImg

Basic optimized image component:

```vue
<template>
  <NuxtImg src="/images/hero.jpg" alt="Hero image" width="800" height="600" />
</template>
```

**Common Props:**

- `src` - Image source (path or URL)
- `alt` - Alt text for accessibility
- `width` / `height` - Dimensions
- `loading` - `"lazy"` (default) or `"eager"`
- `fit` - `"cover"`, `"contain"`, `"fill"`, `"inside"`, `"outside"`
- `format` - `"webp"`, `"avif"`, `"jpg"`, `"png"`
- `quality` - Image quality (0-100)
- `provider` - Image provider to use

### NuxtPicture

Responsive image with multiple formats:

```vue
<template>
  <NuxtPicture
    src="/images/hero.jpg"
    :img-attrs="{ alt: 'Hero image', class: 'rounded-lg' }"
    sizes="sm:100vw md:50vw lg:400px"
  />
</template>
```

**Benefits:**

- Automatically generates multiple formats (WebP, AVIF)
- Creates responsive srcset for different screen sizes
- Better browser compatibility with fallbacks

## Common Patterns

### Responsive Images

```vue
<template>
  <NuxtPicture
    src="/images/product.jpg"
    :img-attrs="{ alt: 'Product image' }"
    sizes="xs:100vw sm:100vw md:50vw lg:33vw"
    :modifiers="{ fit: 'cover' }"
  />
</template>
```

### Image with Loading States

```vue
<template>
  <div class="relative">
    <NuxtImg
      src="/images/large.jpg"
      alt="Large image"
      loading="lazy"
      placeholder
      @load="imageLoaded = true"
    />
    <div
      v-if="!imageLoaded"
      class="absolute inset-0 bg-gray-200 animate-pulse"
    />
  </div>
</template>

<script setup lang="ts">
const imageLoaded = ref(false)
</script>
```

### Background Images

```vue
<template>
  <div
    :style="{
      backgroundImage: `url(${$img('/images/hero.jpg', { width: 1920, height: 1080 })})`,
      backgroundSize: 'cover',
    }"
    class="h-96"
  >
    Content
  </div>
</template>
```

### Image with Different Formats

```vue
<template>
  <NuxtPicture
    src="/images/photo.jpg"
    format="webp"
    :img-attrs="{ alt: 'Photo', class: 'w-full' }"
  />
</template>
```

### Fit Options

```vue
<template>
  <div class="grid grid-cols-3 gap-4">
    <!-- Cover: Crop to fill dimensions -->
    <NuxtImg
      src="/images/photo.jpg"
      fit="cover"
      width="300"
      height="300"
      alt="Cover"
    />

    <!-- Contain: Fit within dimensions -->
    <NuxtImg
      src="/images/photo.jpg"
      fit="contain"
      width="300"
      height="300"
      alt="Contain"
    />

    <!-- Fill: Stretch to fill -->
    <NuxtImg
      src="/images/photo.jpg"
      fit="fill"
      width="300"
      height="300"
      alt="Fill"
    />
  </div>
</template>
```

## Image Providers

### Local Provider (Default)

For images in `public/` directory:

```vue
<template>
  <NuxtImg src="/images/local.jpg" />
</template>
```

### External URLs

```vue
<template>
  <NuxtImg src="https://example.com/image.jpg" provider="cloudinary" />
</template>
```

### Cloudinary

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  image: {
    cloudinary: {
      baseURL: "https://res.cloudinary.com/{your-cloud-name}/image/upload/",
    },
  },
})
```

```vue
<template>
  <NuxtImg provider="cloudinary" src="sample.jpg" width="600" height="400" />
</template>
```

### Vercel / Netlify

Automatically detected and configured when deployed:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  image: {
    provider: "vercel", // or 'netlify'
  },
})
```

### Custom Provider

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  image: {
    providers: {
      custom: {
        provider: "~/providers/custom-provider.ts",
        options: {
          baseURL: "https://cdn.example.com",
        },
      },
    },
  },
})
```

```typescript
// providers/custom-provider.ts
import { joinURL } from "ufo"
import type { ProviderGetImage } from "@nuxt/image"

export const getImage: ProviderGetImage = (src, { modifiers, baseURL }) => {
  const { width, height, format, quality } = modifiers
  const url = joinURL(baseURL, src)

  return {
    url: `${url}?w=${width}&h=${height}&fm=${format}&q=${quality}`,
  }
}
```

### Other Providers

25+ providers available including: AWS Amplify, Bunny, Cloudflare, Contentful, Directus, GitHub, ImageKit, Imgix, Sanity, Shopify, Strapi, Supabase, Twicpics, Uploadcare.

See full list: https://image.nuxt.com/providers

## Composables

### useImage (Recommended)

Generate image URLs programmatically:

```vue
<script setup lang="ts">
const img = useImage()

// Generate optimized URL
const imageUrl = img("/images/photo.jpg", {
  width: 800,
  height: 600,
  format: "webp",
  quality: 80,
})

// Use in v-bind or computed
const backgroundImage = computed(() => img("/images/hero.jpg", { width: 1920 }))
</script>

<template>
  <div :style="{ backgroundImage: `url(${backgroundImage})` }">Content</div>
</template>
```

### $img Helper (Legacy)

Alternative via `useNuxtApp()`:

```vue
<script setup lang="ts">
const { $img } = useNuxtApp()
const imageUrl = $img("/images/photo.jpg", { width: 800 })
</script>
```

## Performance Optimization

### Lazy Loading (Default)

Images are lazy-loaded by default:

```vue
<template>
  <!-- Lazy loaded (default) -->
  <NuxtImg src="/images/photo.jpg" loading="lazy" />

  <!-- Eager load for above-the-fold images -->
  <NuxtImg src="/images/hero.jpg" loading="eager" />
</template>
```

### Preload Critical Images

```vue
<script setup lang="ts">
useHead({
  link: [
    {
      rel: "preload",
      as: "image",
      href: "/images/hero.jpg",
      type: "image/jpeg",
    },
  ],
})
</script>

<template>
  <NuxtImg src="/images/hero.jpg" loading="eager" />
</template>
```

### Placeholder / Blur

```vue
<template>
  <NuxtImg
    src="/images/large.jpg"
    placeholder
    alt="Image with blur placeholder"
  />
</template>
```

### Image Sizes

Specify responsive sizes for optimal loading:

```vue
<template>
  <NuxtPicture
    src="/images/responsive.jpg"
    sizes="xs:100vw sm:100vw md:50vw lg:400px xl:400px"
    :img-attrs="{ alt: 'Responsive image' }"
  />
</template>
```

## Advanced Usage

### Modifiers Object

Pass multiple modifiers:

```vue
<script setup lang="ts">
const imageModifiers = {
  width: 800,
  height: 600,
  fit: "cover",
  format: "webp",
  quality: 85,
}
</script>

<template>
  <NuxtImg src="/images/photo.jpg" :modifiers="imageModifiers" alt="Photo" />
</template>
```

### Dynamic Sources

```vue
<script setup lang="ts">
const images = ref([
  { id: 1, src: "/images/photo1.jpg", alt: "Photo 1" },
  { id: 2, src: "/images/photo2.jpg", alt: "Photo 2" },
  { id: 3, src: "/images/photo3.jpg", alt: "Photo 3" },
])
</script>

<template>
  <div class="grid grid-cols-3 gap-4">
    <NuxtImg
      v-for="image of images"
      :key="image.id"
      :src="image.src"
      :alt="image.alt"
      width="400"
      height="300"
      fit="cover"
    />
  </div>
</template>
```

### Image Gallery

```vue
<template>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    <NuxtPicture
      v-for="(image, index) of gallery"
      :key="index"
      :src="image.src"
      :img-attrs="{
        alt: image.alt,
        class: 'w-full h-64 object-cover rounded-lg cursor-pointer',
      }"
      sizes="sm:50vw md:33vw lg:25vw"
      @click="openLightbox(image)"
    />
  </div>
</template>

<script setup lang="ts">
const gallery = ref([
  { src: "/images/gallery1.jpg", alt: "Gallery 1" },
  { src: "/images/gallery2.jpg", alt: "Gallery 2" },
  { src: "/images/gallery3.jpg", alt: "Gallery 3" },
])

function openLightbox(image: any) {
  // Handle lightbox
}
</script>
```

### Art Direction

Different images for different screen sizes:

```vue
<template>
  <picture>
    <source
      media="(min-width: 1024px)"
      :srcset="$img('/images/hero-desktop.jpg', { width: 1920 })"
    />
    <source
      media="(min-width: 768px)"
      :srcset="$img('/images/hero-tablet.jpg', { width: 1024 })"
    />
    <NuxtImg src="/images/hero-mobile.jpg" alt="Hero" width="768" />
  </picture>
</template>
```

## Configuration Reference

### Global Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  image: {
    // Default quality
    quality: 80,

    // Default formats
    formats: ["webp", "avif", "jpg"],

    // Image sizes for responsive images
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536,
      "2xl": 1536,
    },

    // Provider configuration
    provider: "cloudinary",
    providers: {
      cloudinary: {
        baseURL: "https://res.cloudinary.com/{cloud-name}/image/upload/",
      },
    },

    // IPX options (local provider)
    ipx: {
      maxAge: 60 * 60 * 24 * 365, // 1 year cache
    },

    // Presets
    presets: {
      avatar: {
        modifiers: {
          format: "webp",
          width: 100,
          height: 100,
          fit: "cover",
        },
      },
      thumbnail: {
        modifiers: {
          format: "webp",
          width: 300,
          height: 200,
          fit: "cover",
        },
      },
    },
  },
})
```

### Using Presets

```vue
<template>
  <NuxtImg src="/images/user.jpg" preset="avatar" alt="User avatar" />

  <NuxtImg
    src="/images/product.jpg"
    preset="thumbnail"
    alt="Product thumbnail"
  />
</template>
```

## Best Practices

1. **Include alt text** - Essential for accessibility
2. **Use NuxtPicture for hero images** - Better format support and responsiveness
3. **Specify dimensions** - Prevents layout shift
4. **Lazy load by default** - Except above-the-fold images
5. **Use appropriate fit** - `cover` for thumbnails, `contain` for products
6. **Optimize quality** - 80-85 is usually sufficient
7. **Leverage providers** - Use CDN providers for external images
8. **Use presets** - Define common image styles once
9. **Test on slow networks** - Verify lazy loading and placeholders work
10. **Prefer WebP/AVIF** - Modern formats for better compression

## Troubleshooting

### Images Not Optimizing

Check:

1. `@nuxt/image` is in `nuxt.config.ts` modules
2. Images are in `public/` directory for local provider
3. Provider is correctly configured
4. Development server was restarted after config changes

### Images Not Loading

1. Verify src path is correct
2. Check provider baseURL configuration
3. Ensure CORS is configured for external images
4. Check network tab for 404/403 errors

### Poor Performance

1. Enable lazy loading (default)
2. Use appropriate image sizes
3. Implement placeholders
4. Use WebP/AVIF formats
5. Configure CDN caching

### Layout Shift

Specify width and height:

```vue
<template>
  <!-- Bad: No dimensions -->
  <NuxtImg src="/images/photo.jpg" />

  <!-- Good: Dimensions specified -->
  <NuxtImg src="/images/photo.jpg" width="800" height="600" />
</template>
```

## Official Resources

- **Documentation:** https://image.nuxt.com
- **Providers:** https://image.nuxt.com/providers
- **API Reference:** https://image.nuxt.com/api
- **GitHub:** https://github.com/nuxt/image

---

**Note:** Verify provider-specific features with official documentation. Image optimization strategies may vary by provider.
