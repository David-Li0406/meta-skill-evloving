# GenerateBlocks Dynamic Content Skill

Work with dynamic tags and content in GenerateBlocks Pro for data-driven layouts.

## When to Use This Skill

- Displaying post meta, author info, dates, taxonomies
- Building dynamic templates with live data
- Integrating ACF/custom fields with GenerateBlocks
- Creating reusable dynamic components

## Dynamic Content Overview

GenerateBlocks Pro provides dynamic tags that pull content from:
- Post data (title, content, excerpt, date)
- Post meta (custom fields)
- Author information
- Taxonomies (categories, tags)
- Site data (site title, URL)
- User data
- ACF fields (with ACF plugin)

## Dynamic Tag Syntax

### Basic Syntax

```
{{tag_name}}
{{tag_name attribute="value"}}
{{tag_name attribute="value" another="value"}}
```

### In Block Attributes

Dynamic tags can be used in:
- Text content
- HTML attributes (href, src, alt)
- CSS values
- Conditional display

## Core Dynamic Tags

### Post Tags

| Tag | Description | Example Output |
|-----|-------------|----------------|
| `{{post_title}}` | Post title | "My Blog Post" |
| `{{post_content}}` | Full post content | HTML content |
| `{{post_excerpt}}` | Post excerpt | "This is..." |
| `{{post_date}}` | Publication date | "January 1, 2024" |
| `{{post_modified_date}}` | Modified date | "January 5, 2024" |
| `{{post_id}}` | Post ID | "123" |
| `{{post_url}}` | Post permalink | "https://..." |
| `{{post_slug}}` | Post slug | "my-blog-post" |
| `{{post_type}}` | Post type | "post" |
| `{{post_status}}` | Post status | "publish" |

### Date Formatting

```
{{post_date format="F j, Y"}}        → January 1, 2024
{{post_date format="Y-m-d"}}         → 2024-01-01
{{post_date format="M j"}}           → Jan 1
{{post_date format="l"}}             → Monday
{{post_modified_date format="F Y"}}  → January 2024
```

### Author Tags

| Tag | Description |
|-----|-------------|
| `{{author_name}}` | Display name |
| `{{author_first_name}}` | First name |
| `{{author_last_name}}` | Last name |
| `{{author_email}}` | Email address |
| `{{author_url}}` | Author website |
| `{{author_description}}` | Bio/description |
| `{{author_avatar}}` | Avatar URL |
| `{{author_posts_url}}` | Author archive URL |
| `{{author_id}}` | Author user ID |

### Avatar with Size

```
{{author_avatar size="96"}}   → 96x96 avatar URL
{{author_avatar size="150"}}  → 150x150 avatar URL
```

### Taxonomy Tags

```
{{post_terms taxonomy="category"}}
{{post_terms taxonomy="post_tag"}}
{{post_terms taxonomy="custom_taxonomy"}}
{{post_terms taxonomy="category" separator=", "}}
{{post_terms taxonomy="category" link="true"}}
```

### Featured Image Tags

| Tag | Description |
|-----|-------------|
| `{{featured_image}}` | Full image URL |
| `{{featured_image size="medium"}}` | Specific size URL |
| `{{featured_image_id}}` | Attachment ID |
| `{{featured_image_alt}}` | Alt text |
| `{{featured_image_caption}}` | Caption |
| `{{featured_image_title}}` | Image title |

### Image Sizes

```
{{featured_image size="thumbnail"}}   → 150x150
{{featured_image size="medium"}}      → 300x300
{{featured_image size="large"}}       → 1024x1024
{{featured_image size="full"}}        → Original size
{{featured_image size="custom-size"}} → Custom registered size
```

### Site Tags

| Tag | Description |
|-----|-------------|
| `{{site_title}}` | Site name |
| `{{site_tagline}}` | Site description |
| `{{site_url}}` | Site URL |
| `{{home_url}}` | Home URL |
| `{{current_year}}` | Current year |
| `{{current_date}}` | Current date |

