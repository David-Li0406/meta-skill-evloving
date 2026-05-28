---
name: css-best-practices
description: Use this skill when developing maintainable, modular stylesheets with CSS preprocessors like Less, Sass, or SCSS.
---

# CSS Best Practices

You are an expert in CSS preprocessors (Less, Sass, SCSS), CSS architecture, and maintainable stylesheet development.

## Key Principles

- Write modular, reusable styles that leverage variables, mixins, and functions.
- Follow consistent naming conventions and file organization.
- Keep specificity low and avoid overly complex selectors.
- Prioritize readability and maintainability.

## File Organization

### Project Structure
```
<preprocessor>/
├── abstracts/
│   ├── _variables.<ext>      # Global variables
│   ├── _mixins.<ext>         # Reusable mixins
│   ├── _functions.<ext>      # Functions
│   └── _placeholders.<ext>   # Extendable placeholders
├── base/
│   ├── _reset.<ext>          # CSS reset/normalize
│   ├── _typography.<ext>     # Typography rules
│   └── _base.<ext>           # Base element styles
├── components/
│   ├── _buttons.<ext>        # Button components
│   ├── _cards.<ext>          # Card components
│   └── _forms.<ext>          # Form components
├── layout/
│   ├── _header.<ext>         # Header layout
│   ├── _footer.<ext>         # Footer layout
│   ├── _grid.<ext>           # Grid system
│   └── _navigation.<ext>     # Navigation layout
├── pages/
│   ├── _home.<ext>           # Home page specific
│   └── _contact.<ext>        # Contact page specific
├── themes/
│   └── _default.<ext>        # Default theme
├── vendors/
│   └── _normalize.<ext>      # Third-party styles
└── main.<ext>                # Main manifest file
```

### Main Manifest
```<preprocessor>
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
```<preprocessor>
// Colors
$color-primary: #3498db;
$color-primary-light: lighten($color-primary, 15%);
$color-primary-dark: darken($color-primary, 15%);
$color-secondary: #2ecc71;
$color-text: #333333;
$color-background: #ffffff;

// Typography
$font-family-base: 'Helvetica Neue', Arial, sans-serif;
$font-size-base: 1rem;
$font-size-small: 0.875rem;
$font-weight-normal: 400;
$font-weight-bold: 700;

// Spacing Scale
$spacing-unit: 8px;
$spacing-xs: $spacing-unit * 0.5;   // 4px
$spacing-sm: $spacing-unit;          // 8px
$spacing-md: $spacing-unit * 2;      // 16px
$spacing-lg: $spacing-unit * 3;      // 24px
$spacing-xl: $spacing-unit * 4;      // 32px
```

## Mixins

### Responsive Design
```<preprocessor>
@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  } @else {
    @warn "Unknown breakpoint: #{$breakpoint}";
  }
}

// Usage
.element {
  width: 100%;

  @include respond-to('md') {
    width: 50%;
  }
}
```

### Flexbox Utilities
```<preprocessor>
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

// Usage
.container {
  @include flex-center;
  min-height: 100vh;
}
```

## BEM Naming Convention

```<preprocessor>
// Block
.card {
  background: $color-background;
  border-radius: $border-radius-md;

  // Element
  &__header {
    padding: $spacing-md;
  }

  &__title {
    margin: 0;
    font-size: $font-size-large;
  }

  // Modifier
  &--featured {
    border: 2px solid $color-primary;
  }
}
```

## Nesting Guidelines

### Keep Nesting Shallow
```<preprocessor>
// BAD: Too deep nesting
.nav {
  .nav-list {
    .nav-item {
      .nav-link {
        // 4 levels deep - avoid this
      }
    }
  }
}

// GOOD: Flat BEM structure
.nav {
  display: flex;
}

.nav__list {
  display: flex;
  list-style: none;
}
```

## Performance Best Practices

- Avoid deeply nested selectors (max 3 levels).
- Keep specificity low - prefer single class selectors.
- Never use `!important` except for utility overrides.
- Compile to compressed CSS in production.
- Enable source maps in development only.

## Code Style Guidelines

- Use 2 spaces for indentation.
- Use single quotes for strings.
- Add a space after colons in declarations.
- Separate rule sets with blank lines.
- Order properties consistently (positioning, box model, typography, visual, misc).
- Comment complex logic.