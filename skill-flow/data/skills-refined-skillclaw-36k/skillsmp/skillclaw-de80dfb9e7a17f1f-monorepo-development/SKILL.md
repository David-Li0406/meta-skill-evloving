---
name: monorepo-development
description: Use this skill when you want to implement best practices for monorepo development with TypeScript, React, Next.js, Expo, and related technologies.
---

# Monorepo Development

You are an expert in TypeScript, React, Next.js, Expo, Tamagui, Supabase, Zod, Turbo, i18next, Zustand, TanStack React Query, Solito, and Stripe.

## Code Style and Structure

- Write concise, technical TypeScript code using functional and declarative programming patterns; avoid classes.
- Use descriptive variable names with auxiliary verbs (e.g., `isLoading`, `hasError`).
- Structure files with exported components, helpers, and types using named exports.
- Favor lowercase with dashes for directory names (e.g., `components/auth-wizard`).

## TypeScript and Validation

- Use TypeScript for all code; prefer interfaces over types for object shapes.
- Utilize Zod for schema validation and type inference.
- Avoid enums; use literal types or maps instead.
- Implement proper error handling with discriminated unions.

## State and Data Management

- Use Zustand for state management.
- Use TanStack React Query for data fetching and caching.
- Minimize `useEffect` and `setState`; favor derived state.
- Implement optimistic updates for better UX.

## Monorepo Structure

- Follow best practices using Turbo for monorepo management.
- Use separate `apps` and `packages` directories.
- Keep shared configurations in the root `configs/` directory.
- Follow the standard Turborepo workspaces directory structure:
  - `apps/` for application workspaces (Next.js, Expo apps).
  - `packages/` for shared package workspaces (UI, utils, configs).

## Internationalization

- Use i18next for web internationalization and expo-localization for React Native.
- Keep translation files organized by feature or domain.

## Error Handling

- Prioritize error handling and edge cases.
- Handle errors early with guard clauses and implement custom error types for consistency.
- Use early returns for error conditions to avoid deeply nested if statements.

## Performance Optimization

- Optimize both web and native platforms.
- Use dynamic imports in Next.js and implement lazy loading.
- Optimize images with proper formats.

## Cross-Platform Development

- Use Solito for navigation and create `.native.tsx` files for platform-specific code.
- Use SolitoImage for cross-platform image compatibility.

## Stripe Integration

- Implement payment processing and subscriptions using Stripe.
- Handle webhooks for subscription events and sync subscription status with Supabase.