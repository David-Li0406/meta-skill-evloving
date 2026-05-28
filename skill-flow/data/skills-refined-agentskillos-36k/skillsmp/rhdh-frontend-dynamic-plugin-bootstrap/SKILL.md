---
name: RHDH Frontend Dynamic Plugin Bootstrap
description: This skill should be used when the user asks to "create RHDH frontend plugin", "bootstrap frontend dynamic plugin", "create UI plugin for RHDH", "new frontend plugin for Red Hat Developer Hub", "add entity card to RHDH", "create dynamic route", "add sidebar menu item", "configure mount points", "create theme plugin", or mentions creating frontend components, UI pages, entity cards, or visual customizations for Red Hat Developer Hub or RHDH. This skill is specifically for frontend plugins - for backend plugins, use the separate backend plugin skill.
---

## Purpose

Bootstrap a new **frontend** dynamic plugin for Red Hat Developer Hub (RHDH). Frontend dynamic plugins provide UI components, pages, entity cards, themes, and visual customizations that integrate with the RHDH application shell.

> **Note:** This skill covers **frontend plugins only**. Backend dynamic plugins (APIs, scaffolder actions, processors) are covered in a separate skill.

## When to Use

Use this skill when creating a new **frontend** plugin intended for RHDH dynamic plugin deployment. This includes:
- New pages and routes
- Entity page cards and tabs
- Sidebar menu items
- Custom themes
- Scaffolder field extensions
- TechDocs addons
- Search result types and filters
- Any UI component for RHDH

**Do NOT use this skill for:**
- Backend API plugins
- Scaffolder actions (server-side)
- Catalog processors or providers
- Authentication modules

## Prerequisites

Before starting, ensure the following are available:
- Node.js 22+ and Yarn
- Container runtime (`podman` or `docker`)
- Access to a container registry (e.g., quay.io) for publishing

## Workflow Overview

1. **Determine RHDH Version** - Identify target RHDH version for compatibility
2. **Create Backstage App** - Scaffold Backstage app with matching version
3. **Create Frontend Plugin** - Generate new frontend plugin using Backstage CLI
4. **Implement Plugin Components** - Build React components and exports
5. **Configure Scalprum** - Set up module federation for dynamic loading
6. **Export as Dynamic Plugin** - Build and export using RHDH CLI
7. **Package as OCI Image** - Create container image for deployment
8. **Configure Plugin Wiring** - Define routes, mount points, and menu items

## Step 1: Determine RHDH Version

Check the target RHDH version and find the compatible Backstage version. Consult `references/versions.md` (in the backend skill) for the version compatibility matrix.

| RHDH Version | Backstage Version | create-app Version |
|--------------|-------------------|-------------------|
| 1.8 / next   | 1.42.5           | 0.7.3             |
| 1.7          | 1.39.1           | 0.6.2             |
| 1.6          | 1.36.1           | 0.5.25            |

Ask the user which RHDH version they are targeting if not specified.

## Step 2: Create Backstage Application

```bash
# For RHDH 1.7 (adjust version as needed)
npx @backstage/create-app@0.6.2

cd <app-name>
yarn install
```

(you can create backstage app in the current directory by specifying `--path .`)

## Step 3: Decide if you want to use RHDH themes. 

If you want to use RHDH themes, follow the steps below. If you don't want to use RHDH themes, skip to Step 4.

Add RHDH theme to Backstage app dependencies:

```bash
yarn workspace app add @red-hat-developer-hub/backstage-plugin-theme
```

Update `packages/app/src/App.tsx` and apply the themes to `createApp`:

```typescript
import { getThemes } from '@red-hat-developer-hub/backstage-plugin-theme';

// ...

const app = createApp({
  apis,
  // ...
  themes: getThemes(),
});
```

## Step 3: Create Frontend Plugin

Generate a new frontend plugin:

```bash
yarn new --select frontend-plugin --option id=<plugin-id>
```

The plugin will be created at `plugins/<plugin-id>/`

Generated structure:

```
plugins/<plugin-id>/
├── src/
│   ├── index.ts              # Public exports
│   ├── plugin.ts             # Plugin definition
│   ├── routes.ts             # Route references
│   └── components/
│       └── ExampleComponent/
├── package.json
└── dev/
    └── index.tsx             # Development harness
```


## Step 4: If you decided to use RHDH themes, add RHDH Theme to Development Harness

By default, `yarn start` uses standard Backstage themes. To preview your plugin with RHDH styling during local development, configure the RHDH theme package.

### Install Theme Package

```bash
cd plugins/<plugin-id>
yarn add @red-hat-developer-hub/backstage-plugin-theme
```

### Configure Development Harness

Update `dev/index.tsx` to use RHDH themes:

```typescript
import { getAllThemes } from '@red-hat-developer-hub/backstage-plugin-theme';
import { createDevApp } from '@backstage/dev-utils';
import { myPlugin, MyPage } from '../src';

createDevApp()
  .registerPlugin(myPlugin)
  .addPage({
    element: <MyPage />,
    title: 'My Plugin',
    path: '/my-plugin',
  })
  .addThemes(getAllThemes())
  .render();
```

### Available Theme APIs

- `getThemes()` / `useThemes()` - Latest RHDH light and dark themes
- `getAllThemes()` / `useAllThemes()` - All themes including legacy versions
- `useLoaderTheme()` - Returns Material-UI v5 theme object

> **Note:** When deployed to RHDH, the application shell provides theming automatically. This configuration is only needed for local development.



