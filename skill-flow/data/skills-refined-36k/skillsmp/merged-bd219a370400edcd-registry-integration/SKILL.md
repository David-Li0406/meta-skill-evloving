---
name: registry-integration
description: Use this skill when registering 8-bit components in `registry.json` for the shadcn/ui add command.
---

## Registry Integration

Register 8-bit components in `registry.json` for discovery via `shadcn add @8bitcn/[component-name]`.

### Component Entry Pattern

```json
{
  "name": "<component-name>",
  "type": "registry:component",
  "title": "<Component Title>",
  "description": "<Component Description>",
  "registryDependencies": ["<dependency1>", "<dependency2>"],
  "files": [
    {
      "path": "components/ui/8bit/<component-name>.tsx",
      "type": "registry:component",
      "target": "components/ui/8bit/<component-name>.tsx"
    },
    {
      "path": "components/ui/8bit/styles/retro.css",
      "type": "registry:component",
      "target": "components/ui/8bit/styles/retro.css"
    }
  ]
}
```

### Block Entry Pattern

For pre-built layouts like game UIs:

```json
{
  "name": "<block-name>",
  "type": "registry:block",
  "title": "<Block Title>",
  "description": "<Block Description>",
  "registryDependencies": ["<dependency1>", "<dependency2>"],
  "categories": ["gaming"],
  "files": [
    {
      "path": "components/ui/8bit/blocks/<block-name>.tsx",
      "type": "registry:block",
      "target": "components/ui/8bit/blocks/<block-name>.tsx"
    },
    {
      "path": "components/ui/8bit/styles/retro.css",
      "type": "registry:component",
      "target": "components/ui/8bit/styles/retro.css"
    }
  ]
}
```

### Required retro.css

Always include `retro.css` in the files array:

```json
"files": [
  {
    "path": "components/ui/8bit/<new-component>.tsx",
    "type": "registry:component",
    "target": "components/ui/8bit/<new-component>.tsx"
  },
  {
    "path": "components/ui/8bit/styles/retro.css",
    "type": "registry:component",
    "target": "components/ui/8bit/styles/retro.css"
  }
]
```

### Categories

Use gaming-specific categories for game components:

```json
"categories": ["gaming"]
```

Available categories: `gaming`, `layout`, `form`, `data-display`, `feedback`, `navigation`, `overlay`.

### Registry Dependencies

List base shadcn dependencies (not 8-bit versions):

```json
"registryDependencies": ["<dependency1>", "<dependency2>"]
```

For blocks with multiple components:

```json
"registryDependencies": ["<dependency1>", "<dependency2>", "<dependency3>"]
```

### Key Principles

1. **Type** - Use `registry:component` for single components, `registry:block` for layouts.
2. **retro.css required** - Always include in the files array.
3. **Target path** - Use the same path for source and target.
4. **Categories** - Use `gaming` for retro-themed components.
5. **Dependencies** - List base shadcn/ui components (not 8-bit versions).
6. **Description** - Provide a clear, concise description for CLI output.

### Adding a New Component

1. Create the component in `components/ui/8bit/<component-name>.tsx`.
2. Update `registry.json` with the new entry:
   - Copy an existing component as a template.
   - Update name, title, description, and registryDependencies.
   - Include `retro.css` in the files.
3. Test the integration with: `pnpm dlx shadcn@latest add @8bitcn/<component-name>`.

### Reference

- `registry.json` - Full component registry.
- `content/docs/components/*.mdx` - Component documentation.