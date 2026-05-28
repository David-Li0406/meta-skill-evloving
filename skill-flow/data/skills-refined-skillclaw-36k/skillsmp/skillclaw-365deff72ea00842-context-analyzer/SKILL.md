---
name: context-analyzer
description: Use this skill when you need to analyze the project context, Nuxt structure, and dependencies for planning and debugging.
---

# Skill body

## Capabilities

- **Project Structure Analysis**: Understand Nuxt 3/4 directory conventions (`server/api`, `components`, `pages`, `layouts`, `server/entities`, `server/utils`, `server/database`).
- **Symbol Resolution**: Locate definitions of components, auto-imported composables, and TypeORM entities.
- **Dependency Check**: Read `package.json` to verify installed packages and their versions.

## Instructions

1. **Read Structure**: Use a directory listing tool to understand the layout, ignoring `node_modules` and `.output`.
2. **Identify Backend Directories**: Recognize `server/` as containing backend logic, including API (`server/api`), entities (`server/entities`), utility libraries (`server/utils`), and database configurations (`server/database`).
3. **Identify Frontend Directories**: Recognize `pages`, `components`, `composables`, and `layouts` as frontend components.
4. **Trace Logic**: Search broadly for symbol definitions to understand how data flows between backend entities and frontend components.
5. **Dependency Review**: Check `package.json` before suggesting imports to understand available libraries (e.g., `dayjs`, `lodash-es`, `fs-extra`).

## Usage Example

Input: "Analyze the current user authentication flow."
Action: Read `server/api/auth/*`, `lib/auth.ts`, `middleware/auth.global.ts`, and `pages/login.vue` to map the flow.