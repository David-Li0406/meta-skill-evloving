---
name: i18n-manager
description: Manage internationalization for NutriProfile's 7 languages. Use this skill when adding translations, creating new i18n keys, checking translation coverage, or working with RTL support for Arabic. Ensures consistency across FR, EN, DE, ES, PT, ZH, AR.
allowed-tools: Read,Write,Edit,Grep,Glob
---

# NutriProfile i18n Manager Skill

You are an internationalization expert for the NutriProfile application. This skill helps you manage translations across 7 languages with proper formatting and consistency.

## Supported Languages

| Code | Language | Direction | Status |
|------|----------|-----------|--------|
| `fr` | Français | LTR | Primary |
| `en` | English | LTR | Complete |
| `de` | Deutsch | LTR | Complete |
| `es` | Español | LTR | Complete |
| `pt` | Português | LTR | Complete |
| `zh` | 中文 | LTR | Complete |
| `ar` | العربية | RTL | Complete |

## File Structure

```
frontend/src/i18n/
├── index.ts                    # i18next configuration
└── locales/
    ├── en/
    │   ├── common.json         # Shared translations
    │   ├── auth.json           # Authentication
    │   ├── dashboard.json      # Dashboard
    │   ├── vision.json         # Food analysis
    │   ├── recipes.json        # Recipe generation
    │   ├── tracking.json       # Activity tracking
    │   ├── settings.json       # User settings
    │   ├── onboarding.json     # Onboarding wizard
    │   ├── home.json           # Landing page
    │   ├── pricing.json        # Pricing/subscriptions
    │   ├── terms.json          # Terms of service
    │   ├── privacy.json        # Privacy policy
    │   ├── refund.json         # Refund policy
    │   └── pro.json            # Pro features
    ├── fr/
    │   └── [same structure]
    ├── de/
    ├── es/
    ├── pt/
    ├── zh/
    └── ar/
```

## Namespaces

| Namespace | Purpose | Example Keys |
|-----------|---------|--------------|
| `common` | Shared actions, units, errors | `save`, `cancel`, `error.generic` |
| `auth` | Login, register, password | `login.title`, `register.submit` |
| `dashboard` | Main dashboard | `dashboard.welcome`, `stats.title` |
| `vision` | Food analysis | `vision.analyze`, `result.calories` |
| `recipes` | Recipe generation | `recipes.generate`, `ingredients` |
| `tracking` | Activity/weight | `tracking.activity`, `weight.log` |
| `settings` | User settings | `settings.language`, `account.delete` |
| `onboarding` | Setup wizard | `step1.title`, `goal.weight_loss` |
| `home` | Landing page | `hero.title`, `features.vision` |
| `pricing` | Plans/pricing | `plans.premium`, `trial.title` |

## Usage in Components

### Basic Usage
```typescript
import { useTranslation } from 'react-i18next'

function MyComponent() {
  const { t } = useTranslation('vision')

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
    </div>
  )
}
```

### With Parameters
```typescript
// JSON: "welcome": "Bonjour {{name}} !"
t('welcome', { name: user.name })

// JSON: "count": "{{count}} repas"
t('count', { count: meals.length })
```

### Pluralization
```typescript
// JSON:
// "item": "{{count}} item"
// "item_plural": "{{count}} items"
t('item', { count: items.length })
```

### Multiple Namespaces
```typescript
const { t } = useTranslation(['vision', 'common'])

// Access vision namespace
t('vision:title')

// Access common namespace
t('common:save')
```

## Adding New Translations

### Step-by-Step Process

1. **Identify the namespace** - Choose appropriate namespace for the content

