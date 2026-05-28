# GenerateBlocks Patterns Skill

Create and manage reusable block patterns with GenerateBlocks elements.

## When to Use This Skill

- Creating reusable layout components
- Registering custom block patterns in PHP
- Building pattern libraries for themes/plugins
- Converting layouts into shareable patterns

## Pattern Fundamentals

### What Are Block Patterns?

Block patterns are predefined block layouts that can be inserted anywhere. GenerateBlocks patterns combine:
- GenerateBlocks elements (element, text, media, shape)
- WordPress core blocks
- Custom styling via inline CSS

### Pattern Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Unsynced** | Independent copies | Hero sections, cards, layouts |
| **Synced** (Reusable) | Linked instances | Headers, footers, CTAs |
| **Template Parts** | Theme-level patterns | Site-wide elements |

## Registering Patterns in PHP

### Basic Pattern Registration

```php
<?php
/**
 * Register block patterns
 */
function theme_register_block_patterns() {
    // Register pattern category first
    register_block_pattern_category(
        'theme-layouts',
        array(
            'label' => __( 'Theme Layouts', 'theme-slug' ),
        )
    );

    // Register the pattern
    register_block_pattern(
        'theme-slug/hero-section',
        array(
            'title'       => __( 'Hero Section', 'theme-slug' ),
            'description' => __( 'Full-width hero with heading and CTA', 'theme-slug' ),
            'categories'  => array( 'theme-layouts', 'featured' ),
            'keywords'    => array( 'hero', 'banner', 'header' ),
            'blockTypes'  => array( 'core/post-content' ),
            'content'     => '<!-- Pattern content here -->',
        )
    );
}
add_action( 'init', 'theme_register_block_patterns' );
```

### Pattern from File

```php
<?php
function theme_register_block_patterns() {
    register_block_pattern_category( 'theme-layouts', array(
        'label' => __( 'Theme Layouts', 'theme-slug' ),
    ) );

    // Load pattern from file
    $pattern_content = file_get_contents(
        get_template_directory() . '/patterns/hero-section.html'
    );

    register_block_pattern( 'theme-slug/hero-section', array(
        'title'      => __( 'Hero Section', 'theme-slug' ),
        'categories' => array( 'theme-layouts' ),
        'content'    => $pattern_content,
    ) );
}
add_action( 'init', 'theme_register_block_patterns' );
```

### File-Based Patterns (WordPress 6.0+)

Create patterns in `/patterns/` directory with header comment:

```html
<?php
/**
 * Title: Hero Section
 * Slug: theme-slug/hero-section
 * Categories: theme-layouts, featured
 * Keywords: hero, banner, header
 * Block Types: core/post-content
 * Viewport Width: 1400
 */
?>

<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{"minHeight":"600px","display":"flex","alignItems":"center","justifyContent":"center","padding":"4rem 2rem","backgroundColor":"#0a0a0a"},"css":".gb-element-hero001{min-height:600px;display:flex;align-items:center;justify-content:center;padding:4rem 2rem;background-color:#0a0a0a}"} -->
<section class="gb-element gb-element-hero001">
    <!-- Pattern content -->
</section>
<!-- /wp:generateblocks/element -->
```

## Pattern Categories

### Register Custom Categories

```php
<?php
function theme_register_pattern_categories() {
    register_block_pattern_category( 'theme-headers', array(
        'label'       => __( 'Headers', 'theme-slug' ),
        'description' => __( 'Header patterns for pages', 'theme-slug' ),
    ) );

    register_block_pattern_category( 'theme-cards', array(
        'label' => __( 'Cards', 'theme-slug' ),
    ) );

    register_block_pattern_category( 'theme-cta', array(
        'label' => __( 'Call to Action', 'theme-slug' ),
    ) );
}
add_action( 'init', 'theme_register_pattern_categories' );
```

### Core Categories

WordPress provides these built-in categories:
- `featured` - Featured patterns
- `text` - Text patterns
- `columns` - Column layouts
- `header` - Header patterns
- `footer` - Footer patterns
- `buttons` - Button patterns
- `gallery` - Gallery patterns
- `query` - Query loop patterns

## Common Pattern Examples

### Hero Section Pattern

