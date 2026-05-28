---
name: web-development
description: >
  Web development patterns including frontend templates, CSS architecture,
  and server-side rendering infrastructure. Includes PageDef and TemplateSet
  for Go template rendering.
  Triggers: Web Components, al-* components, templates, Vite, TypeScript,
  custom elements, shadow DOM, frontend, client-side, CSS classes, PageDef,
  TemplateSet, PageData, server-side rendering, Go templates.
  File patterns: web/**/*.ts, web/**/*.html, web/**/*.css, web/**/*.go, pkg/web/*.go
---

# Web Development Patterns

## When This Skill Applies

- Deciding whether to create a component or use native HTML
- Implementing frontend components in `web/`
- Working with TypeScript custom elements
- Styling native elements with semantic classes
- Creating server-side rendered pages with Go templates
- Using PageDef and TemplateSet for template infrastructure

## Native-First Principle

**Goal**: Keep the frontend as native as possible so a designer can extend it rather than fight an opinionated system.

**Architecture**:
- Server-side rendering with traditional form submissions
- Semantic CSS classes for styling native elements
- Web components only for functionality HTML cannot provide

### Don't Create Components For

Use native HTML with CSS classes instead:

| Need | Use |
|------|-----|
| Buttons | `<button class="btn btn-primary">` |
| Inputs | `<input class="input">`, `<textarea>`, `<select>` |
| Badges | `<span class="badge badge-success">` |
| Cards | `<article>` or `<section>` |
| Lists | `<ul>`, `<ol>`, `<li>` |
| Dialogs | `<dialog>` |
| Forms | `<form>` |
| Tables | `<table class="table">` |

### Create Components When

1. **Native HTML lacks the functionality**
   - SSE streaming connections
   - D3.js or canvas-based visualizations
   - Complex nested data editors

2. **Client-side state management is required**
   - Reactive updates during live execution
   - Real-time data synchronization

## Component Candidates

| Component | Justification | Session |
|-----------|---------------|---------|
| `al-workflow-monitor` | SSE + reactive state for live execution | 05h |
| `al-confidence-chart` | D3.js visualization | 05i |
| `al-stage-editor` | Complex nested data editing (evaluate need) | 05f |

## CSS Classes Reference

### Buttons

```html
<button class="btn">Default</button>
<button class="btn btn-primary">Primary action</button>
<button class="btn btn-danger">Destructive action</button>
```

### Form Elements

```html
<div class="form-group">
  <label class="form-label">Field name</label>
  <input class="input" type="text">
  <span class="form-error">Error message</span>
</div>

<input class="input input-error" type="text">
```

### Tables

```html
<table class="table">
  <thead>...</thead>
  <tbody>...</tbody>
</table>

<table class="table table-striped">...</table>
```

### Badges

```html
<span class="badge">Default</span>
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-error">Failed</span>
```

## Component Implementation Pattern

When a component IS needed, follow this pattern:

```typescript
class AlWorkflowMonitor extends HTMLElement {
  static observedAttributes = ['workflow-id'];

  connectedCallback() {
    this.render();
    this.connect();
  }

  disconnectedCallback() {
    this.disconnect();
  }

  attributeChangedCallback() {
    this.render();
  }

  private render() {
    // Update DOM based on state
  }

  private connect() {
    // SSE or other async connection
  }

  private disconnect() {
    // Cleanup
  }
}

customElements.define('al-workflow-monitor', AlWorkflowMonitor);
```

**Conventions**:
- `al-` prefix for all custom elements
- Light DOM (no shadow DOM) for global CSS access
- Cleanup in `disconnectedCallback`
- Minimal internal state

## Server-Side Rendering Infrastructure

### PageDef and TemplateSet

The `pkg/web` package provides infrastructure for server-side rendered pages:

```go
// PageDef defines a page with route, template, title, and bundle
type PageDef struct {
    Route    string  // URL pattern (e.g., "/", "/workflows")
    Template string  // Template file path (e.g., "home.html")
    Title    string  // Page title
    Bundle   string  // JS bundle name (e.g., "app")
}

// PageData passed to templates during rendering
type PageData struct {
    Title    string
    Bundle   string
    BasePath string  // For portable URL generation
    Data     any     // Custom page data
}

// TemplateSet holds pre-parsed templates
type TemplateSet struct {
    pages    map[string]*template.Template
    basePath string
}
```

**Creating a TemplateSet**:
```go
templates, err := web.NewTemplateSet(
    layoutFS, pageFS,
    "layouts/*.html",  // Layout glob
    "pages",           // Page subdirectory
    "/app",            // Base path for URLs
    pages,             // []PageDef
)
```

**Generating Handlers**:
```go
// Page handler - renders template with PageData
mux.HandleFunc("GET /", templates.PageHandler("app.html", homePage))

// Error handler - renders with status code
mux.HandleFunc("GET /404", templates.ErrorHandler("app.html", notFoundPage, 404))
```

**Template Usage**:
```html
<!-- Use BasePath for portable URLs -->
<base href="{{ .BasePath }}/">
<link rel="stylesheet" href="dist/{{ .Bundle }}.css">
<script type="module" src="dist/{{ .Bundle }}.js"></script>
```

## Directory Structure

Each web client is fully isolated in its own directory:

```
web/
├── app/                         # Main app client (fully self-contained)
│   ├── client/                  # TypeScript source
│   │   ├── app.ts               # Entry point → dist/app.js
│   │   ├── core/                # Foundation (created when needed)
│   │   ├── design/              # CSS architecture
│   │   └── components/          # Custom elements (when needed)
│   ├── dist/                    # Build output (gitignored)
│   ├── public/                  # Static assets (favicons, manifest)
│   ├── server/                  # Go templates (SSR)
│   │   ├── layouts/
│   │   └── pages/
│   └── app.go                   # NewModule()
├── scalar/                      # Scalar OpenAPI UI (fully self-contained)
│   ├── app.ts                   # Entry point → scalar.js
│   ├── index.html               # Scalar mount point
│   ├── scalar.go                # NewModule()
│   └── [scalar.js/css]          # Build output (gitignored)
├── vite.client.ts               # Shared Vite config module
├── vite.config.ts               # Root config (merges clients)
└── package.json
```

**URL Routing:**
- `/app/*` - Main app (SSR pages, assets, public files)
- `/scalar/*` - OpenAPI documentation UI

## Mountable Web Clients

Each `web/[client-name]/` directory is a self-contained web client that mounts to `/[client-name]`.

### Module Pattern

Web clients implement `NewModule(basePath)` which returns a `*module.Module`:

```go
func NewModule(basePath string) (*module.Module, error) {
    router := buildRouter()
    return module.New(basePath, router), nil
}

func buildRouter() http.Handler {
    mux := http.NewServeMux()
    // Register routes, file servers, etc.
    return mux
}
```

The module handles path prefix stripping automatically. Requests to `/app/components/` are routed to the internal handler as `/components/`.

### Middleware Integration

Modules have their own middleware chains:

```go
appModule, _ := app.NewModule("/app")
appModule.Use(middleware.AddSlash())  // Redirect /app/components to /app/components/
appModule.Use(middleware.Logger(runtime.Logger))

router := module.NewRouter()
router.Mount(appModule)
```

### Asset Paths

- **SSR templates**: Use `<base href="{{ .BasePath }}/">` tag with relative URLs
- **Static HTML**: Same base tag pattern for relative URL resolution

### Adding a New Client

1. Create `web/[client-name]/` with standard structure
2. Implement `NewModule(basePath)` function in `[client-name].go`
3. Add per-client config at `web/[client-name]/client.config.ts` (exports `ClientConfig`)
4. Import config in `web/vite.config.ts`
5. Create and mount module in `cmd/server/modules.go`

### Vite Configuration

Per-client configs are named `client.config.ts` to distinguish from the root `vite.config.ts`:

```
web/
├── vite.config.ts            # Root config (imports and merges clients)
├── vite.client.ts            # Shared merge utilities and ClientConfig type
├── app/
│   └── client.config.ts      # App client config
└── scalar/
    └── client.config.ts      # Scalar client config
```

## Asset Co-location

Global styles live in `client/design/`. Page-specific styles can be co-located with templates when needed:

```
web/server/
├── layouts/
│   └── app.html
└── pages/
    └── workflows/
        ├── list.html
        └── list.css         # Page-scoped styles (optional)
```

**Loading scoped assets**: Entry files import the assets they need:

```typescript
// client/app.ts
import '@design/styles.css';
import '../server/pages/workflows/list.css';  // If page-specific styles exist
```

**When to co-locate**: Only create scoped CSS when styles are unique to that template. Prefer global utilities in `client/design/` when patterns are reusable.

## Core Principles

**Separation of Concerns**:
- Styles belong in `.css` files
- Markup belongs in `.html` files
- Code belongs in `.ts` files
- Never use inline `style` attributes in templates

**Exception**: Third-party library overrides (e.g., Scalar font variables in `web/scalar/index.html`) may use `<style>` in `<head>` when the library doesn't expose CSS custom properties.

## Anti-Patterns

- Creating `al-button` when `<button class="btn">` works
- Adding client-side validation when server validation suffices
- Building component wrappers for native elements
- Using shadow DOM when global styles should apply
- Using inline `style` attributes instead of CSS classes
