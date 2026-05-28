---
name: shopify-app-i18n
description: Use this skill when you need to add multi-language support to your Shopify app using i18next, covering setup, localization files, and integration with the Shopify Admin context.
---

# Internationalization (i18n) for Shopify Apps

Shopify merchants exist globally. Your app MUST support multiple languages to be featured or widely adopted.

## 1. Stack
- **Library**: `i18next` (Standard)
- **React**: `react-i18next`
- **Remix**: `remix-i18next`

## 2. Setup

### Installation
```bash
npm install i18next react-i18next remix-i18next i18next-fs-backend i18next-http-backend
```

### Configuration (`app/i18n.server.ts`)
Create a server-side instance to detect language.

```typescript
import { RemixI18Next } from "remix-i18next/server";
import i18n from "~/i18n"; // client config
import { resolve } from "node:path";

export const i18nServer = new RemixI18Next({
  detection: {
    supportedLanguages: i18n.supportedLngs,
    fallbackLanguage: i18n.fallbackLng,
  },
  i18next: {
    ...i18n,
    backend: {
      loadPath: resolve("./public/locales/{{lng}}/{{ns}}.json"),
    },
  },
});
```

### Root Loader (`app/root.tsx`)
Inject the locale into the document.

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const locale = await i18nServer.getLocale(request);
  return json({ locale });
}

export const handle = {
  i18n: "common", // Reference to a translation namespace
};

export default function App() {
  const { locale } = useLoaderData<typeof loader>();
  useChangeLanguage(locale); // Syncs remix locale with i18next
  
  return (
    <html lang={locale} dir={i18n.dir(locale)}>
      {/* ... */}
    </html>
  );
}
```

## 3. Translation Files
Store JSON files in `public/locales`.

```
public/
  locales/
    en/
      common.json
    fr/
      common.json
    vi/
      common.json
```

**Example `common.json`**:
```json
{
  "welcome": "Welcome to my app",
  "dashboard": {
    "title": "Dashboard",
    "stats": "Statistics"
  }
}
```

## 4. Usage in Components

```typescript
import { useTranslation } from "react-i18next";

export function DashboardHeader() {
  const { t } = useTranslation("common");

  return (
    <Page title={t("dashboard.title")}>
      <p>{t("welcome")}</p>
    </Page>
  );
}
```

## 5. Detecting Shopify Admin Language
Shopify passes the locale in the request, which can be used to set the language dynamically.