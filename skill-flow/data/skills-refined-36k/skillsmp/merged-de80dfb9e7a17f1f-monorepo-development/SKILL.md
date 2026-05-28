---
name: monorepo-development
description: Use this skill for best practices in monorepo development with TypeScript, React, Next.js, Expo, and related technologies.
---

# Monorepo Development

You are an expert in TypeScript, React, Next.js, Expo (React Native), Tamagui, Supabase, Zod, Turbo (Monorepo Management), i18next, Zustand, TanStack React Query, Solito, and Stripe.

## Code Style and Structure

- Write concise, technical TypeScript code using functional and declarative programming patterns; avoid classes.
- Use descriptive variable names with auxiliary verbs (e.g., `isLoading`, `hasError`).
- Structure files with exported components, helpers, and types, favoring named exports.
- Use lowercase with dashes for directory names (e.g., `components/auth-wizard`).

## TypeScript and Validation

- Use TypeScript for all code; prefer interfaces over types for object shapes.
- Utilize Zod for schema validation and type inference; avoid enums in favor of literal types or maps.
- Implement proper error handling with discriminated unions and custom error types.

## State and Data Management

- Use Zustand for state management and TanStack React Query for data fetching and caching.
- Minimize `useEffect` and `setState`; favor derived state and implement optimistic updates for better UX.

## Monorepo Structure

- Follow best practices using Turbo for monorepo management, with separate `apps` and `packages` directories.
- Keep shared configurations in the root `configs/` directory and use consistent naming conventions for workspaces.

## Internationalization

- Use i18next for web internationalization and expo-localization for React Native.
- Organize translation files by feature or domain and internationalize all user-facing text.

## Error Handling and Validation

- Prioritize error handling and edge cases; handle errors early with guard clauses and use early returns to avoid deeply nested if statements.
- Implement proper error logging and user-friendly error messages.

## Performance Optimization

- Use dynamic imports for code splitting and implement lazy loading for non-critical components.
- Optimize images: use WebP format, include size data, and implement lazy loading.

## Cross-Platform Development

- Use Solito for navigation across web and mobile, creating `.native.tsx` files for platform-specific code.
- Share business logic and UI components through packages, and use SolitoImage for cross-platform image compatibility.

## Backend Integration

- Use Supabase for authentication and database, implementing Row Level Security (RLS) policies and Zod schemas for API validation.
- Handle webhook events properly and implement Stripe integration with proper webhook handlers, including subscription syncing between Stripe and your database.