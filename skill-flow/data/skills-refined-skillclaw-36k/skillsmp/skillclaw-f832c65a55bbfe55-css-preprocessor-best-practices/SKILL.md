---
name: css-preprocessor-best-practices
description: Use this skill when you want to implement best practices for maintainable and scalable stylesheets using CSS preprocessors like Less, Sass, or SCSS.
---

# CSS Preprocessor Best Practices

You are an expert in CSS preprocessors (Less, Sass, SCSS), CSS architecture, and maintainable stylesheet development.

## Key Principles

- Write modular, reusable code that leverages variables, mixins, and functions.
- Follow consistent naming conventions and file organization to enhance readability and maintainability.
- Keep specificity low and avoid overly complex selectors.
- Prioritize simplicity and clarity in style organization, adhering to the DRY (Don't Repeat Yourself) principle.

## File Organization

### Project Structure
```
<preprocessor>/
├── abstracts/
│   ├── _variables.<ext>    # Global variables
│   ├── _mixins.<ext>       # Reusable mixins
│   ├── _functions.<ext>    # Functions
│   └── _placeholders.<ext>  # Extendable placeholders
├── base/
│   ├── _reset.<ext>        # CSS reset/normalize
│   ├── _typography.<ext>   # Typography rules
│   └── _base.<ext>         # Base element styles
├── components/
│   ├── _buttons.<ext>      # Button components
│   ├── _cards.<ext>        # Card components
│   └── _forms.<ext>        # Form components
├── layout/
│   ├── _header.<ext>       # Header layout
│   ├── _footer.<ext>       # Footer layout
│   ├── _grid.<ext>         # Grid system
│   └── _navigation.<ext>   # Navigation layout
├── pages/
│   ├── _home.<ext>         # Home page specific
│   └── _contact.<ext>      # Contact page specific
├── themes/
│   └── _default.<ext>      # Default theme
├── vendors/
│   └── _normalize.<ext>    # Third-party styles
└── main.<ext>              # Main manifest file
```
*Replace `<preprocessor>` with `less`, `sass`, or `scss` and `<ext>` with the appropriate file extension.*

### Main Manifest
```scss
// main.<ext>
@use 'abstracts/variables';
@use 'abstracts/functions';
@use 'abstracts/mixins';
@use 'abstracts/placeholders';

@use 'vendors/normalize';

@use 'base/reset';
@use 'base/typography';
@use 'base/base';

@use 'layout/grid';
@use 'layout/header';
@use 'layout/navigation';
@use 'layout/footer';

@use 'components/buttons';
@use 'components/cards';
@use 'components/forms';

@use 'pages/home';

@use 'themes/default';
```

## Variables

### Naming Convention
```scss
// _variables.<ext>

// Colors
$color-primary: #3498db;
$color-primary-light: lighten($color-primary, 15%);
$color-primary-dark: darken($color-primary, 15%);
$color-secondary: #2ecc71;
$color-text: #333333;
$color-text-muted: #666666;
$color-background: #ffffff;
$color-border: #e0e0e0;
$color-error: #e74c3c;
$color-success: #27ae60;
$color-warning: #f39c12;
```
*Use semantic names for variables to enhance clarity and maintainability.*