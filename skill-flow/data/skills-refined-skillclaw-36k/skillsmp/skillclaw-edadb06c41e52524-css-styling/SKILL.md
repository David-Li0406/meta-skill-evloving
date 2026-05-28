---
name: css-styling
description: Use this skill when you need to implement consistent CSS styling patterns for the MotoRent application using `mr-*` prefixed classes.
---

# MotoRent CSS Styling Patterns

This skill documents the CSS styling conventions using `mr-` prefixed classes for consistent UI across the application.

## CSS Location
All custom styles are in: `src/MotoRent.Server/wwwroot/css/site.css`

## Naming Convention
- All MotoRent-specific CSS classes use the `mr-` prefix.
- Tabler/Bootstrap variables use the `--tblr-` prefix.
- MotoRent CSS variables use the `--mr-` prefix.

## Brand Colors
```css
--tblr-primary: #00897B;        /* Tropical Teal */
--tblr-primary-darken: #00695C;
--tblr-primary-lighten: #4DB6AC;
--tblr-secondary: #FF7043;      /* Deep Orange */
```

## Page Header with Breadcrumb

Compact page header with breadcrumb navigation and subtle background.

```html
<div class="mr-page-header">
    <div class="container-xl">
        <nav class="mr-breadcrumb">
            <span class="mr-breadcrumb-item"><a href="/"><i class="ti ti-home"></i></a></span>
            <span class="mr-breadcrumb-separator"><i class="ti ti-chevron-right"></i></span>
            <span class="mr-breadcrumb-item"><a href="/section">Section</a></span>
            <span class="mr-breadcrumb-separator"><i class="ti ti-chevron-right"></i></span>
            <span class="mr-breadcrumb-item active">Current Page</span>
        </nav>
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h1 class="mr-page-title"><i class="ti ti-icon"></i> Title</h1>
                <p class="mr-page-subtitle">Subtitle</p>
            </div>
            <a href="/back" class="mr-btn-header-action">
                <i class="ti ti-arrow-left"></i> Back
            </a>
        </div>
    </div>
</div>
```

### CSS Classes
```css
.mr-page-header {
    background: var(--mr-bg-header-gradient);  /* Light gray, not teal */
    border-bottom: 1px solid var(--mr-border-default);
    padding: 0.75rem 0 0;
}

.mr-page-title { color: var(--mr-text-primary); font-size: 1.5rem; }
.mr-page-title i { color: var(--mr-accent-primary); }  /* Teal icon */
.mr-page-subtitle { color: var(--mr-text-muted); }

.mr-breadcrumb-item a { color: var(--mr-text-muted); }
.mr-breadcrumb-item a:hover { color: var(--mr-accent-primary); }

.mr-btn-header-action {
    background: var(--mr-bg-card);
    border: 1px solid var(--mr-border-default);
    color: var(--mr-text-secondary);
}
```