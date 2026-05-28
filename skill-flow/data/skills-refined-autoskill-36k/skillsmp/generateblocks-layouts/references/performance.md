# GenerateBlocks Performance Skill

Optimize GenerateBlocks output for speed, efficient CSS delivery, and minimal overhead.

## When to Use This Skill

- Optimizing CSS loading and delivery
- Reducing render-blocking resources
- Implementing critical CSS strategies
- Debugging performance issues with GenerateBlocks

## Performance Overview

GenerateBlocks performance factors:

1. **CSS Generation** - How styles are compiled and delivered
2. **Block Rendering** - Server-side vs client-side rendering
3. **Asset Loading** - JavaScript and CSS file management
4. **DOM Complexity** - Nesting depth and element count

## CSS Delivery Strategies

### 1. Inline CSS (Default)

GenerateBlocks inlines CSS in the `<head>`:

```html
<style id="generateblocks-inline-css">
.gb-element-abc123{display:flex;gap:1rem}
.gb-text-def456{font-size:1.25rem}
</style>
```

**Pros:**
- No extra HTTP request
- Styles available immediately
- Good for small amounts of CSS

**Cons:**
- Not cached separately
- Increases HTML size
- Repeated on every page

### 2. External CSS File

Configure GenerateBlocks to output external CSS:

```php
<?php
// In theme or plugin
add_filter( 'generateblocks_use_external_css', '__return_true' );
```

**Pros:**
- Browser caching
- Smaller HTML
- Single file for multiple pages

**Cons:**
- Extra HTTP request
- Potential FOUC

### 3. Hybrid Approach

Critical CSS inline, rest external:

```php
<?php
add_filter( 'generateblocks_css_output', function( $css, $context ) {
    // Inline above-the-fold CSS
    if ( $context === 'above-fold' ) {
        return $css;
    }

    // Defer below-fold CSS
    return '';
}, 10, 2 );
```

## CSS Optimization

### Minification

GenerateBlocks minifies CSS by default. Verify with:

```php
<?php
// Should be enabled by default
add_filter( 'generateblocks_minify_css', '__return_true' );
```

### Deduplication

GenerateBlocks deduplicates identical styles. When creating blocks:

```html
<!-- These will share CSS if styles are identical -->
<!-- wp:generateblocks/element {"uniqueId":"card001","styles":{"padding":"2rem","backgroundColor":"#ffffff"}} -->
<!-- wp:generateblocks/element {"uniqueId":"card002","styles":{"padding":"2rem","backgroundColor":"#ffffff"}} -->
```

### Remove Unused CSS

For inline styles approach, CSS is already scoped. For external:

```php
<?php
// Remove GenerateBlocks CSS on pages without GB blocks
add_action( 'wp_enqueue_scripts', function() {
    if ( ! has_block( 'generateblocks/' ) ) {
        wp_dequeue_style( 'generateblocks' );
    }
}, 100 );
```

### Combine Similar Styles

Use global classes for repeated patterns:

```html
<!-- Instead of repeating styles -->
<!-- wp:generateblocks/element {"uniqueId":"a1","styles":{"padding":"2rem","borderRadius":"1rem","backgroundColor":"#fff"}} -->
<!-- wp:generateblocks/element {"uniqueId":"a2","styles":{"padding":"2rem","borderRadius":"1rem","backgroundColor":"#fff"}} -->

<!-- Use global classes -->
<!-- wp:generateblocks/element {"uniqueId":"a1","globalClasses":["card-base"]} -->
<!-- wp:generateblocks/element {"uniqueId":"a2","globalClasses":["card-base"]} -->
```

## Asset Loading

### Defer Non-Critical JavaScript

```php
<?php
add_filter( 'script_loader_tag', function( $tag, $handle ) {
    $defer_scripts = array(
        'generateblocks-frontend',
    );

    if ( in_array( $handle, $defer_scripts ) ) {
        return str_replace( ' src', ' defer src', $tag );
    }

    return $tag;
}, 10, 2 );
```

### Conditional Loading

```php
<?php
// Only load GB assets when blocks are present
add_action( 'wp_enqueue_scripts', function() {
    global $post;

    if ( ! $post || ! has_blocks( $post->post_content ) ) {
        return;
    }

    // Check for specific GB blocks
    $gb_blocks = array(
        'generateblocks/element',
        'generateblocks/text',
        'generateblocks/media',
        'generateblocks/shape',
    );

    $has_gb_block = false;
    foreach ( $gb_blocks as $block ) {
        if ( has_block( $block, $post ) ) {
            $has_gb_block = true;
            break;
        }
    }

    if ( ! $has_gb_block ) {
        wp_dequeue_style( 'generateblocks' );
        wp_dequeue_script( 'generateblocks-frontend' );
    }
}, 100 );
```

### Lazy Load JavaScript

For interactive components:

```php
<?php
// Use Intersection Observer for below-fold interactivity
add_filter( 'generateblocks_frontend_script_strategy', function() {
    return 'defer'; // or 'async'
} );
```

