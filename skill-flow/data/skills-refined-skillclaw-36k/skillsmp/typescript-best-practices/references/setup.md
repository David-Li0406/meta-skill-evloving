# Environment Setup

## Recommended tsconfig

Use the strictest base from [tsconfig/bases](https://github.com/tsconfig/bases):

```bash
npm install -D @tsconfig/strictest
```

```json
{
  "extends": "@tsconfig/strictest/tsconfig.json",
  "compilerOptions": {
    "outDir": "dist"
  }
}
```

## Important Strict Options

`@tsconfig/strictest` already enables these options. Ensure they remain enabled:

| Option | Effect |
|--------|--------|
| `noUncheckedIndexedAccess` | Array/object index access returns `T \| undefined`, forcing null checks |
| `noPropertyAccessFromIndexSignature` | Requires bracket notation for index signatures, making dynamic access explicit |

If not using `@tsconfig/strictest`, add them manually:

```json
{
  "compilerOptions": {
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

## ts-reset

Install [ts-reset](https://github.com/mattpocock/ts-reset) for better built-in types:

```bash
npm install -D @total-typescript/ts-reset
```

```typescript
// reset.d.ts
import '@total-typescript/ts-reset';
```

Place this file in each TypeScript project root (where `tsconfig.json` is located). If using **project references** (build mode) with multiple `tsconfig.json` files, each project needs its own `reset.d.ts`:

```
packages/
├── core/
│   ├── tsconfig.json
│   └── reset.d.ts        ← needed
├── utils/
│   ├── tsconfig.json
│   └── reset.d.ts        ← needed
└── tsconfig.json         ← root (references only, no reset needed)
```

**Benefits:**
- `JSON.parse` returns `unknown` instead of `any`
- `.filter(Boolean)` removes falsy types correctly
- `Array.includes` has stricter checking

## Additional Resources

- [tsconfig/bases](https://github.com/tsconfig/bases) - Strictest base configs
- [ts-reset](https://github.com/mattpocock/ts-reset) - Better built-in types
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/) - Official documentation
