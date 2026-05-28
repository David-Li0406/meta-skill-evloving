---
name: moonbit-luna-ui
description: Use this skill when developing web applications with MoonBit and Luna UI (Sol Framework) for Cloudflare Workers.
---

# MoonBit + Luna UI Development Guide

This guide provides the know-how for developing web applications using MoonBit and Luna UI (Sol Framework) for Cloudflare Workers.

## Prerequisites

### Choosing an Approach

**→ Refer to [ECOSYSTEM.md](./ECOSYSTEM.md)**

There are alternatives to Luna UI (Sol Framework):
- **vite-plugin-moonbit**: For integration into existing Vite projects with HMR support.
- **mizchi/js**: JS FFI bindings (essential library).
- **mizchi/npm_typed**: Bindings for over 50 packages including Hono and Playwright.

Make sure to check existing libraries before writing your own FFI.

### Target Audience

This skill is a guide for using **Luna UI + Sol Framework**. For simpler applications or existing Vite projects, **vite-plugin-moonbit** is recommended.

## Technology Stack Overview

| Technology       | Role                                      |
|------------------|-------------------------------------------|
| MoonBit          | Main language (supports both WASM and JS targets) |
| Luna UI          | UI framework (Island Architecture)        |
| Sol Framework    | Routing, SSR, and Server Actions         |
| Cloudflare Workers| Runtime                                  |
| D1               | SQLite-based database                     |
| Hono             | HTTP middleware (for authentication, etc.) |

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

## Development Commands (just)

Use the `just` command to execute development tasks.

```bash
# Main commands
just dev          # Start development server (wrangler dev)
just build        # Full build
just deploy       # Deploy to Cloudflare Workers

# Build-related
just generate     # Execute sol generate
just moon-build   # Build MoonBit
just bundle       # Bundle client
just clean        # Remove build artifacts

# Testing-related
just test         # Run MoonBit unit tests
just test-e2e     # Run E2E tests
just test-all     # Run all tests

# SSG-related
just ssg          # SSG build
just ssg-preview  # SSG build + preview

# Type checking and linting
just check        # Execute moon check
just fmt          # Execute moon fmt
```

## Build Process

```bash
# Full build
pnpm build
# Internal processes executed:
# 1. sol generate        - Generate __gen__ and .sol
# 2. moon build --target js  - Compile MoonBit to JS
# 3. patch-for-cloudflare.js - Patch for CF Workers
# 4. bundle-client.js    - Bundle Island Components
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

## Detailed References

- Routing and page definitions → [SOL-ROUTING.md](SOL-ROUTING.md)
- Island Components → [ISLAND-COMPONENTS.md](ISLAND-COMPONENTS.md)
- Server Actions → [SERVER-ACTIONS.md](SERVER-ACTIONS.md)
- MoonBit FFI patterns → [MOONBIT-FFI.md](MOONBIT-FFI.md)
- Deploying to Cloudflare Workers → [CLOUDFLARE-DEPLOY.md](CLOUDFLARE-DEPLOY.md)

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
      on=events().click(fn(_) { count
```