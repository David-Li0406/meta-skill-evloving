---
name: nuxt-better-auth
description: Use this skill when implementing authentication in Nuxt apps with @onmax/nuxt-better-auth, which provides user session management, server auth helpers, route protection, and integration with Better Auth plugins.
---

# Nuxt Better Auth

Authentication module for Nuxt 4+ built on [Better Auth](https://www.better-auth.com/). This module provides composables, server utilities, and route protection.

> **Alpha Status**: This module is currently in alpha (v0.0.2-alpha.14) and not recommended for production use. APIs may change.

## When to Use

- Installing/configuring `@onmax/nuxt-better-auth`
- Implementing login, signup, and signout flows
- Protecting routes on both client and server
- Accessing user session in API routes
- Integrating Better Auth plugins (admin, passkey, 2FA)
- Setting up a database with NuxtHub
- Using client-only mode for external authentication backends

**For Nuxt patterns:** use `nuxt` skill  
**For NuxtHub database:** use `nuxthub` skill

## Available Guidance

| File                                                                 | Topics                                                                 |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **[references/installation.md](references/installation.md)**         | Module setup, environment variables, configuration files               |
| **[references/client-auth.md](references/client-auth.md)**           | useUserSession, signIn/signUp/signOut, BetterAuthState, safe redirects |
| **[references/server-auth.md](references/server-auth.md)**           | serverAuth, getUserSession, requireUserSession                         |
| **[references/route-protection.md](references/route-protection.md)** | routeRules, definePageMeta, middleware                                 |
| **[references/plugins.md](references/plugins.md)**                   | Better Auth plugins (admin, passkey, 2FA)                              |
| **[references/database.md](references/database.md)**                 | NuxtHub integration, Drizzle schema, custom tables with foreign keys   |
| **[references/client-only.md](references/client-only.md)**           | External auth backend, client-only mode, CORS                          |
| **[references/types.md](references/types.md)**                       | AuthUser, AuthSession, type augmentation                               |

## Usage Pattern

**Load based on context:**

- Install and configure the module according to the provided guidance.