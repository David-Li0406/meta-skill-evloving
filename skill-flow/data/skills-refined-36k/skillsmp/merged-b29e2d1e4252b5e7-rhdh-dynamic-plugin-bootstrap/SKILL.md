---
name: rhdh-dynamic-plugin-bootstrap
description: Use this skill when creating dynamic plugins for the Red Hat Developer Hub (RHDH), whether frontend or backend, to bootstrap and configure the necessary components for deployment.
---

## Purpose

Bootstrap a new dynamic plugin for Red Hat Developer Hub (RHDH). This skill supports both **frontend** and **backend** dynamic plugins, which provide various functionalities and integrations within the RHDH application shell.

> **Note:** This skill covers both frontend and backend plugins. Use the appropriate sections based on the type of plugin being created.

## When to Use

Use this skill when creating a new dynamic plugin intended for RHDH deployment. This includes:
- **Frontend Plugins**: UI components, pages, entity cards, themes, and visual customizations.
- **Backend Plugins**: API plugins, backend modules, scaffolder actions, catalog processors, and server-side functionalities.

**Do NOT use this skill for:**
- Frontend plugins when only backend functionalities are needed, or vice versa.
- Non-plugin related tasks.

## Prerequisites

Before starting, ensure the following are available:
- Node.js 22+ and Yarn
- Container runtime (`podman` or `docker`)
- Access to a container registry (e.g., quay.io) for publishing

## Workflow Overview

1. **Determine RHDH Version** - Identify target RHDH version for compatibility.
2. **Create Backstage App** - Scaffold Backstage app with matching version.
3. **Create Plugin** - Generate new frontend or backend plugin using Backstage CLI.
4. **Implement Plugin Logic** - Write the plugin code using the appropriate system.
5. **Export as Dynamic Plugin** - Build and export using RHDH CLI.
6. **Package as OCI Image** - Create container image for deployment.
7. **Configure Plugin Wiring** - Define routes, mount points, and menu items for frontend; create dynamic-plugins.yaml for backend.

## Step 1: Determine RHDH Version

Check the target RHDH version and find the compatible Backstage version. Consult the version compatibility matrix.

| RHDH Version | Backstage Version | create-app Version |
|--------------|-------------------|-------------------|
| 1.8 / next   | 1.42.5           | 0.7.3             |
| 1.7          | 1.39.1           | 0.6.2             |
| 1.6          | 1.36.1           | 0.5.25            |
| 1.5          | 1.35.1           | 0.5.24            |

Ask the user which RHDH version they are targeting if not specified.

## Step 2: Create Backstage Application

```bash
# For RHDH 1.7 (adjust version as needed)
npx @backstage/create-app@0.6.2

cd <app-name>
yarn install
```

## Step 3: Create Plugin

### For Frontend Plugin

Generate a new frontend plugin:

```bash
yarn new --select frontend-plugin --option id=<plugin-id>
```

### For Backend Plugin

Generate a new backend plugin:

```bash
yarn new
```

When prompted:
1. Select **"backend-plugin"** as the plugin type.
2. Enter a plugin ID (e.g., `my-plugin`).

## Step 4: Implement Plugin Logic

### Frontend Plugin

Implement React components and exports. Example structure for a page component:

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

### Backend Plugin

Use the new backend system for dynamic plugin compatibility. Example plugin structure:

```typescript
import {
  coreServices,
  createBackendPlugin,
} from '@backstage/backend-plugin-api';
import { createRouter } from './service/router';

export const myPlugin = createBackendPlugin({
  pluginId: 'my-plugin',
  register(env) {
    env.registerInit({
      deps: {
        httpRouter: coreServices.httpRouter,
        logger: coreServices.logger,
        config: coreServices.rootConfig,
      },
      async init({ httpRouter, logger, config }) {
        httpRouter.use(
          await createRouter({
            logger,
            config,
          }),
        );
      },
    });
  },
});

export default myPlugin;
```

## Step 5: Export as Dynamic Plugin

### For Frontend Plugin

```bash
cd plugins/<plugin-id>
npx @red-hat-developer-hub/cli@latest plugin export
```

### For Backend Plugin

```bash
cd plugins/<plugin-id>-backend
npx @red-hat-developer-hub/cli@latest plugin export
```

## Step 6: Package as OCI Image

```bash
cd plugins/<plugin-id>
npx @red-hat-developer-hub/cli@latest plugin package \
  --tag quay.io/<namespace>/<plugin-name>:v0.1.0

podman push quay.io/<namespace>/<plugin-name>:v0.1.0
```

## Step 7: Configure Plugin Wiring

### For Frontend Plugin

Define routes, mount points, and menu items in `dynamic-plugins.yaml`:

```yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:v0.1.0!my-plugin
    disabled: false
    pluginConfig:
      dynamicPlugins:
        frontend:
          my-org.plugin-my-plugin:
            dynamicRoutes:
              - path: /my-plugin
                importName: MyPage
                menuItem:
                  icon: dashboard
                  text: My Plugin
```

### For Backend Plugin

Create dynamic-plugins.yaml configuration:

```yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:v0.1.0!<plugin-id>-backend-dynamic
    disabled: false
    pluginConfig:
      myPlugin:
        someOption: value
```

## Debugging

For local debugging of dynamic plugins, build and copy the plugin to the appropriate directory, then start RHDH backend with debugging enabled.

## Additional Resources

### Reference Files

- **`references/versions.md`** - Version compatibility matrix.
- **`references/export-guide.md`** - Export options and flags.
- **`references/packaging-guide.md`** - Packaging methods.
- **`references/debugging.md`** - Local and container debugging.

### External Resources

- [RHDH Dynamic Plugins Documentation](https://github.com/redhat-developer/rhdh/tree/main/docs/dynamic-plugins)
- [Backstage Plugin Development](https://backstage.io/docs/plugins/)