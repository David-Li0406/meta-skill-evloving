---
name: biome-to-oxc
description: Migrate JavaScript/TypeScript projects from Biome to oxlint + oxfmt with Prettier fallback. Use when user asks to "migrate to oxlint", "switch from biome to oxc", "use oxfmt", or wants to adopt the oxc toolchain for linting and formatting.
---

# Biome to Oxc Migration

Migrate from Biome to oxlint (linting) + oxfmt (formatting) with Prettier for unsupported file types.

## File Type Strategy

| File Type | Lint | Format |
|-----------|------|--------|
| `.ts`, `.tsx`, `.js`, `.jsx` | oxlint | oxfmt |
| `.json`, `.jsonc`, `.css` | - | oxfmt |
| `.md`, `.mdx`, `.astro`, `.yaml`, `.yml` | - | Prettier |

## Migration Checklist

1. **Remove Biome packages** - `@biomejs/biome`, `ultracite`, or similar presets
2. **Add new packages** - `oxlint`, `oxfmt`, `prettier`, framework-specific prettier plugins if needed
3. **Delete** `biome.json` or `biome.jsonc`
4. **Create `.oxlintrc.json`**
5. **Create `.prettierrc.json`** and **`.prettierignore`**
6. **Update build scripts** - Replace biome commands with oxlint/oxfmt/prettier
7. **Update VSCode settings** - Switch formatter to `oxc.oxc-vscode`
8. **Run format and lint** - Verify everything works

## Configuration Templates

### .oxlintrc.json

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["typescript", "import", "unicorn", "oxc", "jsdoc", "promise", "node"],
  "rules": {}
}
```

Available plugins: `eslint`, `react`, `unicorn`, `typescript`, `oxc`, `import`, `jsdoc`, `jest`, `vitest`, `jsx-a11y`, `nextjs`, `react-perf`, `promise`, `node`, `vue`

Enable plugins relevant to your project. For library projects, exclude framework-specific plugins (react, vue, nextjs, jest, vitest).

### .prettierrc.json

```json
{
  "printWidth": 120,
  "plugins": ["prettier-plugin-astro"]
}
```

Add plugins as needed: `prettier-plugin-astro`, `prettier-plugin-svelte`, `prettier-plugin-tailwindcss`

### .prettierignore

```
dist/
node_modules/
**/*.ts
**/*.tsx
**/*.js
**/*.jsx
**/*.json
**/*.css
```

Exclude files handled by oxfmt.

## VSCode Settings

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript][typescript][javascriptreact][typescriptreact][json][jsonc][css]": {
    "editor.defaultFormatter": "oxc.oxc-vscode"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.oxc": "always"
  }
}
```

## Rule Migration

Common Biome to oxlint rule mappings:

| Biome Rule | oxlint Equivalent |
|------------|-------------------|
| `noBarrelFile` | `no-barrel-file` |
| `useConsistentTypeDefinitions` | Not directly available |
| `noUnusedVariables` | `no-unused-vars` |
| `noConsole` | `no-console` |

oxlint uses ESLint-compatible rule names with kebab-case.

## CLI Commands

```bash
# Lint with auto-fix
oxlint --fix

# Format with oxfmt (use .gitignore for ignoring)
oxfmt --write --ignore-path=.gitignore .

# Format remaining files with Prettier
prettier --write --no-error-on-unmatched-pattern "**/*.{md,mdx,astro,yaml,yml}"
```

Note: oxfmt reads `.prettierignore` by default. Use `--ignore-path=.gitignore` to use gitignore instead.
