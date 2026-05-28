---
name: hugo-asset-pipeline
description: This skill should be used when the user mentions "scss", "sass", "css processing", "javascript bundling", "js.Build", "hugo pipes", "asset pipeline", "fingerprint", "cache busting", "minify assets", "image processing", "responsive images", "webp", "toCSS", "resources.Get", "resources.Concat", "sri", "subresource integrity", or any Hugo asset processing topics. Provides comprehensive guidance on Hugo's built-in asset pipeline for SCSS compilation, JavaScript bundling, image optimization, and cache management.
---

# Hugo Asset Pipeline (Hugo Pipes)

## Overview

Hugo Pipes is Hugo's built-in asset processing pipeline that replaces traditional bundlers like webpack, Vite, or esbuild. **Hugo projects DO have a build step** - it's just handled by Hugo itself, not external tools.

**CRITICAL**: When working on Hugo projects, use Hugo Pipes for all asset processing. Do NOT add webpack, Vite, Rollup, or other JavaScript bundlers - Hugo handles this natively.

## Hugo Extended Requirement

**SCSS/SASS compilation requires Hugo Extended edition.** Check your version:

```bash
hugo version
# Look for "extended" in the output: hugo v0.XXX.X-extended
```

If you need Extended and don't have it, install via:
```bash
# macOS
brew install hugo

# Or download extended version from GitHub releases
```

## Core Hugo Pipes Functions

### resources.Get - Load Assets

Load files from the `assets/` directory (NOT `static/`):

```go-html-template
{{ $styles := resources.Get "scss/main.scss" }}
{{ $script := resources.Get "js/app.js" }}
{{ $image := resources.Get "images/hero.jpg" }}
```

**Important**: Assets MUST be in `assets/` directory, not `static/`. The `static/` directory is for files that need no processing.

### resources.Concat - Combine Files

Merge multiple files into one:

```go-html-template
{{ $vendorJS := resources.Get "js/vendor/jquery.js" }}
{{ $appJS := resources.Get "js/app.js" }}
{{ $allJS := slice $vendorJS $appJS | resources.Concat "js/bundle.js" }}
```

### toCSS - SCSS/SASS Compilation

Compile SCSS to CSS (requires Hugo Extended):

```go-html-template
{{ $opts := dict "transpiler" "libsass" "targetPath" "css/style.css" }}
{{ $styles := resources.Get "scss/main.scss" | toCSS $opts }}
```

Options:
- `transpiler`: "libsass" (default) or "dartsass"
- `targetPath`: Output path relative to publishDir
- `outputStyle`: "nested", "expanded", "compact", "compressed"
- `precision`: Decimal precision for calculations
- `enableSourceMap`: true/false

### js.Build - JavaScript Bundling

Bundle JavaScript with Hugo's built-in esbuild:

```go-html-template
{{ $opts := dict
    "targetPath" "js/app.js"
    "minify" true
    "target" "es2020"
    "format" "esm"
}}
{{ $js := resources.Get "js/main.js" | js.Build $opts }}
```

Options:
- `targetPath`: Output filename
- `minify`: true/false
- `target`: "es2015", "es2017", "es2020", etc.
- `format`: "iife", "cjs", "esm"
- `externals`: Array of packages to exclude from bundle
- `defines`: Global constant replacements
- `sourceMap`: "inline", "external", or empty

### minify - Minification

Minify CSS, JS, JSON, HTML, SVG, XML:

```go-html-template
{{ $styles := resources.Get "scss/main.scss" | toCSS | minify }}
{{ $js := resources.Get "js/app.js" | js.Build | minify }}
```

### fingerprint - Cache Busting

Add content hash to filename for cache invalidation:

```go-html-template
{{ $styles := resources.Get "scss/main.scss" | toCSS | minify | fingerprint }}
{{/* Output: /css/style.a1b2c3d4.css */}}

<link rel="stylesheet" href="{{ $styles.RelPermalink }}">
```

Fingerprint options:
- `fingerprint` - SHA256 (default)
- `fingerprint "sha384"` - SHA384
- `fingerprint "sha512"` - SHA512
- `fingerprint "md5"` - MD5 (not recommended)

## Development vs Production Patterns

### Conditional Processing with hugo.IsServer

```go-html-template
{{ $styles := resources.Get "scss/main.scss" }}

{{ if hugo.IsServer }}
  {{/* Development: source maps, no minification */}}
  {{ $opts := dict "enableSourceMap" true "outputStyle" "expanded" }}
  {{ $styles = $styles | toCSS $opts }}
{{ else }}
  {{/* Production: minified and fingerprinted */}}
  {{ $styles = $styles | toCSS | minify | fingerprint }}
{{ end }}

<link rel="stylesheet" href="{{ $styles.RelPermalink }}">
```