### Comments Tags

| Tag | Description |
|-----|-------------|
| `{{comments_number}}` | Comment count |
| `{{comments_url}}` | Comments link |

## Post Meta / Custom Fields

### Basic Meta

```
{{post_meta key="custom_field_name"}}
{{post_meta key="price"}}
{{post_meta key="_custom_field"}}  → Private meta
```

### With Default Value

```
{{post_meta key="price" default="Contact for pricing"}}
```

### ACF Fields

GenerateBlocks Pro integrates with Advanced Custom Fields:

```
{{acf field="field_name"}}
{{acf field="text_field"}}
{{acf field="image_field"}}         → Returns image URL
{{acf field="image_field" size="medium"}}
{{acf field="repeater_field"}}      → Returns count
```

### ACF Field Types

| Field Type | Output |
|------------|--------|
| Text, Textarea | String value |
| Number | Numeric value |
| Email | Email string |
| URL | URL string |
| Image | Image URL (or array) |
| File | File URL |
| Select, Radio | Selected value |
| Checkbox | Comma-separated values |
| True/False | 1 or 0 |
| Date Picker | Formatted date |
| Color Picker | Hex color |
| Link | URL or array |

### ACF Image Field

```
{{acf field="hero_image"}}                    → Full URL
{{acf field="hero_image" size="large"}}       → Large size URL
{{acf field="hero_image" return="id"}}        → Attachment ID
{{acf field="hero_image" return="alt"}}       → Alt text
```

### ACF Repeater Access

For repeater fields, use within query context:

```
{{acf field="repeater_field" index="0" sub_field="title"}}
```

## Usage in Blocks

### Dynamic Text Content

```html
<!-- wp:generateblocks/text {"uniqueId":"dyn001","tagName":"h1","useDynamicData":true,"dynamicContentType":"post-title"} -->
<h1 class="gb-text gb-text-dyn001">{{post_title}}</h1>
<!-- /wp:generateblocks/text -->
```

### Dynamic Link

```html
<!-- wp:generateblocks/text {"uniqueId":"dyn002","tagName":"a","htmlAttributes":[{"attribute":"href","value":"{{post_url}}"}],"useDynamicData":true} -->
<a class="gb-text gb-text-dyn002" href="{{post_url}}">Read More</a>
<!-- /wp:generateblocks/text -->
```

### Dynamic Image

```html
<!-- wp:generateblocks/media {"uniqueId":"dyn003","useDynamicData":true,"htmlAttributes":[{"attribute":"src","value":"{{featured_image size=\"large\"}}"},{"attribute":"alt","value":"{{featured_image_alt}}"}]} -->
<img class="gb-media gb-media-dyn003" src="{{featured_image size='large'}}" alt="{{featured_image_alt}}" />
<!-- /wp:generateblocks/media -->
```

### Dynamic Background Image

```html
<!-- wp:generateblocks/element {"uniqueId":"dyn004","tagName":"div","styles":{"backgroundImage":"url({{featured_image size='large'}})","backgroundSize":"cover","backgroundPosition":"center"},"css":".gb-element-dyn004{background-image:url({{featured_image size='large'}});background-size:cover;background-position:center}"} -->
<div class="gb-element gb-element-dyn004">
    <!-- Content -->
</div>
<!-- /wp:generateblocks/element -->
```

## Conditional Display

### Show/Hide Based on Content

```html
<!-- wp:generateblocks/element {"uniqueId":"cond001","tagName":"div","showIf":"{{post_meta key='show_banner'}}"} -->
<div class="gb-element gb-element-cond001">
    <!-- Only shows if show_banner meta is truthy -->
</div>
<!-- /wp:generateblocks/element -->
```

### Conditional Operators

```
{{post_meta key="price"}}              → Show if has value
{{post_meta key="featured" value="1"}} → Show if equals "1"
```

## Dynamic Content Patterns

### Author Box

