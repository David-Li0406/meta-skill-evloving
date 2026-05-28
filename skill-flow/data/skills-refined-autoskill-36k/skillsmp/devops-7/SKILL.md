---
name: devops
description: Manages CI/CD pipelines, linting with ESLint/SonarJS, and release tagging for production deployments
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## What I do

I manage the development operations including CI/CD pipelines, linting, and release processes. I ensure code quality through automated checks and maintain deployment workflows.

## When to use me

Use this when:

- You need to build or deploy the application
- You're investigating build failures or lint errors
- You need to create a release or tag

## Key Concepts

- **Vite**: Build tool for production bundles
- **ESLint**: JavaScript/TypeScript linting
- **SonarJS**: Static analysis for code quality
- **Release Tagging**: Version management for deployments

## Commands

```bash
npm run dev              # Start dev server (localhost:5173)
npm run build            # Production bundle
npm run preview          # Preview production build
npm run lint             # Run ESLint on all files
```

## Source Files

- `package.json`: Build and lint scripts
- `vite.config.ts`: Vite configuration
- `eslint.config.js`: ESLint configuration
- `.github/`: CI/CD workflows

## Code Patterns

- Manual chunks for production builds
- ESLint with SonarJS rules enabled
- Environment-specific configurations

## Operational Constraints

- Build must pass before deployment
- Lint errors are blocking (must fix, not bypass)
- Semantic versioning for release tags
