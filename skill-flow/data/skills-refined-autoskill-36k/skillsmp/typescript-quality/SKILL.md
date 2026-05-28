---
name: typescript-quality
description: This skill should be used when the user asks to "fix type errors", "fix tsc errors", "add TypeScript types", "enable strict mode", "strict null checks", "noImplicitAny", "add TSDoc", "install @types", "run typecheck", "handle implicit any", or needs guidance on TypeScript type safety, strict mode compliance, TSDoc documentation, or DefinitelyTyped packages.
---

# TypeScript Quality Standards

This skill covers TypeScript-specific quality requirements including strict mode compliance, type safety, and documentation standards.

## Type Checking

Run type checking through package.json scripts:
```bash
bun run typecheck     # Preferred - uses project tsconfig.json
bunx tsc --noEmit     # Only if no typecheck script exists
```

**CRITICAL: NEVER run tsc with individual file arguments.** TypeScript needs the full project context for proper type-checking. The `block-tsc-with-files` hook will prevent this, but avoid attempting it.

## Strict Mode Compliance

All TypeScript projects use strict mode. Ensure:
- No implicit `any` types - all variables, parameters, and return types should have explicit types or be inferable
- Proper null safety - no unguarded access to potentially null/undefined values
- No `@ts-ignore` without exceptional justification and comment explaining why
- No non-null assertion (`!`) without safety checks or clear documentation

## TSDoc Documentation

Document public APIs with TSDoc format:
```typescript
/**
 * Brief description of function purpose
 *
 * @param input - Description of the input parameter
 * @param schema - Description of the schema parameter
 * @returns Description of return value
 * @throws {ErrorType} When this error is thrown
 * @example
 * ```typescript
 * const result = myFunction(input, schema);
 * ```
 */
export function myFunction<T>(input: unknown, schema: Schema<T>): T {
  // implementation
}
```

## Type Definitions

### Bundled Types (Preferred)
Package includes `types` field in package.json - no @types package needed.

### DefinitelyTyped (@types)
For packages without bundled types:
1. Search for an existing @types package first
2. Install as dev dependency:
```bash
bun add -d @types/package-name
```
Match the @types major version to the package major version (e.g., lodash@4.x uses @types/lodash@4.x).

### No Types Available
If a package has no types and no @types package exists:
1. Check if a newer version of the package has types
2. Search npm for alternative @types packages (sometimes named differently)
3. Create local `.d.ts` file with minimal declarations
4. As last resort, use `declare module 'package-name';`

## Quality Checklist

Before completing TypeScript work:
1. Zero TypeScript errors (check with `bun run typecheck` or watcher)
2. Zero TypeScript warnings
3. Proper type annotations on public APIs (no implicit any)
4. TSDoc comments on exported functions, classes, and types
5. Strict mode compliance (null safety, no @ts-ignore abuse)
6. @types packages added for dependencies without bundled types