```html
<!-- wp:generateblocks/element {"uniqueId":"auth001","tagName":"div","styles":{"display":"flex","gap":"1.5rem","padding":"2rem","backgroundColor":"#f8f9fa","borderRadius":"1rem"},"css":".gb-element-auth001{display:flex;gap:1.5rem;padding:2rem;background-color:#f8f9fa;border-radius:1rem}@media(max-width:768px){.gb-element-auth001{flex-direction:column;text-align:center}}"} -->
<div class="gb-element gb-element-auth001">

    <!-- wp:generateblocks/media {"uniqueId":"auth002","useDynamicData":true,"htmlAttributes":[{"attribute":"src","value":"{{author_avatar size='96'}}"},{"attribute":"alt","value":"{{author_name}}"}],"styles":{"width":"96px","height":"96px","borderRadius":"50%","objectFit":"cover"},"css":".gb-media-auth002{width:96px;height:96px;border-radius:50%;object-fit:cover}"} -->
    <img class="gb-media gb-media-auth002" src="{{author_avatar size='96'}}" alt="{{author_name}}" />
    <!-- /wp:generateblocks/media -->

    <!-- wp:generateblocks/element {"uniqueId":"auth003","tagName":"div","styles":{"flex":"1"},"css":".gb-element-auth003{flex:1}"} -->
    <div class="gb-element gb-element-auth003">

        <!-- wp:generateblocks/text {"uniqueId":"auth004","tagName":"p","styles":{"fontSize":"0.875rem","color":"#666","marginBottom":"0.25rem"},"css":".gb-text-auth004{font-size:0.875rem;color:#666;margin-bottom:0.25rem}"} -->
        <p class="gb-text gb-text-auth004">Written by</p>
        <!-- /wp:generateblocks/text -->

        <!-- wp:generateblocks/text {"uniqueId":"auth005","tagName":"h3","useDynamicData":true,"dynamicContentType":"author-name","styles":{"fontSize":"1.25rem","fontWeight":"700","marginBottom":"0.5rem"},"css":".gb-text-auth005{font-size:1.25rem;font-weight:700;margin-bottom:0.5rem}"} -->
        <h3 class="gb-text gb-text-auth005">{{author_name}}</h3>
        <!-- /wp:generateblocks/text -->

        <!-- wp:generateblocks/text {"uniqueId":"auth006","tagName":"p","useDynamicData":true,"dynamicContentType":"author-description","styles":{"color":"#444","lineHeight":"1.6"},"css":".gb-text-auth006{color:#444;line-height:1.6}"} -->
        <p class="gb-text gb-text-auth006">{{author_description}}</p>
        <!-- /wp:generateblocks/text -->

    </div>
    <!-- /wp:generateblocks/element -->

</div>
<!-- /wp:generateblocks/element -->
```

### Post Meta Display

```html
<!-- wp:generateblocks/element {"uniqueId":"meta001","tagName":"div","styles":{"display":"flex","gap":"1rem","flexWrap":"wrap","fontSize":"0.875rem","color":"#666"},"css":".gb-element-meta001{display:flex;gap:1rem;flex-wrap:wrap;font-size:0.875rem;color:#666}"} -->
<div class="gb-element gb-element-meta001">

    <!-- wp:generateblocks/text {"uniqueId":"meta002","tagName":"span","useDynamicData":true} -->
    <span class="gb-text">{{post_date format="F j, Y"}}</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"meta003","tagName":"span"} -->
    <span class="gb-text">•</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"meta004","tagName":"span","useDynamicData":true} -->
    <span class="gb-text">{{post_terms taxonomy="category" separator=", "}}</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"meta005","tagName":"span"} -->
    <span class="gb-text">•</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"meta006","tagName":"span","useDynamicData":true} -->
    <span class="gb-text">{{comments_number}} comments</span>
    <!-- /wp:generateblocks/text -->

</div>
<!-- /wp:generateblocks/element -->
```

### Price Display with ACF