```html
<?php
/**
 * Title: Hero with CTA
 * Slug: theme-slug/hero-cta
 * Categories: theme-layouts, featured
 */
?>

<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{"minHeight":"80vh","display":"flex","flexDirection":"column","alignItems":"center","justifyContent":"center","padding":"4rem 2rem","background":"linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)","color":"#ffffff","textAlign":"center"},"css":".gb-element-hero001{min-height:80vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4rem 2rem;background:linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);color:#ffffff;text-align:center}@media(max-width:768px){.gb-element-hero001{min-height:auto;padding:3rem 1.5rem}}"} -->
<section class="gb-element gb-element-hero001">

    <!-- wp:generateblocks/text {"uniqueId":"hero002","tagName":"h1","styles":{"fontSize":"3.5rem","fontWeight":"900","marginBottom":"1.5rem","maxWidth":"800px","lineHeight":"1.1"},"css":".gb-text-hero002{font-size:3.5rem;font-weight:900;margin-bottom:1.5rem;max-width:800px;line-height:1.1}@media(max-width:768px){.gb-text-hero002{font-size:2.5rem}}"} -->
    <h1 class="gb-text gb-text-hero002">Build Beautiful Websites with GenerateBlocks</h1>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"hero003","tagName":"p","styles":{"fontSize":"1.25rem","marginBottom":"2rem","maxWidth":"600px","opacity":"0.9"},"css":".gb-text-hero003{font-size:1.25rem;margin-bottom:2rem;max-width:600px;opacity:0.9}"} -->
    <p class="gb-text gb-text-hero003">Create stunning layouts without writing code. Flexible, lightweight, and powerful.</p>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/element {"uniqueId":"hero004","tagName":"div","styles":{"display":"flex","gap":"1rem","flexWrap":"wrap","justifyContent":"center"},"css":".gb-element-hero004{display:flex;gap:1rem;flex-wrap:wrap;justify-content:center}"} -->
    <div class="gb-element gb-element-hero004">

        <!-- wp:generateblocks/text {"uniqueId":"hero005","tagName":"a","htmlAttributes":[{"attribute":"href","value":"#"}],"styles":{"padding":"1rem 2rem","backgroundColor":"#e94560","color":"#ffffff","borderRadius":"0.5rem","textDecoration":"none","fontWeight":"600"},"css":".gb-text-hero005{padding:1rem 2rem;background-color:#e94560;color:#ffffff;border-radius:0.5rem;text-decoration:none;font-weight:600;transition:all 0.3s}.gb-text-hero005:hover{background-color:#d63850;transform:translateY(-2px)}"} -->
        <a class="gb-text gb-text-hero005" href="#">Get Started</a>
        <!-- /wp:generateblocks/text -->

        <!-- wp:generateblocks/text {"uniqueId":"hero006","tagName":"a","htmlAttributes":[{"attribute":"href","value":"#"}],"styles":{"padding":"1rem 2rem","backgroundColor":"transparent","color":"#ffffff","border":"2px solid #ffffff","borderRadius":"0.5rem","textDecoration":"none","fontWeight":"600"},"css":".gb-text-hero006{padding:1rem 2rem;background-color:transparent;color:#ffffff;border:2px solid #ffffff;border-radius:0.5rem;text-decoration:none;font-weight:600;transition:all 0.3s}.gb-text-hero006:hover{background-color:#ffffff;color:#1a1a2e}"} -->
        <a class="gb-text gb-text-hero006" href="#">Learn More</a>
        <!-- /wp:generateblocks/text -->

    </div>
    <!-- /wp:generateblocks/element -->

</section>
<!-- /wp:generateblocks/element -->
```

### Feature Card Pattern

```html
<?php
/**
 * Title: Feature Card
 * Slug: theme-slug/feature-card
 * Categories: theme-cards
 */
?>

<!-- wp:generateblocks/element {"uniqueId":"card001","tagName":"article","styles":{"padding":"2rem","backgroundColor":"#ffffff","borderRadius":"1rem","boxShadow":"0 4px 20px rgba(0,0,0,0.08)","display":"flex","flexDirection":"column","gap":"1rem"},"css":".gb-element-card001{padding:2rem;background-color:#ffffff;border-radius:1rem;box-shadow:0 4px 20px rgba(0,0,0,0.08);display:flex;flex-direction:column;gap:1rem;transition:all 0.3s}.gb-element-card001:hover{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,0.12)}"} -->
<article class="gb-element gb-element-card001">

    <!-- wp:generateblocks/element {"uniqueId":"card002","tagName":"div","styles":{"width":"3rem","height":"3rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"#e94560","borderRadius":"0.75rem","color":"#ffffff"},"css":".gb-element-card002{width:3rem;height:3rem;display:flex;align-items:center;justify-content:center;background-color:#e94560;border-radius:0.75rem;color:#ffffff}"} -->
    <div class="gb-element gb-element-card002">
        <!-- Icon placeholder -->
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l10 5-10 5-10-5 10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    </div>
    <!-- /wp:generateblocks/element -->

    <!-- wp:generateblocks/text {"uniqueId":"card003","tagName":"h3","styles":{"fontSize":"1.25rem","fontWeight":"700","marginBottom":"0"},"css":".gb-text-card003{font-size:1.25rem;font-weight:700;margin-bottom:0}"} -->
    <h3 class="gb-text gb-text-card003">Feature Title</h3>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/text {"uniqueId":"card004","tagName":"p","styles":{"color":"#666666","lineHeight":"1.6"},"css":".gb-text-card004{color:#666666;line-height:1.6}"} -->
    <p class="gb-text gb-text-card004">Feature description goes here. Explain the benefit in a concise way.</p>
    <!-- /wp:generateblocks/text -->

</article>
<!-- /wp:generateblocks/element -->
```

