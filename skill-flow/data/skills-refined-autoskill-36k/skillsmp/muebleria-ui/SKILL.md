---
name: muebleria-ui
description: >
  MuebleriaIris UI patterns: Astro + React + TailwindCSS v4.
  Trigger: When working in src/ on components, layouts, pages, or Astro-specific patterns.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating/modifying UI components"
    - "Working on Astro layouts and pages"
    - "Styling with TailwindCSS v4"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating or modifying Astro components (`.astro` files)
- Building React components for interactive UI
- Working with TailwindCSS v4 styling
- Structuring layouts and pages
- Integrating frontend with Flask API

---

## Tech Stack (Versions)

```
Astro 5.16.4 | React 19.2.1 | TailwindCSS 4.1.17
TypeScript (strict mode) | @astrojs/react 4.4.2
```

---

## Critical Patterns

### Pattern 1: Astro vs React Decision

```
Static content?          → .astro component
Needs interactivity?     → .tsx React component
Form with validation?    → React + react-hook-form
Data fetching?           → Astro (server-side) or React (client-side)
```

### Pattern 2: Component Organization

```
src/
├── components/
│   ├── ui/              # Reusable UI primitives
│   ├── data/            # Data display components
│   ├── desktop/         # Desktop-specific layouts
│   ├── mobile/          # Mobile-specific layouts
│   └── {feature}/       # Feature-specific components
├── layouts/
│   └── Layout.astro     # Base layout wrapper
└── pages/
    └── *.astro          # Routes (file-based routing)
```

---

## Code Examples

### Example 1: Astro Layout

```astro
---
// src/layouts/Layout.astro
import '@/styles/global.css';

interface Props {
  title: string;
}

const { title } = Astro.props;
---

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>{title} - MuebleriaIris</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

### Example 2: React Component

```tsx
// src/components/ui/ProductCard.tsx
interface ProductCardProps {
  nombre: string;
  precio: number;
  imagen_principal: string;
}

export function ProductCard({ nombre, precio, imagen_principal }: ProductCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <img src={imagen_principal} alt={nombre} className="w-full h-48 object-cover" />
      <h3 className="text-lg font-semibold mt-2">{nombre}</h3>
      <p className="text-xl text-green-600">${precio}</p>
    </div>
  );
}
```

---

## Commands

```bash
npm run dev          # localhost:4321
npm run build        # Production build
npm run preview      # Preview build
```

---

## Resources

- **API Reference**: See `backend/app/routes.py`
