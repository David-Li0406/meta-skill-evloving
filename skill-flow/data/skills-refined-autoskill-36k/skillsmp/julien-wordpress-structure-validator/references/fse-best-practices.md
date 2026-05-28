# WordPress FSE Best Practices

Comprehensive guide to Full Site Editing theme development best practices.

## Template Development

### Homepage Templates

**✅ DO**:
- Use `front-page.html` OR `page-{slug}.html` for custom homepage
- Remove Featured Image display if content already includes imagery
- Keep homepage template minimal - let content drive the layout
- Use `<!-- wp:post-content /-->` to render page content

**❌ DON'T**:
- Use generic `page.html` for homepage (not specific enough)
- Add both template parts AND hardcoded header/footer
- Include excessive spacers/padding in template (use content blocks instead)

**Example minimal homepage template** (`page-accueil.html`):
```html
<!-- wp:template-part {"slug":"header","area":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main"} -->
<main class="wp-block-group">
	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","area":"footer","tagName":"footer"} /-->
```

### Standard Page Template

**✅ DO**:
- Include post title display
- Show Featured Image (good for SEO/social sharing)
- Add appropriate spacing
- Use semantic HTML5 tags (`<main>`, `<article>`)

**Example** (`page.html`):
```html
<!-- wp:template-part {"slug":"header"} /-->

<!-- wp:group {"tagName":"main"} -->
<main class="wp-block-group">
	<!-- wp:group {"layout":{"type":"constrained"}} -->
	<div class="wp-block-group">

		<!-- wp:spacer {"height":"var:preset|spacing|50"} -->
		<div style="height:var(--wp--preset--spacing--50)" class="wp-block-spacer"></div>
		<!-- /wp:spacer -->

		<!-- wp:post-title {"level":1} /-->

		<!-- wp:post-featured-image /-->

		<!-- wp:post-content {"layout":{"type":"constrained"}} /-->

	</div>
	<!-- /wp:group -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer"} /-->
```

## theme.json Configuration

### Required Structure

**✅ DO**:
- Always include `version` field (2 or 3)
- Define complete color palette with semantic names
- Set up spacing scale for consistency
- Configure typography settings
- Ensure all colors meet WCAG AA contrast (4.5:1 minimum)

**❌ DON'T**:
- Use hardcoded colors in templates
- Skip color naming (use semantic names, not "color1", "color2")
- Ignore accessibility (contrast ratios)

**Example minimal theme.json**:
```json
{
  "version": 3,
  "settings": {
    "color": {
      "palette": [
        {"slug": "primary", "color": "#5b2e7f", "name": "Primary"},
        {"slug": "secondary", "color": "#f89420", "name": "Secondary"},
        {"slug": "white", "color": "#ffffff", "name": "White"},
        {"slug": "black", "color": "#000000", "name": "Black"}
      ]
    },
    "typography": {
      "fontSizes": [
        {"slug": "small", "size": "0.875rem", "name": "Small"},
        {"slug": "base", "size": "1rem", "name": "Base"},
        {"slug": "large", "size": "1.5rem", "name": "Large"}
      ]
    },
    "spacing": {
      "units": ["px", "rem", "vh"],
      "spacingSizes": [
        {"slug": "10", "size": "0.5rem", "name": "XS"},
        {"slug": "20", "size": "1rem", "name": "S"},
        {"slug": "30", "size": "2rem", "name": "M"}
      ]
    }
  }
}
```

### Color Accessibility

**WCAG AA Requirements** (minimum 4.5:1 contrast):
- Text on background
- Interactive elements (buttons, links)

**WCAG AAA Requirements** (7:1 contrast):
- Large text (18pt+ regular, 14pt+ bold)
- Enhanced accessibility mode

**Testing tools**:
- WebAIM Contrast Checker
- Chrome DevTools (Lighthouse)
- `culori` library (OKLCH color space)

## Block Styles

### Registration

**✅ DO**:
- Register block styles in `functions.php` via `register_block_style()`
- Use semantic, descriptive names (e.g., `violet-title`, `hero-section`)
- Add both `name` and `label` properties
- Use inline styles for simple CSS, external files for complex styles

**❌ DON'T**:
- Add custom classes directly in Gutenberg (not reusable)
- Use vague names (e.g., `style1`, `custom`)
- Duplicate styles across multiple functions

**Example registration**:
```php
register_block_style(
    'core/heading',
    array(
        'name' => 'violet-title',
        'label' => __('Titre Violet', 'theme-slug'),
        'inline_style' => '
            .wp-block-heading.is-style-violet-title {
                color: var(--wp--preset--color--violet-500);
            }
        '
    )
);
```

### External CSS for Complex Styles

**When to use `wp_enqueue_block_style()`**:
- Styles > 10 lines of CSS
- Styles requiring media queries
- Styles with pseudo-elements (::before, ::after)
- Styles with animations/transitions

**Example**:
```php
wp_enqueue_block_style(
    'core/button',
    array(
        'handle' => 'theme-button-outline',
        'src' => get_template_directory_uri() . '/assets/css/button-outline.css',
        'ver' => '1.0.0',
        'path' => get_template_directory_path() . '/assets/css/button-outline.css'
    )
);
```

