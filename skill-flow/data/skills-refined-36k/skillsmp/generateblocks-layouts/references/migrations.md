# GenerateBlocks Migrations Skill

Handle V1 to V2 block migrations, deprecations, and backward compatibility.

## When to Use This Skill

- Migrating sites from GenerateBlocks V1 to V2
- Understanding block deprecation patterns
- Creating migration scripts for bulk updates
- Maintaining backward compatibility

## V1 vs V2 Architecture

### V1 Blocks (Legacy)

```
generateblocks/container    → Wrapper/layout block
generateblocks/button       → Button element
generateblocks/headline     → Heading element
generateblocks/grid         → Grid layout
generateblocks/image        → Image element
```

### V2 Blocks (Current)

```
generateblocks/element      → All container types (div, section, etc.)
generateblocks/text         → All text types (p, h1-h6, a, button, etc.)
generateblocks/media        → Images
generateblocks/shape        → SVG icons and shapes
```

### Key Differences

| Aspect | V1 | V2 |
|--------|-----|-----|
| Block types | Specific purpose | Generic, flexible |
| Tag names | Fixed per block | Configurable via `tagName` |
| Styling | Attribute-based | Attribute + inline CSS |
| Classes | Generated | Unique ID based |
| Nesting | Explicit containers | Any element can contain |

## Block Mapping

### Container to Element

**V1:**
```html
<!-- wp:generateblocks/container {"uniqueId":"abc123","paddingTop":"40","paddingBottom":"40","backgroundColor":"#ffffff"} -->
<div class="gb-container gb-container-abc123">
    <!-- Content -->
</div>
<!-- /wp:generateblocks/container -->
```

**V2:**
```html
<!-- wp:generateblocks/element {"uniqueId":"abc123","tagName":"div","styles":{"paddingTop":"40px","paddingBottom":"40px","backgroundColor":"#ffffff"},"css":".gb-element-abc123{padding-top:40px;padding-bottom:40px;background-color:#ffffff}"} -->
<div class="gb-element gb-element-abc123">
    <!-- Content -->
</div>
<!-- /wp:generateblocks/element -->
```

### Button to Text

**V1:**
```html
<!-- wp:generateblocks/button {"uniqueId":"btn123","backgroundColor":"#0073aa","textColor":"#ffffff","paddingTop":"15","paddingRight":"30","paddingBottom":"15","paddingLeft":"30"} -->
<a class="gb-button gb-button-btn123" href="#">Click Me</a>
<!-- /wp:generateblocks/button -->
```

**V2:**
```html
<!-- wp:generateblocks/text {"uniqueId":"btn123","tagName":"a","htmlAttributes":[{"attribute":"href","value":"#"}],"styles":{"display":"inline-flex","padding":"15px 30px","backgroundColor":"#0073aa","color":"#ffffff","textDecoration":"none"},"css":".gb-text-btn123{display:inline-flex;padding:15px 30px;background-color:#0073aa;color:#ffffff;text-decoration:none}"} -->
<a class="gb-text gb-text-btn123" href="#">Click Me</a>
<!-- /wp:generateblocks/text -->
```

### Headline to Text

**V1:**
```html
<!-- wp:generateblocks/headline {"uniqueId":"head123","element":"h2","fontSize":"32","fontWeight":"700"} -->
<h2 class="gb-headline gb-headline-head123">My Heading</h2>
<!-- /wp:generateblocks/headline -->
```

**V2:**
```html
<!-- wp:generateblocks/text {"uniqueId":"head123","tagName":"h2","styles":{"fontSize":"32px","fontWeight":"700"},"css":".gb-text-head123{font-size:32px;font-weight:700}"} -->
<h2 class="gb-text gb-text-head123">My Heading</h2>
<!-- /wp:generateblocks/text -->
```

### Grid to Element

**V1:**
```html
<!-- wp:generateblocks/grid {"uniqueId":"grid123","columns":"3","horizontalGap":"30"} -->
<div class="gb-grid-wrapper">
    <div class="gb-grid gb-grid-grid123">
        <!-- Grid items -->
    </div>
</div>
<!-- /wp:generateblocks/grid -->
```

**V2:**
```html
<!-- wp:generateblocks/element {"uniqueId":"grid123","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(3, 1fr)","gap":"30px"},"css":".gb-element-grid123{display:grid;grid-template-columns:repeat(3, 1fr);gap:30px}"} -->
<div class="gb-element gb-element-grid123">
    <!-- Grid items -->
</div>
<!-- /wp:generateblocks/element -->
```