### Three-Column Features Grid

```html
<?php
/**
 * Title: Three Column Features
 * Slug: theme-slug/three-features
 * Categories: theme-layouts, columns
 * Viewport Width: 1200
 */
?>

<!-- wp:generateblocks/element {"uniqueId":"feat001","tagName":"section","styles":{"padding":"5rem 2rem","backgroundColor":"#f8f9fa"},"css":".gb-element-feat001{padding:5rem 2rem;background-color:#f8f9fa}@media(max-width:768px){.gb-element-feat001{padding:3rem 1.5rem}}"} -->
<section class="gb-element gb-element-feat001">

    <!-- wp:generateblocks/element {"uniqueId":"feat002","tagName":"div","styles":{"maxWidth":"1200px","margin":"0 auto"},"css":".gb-element-feat002{max-width:1200px;margin:0 auto}"} -->
    <div class="gb-element gb-element-feat002">

        <!-- wp:generateblocks/text {"uniqueId":"feat003","tagName":"h2","styles":{"fontSize":"2.5rem","fontWeight":"800","textAlign":"center","marginBottom":"3rem"},"css":".gb-text-feat003{font-size:2.5rem;font-weight:800;text-align:center;margin-bottom:3rem}@media(max-width:768px){.gb-text-feat003{font-size:2rem}}"} -->
        <h2 class="gb-text gb-text-feat003">Why Choose Us</h2>
        <!-- /wp:generateblocks/text -->

        <!-- wp:generateblocks/element {"uniqueId":"feat004","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(3, 1fr)","gap":"2rem"},"css":".gb-element-feat004{display:grid;grid-template-columns:repeat(3, 1fr);gap:2rem}@media(max-width:1024px){.gb-element-feat004{grid-template-columns:repeat(2, 1fr)}}@media(max-width:768px){.gb-element-feat004{grid-template-columns:1fr}}"} -->
        <div class="gb-element gb-element-feat004">

            <!-- Feature cards would be inserted here -->
            <!-- Use wp:pattern to include the feature-card pattern -->

        </div>
        <!-- /wp:generateblocks/element -->

    </div>
    <!-- /wp:generateblocks/element -->

</section>
<!-- /wp:generateblocks/element -->
```

## Advanced Patterns

### Pattern with Placeholders

Use content lock and placeholder text for user customization:

```html
<?php
/**
 * Title: Testimonial
 * Slug: theme-slug/testimonial
 * Categories: theme-layouts
 */
?>

<!-- wp:generateblocks/element {"uniqueId":"test001","tagName":"blockquote","styles":{"padding":"2rem","borderLeft":"4px solid #e94560","backgroundColor":"#ffffff","borderRadius":"0 1rem 1rem 0"},"css":".gb-element-test001{padding:2rem;border-left:4px solid #e94560;background-color:#ffffff;border-radius:0 1rem 1rem 0}"} -->
<blockquote class="gb-element gb-element-test001">

    <!-- wp:generateblocks/text {"uniqueId":"test002","tagName":"p","styles":{"fontSize":"1.125rem","fontStyle":"italic","marginBottom":"1rem","lineHeight":"1.7"},"css":".gb-text-test002{font-size:1.125rem;font-style:italic;margin-bottom:1rem;line-height:1.7}"} -->
    <p class="gb-text gb-text-test002">"Add your testimonial text here. Share what your customer loved about your product or service."</p>
    <!-- /wp:generateblocks/text -->

    <!-- wp:generateblocks/element {"uniqueId":"test003","tagName":"footer","styles":{"display":"flex","alignItems":"center","gap":"1rem"},"css":".gb-element-test003{display:flex;align-items:center;gap:1rem}"} -->
    <footer class="gb-element gb-element-test003">

        <!-- wp:generateblocks/media {"uniqueId":"test004","mediaType":"image","htmlAttributes":[{"attribute":"src","value":"https://via.placeholder.com/48"},{"attribute":"alt","value":"Customer photo"}],"styles":{"width":"48px","height":"48px","borderRadius":"50%","objectFit":"cover"},"css":".gb-media-test004{width:48px;height:48px;border-radius:50%;object-fit:cover}"} -->
        <img class="gb-media gb-media-test004" src="https://via.placeholder.com/48" alt="Customer photo" />
        <!-- /wp:generateblocks/media -->

        <!-- wp:generateblocks/element {"uniqueId":"test005","tagName":"div"} -->
        <div class="gb-element">
            <!-- wp:generateblocks/text {"uniqueId":"test006","tagName":"p","styles":{"fontWeight":"600","marginBottom":"0"},"css":".gb-text-test006{font-weight:600;margin-bottom:0}"} -->
            <p class="gb-text gb-text-test006">Customer Name</p>
            <!-- /wp:generateblocks/text -->

            <!-- wp:generateblocks/text {"uniqueId":"test007","tagName":"p","styles":{"fontSize":"0.875rem","color":"#666666"},"css":".gb-text-test007{font-size:0.875rem;color:#666666}"} -->
            <p class="gb-text gb-text-test007">Position, Company</p>
            <!-- /wp:generateblocks/text -->
        </div>
        <!-- /wp:generateblocks/element -->

    </footer>
    <!-- /wp:generateblocks/element -->

</blockquote>
<!-- /wp:generateblocks/element -->
```