### Using hugo.IsProduction

```go-html-template
{{ $js := resources.Get "js/app.js" }}

{{ $opts := dict "targetPath" "js/bundle.js" }}
{{ if hugo.IsProduction }}
  {{ $opts = merge $opts (dict "minify" true "target" "es2017") }}
{{ else }}
  {{ $opts = merge $opts (dict "sourceMap" "inline") }}
{{ end }}

{{ $js = $js | js.Build $opts }}
```

## SCSS Compilation Patterns

### Basic SCSS Setup

Directory structure:
```
assets/
  scss/
    main.scss
    _variables.scss
    _mixins.scss
    components/
      _buttons.scss
      _forms.scss
```

main.scss:
```scss
@import "variables";
@import "mixins";
@import "components/buttons";
@import "components/forms";
```

Template:
```go-html-template
{{ $styles := resources.Get "scss/main.scss" | toCSS | minify | fingerprint }}
<link rel="stylesheet" href="{{ $styles.RelPermalink }}">
```

### SCSS with npm Packages (Bootstrap Example)

Install with Bun:
```bash
bun add bootstrap
```

Configure module mounts in `hugo.toml`:
```toml
[[module.mounts]]
  source = "assets"
  target = "assets"

[[module.mounts]]
  source = "node_modules/bootstrap/scss"
  target = "assets/scss/bootstrap"

[[module.mounts]]
  source = "node_modules/bootstrap/dist/js"
  target = "assets/js/bootstrap"
```

Import in your SCSS:
```scss
// assets/scss/main.scss
@import "bootstrap/bootstrap";

// Or import specific components
@import "bootstrap/functions";
@import "bootstrap/variables";
@import "bootstrap/mixins";
@import "bootstrap/grid";
```

## JavaScript Bundling Patterns

### Basic JavaScript Bundle

```go-html-template
{{ $js := resources.Get "js/main.js" | js.Build (dict "minify" hugo.IsProduction) | fingerprint }}
<script src="{{ $js.RelPermalink }}"></script>
```

### ES Modules with Imports

assets/js/main.js:
```javascript
import { initNav } from './components/navigation.js';
import { setupForms } from './components/forms.js';

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  setupForms();
});
```

Template:
```go-html-template
{{ $opts := dict
    "targetPath" "js/bundle.js"
    "format" "iife"
    "minify" hugo.IsProduction
}}
{{ $js := resources.Get "js/main.js" | js.Build $opts | fingerprint }}
<script src="{{ $js.RelPermalink }}"></script>
```

### npm Package Integration

Install packages:
```bash
bun add alpinejs
```

Mount in hugo.toml:
```toml
[[module.mounts]]
  source = "node_modules/alpinejs/dist"
  target = "assets/js/alpine"
```

Import in your JS:
```javascript
// assets/js/main.js
import Alpine from 'js/alpine/module.esm.js';
window.Alpine = Alpine;
Alpine.start();
```

## Image Processing

### Basic Resizing

```go-html-template
{{ $image := resources.Get "images/hero.jpg" }}
{{ $resized := $image.Resize "800x" }}
<img src="{{ $resized.RelPermalink }}" width="{{ $resized.Width }}" height="{{ $resized.Height }}">
```

### Resize Operations

```go-html-template
{{/* Resize to width, maintain aspect ratio */}}
{{ $img := $image.Resize "800x" }}

{{/* Resize to height, maintain aspect ratio */}}
{{ $img := $image.Resize "x600" }}

{{/* Resize to exact dimensions (may distort) */}}
{{ $img := $image.Resize "800x600" }}

{{/* Fit within bounds, maintain aspect ratio */}}
{{ $img := $image.Fit "800x600" }}

{{/* Fill dimensions, crop as needed */}}
{{ $img := $image.Fill "800x600 Center" }}
```

Fill anchor positions: `Center`, `TopLeft`, `Top`, `TopRight`, `Left`, `Right`, `BottomLeft`, `Bottom`, `BottomRight`, `Smart`

### WebP Conversion

```go-html-template
{{ $original := resources.Get "images/photo.jpg" }}
{{ $webp := $original.Resize "800x webp" }}
{{ $jpg := $original.Resize "800x" }}

<picture>
  <source srcset="{{ $webp.RelPermalink }}" type="image/webp">
  <img src="{{ $jpg.RelPermalink }}" alt="Photo">
</picture>
```

### Responsive Images with srcset