### Image to Media

**V1:**
```html
<!-- wp:generateblocks/image {"uniqueId":"img123","mediaId":456,"width":"600","height":"400"} -->
<figure class="gb-image gb-image-img123">
    <img src="image.jpg" alt="Description" width="600" height="400">
</figure>
<!-- /wp:generateblocks/image -->
```

**V2:**
```html
<!-- wp:generateblocks/media {"uniqueId":"img123","mediaId":456,"htmlAttributes":[{"attribute":"src","value":"image.jpg"},{"attribute":"alt","value":"Description"},{"attribute":"width","value":"600"},{"attribute":"height","value":"400"}],"styles":{"width":"600px","height":"400px"},"css":".gb-media-img123{width:600px;height:400px}"} -->
<img class="gb-media gb-media-img123" src="image.jpg" alt="Description" width="600" height="400" />
<!-- /wp:generateblocks/media -->
```

## Migration Scripts

### PHP Migration Helper

```php
<?php
/**
 * Migrate GenerateBlocks V1 to V2
 */
class GB_Block_Migrator {

    /**
     * Migrate all posts
     */
    public function migrate_all_posts() {
        $posts = get_posts( array(
            'post_type'      => array( 'post', 'page' ),
            'posts_per_page' => -1,
            'post_status'    => 'any',
        ) );

        foreach ( $posts as $post ) {
            $this->migrate_post( $post->ID );
        }
    }

    /**
     * Migrate single post
     */
    public function migrate_post( $post_id ) {
        $content = get_post_field( 'post_content', $post_id );
        $migrated = $this->migrate_content( $content );

        if ( $migrated !== $content ) {
            wp_update_post( array(
                'ID'           => $post_id,
                'post_content' => $migrated,
            ) );

            // Log migration
            update_post_meta( $post_id, '_gb_migrated', current_time( 'mysql' ) );
        }
    }

    /**
     * Migrate content blocks
     */
    public function migrate_content( $content ) {
        // Migrate containers
        $content = $this->migrate_containers( $content );

        // Migrate buttons
        $content = $this->migrate_buttons( $content );

        // Migrate headlines
        $content = $this->migrate_headlines( $content );

        // Migrate grids
        $content = $this->migrate_grids( $content );

        // Migrate images
        $content = $this->migrate_images( $content );

        return $content;
    }

    /**
     * Migrate container blocks
     */
    private function migrate_containers( $content ) {
        $pattern = '/<!-- wp:generateblocks\/container (\{.*?\}) -->/s';

        return preg_replace_callback( $pattern, function( $matches ) {
            $attrs = json_decode( $matches[1], true );

            $new_attrs = array(
                'uniqueId' => $attrs['uniqueId'] ?? $this->generate_id(),
                'tagName'  => $attrs['tagName'] ?? 'div',
                'styles'   => $this->convert_container_styles( $attrs ),
            );

            $new_attrs['css'] = $this->generate_css( 'element', $new_attrs );

            return '<!-- wp:generateblocks/element ' . wp_json_encode( $new_attrs ) . ' -->';
        }, $content );
    }

    /**
     * Convert container attributes to V2 styles
     */
    private function convert_container_styles( $attrs ) {
        $styles = array();

        // Padding
        if ( ! empty( $attrs['paddingTop'] ) ) {
            $styles['paddingTop'] = $attrs['paddingTop'] . ( $attrs['paddingUnit'] ?? 'px' );
        }
        if ( ! empty( $attrs['paddingRight'] ) ) {
            $styles['paddingRight'] = $attrs['paddingRight'] . ( $attrs['paddingUnit'] ?? 'px' );
        }
        if ( ! empty( $attrs['paddingBottom'] ) ) {
            $styles['paddingBottom'] = $attrs['paddingBottom'] . ( $attrs['paddingUnit'] ?? 'px' );
        }
        if ( ! empty( $attrs['paddingLeft'] ) ) {
            $styles['paddingLeft'] = $attrs['paddingLeft'] . ( $attrs['paddingUnit'] ?? 'px' );
        }

        // Margin
        if ( ! empty( $attrs['marginTop'] ) ) {
            $styles['marginTop'] = $attrs['marginTop'] . ( $attrs['marginUnit'] ?? 'px' );
        }
        if ( ! empty( $attrs['marginBottom'] ) ) {
            $styles['marginBottom'] = $attrs['marginBottom'] . ( $attrs['marginUnit'] ?? 'px' );
        }

        // Background
        if ( ! empty( $attrs['backgroundColor'] ) ) {
            $styles['backgroundColor'] = $attrs['backgroundColor'];
        }

        // Flex/Grid
        if ( ! empty( $attrs['display'] ) ) {
            $styles['display'] = $attrs['display'];
        }
        if ( ! empty( $attrs['flexDirection'] ) ) {
            $styles['flexDirection'] = $attrs['flexDirection'];
        }
        if ( ! empty( $attrs['alignItems'] ) ) {
            $styles['alignItems'] = $attrs['alignItems'];
        }
        if ( ! empty( $attrs['justifyContent'] ) ) {
            $styles['justifyContent'] = $attrs['justifyContent'];
        }

        return $styles;
    }

    /**
     * Generate CSS string from styles
     */
    private function generate_css( $type, $attrs ) {
        $selector = '.gb-' . $type . '-' . $attrs['uniqueId'];
        $css = $selector . '{';

        foreach ( $attrs['styles'] as $prop => $value ) {
            $css .= $this->camel_to_kebab( $prop ) . ':' . $value . ';';
        }

        $css .= '}';

        return $css;
    }

    /**
     * Convert camelCase to kebab-case
     */
    private function camel_to_kebab( $string ) {
        return strtolower( preg_replace( '/([a-z])([A-Z])/', '$1-$2', $string ) );
    }

    /**
     * Generate unique ID
     */
    private function generate_id() {
        return substr( md5( uniqid() ), 0, 8 );
    }
}
```