## Step 5: Implement Plugin Components

### Page Component

Create a full-page component for dynamic routes:

```typescript
// src/components/MyPage/MyPage.tsx
import React from 'react';
import { Page, Header, Content } from '@backstage/core-components';

export const MyPage = () => (
  <Page themeId="tool">
    <Header title="My Plugin" />
    <Content>
      <h1>Hello from My Plugin</h1>
    </Content>
  </Page>
);
```

### Entity Card Component

Create a card for entity pages:

```typescript
// src/components/MyCard/MyCard.tsx
import React from 'react';
import { InfoCard } from '@backstage/core-components';
import { useEntity } from '@backstage/plugin-catalog-react';

export const MyEntityCard = () => {
  const { entity } = useEntity();
  return (
    <InfoCard title="My Plugin Info">
      <p>Entity: {entity.metadata.name}</p>
    </InfoCard>
  );
};
```

### Export Components

Export all components in `src/index.ts`:

```typescript
// src/index.ts
export { myPlugin } from './plugin';
export { MyPage } from './components/MyPage';
export { MyEntityCard } from './components/MyCard';
```

Build and verify:

```bash
cd plugins/<plugin-id>
yarn build
```

## Step 6: Export as Dynamic Plugin

```bash
cd plugins/<plugin-id>
npx @red-hat-developer-hub/cli@latest plugin export
```

Output shows the generated Scalprum configuration:

```
No scalprum config. Using default dynamic UI configuration:
{
  "name": "my-org.plugin-my-plugin",
  "exposedModules": {
    "PluginRoot": "./src/index.ts"
  }
}
```

The `dist-dynamic/` directory contains:
- `dist-scalprum/` - Webpack federated modules
- `package.json` - Modified for dynamic loading

## Step 7: Package as OCI Image

```bash
npx @red-hat-developer-hub/cli@latest plugin package \
  --tag quay.io/<namespace>/<plugin-name>:v0.1.0

podman push quay.io/<namespace>/<plugin-name>:v0.1.0
```

## Step 8: Configure Plugin Wiring

Frontend plugins require configuration in `dynamic-plugins.yaml` to define how they integrate with RHDH. This is the critical step that differentiates frontend from backend plugins.

### Basic Structure

```yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:v0.1.0!my-plugin
    disabled: false
    pluginConfig:
      dynamicPlugins:
        frontend:
          my-org.plugin-my-plugin:  # Must match scalprum.name
            dynamicRoutes: []       # Full page routes
            mountPoints: []         # Entity page integrations
            menuItems: {}           # Sidebar configuration
            appIcons: []            # Custom icons
            routeBindings: {}       # External route bindings
```

### Dynamic Routes (Full Pages)

Add a new page with sidebar menu:

```yaml
dynamicRoutes:
  - path: /my-plugin
    importName: MyPage
    menuItem:
      icon: dashboard
      text: My Plugin
```

### Mount Points (Entity Cards)

Add a card to entity overview:

```yaml
mountPoints:
  - mountPoint: entity.page.overview/cards
    importName: MyEntityCard
    config:
      layout:
        gridColumn: '1 / -1'
      if:
        allOf:
          - isKind: component
```

### Menu Items (Sidebar)

Configure sidebar ordering and nesting:

```yaml
menuItems:
  my-plugin:
    priority: 10
    parent: tools
  tools:
    icon: build
    title: Tools
    priority: 50
```

See `references/frontend-wiring.md` for complete wiring options.

## Common Wiring Patterns

### Entity Tab with Cards

```yaml
entityTabs:
  - path: /my-tab
    title: My Tab
    mountPoint: entity.page.my-tab

mountPoints:
  - mountPoint: entity.page.my-tab/cards
    importName: MyTabContent
```

### Conditional Rendering

```yaml
mountPoints:
  - mountPoint: entity.page.overview/cards
    importName: MyCard
    config:
      if:
        anyOf:
          - hasAnnotation: my-plugin/enabled
          - isType: service
```

### Custom Icons

```yaml
appIcons:
  - name: myCustomIcon
    importName: MyCustomIcon

dynamicRoutes:
  - path: /my-plugin
    importName: MyPage
    menuItem:
      icon: myCustomIcon
      text: My Plugin
```

## Known Issues

### MUI v5 Styles Missing

If using MUI v5, add class name generator to `src/index.ts`:

```typescript
import { unstable_ClassNameGenerator as ClassNameGenerator } from '@mui/material/className';

ClassNameGenerator.configure(componentName =>
  componentName.startsWith('v5-') ? componentName : `v5-${componentName}`
);

export * from './plugin';
```

### Grid Spacing Missing

Apply spacing manually to MUI v5 Grid:

```tsx
<Grid container spacing={2}>
  <Grid item>...</Grid>
</Grid>
```

## Debugging

Frontend plugins can be debugged in browser DevTools:
1. Open Developer Tools (F12)
2. Go to Sources tab
3. Find plugin source files (source maps included)
4. Set breakpoints

## Additional Resources

### Reference Files

- **`references/frontend-wiring.md`** - Complete mount points, routes, bindings
- **`references/entity-page.md`** - Entity page customization

### Example Files

- **`examples/frontend-plugin-config.yaml`** - Complete frontend wiring example

### External Resources

- [RHDH Frontend Plugin Wiring](https://github.com/redhat-developer/rhdh/blob/main/docs/dynamic-plugins/frontend-plugin-wiring.md)
- [Backstage Plugin Development](https://backstage.io/docs/plugins/)
