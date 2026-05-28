# i18n API Reference

## Table of Contents
1. [Package Exports](#package-exports)
2. [useLanguage Hook](#uselanguage-hook)
3. [useTranslation Hook](#usetranslation-hook)
4. [Trans Component](#trans-component)
5. [Date/Number Formatting](#datenumber-formatting)
6. [Finnish Language Guidelines](#finnish-language-guidelines)

---

## Package Exports

From `@shared-i18n/index`:

```ts
// Core
export { i18n } from './config';
export { I18nProvider } from './provider';

// Hooks
export { useLanguage } from './hooks/useLanguage';
export { useTranslation, Trans } from 'react-i18next';

// Utils
export { setLanguage } from './utils/setLanguage';
export { getDateLocale } from './utils/dateLocale';

// Types
export type { SupportedLanguage, LanguageInfo } from './types';
export { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, FALLBACK_LANGUAGE, LANGUAGE_INFO } from './types';
```

---

## useLanguage Hook

Custom hook for language preference management.

```ts
interface UseLanguageReturn {
  currentLanguage: SupportedLanguage;           // 'fi' | 'en'
  supportedLanguages: Record<SupportedLanguage, LanguageInfo>;
  hasUnsavedChanges: boolean;                   // temp differs from profile
  setLanguageTemporary: (lang: SupportedLanguage) => void;   // localStorage
  saveLanguageToProfile: (lang: SupportedLanguage) => Promise<boolean>;  // DB
  resetToProfileLanguage: () => void;           // discard temp changes
}

// Usage
const { currentLanguage, setLanguageTemporary, saveLanguageToProfile } = useLanguage({
  profileLanguage: profile?.language_preference  // from bootstrap
});
```

---

## useTranslation Hook

From react-i18next. Primary way to access translations.

```ts
const { t, i18n } = useTranslation('namespace');

// Basic usage
t('key')                          // "Translation"
t('nested.key')                   // Access nested JSON
t('key', { defaultValue: 'fallback' })

// Interpolation
t('greeting', { name: 'John' })   // "Hello, John!"

// Pluralization
t('item', { count: 1 })           // "1 item"
t('item', { count: 5 })           // "5 items"

// Namespace override
t('other:key')                    // Load from 'other' namespace

// Language info
i18n.language                     // Current language code
i18n.changeLanguage('en')         // Switch language
```

---

## Trans Component

For translations containing JSX elements.

```tsx
import { Trans } from '@shared-i18n/index';

// JSON: "terms": "By continuing you agree to our <link>terms</link>."
<Trans
  i18nKey="terms"
  t={t}
  components={{ link: <Link to="/terms" /> }}
/>

// With count
<Trans i18nKey="items" count={5}>
  You have <strong>{{count}}</strong> items
</Trans>
```

---

## Date/Number Formatting

Use date-fns with locale-aware formatting:

```ts
import { getDateLocale } from '@shared-i18n/index';
import { format, formatDistance } from 'date-fns';

const locale = getDateLocale(currentLanguage);

// Date formatting
format(date, 'PPP', { locale })           // "January 14, 2026" / "14. tammikuuta 2026"
format(date, 'p', { locale })             // "3:30 PM" / "15.30"

// Relative time
formatDistance(date, new Date(), { locale, addSuffix: true })
// "2 days ago" / "2 päivää sitten"
```

### Number formatting
```ts
const formatter = new Intl.NumberFormat(currentLanguage, {
  style: 'decimal',
  minimumFractionDigits: 2
});
formatter.format(1234.5)  // "1,234.50" (en) / "1 234,50" (fi)
```

---

## Finnish Language Guidelines

Finnish translations require attention to:

### Grammatical cases
Finnish has 15 grammatical cases. Common ones in UI:
- Nominative: basic form ("Kirja" = Book)
- Genitive: possession ("Kirjan" = Book's)
- Partitive: partial/negation ("Kirjaa" = Some book / No book)
- Inessive: inside ("Kirjassa" = In the book)
- Elative: from inside ("Kirjasta" = From the book)
- Illative: into ("Kirjaan" = Into the book)

### Common patterns
```json
{
  "loadingBook": "Ladataan kirjaa...",      // Partitive (partial action)
  "bookLoaded": "Kirja ladattu",            // Nominative (completed)
  "inBook": "Kirjassa",                      // Inessive (location)
  "fromBook": "Kirjasta",                    // Elative (source)
  "chapters_one": "{{count}} luku",          // Singular
  "chapters_other": "{{count}} lukua"        // Partitive plural
}
```

### Verb conjugation
- Infinitive: "tallentaa" (to save)
- Imperative: "Tallenna" (Save!) - use this for buttons
- Present: "tallennetaan" (is being saved)
- Past participle: "tallennettu" (saved)

### Button/action patterns
| English | Finnish | Note |
|---------|---------|------|
| Save | Tallenna | Imperative |
| Cancel | Peruuta | Imperative |
| Delete | Poista | Imperative |
| Loading... | Ladataan... | Present passive |
| Saved | Tallennettu | Past participle |
| Error | Virhe | Nominative |

---

## Namespace Organization

Recommended namespace structure:

| Namespace | Purpose | Example keys |
|-----------|---------|--------------|
| `common` | Shared UI elements | save, cancel, loading, error |
| `profile` | Profile/settings page | tabs.*, audio.*, language.* |
| `reader` | Bible reader UI | verse, chapter, navigation |
| `search` | Search functionality | placeholder, results, filters |
| `admin` | Admin panel | users, settings, dashboard |
| `auth` | Authentication | signIn, signUp, forgotPassword |

---

## Troubleshooting

### Translation not showing
1. Check key exists in both locale files
2. Verify namespace is loaded in config.ts
3. Check for typos in key path

### Language not switching
1. Verify language code in SUPPORTED_LANGUAGES
2. Check localStorage: `localStorage.getItem('i18nextLng')`
3. Clear cache: `localStorage.removeItem('i18nextLng')`

### Suspense boundary errors
Wrap translated content in Suspense:
```tsx
<Suspense fallback={<Loading />}>
  <ComponentWithTranslations />
</Suspense>
```