### WP-CLI Migration Command

```php
<?php
/**
 * WP-CLI command for GenerateBlocks migration
 */
if ( defined( 'WP_CLI' ) && WP_CLI ) {

    class GB_Migration_Command {

        /**
         * Migrate all GenerateBlocks V1 blocks to V2
         *
         * ## OPTIONS
         *
         * [--dry-run]
         * : Preview changes without saving
         *
         * [--post-type=<type>]
         * : Limit to specific post type
         *
         * ## EXAMPLES
         *
         *     wp gb-migrate all
         *     wp gb-migrate all --dry-run
         *     wp gb-migrate all --post-type=page
         */
        public function all( $args, $assoc_args ) {
            $dry_run = isset( $assoc_args['dry-run'] );
            $post_type = $assoc_args['post-type'] ?? array( 'post', 'page' );

            $migrator = new GB_Block_Migrator();

            $posts = get_posts( array(
                'post_type'      => $post_type,
                'posts_per_page' => -1,
                'post_status'    => 'any',
            ) );

            $count = 0;

            foreach ( $posts as $post ) {
                $content = get_post_field( 'post_content', $post->ID );

                // Check for V1 blocks
                if ( strpos( $content, 'wp:generateblocks/container' ) !== false ||
                     strpos( $content, 'wp:generateblocks/button' ) !== false ||
                     strpos( $content, 'wp:generateblocks/headline' ) !== false ||
                     strpos( $content, 'wp:generateblocks/grid' ) !== false ) {

                    WP_CLI::log( "Processing: {$post->post_title} (ID: {$post->ID})" );

                    if ( ! $dry_run ) {
                        $migrator->migrate_post( $post->ID );
                    }

                    $count++;
                }
            }

            if ( $dry_run ) {
                WP_CLI::success( "Would migrate {$count} posts. Run without --dry-run to apply." );
            } else {
                WP_CLI::success( "Migrated {$count} posts." );
            }
        }

        /**
         * Migrate single post
         *
         * ## OPTIONS
         *
         * <post_id>
         * : Post ID to migrate
         */
        public function post( $args, $assoc_args ) {
            $post_id = $args[0];
            $migrator = new GB_Block_Migrator();

            $migrator->migrate_post( $post_id );

            WP_CLI::success( "Migrated post {$post_id}" );
        }
    }

    WP_CLI::add_command( 'gb-migrate', 'GB_Migration_Command' );
}
```

## Block Deprecations

### How Deprecations Work

GenerateBlocks uses WordPress block deprecations to handle backward compatibility:

```javascript
// In block registration
registerBlockType( 'generateblocks/element', {
    // Current version
    attributes: currentAttributes,
    save: currentSave,

    // Deprecated versions
    deprecated: [
        {
            attributes: v1Attributes,
            save: v1Save,
            migrate: migrateFromV1,
        },
    ],
} );
```

