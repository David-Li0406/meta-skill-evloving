# Installation

Install the three core Evolu packages for React web applications:

```bash
npm install @evolu/common @evolu/react @evolu/react-web
```

## TypeScript Configuration

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "exactOptionalPropertyTypes": true
  }
}
```

Both settings are **required** for Evolu's branded types to work correctly.

## Platform Variants

| Platform | Packages |
|----------|----------|
| React web | `@evolu/react` + `@evolu/react-web` |
| React Native | `@evolu/react` + `@evolu/react-native` |
| Expo | `@evolu/react` + `@evolu/expo` |
| Svelte | `@evolu/svelte` + `@evolu/svelte-web` |

## Prerequisites Checklist

- [ ] TypeScript 5.7 or later
- [ ] `strict: true` in tsconfig.json
- [ ] `exactOptionalPropertyTypes: true` in tsconfig.json
- [ ] Next.js 13+ with App Router
