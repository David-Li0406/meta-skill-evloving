---
name: nextjs-i18n
description: Implement and manage internationalization (i18n) for the LucidData Next.js application using next-intl. Use when adding multi-language support, creating translation files, configuring locale routing, or adapting UI components for internationalization. Supports data sovereignty compliance through localized consent forms and privacy policies.
license: MIT
compatibility: Designed for Claude Code and GitHub Copilot. Requires Next.js 15+ with App Router. Uses next-intl library for i18n implementation.
metadata:
  author: LucidData Team
  version: "1.0"
  framework: Next.js 15 App Router
  library: next-intl
  priority_locales: ["en", "es", "fr", "de"]
allowed-tools: Bash(npm:*) Read Write Edit
---

# Next.js Internationalization (i18n)

Internationalization implementation for the LucidData Next.js application using next-intl.

## Overview

This skill enables multi-language support for LucidData, allowing the application to serve users in different locales with properly translated content. While not currently required, i18n infrastructure future-proofs the application for international expansion and ensures compliance with data sovereignty laws requiring localized consent forms.

## When to Use This Skill

Activate this skill when you need to:

- **Setup i18n**: Install next-intl and configure locale routing
- **Add languages**: Support Spanish, French, German, or other locales
- **Translate content**: Create translation files for UI text
- **Localize consent forms**: Translate legal language for GDPR compliance
- **Format dates/numbers**: Display locale-appropriate formatting
- **Handle pluralization**: Implement locale-specific plural rules
- **Test translations**: Verify all locales render correctly

## Why i18n Matters for LucidData

### Data Sovereignty Compliance
- **GDPR (EU)**: Requires consent forms in user's language
- **LGPD (Brazil)**: Portuguese translations mandatory
- **PIPEDA (Canada)**: English and French required

### International Expansion
- Prepares for multi-market launch
- Improves user trust with native language
- Reduces legal risk from mistranslated consent

### User Experience
- Users understand privacy controls better in native language
- Increases consent comprehension
- Builds trust in data handling

## Recommended Library: next-intl

**Why next-intl?**
- Built for Next.js 15 App Router
- Server Component support
- TypeScript-first
- Lightweight (~2KB gzipped)
- Active maintenance

**Alternatives considered:**
- `next-i18next` - Designed for Pages Router (not App Router)
- `react-i18next` - Larger bundle, more client-side

## Implementation Phases

### Phase 1: Installation & Setup

```bash
# Install next-intl
npm install next-intl

# Create i18n configuration
# File: i18n.ts
```

**i18n.ts**:
```typescript
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default
}));
```

### Phase 2: Middleware Configuration

**middleware.ts** (update existing):
```typescript
import createMiddleware from 'next-intl/middleware';
import { createServerClient } from '@supabase/ssr';

const i18nMiddleware = createMiddleware({
  locales: ['en', 'es', 'fr', 'de'],
  defaultLocale: 'en'
});

export async function middleware(request: NextRequest) {
  // Run i18n middleware first
  const response = i18nMiddleware(request);

  // Then run Supabase auth middleware
  // ... existing auth logic ...

  return response;
}

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)']
};
```

### Phase 3: Directory Structure

```
messages/
├── en.json          # English (default)
├── es.json          # Spanish
├── fr.json          # French
└── de.json          # German

app/
└── [locale]/        # Dynamic locale segment
    ├── layout.tsx   # i18n-aware layout
    ├── page.tsx     # Landing page
    ├── (auth)/
    │   ├── login/page.tsx
    │   └── signup/page.tsx
    └── (dashboard)/
        ├── dashboard/page.tsx
        ├── vault/page.tsx
        ├── consent/page.tsx
        └── audit/page.tsx
```

### Phase 4: Root Layout Update

**app/[locale]/layout.tsx**:
```typescript
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export async function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'es' }, { locale: 'fr' }, { locale: 'de' }];
}

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### Phase 5: Translation Files

**messages/en.json**:
```json
{
  "common": {
    "appName": "Lucid",
    "tagline": "Your Personal Data Bank",
    "actions": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete",
      "edit": "Edit",
      "create": "Create",
      "view": "View"
    }
  },
  "nav": {
    "dashboard": "Dashboard",
    "vault": "Vault",
    "consent": "Consent",
    "audit": "Audit Log",
    "settings": "Settings"
  },
  "vault": {
    "title": "Data Vault",
    "description": "Securely store your personal information",
    "create": "Create Entry",
    "empty": "No entries yet. Create your first one!",
    "labels": {
      "label": "Label",
      "category": "Category",
      "metadata": "Metadata",
      "createdAt": "Created"
    },
    "categories": {
      "identity": "Identity",
      "financial": "Financial",
      "health": "Health",
      "contact": "Contact",
      "employment": "Employment",
      "education": "Education"
    }
  },
  "consent": {
    "title": "Consent Management",
    "description": "Control who accesses your data",
    "grant": "Grant Consent",
    "revoke": "Revoke Consent",
    "labels": {
      "grantedTo": "Granted To",
      "purpose": "Purpose",
      "accessLevel": "Access Level",
      "duration": "Duration",
      "status": "Status"
    },
    "status": {
      "active": "Active",
      "expired": "Expired",
      "revoked": "Revoked"
    },
    "legal": {
      "agreement": "I consent to share this data for the stated purpose and duration.",
      "gdprNotice": "You have the right to withdraw consent at any time."
    }
  },
  "audit": {
    "title": "Audit Log",
    "description": "Track all data access and changes",
    "events": {
      "DATA_CREATED": "Data Created",
      "DATA_UPDATED": "Data Updated",
      "DATA_DELETED": "Data Deleted",
      "CONSENT_GRANTED": "Consent Granted",
      "CONSENT_REVOKED": "Consent Revoked"
    }
  },
  "auth": {
    "login": "Sign In",
    "signup": "Sign Up",
    "logout": "Sign Out",
    "email": "Email",
    "password": "Password"
  }
}
```

**messages/es.json** (Spanish):
```json
{
  "common": {
    "appName": "Lucid",
    "tagline": "Tu Banco de Datos Personal",
    "actions": {
      "save": "Guardar",
      "cancel": "Cancelar",
      "delete": "Eliminar",
      "edit": "Editar",
      "create": "Crear",
      "view": "Ver"
    }
  },
  "vault": {
    "title": "Bóveda de Datos",
    "description": "Almacena de forma segura tu información personal",
    "create": "Crear Entrada"
  },
  "consent": {
    "title": "Gestión de Consentimiento",
    "legal": {
      "agreement": "Consiento compartir estos datos para el propósito y duración indicados.",
      "gdprNotice": "Tienes derecho a retirar el consentimiento en cualquier momento."
    }
  }
}
```

## Component Usage

### Server Components

```tsx
import { useTranslations } from 'next-intl';

