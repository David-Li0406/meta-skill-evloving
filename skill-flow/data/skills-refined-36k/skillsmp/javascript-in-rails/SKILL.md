---
name: javascript-in-rails
description: Guidance for integrating JavaScript in Rails: import maps, jsbundling-rails (Bun/esbuild/Rollup/Webpack), Turbo helpers, request.js, and UJS replacements. Use when the user asks about JavaScript setup, bundlers, or client-side behavior in Rails.
version: 1.0.0
---

# JavaScript in Rails

Guide Rails applications through JavaScript setup, bundling choices, and
Turbo/UJS replacements using Rails 7+ conventions.

## Choose a JavaScript strategy

### Import maps (default for Rails 7+)
- No Node.js or Yarn required.
- No build step; run `bin/rails server`.
- Use for most Hotwire-first apps and smaller JS needs.

### JavaScript bundlers
- Use Bun, esbuild, Rollup, or Webpack.
- Bundlers integrate via `jsbundling-rails`.
- Run `bin/dev` during development.
- Node.js + Yarn required for esbuild/Rollup/Webpack.
- Bun is both runtime and bundler.

## Import maps

Install (existing apps):
```bash
bundle add importmap-rails
bin/rails importmap:install
```

Pin packages:
```bash
bin/importmap pin react react-dom
```

Import in `app/javascript/application.js`:
```js
import React from "react"
import ReactDOM from "react-dom"
```

Common files:
- `config/importmap.rb`
- `app/javascript/application.js`

## Bundlers

Create a new app with a bundler:
```bash
rails new my_app --javascript=bun
```

Available options:
- `bun`
- `esbuild`
- `rollup`
- `webpack`

## Turbo and UJS replacements

Use Turbo helpers and data attributes instead of Rails UJS:

Method override:
```erb
<%= link_to "Delete", post_path(@post), data: { turbo_method: "delete" } %>
```

Confirmations:
```erb
<%= link_to "Delete", post_path(@post), data: { turbo_confirm: "Are you sure?" } %>
```

Prefer `button_to` for non-GET actions when possible.

## Ajax and request.js

Non-GET requests require `X-CSRF-Token`. Rails Request.JS handles this:
```js
import { FetchRequest } from "@rails/request.js"

const request = new FetchRequest("post", "/posts", {
  body: JSON.stringify({ post: { title: "Hello" } })
})

await request.perform()
```

## When to use this skill
- Choosing between import maps and bundlers
- Setting up or migrating JavaScript tooling
- Turbo helpers and UJS replacements
- request.js and CSRF-safe Ajax
