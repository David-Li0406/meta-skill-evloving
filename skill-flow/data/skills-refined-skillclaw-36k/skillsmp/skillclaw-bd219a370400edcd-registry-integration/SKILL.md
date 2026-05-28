---
name: registry-integration
description: Use this skill when registering 8-bit components in `registry.json` for the shadcn/ui add command.
---

# Skill body

## Registry Integration

Register 8-bit components in `registry.json` for discovery via `shadcn add @8bitcn/[component-name]`.

### Component Entry Pattern

```json
{
  "name": "button",
  "type": "registry:component",
  "title": "8-bit Button",
  "description": "A simple 8-bit button component",
  "registryDependencies": ["button"],
  "files": [
    {
      "path": "components/ui/8bit/button.tsx",
      "type": "registry:component",
      "target": "components/ui/8bit/button.tsx"
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
  "name": "quest-log",
  "type": "registry:block",
  "title": "8-bit Quest Log",
  "description": "An 8-bit quest and mission tracking system.",
  "registryDependencies": ["card", "accordion"],
  "categories": ["gaming"],
  "files": [
    {
      "path": "components/ui/8bit/quest-log.tsx",
      "type": "registry:block",
      "target": "components/ui/8bit/quest-log.tsx"
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
    "path": "components/ui/8bit/new-component.tsx",
    "type": "registry:component",
    "target": "components/ui/8bit/new-component.tsx"
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
"registryDependencies": ["button", "dialog", "progress"]
```

For blocks with multiple components:

```json
"registryDependencies": ["card", "button", "progress", "tabs"]
```

### Type Selection

**registry:component** - Single reusable component:

```json
{
  "type": "registry:component",
  "files": [...]
}
```

**registry:block** - A collection of components for a specific layout or functionality.