# TypeScript Configuration Best Practices

Optimal tsconfig.json settings for type safety.

## Recommended Base Configuration

```json
{
  "compilerOptions": {
    // Strict type checking
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,

    // Module settings
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "isolatedModules": true,

    // Output settings
    "target": "ES2022",
    "outDir": "./dist",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Path settings
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    },

    // Skip type checking node_modules
    "skipLibCheck": true,

    // Allow importing JSON
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Strict Mode Flags Explained

| Flag | Purpose | Why Enable |
|------|---------|------------|
| `strict` | Enables all strict flags | Base requirement |
| `noUncheckedIndexedAccess` | Array access returns `T \| undefined` | Catches out-of-bounds |
| `noImplicitReturns` | All code paths must return | Catches missing returns |
| `noFallthroughCasesInSwitch` | Switch cases must break/return | Prevents bugs |
| `noImplicitOverride` | Explicit override keyword | Clearer inheritance |

## Project-Specific Configurations

### Node.js Backend

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "target": "ES2022",
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### React Frontend

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

### Library Package

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "composite": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

## Common Problems

### "Cannot find module"

```json
{
  "compilerOptions": {
    "moduleResolution": "NodeNext",  // or "bundler" for Vite/webpack
    "esModuleInterop": true
  }
}
```

### Slow Compilation

```json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "incremental": true
  }
}
```

### Path Aliases Not Working

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}

// Also configure in bundler (vite.config.ts, etc.)
```

## ESLint Integration

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-type-checked"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```
