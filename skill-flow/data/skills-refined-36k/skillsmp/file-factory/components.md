# Creating a new component

```bash
# Basic component (CSS Modules by default)
pnpm file-factory component Button --package squareone

# Component with its own scoped context
pnpm file-factory component DataTable --with-context --package squareone

# With Storybook story
pnpm file-factory component Card --with-story --package squared

# Without test file
pnpm file-factory component Modal --no-test --package squareone

# Explicitly specify CSS Modules (default)
pnpm file-factory component Modal --style css-modules --package squared
```

## Command reference

| Option                 | Description                                                   |
| ---------------------- | ------------------------------------------------------------- |
| `--with-context`       | Include a component-scoped context                            |
| `--with-test`          | Include test file (default from config)                       |
| `--no-test`            | Exclude test file                                             |
| `--with-story`         | Include Storybook story                                       |
| `--no-story`           | Exclude Storybook story                                       |
| `--style <system>`     | Style system: `css-modules` (default), `tailwind`, `none` |
| `-p, --package <name>` | Target package (e.g., `squared`, `squareone`)                 |
| `--dry-run`            | Show what would be created without writing files              |
| `-v, --verbose`        | Verbose output                                                |

## File structures

**Basic component structure:**

```
src/components/Button/
├── Button.tsx           # Main component
├── Button.module.css    # CSS Module styles (when using css-modules)
├── Button.test.tsx      # Test file (when withTest is true)
├── Button.stories.tsx   # Storybook story (when withStory is true)
└── index.ts             # Barrel file
```

**Component with context structure (`--with-context`):**

```
src/components/DataTable/
├── DataTable.tsx            # Main component
├── DataTableContext.tsx     # Scoped context (Provider + useDataTable hook)
├── DataTable.module.css     # CSS Module styles
├── DataTable.test.tsx       # Test file
└── index.ts                 # Exports component, provider, and hook
```

For details on coding conventions for components, see the [component-creation](../component-creation/SKILL.md) Claude Skill.
