# Kyotee: Hono + Datastar on Cloudflare Workers

Use these patterns when building hypermedia-driven apps with Hono and Datastar on Cloudflare Workers.

## Project Structure

```
src/
  index.ts           # Hono app entry point
  components/        # Server-rendered HTML components
    layout.ts        # Base HTML layout with Datastar
    nav.ts
    forms/
  routes/            # Route handlers
    api.ts           # API/SSE endpoints
  lib/               # Utilities
    html.ts          # HTML helpers
    sse.ts           # SSE streaming helpers
public/              # Static assets (served via wrangler)
  styles.css
wrangler.toml
package.json
tsconfig.json
```

## Naming Conventions

- **Files**: kebab-case (`user-profile.ts`)
- **Functions**: camelCase (`export function userProfile()`)
- **Components**: Return `HtmlEscapedString` from `hono/html`
- **Routes**: Group by feature in `/routes`

## wrangler.toml

```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[assets]
directory = "./public"
```

## package.json

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "hono": "^4"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4",
    "typescript": "^5",
    "wrangler": "^3"
  }
}
```

## Layout with Datastar

```typescript
// src/components/layout.ts
import { html } from 'hono/html'
import type { HtmlEscapedString } from 'hono/utils/html'

export const layout = (content: HtmlEscapedString, title = 'My App') => html`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <script type="module" src="https://cdn.jsdelivr.net/npm/@starfederation/datastar"></script>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  ${content}
</body>
</html>
`
```

## Hono App Setup

```typescript
// src/index.ts
import { Hono } from 'hono'
import { html } from 'hono/html'
import { layout } from './components/layout'
import { apiRoutes } from './routes/api'

const app = new Hono()

// Home page
app.get('/', (c) => {
  return c.html(layout(html`
    <main>
      <h1>Welcome</h1>
    </main>
  `))
})

// API routes
app.route('/api', apiRoutes)

export default app
```

## Datastar Signals Pattern

```typescript
// Signals are declared with data-signals
// Use JSON syntax for initial values
html`
<div data-signals='{"count": 0, "name": ""}'>
  <p>Count: <span data-text="$count"></span></p>
  <button data-on-click="$count++">Increment</button>
</div>
`
```

## Datastar Click Actions

```typescript
// Client-side action
html`<button data-on-click="$count++">Add</button>`

// Server request (GET)
html`<button data-on-click="@get('/api/items')">Load Items</button>`

// Server request (POST with signals)
html`<button data-on-click="@post('/api/items')">Submit</button>`

// Server request (DELETE)
html`<button data-on-click="@delete('/api/items/1')">Delete</button>`
```

## Datastar Form Pattern

```typescript
html`
<form
  data-signals='{"email": "", "message": ""}'
  data-on-submit__prevent="@post('/api/contact')"
>
  <input type="email" data-bind="email" placeholder="Email">
  <textarea data-bind="message" placeholder="Message"></textarea>
  <button type="submit">Send</button>
</form>
`
```

## SSE Response Pattern (Datastar Backend)

```typescript
// src/routes/api.ts
import { Hono } from 'hono'
import { streamSSE } from 'hono/streaming'

const api = new Hono()

// Return HTML fragments via SSE
api.get('/items', async (c) => {
  return streamSSE(c, async (stream) => {
    const items = await getItems()

    // Send fragment to merge into DOM
    await stream.writeSSE({
      event: 'datastar-merge-fragments',
      data: `<div id="items-list">
        ${items.map(item => `<div>${item.name}</div>`).join('')}
      </div>`
    })
  })
})

// Handle form submission
api.post('/contact', async (c) => {
  const signals = await c.req.json()

  // Process form data from signals
  await saveContact(signals.email, signals.message)

  return streamSSE(c, async (stream) => {
    // Update signals on client
    await stream.writeSSE({
      event: 'datastar-merge-signals',
      data: 'signals {"email": "", "message": ""}'
    })

    // Show success message
    await stream.writeSSE({
      event: 'datastar-merge-fragments',
      data: '<div id="form-status" class="success">Sent!</div>'
    })
  })
})

export { api as apiRoutes }
```

## SSE Helper

```typescript
// src/lib/sse.ts
import type { SSEStreamingApi } from 'hono/streaming'

export const sendFragment = async (
  stream: SSEStreamingApi,
  html: string,
  options?: { settle?: number }
) => {
  let data = html.trim()
  if (options?.settle) {
    data = `settle ${options.settle}\n${data}`
  }
  await stream.writeSSE({
    event: 'datastar-merge-fragments',
    data
  })
}

export const sendSignals = async (
  stream: SSEStreamingApi,
  signals: Record<string, unknown>
) => {
  await stream.writeSSE({
    event: 'datastar-merge-signals',
    data: `signals ${JSON.stringify(signals)}`
  })
}

export const sendRedirect = async (
  stream: SSEStreamingApi,
  url: string
) => {
  await stream.writeSSE({
    event: 'datastar-execute-script',
    data: `script window.location.href = '${url}'`
  })
}
```

## Datastar Attributes Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `data-signals` | Declare reactive signals | `data-signals='{"x": 0}'` |
| `data-bind` | Two-way binding | `data-bind="email"` |
| `data-text` | Text content | `data-text="$count"` |
| `data-show` | Conditional display | `data-show="$isOpen"` |
| `data-class` | Dynamic classes | `data-class="{'active': $isActive}"` |
| `data-on-click` | Click handler | `data-on-click="@get('/api/x')"` |
| `data-on-submit` | Form submit | `data-on-submit__prevent="@post('/api/x')"` |
| `data-indicator` | Loading indicator | `data-indicator="#spinner"` |

## Loading States

```typescript
html`
<div>
  <button
    data-on-click="@get('/api/slow')"
    data-indicator="#loading"
  >
    Load Data
  </button>
  <span id="loading" style="display:none">Loading...</span>
</div>
`
```

## D1 Database Integration

```typescript
// wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

// src/index.ts
type Env = {
  DB: D1Database
}

const app = new Hono<{ Bindings: Env }>()

app.get('/api/items', async (c) => {
  const items = await c.env.DB.prepare('SELECT * FROM items').all()
  return c.json(items.results)
})
```

## KV Storage Integration

```typescript
// wrangler.toml
[[kv_namespaces]]
binding = "CACHE"
id = "xxx"

// Usage
const value = await c.env.CACHE.get('key')
await c.env.CACHE.put('key', 'value', { expirationTtl: 3600 })
```

## Tips

- **No build step needed** - Wrangler handles TypeScript
- **Use `html` helper** - Auto-escapes values, prevents XSS
- **SSE for updates** - Datastar expects SSE responses for @get/@post
- **Signals are JSON** - Always use valid JSON in `data-signals`
- **ID your fragments** - Datastar merges by matching element IDs
- **Streaming** - Use `streamSSE` for real-time updates
