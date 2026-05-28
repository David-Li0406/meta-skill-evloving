---
name: shadcn-ui
description: Use this skill when setting up the shadcn/ui component library, including installation, configuration, and implementation of accessible React components.
---

# shadcn/ui Component Library

shadcn/ui is a collection of beautifully-designed, accessible components built with TypeScript, Tailwind CSS, and Radix UI primitives. It supports multiple frameworks including Next.js, Vite, Remix, and Astro. This skill provides guidance on installation, configuration, and usage of the library.

## Key Principles

- **Open Code**: Components are copied into your project, not installed as dependencies.
- **Composition**: Build complex UIs by composing simple components.
- **Distribution**: CLI and registry system for easy component management.
- **Beautiful Defaults**: Production-ready styling out of the box.
- **AI-Ready**: Designed to work well with AI assistants.

## Quick Start

### Installation & Setup

For new projects, use the automated setup:

```bash
# Create Next.js project with shadcn/ui
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Install essential components
npx shadcn@latest add button input form card dialog select
```

For existing projects:

```bash
# Install dependencies
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge lucide-react

# Initialize shadcn/ui
npx shadcn@latest init
```

### CLI Commands

```bash
# Add a component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button card dialog

# Add all components
npx shadcn@latest add --all

# Update components
npx shadcn@latest diff

# List available components
npx shadcn@latest add
```

### Configuration (components.json)

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

## Core Components

- **Button**
- **Input & Form Fields**
- **Forms with Validation**
- **Card**
- **Dialog (Modal)**
- **Select (Dropdown)**
- **Sheet (Slide-over)**
- **Menubar & Navigation**
- **Table**
- **Toast Notifications**

## Customization

Customize component styling with Tailwind CSS and implement design systems with shadcn/ui.

## Best Practices

- Create accessible UI components (buttons, dialogs, dropdowns).
- Build forms with React Hook Form and Zod validation.
- Implement complex layouts and data displays.

## Documentation Index

| Topic | URL | Description |
|-------|-----|-------------|
| Introduction | https://ui.shadcn.com/docs | Core principles and getting started |
| CLI | https://ui.shadcn.com/docs/cli | Command-line tool reference |
| components.json | https://ui.shadcn.com/docs/components-json | Configuration file documentation |
| Theming | https://ui.shadcn.com/docs/theming | Colors, typography, design tokens |
| Changelog | https://ui.shadcn.com/docs/changelog | Release notes and version history |