## Featured Images

### Usage

**✅ DO**:
- Set Featured Image for ALL pages (SEO, social sharing)
- Use appropriate image sizes (minimum 1200x630 for social)
- Optimize images (WebP format, compression)
- Add alt text for accessibility

**❌ DON'T**:
- Display Featured Image if page content already has hero image
- Skip Featured Image (breaks Open Graph metadata)
- Use low-resolution images (<800px width)

### Template Handling

If page content includes hero image, **hide Featured Image in template**:

Option 1: Custom template without Featured Image block
Option 2: CSS (less preferred)
```css
.page-id-5 .wp-block-post-featured-image {
    display: none;
}
```

### Setting via WP-CLI

```bash
# Upload image
wp media import /path/to/image.jpg --title="Page Title" --allow-root

# Get image ID from output (e.g., 42)

# Set as featured image
wp post meta update 5 _thumbnail_id 42 --allow-root
```

## File Organization

### Directory Structure

```
theme-name/
├── style.css               ← Required theme metadata
├── theme.json              ← FSE configuration
├── functions.php           ← Theme functions
├── templates/              ← Page templates
│   ├── index.html         ← REQUIRED fallback
│   ├── page.html
│   ├── single.html
│   └── 404.html
├── parts/                  ← Template parts
│   ├── header.html
│   └── footer.html
├── patterns/               ← Block patterns
│   └── hero-section.php
├── styles/                 ← Theme style variations
│   └── dark.json
└── assets/                 ← Static assets
    ├── css/
    ├── js/
    └── images/
```

### File Permissions (Docker/VPS)

**Correct ownership**:
```bash
chown -R www-data:www-data /var/www/html/wp-content/themes/theme-name/
```

**Correct permissions**:
- Files: `644` (rw-r--r--)
- Directories: `755` (rwxr-xr-x)

```bash
find theme-name/ -type f -exec chmod 644 {} \;
find theme-name/ -type d -exec chmod 755 {} \;
```

## Performance

### CSS Enqueuing

**✅ DO**:
- Use version numbers for cache busting
- Load only necessary CSS per page
- Concatenate small CSS files
- Use `wp_enqueue_block_style()` for block-specific CSS (loads only when block used)

**❌ DON'T**:
- Load all CSS on all pages
- Forget version numbers (browser caching issues)
- Inline huge CSS blocks in `functions.php`

**Example with versioning**:
```php
wp_enqueue_style(
    'theme-custom',
    get_template_directory_uri() . '/assets/css/custom.css',
    array(),
    wp_get_theme()->get('Version') // Dynamic versioning
);
```

### Image Optimization

**✅ DO**:
- Use modern formats (WebP, AVIF)
- Implement lazy loading
- Define responsive image sizes in `functions.php`
- Compress images (TinyPNG, ImageOptim)

**Add custom image sizes**:
```php
add_image_size('hero', 1920, 800, true);
add_image_size('card', 600, 400, true);
```

## Accessibility

### WCAG AA Compliance Checklist

- [ ] All text meets 4.5:1 contrast ratio
- [ ] Focus visible on all interactive elements
- [ ] Keyboard navigation works throughout site
- [ ] Images have meaningful alt text
- [ ] Semantic HTML5 elements used (`<header>`, `<main>`, `<nav>`, `<footer>`)
- [ ] ARIA labels where needed
- [ ] Forms have associated labels
- [ ] Color not sole means of conveying information

### Testing

**Tools**:
- Lighthouse (Chrome DevTools)
- WAVE browser extension
- axe DevTools
- Keyboard-only navigation testing

## Common Anti-Patterns

### ❌ DON'T: Duplicate Content in Template

Bad:
```html
<!-- Template with hardcoded content -->
<main>
    <h1>Welcome to Our Site</h1>
    <p>Lorem ipsum dolor sit amet...</p>
    <!-- wp:post-content /-->
</main>
```

Good:
```html
<!-- Template that renders page content -->
<main>
    <!-- wp:post-content /-->
</main>
```

### ❌ DON'T: Excessive Inline Styles

Bad:
```php
'inline_style' => '
    /* 200 lines of CSS... */
'
```

Good:
```php
wp_enqueue_block_style('core/group', array(
    'handle' => 'theme-complex-style',
    'src' => get_template_directory_uri() . '/assets/css/complex-style.css'
));
```

### ❌ DON'T: Ignore Template Hierarchy

Bad: Creating `services.html` (won't work)

Good: Creating `page-services.html` (follows convention)

## Deployment Checklist

Before deploying to production:

- [ ] Run template validator (`validate_templates.sh`)
- [ ] Validate theme.json (`check_theme_json.py`)
- [ ] Check block styles (`check_block_styles.sh`)
- [ ] Test all page templates
- [ ] Verify featured images set
- [ ] Check file permissions (Docker/VPS)
- [ ] Run Lighthouse audit (Performance, Accessibility, SEO)
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Validate HTML (W3C Validator)
- [ ] Check cross-browser compatibility

## References

- [WordPress Block Theme Documentation](https://developer.wordpress.org/themes/block-themes/)
- [theme.json Reference](https://developer.wordpress.org/themes/global-settings-and-styles/theme-json/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