## DOM Optimization

### Minimize Nesting

```html
<!-- Avoid excessive nesting -->
<!-- Bad: 5 levels deep -->
<section>
    <div>
        <div>
            <div>
                <p>Content</p>
            </div>
        </div>
    </div>
</section>

<!-- Good: 2 levels -->
<section>
    <p>Content</p>
</section>
```

### Reduce Block Count

Combine elements where possible:

```html
<!-- Instead of separate blocks for each element -->
<!-- wp:generateblocks/element -->
    <!-- wp:generateblocks/element -->
        <!-- wp:generateblocks/text -->
    <!-- /wp:generateblocks/element -->
<!-- /wp:generateblocks/element -->

<!-- Use flexbox/grid on parent -->
<!-- wp:generateblocks/element {"styles":{"display":"flex","gap":"1rem"}} -->
    <!-- wp:generateblocks/text -->
    <!-- wp:generateblocks/text -->
<!-- /wp:generateblocks/element -->
```

### Use Semantic Elements

Semantic elements reduce the need for wrapper divs:

```html
<!-- Good: semantic tags -->
<section>
    <article>
        <header>
            <h2>Title</h2>
        </header>
        <p>Content</p>
    </article>
</section>

<!-- Avoid: div soup -->
<div class="section">
    <div class="article">
        <div class="header">
            <div class="title">Title</div>
        </div>
        <div class="content">Content</div>
    </div>
</div>
```

## Image Optimization

### Lazy Loading

```html
<!-- wp:generateblocks/media {"htmlAttributes":[{"attribute":"loading","value":"lazy"},{"attribute":"decoding","value":"async"}]} -->
<img loading="lazy" decoding="async" ... />
<!-- /wp:generateblocks/media -->
```

### Responsive Images

```html
<!-- wp:generateblocks/media {"htmlAttributes":[{"attribute":"srcset","value":"img-400.jpg 400w, img-800.jpg 800w"},{"attribute":"sizes","value":"(max-width: 600px) 100vw, 50vw"}]} -->
<img srcset="img-400.jpg 400w, img-800.jpg 800w" sizes="(max-width: 600px) 100vw, 50vw" ... />
<!-- /wp:generateblocks/media -->
```

### WebP with Fallback

```php
<?php
// Serve WebP when supported
add_filter( 'generateblocks_image_attributes', function( $attributes ) {
    if ( isset( $attributes['src'] ) ) {
        $webp_url = preg_replace( '/\.(jpg|jpeg|png)$/i', '.webp', $attributes['src'] );

        // Check if WebP exists
        if ( file_exists( str_replace( site_url(), ABSPATH, $webp_url ) ) ) {
            $attributes['src'] = $webp_url;
        }
    }

    return $attributes;
} );
```

### Background Images

For CSS background images, use modern formats:

```css
.hero-bg {
    background-image: url('hero.webp');
}

/* Fallback for older browsers */
@supports not (background-image: url('test.webp')) {
    .hero-bg {
        background-image: url('hero.jpg');
    }
}
```

## Caching Strategies

### Page Cache Compatibility

Ensure GenerateBlocks works with caching:

```php
<?php
// CSS is page-specific, but patterns are cacheable
add_filter( 'generateblocks_css_cache_key', function( $key ) {
    // Add cache busting for dynamic content
    if ( is_singular() ) {
        $key .= '_' . get_the_modified_time( 'U' );
    }

    return $key;
} );
```

### Object Caching

Use object cache for computed styles:

```php
<?php
add_filter( 'generateblocks_get_computed_css', function( $css, $block_id ) {
    $cache_key = 'gb_css_' . $block_id;
    $cached = wp_cache_get( $cache_key, 'generateblocks' );

    if ( false !== $cached ) {
        return $cached;
    }

    // Compute CSS...
    wp_cache_set( $cache_key, $css, 'generateblocks', HOUR_IN_SECONDS );

    return $css;
}, 10, 2 );
```

### CDN Configuration

For external CSS:

```php
<?php
add_filter( 'generateblocks_css_url', function( $url ) {
    // Rewrite to CDN
    return str_replace(
        'https://example.com',
        'https://cdn.example.com',
        $url
    );
} );
```

## Critical CSS

### Extract Above-Fold Styles

```php
<?php
/**
 * Output critical CSS inline, defer the rest
 */
function theme_critical_css() {
    // Define critical selectors
    $critical_selectors = array(
        '.gb-element-hero',
        '.gb-text-hero',
        '.gb-element-nav',
        // Add above-fold elements
    );

    $all_css = generateblocks_get_all_css();
    $critical_css = '';
    $deferred_css = '';

    foreach ( explode( '}', $all_css ) as $rule ) {
        $is_critical = false;

        foreach ( $critical_selectors as $selector ) {
            if ( strpos( $rule, $selector ) !== false ) {
                $is_critical = true;
                break;
            }
        }

        if ( $is_critical ) {
            $critical_css .= $rule . '}';
        } else {
            $deferred_css .= $rule . '}';
        }
    }

    // Inline critical CSS
    echo '<style id="critical-css">' . $critical_css . '</style>';

    // Defer non-critical CSS
    echo '<link rel="preload" href="' . esc_url( get_deferred_css_url() ) . '" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">';
}
add_action( 'wp_head', 'theme_critical_css', 1 );
```

