# Create a Global Context

Use this for **app-wide contexts** like Theme, Auth, or Config. For component-scoped contexts, use `--with-context` on the component command instead (see components.md).

```bash
pnpm file-factory context Theme --package squareone
pnpm file-factory context RSPConfig --package squareone
```

## Command Options

| Option                 | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `-p, --package <name>` | Target package (e.g., `squared`, `squareone`)     |
| `--dry-run`            | Show what would be created without writing files  |
| `-v, --verbose`        | Verbose output                                    |

## File structures

**Generated structure:**

```
src/contexts/ThemeContext/
├── ThemeContext.tsx     # ThemeProvider + useTheme hook
└── index.ts             # Exports provider, hook, and types
```

**What's exported:**

- `ThemeProvider` - The provider component
- `useTheme` - The consumer hook
- `ThemeContextValue` - TypeScript type
- **NOT** the raw `ThemeContext` (encapsulated)