### Deprecation Flow

1. User opens editor with old block
2. WordPress detects version mismatch
3. Migration function runs
4. Block updates to new format
5. User saves (or auto-saves)

### Creating Custom Deprecations

```javascript
const deprecated = [
    {
        // V1 attributes
        attributes: {
            uniqueId: { type: 'string' },
            paddingTop: { type: 'number' },
            paddingBottom: { type: 'number' },
            backgroundColor: { type: 'string' },
        },

        // Check if this deprecation applies
        isEligible( attributes ) {
            return typeof attributes.paddingTop === 'number';
        },

        // Transform old to new
        migrate( attributes, innerBlocks ) {
            const { paddingTop, paddingBottom, backgroundColor, ...rest } = attributes;

            return [
                {
                    ...rest,
                    styles: {
                        paddingTop: paddingTop ? `${paddingTop}px` : undefined,
                        paddingBottom: paddingBottom ? `${paddingBottom}px` : undefined,
                        backgroundColor,
                    },
                },
                innerBlocks,
            ];
        },

        // Old save function
        save( { attributes } ) {
            return (
                <div className={`gb-container-${attributes.uniqueId}`}>
                    <InnerBlocks.Content />
                </div>
            );
        },
    },
];
```

## CSS Migration

### Class Name Changes

| V1 Class | V2 Class |
|----------|----------|
| `.gb-container-{id}` | `.gb-element-{id}` |
| `.gb-button-{id}` | `.gb-text-{id}` |
| `.gb-headline-{id}` | `.gb-text-{id}` |
| `.gb-grid-{id}` | `.gb-element-{id}` |
| `.gb-image-{id}` | `.gb-media-{id}` |

### Update Theme CSS

```css
/* Before: V1 selectors */
.gb-container-hero { }
.gb-button-primary { }
.gb-headline-main { }

/* After: V2 selectors */
.gb-element-hero { }
.gb-text-primary { }
.gb-text-main { }
```

### Migration Script for CSS

```php
<?php
/**
 * Migrate CSS class references
 */
function migrate_css_classes( $css ) {
    $replacements = array(
        '/\.gb-container-/' => '.gb-element-',
        '/\.gb-button-/'    => '.gb-text-',
        '/\.gb-headline-/'  => '.gb-text-',
        '/\.gb-grid-/'      => '.gb-element-',
        '/\.gb-image-/'     => '.gb-media-',
    );

    foreach ( $replacements as $pattern => $replacement ) {
        $css = preg_replace( $pattern, $replacement, $css );
    }

    return $css;
}
```

## Backward Compatibility

### Support Both Versions

```php
<?php
/**
 * Load styles for both V1 and V2 blocks
 */
add_action( 'wp_enqueue_scripts', function() {
    // V1 styles (legacy support)
    wp_enqueue_style(
        'generateblocks-legacy',
        get_template_directory_uri() . '/css/gb-v1-compat.css'
    );

    // V2 styles (current)
    wp_enqueue_style(
        'generateblocks-v2',
        get_template_directory_uri() . '/css/gb-v2.css'
    );
} );
```

### Gradual Migration

```php
<?php
/**
 * Check migration status
 */
function get_migration_status() {
    global $wpdb;

    $v1_blocks = $wpdb->get_var(
        "SELECT COUNT(*) FROM {$wpdb->posts}
        WHERE post_content LIKE '%wp:generateblocks/container%'
        OR post_content LIKE '%wp:generateblocks/button%'
        OR post_content LIKE '%wp:generateblocks/headline%'"
    );

    $v2_blocks = $wpdb->get_var(
        "SELECT COUNT(*) FROM {$wpdb->posts}
        WHERE post_content LIKE '%wp:generateblocks/element%'
        OR post_content LIKE '%wp:generateblocks/text%'
        OR post_content LIKE '%wp:generateblocks/media%'"
    );

    return array(
        'v1_posts' => $v1_blocks,
        'v2_posts' => $v2_blocks,
        'migration_complete' => $v1_blocks === 0,
    );
}
```

## Testing Migrations

### Pre-Migration Checklist

1. **Backup database** before any migration
2. **Test on staging** first
3. **Document current state** (screenshots, block counts)
4. **Check custom CSS** for V1 class references

### Validation Script