```html
<!-- wp:generateblocks/element {"uniqueId":"price001","tagName":"div","styles":{"display":"flex","alignItems":"baseline","gap":"0.5rem"},"css":".gb-element-price001{display:flex;align-items:baseline;gap:0.5rem}"} -->
<div class="gb-element gb-element-price001">

    <!-- wp:generateblocks/text {"uniqueId":"price002","tagName":"span","styles":{"fontSize":"0.875rem","color":"#666"},"css":".gb-text-price002{font-size:0.875rem;color:#666}"} -->
    <span class="gb-text gb-text-price002">Starting at</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"price003","tagName":"span","useDynamicData":true,"styles":{"fontSize":"2rem","fontWeight":"700","color":"#0a0a0a"},"css":".gb-text-price003{font-size:2rem;font-weight:700;color:#0a0a0a}"} -->
    <span class="gb-text gb-text-price003">${{acf field="price"}}</span>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"price004","tagName":"span","styles":{"fontSize":"0.875rem","color":"#666"},"css":".gb-text-price004{font-size:0.875rem;color:#666}"} -->
    <span class="gb-text gb-text-price004">/month</span>
    <!-- /wp:generateblocks/text -->

</div>
<!-- /wp:generateblocks/element -->
```

### Dynamic CTA with Custom Field Link

```html
<!-- wp:generateblocks/text {"uniqueId":"cta001","tagName":"a","useDynamicData":true,"htmlAttributes":[{"attribute":"href","value":"{{acf field='cta_link'}}"},{"attribute":"target","value":"_blank"},{"attribute":"rel","value":"noopener"}],"styles":{"display":"inline-flex","padding":"1rem 2rem","backgroundColor":"#e94560","color":"#ffffff","borderRadius":"0.5rem","textDecoration":"none","fontWeight":"600"},"css":".gb-text-cta001{display:inline-flex;padding:1rem 2rem;background-color:#e94560;color:#ffffff;border-radius:0.5rem;text-decoration:none;font-weight:600;transition:all 0.3s}.gb-text-cta001:hover{background-color:#d63850;transform:translateY(-2px)}"} -->
<a class="gb-text gb-text-cta001" href="{{acf field='cta_link'}}" target="_blank" rel="noopener">{{acf field="cta_text" default="Learn More"}}</a>
<!-- /wp:generateblocks/text -->
```

## Custom Dynamic Tag Registration

### Register Custom Tag in PHP

```php
<?php
/**
 * Register custom dynamic tag
 */
function theme_register_dynamic_tags( $tags ) {
    // Add reading time tag
    $tags['reading_time'] = array(
        'label'    => __( 'Reading Time', 'theme' ),
        'group'    => 'post',
        'callback' => 'theme_reading_time_callback',
    );

    // Add custom meta tag
    $tags['product_sku'] = array(
        'label'    => __( 'Product SKU', 'theme' ),
        'group'    => 'post-meta',
        'callback' => 'theme_product_sku_callback',
    );

    return $tags;
}
add_filter( 'generateblocks_dynamic_tags', 'theme_register_dynamic_tags' );
```

### Tag Callback Functions

```php
<?php
/**
 * Reading time callback
 */
function theme_reading_time_callback( $attributes ) {
    $post_id = get_the_ID();
    $content = get_post_field( 'post_content', $post_id );
    $word_count = str_word_count( strip_tags( $content ) );
    $reading_time = ceil( $word_count / 200 ); // 200 words per minute

    return sprintf(
        _n( '%d min read', '%d min read', $reading_time, 'theme' ),
        $reading_time
    );
}

/**
 * Product SKU callback
 */
function theme_product_sku_callback( $attributes ) {
    $post_id = get_the_ID();
    $sku = get_post_meta( $post_id, '_sku', true );

    if ( empty( $sku ) && isset( $attributes['default'] ) ) {
        return $attributes['default'];
    }

    return $sku;
}
```

### Tag with Attributes

