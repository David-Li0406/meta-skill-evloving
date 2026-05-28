# AppConfig Schema Reference

This document describes the complete AppConfig interface and the corresponding YAML configuration schema.

## AppConfig TypeScript Interface

```typescript
interface AppConfig {
  // Required fields
  siteName: string;
  baseUrl: string;
  environmentName: string;
  siteDescription: string;
  docsBaseUrl: string;
  timesSquareUrl: string;
  coManageRegistryUrl: string;
  enableAppsMenu: boolean;
  appLinks: Array<{
    label: string;
    href: string;
    internal: boolean;
  }>;
  showPreview: boolean;
  mdxDir: string;

  // Optional fields
  semaphoreUrl?: string;
  plausibleDomain?: string;
  previewLink?: string;

  // Sentry configuration (injected at runtime)
  sentryDsn?: string;
  sentryTracesSampleRate?: number;
  sentryReplaysSessionSampleRate?: number;
  sentryReplaysOnErrorSampleRate?: number;
  sentryDebug?: boolean;
}
```

## Configuration Fields

### Core Site Information

**siteName** (string, required)
- Display name for the site
- Used in page titles, headers, and branding
- Example: `'Rubin Science Platform'`

**baseUrl** (string, required)
- Base URL of the application
- Used for generating absolute URLs
- Example: `'https://data.lsst.cloud'`

**environmentName** (string, required)
- Environment identifier
- Common values: `'development'`, `'staging'`, `'production'`
- Can be used for conditional behavior/styling

**siteDescription** (string, required)
- Short description of the site
- Used in meta tags for SEO
- Can be multi-line YAML string

### Documentation and External Services

**docsBaseUrl** (string, required)
- Base URL for documentation site
- Example: `'https://rsp.lsst.io'`

**timesSquareUrl** (string, required)
- URL for Times Square API
- Example: `'https://data.lsst.cloud/times-square/api'`

**coManageRegistryUrl** (string, required)
- COmanage Registry URL for identity management
- Example: `'https://id.lsst.cloud'`

**semaphoreUrl** (string, optional)
- URL for Semaphore service
- Example: `'https://data.lsst.cloud/semaphore'`

**plausibleDomain** (string, optional)
- Domain for Plausible Analytics
- Example: `'data.lsst.cloud'`

### Application Menu

**enableAppsMenu** (boolean, required)
- Whether to show the applications menu
- Default: `true`

**appLinks** (array, required)
- List of application links to display in menu
- Each link has:
  - `label` (string): Display text
  - `href` (string): URL (relative or absolute)
  - `internal` (boolean): Whether link is internal to app

Example:
```yaml
appLinks:
  - label: 'Times Square'
    href: '/times-square/'
    internal: true
  - label: 'Argo CD'
    href: 'https://argo.example.com/'
    internal: false
```

### Preview Feature

**showPreview** (boolean, required)
- Whether to show preview/roadmap links
- Default: `false`

**previewLink** (string, optional)
- URL to preview/roadmap page
- Only used if `showPreview` is `true`

### Content Management

**mdxDir** (string, required)
- Directory containing MDX content files
- **Development**: Relative path like `'src/content/pages'`
- **Production**: Absolute path like `'/config/mdx'` for ConfigMap mounts

### Sentry Error Tracking

All Sentry fields are optional and typically injected at runtime from environment variables:

**sentryDsn** (string, optional)
- Sentry Data Source Name
- Injected from `process.env.SENTRY_DSN`

**sentryTracesSampleRate** (number, optional)
- Sample rate for performance monitoring (0.0 to 1.0)
- Example: `0.1` = 10% of transactions traced

**sentryReplaysSessionSampleRate** (number, optional)
- Sample rate for session replays (0.0 to 1.0)
- Example: `0.1` = 10% of normal sessions recorded

**sentryReplaysOnErrorSampleRate** (number, optional)
- Sample rate for replays when errors occur (0.0 to 1.0)
- Example: `1.0` = 100% of error sessions recorded

**sentryDebug** (boolean, optional)
- Enable Sentry debug logging
- Default: `false`

## Configuration File Locations

### Public Configuration (squareone.config.yaml)

Contains publicly accessible configuration that can be sent to the client.

**Default location**: `squareone.config.yaml` in app root
**Environment override**: `SQUAREONE_CONFIG_PATH`

Example:
```yaml
siteName: 'Rubin Science Platform'
baseUrl: 'https://data.lsst.cloud'
environmentName: 'production'
siteDescription: |
  The Rubin Science Platform provides access to
  LSST data products and computational resources.
docsBaseUrl: 'https://rsp.lsst.io'
timesSquareUrl: 'https://data.lsst.cloud/times-square/api'
coManageRegistryUrl: 'https://id.lsst.cloud'
enableAppsMenu: true
appLinks:
  - label: 'Times Square'
    href: '/times-square/'
    internal: true
showPreview: false
mdxDir: '/config/mdx'
```

### Server Configuration (squareone.serverconfig.yaml)

Contains server-only configuration (secrets, internal URLs).

**Default location**: `squareone.serverconfig.yaml` in app root
**Environment override**: `SQUAREONE_SERVER_CONFIG_PATH`

This file typically contains overrides or additional configuration that shouldn't be sent to the client.

## JSON Schema Files

Configuration is validated using JSON Schema with Ajv:

- **`squareone.config.schema.json`** - Schema for public config
- **`squareone.serverconfig.schema.json`** - Schema for server config

Schema features:
- **Default values** automatically applied
- **Additional properties** automatically removed
- **Type validation** enforced
- **Required fields** checked

## Environment Variable Overrides

Several configuration aspects can be overridden via environment variables:

| Environment Variable | Purpose |
|---------------------|---------|
| `SQUAREONE_CONFIG_PATH` | Override public config file path |
| `SQUAREONE_SERVER_CONFIG_PATH` | Override server config file path |
| `SQUAREONE_ENABLE_CACHING` | Force caching in development (true/false) |
| `SENTRY_DSN` | Sentry Data Source Name (injected into config) |
| `NODE_ENV` | Node environment (affects caching behavior) |

## Configuration Merging

When loading configuration:

1. Load `squareone.config.yaml` (public config)
2. Load `squareone.serverconfig.yaml` (server config)
3. Merge server config over public config (server config wins)
4. Inject environment-based values (like `SENTRY_DSN`)
5. Cache the result (in production)

This allows server config to override public config values when needed.

## Kubernetes ConfigMap Pattern

For Kubernetes deployments, configuration is typically split:

**ConfigMap for public config**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: squareone-config
data:
  squareone.config.yaml: |
    siteName: 'Rubin Science Platform'
    baseUrl: 'https://data.lsst.cloud'
    mdxDir: '/config/mdx'
    # ...
```

**Secret for sensitive config**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: squareone-secrets
stringData:
  squareone.serverconfig.yaml: |
    # Sensitive overrides if needed
```

**Deployment mounts**:
```yaml
volumeMounts:
  - name: config
    mountPath: /app/squareone.config.yaml
    subPath: squareone.config.yaml
  - name: secrets
    mountPath: /app/squareone.serverconfig.yaml
    subPath: squareone.serverconfig.yaml
  - name: mdx-content
    mountPath: /config/mdx
volumes:
  - name: config
    configMap:
      name: squareone-config
  - name: secrets
    secret:
      secretName: squareone-secrets
  - name: mdx-content
    configMap:
      name: squareone-mdx-content
```

This pattern allows configuration updates without rebuilding the container image.
