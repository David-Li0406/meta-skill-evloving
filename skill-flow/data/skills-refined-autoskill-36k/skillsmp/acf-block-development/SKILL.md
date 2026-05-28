---
name: ACF Block Development
description: Create ACF flexible content blocks (partials) following SOMA PageBuilder architecture
---

# ACF Block Development Skill

This skill guides the creation of ACF flexible content blocks (partials) for the SOMA theme's PageBuilder system.

## When to Use This Skill

Use this skill when you need to:
- Create a new ACF flexible content block
- Add a new page section/component
- Modify existing block layouts
- Work with BlockRegistry and BlockRenderer
- Create reusable content patterns

## PageBuilder Architecture

### System Overview

```
ACF Field: soma_blocks (Flexible Content)
    ↓
page-builder.php (calls BlockRenderer)
    ↓
BlockRegistry (53 blocks mapped: layout → field_group + partial)
    ↓
BlockRenderer (validates, sets query vars, includes partial)
    ↓
partials/ComponentName.php (renders HTML)
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| BlockRegistry | `includes/PageBuilder/BlockRegistry.php` | Maps layouts to field groups and partials |
| BlockRenderer | `includes/PageBuilder/BlockRenderer.php` | Renders blocks with validation and caching |
| Loader | `includes/PageBuilder/Loader.php` | Initializes PageBuilder system |

## Creating a New ACF Block

### Step 1: Create ACF Field Group

**Option A: ACF Admin UI**
1. Go to **Custom Fields** → **Add New**
2. Create field group with fields for your block
3. Set Location: `Flexible Content` > `soma_blocks` > `Layout` equals `ComponentName`

**Option B: ACF JSON (Recommended)**

Create `acf-json/group_component_name.json`:
```json
{
    "key": "group_component_name",
    "title": "Component Name Block",
    "fields": [
        {
            "key": "field_component_title",
            "label": "Title",
            "name": "title",
            "type": "text"
        },
        {
            "key": "field_component_content",
            "label": "Content",
            "name": "content",
            "type": "wysiwyg"
        }
    ],
    "location": [
        [
            {
                "param": "flexible_content_layout",
                "operator": "==",
                "value": "ComponentName"
            }
        ]
    ]
}
```

### Step 2: Register Block in BlockRegistry

**File**: `includes/PageBuilder/BlockRegistry.php`

```php
private function register_default_blocks(): void {
    // ... existing blocks ...
    
    // Add your new block
    $this->register_block(
        'ComponentName',          // ACF layout name
        'component_name_content', // ACF field group key (for validation)
        'ComponentName'           // Partial filename (without .php)
    );
}
```

### Step 3: Create Partial Template

**File**: `partials/ComponentName.php`

```php
<?php
/**
 * Component Name Block
 *
 * Renders the Component Name section.
 *
 * @package Soma
 * @since   3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly.
}

// Access block data via WordPress query vars (v3.0+)
$block_counter = get_query_var( 'soma_block_counter' );
$block_content = get_query_var( 'soma_block_content' );
$block_layout  = get_query_var( 'soma_block_layout' );

// Extract fields with defaults
$title   = $block_content['title'] ?? '';
$content = $block_content['content'] ?? '';
$image   = $block_content['image'] ?? null;

// Generate unique hash for CSS class
$hash = substr( md5( $block_layout . $block_counter ), 0, 6 );
?>

<section class="componentname-partial-<?php echo esc_attr( $hash ); ?>" 
         data-block="<?php echo esc_attr( $block_counter ); ?>">
    
    <?php if ( $title ) : ?>
        <h2 class="section-title"><?php echo esc_html( $title ); ?></h2>
    <?php endif; ?>
    
    <?php if ( $content ) : ?>
        <div class="section-content">
            <?php echo wp_kses_post( $content ); ?>
        </div>
    <?php endif; ?>
    
    <?php if ( $image ) : ?>
        <div class="section-image">
            <?php echo wp_get_attachment_image( $image, 'large' ); ?>
        </div>
    <?php endif; ?>
    
</section>
```

### Step 4: Create SCSS Styles

**File**: `sass/partials/_ComponentName.scss`

```scss
/**
 * Component Name Partial Styles
 *
 * @package Soma
 * @since   3.0.0
 */