```php
<?php
function theme_register_complex_tag( $tags ) {
    $tags['custom_date'] = array(
        'label'      => __( 'Custom Date', 'theme' ),
        'group'      => 'post',
        'callback'   => 'theme_custom_date_callback',
        'attributes' => array(
            'format' => array(
                'label'   => __( 'Date Format', 'theme' ),
                'type'    => 'text',
                'default' => 'F j, Y',
            ),
            'relative' => array(
                'label'   => __( 'Show Relative', 'theme' ),
                'type'    => 'boolean',
                'default' => false,
            ),
        ),
    );

    return $tags;
}
add_filter( 'generateblocks_dynamic_tags', 'theme_register_complex_tag' );

function theme_custom_date_callback( $attributes ) {
    $format = isset( $attributes['format'] ) ? $attributes['format'] : 'F j, Y';
    $relative = isset( $attributes['relative'] ) && $attributes['relative'];

    if ( $relative ) {
        return human_time_diff( get_the_time( 'U' ), current_time( 'timestamp' ) ) . ' ago';
    }

    return get_the_date( $format );
}
```

## Dynamic Content in Query Loops

When inside a query loop, dynamic tags automatically use the current post context:

```html
<!-- wp:query {"queryId":1,"query":{"perPage":6,"postType":"post"}} -->
<div class="wp-block-query">
    <!-- wp:post-template -->

        <!-- Each dynamic tag uses the loop's current post -->
        <!-- wp:generateblocks/text {"uniqueId":"loop001","tagName":"h3","useDynamicData":true} -->
        <h3 class="gb-text gb-text-loop001">{{post_title}}</h3>
        <!-- /wp:generateblocks/text -->

        <!-- wp:generateblocks/text {"uniqueId":"loop002","tagName":"p","useDynamicData":true} -->
        <p class="gb-text gb-text-loop002">{{post_excerpt}}</p>
        <!-- /wp:generateblocks/text -->

    <!-- /wp:post-template -->
</div>
<!-- /wp:query -->
```

## Best Practices

### 1. Always Provide Defaults

```
{{acf field="subtitle" default="Welcome to our site"}}
{{post_meta key="price" default="Contact us"}}
```

### 2. Use Appropriate Image Sizes

```
{{featured_image size="medium"}}      → For thumbnails
{{featured_image size="large"}}       → For hero images
{{featured_image size="full"}}        → Only when necessary
```

### 3. Sanitize Output

Dynamic content is automatically escaped, but for custom tags:

```php
function my_custom_tag_callback( $attributes ) {
    $value = get_post_meta( get_the_ID(), 'field', true );
    return esc_html( $value ); // For text
    return esc_url( $value );  // For URLs
    return wp_kses_post( $value ); // For HTML
}
```

### 4. Cache Expensive Lookups

```php
function theme_expensive_tag_callback( $attributes ) {
    $post_id = get_the_ID();
    $cache_key = 'theme_tag_' . $post_id;
    $cached = wp_cache_get( $cache_key );

    if ( false !== $cached ) {
        return $cached;
    }

    // Expensive operation
    $result = expensive_calculation();

    wp_cache_set( $cache_key, $result, '', HOUR_IN_SECONDS );
    return $result;
}
```

### 5. Test Empty States

Always check how dynamic content looks when:
- Field is empty
- Post has no featured image
- Author has no bio
- No categories assigned

## Troubleshooting

### Dynamic Content Not Rendering

1. Check if GenerateBlocks Pro is active
2. Verify `useDynamicData` is set to `true`
3. Check tag syntax (double curly braces)
4. Ensure post context exists (not in query loop outside template)

### Wrong Data Displayed

1. Check if inside correct query loop context
2. Verify post ID is correct
3. Check meta key spelling
4. Look for caching issues

### ACF Fields Not Working

1. Verify ACF plugin is active
2. Check field name matches exactly
3. Ensure field is published to correct post type
4. Check field return format settings
