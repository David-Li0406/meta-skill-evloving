# GenerateBlocks Global Styles Skill

Manage global styling system, design tokens, and consistent theming across GenerateBlocks layouts.

## When to Use This Skill

- Setting up global colors, typography, and spacing
- Creating reusable style presets
- Integrating with WordPress theme.json
- Building consistent design systems

## Global Styles Overview

GenerateBlocks provides multiple layers of styling:

1. **WordPress theme.json** - Site-wide design tokens
2. **GenerateBlocks Settings** - Plugin-level defaults
3. **Global Classes** - Reusable style sets
4. **Block Styles** - Individual block settings
5. **Inline CSS** - Per-block custom styles

## Theme.json Integration

### Basic theme.json Structure

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "color": {
      "palette": [],
      "gradients": [],
      "custom": true
    },
    "typography": {
      "fontFamilies": [],
      "fontSizes": [],
      "customFontSize": true
    },
    "spacing": {
      "spacingSizes": [],
      "units": ["px", "rem", "%", "vh", "vw"]
    },
    "layout": {
      "contentSize": "1200px",
      "wideSize": "1400px"
    }
  },
  "styles": {}
}
```

### Color Palette

```json
{
  "settings": {
    "color": {
      "palette": [
        {
          "slug": "primary",
          "color": "#0073aa",
          "name": "Primary"
        },
        {
          "slug": "secondary",
          "color": "#23282d",
          "name": "Secondary"
        },
        {
          "slug": "accent",
          "color": "#e94560",
          "name": "Accent"
        },
        {
          "slug": "background",
          "color": "#ffffff",
          "name": "Background"
        },
        {
          "slug": "foreground",
          "color": "#0a0a0a",
          "name": "Foreground"
        },
        {
          "slug": "muted",
          "color": "#f8f9fa",
          "name": "Muted"
        },
        {
          "slug": "border",
          "color": "#e5e5e5",
          "name": "Border"
        }
      ]
    }
  }
}
```

### Typography Settings

```json
{
  "settings": {
    "typography": {
      "fontFamilies": [
        {
          "slug": "system",
          "name": "System Font",
          "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        },
        {
          "slug": "heading",
          "name": "Heading Font",
          "fontFamily": "'Inter', sans-serif",
          "fontFace": [
            {
              "fontFamily": "Inter",
              "fontWeight": "400 900",
              "fontStyle": "normal",
              "fontDisplay": "swap",
              "src": ["file:./assets/fonts/inter-variable.woff2"]
            }
          ]
        },
        {
          "slug": "mono",
          "name": "Monospace",
          "fontFamily": "'JetBrains Mono', monospace"
        }
      ],
      "fontSizes": [
        { "slug": "xs", "size": "0.75rem", "name": "Extra Small" },
        { "slug": "sm", "size": "0.875rem", "name": "Small" },
        { "slug": "base", "size": "1rem", "name": "Base" },
        { "slug": "lg", "size": "1.125rem", "name": "Large" },
        { "slug": "xl", "size": "1.25rem", "name": "XL" },
        { "slug": "2xl", "size": "1.5rem", "name": "2XL" },
        { "slug": "3xl", "size": "2rem", "name": "3XL" },
        { "slug": "4xl", "size": "2.5rem", "name": "4XL" },
        { "slug": "5xl", "size": "3rem", "name": "5XL" }
      ]
    }
  }
}
```

### Spacing Scale

```json
{
  "settings": {
    "spacing": {
      "spacingSizes": [
        { "slug": "xs", "size": "0.5rem", "name": "XS" },
        { "slug": "sm", "size": "1rem", "name": "Small" },
        { "slug": "md", "size": "1.5rem", "name": "Medium" },
        { "slug": "lg", "size": "2rem", "name": "Large" },
        { "slug": "xl", "size": "3rem", "name": "XL" },
        { "slug": "2xl", "size": "4rem", "name": "2XL" },
        { "slug": "3xl", "size": "6rem", "name": "3XL" }
      ]
    }
  }
}
```

## CSS Custom Properties

### Generated Variables

theme.json generates CSS custom properties:

```css
:root {
  /* Colors */
  --wp--preset--color--primary: #0073aa;
  --wp--preset--color--secondary: #23282d;
  --wp--preset--color--accent: #e94560;

  /* Typography */
  --wp--preset--font-family--system: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --wp--preset--font-family--heading: 'Inter', sans-serif;
  --wp--preset--font-size--base: 1rem;
  --wp--preset--font-size--lg: 1.125rem;

  /* Spacing */
  --wp--preset--spacing--sm: 1rem;
  --wp--preset--spacing--md: 1.5rem;
  --wp--preset--spacing--lg: 2rem;

  /* Layout */
  --wp--style--global--content-size: 1200px;
  --wp--style--global--wide-size: 1400px;
}
```

### Using Variables in GenerateBlocks

```html
<!-- wp:generateblocks/element {"uniqueId":"var001","tagName":"section","styles":{"padding":"var(--wp--preset--spacing--lg)","backgroundColor":"var(--wp--preset--color--muted)"},"css":".gb-element-var001{padding:var(--wp--preset--spacing--lg);background-color:var(--wp--preset--color--muted)}"} -->
<section class="gb-element gb-element-var001">
    <!-- Content -->
</section>
<!-- /wp:generateblocks/element -->
```

## Global Classes

### What Are Global Classes?

Global Classes are predefined style sets that can be applied to any GenerateBlocks element, providing consistent styling across the site.

### Setting Up Global Classes

In GenerateBlocks settings (GenerateBlocks > Settings > Global Classes):

```json
{
  "globalClasses": [
    {
      "id": "button-primary",
      "name": "Button Primary",
      "styles": {
        "padding": "1rem 2rem",
        "backgroundColor": "var(--wp--preset--color--primary)",
        "color": "#ffffff",
        "borderRadius": "0.5rem",
        "fontWeight": "600",
        "textDecoration": "none"
      }
    },
    {
      "id": "card-shadow",
      "name": "Card with Shadow",
      "styles": {
        "backgroundColor": "#ffffff",
        "borderRadius": "1rem",
        "boxShadow": "0 4px 20px rgba(0,0,0,0.08)",
        "padding": "2rem"
      }
    }
  ]
}
```

### Using Global Classes in Blocks

```html
<!-- wp:generateblocks/text {"uniqueId":"gc001","tagName":"a","globalClasses":["button-primary"],"htmlAttributes":[{"attribute":"href","value":"#"}]} -->
<a class="gb-text button-primary" href="#">Get Started</a>
<!-- /wp:generateblocks/text -->

<!-- wp:generateblocks/element {"uniqueId":"gc002","tagName":"article","globalClasses":["card-shadow"]} -->
<article class="gb-element card-shadow">
    <!-- Card content -->
</article>
<!-- /wp:generateblocks/element -->
```

### Common Global Classes

#### Typography Classes

```css
/* Heading Styles */
.heading-1 {
  font-size: var(--wp--preset--font-size--5xl);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.heading-2 {
  font-size: var(--wp--preset--font-size--4xl);
  font-weight: 800;
  line-height: 1.2;
}

.heading-3 {
  font-size: var(--wp--preset--font-size--3xl);
  font-weight: 700;
  line-height: 1.3;
}

/* Body Text */
.text-lead {
  font-size: var(--wp--preset--font-size--lg);
  line-height: 1.7;
  color: var(--wp--preset--color--secondary);
}

.text-small {
  font-size: var(--wp--preset--font-size--sm);
  color: #666666;
}

.text-muted {
  color: #888888;
}
```

#### Button Classes

```css
.button-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  background-color: var(--wp--preset--color--primary);
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
}

.button-primary:hover {
  background-color: var(--wp--preset--color--secondary);
  transform: translateY(-2px);
}

.button-secondary {
  display: inline-flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: transparent;
  color: var(--wp--preset--color--primary);
  border: 2px solid var(--wp--preset--color--primary);
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.button-secondary:hover {
  background-color: var(--wp--preset--color--primary);
  color: #ffffff;
}

.button-ghost {
  padding: 1rem 2rem;
  background: transparent;
  color: var(--wp--preset--color--foreground);
  border: none;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
}

.button-ghost:hover {
  color: var(--wp--preset--color--primary);
}
```

#### Card Classes

```css
.card {
  background-color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
}

.card-elevated {
  background-color: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: all 0.3s;
}

.card-elevated:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-bordered {
  background-color: #ffffff;
  border: 1px solid var(--wp--preset--color--border);
  border-radius: 1rem;
  overflow: hidden;
}

.card-dark {
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
}
```

#### Layout Classes

```css
.container {
  width: 100%;
  max-width: var(--wp--style--global--content-size);
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.container-wide {
  max-width: var(--wp--style--global--wide-size);
}

.container-narrow {
  max-width: 800px;
}

.section {
  padding-top: var(--wp--preset--spacing--2xl);
  padding-bottom: var(--wp--preset--spacing--2xl);
}

.section-sm {
  padding-top: var(--wp--preset--spacing--lg);
  padding-bottom: var(--wp--preset--spacing--lg);
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--wp--preset--spacing--md);
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--wp--preset--spacing--md);
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--wp--preset--spacing--md);
}
```

## GenerateBlocks Default Settings

### Configure in Plugin Settings

Navigate to GenerateBlocks > Settings > Defaults:

```php
<?php
// Filter to set defaults programmatically
add_filter( 'generateblocks_defaults', function( $defaults ) {
    // Element defaults
    $defaults['element']['paddingTop'] = '2rem';
    $defaults['element']['paddingBottom'] = '2rem';

    // Text defaults
    $defaults['text']['fontFamily'] = 'var(--wp--preset--font-family--system)';
    $defaults['text']['lineHeight'] = '1.6';

    // Button defaults (text with button tag)
    $defaults['button']['backgroundColor'] = 'var(--wp--preset--color--primary)';
    $defaults['button']['color'] = '#ffffff';
    $defaults['button']['paddingTop'] = '1rem';
    $defaults['button']['paddingRight'] = '2rem';
    $defaults['button']['paddingBottom'] = '1rem';
    $defaults['button']['paddingLeft'] = '2rem';
    $defaults['button']['borderRadius'] = '0.5rem';

    return $defaults;
} );
```

## Style Presets

### Creating Style Presets

Style presets are predefined combinations of styles:

```php
<?php
add_filter( 'generateblocks_style_presets', function( $presets ) {
    $presets['hero-section'] = array(
        'label'  => __( 'Hero Section', 'theme' ),
        'styles' => array(
            'minHeight'       => '80vh',
            'display'         => 'flex',
            'alignItems'      => 'center',
            'justifyContent'  => 'center',
            'padding'         => '4rem 2rem',
            'backgroundColor' => 'var(--wp--preset--color--muted)',
        ),
    );

    $presets['feature-card'] = array(
        'label'  => __( 'Feature Card', 'theme' ),
        'styles' => array(
            'padding'         => '2rem',
            'backgroundColor' => '#ffffff',
            'borderRadius'    => '1rem',
            'boxShadow'       => '0 4px 20px rgba(0,0,0,0.08)',
        ),
    );

    return $presets;
} );
```

## Design Token System

### Organizing Tokens

Create a comprehensive token system:

```json
{
  "settings": {
    "custom": {
      "color": {
        "brand": {
          "primary": "#0073aa",
          "primaryHover": "#005a87",
          "secondary": "#23282d",
          "accent": "#e94560"
        },
        "neutral": {
          "50": "#fafafa",
          "100": "#f5f5f5",
          "200": "#e5e5e5",
          "300": "#d4d4d4",
          "400": "#a3a3a3",
          "500": "#737373",
          "600": "#525252",
          "700": "#404040",
          "800": "#262626",
          "900": "#171717"
        },
        "semantic": {
          "success": "#22c55e",
          "warning": "#f59e0b",
          "error": "#ef4444",
          "info": "#3b82f6"
        }
      },
      "spacing": {
        "base": "0.25rem",
        "scale": {
          "1": "0.25rem",
          "2": "0.5rem",
          "3": "0.75rem",
          "4": "1rem",
          "5": "1.25rem",
          "6": "1.5rem",
          "8": "2rem",
          "10": "2.5rem",
          "12": "3rem",
          "16": "4rem",
          "20": "5rem",
          "24": "6rem"
        }
      },
      "borderRadius": {
        "none": "0",
        "sm": "0.25rem",
        "md": "0.5rem",
        "lg": "1rem",
        "xl": "1.5rem",
        "full": "9999px"
      },
      "shadow": {
        "sm": "0 1px 2px rgba(0,0,0,0.05)",
        "md": "0 4px 6px rgba(0,0,0,0.1)",
        "lg": "0 10px 15px rgba(0,0,0,0.1)",
        "xl": "0 20px 25px rgba(0,0,0,0.15)"
      },
      "transition": {
        "fast": "150ms ease",
        "base": "300ms ease",
        "slow": "500ms ease"
      }
    }
  }
}
```

### Using Custom Tokens

```css
.component {
  padding: var(--wp--custom--spacing--scale--4);
  background-color: var(--wp--custom--color--neutral--50);
  border-radius: var(--wp--custom--border-radius--lg);
  box-shadow: var(--wp--custom--shadow--md);
  transition: var(--wp--custom--transition--base);
}

