# React Package Structure

## Standard Layout

```
packages/<package-name>/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # Public exports only
│   ├── <MainComponent>.tsx   # Primary component
│   ├── types.ts              # Public type definitions
│   │
│   ├── engine/               # Animation/logic engines (optional)
│   │   ├── types.ts
│   │   └── <engine-name>.ts
│   │
│   ├── ui/                   # Internal sub-components
│   │   └── *.tsx
│   │
│   ├── hooks/                # Internal hooks
│   │   └── use*.ts
│   │
│   └── styles/               # CSS (if needed)
│       └── *.css
```

## package.json Template

```json
{
  "name": "@raamattu-nyt/<package-name>",
  "version": "1.0.0",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "peerDependencies": {
    "react": ">=18"
  },
  "dependencies": {}
}
```

## tsconfig.json Template

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

## index.ts Export Pattern

```typescript
// Public component
export { MainComponent } from "./MainComponent";

// Public types
export type {
  MainComponentProps,
  PublicType1,
  PublicType2,
} from "./types";

// DO NOT export internal hooks, ui components, or engine details
```

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Package | kebab-case | `cinema-reader` |
| Component | PascalCase | `CinemaReader` |
| Hook | camelCase with `use` | `useFullscreen` |
| Type | PascalCase | `CinemaVerse` |
| Engine | camelCase with suffix | `gsapVerticalLoopEngine` |
