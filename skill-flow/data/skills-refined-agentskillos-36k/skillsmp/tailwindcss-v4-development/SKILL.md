---
name: tailwindcss-v4-development
description: Comprehensive Tailwind CSS v4 development guidance for modern CSS-in-JS patterns, responsive design, and performance optimization
---

# Tailwind CSS v4 Development Skill

## What I Cover

This skill provides comprehensive guidance for developing with Tailwind CSS v4, focusing on:

- **Modern CSS Architecture**: @theme directive, CSS variables, and design tokens
- **Performance Optimization**: Bundle size reduction, purging, and tree-shaking
- **Responsive Design**: Mobile-first approach, breakpoint management, and fluid typography
- **Component Patterns**: Utility-first composition, CSS-in-JS integration, and reusable patterns
- **Build Integration**: Vite plugin setup, SvelteKit compatibility, and production builds
- **Migration Strategies**: Upgrading from v3 to v4, compatibility considerations

## Common Patterns

### Theme Configuration with @theme

```css
@import 'tailwindcss';

@theme {
  /* Primary color palette */
  --color-primary: var(--color-slate-800);
  --color-primary-hover: var(--color-slate-700);
  --color-ring-primary: var(--color-slate-600);

  /* Semantic color aliases */
  --color-muted: var(--color-slate-50);
  --color-success: var(--color-green-600);
  --color-danger: var(--color-red-600);

  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
}
```

### Utility-First Component Composition

```svelte
<!-- LoginLayout.svelte -->
<div class="min-h-screen flex items-center justify-center">
  <div class="max-w-md w-full p-6 bg-white rounded-lg shadow-md">
    <div class="flex justify-center mb-6">
      <img src="{base}/GoPayBadEdition.png" alt="Logo" class="h-28 w-auto" />
    </div>
    {@render children?.()}
  </div>
</div>
```

### Responsive Design Patterns

```svelte
<!-- Responsive card grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-muted p-4 rounded-lg">
    <!-- Card content -->
  </div>
</div>

<!-- Fluid typography -->
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">
  Responsive heading
</h1>
```

### CSS-in-JS with Tailwind Classes

```svelte
<script>
  let isLoading = $state(false);
</script>

<button
  class="px-4 py-2 bg-primary text-white rounded hover:bg-primary-hover disabled:opacity-50"
  disabled={isLoading}
>
  {#if isLoading}
    <span class="animate-spin">⟳</span>
  {/if}
  Submit
</button>
```

## Best Practices

### Performance Optimization

1. **Use semantic color tokens** instead of hardcoded values:
   ```css
   /* Good */
   .btn-primary { @apply bg-primary hover:bg-primary-hover; }

   /* Avoid */
   .btn-primary { @apply bg-slate-800 hover:bg-slate-700; }
   ```

2. **Leverage CSS variables for theming**:
   ```css
   @theme {
     --color-brand: #3b82f6;
     --color-brand-dark: #2563eb;
   }
   ```

3. **Minimize bundle size** with tree-shaking:
   - Only import used utilities
   - Use @apply for repeated patterns
   - Configure content paths correctly

### Responsive Design

1. **Mobile-first approach**:
   ```svelte
   <!-- Mobile styles first, then overrides -->
   <div class="text-sm md:text-base lg:text-lg">
     Responsive text
   </div>
   ```

2. **Use container queries** for component-based responsive design:
   ```css
   .card {
     container-type: inline-size;
   }

   @container (min-width: 400px) {
     .card-content { @apply grid-cols-2; }
   }
   ```

3. **Fluid typography** with clamp:
   ```css
   .fluid-text {
     font-size: clamp(1rem, 2vw + 0.5rem, 2rem);
   }
   ```

### Component Architecture

1. **Utility-first composition**:
   ```svelte
   <!-- Button component -->
   <button class={twMerge(
     "px-4 py-2 rounded font-medium transition-colors",
     variant === 'primary' && "bg-primary text-white hover:bg-primary-hover",
     variant === 'secondary' && "bg-secondary text-slate-900 hover:bg-secondary-hover",
     size === 'sm' && "text-sm px-3 py-1",
     size === 'lg' && "text-lg px-6 py-3",
     className
   )}>
     {@render children?.()}
   </button>
   ```

2. **Consistent spacing scale**:
   ```css
   @theme {
     --spacing-1: 0.25rem;
     --spacing-2: 0.5rem;
     --spacing-3: 1rem;
     --spacing-4: 1.5rem;
   }
   ```

### Project-Specific Examples

Based on this SvelteKit + Tailwind CSS v4 project:

1. **Custom color tokens** in `app.css`:
   ```css
   @theme {
     --color-primary: var(--color-slate-800);
     --color-muted: var(--color-slate-50);
     --color-success: var(--color-green-600);
   }
   ```

2. **Vite integration** in `vite.config.ts`:
   ```typescript
   import tailwindcss from '@tailwindcss/vite';
   export default defineConfig({
     plugins: [tailwindcss(), sveltekit()],
   });
   ```

3. **Layout components** using semantic classes:
   ```svelte
   <div class="min-h-screen bg-muted">
     <!-- Content -->
   </div>
   ```

## Related Skills

- **sveltekit-development**: Framework integration and routing patterns
- **frontend-design**: UI/UX principles and design system creation
- **svelte5-development**: Modern Svelte patterns with Tailwind
- **software-architecture**: CSS architecture and design token management</content>
<parameter name="filePath">.opencode/skill/tailwindcss-v4-development/SKILL.md