2. **Add to English first** (en/*.json)
```json
{
  "newFeature": {
    "title": "New Feature",
    "description": "This is a new feature",
    "actions": {
      "start": "Get Started",
      "learn": "Learn More"
    }
  }
}
```

3. **Translate to all 6 other languages**

**French (fr):**
```json
{
  "newFeature": {
    "title": "Nouvelle Fonctionnalité",
    "description": "Ceci est une nouvelle fonctionnalité",
    "actions": {
      "start": "Commencer",
      "learn": "En savoir plus"
    }
  }
}
```

**German (de):**
```json
{
  "newFeature": {
    "title": "Neue Funktion",
    "description": "Dies ist eine neue Funktion",
    "actions": {
      "start": "Loslegen",
      "learn": "Mehr erfahren"
    }
  }
}
```

**Spanish (es):**
```json
{
  "newFeature": {
    "title": "Nueva Función",
    "description": "Esta es una nueva función",
    "actions": {
      "start": "Comenzar",
      "learn": "Saber más"
    }
  }
}
```

**Portuguese (pt):**
```json
{
  "newFeature": {
    "title": "Nova Funcionalidade",
    "description": "Esta é uma nova funcionalidade",
    "actions": {
      "start": "Começar",
      "learn": "Saiba mais"
    }
  }
}
```

**Chinese (zh):**
```json
{
  "newFeature": {
    "title": "新功能",
    "description": "这是一个新功能",
    "actions": {
      "start": "开始使用",
      "learn": "了解更多"
    }
  }
}
```

**Arabic (ar):**
```json
{
  "newFeature": {
    "title": "ميزة جديدة",
    "description": "هذه ميزة جديدة",
    "actions": {
      "start": "ابدأ",
      "learn": "اعرف المزيد"
    }
  }
}
```

## RTL Support for Arabic

### CSS Classes
```css
/* Applied automatically when lang="ar" */
[dir="rtl"] {
  text-align: right;
}

/* Flip icons and directional elements */
[dir="rtl"] .icon-arrow {
  transform: scaleX(-1);
}
```

### Component Considerations
```typescript
// Use logical properties instead of left/right
className="ms-4"  // margin-start (left in LTR, right in RTL)
className="me-4"  // margin-end (right in LTR, left in RTL)
className="ps-4"  // padding-start
className="pe-4"  // padding-end

// Tailwind RTL variants
className="text-left rtl:text-right"
className="ml-4 rtl:mr-4 rtl:ml-0"
```

## Checking Translation Coverage

### Find Missing Keys
```bash
# Grep for t() calls without corresponding keys
cd frontend
grep -r "t('" src/ | grep -oP "t\('\K[^']+(?=')" | sort -u > used_keys.txt
```

### Compare Language Files
```bash
# Check if all languages have same keys
diff <(jq -S 'keys' locales/en/vision.json) <(jq -S 'keys' locales/fr/vision.json)
```

## Best Practices

### DO:
- Use nested objects for organization
- Keep keys semantic and descriptive
- Use parameters for dynamic content
- Maintain consistent key naming across namespaces
- Test with longest language (German often longer)
- Check Arabic RTL layout after changes

### DON'T:
- Hardcode ANY user-visible text
- Use translation keys as display text
- Concatenate translated strings
- Assume text length is similar across languages
- Forget to handle pluralization

## Common Translation Patterns

### Button Actions
```json
{
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "submit": "Submit",
    "confirm": "Confirm"
  }
}
```

### Form Labels
```json
{
  "form": {
    "email": "Email",
    "password": "Password",
    "name": "Name",
    "required": "This field is required"
  }
}
```

### Error Messages
```json
{
  "errors": {
    "generic": "An error occurred",
    "network": "Network error. Please try again.",
    "validation": "Please check your input",
    "unauthorized": "Please log in to continue"
  }
}
```

### Success Messages
```json
{
  "success": {
    "saved": "Changes saved successfully",
    "deleted": "Item deleted",
    "created": "Item created successfully"
  }
}
```

## Quality Checklist

Before committing translations:
- [ ] All 7 languages have the new keys
- [ ] Keys are in the correct namespace
- [ ] Parameters match across all languages
- [ ] Pluralization is handled where needed
- [ ] Arabic text reads naturally RTL
- [ ] No hardcoded text remains in component
- [ ] Translations are contextually appropriate
