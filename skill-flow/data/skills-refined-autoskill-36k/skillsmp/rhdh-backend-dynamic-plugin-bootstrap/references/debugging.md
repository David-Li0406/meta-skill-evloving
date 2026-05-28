# Debugging Dynamic Plugins

This reference covers debugging techniques for RHDH dynamic plugins.

## Backend Plugin Local Debug

For local debugging, clone RHDH, run with debugging enabled, and attach your IDE debugger.

### Prerequisites

- RHDH source code cloned locally
- Plugin built and exported
- IDE with Node.js debugging support

### Step 1: Build and Deploy Plugin

```bash
cd ${pluginRootDir}
yarn build && yarn run export-dynamic
```

Copy to RHDH's dynamic plugins directory:

```bash
cp -r dist-dynamic /path/to/rhdh/dynamic-plugins-root/<plugin-id>-dynamic
```

### Step 2: Start RHDH in Debug Mode

From RHDH root directory:

```bash
yarn workspace backend start --inspect
```

Expected output:

```
Debugger listening on ws://127.0.0.1:9229/9299bb26-3c32-4781-9488-7759b8781db5
```

### Step 3: Access the Application

- Backend: http://localhost:7007
- Frontend (optional): `yarn start --filter=app` → http://localhost:3000

### Step 4: Attach IDE Debugger

#### VS Code

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to RHDH Backend",
      "port": 9229,
      "restart": true,
      "sourceMaps": true,
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "${workspaceFolder}"
    }
  ]
}
```

#### JetBrains IDEs

1. Run → Edit Configurations
2. Add → Attach to Node.js/Chrome
3. Port: 9229
4. Click Debug

### Step 5: Set Breakpoints

Add breakpoints in:
- `dynamic-plugins-root/<plugin-id>/dist/*.js`
- Or TypeScript sources if source maps are configured

### Source Map Configuration

For TypeScript debugging, ensure source maps are generated:

```json
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSources": true
  }
}
```

Configure IDE to use source maps for the plugin.

## Backend Plugin Container Debug

Debug plugins running in a container without cloning RHDH source.

### Prerequisites

- Plugin built and exported
- Container runtime (podman/docker)
- RHDH container image

### Step 1: Prepare Plugin

```bash
mkdir dynamic-plugins-root
yarn build && yarn export-dynamic
cp -r dist-dynamic ./dynamic-plugins-root/<plugin-id>-dynamic
```

### Step 2: Create App Config

Create `app-config.local.yaml` with plugin configuration:

```yaml
app:
  baseUrl: http://localhost:7007

backend:
  baseUrl: http://localhost:7007

# Plugin-specific config
myPlugin:
  someOption: value
```

### Step 3: Run Container with Debug

```bash
podman run \
  -v ./dynamic-plugins-root:/opt/app-root/src/dynamic-plugins-root:Z \
  -v ./app-config.local.yaml:/opt/app-root/src/app-config.local.yaml:Z \
  -p 7007:7007 \
  -p 9229:9229 \
  -e NODE_OPTIONS=--no-node-snapshot \
  --entrypoint='["node", "--inspect=0.0.0.0:9229", "packages/backend", "--config", "app-config.yaml", "--config", "app-config.example.yaml", "--config", "app-config.local.yaml"]' \
  quay.io/rhdh/rhdh-hub-rhel9:1.3
```

Key options:
- `-p 9229:9229` - Expose debug port
- `--inspect=0.0.0.0:9229` - Enable debugging on all interfaces
- `NODE_OPTIONS=--no-node-snapshot` - Required for debugging

### Step 4: Attach Debugger

Connect to `localhost:9229` from your IDE.

## Frontend Plugin Debug

Frontend plugins can be debugged directly in the browser.

### Enable Source Maps

Source maps are exported by default. Verify in `dist-scalprum/`:

```
dist-scalprum/
├── static/
│   ├── main.js
│   └── main.js.map
└── ...
```

### Browser DevTools

1. Open RHDH in browser
2. Open Developer Tools (F12)
3. Go to Sources tab
4. Find plugin source files
5. Set breakpoints

### React DevTools

Install React DevTools browser extension for component debugging:
- Inspect component props
- View component hierarchy
- Profile performance

## Common Debugging Scenarios

### Plugin Not Loading

Check RHDH logs for errors:

```bash
# Container logs
podman logs <container-id>

# Local logs
yarn workspace backend start 2>&1 | tee backend.log
```

Look for:
- `loaded dynamic backend plugin` - Success
- `Skipping disabled dynamic plugin` - Plugin disabled
- Error messages during plugin initialization

### Dependency Errors

```
Error: Cannot find module '@backstage/...'
```

Solutions:
1. Verify version compatibility
2. Check if dependency should be shared or bundled
3. Re-export with correct flags

### Configuration Errors

```
Error: Missing required config value
```

Solutions:
1. Check `app-config.yaml` has required values
2. Verify config schema matches plugin expectations
3. Check environment variables

### Runtime Errors

Set breakpoints at:
- Plugin entry point (`src/index.ts`)
- Router initialization
- API handlers

### Performance Issues

Use Node.js profiling:

```bash
yarn workspace backend start --inspect --prof
```

Analyze with:
```bash
node --prof-process isolate-*.log > profile.txt
```

## Logging Best Practices

### Use Logger Service

```typescript
import { coreServices } from '@backstage/backend-plugin-api';

env.registerInit({
  deps: {
    logger: coreServices.logger,
  },
  async init({ logger }) {
    logger.info('Plugin initialized');
    logger.debug('Debug info', { context: 'value' });
    logger.error('Error occurred', error);
  },
});
```

### Log Levels

Configure in app-config:

```yaml
backend:
  logging:
    level: debug  # error, warn, info, debug
```

### Structured Logging

Include context in logs:

```typescript
logger.info('Processing request', {
  requestId: req.id,
  userId: user.id,
  action: 'fetch',
});
```

## IDE-Specific Tips

### VS Code

- Use "JavaScript Debug Terminal" for automatic attach
- Install "Debugger for Chrome" for frontend
- Use compound configurations for full-stack debugging

### JetBrains

- Configure path mappings for source maps
- Use "Debug" tool window for variable inspection
- Set conditional breakpoints

### Vim/Neovim

- Use nvim-dap with node-debug2-adapter
- Configure launch.json equivalent in dap configuration
