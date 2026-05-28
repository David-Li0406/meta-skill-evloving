# i18next API Reference

**Version**: 24.2.1

## Official Documentation

- **Introduction**: https://www.i18next.com/overview/api
- **React**: https://react.i18next.com/
- **Translation Functions**: https://www.i18next.com/overview/api#t

## Core API

### useTranslation

Access translation function in components.

```typescript
import { useTranslation } from 'react-i18next';

const { t, i18n } = useTranslation('namespace');

const title = t('key'); // Simple translation
const message = t('key', { count: 5 }); // With parameters
const fallback = t('key', { defaultValue: 'Fallback' });
```

**Returns**:
- `t` - Translation function
- `i18n` - i18next instance
- `ready` - Boolean, namespace loaded

### t() Function

Translate keys with parameters.

```typescript
// Simple
t('welcome');

// With namespace
t('common:welcome');

// With parameters
t('greeting', { name: 'John' }); // "Hello, {{name}}"

// With count (pluralization)
t('item', { count: 1 }); // "1 item"
t('item', { count: 5 }); // "5 items"

// With context
t('friend', { context: 'male' }); // "friend_male"

// With default value
t('missing_key', { defaultValue: 'Fallback text' });

// Returning objects
t('metadata', { returnObjects: true });
```

### i18n Instance

```typescript
// Change language
i18n.changeLanguage('de');

// Get current language
const lang = i18n.language; // 'en'

// Check if key exists
const exists = i18n.exists('key');

// Get fixed T function
const fixedT = i18n.getFixedT('en', 'common');
```

## Configuration

### i18n.init()

Initialize i18next.

```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          welcome: 'Welcome',
        },
      },
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false, // React already escapes
    },
    react: {
      useSuspense: false,
    },
  });
```

**Key Options**:
- `resources` - Translation resources
- `lng` - Default language
- `fallbackLng` - Fallback language
- `ns` - Default namespace(s)
- `defaultNS` - Default namespace
- `interpolation` - Interpolation options
- `react` - React-specific options

## Namespaces

### Using Namespaces

```typescript
// Single namespace
const { t } = useTranslation('common');
t('welcome'); // Looks in common namespace

// Multiple namespaces
const { t } = useTranslation(['common', 'errors']);
t('welcome'); // Looks in common first
t('errors:not_found'); // Explicit namespace
```

### Loading Namespaces

```typescript
i18n.loadNamespaces('profile').then(() => {
  // Namespace loaded
});

// Check if loaded
const isLoaded = i18n.hasLoadedNamespace('profile');
```

## Interpolation

### Basic Interpolation

```typescript
// Translation: "Hello, {{name}}!"
t('greeting', { name: 'John' }); // "Hello, John!"

// Nesting
t('key', { val: t('nested.key') });

// Formatting
t('date', { val: new Date(), formatParams: {
  val: { weekday: 'long', year: 'numeric' }
}});
```

### Formatting

```typescript
// Built-in formats
i18n.init({
  interpolation: {
    format: (value, format, lng) => {
      if (format === 'uppercase') return value.toUpperCase();
      if (format === 'lowercase') return value.toLowerCase();
      return value;
    },
  },
});

// Usage: "{{name, uppercase}}"
t('greeting', { name: 'john' }); // "JOHN"
```

## Pluralization

### Simple Plurals

```typescript
// Translation keys:
// "item_one": "{{count}} item"
// "item_other": "{{count}} items"

t('item', { count: 1 }); // "1 item"
t('item', { count: 5 }); // "5 items"
```

### Complex Plurals

```typescript
// With intervals
// "item_zero": "no items"
// "item_one": "one item"
// "item_other": "{{count}} items"
// "item_many": "many items"

t('item', { count: 0 }); // "no items"
t('item', { count: 1 }); // "one item"
t('item', { count: 5 }); // "5 items"
```

## Context

### Contextual Translations

```typescript
// Translation keys:
// "friend": "friend"
// "friend_male": "boyfriend"
// "friend_female": "girlfriend"

t('friend'); // "friend"
t('friend', { context: 'male' }); // "boyfriend"
t('friend', { context: 'female' }); // "girlfriend"
```

## Events

### Language Change

```typescript
i18n.on('languageChanged', (lng) => {
  console.log('Language changed to:', lng);
});

i18n.off('languageChanged', handler);
```

### Resource Loading

```typescript
i18n.on('loaded', (loaded) => {
  console.log('Resources loaded:', loaded);
});

i18n.on('failedLoading', (lng, ns, msg) => {
  console.error('Failed to load:', lng, ns, msg);
});
```

## Backend Integration

### Dynamic Loading

```typescript
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)
  .init({
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
  });
```

## React Components

### Trans Component

```typescript
import { Trans } from 'react-i18next';

// Translation: "Hello <1>{{name}}</1>!"
<Trans i18nKey="greeting" values={{ name: 'John' }}>
  Hello <strong>{{name}}</strong>!
</Trans>
```

### Translation Component

```typescript
import { Translation } from 'react-i18next';

<Translation>
  {(t, { i18n }) => <Text>{t('welcome')}</Text>}
</Translation>
```

## Custom Hooks

### useTranslation with Options

```typescript
const { t, ready } = useTranslation('namespace', {
  useSuspense: false,
  keyPrefix: 'common.buttons', // Prefix all keys
});

t('submit'); // Looks up 'common.buttons.submit'
```

## Testing

### Mock useTranslation

```typescript
jest.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: {
      changeLanguage: jest.fn(),
      language: 'en',
    },
  }),
}));
```

### Test with Real Translations

```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n.use(initReactI18next).init({
  resources: {
    en: {
      translation: {
        welcome: 'Welcome',
      },
    },
  },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

// Use in tests
render(<Component />, { wrapper: I18nextProvider });
```

## Common Patterns

### Translation Key Conventions

```typescript
// Hierarchical keys
t('feature.screen.title');
t('feature.screen.button.submit');

// Contextual keys
t('error.network'); // "Network error"
t('error.validation'); // "Validation error"

// Component-specific keys
t('cart.empty_state.title');
t('cart.empty_state.description');
```

### Loading States

```typescript
const { t, ready } = useTranslation();

if (!ready) return <LoadingSpinner />;

return <Text>{t('welcome')}</Text>;
```

### Fallback Languages

```typescript
i18n.init({
  fallbackLng: {
    'de-CH': ['de', 'en'],
    'default': ['en'],
  },
});
```

## Key Considerations

- Use namespaces to organize translations by feature
- Always provide fallbackLng for missing translations
- Use interpolation for dynamic values
- Leverage pluralization for count-based strings
- Use context for conditional translations
- Test with mock translations to avoid loading overhead
- Prefix keys with feature names for clarity
- Use `returnObjects: true` for complex structures
- Disable `escapeValue` in React (already escapes)
- Use `keyPrefix` option to avoid repetition
