---
name: svelte-i18n-development
description: Comprehensive svelte-i18n development guidance for internationalization, localization, and multi-language support in Svelte applications
---

## What I Cover

This skill provides comprehensive guidance for implementing internationalization (i18n) and localization (l10n) in Svelte applications using svelte-i18n. It covers:

- **Setup and Configuration**: Initializing svelte-i18n, registering locales, and configuring fallback behavior
- **Translation Management**: Loading translation files, handling lazy loading, and organizing translation keys
- **Component Integration**: Using translation functions in Svelte components, reactive locale switching
- **Date/Time Localization**: Integrating with date-fns for locale-aware date formatting
- **Best Practices**: Performance optimization, key naming conventions, and maintainability patterns
- **SSR Support**: Handling server-side rendering and prerendering scenarios
- **Testing**: Strategies for testing internationalized components

## Common Patterns

### Basic Translation Usage
```typescript
import { _ } from 'svelte-i18n';

// In component script
$: greeting = $_('auth.login.button');

// In template
<h1>{$_('auth.login.button')}</h1>
```

### Locale Detection and Initialization
```typescript
// +layout.ts - Project example
import { register, init, getLocaleFromNavigator, waitLocale } from 'svelte-i18n';

// Register locales with lazy loading
register('en', () => import('$lib/i18n/en.json'));
register('da', () => import('$lib/i18n/da.json'));

// Initialize with automatic locale detection
init({
  fallbackLocale: 'en',
  initialLocale: (() => {
    const detected = getLocaleFromNavigator();
    if (detected?.startsWith('da')) return 'da';
    if (detected?.startsWith('en')) return 'en';
    return 'en';
  })()
});

// Wait for translations in load function
export const load: LayoutLoad = async () => {
  await waitLocale();
  return {};
};
```

### Hierarchical Translation Structure
```json
{
  "auth": {
    "email": {
      "label": "Email address",
      "placeholder": "Enter your email",
      "required": "Email is required"
    },
    "login": {
      "button": "Log in",
      "continue": "Continue"
    }
  }
}
```

### Reactive Locale Switching
```svelte
<script>
  import { locale } from 'svelte-i18n';

  $effect(() => {
    document.documentElement.lang = $locale || 'en';
  });
</script>
```

### Date Formatting with Localization
```typescript
import { addWeeks, startOfWeek, endOfWeek, getWeek, format } from 'date-fns';
import { da, enUS } from 'date-fns/locale';
import { locale } from 'svelte-i18n';

const currentLocale = $derived($locale && $locale.startsWith('en') ? enUS : da);
const weekStart = $derived(() => startOfWeek(date, { weekStartsOn: 1 }));
const weekRange = $derived(
  `${format(weekStart(), 'd', { locale: currentLocale })}-${format(weekEnd(), 'd', { locale: currentLocale })} ${format(weekEnd(), 'MMM', { locale: currentLocale })}`
);
```

### Translation with Interpolation
```json
{
  "orders": {
    "product": "Product #{id}"
  }
}
```

```svelte
<p>{$_('orders.product', { values: { id: productId } })}</p>
```

## Best Practices

### Translation Key Organization
- Use hierarchical keys (e.g., `auth.login.button` instead of `loginButton`)
- Group related translations by feature/domain
- Use consistent naming patterns across languages
- Avoid generic keys like "submit" - prefer contextual ones like "auth.login.button"

### Performance Optimization
- Use lazy loading for translation files with `register()`
- Call `waitLocale()` in layout load functions to ensure translations are loaded before rendering
- Avoid loading all locales upfront unless necessary

### Locale Detection
- Use `getLocaleFromNavigator()` for automatic browser language detection
- Implement custom logic for locale persistence (localStorage, URL params)
- Always provide a sensible fallback locale

### Component Patterns
- Import `_` function in components that need translations
- Use `locale` store for reactive locale-dependent logic
- Update `document.documentElement.lang` for accessibility and SEO

### Translation File Management
- Keep translation files in a dedicated `i18n` or `locales` directory
- Use JSON format for simplicity and tooling support
- Maintain consistent structure across all language files
- Use descriptive keys that explain context

### SSR Considerations
- Set `prerender = true` and `ssr = false` for i18n-heavy layouts
- Ensure translations are loaded before component rendering
- Handle locale detection on both client and server sides

## Related Skills

- **sveltekit-development**: Core SvelteKit patterns and layout handling
- **svelte5-development**: Svelte 5 reactive patterns with i18n integration
- **frontend-design**: UI considerations for internationalized interfaces</content>
<parameter name="filePath">.opencode/skill/svelte-i18n-development/SKILL.md