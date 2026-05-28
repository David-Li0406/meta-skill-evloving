# ESLint Configuration (Legacy)

this project currently uses ESLint for static analysis in its microservices, progressively migrating toward Biome.

## Reglas Principales

- `@typescript-eslint/no-unused-vars`: `warn`
- `prettier/prettier`: `error`
- `import/no-unresolved`: `error`

## Configuration Files

Each module has its own `.eslintrc.js` extending the base configuration.
