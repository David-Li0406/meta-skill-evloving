# Nuxt I18n Reference

**Last Updated:** 2025-11 (v10.2.0)

**Check:** `@nuxtjs/i18n` in package.json

Nuxt I18n v10 provides internationalization (i18n) for Nuxt applications with auto-imports, locale routing, SEO support, and integration with Vue I18n v11.

## Installation & Setup

```bash
pnpm add @nuxtjs/i18n
```

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  modules: ["@nuxtjs/i18n"],

  i18n: {
    locales: [
      { code: "en", iso: "en-US", name: "English", file: "en.json" },
      { code: "fr", iso: "fr-FR", name: "Français", file: "fr.json" },
      { code: "es", iso: "es-ES", name: "Español", file: "es.json" },
    ],
    defaultLocale: "en",
    langDir: "locales/",
    strategy: "prefix_except_default", // or 'prefix', 'no_prefix'
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      redirectOn: "root",
    },
  },
})
```

## Directory Structure

```
locales/
├── en.json
├── fr.json
└── es.json
```

**Example locale file (en.json):**

```json
{
  "welcome": "Welcome",
  "hello": "Hello {name}",
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "products": {
    "title": "Our Products",
    "description": "Browse our collection"
  }
}
```

## Basic Usage

### Translation in Templates

```vue
<template>
  <div>
    <!-- Simple translation -->
    <h1>{{ $t("welcome") }}</h1>

    <!-- With parameters -->
    <p>{{ $t("hello", { name: "John" }) }}</p>

    <!-- Nested keys -->
    <nav>
      <NuxtLink to="/">{{ $t("nav.home") }}</NuxtLink>
      <NuxtLink to="/about">{{ $t("nav.about") }}</NuxtLink>
    </nav>

    <!-- Pluralization -->
    <p>{{ $t("items", { count: 5 }) }}</p>

    <!-- Number formatting -->
    <p>{{ $n(1000, "currency") }}</p>

    <!-- Date formatting -->
    <p>{{ $d(new Date(), "long") }}</p>
  </div>
</template>
```

### Translation in Script

```vue
<script setup lang="ts">
const { t, locale, locales, setLocale } = useI18n()

// Get translation
const welcomeMessage = t("welcome")

// With parameters
const greeting = t("hello", { name: "John" })

// Current locale
console.log(locale.value) // 'en'

// Available locales
console.log(locales.value) // [{ code: 'en', ... }, ...]

// Change locale
async function switchLanguage(code: string) {
  await setLocale(code)
}
</script>
```

## Routing

### Route Strategies

**prefix_except_default** (recommended):

- Default locale: `/about`
- Other locales: `/fr/about`, `/es/about`

**prefix**:

- All locales: `/en/about`, `/fr/about`, `/es/about`

**no_prefix**:

- All locales use same path: `/about`
- Locale detected from cookie/browser

### Locale Links

```vue
<script setup lang="ts">
const localePath = useLocalePath()
const switchLocalePath = useSwitchLocalePath()
</script>

<template>
  <div>
    <!-- Link with current locale -->
    <NuxtLink :to="localePath('/')">
      {{ $t("nav.home") }}
    </NuxtLink>

    <NuxtLink :to="localePath('/about')">
      {{ $t("nav.about") }}
    </NuxtLink>

    <!-- Switch locale links -->
    <NuxtLink :to="switchLocalePath('fr')"> Français </NuxtLink>

    <NuxtLink :to="switchLocalePath('es')"> Español </NuxtLink>

    <!-- With named routes -->
    <NuxtLink :to="localePath({ name: 'products-id', params: { id: '123' } })">
      Product
    </NuxtLink>
  </div>
</template>
```

### Programmatic Navigation

```vue
<script setup lang="ts">
const localePath = useLocalePath()
const router = useRouter()

async function goToAbout() {
  await router.push(localePath("/about"))
}

async function goToProduct(id: string) {
  await navigateTo(localePath({ name: "products-id", params: { id } }))
}
</script>
```

## Composables

### useI18n

Main composable for translations:

```vue
<script setup lang="ts">
const {
  t, // Translation function
  locale, // Current locale ref
  locales, // Available locales
  setLocale, // Change locale function
  n, // Number formatting
  d, // Date formatting
  tm, // Translation messages
  te, // Translation exists check
  getLocaleCookie, // Get locale cookie
} = useI18n()

// Check if translation exists
if (te("optional.message")) {
  console.log(t("optional.message"))
}

