---
name: sveltekit-development
description: Comprehensive SvelteKit development guidance for building modern web applications with static site generation, TypeScript, and TailwindCSS v4
---

## What I Cover

This skill provides guidance for developing web applications using SvelteKit, focusing on:

- **File-based routing** and layout composition in `src/routes/`
- **Data loading patterns** using `load` functions for server-side and client-side data fetching
- **Form handling** with SvelteKit actions and progressive enhancement
- **API routes** for dynamic data endpoints
- **Static site generation** using `@sveltejs/adapter-static` for deployment to GitHub Pages
- **Component architecture** following atomic design principles (atoms/molecules/organisms/templates)
- **TypeScript integration** for type-safe development
- **TailwindCSS v4** styling with custom theme configuration
- **Svelte 5 runes** for reactive state management
- **Deployment workflows** to static hosting platforms

## Common Patterns

### Project Structure
```
frontend/
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # Home page
│   │   ├── login/+page.svelte    # Route-specific page
│   │   ├── +layout.svelte        # Root layout
│   │   └── debug/
│   │       ├── +page.svelte      # Debug overview
│   │       └── atoms/+page.svelte # Debug atoms
│   ├── lib/
│   │   ├── features/             # Feature-based organization
│   │   │   ├── orders/
│   │   │   │   ├── atoms/
│   │   │   │   ├── molecules/
│   │   │   │   ├── organisms/
│   │   │   │   └── templates/
│   │   │   └── auth/
│   │   ├── components/           # Shared atomic components
│   │   └── core/                 # Core functionality (loading, notifications)
│   ├── app.css                  # Global styles with Tailwind v4
│   └── app.d.ts                 # TypeScript declarations
├── svelte.config.js             # Static adapter configuration
└── package.json                 # Dependencies and scripts
```

### Static Generation Configuration
```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: undefined,
      precompress: false,
      strict: true
    }),
    paths: {
      base: process.argv.includes('dev') ? '' : process.env.BASE_PATH
    }
  }
};
```

### TailwindCSS v4 Theme
```css
/* src/app.css */
@import 'tailwindcss';

@theme {
  /* Custom color palette */
  --color-primary: var(--color-slate-800);
  --color-primary-hover: var(--color-slate-700);
  --color-muted: var(--color-slate-50);
  --color-success: var(--color-green-600);
  --color-danger: var(--color-red-600);
}
```

### Component Organization
Following atomic design:
- **Atoms**: Basic UI elements (Button, Input, Icon)
- **Molecules**: Combinations of atoms (FormField, NotificationItem)
- **Organisms**: Complex components (AuthForm, OrderCard)
- **Templates**: Page layouts (LoginLayout, DayViewTemplate)

### Data Loading Example
```typescript
// src/routes/orders/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  const response = await fetch('/api/orders');
  const orders = await response.json();
  
  return {
    orders
  };
};
```

## Best Practices

### TypeScript Integration
- Use TypeScript for all components and utilities
- Define proper interfaces for data structures
- Leverage SvelteKit's generated types (`$types`)
- Enable strict type checking in `tsconfig.json`

### Static Site Generation
- Design for static generation from the start
- Use `load` functions for data that can be pre-rendered
- Handle dynamic data through client-side JavaScript
- Configure adapter-static for optimal deployment

### Component Design
- Follow atomic design for maintainable components
- Use Svelte 5 runes for reactive state
- Implement proper error boundaries
- Optimize component re-rendering with `$:` reactive statements

### Styling with TailwindCSS v4
- Define custom theme variables in `@theme` directive
- Use semantic color names (primary, secondary, muted)
- Leverage Tailwind's utility classes for responsive design
- Minimize custom CSS in favor of utility classes

### Performance Optimization
- Use static generation for better performance
- Implement code splitting with dynamic imports
- Optimize images and assets for web
- Monitor bundle size with build analysis

### Development Workflow
- Use `npm run check` for type checking
- Run `npm run lint` for code quality
- Test static builds with `npm run build && npm run preview`
- Use debug routes for component development

## Related Skills

- **vite**: Build tool and development server used by SvelteKit
- **bun**: Alternative JavaScript runtime for faster development
- **github-actions**: CI/CD pipelines for automated deployment
- **frontend-design**: UI/UX design patterns and component libraries