[class^="componentname-partial-"] {
    padding: var(--soma-spacing-2xl) 0;
    background: var(--soma-bg-white);
    
    .section-title {
        font-family: var(--soma-font-family-primary);
        font-size: var(--soma-font-size-h2);
        color: var(--soma-color-text-primary);
        margin-bottom: var(--soma-spacing-lg);
    }
    
    .section-content {
        font-size: var(--soma-font-size-body);
        line-height: var(--soma-line-height-relaxed);
        color: var(--soma-color-text-secondary);
        
        p {
            margin-bottom: var(--soma-spacing-md);
        }
    }
    
    .section-image {
        margin-top: var(--soma-spacing-xl);
        
        img {
            width: 100%;
            height: auto;
            border-radius: var(--soma-border-radius);
        }
    }
    
    // Responsive
    @media (max-width: 991px) {
        padding: var(--soma-spacing-xl) 0;
        
        .section-title {
            font-size: var(--soma-font-size-h3);
        }
    }
    
    @media (max-width: 767px) {
        padding: var(--soma-spacing-lg) 0;
        
        .section-title {
            font-size: var(--soma-font-size-h4);
        }
    }
}
```

### Step 5: Import SCSS in Main File

**File**: `sass/main.scss`

```scss
// ... existing imports ...

// #DittoPartials
@import 'partials/ComponentName';  // Add under this marker
```

### Step 6: Add JavaScript (if needed)

**File**: `js/components/componentName.js`

```javascript
/**
 * Component Name Handler
 *
 * @package Soma
 * @since   3.0.0
 */

export function componentNameHandler($element) {
    if (!$element || !$element.length) {
        return;
    }
    
    // Your interactive code here
    $element.each(function() {
        const $this = $(this);
        
        // Example: Click handler
        $this.find('.clickable').on('click', function(e) {
            e.preventDefault();
            // Handle click
        });
    });
}
```

**File**: `js/main.js`

```javascript
import { componentNameHandler } from './components/componentName';

// Initialize conditionally
if ($('[class^="componentname-partial-"]').length > 0) {
    componentNameHandler($('[class^="componentname-partial-"]'));
}
```

### Step 7: Build Assets

```bash
npm run prod
```

## Query Vars Reference

The BlockRenderer sets these WordPress query vars for each block:

| Query Var | Type | Description |
|-----------|------|-------------|
| `soma_block_counter` | int | Block index (1-based) |
| `soma_block_content` | array | ACF field data for block |
| `soma_block_layout` | string | Layout name (e.g., 'ComponentName') |

```php
// Access in partial
$counter = get_query_var( 'soma_block_counter' ); // e.g., 1, 2, 3
$content = get_query_var( 'soma_block_content' ); // ACF fields array
$layout  = get_query_var( 'soma_block_layout' );  // 'ComponentName'
```

## Common ACF Field Types

### Text Fields
```php
$title = $block_content['title'] ?? '';
echo esc_html( $title );
```

### WYSIWYG/Textarea
```php
$content = $block_content['content'] ?? '';
echo wp_kses_post( $content );
```

### Image
```php
$image_id = $block_content['image'] ?? null;
if ( $image_id ) {
    echo wp_get_attachment_image( $image_id, 'large', false, [
        'class' => 'section-image',
        'alt'   => get_post_meta( $image_id, '_wp_attachment_image_alt', true ),
    ] );
}
```

### Gallery
```php
$gallery = $block_content['gallery'] ?? [];
foreach ( $gallery as $image_id ) {
    echo wp_get_attachment_image( $image_id, 'medium' );
}
```

### Link
```php
$link = $block_content['link'] ?? null;
if ( $link ) {
    printf(
        '<a href="%s" target="%s" class="btn">%s</a>',
        esc_url( $link['url'] ),
        esc_attr( $link['target'] ?: '_self' ),
        esc_html( $link['title'] )
    );
}
```

### Repeater
```php
$items = $block_content['items'] ?? [];
if ( $items ) {
    echo '<ul class="items-list">';
    foreach ( $items as $item ) {
        printf(
            '<li>%s</li>',
            esc_html( $item['title'] )
        );
    }
    echo '</ul>';
}
```

### Select/Radio
```php
$style = $block_content['style'] ?? 'default';
$class = 'section-style-' . sanitize_html_class( $style );
```

### True/False (Switcher)
```php
$show_button = $block_content['show_button'] ?? false;
if ( $show_button ) {
    // Render button
}
```

### Post Object
```php
$selected_post = $block_content['featured_post'] ?? null;
if ( $selected_post ) {
    $post_id    = is_object( $selected_post ) ? $selected_post->ID : $selected_post;
    $post_title = get_the_title( $post_id );
    $post_url   = get_permalink( $post_id );
}
```

### Relationship (Multiple Posts)
```php
$posts = $block_content['related_posts'] ?? [];
foreach ( $posts as $post ) {
    $post_id = is_object( $post ) ? $post->ID : $post;
    // Use get_the_title($post_id), get_permalink($post_id), etc.
}
```

## Internationalized Fields

For bilingual content (EN/ES), use the helper function:

```php
// ACF fields: file (EN), file_es (ES)
$file = soma_get_i18n_field( $block_content, 'file' );