// Get all translations for a key
const navTranslations = tm("nav")
console.log(navTranslations) // { home: 'Home', about: 'About', ... }
</script>
```

### useLocalePath

Generate localized paths:

```vue
<script setup lang="ts">
const localePath = useLocalePath()

// Simple path
const homePath = localePath("/")

// With route object
const productPath = localePath({
  name: "products-id",
  params: { id: "123" },
  query: { tab: "reviews" },
})

// With specific locale
const frenchPath = localePath("/about", "fr")
</script>
```

### useSwitchLocalePath

Generate paths for locale switching:

```vue
<script setup lang="ts">
const switchLocalePath = useSwitchLocalePath()
const route = useRoute()

// Get path for switching to French on current page
const frenchPath = switchLocalePath("fr")

// Custom route
const customPath = switchLocalePath("es", "/about")
</script>
```

### useRouteBaseName

Get route name without locale prefix:

```vue
<script setup lang="ts">
const getRouteBaseName = useRouteBaseName()
const route = useRoute()

// Current route: /fr/products/123
const baseName = getRouteBaseName(route) // 'products-id'
</script>
```

### useBrowserLocale

Detect browser locale:

```vue
<script setup lang="ts">
const browserLocale = useBrowserLocale()
console.log(browserLocale) // 'en-US'
</script>
```

### useLocaleRoute

Get localized route object (includes locale prefix):

```vue
<script setup lang="ts">
const localeRoute = useLocaleRoute()

// Get route object for about page in current locale
const aboutRoute = localeRoute({ name: "about" })

// Navigate with full route object
navigateTo(aboutRoute)
</script>
```

### useLocaleHead

SEO meta for current locale:

```vue
<script setup lang="ts">
const i18nHead = useLocaleHead({ addSeoAttributes: true })

useHead({
  htmlAttrs: { lang: i18nHead.value.htmlAttrs?.lang },
  link: i18nHead.value.link,
  meta: i18nHead.value.meta,
})
</script>
```

### useSetI18nParams

Set route params per locale for SEO:

```vue
<script setup lang="ts">
const setI18nParams = useSetI18nParams()

// Set different slugs for different locales
setI18nParams({
  en: { slug: "about-us" },
  fr: { slug: "a-propos" },
})
</script>
```

### useCookieLocale

Access locale cookie directly:

```vue
<script setup lang="ts">
const cookieLocale = useCookieLocale()
console.log(cookieLocale.value) // 'en' or null
</script>
```

## Components

### NuxtLinkLocale

Localized link component (auto-prefixes current locale):

```vue
<template>
  <NuxtLinkLocale to="/about">About</NuxtLinkLocale>
  <!-- Renders: /fr/about when locale is 'fr' -->

  <NuxtLinkLocale to="/contact" locale="es">Contact (ES)</NuxtLinkLocale>
  <!-- Forces Spanish locale: /es/contact -->
</template>
```

### SwitchLocalePathLink

Link to current page in different locale:

```vue
<template>
  <SwitchLocalePathLink locale="fr">Français</SwitchLocalePathLink>
  <SwitchLocalePathLink locale="es">Español</SwitchLocalePathLink>
</template>
```

## Macros

### defineI18nRoute

Per-page locale configuration:

```vue
<script setup lang="ts">
defineI18nRoute({
  locales: ["en", "fr"], // Only available in these locales
  // or
  locales: false, // Disable localization for this page
})
</script>
```

## Common Patterns

### Language Switcher

```vue
<script setup lang="ts">
const { locale, locales, setLocale } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const availableLocales = computed(() =>
  locales.value.filter((l) => l.code !== locale.value),
)
</script>

<template>
  <div class="flex gap-2">
    <NuxtLink
      v-for="loc of availableLocales"
      :key="loc.code"
      :to="switchLocalePath(loc.code)"
      class="px-3 py-1 rounded hover:bg-gray-100"
    >
      {{ loc.name }}
    </NuxtLink>
  </div>
