---
name: RHDH Backend Dynamic Plugin Bootstrap
description: This skill should be used when the user asks to "create RHDH backend plugin", "bootstrap backend dynamic plugin", "create backstage backend plugin for RHDH", "new backend plugin for Red Hat Developer Hub", "create dynamic backend plugin", "scaffold RHDH backend plugin", "new scaffolder action", "create catalog processor", or mentions creating a new backend plugin, backend module, or server-side functionality for Red Hat Developer Hub or RHDH. This skill is specifically for backend plugins - for frontend plugins, use the separate frontend plugin skill.
---

## Purpose

Bootstrap a new **backend** dynamic plugin for Red Hat Developer Hub (RHDH). RHDH is the enterprise-ready Backstage applicationthat supports dynamic plugins - plugins that can be installed or uninstalled without rebuilding the application.

> **Note:** This skill covers **backend plugins only**. Frontend dynamic plugins have different requirements (Scalprum configuration, mount points, dynamic routes) and are covered in a separate skill.

## When to Use

Use this skill when creating a new **backend** plugin intended for RHDH dynamic plugin deployment. This includes:
- New backend API plugins
- Backend modules for existing plugins (e.g., `catalog-backend-module-*`)
- Scaffolder actions and templates
- Catalog processors and providers
- Authentication modules
- Any server-side functionality for RHDH

**Do NOT use this skill for:**
- Frontend plugins (UI components, pages, cards)
- Frontend plugin wiring (mount points, dynamic routes)
- Themes or frontend customizations

## Prerequisites

Before starting, ensure the following are available:
- Node.js 22+ and Yarn
- Container runtime (`podman` or `docker`)
- Access to a container registry (e.g., quay.io) for publishing

## Workflow Overview

1. **Determine RHDH Version** - Identify target RHDH version for compatibility
2. **Create Backstage App** - Scaffold Backstage app with matching version
3. **Create Backend Plugin** - Generate new backend plugin using Backstage CLI
4. **Implement Plugin Logic** - Write the plugin code using new backend system
5. **Export as Dynamic Plugin** - Build and export using RHDH CLI
6. **Package as OCI Image** - Create container image for deployment
7. **Configure for RHDH** - Create dynamic-plugins.yaml configuration

## Step 1: Determine RHDH Version

Check the target RHDH version and find the compatible Backstage version. Consult `references/versions.md` for the version compatibility matrix.

| RHDH Version | Backstage Version | create-app Version |
|--------------|-------------------|-------------------|
| 1.8 / next   | 1.42.5           | 0.7.3             |
| 1.7          | 1.39.1           | 0.6.2             |
| 1.6          | 1.36.1           | 0.5.25            |
| 1.5          | 1.35.1           | 0.5.24            |

Ask the user which RHDH version they are targeting if not specified.

## Step 2: Create Backstage Application

Create a new Backstage application using the version-appropriate create-app:

```bash
# For RHDH 1.7 (adjust version as needed)
npx @backstage/create-app@0.6.2

# Follow prompts to name the application
# This creates the monorepo structure needed for plugin development
```

After creation, navigate to the app directory and install dependencies:

```bash
cd <app-name>
yarn install
```

## Step 3: Create Backend Plugin

Generate a new backend plugin using the Backstage CLI:

```bash
yarn new
```

When prompted:
1. Select **"backend-plugin"** as the plugin type
2. Enter a plugin ID (e.g., `my-plugin`)
3. The plugin will be created at `plugins/<plugin-id>-backend/`

The generated plugin structure:

```
plugins/<plugin-id>-backend/
├── src/
│   ├── index.ts           # Main entry point
│   ├── plugin.ts          # Plugin definition (new backend system)
│   └── service/
│       └── router.ts      # Express router
├── package.json
└── README.md
```

## Step 4: Implement Plugin Logic

Backend plugins must use the **new backend system** for dynamic plugin compatibility. The plugin entry point should export a default using `createBackendPlugin()` or `createBackendModule()`.

Example plugin structure (`src/plugin.ts`):

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
        httpRouter.addAuthPolicy({
          path: '/health',
          allow: 'unauthenticated',
        });
      },
    });
  },
});