```php
<?php
/**
 * Validate migration results
 */
function validate_migration( $post_id ) {
    $content = get_post_field( 'post_content', $post_id );
    $errors = array();

    // Check for orphaned V1 blocks
    if ( preg_match( '/wp:generateblocks\/(container|button|headline|grid|image)/', $content ) ) {
        $errors[] = 'V1 blocks still present';
    }

    // Check for valid V2 structure
    if ( preg_match_all( '/<!-- wp:generateblocks\/element (\{.*?\}) -->/s', $content, $matches ) ) {
        foreach ( $matches[1] as $attrs_json ) {
            $attrs = json_decode( $attrs_json, true );

            if ( empty( $attrs['uniqueId'] ) ) {
                $errors[] = 'Missing uniqueId';
            }

            if ( empty( $attrs['tagName'] ) ) {
                $errors[] = 'Missing tagName';
            }

            if ( ! empty( $attrs['styles'] ) && empty( $attrs['css'] ) ) {
                $errors[] = 'Styles without CSS';
            }
        }
    }

    return $errors;
}
```

### Post-Migration Verification

```php
<?php
/**
 * Verify all pages render correctly
 */
function verify_rendered_output() {
    $posts = get_posts( array(
        'post_type'      => array( 'post', 'page' ),
        'posts_per_page' => -1,
        'meta_key'       => '_gb_migrated',
    ) );

    $results = array();

    foreach ( $posts as $post ) {
        $response = wp_remote_get( get_permalink( $post->ID ) );

        if ( is_wp_error( $response ) ) {
            $results[ $post->ID ] = 'Error: ' . $response->get_error_message();
        } elseif ( wp_remote_retrieve_response_code( $response ) !== 200 ) {
            $results[ $post->ID ] = 'HTTP ' . wp_remote_retrieve_response_code( $response );
        } else {
            $body = wp_remote_retrieve_body( $response );

            // Check for PHP errors
            if ( strpos( $body, 'Fatal error' ) !== false ) {
                $results[ $post->ID ] = 'PHP Fatal Error';
            } elseif ( strpos( $body, 'Warning:' ) !== false ) {
                $results[ $post->ID ] = 'PHP Warning';
            } else {
                $results[ $post->ID ] = 'OK';
            }
        }
    }

    return $results;
}
```

## Best Practices

### 1. Migrate Incrementally

Don't migrate everything at once:

```php
<?php
// Migrate 10 posts at a time
function migrate_batch( $batch_size = 10 ) {
    $posts = get_posts( array(
        'posts_per_page' => $batch_size,
        'meta_query'     => array(
            array(
                'key'     => '_gb_migrated',
                'compare' => 'NOT EXISTS',
            ),
        ),
    ) );

    foreach ( $posts as $post ) {
        migrate_post( $post->ID );
    }

    return count( $posts );
}
```

### 2. Preserve Original Content

```php
<?php
// Store original content before migration
update_post_meta( $post_id, '_gb_original_content', $original_content );
update_post_meta( $post_id, '_gb_migration_version', '2.0' );
```

### 3. Log All Changes

```php
<?php
function log_migration( $post_id, $changes ) {
    $log = get_option( 'gb_migration_log', array() );

    $log[] = array(
        'post_id'   => $post_id,
        'timestamp' => current_time( 'mysql' ),
        'changes'   => $changes,
    );

    update_option( 'gb_migration_log', $log );
}
```

### 4. Rollback Capability

```php
<?php
function rollback_migration( $post_id ) {
    $original = get_post_meta( $post_id, '_gb_original_content', true );

    if ( $original ) {
        wp_update_post( array(
            'ID'           => $post_id,
            'post_content' => $original,
        ) );

        delete_post_meta( $post_id, '_gb_migrated' );
        delete_post_meta( $post_id, '_gb_original_content' );

        return true;
    }

    return false;
}
```

## Troubleshooting

### Block Shows "This block contains unexpected content"

1. Check block attributes are valid JSON
2. Verify all required attributes present
3. Compare with working V2 block
4. Check for encoding issues

### Styles Not Applying

1. Verify CSS string matches styles object
2. Check class names are correct
3. Clear all caches
4. Check for CSS conflicts

### Inner Blocks Missing

1. Ensure inner content is preserved during migration
2. Check for nesting errors
3. Verify closing tags match

### Migration Crashes

1. Increase PHP memory limit
2. Process in smaller batches
3. Check for malformed content
4. Review error logs