</template>
```

### Dropdown Language Switcher

```vue
<script setup lang="ts">
const { locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()

const currentLocale = computed(() =>
  locales.value.find((l) => l.code === locale.value),
)
</script>

<template>
  <UDropdown>
    <template #trigger>
      <UButton>
        {{ currentLocale?.name }}
      </UButton>
    </template>

    <div class="p-2">
      <NuxtLink
        v-for="loc of locales"
        :key="loc.code"
        :to="switchLocalePath(loc.code)"
        class="block px-4 py-2 hover:bg-gray-100"
      >
        {{ loc.name }}
      </NuxtLink>
    </div>
  </UDropdown>
</template>
```

### SEO with I18n

```vue
<script setup lang="ts">
const { locale, locales, t } = useI18n()
const route = useRoute()
const switchLocalePath = useSwitchLocalePath()

useSeoMeta({
  title: t("seo.title"),
  description: t("seo.description"),
  ogLocale: locale.value,
  ogTitle: t("seo.ogTitle"),
  ogDescription: t("seo.ogDescription"),
})

useHead({
  htmlAttrs: {
    lang: locale.value,
  },
  link: [
    // Alternate language links for SEO
    ...locales.value.map((loc) => ({
      rel: "alternate",
      hreflang: loc.iso,
      href: `https://example.com${switchLocalePath(loc.code)}`,
    })),
  ],
})
</script>
```

### Per-Page Translations

```vue
<script setup lang="ts">
const { t } = useI18n({
  useScope: "local",
})
</script>

<template>
  <div>
    <h1>{{ t("title") }}</h1>
    <p>{{ t("description") }}</p>
  </div>
</template>

<i18n lang="json">
{
  "en": {
    "title": "About Us",
    "description": "Learn more about our company"
  },
  "fr": {
    "title": "À propos",
    "description": "En savoir plus sur notre entreprise"
  }
}
</i18n>
```

### Dynamic Content Translation

```vue
<script setup lang="ts">
const { data: products } = await useFetch("/api/products")
const { locale } = useI18n()

// Assuming API returns translations
const localizedProducts = computed(() =>
  products.value?.map((product) => ({
    ...product,
    name: product.translations[locale.value]?.name || product.name,
    description:
      product.translations[locale.value]?.description || product.description,
  })),
)
</script>

<template>
  <div v-for="product of localizedProducts" :key="product.id">
    <h3>{{ product.name }}</h3>
    <p>{{ product.description }}</p>
  </div>
</template>
```

### Lazy Loading Translations

For large translation files:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  i18n: {
    lazy: true,
    langDir: "locales/",
    locales: [
      { code: "en", file: "en.json" },
      { code: "fr", file: "fr.json" },
      { code: "es", file: "es.json" },
    ],
  },
})
```

## Number & Date Formatting

### Number Formatting

Define formats in config:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  i18n: {
    numberFormats: {
      en: {
        currency: {
          style: "currency",
          currency: "USD",
        },
        decimal: {
          style: "decimal",
          minimumFractionDigits: 2,
        },
      },
      fr: {
        currency: {
          style: "currency",
          currency: "EUR",
        },
        decimal: {
          style: "decimal",
          minimumFractionDigits: 2,
        },
      },
    },
  },
})
```

Usage:

```vue
<template>
  <div>
    <!-- Currency -->
    <p>{{ $n(1234.56, "currency") }}</p>
    <!-- en: $1,234.56 -->
    <!-- fr: 1 234,56 € -->

    <!-- Decimal -->
    <p>{{ $n(123456.789, "decimal") }}</p>
    <!-- en: 123,456.79 -->
    <!-- fr: 123 456,79 -->
  </div>
</template>
```

### Date Formatting

Define formats in config:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  i18n: {
    datetimeFormats: {
      en: {
        short: {
          year: "numeric",
          month: "short",
          day: "numeric",
        },
        long: {
          year: "numeric",
          month: "long",
          day: "numeric",
          weekday: "long",
        },
      },
      fr: {
        short: {
          year: "numeric",
          month: "short",
          day: "numeric",
        },
        long: {
          year: "numeric",
          month: "long",
          day: "numeric",
          weekday: "long",
        },
      },
    },
  },
})
```

Usage:

```vue
<script setup lang="ts">
const date = new Date("2025-01-04")
</script>

<template>
  <div>
    <!-- Short format -->
    <p>{{ $d(date, "short") }}</p>
    <!-- en: Jan 4, 2025 -->
    <!-- fr: 4 janv. 2025 -->

    <!-- Long format -->
    <p>{{ $d(date, "long") }}</p>
    <!-- en: Saturday, January 4, 2025 -->
    <!-- fr: samedi 4 janvier 2025 -->
  </div>
</template>
```

## Pluralization

**Translation file:**

```json
{
  "items": "no items | one item | {count} items",
  "cart": "You have {n} item in your cart | You have {n} items in your cart"
}
```

**Usage:**

