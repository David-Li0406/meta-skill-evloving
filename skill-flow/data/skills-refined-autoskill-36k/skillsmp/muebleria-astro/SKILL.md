---
name: muebleria-astro
description: >
  Astro 5-specific patterns for MuebleriaIris.
  Trigger: When working with Astro pages, routing, SSR, Islands, or integrations.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Working with Astro routing"
    - "Creating Astro pages"
    - "Using Astro Islands"
    - "Configuring Astro integrations"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating or modifying Astro pages
- Working with file-based routing
- Using Astro Islands architecture
- Configuring integrations (@astrojs/react)
- Server-side rendering (SSR)
- Static site generation (SSG)

---

## Tech Stack

```
Astro 5.16.4 | File-based routing | Islands architecture
SSR + SSG hybrid | @astrojs/react integration
```

---

## Critical Patterns

### Pattern 1: Astro Component Structure

```astro
---
// Frontmatter (runs server-side, executes once)
import Layout from '@/layouts/Layout.astro';
import { ProductCard } from '@/components/ui/ProductCard';

interface Props {
  title: string;
}

const { title } = Astro.props;

// Fetch data server-side (runs at build or request time)
const response = await fetch('http://localhost:5000/api/productos');
const productos = await response.json();
---

<!-- Template (HTML + components) -->
<Layout title={title}>
  <main>
    <h1>{title}</h1>
    {productos.map(p => (
      <ProductCard {...p} client:load />
    ))}
  </main>
</Layout>
```

### Pattern 2: File-Based Routing

```
src/pages/
├── index.astro                  → /
├── productos/
│   ├── index.astro             → /productos
│   ├── [id].astro              → /productos/123
│   └── categoria/
│       └── [slug].astro        → /productos/categoria/sofas
├── admin/
│   ├── index.astro             → /admin
│   └── productos.astro         → /admin/productos
└── api/
    └── products.json.ts        → /api/products.json (API endpoint)
```

### Pattern 3: Islands Architecture

```astro
---
// Interactive React component in Astro
import { ProductCard } from '@/components/ui/ProductCard';
import { ShoppingCart } from '@/components/ui/ShoppingCart';
---

<div>
  <!-- Static (no JS shipped) -->
  <h1>Productos</h1>
  
  <!-- Interactive on page load -->
  <ProductCard client:load nombre="Sofá" precio={1500} />
  
  <!-- Interactive when visible -->
  <ProductCard client:visible nombre="Mesa" precio={800} />
  
  <!-- Interactive on idle -->
  <ShoppingCart client:idle />
  
  <!-- Hydrate immediately (for critical interactivity) -->
  <button client:only="react">Comprar Ahora</button>
</div>
```

---

## Client Directives

```astro
<!-- NO JavaScript (static HTML) -->
<Component />

<!-- Load immediately -->
<Component client:load />

<!-- Load when visible (lazy load) -->
<Component client:visible />

<!-- Load when browser idle -->
<Component client:idle />

<!-- Load on media query -->
<Component client:media="(max-width: 768px)" />

<!-- Only client-side (no SSR) -->
<Component client:only="react" />
```

**Choose wisely:**
- `client:load` → Critical UI (navigation, forms)
- `client:visible` → Below the fold (product cards)
- `client:idle` → Non-critical (chat, modals)

---

## Dynamic Routes

```astro
---
// src/pages/productos/[id].astro
export async function getStaticPaths() {
  // Generate all possible paths at build time
  const productos = await fetch('http://localhost:5000/api/productos').then(r => r.json());
  
  return productos.map(p => ({
    params: { id: p.id.toString() },
    props: { producto: p }
  }));
}

const { id } = Astro.params;
const { producto } = Astro.props;
---

<Layout title={producto.nombre}>
  <h1>{producto.nombre}</h1>
  <p>${producto.precio}</p>
</Layout>
```

---

## API Endpoints

```typescript
// src/pages/api/productos.json.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  const productos = await fetch('http://localhost:5000/api/productos').then(r => r.json());
  
  return new Response(
    JSON.stringify(productos),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  
  // Proxy to Flask backend
  const response = await fetch('http://localhost:5000/api/productos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  
  return new Response(await response.text(), {
    status: response.status
  });
};
```

---

## Layouts

```astro
---
// src/layouts/Layout.astro
import '@/styles/global.css';

interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Sistema ERP MuebleriaIris' } = Astro.props;
---

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <meta name="description" content={description} />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

---

## Configuration (astro.config.mjs)

```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  // Integrations
  integrations: [react()],
  
  // Vite config
  vite: {
    plugins: [tailwindcss()]
  },
  
  // Output mode
  output: 'static',  // or 'server' for SSR
  
  // Build config
  build: {
    assets: '_astro'
  },
  
  // Server config
  server: {
    port: 4321,
    host: true
  }
});
```

---

## Decision Trees

### When to use Astro vs React

```
Need server-side data?        → Astro page
Static content?               → Astro component
Need interactivity?           → React component with client:* directive
Form with validation?         → React component
SEO critical?                 → Astro page (SSR/SSG)
Need real-time updates?       → React component with client:load
```

### Which client directive?

```
Critical interaction?         → client:load
Below fold?                   → client:visible
Non-critical?                 → client:idle
Mobile only?                  → client:media
No SSR needed?                → client:only
```

---

## Common Patterns

### Fetch Data Server-Side

```astro
---
// Runs once at build/request time
const productos = await fetch('http://localhost:5000/api/productos')
  .then(r => r.json())
  .catch(() => []);  // Fallback
---

<div>
  {productos.length === 0 ? (
    <p>No hay productos</p>
  ) : (
    productos.map(p => <ProductCard {...p} />)
  )}
</div>
```

### Pass Props to Islands

```astro
---
import { InteractiveCard } from '@/components/ui/InteractiveCard';

const data = { id: 1, name: 'Producto' };
---

<!-- Pass server data to client component -->
<InteractiveCard client:load data={data} />
```

---

## Commands

```bash
npm run dev          # Dev server (localhost:4321)
npm run build        # Build for production
npm run preview      # Preview build
npm run astro add react  # Add integration
npm run astro check  # Type check
```

---

## QA Checklist

- [ ] Use client:* directive only when needed
- [ ] Fetch data in frontmatter (server-side)
- [ ] Use appropriate client directive (load/visible/idle)
- [ ] Dynamic routes have getStaticPaths()
- [ ] Layouts are reusable
- [ ] API endpoints return proper status codes
- [ ] SEO meta tags in pages
- [ ] No unnecessary JavaScript shipped

---

## Resources

- **Astro Docs**: https://docs.astro.build
- **Islands Architecture**: https://docs.astro.build/en/concepts/islands/
- **React Integration**: https://docs.astro.build/en/guides/integrations-guide/react/