.component:hover {
  box-shadow: var(--wp--custom--shadow--xl);
}
```

## Responsive Global Styles

### Media Query Tokens

```json
{
  "settings": {
    "custom": {
      "breakpoint": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px"
      }
    }
  }
}
```

### Responsive Typography

In theme.json:

```json
{
  "settings": {
    "typography": {
      "fluid": true,
      "fontSizes": [
        {
          "slug": "heading-1",
          "size": "clamp(2rem, 5vw, 3.5rem)",
          "name": "Heading 1"
        },
        {
          "slug": "heading-2",
          "size": "clamp(1.75rem, 4vw, 2.5rem)",
          "name": "Heading 2"
        },
        {
          "slug": "heading-3",
          "size": "clamp(1.5rem, 3vw, 2rem)",
          "name": "Heading 3"
        }
      ]
    }
  }
}
```

## Best Practices

### 1. Use CSS Variables

Always prefer CSS variables over hard-coded values:

```html
<!-- Good -->
<!-- wp:generateblocks/element {"styles":{"backgroundColor":"var(--wp--preset--color--primary)"}}} -->

<!-- Avoid -->
<!-- wp:generateblocks/element {"styles":{"backgroundColor":"#0073aa"}} -->
```

### 2. Create Semantic Classes

Name classes by purpose, not appearance:

```css
/* Good */
.card-featured { }
.text-emphasis { }
.button-action { }