```vue
<template>
  <div>
    <p>{{ $t("items", 0) }}</p>
    <!-- "no items" -->
    <p>{{ $t("items", 1) }}</p>
    <!-- "one item" -->
    <p>{{ $t("items", 5) }}</p>
    <!-- "5 items" -->

    <p>{{ $t("cart", { n: 1 }) }}</p>
    <!-- "You have 1 item in your cart" -->
    <p>{{ $t("cart", { n: 3 }) }}</p>
    <!-- "You have 3 items in your cart" -->
  </div>
</template>
```

## TypeScript Support

### Typed Translations

```typescript
// types/i18n.ts
export interface LocaleMessages {
  welcome: string
  hello: (params: { name: string }) => string
  nav: {
    home: string
    about: string
    contact: string
  }
}
```

Usage:

```vue
<script setup lang="ts">
import type { LocaleMessages } from "~/types/i18n"

const { t } = useI18n<LocaleMessages>()

// TypeScript will check keys and parameters
const welcome = t("welcome")
const hello = t("hello", { name: "John" })
const navHome = t("nav.home")
</script>
```

## API Routes with I18n

```typescript
// server/api/products.get.ts
export default defineEventHandler(async (event) => {
  const locale = getCookie(event, "i18n_redirected") || "en"

  const products = await db.products.findMany({
    include: {
      translations: {
        where: { locale },
      },
    },
  })

  return products.map((product) => ({
    ...product,
    name: product.translations[0]?.name || product.name,
    description: product.translations[0]?.description || product.description,
  }))
})
```

## Best Practices

1. **Use prefix_except_default strategy** - Better UX for default locale users
2. **Enable browser detection** - Auto-redirect to user's preferred language
3. **Provide language switcher** - Visible on every page
4. **Use lazy loading for large apps** - Load translations on demand
5. **Organize translations by feature** - Use nested keys (`nav.home`, `products.title`)
6. **Include locale in SEO** - Use `hreflang` links and `og:locale`
7. **Handle missing translations** - Provide fallback locale
8. **Use placeholders consistently** - `{name}` for simple, `{n}` for pluralization
9. **Test all locales** - Verify layout with longer translations (German, French)
10. **Keep keys consistent** - Same structure across all locale files

## Troubleshooting

### Translations Not Loading

Check:

1. `@nuxtjs/i18n` in `modules` array
2. Locale files in correct `langDir` path
3. File names match `file` property in config
4. JSON is valid (no trailing commas)

### Routes Not Localized

1. Verify `strategy` is set correctly
2. Check `defaultLocale` matches one of your locales
3. Ensure you're using `localePath()` for links

### Browser Detection Not Working

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  i18n: {
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      redirectOn: "root",
      alwaysRedirect: true,
      fallbackLocale: "en",
    },
  },
})
```

### Missing Translations

Enable warnings in development:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  i18n: {
    compilation: {
      strictMessage: false,
    },
    vueI18n: "./i18n.config.ts",
  },
})
```

```typescript
// i18n.config.ts
export default {
  legacy: false,
  locale: "en",
  missingWarn: true,
  fallbackWarn: true,
}
```

## v10 Changes from v9

### Key Updates

1. **Vue I18n v11** - Upgraded from v10 with JIT compilation as default
2. **Improved Nuxt 4 Support** - Better compatibility with Nuxt 4
3. **Custom Routes** - Use `definePageMeta` for per-page locale configuration
4. **Server-Side Redirects** - Improved server-side redirection behavior
5. **Strict SEO** - Experimental strict SEO head management
6. **Fixed Behaviors** - `strategy` and `redirectOn` combinations now work as expected

### Migration Notes

- `$tc()` API integrated into `$t()` (from Vue I18n v10→v11 upgrade)
- JIT compilation now default (no need for `jit` option)
- New directory structure: i18n files resolved from `<rootDir>/i18n` (configurable with `restructureDir`)
- Context functions require `$` prefix: use `$localePath()` not `localePath()` in templates

## Official Resources

- **Documentation:** https://i18n.nuxtjs.org
- **Migration Guide:** https://i18n.nuxtjs.org/docs/guide/migrating
- **API Reference:** https://i18n.nuxtjs.org/api
- **Vue I18n Docs:** https://vue-i18n.intlify.dev
- **Examples:** https://i18n.nuxtjs.org/examples
- **GitHub:** https://github.com/nuxt-modules/i18n

---

**Note:** This reference covers Nuxt I18n v10 (latest as of 2025-11) with Vue I18n v11. For v9 projects, consult the migration guide.