export default myPlugin;
```

The `src/index.ts` must export the plugin as default:

```typescript
export { default } from './plugin';
```

Build and verify the plugin compiles:

```bash
cd plugins/<plugin-id>-backend
yarn build
```

## Step 5: Export as Dynamic Plugin

Use the RHDH CLI to export the plugin as a dynamic plugin package:

```bash
cd plugins/<plugin-id>-backend
npx @red-hat-developer-hub/cli@latest plugin export
```

This command:
- Builds the plugin
- Creates `dist-dynamic/` directory with the dynamic plugin package
- Configures dependencies (peer vs bundled)
- Generates config schema

The CLI automatically handles:
- **Shared dependencies**: `@backstage/*` packages become peerDependencies
- **Bundled dependencies**: Non-backstage deps are bundled in the package
- **Embedded packages**: `-node` and `-common` suffix packages are embedded

For custom dependency handling, use flags:

```bash
# Mark a @backstage package as NOT shared (bundle it)
npx @red-hat-developer-hub/cli@latest plugin export \
  --shared-package '!/@backstage/plugin-notifications/'

# Embed a specific package
npx @red-hat-developer-hub/cli@latest plugin export \
  --embed-package @my-org/common-utils
```

See `references/export-guide.md` for detailed export options.

## Step 6: Package as OCI Image

Package the dynamic plugin as an OCI container image for distribution:

```bash
cd plugins/<plugin-id>-backend
npx @red-hat-developer-hub/cli@latest plugin package \
  --tag quay.io/<namespace>/<plugin-name>:v0.1.0
```

Push the image to your container registry:

```bash
podman push quay.io/<namespace>/<plugin-name>:v0.1.0
# or
docker push quay.io/<namespace>/<plugin-name>:v0.1.0
```

See `references/packaging-guide.md` for alternative packaging methods (tgz, npm).

## Step 7: Configure for RHDH

Create the dynamic plugin configuration for RHDH. Add to `dynamic-plugins.yaml`:

```yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:v0.1.0!<plugin-id>-backend-dynamic
    disabled: false
    pluginConfig:
      # Plugin-specific configuration (optional)
      myPlugin:
        someOption: value
```

For local development/testing, copy `dist-dynamic` to RHDH's `dynamic-plugins-root`:

```bash
cp -r dist-dynamic /path/to/rhdh/dynamic-plugins-root/<plugin-id>-backend-dynamic
```

See `examples/dynamic-plugins.yaml` for a complete configuration example.

## Debugging

For local debugging of dynamic plugins:

1. Build and copy plugin to `dynamic-plugins-root/`
2. Start RHDH backend with debugging:
   ```bash
   yarn workspace backend start --inspect
   ```
3. Attach IDE debugger to port 9229
4. Set breakpoints in `dynamic-plugins-root/<plugin-id>/` files

See `references/debugging.md` for container-based debugging.

## Common Issues

### Plugin Not Loading
- Verify plugin uses new backend system (`createBackendPlugin`)
- Check plugin is exported as default export
- Ensure version compatibility with target RHDH

### Dependency Conflicts
- Use `--shared-package` to exclude problematic shared deps
- Use `--embed-package` to bundle required deps

### Build Failures
- Run `yarn tsc` to check TypeScript errors before export
- Ensure all `@backstage/*` versions match target RHDH

## Additional Resources

### Reference Files

For detailed documentation, consult:
- **`references/versions.md`** - Complete version compatibility matrix
- **`references/export-guide.md`** - Detailed export options and flags
- **`references/packaging-guide.md`** - OCI, tgz, and npm packaging
- **`references/debugging.md`** - Local and container debugging

### Example Files

Examples in `examples/`:
- **`dynamic-plugins.yaml`** - Example RHDH plugin configuration

### External Resources

- [RHDH Dynamic Plugins Documentation](https://github.com/redhat-developer/rhdh/tree/main/docs/dynamic-plugins)
- [Backstage New Backend System](https://backstage.io/docs/backend-system/)
