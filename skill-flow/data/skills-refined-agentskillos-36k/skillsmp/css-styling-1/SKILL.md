---
name: css-styling
description: MotoRent CSS styling patterns using mr-* prefixed classes for consistent UI components, gradients, and theme support.
context: fork
---

# MotoRent CSS Styling Patterns

This skill documents the CSS styling conventions using `mr-` prefixed classes for consistent UI across the application.

## CSS Location
All custom styles are in: `src/MotoRent.Server/wwwroot/css/site.css`

## Naming Convention
- All MotoRent-specific CSS classes use `mr-` prefix
- Tabler/Bootstrap variables use `--tblr-` prefix
- MotoRent CSS variables use `--mr-` prefix

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

## Component Classes

### Primary Action Button
```css
.mr-btn-primary-action {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
    color: white;
    border-radius: 10px;
    font-weight: 500;
    text-decoration: none;
    box-shadow: 0 4px 14px rgba(0, 137, 123, 0.25);
    transition: all 0.2s ease;
}
```

### Status Badges
```css
.mr-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
}

/* Variants: mr-status-badge-success, mr-status-badge-warning, mr-status-badge-danger */
```

### Field Labels
```css
.mr-field-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--mr-text-muted);
}

.mr-field-value {
    font-size: 14px;
    color: var(--mr-text-primary);
}

.mr-mono { font-family: 'JetBrains Mono', monospace; }
.mr-highlight { color: var(--mr-accent-primary); font-weight: 600; }
```

### Cards
```css
.mr-card {
    background: var(--mr-bg-card);
    border: 1px solid var(--mr-border-default);
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 6px 16px rgba(0,0,0,0.06);
}
```

## Form Panels & Inputs

### Form Panel Structure
```html
<div class="mr-form-panel">
    <div class="mr-form-panel-header">
        <div class="mr-form-panel-header-icon"><i class="ti ti-send"></i></div>
        <h3 class="mr-form-panel-title">New Request</h3>
    </div>
    <div class="mr-form-panel-body">
        <!-- Form content -->
    </div>
    <div class="mr-form-panel-footer">
        <button class="mr-btn-cancel">Cancel</button>
        <button class="mr-btn-submit"><i class="ti ti-send"></i> Submit</button>
    </div>
</div>
```

### Input with Prefix (Currency)
```html
<div class="mr-input-group">
    <span class="mr-input-group-text">RM</span>
    <input type="text" class="mr-form-control mr-mono" placeholder="0.00">
</div>
```

### Info Highlight Box (Blue Gradient)
```html
<div class="mr-info-highlight">
    <div class="mr-info-highlight-icon"><i class="ti ti-wallet"></i></div>
    <div class="mr-info-highlight-content">
        <div class="mr-info-highlight-label">YOUR ELIGIBLE AMOUNT</div>
        <div class="mr-info-highlight-value">RM 500.00</div>
    </div>
</div>
```

### Quick Select Buttons
```html
<div class="mr-quick-select">
    <button class="mr-quick-select-btn">RM 50.00</button>
    <button class="mr-quick-select-btn active">RM 100.00</button>
    <button class="mr-quick-select-btn">MAX</button>
</div>
```

### File Upload Area
```html
<div class="mr-file-upload">
    <div class="mr-file-upload-inner">
        <div class="mr-file-upload-icon"><i class="ti ti-cloud-upload"></i></div>
        <div class="mr-file-upload-text">
            <span class="mr-file-upload-link">Click to upload</span> or drag and drop
        </div>
        <div class="mr-file-upload-hint">PDF, JPG, PNG or DOC (max. 5MB)</div>
    </div>
</div>
```

### Detail Rows (Label/Value pairs)
```html
<div class="mr-detail-row">
    <span class="mr-detail-label">Policy Type</span>
    <span class="mr-detail-badge">Advance Payroll</span>
</div>
<div class="mr-detail-row">
    <span class="mr-detail-label">Maximum Limit</span>
    <span class="mr-detail-value mr-mono mr-blue">RM 500.00</span>
</div>
```

## Border Radius Standards
- Cards: `16px`
- Buttons: `10px`
- Badges: `20px` (pill) or `8px`
- Inputs: `10px`
- Icon containers: `12px`

## CSS Variables Reference

### Light Theme
```css
:root {
    --mr-bg-card: #ffffff;
    --mr-border-default: #e2e8f0;
    --mr-text-primary: #1e293b;
    --mr-text-secondary: #475569;
    --mr-text-muted: #94a3b8;
    --mr-accent-primary: #0f766e;
    --mr-accent-light: #14b8a6;
}
```

### Dark Theme
```css
[data-bs-theme="dark"] {
    --mr-bg-card: #1e293b;
    --mr-border-default: #334155;
    --mr-text-primary: #f1f5f9;
    --mr-text-secondary: #cbd5e1;
    --mr-text-muted: #64748b;
}
```

See `instructions.md` for complete documentation with all classes and examples.
