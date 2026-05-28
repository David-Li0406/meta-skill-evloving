---
name: hugo-fundamentals
description: This skill should be used when the user mentions "hugo basics", "hugo config", "hugo commands", "project structure", "hugo setup", "hugo.toml", "config.toml", "hugo serve", "hugo build", "content directory", "layouts directory", "static directory", "assets directory", "hugo configuration", "module mounts", "hugo environment", or any general Hugo static site generator questions. Provides foundational Hugo knowledge including project structure, configuration patterns, and essential commands.
---

# Hugo Fundamentals

## Hugo Project Structure

Hugo follows a convention-over-configuration approach with a well-defined directory structure. Understanding each directory's purpose is essential for effective Hugo development.

### Core Directories

#### content/
The `content/` directory holds all Markdown content files organized into sections. Each subdirectory becomes a section with its own list page.

```
content/
  _index.md           # Homepage content
  about.md            # Single page at /about/
  blog/
    _index.md         # Blog section list page
    first-post.md     # Blog post at /blog/first-post/
    2024/
      year-review.md  # Nested at /blog/2024/year-review/
  docs/
    _index.md         # Docs section list page
    getting-started/
      _index.md       # Subsection list
      install.md      # /docs/getting-started/install/
```

**Key concepts:**
- `_index.md` defines section/list pages (has `.Pages` in templates)
- Files without underscore are single pages
- Directory structure maps directly to URL paths
- Front matter controls metadata, dates, taxonomies

#### layouts/
Templates that control HTML rendering. Hugo's lookup order searches here before theme layouts.

```
layouts/
  _default/
    baseof.html       # Base template all pages extend
    list.html         # Default list/section template
    single.html       # Default single page template
  partials/
    header.html       # Reusable header partial
    footer.html       # Reusable footer partial
    meta.html         # SEO meta tags
  shortcodes/
    youtube.html      # Custom shortcode
    figure.html       # Enhanced figure shortcode
  blog/
    single.html       # Blog-specific single template
    list.html         # Blog-specific list template
  index.html          # Homepage template (overrides _default)
  404.html            # Custom 404 page
```

**Template inheritance:** All templates extend `baseof.html` using `{{ define "main" }}` blocks.

#### assets/
Files processed by Hugo Pipes (SCSS compilation, JS bundling, image processing, fingerprinting).

```
assets/
  scss/
    main.scss         # Compiled to CSS via Hugo Pipes
    _variables.scss   # Sass partials
  js/
    app.js            # Bundled/minified via Hugo Pipes
  images/
    hero.jpg          # Processed for responsive images
```

**Critical distinction:** Files in `assets/` are NOT automatically published. They must be explicitly processed in templates using `resources.Get` and Hugo Pipes.

#### static/
Files copied directly to the output with no processing. Use for files that don't need transformation.

```
static/
  favicon.ico         # Copied to /favicon.ico
  robots.txt          # Copied to /robots.txt
  downloads/
    guide.pdf         # Copied to /downloads/guide.pdf
```

**When to use static/ vs assets/:**
- `static/`: Pre-optimized images, PDFs, fonts, legacy JS/CSS
- `assets/`: SCSS, modern JS, images needing processing

#### data/
Structured data files accessible in templates via `.Site.Data`.

```
data/
  team.yaml           # Access as .Site.Data.team
  products.json       # Access as .Site.Data.products
  config/
    features.toml     # Access as .Site.Data.config.features
```

Useful for: navigation menus, team members, product catalogs, feature flags.

#### archetypes/
Content templates for `hugo new` command.

```
archetypes/
  default.md          # Default for all content
  blog.md             # Template for hugo new blog/post.md
  docs.md             # Template for hugo new docs/page.md
```

#### resources/
Hugo's generated cache directory. Contains processed assets (resized images, compiled SCSS). Should be gitignored or committed for faster builds depending on your workflow.

## Configuration File Locations

Hugo supports multiple configuration patterns. Detection order matters.

### Single File Configuration (Most Common)
```
project/
  hugo.toml           # Primary (preferred name)
  # OR
  config.toml         # Legacy name (still supported)
  # OR
  hugo.yaml           # YAML format
  # OR
  hugo.json           # JSON format
```

### Nested Configuration (Monorepo Pattern)
For projects where Hugo lives in a subdirectory:
```
project/
  hugo/
    hugo.toml         # Config at hugo/hugo.toml
    content/
    layouts/
```

Run with: `hugo -s hugo` or `hugo serve -s hugo`

### Configuration Directory (Environment-Based)
For complex sites with environment-specific settings:
```
project/
  config/
    _default/
      hugo.toml       # Base configuration
      menus.toml      # Menu definitions
      params.toml     # Site parameters
    production/
      hugo.toml       # Production overrides
    staging/
      hugo.toml       # Staging overrides
```

**Detection logic when working with a project:**
1. Check for `hugo.toml` or `config.toml` in root
2. Check for `hugo/hugo.toml` (nested pattern)
3. Check for `config/_default/` directory (config dir pattern)
4. Examine build scripts or CI config for `-s` flag usage

## Essential Hugo Commands

### Development Server

```bash
# Full development command with all useful flags
hugo serve --watch --renderToMemory --minify --disableFastRender

# Common variations
hugo serve -D              # Include draft content
hugo serve -F              # Include future-dated content
hugo serve -D -F           # Both drafts and future
hugo serve -s hugo         # Source in hugo/ subdirectory
hugo serve --bind 0.0.0.0  # Expose to network (for mobile testing)
hugo serve --port 3000     # Custom port
```