// Returns file_es if Spanish, file if English
if ( $file ) {
    echo '<a href="' . esc_url( $file['url'] ) . '">Download</a>';
}
```

## CSS Variables Reference

```scss
// Colors
--soma-primary
--soma-secondary
--soma-color-text-primary
--soma-color-text-secondary
--soma-bg-white
--soma-bg-light
--soma-bg-dark

// Typography
--soma-font-family-primary
--soma-font-size-h1
--soma-font-size-h2
--soma-font-size-h3
--soma-font-size-body
--soma-line-height-tight
--soma-line-height-relaxed

// Spacing
--soma-spacing-xs
--soma-spacing-sm
--soma-spacing-md
--soma-spacing-lg
--soma-spacing-xl
--soma-spacing-2xl

// Layout
--soma-container-max-width
--soma-border-radius

// Transitions
--soma-transition-base
--soma-transition-slow
```

## Dark Mode Support

```php
// Check if previous block had dark background
$previous_is_dark = get_query_var( 'soma_previous_block_dark' ) ?? false;

// Check if this block should be dark
$is_dark = $block_content['dark_style'] ?? false;
$dark_class = $is_dark ? 'dark-style' : '';
?>

<section class="componentname-partial <?php echo esc_attr( $dark_class ); ?>">
```

```scss
[class^="componentname-partial-"] {
    &.dark-style {
        background: var(--soma-bg-dark);
        color: var(--soma-color-text-light);
        
        .section-title {
            color: var(--soma-color-text-light);
        }
    }
}
```

## Block Validation

The BlockRenderer validates blocks before rendering:

1. **Structure Validation** - Checks for `acf_fc_layout` key
2. **Registry Validation** - Verifies block is registered in BlockRegistry
3. **File Existence** - Checks partial file exists

Errors are logged to `wp-content/uploads/soma-logs/soma.log`.

## Debugging Blocks

```php
// In partial, temporarily add for debugging:
if ( WP_DEBUG ) {
    echo '<!-- Block Data: ';
    print_r( $block_content );
    echo ' -->';
}
```

Or use the logger:
```php
soma_log_debug( 'Block content', [
    'layout'  => $block_layout,
    'counter' => $block_counter,
    'content' => $block_content,
] );
```

## Checklist Before Committing

- [ ] ACF field group created (JSON or Admin UI)
- [ ] Block registered in `BlockRegistry.php`
- [ ] Partial created in `partials/` directory
- [ ] Query vars used (not global `$pageBlock`)
- [ ] All output properly escaped
- [ ] SCSS file created and imported in `main.scss`
- [ ] JavaScript handler added (if interactive)
- [ ] Assets rebuilt (`npm run prod`)
- [ ] Block renders correctly on frontend
- [ ] Responsive design tested
- [ ] PHPCS passes on partial file
