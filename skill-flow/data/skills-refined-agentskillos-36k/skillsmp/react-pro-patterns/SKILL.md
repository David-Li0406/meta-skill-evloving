---
name: react-pro-patterns
description: Unified guidance for React, Next.js, React Native, and Expo development.
---

# React Pro Patterns

This suite contains a collection of specialized guidelines and tools.

## ️ Included Guidelines & Tools

### ️ React Dev


> **Reference: selected_skills/Frontend/react-dev/SKILL.md**

### ️ React Best Practices


> **Reference: selected_skills/Frontend/react-best-practices/SKILL.md**

### ️ React Native Best Practices


> **Reference: selected_skills/Frontend/react-native-best-practices/SKILL.md**

### ️ React Useeffect


> **Reference: selected_skills/Frontend/react-useeffect/SKILL.md**

### ️ Building Native Ui


> **Reference: selected_skills/Frontend/building-native-ui/SKILL.md**

### ️ Native Data Fetching


> **Reference: selected_skills/Backend/native-data-fetching/SKILL.md**

### ️ Expo Api Routes

## When to Use API Routes

Use API routes when you need:

- **Server-side secrets** — API keys, database credentials, or tokens that must never reach the client
- **Database operations** — Direct database queries that shouldn't be exposed
- **Third-party API proxies** — Hide API keys when calling external services (OpenAI, Stripe, etc.)
- **Server-side validation** — Validate data before database writes
- **Webhook endpoints** — Receive callbacks from services like Stripe or GitHub
- **Rate limiting** — Control access at the server level
- **Heavy computation** — Offload processing that would be slow on mobile

## When NOT to Use API Routes

Avoid API routes when:

> **Reference: selected_skills/Backend/expo-api-routes/SKILL.md**

### ️ Expo Tailwind Setup


> **Reference: selected_skills/Frontend/expo-tailwind-setup/SKILL.md**

### ️ Expo Dev Client

Use EAS Build to create development clients for testing native code changes on physical devices. Use this for creating custom Expo Go clients for testing branches of your app.

## Important: When Development Clients Are Needed

**Only create development clients when your app requires custom native code.** Most apps work fine in Expo Go.

You need a dev client ONLY when using:
- Local Expo modules (custom native code)
- Apple targets (widgets, app clips, extensions)
- Third-party native modules not in Expo Go

**Try Expo Go first** with `npx expo start`. If everything works, you don't need a dev client.

## EAS Configuration


> **Reference: selected_skills/DevOps/expo-dev-client/SKILL.md**

### ️ Expo Deployment


> **Reference: selected_skills/DevOps/expo-deployment/SKILL.md**

### ️ Expo Cicd Workflows


> **Reference: selected_skills/DevOps/expo-cicd-workflows/SKILL.md**

### ️ Upgrading Expo

## References

- ./references/new-architecture.md -- SDK +53: New Architecture migration guide
- ./references/react-19.md -- SDK +54: React 19 changes (useContext → use, Context.Provider → Context, forwardRef removal)
- ./references/react-compiler.md -- SDK +54: React Compiler setup and migration guide

## Step-by-Step Upgrade Process

1. Upgrade Expo and dependencies

```bash
npx expo install expo@latest
npx expo install --fix
```


> **Reference: selected_skills/Frontend/upgrading-expo/SKILL.md**

### ️ Use Dom

## What are DOM Components?

DOM components allow web code to run verbatim in a webview on native platforms while rendering as-is on web. This enables using web-only libraries like `recharts`, `react-syntax-highlighter`, or any React web library in your Expo app without modification.

## When to Use DOM Components

Use DOM components when you need:

- **Web-only libraries** — Charts (recharts, chart.js), syntax highlighters, rich text editors, or any library that depends on DOM APIs
- **Migrating web code** — Bring existing React web components to native without rewriting
- **Complex HTML/CSS layouts** — When CSS features aren't available in React Native
- **iframes or embeds** — Embedding external content that requires a browser context
- **Canvas or WebGL** — Web graphics APIs not available natively

## When NOT to Use DOM Components

> **Reference: selected_skills/Frontend/use-dom/SKILL.md**
