# Tool Support

## Runtimes

| Runtime | Version  | Year | Default Conditions                           | Custom Conditions | Docs                                                               |
| ------- | -------- | ---- | -------------------------------------------- | ----------------- | ------------------------------------------------------------------ |
| Node.js | v14.6.0+ | 2020 | `node`, `import`/`require`, `default`        | `--conditions=X`  | [nodejs.org](https://nodejs.org/api/packages.html#subpath-imports) |
| Deno    | v1.25+   | 2022 | `deno`, `node`, `import`, `default`          | `--conditions=X`  | [docs.deno.com](https://docs.deno.com/runtime/fundamentals/node/)  |
| Bun     | v1.0+    | 2023 | `bun`, `node`, `import`/`require`, `default` | `--conditions=X`  | [bun.sh](https://bun.sh/docs/runtime/modules)                      |

## Type Checkers

| Tool       | Version | Custom Conditions  | Docs                                                                                |
| ---------- | ------- | ------------------ | ----------------------------------------------------------------------------------- |
| TypeScript | v5.0+   | `customConditions` | [typescriptlang.org](https://www.typescriptlang.org/tsconfig/customConditions.html) |
| tsgo       | preview | `customConditions` | [github](https://github.com/microsoft/typescript-go)                                |

### TypeScript Support Timeline

| Version | Year | What Changed                                                                                                     |
| ------- | ---- | ---------------------------------------------------------------------------------------------------------------- |
| 4.5     | 2021 | Basic `imports` field resolution (compiles correctly)                                                            |
| 5.0     | 2023 | `resolvePackageJsonImports` option formalized                                                                    |
| 5.4     | 2024 | Language Server catches up (hover, go-to-definition)                                                             |
| 5.7     | 2024 | Path completions + auto-import for `#` imports ([PR #57718](https://github.com/microsoft/TypeScript/pull/57718)) |

### TypeScript Config

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "customConditions": ["my-dev"]
  }
}
```

| Option                      | Default                             | Required `moduleResolution` |
| --------------------------- | ----------------------------------- | --------------------------- |
| `resolvePackageJsonImports` | `true` with node16/nodenext/bundler | node16, nodenext, bundler   |
| `customConditions`          | `[]`                                | node16, nodenext, bundler   |

### moduleResolution Behavior

| Behavior                             | `nodenext`         | `bundler` |
| ------------------------------------ | ------------------ | --------- |
| Extensionless relative imports       | Forbidden (TS2835) | Allowed   |
| Extensionless in patterns (`#foo/*`) | Forbidden          | Forbidden |
| File extensions required             | Yes (`.js` in ESM) | No        |

Both modes follow Node.js spec for pattern targets - no extension guessing.

### Dev/Prod Pattern

```json
// package.json
{
  "imports": {
    "#lib/*": {
      "my-dev": "./src/lib/*.ts",
      "default": "./dist/lib/*.js"
    }
  }
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "nodenext",
    "customConditions": ["my-dev"]
  }
}
```

Use unique condition names (not generic `dev`) to prevent deps from matching.

### Known Issues

| Issue                                                          | Status       | Impact                                                                    | Workaround                                                      |
| -------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [#59620](https://github.com/microsoft/TypeScript/issues/59620) | Open         | Auto-import suggests `./relative` instead of `#alias` within same package | Set `importModuleSpecifierPreference: "non-relative"` (partial) |
| [#55337](https://github.com/microsoft/TypeScript/issues/55337) | Closed (WAI) | Extensionless patterns `#foo/*` don't resolve `#foo/Bar`                  | Include extension or use array target                           |
| [#52460](https://github.com/microsoft/TypeScript/issues/52460) | Fixed (5.7)  | Path completions for `#` imports in IDE                                   | Upgrade to TS 5.7+                                              |

### tsgo-Specific Issues

| Issue                                                           | Status | Impact                                |
| --------------------------------------------------------------- | ------ | ------------------------------------- |
| [#1725](https://github.com/microsoft/typescript-go/issues/1725) | Open   | Condition resolution differs from tsc |
| [#916](https://github.com/microsoft/typescript-go/issues/916)   | Open   | May pick wrong export (CJS vs ESM)    |

### tsconfig paths Duplication

**Not needed** on TS 5.7+ if using `node16`, `nodenext`, or `bundler` moduleResolution. TypeScript resolves `imports` field natively including IDE auto-import.

Exception: [#59620](https://github.com/microsoft/TypeScript/issues/59620) - if you need auto-import to suggest `#alias` instead of `./relative` for intra-package imports, `paths` duplication is a workaround until fixed.

## Bundlers

| Bundler  | Config                  | Version                     | Year | Conditions Config         | Docs                                                                                  |
| -------- | ----------------------- | --------------------------- | ---- | ------------------------- | ------------------------------------------------------------------------------------- |
| esbuild  | Native                  | v0.13.9+                    | 2021 | `--conditions=X`          | [esbuild.github.io](https://esbuild.github.io/api/#conditions)                        |
| Webpack  | `resolve.importsFields` | v5+                         | 2020 | `resolve.conditionNames`  | [webpack.js.org](https://webpack.js.org/configuration/resolve/#resolveconditionnames) |
| Rspack   | `resolve.importsFields` | All                         | 2023 | `resolve.conditionNames`  | [rspack.rs](https://rspack.rs/config/resolve#resolveimportsfields)                    |
| Rollup   | Via plugin              | @rollup/plugin-node-resolve | 2021 | `exportConditions` option | [npm](https://www.npmjs.com/package/@rollup/plugin-node-resolve)                      |
| Rolldown | Via oxc-resolver        | All                         | 2024 | `resolve.conditionNames`  | [rolldown.rs](https://rolldown.rs/options/resolve)                                    |
| Metro    | Native                  | v0.82+ (RN 0.79+)           | 2025 | `unstable_conditionNames` | [metrobundler.dev](https://metrobundler.dev/docs/package-exports/)                    |

## Meta-Bundlers

Inherit support from underlying bundler:

| Tool    | Underlying        | Version | Year | Conditions Config    | Docs                                                                                  |
| ------- | ----------------- | ------- | ---- | -------------------- | ------------------------------------------------------------------------------------- |
| Vite    | Rollup/Rolldown   | v4.2.0+ | 2023 | `resolve.conditions` | [vite.dev](https://vite.dev/config/shared-options#resolve-conditions)                 |
| Next.js | Webpack/Turbopack | All     | -    | Via webpack config   | [nextjs.org](https://nextjs.org/docs/app/api-reference/config/next-config-js/webpack) |
| Astro   | Vite              | All     | -    | Via vite config      | [docs.astro.build](https://docs.astro.build/en/guides/integrations-guide/)            |
| Expo    | Metro             | SDK 53+ | 2025 | Via metro.config.js  | [docs.expo.dev](https://docs.expo.dev/versions/latest/config/metro/)                  |

## Quick Reference: Setting Custom Conditions

### CLI

```bash
# Node.js
node --conditions=development app.js

# Deno
deno run --conditions=development main.ts

# Bun
bun --conditions=development app.js

# esbuild
esbuild --conditions=development app.js
```

### Config Files

```javascript
// webpack.config.js / rspack.config.js
module.exports = {
  resolve: {
    conditionNames: ['import', 'module', 'browser', 'development', 'default'],
  },
};

// vite.config.js
export default {
  resolve: {
    conditions: ['development', 'module', 'browser'],
  },
};

// rollup.config.js (with plugin)
import resolve from '@rollup/plugin-node-resolve';
export default {
  plugins: [resolve({ exportConditions: ['development'] })],
};

// rolldown.config.js
export default {
  resolve: {
    conditionNames: ['development', 'import', 'default'],
  },
};

// metro.config.js
module.exports = {
  resolver: {
    unstable_conditionNames: ['require', 'react-native', 'development'],
  },
};
```

For comprehensive conditions documentation by tool, see [cross-platform.md](cross-platform.md).