**Flag explanations:**
- `--watch`: Auto-rebuild on file changes (default: true)
- `--renderToMemory`: Faster, no disk writes during dev
- `--minify`: Minify output (catches minification bugs early)
- `--disableFastRender`: Full rebuild on every change (more reliable)
- `-D` / `--buildDrafts`: Include content with `draft: true`
- `-F` / `--buildFuture`: Include content with future dates
- `-s` / `--source`: Specify source directory
- `--navigateToChanged`: Auto-navigate browser to changed content

### Production Build

```bash
# Standard build
hugo

# With common production flags
hugo --minify --gc

# Nested source directory
hugo -s hugo --minify

# Include drafts (preview environments)
hugo -D --minify

# Specify output directory
hugo -d public --minify
```

**Flag explanations:**
- `--minify`: Minify HTML, CSS, JS, JSON, XML
- `--gc`: Garbage collect unused cache files after build
- `-d` / `--destination`: Output directory (default: public/)
- `--cleanDestinationDir`: Remove files from destination not in source

### Content Validation & Debugging

```bash
# List all content with metadata
hugo list all

# List only drafts
hugo list drafts

# List future-dated content
hugo list future

# List expired content
hugo list expired

# Show configuration
hugo config

# Show configuration for specific environment
hugo config --environment production

# Debug template rendering
hugo --templateMetrics --templateMetricsHints
```

## Key Configuration Sections

### Essential Settings

```toml
# hugo.toml

baseURL = "https://example.com/"  # Required for absolute URLs
title = "Site Title"
languageCode = "en-us"

# Output directory (default: public)
publishDir = "public"

# URL style
uglyURLs = false                  # false: /about/ (pretty)
                                  # true: /about.html (ugly)

# Disable automatic generation
disableKinds = ["taxonomy", "term", "RSS"]
```

### Module Mounts (Importing npm Packages)

Use module mounts to bring npm packages into Hugo's asset pipeline:

```toml
# hugo.toml

[module]
  [[module.mounts]]
    source = "assets"
    target = "assets"

  [[module.mounts]]
    source = "node_modules/bootstrap/scss"
    target = "assets/scss/vendor/bootstrap"

  [[module.mounts]]
    source = "node_modules/@fortawesome/fontawesome-free/webfonts"
    target = "static/fonts"

  [[module.mounts]]
    source = "node_modules/alpinejs/dist"
    target = "assets/js/vendor/alpine"
```

Then in templates:
```go-html-template
{{ $bootstrap := resources.Get "scss/vendor/bootstrap/bootstrap.scss" }}
{{ $alpine := resources.Get "js/vendor/alpine/cdn.min.js" }}
```

### Taxonomies

```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  author = "authors"
  series = "series"
```

### Pagination

```toml
paginate = 10                     # Items per page
paginatePath = "page"             # URL path: /blog/page/2/
```

### Related Content

```toml
[related]
  includeNewer = true
  threshold = 80
  toLower = true

  [[related.indices]]
    name = "tags"
    weight = 100

  [[related.indices]]
    name = "categories"
    weight = 50

  [[related.indices]]
    name = "date"
    weight = 10
```

### Params Section (Site-wide Variables)

```toml
[params]
  description = "Site description for SEO"
  author = "Author Name"

  [params.social]
    twitter = "@handle"
    github = "username"

  [params.features]
    darkMode = true
    search = true
```

Access in templates: `{{ .Site.Params.description }}`, `{{ .Site.Params.social.twitter }}`

## Environment Detection

Hugo provides built-in variables for environment-aware processing.

### hugo.IsServer

True when running `hugo serve`, false during `hugo build`.

```go-html-template
{{ if hugo.IsServer }}
  <!-- Development-only: LiveReload, debug info -->
  <script>console.log('Development mode');</script>
{{ end }}
```

### hugo.IsProduction

True when `--environment production` or `HUGO_ENVIRONMENT=production`.

```go-html-template
{{ if hugo.IsProduction }}
  <!-- Production-only: Analytics, minified assets -->
  {{ partial "analytics.html" . }}
{{ else }}
  <!-- Non-production: Debug toolbar -->
  {{ partial "debug-toolbar.html" . }}
{{ end }}
```

### Conditional Asset Processing

```go-html-template
{{ $styles := resources.Get "scss/main.scss" | toCSS }}

{{ if hugo.IsProduction }}
  {{ $styles = $styles | minify | fingerprint }}
{{ end }}

<link rel="stylesheet" href="{{ $styles.RelPermalink }}">
```

### Environment-Specific Configuration

```go-html-template
{{ $env := hugo.Environment }}  <!-- "development", "production", etc. -->

{{ if eq $env "staging" }}
  <meta name="robots" content="noindex">
{{ end }}
```

### Setting Environment

```bash
# Via flag
hugo --environment production

# Via environment variable
HUGO_ENVIRONMENT=production hugo

# Development server (automatically sets development)
hugo serve  # hugo.Environment = "development"
```

## Quick Reference

| Task | Command |
|------|---------|
| Dev server | `hugo serve -D` |
| Production build | `hugo --minify` |
| Nested project dev | `hugo serve -s hugo -D` |
| Nested project build | `hugo -s hugo --minify` |
| List all content | `hugo list all` |
| Show config | `hugo config` |
| Template debugging | `hugo --templateMetrics` |

| Directory | Purpose | Processed? |
|-----------|---------|------------|
| content/ | Markdown content | Rendered |
| layouts/ | HTML templates | - |
| assets/ | SCSS, JS, images | Hugo Pipes |
| static/ | Direct copy files | No |
| data/ | Structured data | - |
| archetypes/ | Content templates | - |
| resources/ | Build cache | Generated |