export default function VaultPage() {
  const t = useTranslations('vault');

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
      <button>{t('create')}</button>
    </div>
  );
}
```

### Client Components

```tsx
'use client';

import { useTranslations } from 'next-intl';

export function VaultCreateDialog() {
  const t = useTranslations('vault');

  return (
    <Dialog>
      <DialogTitle>{t('create')}</DialogTitle>
      <DialogDescription>{t('description')}</DialogDescription>
      {/* form */}
    </Dialog>
  );
}
```

### Date Formatting

```tsx
import { useFormatter } from 'next-intl';

function VaultCard({ entry }) {
  const format = useFormatter();

  return (
    <p>{format.dateTime(entry.createdAt, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })}</p>
  );
}
```

### Number Formatting

```tsx
const format = useFormatter();

<p>{format.number(1234.56, { style: 'currency', currency: 'EUR' })}</p>
// Output (es): 1.234,56 €
// Output (en): €1,234.56
```

## LucidData-Specific Considerations

### Consent Form Translations

**Critical**: Consent legal language must be reviewed by legal counsel for each locale.

```json
{
  "consent": {
    "legal": {
      "agreement": "I consent to share this data...",
      "gdprNotice": "You have the right to withdraw...",
      "dataProcessing": "Your data will be processed according to...",
      "thirdParty": "Data may be shared with verified partners..."
    }
  }
}
```

**Warning**: Auto-translation (Google Translate) is NOT acceptable for legal text.

### Audit Log Messages

Keep audit log messages in English (for compliance), but display translated descriptions to users:

```typescript
// Store in database (English)
await createAuditLog({
  eventType: 'DATA_CREATED',
  message: 'Vault entry created'
});

// Display to user (localized)
const t = useTranslations('audit.events');
<p>{t('DATA_CREATED')}</p>
```

### Date/Time Formatting

Use user's locale for display:

```tsx
const format = useFormatter();

// Relative time
format.relativeTime(entry.createdAt) // "3 days ago" / "hace 3 días"

// Absolute time
format.dateTime(entry.createdAt, {
  dateStyle: 'medium',
  timeStyle: 'short'
}) // "Jan 13, 2026, 3:45 PM" / "13 ene 2026, 15:45"
```

## Testing i18n

### Manual Testing

```bash
# Start dev server
npm run dev

# Test locales
open http://localhost:3000/en
open http://localhost:3000/es
open http://localhost:3000/fr
```

### Unit Tests (Mock useTranslations)

```typescript
import { vi } from 'vitest';

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}));

it('renders translated text', () => {
  render(<VaultPage />);
  expect(screen.getByText('vault.title')).toBeInTheDocument();
});
```

### E2E Tests (Test Each Locale)

```typescript
test.describe('Vault (Spanish)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/es/dashboard/vault');
  });

  test('should display Spanish text', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Bóveda de Datos' })).toBeVisible();
  });
});
```

## Migration Strategy

1. **Phase 1**: Setup infrastructure (don't change existing routes)
2. **Phase 2**: Create English translations (extract from components)
3. **Phase 3**: Update routes to use `[locale]` segment
4. **Phase 4**: Add secondary languages (Spanish, French)
5. **Phase 5**: Professional translation review (legal content)
6. **Phase 6**: Launch with locale switcher in UI

## References

For more detailed information, see:

- [next-intl Setup](references/next-intl-setup.md) - Installation and configuration
- [Locale Structure](references/locale-structure.md) - Translation file organization

## Translation Template

See [translation-template.json](assets/translation-template.json) for complete structure.

## Quick Reference

| Task | Code | Notes |
|------|------|-------|
| Server translation | `const t = useTranslations('namespace')` | In Server Components |
| Client translation | Same as above | Add `'use client'` |
| Format date | `format.dateTime(date, options)` | Locale-aware |
| Format number | `format.number(num, options)` | Currency, decimals |
| Pluralization | `t('items', { count: n })` | Use ICU syntax |
| Namespace access | `t('vault.title')` | Dot notation |

---

**Version**: 1.0
**Last Updated**: 2026-01-13
**Maintained by**: LucidData Team