## Performance Monitoring

### Core Web Vitals

Monitor these metrics:

| Metric | Target | Impact |
|--------|--------|--------|
| LCP (Largest Contentful Paint) | < 2.5s | Hero images, above-fold content |
| FID (First Input Delay) | < 100ms | JavaScript execution |
| CLS (Cumulative Layout Shift) | < 0.1 | Avoid layout shifts |
| INP (Interaction to Next Paint) | < 200ms | Interactivity responsiveness |

### LCP Optimization

```html
<!-- Preload hero image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- Inline critical hero CSS -->
<style>
.gb-element-hero{min-height:80vh;display:flex;align-items:center}
</style>

<!-- Hero block -->
<!-- wp:generateblocks/element {"uniqueId":"hero001"} -->
```

### CLS Prevention

```html
<!-- Reserve space for images -->
<!-- wp:generateblocks/media {"styles":{"aspectRatio":"16/9","width":"100%"}} -->
<img style="aspect-ratio:16/9;width:100%" ... />
<!-- /wp:generateblocks/media -->

<!-- Define container dimensions -->
<!-- wp:generateblocks/element {"styles":{"minHeight":"400px"}} -->
```

### Debug Performance

```php
<?php
// Add timing markers
add_action( 'wp_head', function() {
    echo '<!-- GB CSS Start: ' . microtime( true ) . ' -->';
}, 0 );

add_action( 'wp_head', function() {
    echo '<!-- GB CSS End: ' . microtime( true ) . ' -->';
}, 100 );

// Log CSS size
add_filter( 'generateblocks_css_output', function( $css ) {
    error_log( 'GenerateBlocks CSS size: ' . strlen( $css ) . ' bytes' );
    return $css;
} );
```

## Build Optimization

### Production Build

For GenerateBlocks development:

```bash
# Production build (minified)
cd generateblocks
npm run build

# Check bundle sizes
npm run build -- --stats
```

### Tree Shaking

Ensure unused code is eliminated:

```javascript
// Only import what you need
import { element } from '@wordpress/element';
// Not: import * as wp from '@wordpress';
```

## Query Optimization

### Reduce Database Queries

```php
<?php
// Cache global classes
add_filter( 'generateblocks_get_global_classes', function( $classes ) {
    $cached = get_transient( 'gb_global_classes' );

    if ( false !== $cached ) {
        return $cached;
    }

    // ... get classes
    set_transient( 'gb_global_classes', $classes, DAY_IN_SECONDS );

    return $classes;
} );

// Clear cache on update
add_action( 'generateblocks_global_classes_updated', function() {
    delete_transient( 'gb_global_classes' );
} );
```

### Batch Meta Queries

```php
<?php
// Prime post meta cache for query loops
add_action( 'generateblocks_before_query_loop', function( $posts ) {
    $post_ids = wp_list_pluck( $posts, 'ID' );
    update_meta_cache( 'post', $post_ids );
} );
```

## Best Practices

### 1. Audit Regularly

Use tools to check performance:
- Lighthouse
- WebPageTest
- Query Monitor (WordPress plugin)

### 2. Set Performance Budgets

| Resource | Budget |
|----------|--------|
| Total CSS | < 50KB |
| Above-fold CSS | < 15KB |
| JavaScript | < 100KB |
| Total page weight | < 1MB |

### 3. Progressive Enhancement

```html
<!-- Base experience works without JS -->
<!-- wp:generateblocks/element {"tagName":"details"} -->
<details>
    <summary>Expand</summary>
    Content
</details>
<!-- /wp:generateblocks/element -->
```

### 4. Avoid Layout Thrashing

```css
/* Use transform instead of changing layout properties */
.card:hover {
    transform: translateY(-4px); /* Good */
    /* margin-top: -4px; */      /* Avoid */
}
```

### 5. Optimize for Repeat Visits

```php
<?php
// Set long cache headers for static assets
add_filter( 'generateblocks_asset_cache_time', function() {
    return YEAR_IN_SECONDS;
} );
```

## Troubleshooting

### Slow Page Load

1. Check CSS file size
2. Look for render-blocking resources
3. Analyze with Chrome DevTools Performance tab
4. Check for excessive DOM depth

### High CLS Score

1. Add dimensions to images
2. Reserve space for dynamic content
3. Avoid inserting content above existing content
4. Use transform for animations

### JavaScript Errors

1. Check console for errors
2. Verify all dependencies are loaded
3. Test without other plugins
4. Check for conflicts with caching

### CSS Not Loading

1. Verify GenerateBlocks is active
2. Check for caching plugin conflicts
3. Clear all caches
4. Check browser console for 404s
