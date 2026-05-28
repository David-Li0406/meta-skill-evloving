# Configuring file-factory for specific apps and packages

The .file-factory directory in each project/app provides customizations and configurations for file creation.

## Template Customization

Each package can override templates in `.file-factory/templates/`. The directory structure mirrors the output:

```
.file-factory/
├── config.mts          # Use .mts for Next.js apps
└── templates/
    └── component/
        └── {{ComponentName}}/
            ├── {{ComponentName}}.tsx.ejs    # Custom component template
            └── index.ts.ejs
```

## Configuration File

Create `.file-factory/config.mts` (or `config.ts`) in your package.

**Recommended**: Use `.mts` extension for packages without `"type": "module"` in package.json (like Next.js apps). The `.mts` extension explicitly marks the file as an ES module.

**Note**: The `defineConfig` import is optional - you can export a plain object. The CLI validates configs with Zod after loading. Use `defineConfig` only when you need TypeScript type hints during authoring in packages with `@lsst-sqre/file-factory` installed as a dependency.

```typescript
// Plain object export (recommended for apps like squareone)
export default {
  component: {
    directory: "src/components",
    styleSystem: "css-modules",
    withTest: true,
    withStory: true,
    appRouterBarrel: false,
    // Display instructions after creation (optional)
    postCreationMessage: {
      message: `Add the component to the package exports:

1. In src/components/index.ts, add:
   export * from './{{ComponentName}}';

2. In src/index.ts, add:
   export * from './components/{{ComponentName}}';`,
    },
  },
  hook: {
    directory: "src/hooks",
    withTest: true,
    useDirectory: true,
  },
  context: {
    directory: "src/contexts",
  },
  page: {
    directory: "src/pages",
    router: "pages",
  },
};
```

## Post-Creation Messages

The `postCreationMessage` option allows packages to display custom instructions after file creation. This is useful for:

- Instructing users to add exports to root barrel files
- Reminding about additional setup steps
- Providing package-specific guidance

The message supports `{{VariableName}}` placeholders that get replaced with:
- **Components**: `{{ComponentName}}`, `{{componentName}}`, `{{component-name}}`
- **Hooks**: `{{hookName}}`, `{{hook-name}}`
- **Contexts**: `{{ContextName}}`, `{{ProviderName}}`, `{{consumerHookName}}`
- **Pages**: `{{pageName}}`, `{{PageName}}`, `{{pagePath}}`
