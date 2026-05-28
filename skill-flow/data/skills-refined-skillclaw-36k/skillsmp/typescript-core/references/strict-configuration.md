# Strict Configuration

We enforce strict TypeScript and project configuration to catch errors early and maintain code quality. This document outlines the required compiler, linter, and tool settings for all projects.

## TypeScript Compiler Settings (tsconfig.json)

All projects must enable `strict` mode and related strictness flags in TypeScript. Key settings in `tsconfig.json`:

- **`"strict": true`**: Master switch that enables all strict type-checking options (below flags). This must always be `true`[12].
- **`"noImplicitAny": true`**: Disallow variables with an `any` type unless explicitly declared. Every value should have an explicit or inferred type.
- **`"noImplicitReturns": true`**: Require every code path in a function to return a value or explicitly not return, preventing `undefined` returns.
- **`"noUncheckedIndexedAccess": true`**: (Not part of `strict` by default) Treat array/object element access as potentially `undefined` unless you have a check. This helps avoid runtime `undefined` when indexing arrays.
- **`"strictNullChecks": true`**: (Included in `strict`) You must handle `null` and `undefined` explicitly. This is crucial – it forces us to use `Maybe`/`Option` types or explicit checks for missing values.
- **`"strictPropertyInitialization": true`**: Class members must be initialized in constructor or marked optional/undefined. Prevents uninitialized class properties.
- **`"useUnknownInCatchVariables": true`**: (Since TS 4.4, part of `strict`) `catch(e)` will have `e: unknown` instead of `any`, encouraging proper error typing or narrowing.
- **`"exactOptionalPropertyTypes": true`**: (TS 4.4+) When enabled, `interface X { foo?: string }` means if `foo` is set it must be `string`, but it could be omitted. This prevents mistakenly assigning `undefined` when not allowed.
- **`"forceConsistentCasingInFileNames": true`**: Ensures imports must match file name casing exactly. This prevents case-sensitivity issues between dev (Windows/mac) and CI (Linux).
- **`"skipLibCheck": false`**: We prefer to set this to `false` if possible, so that even types in `node_modules` are checked. However, if build time is an issue or some libs have bad types, we might set to `true`. Default: `true` for performance, but if a bug occurs from lib types, consider enabling to catch it.
- **`"moduleResolution": "node16"`** (or `"bundler"` for newer TS) – Use Node’s modern resolution rules.
- **`"resolveJsonModule": true`**: Allow importing JSON (often useful for config).
- **`"isolatedModules": true`**: Especially if using Babel/TS in transpile mode (ensures each file can be transpiled in isolation).
- **`"esModuleInterop": true`**: Simplify default imports from CommonJS (allow `import express from 'express'`).
- **`Target` and `lib`**: Use latest stable target we can. E.g., `"target": "ES2022"` and include `libs` like `DOM` if browser code. We aim to always use modern syntax and let build tools handle compatibility.

Keep `tsconfig` updated: When new strict flags or TS features appear (e.g., `noImplicitOverride`, `noPropertyAccessFromIndexSignature` etc.), evaluate and enable them if they catch potential issues. We always upgrade to the latest TS version soon after release (check official TS blog for new flags each version).

## ESLint Configuration

We extend a strict ESLint config (likely `eslint:recommended` and `plugin:@typescript-eslint/recommended`). Key rules we enforce:

- `noUnusedLocals` / `noUnusedVars`: Enabled via TS compiler or ESLint to prevent dead code.
- `noImplicitAny` is already in TS, but ESLint also has `@typescript-eslint/no-explicit-any` to flag any explicit `: any` usage.
- `@typescript-eslint/strict-boolean-expressions`: Ensure you explicitly compare booleans or handle all cases (no truthiness misuse). This avoids accidentally treating `0` or `""` as `false` without intent.
- `eqeqeq: "error"` – Require strict equality `===` (no loose `==`).
- `no-floating-promises` (via `typescript-eslint`): Any `Promise` not `await`ed or handled is an error. This prevents lost async errors – use `void myAsync()` only if intentionally ignoring.
- `import/order` and `import/no-cycle`: We configure import order and forbid circular dependencies. This keeps the project maintainable (circular deps can cause runtime issues).
- `max-len` (perhaps 100 or 120): To keep code readable on GitHub, etc. (We might use Prettier primarily, which wraps lines).
- `no-console`: We disallow direct `console.log` in code; use our logging framework instead. In rare cases (like a small CLI tool script), `console` might be okay, but generally log through LogTape.
- `security/detect-non-literal-fs-filename`, etc.: If using a security plugin, make sure we’re not using dynamic `eval` or insecure APIs.

Our ESLint config is in the repo (e.g., `.eslintrc.cjs`). All team members’ IDEs should integrate it, and CI runs ESLint. No code with ESLint errors should be committed (use pre-commit hooks or CI checks).

We also run Prettier for consistent formatting – set up via an ESLint plugin or separate, but ensure no stylistic nits in PRs.

## Strict Mode in React

If using React, always render the app in `<React.StrictMode>` in development. This doesn’t affect production, but it double-invokes certain functions to help catch side effect issues. Our Next.js apps by default run in strict mode (check `next.config.js` to ensure `reactStrictMode` is `true`).

## Build and Bundle Checks

Using `tsdown` to bundle libraries/CLIs, ensure its config upholds strictness:

- `tsdown` will use our `tsconfig`; ensure `tsconfig` has no `"skipDiagnostics"` or relaxations in production build.
- When bundling, treat type errors as fatal – do not ignore type errors during build (no `--ignore-build-errors` in Next or similar).
- Set up CI to run `tsc --noEmit` as a step. This compiles the project in full strict mode without emitting, catching any type regressions even if we normally rely on just Vite/Next’s build (which might not fail on type errors depending on config).

## Runtime Strictness & Config

- Use TypeScript’s `tsc --strict` for type checks, but also consider runtime checks for critical values: e.g., use Zod to validate environment configs at startup. This fails fast if ENV vars are missing or malformed instead of causing weird errors later.
- In Node apps, enable `"strictBindCallApply": true` (part of `strict`) to catch incorrect usage of `this`.
- If applicable, use flags like `"--enable-source-maps"` in Node so stack traces map to TS sources, aiding debugging.

## Linters/Formatters for Other Concerns

- **Package.json lint**: Use tools to ensure `package.json` dependencies are sorted and no duplicates (could be part of `pnpm`).
- **Import alias enforcement**: If we use path aliases (like `@app/*` in `tsconfig`), ensure TS and ESLint are configured to resolve them, and perhaps ban using long relative imports across certain layers (to enforce using the alias for clarity).
- **Commit hooks**: Possibly use Husky + `lint-staged` to run `eslint --fix` and `tsc --noEmit` on commit, catching issues early.

## Updating and Maintaining Configuration

Our dev dependency updates (like new TS, new ESLint rules) should be done regularly:

- When TS releases a new major/minor, update it and enable any new strict flags it introduces if they catch real issues.
- Periodically review the `strict-configuration.md` (this doc) to update guidance (for 2026, TypeScript 5.x is current; if 2027 TS 6.x introduces stricter checks, incorporate them).
- Automate linting and type-check in CI to prevent merges that break strictness.

By enforcing these configurations:

- We catch `null`/`undefined` issues at compile time instead of production.
- We avoid common JavaScript pitfalls (loose typing, undeclared variables, etc.).
- The codebase remains consistent, which makes it easier to onboard new developers and integrate new tools.

In summary, no code should leave the developer’s desk without passing a strict `tsc` check and ESLint. These checks are our first line of defense for code quality and bug prevention.
