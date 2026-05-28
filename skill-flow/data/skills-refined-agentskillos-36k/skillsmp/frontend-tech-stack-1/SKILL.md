---
name: frontend-tech-stack
description: Provides standards for the frontend application technology stack. This skill should be used when setting up new frontend projects or upgrading existing ones with React 19, Vite, and Tailwind v4.
---

# Frontend Tech Stack

This skill defines the standard technology stack for all frontend applications (`erify_creators`, `erify_studios`, etc.) in the project.

## Core Core Technologies

| Category        | Technology          | Version  | Notes                                     |
| :-------------- | :------------------ | :------- | :---------------------------------------- |
| **Framework**   | **React**           | **19.x** | Use functional components and hooks.      |
| **Build Tool**  | **Vite**            | **6.x**  | Fast HMR, uses `@vitejs/plugin-react`.    |
| **Styling**     | **Tailwind CSS**    | **4.x**  | Use the `@tailwindcss/vite` plugin.       |
| **Routing**     | **TanStack Router** | **1.x**  | File-based routing, type-safe navigation. |
| **State/Query** | **TanStack Query**  | **5.x**  | For async server state management.        |
| **I18n**        | **Paraglide JS**    | **2.x**  | Type-safe internationalization.           |

## Project Structure

Frontend apps should follow this structure:

```
src/
├── routes/             # TanStack Router file-based routes
│   ├── __root.tsx      # Root layout
│   ├── index.tsx       # Homepage
│   └── feature.tsx     # Feature route
├── components/         # App-specific components
├── hooks/              # App-specific hooks
├── lib/                # Utilities and API clients
├── main.tsx            # Entry point
└── index.css           # Global styles (Tailwind imports)
```

## Configuration

### Vite Config ("vite.config.ts")

Ensures Tailwind v4 and TanStack Router integration:

```typescript
import tailwindcss from '@tailwindcss/vite';
import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    tanstackRouter(),
    react(),
    tailwindcss(),
  ],
});
```

### Tailwind Config (v4)

Tailwind v4 uses CSS-first configuration. Your `index.css` should look like:

```css
@import "tailwindcss";

@theme {
  --font-sans: "Inter", sans-serif;
  /* Define custom tokens here */
}
```

## Checklist

- [ ] Project is initialized with Vite + React + TypeScript.
- [ ] Uses Tailwind CSS v4 plugin.
- [ ] Uses TanStack Router for navigation.
- [ ] Depends on workspace packages (`@eridu/ui`, `@eridu/api-types`) where appropriate.