/* Avoid */
.blue-background { }
.large-text { }
.rounded-button { }
```

### 3. Layer Styles Appropriately

1. Global (theme.json) → Base tokens
2. Global Classes → Reusable components
3. Block Styles → Specific instances
4. Inline CSS → One-off overrides

### 4. Document Your System

Create a style guide document:

```markdown
# Design System

## Colors
- Primary: `var(--wp--preset--color--primary)` - #0073aa
- Secondary: `var(--wp--preset--color--secondary)` - #23282d

## Typography
- Headings: Inter, 700-900 weight
- Body: System font, 400 weight

## Spacing Scale
- xs: 0.5rem
- sm: 1rem
- md: 1.5rem
- lg: 2rem

## Components
- Buttons: Use `.button-primary` or `.button-secondary`
- Cards: Use `.card-elevated` for shadows
```

### 5. Test Across Contexts

Ensure global styles work in:
- Block editor
- Frontend
- Pattern previews
- Different post types

## Troubleshooting

### Styles Not Applying

1. Check CSS variable names match theme.json slugs
2. Verify global class is registered
3. Check for specificity conflicts
4. Clear browser and WordPress cache

### Variables Not Working

1. Ensure theme.json version is correct (version 3)
2. Check for typos in variable names
3. Verify theme.json is valid JSON
4. Check theme supports block editor styles

### Inconsistent Appearance

1. Review cascade order
2. Check for !important overrides
3. Ensure all breakpoints are covered
4. Test in multiple browsers
