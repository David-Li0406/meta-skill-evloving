# WordPress Template Hierarchy (FSE)

Complete guide to WordPress Full Site Editing template hierarchy and resolution order.

## Template Resolution Order

WordPress resolves templates using a hierarchical fallback system. It searches for the most specific template first, falling back to more generic templates if needed.

### Homepage Templates

**When homepage is set to a static page** (Settings > Reading > "A static page"):

1. `front-page.html` - Specific homepage template
2. `page-{slug}.html` - Template named after page slug (e.g., `page-accueil.html`)
3. `page-{id}.html` - Template named after page ID (e.g., `page-5.html`)
4. Custom template assigned via `_wp_page_template` metakey
5. `page.html` - Generic page template
6. `index.html` - Universal fallback **(REQUIRED)**

**When homepage displays latest posts** (Settings > Reading > "Your latest posts"):

1. `home.html` - Blog homepage template
2. `index.html` - Universal fallback

### Page Templates

For any standard WordPress page:

1. Custom template assigned in page editor (stored in `_wp_page_template` metakey)
2. `page-{slug}.html` - Template named after page slug
3. `page-{id}.html` - Template named after page ID
4. `page.html` - Generic page template
5. `index.html` - Universal fallback

**Example**: Page with slug "services" (ID 6)
```
page-services.html  ← Most specific
page-6.html
page.html
index.html          ← Fallback
```

### Single Post Templates

For individual blog posts or custom post types:

1. `single-{post-type}-{slug}.html` - Post type + slug specific
2. `single-{post-type}.html` - Post type specific
3. `single.html` - Generic single post template
4. `index.html` - Universal fallback

**Example**: Custom post type "project" with slug "new-website"
```
single-project-new-website.html
single-project.html
single.html
index.html
```

### Archive Templates

For category, tag, date, and author archives:

**Category archives**:
1. `category-{slug}.html`
2. `category-{id}.html`
3. `category.html`
4. `archive.html`
5. `index.html`

**Tag archives**:
1. `tag-{slug}.html`
2. `tag-{id}.html`
3. `tag.html`
4. `archive.html`
5. `index.html`

**Custom taxonomy**:
1. `taxonomy-{taxonomy}-{term}.html`
2. `taxonomy-{taxonomy}.html`
3. `taxonomy.html`
4. `archive.html`
5. `index.html`

**Author archives**:
1. `author-{nicename}.html`
2. `author-{id}.html`
3. `author.html`
4. `archive.html`
5. `index.html`

**Date archives**:
1. `date.html`
2. `archive.html`
3. `index.html`

**Post type archives**:
1. `archive-{post-type}.html`
2. `archive.html`
3. `index.html`

### Search Results

1. `search.html`
2. `index.html`

### 404 (Not Found)

1. `404.html`
2. `index.html`

## Required Templates

Only **one template is required** for a functional WordPress FSE theme:

- **`index.html`** - Universal fallback template

All other templates are optional but recommended based on site needs.

## Minimum Recommended Templates

For a basic website (no blog):
```
templates/
├── index.html          ← REQUIRED
├── page.html           ← For standard pages
├── page-accueil.html   ← Custom homepage (optional)
└── 404.html            ← Not found page (optional)
```

For a blog website:
```
templates/
├── index.html          ← REQUIRED
├── page.html           ← For standard pages
├── home.html           ← Blog homepage
├── single.html         ← Individual posts
├── archive.html        ← Category/tag archives
├── search.html         ← Search results
└── 404.html            ← Not found page
```

## Template Parts

Template parts are reusable sections included in templates. They live in the `parts/` directory.

**Common template parts**:
- `parts/header.html` - Site header/navigation
- `parts/footer.html` - Site footer
- `parts/sidebar.html` - Sidebar content
- `parts/comments.html` - Comments section

**Usage in templates**:
```html
<!-- wp:template-part {"slug":"header","area":"header","tagName":"header"} /-->
```

## Custom Template Assignment

Templates can be manually assigned to pages in three ways:

### 1. Via WordPress Admin
1. Edit page in Gutenberg editor
2. Right sidebar > Template section
3. Select from dropdown
4. Save page

### 2. Via Database
```sql
UPDATE wp_postmeta
SET meta_value = 'page-custom.html'
WHERE post_id = 5 AND meta_key = '_wp_page_template';
```

### 3. Via WP-CLI
```bash
wp post meta update 5 _wp_page_template 'page-custom.html' --allow-root
```

## Template Naming Conventions

**Valid naming patterns**:
- `{type}.html` - Generic template (e.g., `page.html`, `single.html`)
- `{type}-{subtype}.html` - Specific template (e.g., `single-project.html`)
- `{type}-{subtype}-{identifier}.html` - Very specific (e.g., `page-services.html`)
- Special cases: `front-page.html`, `home.html`, `404.html`, `search.html`

**Invalid patterns** (will not be recognized):
- `my-custom-page.html` (doesn't follow conventions)
- `services.html` (missing `page-` prefix)
- `blog-post.html` (should be `single.html` or `single-post.html`)

## Best Practices

1. **Always include `index.html`** - It's the only required template
2. **Use semantic naming** - Follow WordPress conventions
3. **Create specific templates for important pages** - E.g., `page-accueil.html` for homepage
4. **Don't over-template** - Only create templates you actually need
5. **Use template parts** - For shared header/footer across templates
6. **Document custom templates** - Add comments explaining purpose
7. **Test fallback behavior** - Ensure generic templates work when specific ones don't exist

## Checking Active Template

To see which template is being used for a page:

### Via WordPress Admin
1. Edit the page
2. Right sidebar > Summary > Template section
3. Shows current template name

### Via Query Monitor Plugin
Install Query Monitor plugin - it shows the active template file in the admin bar.

### Via Code
```php
// In template file
global $template;
echo basename($template);
```

## References

- [WordPress Template Hierarchy Documentation](https://developer.wordpress.org/themes/basics/template-hierarchy/)
- [Block Theme Template Files](https://developer.wordpress.org/themes/block-themes/templates-and-template-parts/)
- [Template Part Blocks](https://developer.wordpress.org/block-editor/reference-guides/core-blocks/#template-part)