### Nested Pattern Reference

```html
<!-- Include another pattern within a pattern -->
<!-- wp:pattern {"slug":"theme-slug/feature-card"} /-->
```

## Pattern Attributes

### Full Attribute Reference

```php
register_block_pattern( 'namespace/pattern-name', array(
    'title'         => __( 'Pattern Title', 'text-domain' ),
    'description'   => __( 'Pattern description', 'text-domain' ),
    'content'       => '<!-- Block markup -->',
    'categories'    => array( 'category-slug' ),
    'keywords'      => array( 'keyword1', 'keyword2' ),
    'blockTypes'    => array( 'core/post-content' ),
    'postTypes'     => array( 'post', 'page' ),
    'templateTypes' => array( 'front-page', 'single' ),
    'inserter'      => true,  // Show in inserter
    'source'        => 'plugin', // Source attribution
    'viewportWidth' => 1400,  // Preview width
) );
```

## Best Practices

### 1. Unique IDs

Generate unique IDs per pattern instance:

```php
// Generate unique prefix for pattern
function theme_generate_pattern_id( $prefix = 'pat' ) {
    return $prefix . substr( md5( uniqid() ), 0, 6 );
}
```

### 2. Semantic Structure

- Use appropriate tagNames (section, article, header, etc.)
- Include proper heading hierarchy
- Add ARIA attributes where needed

### 3. Responsive Design

Always include responsive breakpoints in CSS:

```css
.selector{/* desktop */}
@media(max-width:1024px){.selector{/* tablet */}}
@media(max-width:768px){.selector{/* mobile */}}
```

### 4. Performance

- Minimize inline CSS
- Use efficient selectors
- Avoid unnecessary nesting

### 5. Maintainability

- Keep patterns in separate files
- Use clear naming conventions
- Document pattern purpose

## Pattern Organization

### Recommended File Structure

```
theme/
├── patterns/
│   ├── hero-default.html
│   ├── hero-centered.html
│   ├── card-feature.html
│   ├── card-testimonial.html
│   ├── grid-three-column.html
│   ├── cta-newsletter.html
│   └── footer-simple.html
├── inc/
│   └── pattern-categories.php
└── functions.php
```

### Category Registration File

```php
<?php
// inc/pattern-categories.php
function theme_pattern_categories() {
    $categories = array(
        'theme-hero'    => __( 'Hero Sections', 'theme' ),
        'theme-cards'   => __( 'Cards', 'theme' ),
        'theme-grids'   => __( 'Grids', 'theme' ),
        'theme-cta'     => __( 'Call to Action', 'theme' ),
        'theme-footer'  => __( 'Footers', 'theme' ),
    );

    foreach ( $categories as $slug => $label ) {
        register_block_pattern_category( $slug, array( 'label' => $label ) );
    }
}
add_action( 'init', 'theme_pattern_categories' );
```

## GenerateBlocks Pro Pattern Library

GenerateBlocks Pro includes a built-in pattern library with:

- Cloud-synced patterns
- Pattern collections
- One-click import
- Style customization

Access via: **GenerateBlocks > Pattern Library**

## Troubleshooting

### Pattern Not Showing

1. Check category registration order (categories before patterns)
2. Verify pattern content is valid block markup
3. Check `inserter` is not set to `false`
4. Clear block editor cache

### Styling Issues

1. Verify unique IDs don't conflict
2. Check CSS selector specificity
3. Ensure styles are properly minified
4. Test responsive breakpoints

### Content Issues

1. Escape HTML entities in content
2. Use proper quote escaping in attributes
3. Validate JSON in block attributes