```go-html-template
{{ $image := resources.Get "images/hero.jpg" }}
{{ $small := $image.Resize "400x" }}
{{ $medium := $image.Resize "800x" }}
{{ $large := $image.Resize "1200x" }}

<img
  src="{{ $medium.RelPermalink }}"
  srcset="{{ $small.RelPermalink }} 400w,
          {{ $medium.RelPermalink }} 800w,
          {{ $large.RelPermalink }} 1200w"
  sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
  alt="Hero image">
```

### Image Fingerprinting

```go-html-template
{{ $image := resources.Get "images/logo.png" }}
{{ $processed := $image.Resize "200x" | fingerprint }}
<img src="{{ $processed.RelPermalink }}" alt="Logo">
```

## Subresource Integrity (SRI)

SRI ensures loaded resources haven't been tampered with. Use with fingerprint:

```go-html-template
{{ $styles := resources.Get "scss/main.scss" | toCSS | minify | fingerprint "sha384" }}
<link rel="stylesheet" href="{{ $styles.RelPermalink }}"
      integrity="{{ $styles.Data.Integrity }}"
      crossorigin="anonymous">

{{ $js := resources.Get "js/app.js" | js.Build | minify | fingerprint "sha384" }}
<script src="{{ $js.RelPermalink }}"
        integrity="{{ $js.Data.Integrity }}"
        crossorigin="anonymous"></script>
```

**Why SRI matters:**
- Protects against CDN compromises
- Detects file tampering
- Required for security compliance in many contexts
- Browser refuses to load resource if hash doesn't match

## Complete Production Template

A full baseof.html head section example:

```go-html-template
{{ $styles := resources.Get "scss/main.scss" }}
{{ $js := resources.Get "js/main.js" }}

{{ if hugo.IsServer }}
  {{/* Development */}}
  {{ $styles = $styles | toCSS (dict "enableSourceMap" true) }}
  {{ $js = $js | js.Build (dict "sourceMap" "inline") }}
  <link rel="stylesheet" href="{{ $styles.RelPermalink }}">
  <script src="{{ $js.RelPermalink }}" defer></script>
{{ else }}
  {{/* Production */}}
  {{ $styles = $styles | toCSS | minify | fingerprint "sha384" }}
  {{ $js = $js | js.Build (dict "minify" true "target" "es2017") | fingerprint "sha384" }}
  <link rel="stylesheet" href="{{ $styles.RelPermalink }}"
        integrity="{{ $styles.Data.Integrity }}" crossorigin="anonymous">
  <script src="{{ $js.RelPermalink }}" defer
          integrity="{{ $js.Data.Integrity }}" crossorigin="anonymous"></script>
{{ end }}
```

## Module Mounts Reference

Full hugo.toml example with multiple npm packages:

```toml
[module]
  [[module.mounts]]
    source = "assets"
    target = "assets"

  [[module.mounts]]
    source = "static"
    target = "static"

  # Bootstrap SCSS
  [[module.mounts]]
    source = "node_modules/bootstrap/scss"
    target = "assets/scss/bootstrap"

  # Bootstrap JS
  [[module.mounts]]
    source = "node_modules/bootstrap/dist/js"
    target = "assets/js/bootstrap"

  # Alpine.js
  [[module.mounts]]
    source = "node_modules/alpinejs/dist"
    target = "assets/js/alpine"

  # FontAwesome
  [[module.mounts]]
    source = "node_modules/@fortawesome/fontawesome-free/scss"
    target = "assets/scss/fontawesome"

  [[module.mounts]]
    source = "node_modules/@fortawesome/fontawesome-free/webfonts"
    target = "static/webfonts"
```

## Troubleshooting

### "SCSS compilation failed"
- Ensure you have Hugo Extended edition
- Check SCSS syntax errors in terminal output
- Verify all imported partials exist (files starting with `_`)

### "Resource not found"
- File must be in `assets/` not `static/`
- Path in `resources.Get` is relative to `assets/`
- Check filename case sensitivity

### "js.Build failed"
- Check for JavaScript syntax errors
- Verify all imports resolve correctly
- Ensure npm packages are installed and mounted

### Images not processing
- Image must be in `assets/` directory
- Use `resources.Get`, not direct path references
- Check supported formats: jpg, png, gif, webp, tiff, bmp

## Key Differences from Traditional Bundlers

| Traditional | Hugo Pipes |
|-------------|------------|
| webpack.config.js | hugo.toml + templates |
| npm run build | hugo (builds everything) |
| npm run dev | hugo server |
| dist/ folder | public/ folder |
| Manual cache busting | Built-in fingerprint |
| Complex configuration | Template-based, declarative |
