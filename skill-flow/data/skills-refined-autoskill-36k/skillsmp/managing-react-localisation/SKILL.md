---
name: managing-react-localisation
description: Manage i18next translations and localisation in React with TypeScript. Use when adding translations, creating language files, implementing i18n, or when user mentions translations, localisation, i18next, languages, or multi-language support.
---

# Manage React Localisation

Manage i18next translations and localisation for React applications with TypeScript. Organize translation files by locale and namespace, use the `useTranslation` hook for component access, and follow consistent key naming patterns for maintainability.

## File Structure

Translation files are organized by locale:

```
resources/locales/{locale}/{namespace}.json
```

**Examples:**

- `resources/locales/en/translation.json` (default namespace)
- `resources/locales/en/validation.json`
- `resources/locales/es/translation.json`
- `resources/locales/fr/validation.json`

## Core Conventions

### 1. Using the `useTranslation` Hook

Access translations in components:

```tsx
import { useTranslation } from 'react-i18next'

export function WelcomeMessage() {
  const { t } = useTranslation()

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('welcomeDescription')}</p>
    </div>
  )
}
```

**With interpolation:**

```tsx
export function UserGreeting({ name }: { name: string }) {
  const { t } = useTranslation()

  return <h1>{t('greeting', { name })}</h1>
}
```

Translation file (`resources/locales/en/translation.json`):

```json
{
  "greeting": "Hello, {{name}}!"
}
```

### 2. Using Namespaces

Access specific translation namespaces:

```tsx
import { useTranslation } from 'react-i18next'

export function LoginForm() {
  const { t } = useTranslation() // Default namespace
  const { t: tValidation } = useTranslation('validation')

  return (
    <form>
      <h1>{t('logIn')}</h1>
      <Input error={tValidation('required', { attribute: 'email' })} />
    </form>
  )
}
```

Or use namespace prefix:

```tsx
export function LoginForm() {
  const { t } = useTranslation()

  return (
    <form>
      <h1>{t('logIn')}</h1>
      <Input error={t('validation:required', { attribute: 'email' })} />
    </form>
  )
}
```

### 3. Translation File Structure

**Default namespace** (`resources/locales/en/translation.json`):

```json
{
  "welcome": "Welcome",
  "logIn": "Log In",
  "register": "Register",
  "email": "Email",
  "password": "Password",
  "name": "Name",
  "alreadyHaveAccount": "Already have an account?",
  "registerNewAccount": "Register new account",
  "registerNewAccountDescription": "Create your account to get started"
}
```

**Validation namespace** (`resources/locales/en/validation.json`):

```json
{
  "required": "The {{attribute}} field is required.",
  "email": "The {{attribute}} must be a valid email address.",
  "min": {
    "string": "The {{attribute}} must be at least {{min}} characters."
  },
  "confirmed": "The {{attribute}} confirmation does not match.",
  "boolean": "The {{attribute}} field must be true or false."
}
```

### 4. Using Translations in Form Validation

Integrate with Zod schemas:

```tsx
import { useFormValidation } from '@/hooks/use-form-validation'
import { useTranslation } from 'react-i18next'
import { z } from 'zod'

export default function Register() {
  const { t } = useTranslation()
  const { passwordConfirmationMessage } = useFormValidation()

  const formSchema = z
    .object({
      name: z.string(),
      email: z.string().email(),
      password: z.string().min(8),
      password_confirmation: z.string().min(8),
    })
    .refine(
      (data) => data.password === data.password_confirmation,
      passwordConfirmationMessage
    )

  // ...
}
```

In `useFormValidation` hook:

```ts
export function useFormValidation() {
  const { t } = useTranslation()

  const passwordConfirmationMessage: z.core.$ZodCustomParams = {
    message: t('validation:confirmed', {
      attribute: t('password').toLowerCase(),
    }),
    path: ['password'],
  }

  const customErrorMap: z.ZodErrorMap = (issue) => {
    switch (issue.code) {
      case 'invalid_type':
        return t('validation:required', {
          attribute: pathToAttribute(issue.path),
        })
      // ... more cases
    }
  }

  return { passwordConfirmationMessage, customErrorMap }
}
```

## Examples

