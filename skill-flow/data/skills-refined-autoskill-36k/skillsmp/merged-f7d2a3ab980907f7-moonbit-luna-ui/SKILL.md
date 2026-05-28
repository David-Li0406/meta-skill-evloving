---
name: moonbit-luna-ui
description: Use this skill for developing web applications with MoonBit and Luna UI (Sol Framework) for Cloudflare Workers, including routing, server actions, and database integration.
---

# MoonBit + Luna UI Development Guide

This guide provides knowledge for developing web applications for Cloudflare Workers using MoonBit and Luna UI (Sol Framework).

## Technical Stack Overview

| Technology      | Role                                           |
|------------------|------------------------------------------------|
| MoonBit          | Main language (supports both WASM and JS targets) |
| Luna UI          | UI framework (Island Architecture)            |
| Sol Framework    | Routing, SSR, and Server Actions              |
| Cloudflare Workers| Runtime                                      |
| D1               | SQLite-based database                          |
| Hono             | HTTP middleware (for authentication, etc.)    |

## Project Structure

```
project/
├── app/
│   ├── server/
│   │   ├── routes.mbt      # Routing, page, and API definitions
│   │   ├── db.mbt          # D1 FFI bindings
│   │   └── _using.mbt      # Common imports
│   ├── client/
│   │   ├── *.mbt           # Island Components
│   │   └── _using.mbt
│   └── __gen__/            # Auto-generated (recommended to .gitignore)
├── src/
│   └── worker.ts           # Cloudflare Worker entry point
├── static/
│   └── loader.js           # Luna UI hydration loader
├── scripts/
│   ├── patch-for-cloudflare.js  # Patch for CF Workers
│   └── bundle-client.js         # Client bundle
├── moon.mod.json           # MoonBit configuration
├── wrangler.json           # Cloudflare configuration
└── .sol/                   # Sol generated files (recommended to .gitignore)
```

## Build Process

```bash
# Full build
pnpm build
# Internal processes executed:
# 1. sol generate        - Generates __gen__ and .sol
# 2. moon build --target js  - Compiles MoonBit to JS
# 3. patch-for-cloudflare.js - Patches for CF Workers
# 4. bundle-client.js    - Bundles Island Components
```

### Automatic Build Configuration in wrangler.json

```json
{
  "build": {
    "command": "pnpm build",
    "watch_dir": ["src", "app"]
  }
}
```

## Quick Reference

### Route Definitions (routes.mbt)

```moonbit
pub fn routes() -> Array[@router.SolRoutes] {
  [
    @router.SolRoutes::Page(
      path="/",
      handler=@router.PageHandler(home_page),
      title="Home",
      meta=[], revalidate=None, cache=None,
    ),
    @router.SolRoutes::Post(
      path="/api/posts",
      handler=@router.ApiHandler(api_create_post),
    ),
  ]
}
```

### Island Component (Client)

```moonbit
pub fn my_component(props : MyProps) -> DomNode {
  let count = @signal.signal(0)

  div(class="container", [
    button(
      on=events().click(fn(_) { count.set(count.get() + 1) }),
      [text_of(count)]
    )
  ])
}
```

### Server Action

```moonbit
let create_action : @action.ActionHandler = @action.ActionHandler(async fn(ctx) {
  let body = ctx.body
  let data = parse_json(body)
  // Processing...
  @action.ActionResult::ok({ message: "Success" })
})

pub fn action_registry() -> @action.ActionRegistry {
  @action.ActionRegistry::new(allowed_origins=[
    "http://localhost:8787",
    "https://your-app.workers.dev",
  ]).register(
    @action.ActionDef::new("create", create_action)
  )
}
```

### D1 FFI

```moonbit
extern "js" fn db_query(sql : String) -> @core.Promise[@core.Any] =
  #| async (sql) => {
  #|   const db = globalThis.__D1_DB;
  #|   return await db.prepare(sql).all();
  #| }
```

## Common Issues and Solutions

### 403 Error (Server Actions)
→ Add your production domain to `allowed_origins` in `action_registry()`.

### CSS Not Applying (Island Component)
→ Ensure CSS class names match the style definitions in routes.mbt.

### Module Errors After Build
→ Patch CF Workers incompatible code in `scripts/patch-for-cloudflare.js`.

### Build Not Triggering on Deploy
→ Set `build.command` in `wrangler.json`.

### Hydration Errors (e.g., entries_json undefined)
→ Ensure JSON data passed to Island Components is ASCII-safe using `json_stringify`.

### High CLS (Cumulative Layout Shift)
→ Approximate the height of skeletons (fallbacks) to actual content.

### SSG Build Not Finding Routes
→ Use a function to return a list of slugs for dynamic routes in `sol.config.json`.

### SSG Using Stale Data
→ Use ISR for frequently updated data or combine with client-side fetching.

### ISR Not Revalidating
→ Check if `revalidate` is set in route definitions and KV bindings in `wrangler.json`.

### Sitemap Not Generating
→ Ensure `metaFiles.sitemap.hostname` is set in `sol.config.json`.

### Duplicate CSS Loading
→ Check for overlapping chunk definitions if `css.splitting` is enabled.