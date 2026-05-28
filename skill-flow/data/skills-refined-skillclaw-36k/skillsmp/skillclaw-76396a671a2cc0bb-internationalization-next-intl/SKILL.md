---
name: internationalization-next-intl
description: Use this skill when working with internationalization (i18n) using next-intl and managing translations in JSON message files.
---

# Internationalization (i18n) Workflow

## Overview

This skill utilizes `next-intl` for internationalization. Translations are stored in JSON message files.

## Key Functions

- **Server Components**: Use `getTranslations` (no locale needed).
- **Client Components**: Use `useTranslations`.
- **Metadata/Server Actions**: Use `getTranslations` with locale parameter.

## Critical Rules

### 1. No Dynamic Values in Translation Keys

**IMPORTANT**: The `t` function does NOT support dynamic values as keys.

```tsx
// BAD: Dynamic key - will NOT work
const category = getCategory();
t(category); // Error!
t(MYLABELS[category]);

// GOOD: String literals only
t("Arts courses");
t("Business courses");
t("Technology courses");
```

### 2. String Interpolation IS Supported

You CAN use string interpolation for dynamic values within translations:

```tsx
// GOOD: Interpolation with static key
t("Explore all {category} courses", { category: "arts" });
t("Welcome, {name}!", { name: user.name });
t("{count} items remaining", { count: 5 });
```

### 3. Don't Pass `t` Function Around

You can't pass the `t` function to other functions or components:

```tsx
// BAD: Passing t function
function myFunction(t, label) {
  return t(label);
}
myFunction(t, "Some label");

// GOOD: Call t directly
function myFunction(translatedLabel: string) {
  return translatedLabel;
}
myFunction(t("Some label"));
```

### 4. Locale Parameter Rules

```tsx
// Server Component - no locale needed
const t = await getTranslations();
t("Hello");

// generateMetadata - needs locale
export async function generateMetadata({ params }) {
  const { locale } = await params;
  const t = await getTranslations({ locale });
  return { title: t("Page Title") };
}
```

## Workflow for Adding Translations

1. **Add translation call in code**:

   ```tsx
   const t = await getTranslations();
   return <h1>{t("New page title")}</h1>;
   ```

2. **Add the key to message files**:

   Find JSON message files in your locales directory (e.g., `messages/en.json`, `messages/es.json`) and add the new key:

   ```json
   {
     "New page title": "New page title"
   }
   ```

3. **Translate for each locale**:

   ```json
   // messages/en.json
   {
     "New page title": "New page title"
   }
   // messages/es.json
   {
     "New page title": "Nuevo título de página"
   }
   ```