### Example 1: Component with Translations

```tsx
import { Button } from '@/components/ui/button'
import { useTranslation } from 'react-i18next'

export function LogoutButton() {
  const { t } = useTranslation()

  const handleLogout = () => {
    // logout logic
  }

  return (
    <Button onClick={handleLogout} variant="ghost">
      {t('logOut')}
    </Button>
  )
}
```

Translation file:

```json
{
  "logOut": "Log Out"
}
```

### Example 2: Translations with Pluralization

```tsx
export function ItemCount({ count }: { count: number }) {
  const { t } = useTranslation()

  return <p>{t('itemCount', { count })}</p>
}
```

Translation file:

```json
{
  "itemCount_one": "{{count}} item",
  "itemCount_other": "{{count}} items"
}
```

### Example 3: Date Formatting with Locale

```tsx
import { usePage } from '@inertiajs/react'
import { useTranslation } from 'react-i18next'

export function FormattedDate({ date }: { date: string }) {
  const { i18n } = useTranslation()
  const locale = i18n.language

  const formatted = new Date(date).toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return <time dateTime={date}>{formatted}</time>
}
```

### Example 4: Language Switcher

```tsx
import { router, usePage } from '@inertiajs/react'
import { useTranslation } from 'react-i18next'
import type { SupportedLocale } from '@/types'

export function LanguageSwitcher() {
  const { i18n } = useTranslation()
  const { supportedLocales } = usePage().props

  const handleChange = (locale: string) => {
    router.post(
      route('locale.update'),
      { language: locale },
      {
        onSuccess: () => {
          i18n.changeLanguage(locale)
        },
      }
    )
  }

  return (
    <select
      value={i18n.language}
      onChange={(e) => handleChange(e.target.value)}
    >
      {Object.entries(supportedLocales).map(([code, locale]) => (
        <option key={code} value={code}>
          {locale.native_name}
        </option>
      ))}
    </select>
  )
}
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't hardcode strings
export function Welcome() {
  return <h1>Welcome to the app</h1> // ❌ Use t('welcome')
}

// Don't call useTranslation conditionally
export function Message({ show }: { show: boolean }) {
  if (show) {
    const { t } = useTranslation() // ❌ Hooks must be at top level
    return <p>{t('message')}</p>
  }
  return null
}

// Don't use translation keys as fallbacks
export function Title() {
  const { t } = useTranslation()
  return <h1>{t('title') || 'Default Title'}</h1> // ❌ Define in translation file
}

// Don't nest translation objects too deeply
{
  "user": {
    "profile": {
      "settings": {
        "privacy": {
          "title": "Privacy" // ❌ Too deep
        }
      }
    }
  }
}
```

### ✅ Do This Instead

```tsx
// Use translations
export function Welcome() {
  const { t } = useTranslation()
  return <h1>{t('welcome')}</h1>
}

// Call useTranslation at top level
export function Message({ show }: { show: boolean }) {
  const { t } = useTranslation()

  if (!show) return null

  return <p>{t('message')}</p>
}

// Define default in translation file
export function Title() {
  const { t } = useTranslation()
  return <h1>{t('title')}</h1>
}

// Keep translation keys flat
{
  "userPrivacyTitle": "Privacy",
  "userProfileSettings": "Profile Settings"
}
```

## Translation File Organization

**Group related translations:**

```json
{
  "logIn": "Log In",
  "logOut": "Log Out",
  "register": "Register",
  "registerNewAccount": "Register new account",
  "registerNewAccountDescription": "Create your account to get started",
  "alreadyHaveAccount": "Already have an account?",
  "forgotPassword": "Forgot your password?"
}
```

**Use consistent naming:**

```json
{
  "buttonSave": "Save",
  "buttonCancel": "Cancel",
  "buttonDelete": "Delete",
  "labelEmail": "Email",
  "labelPassword": "Password",
  "errorRequired": "This field is required"
}
```

## Quality Standards

- All user-facing text must be translatable
- Use `useTranslation()` hook for all translations
- Keep translation keys in camelCase
- Use interpolation for dynamic values
- Provide translations for all supported locales
- Use namespaces to organize translations
- Test UI in all supported languages
- Ensure date/number formatting respects locale
