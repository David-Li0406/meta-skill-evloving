# Backstage

**Category**: cncf
**Description**: Developer portal platform
**Homepage**: https://backstage.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Backstage Node.js packages*

- `@backstage/core-plugin-api` - Core plugin API
- `@backstage/core-components` - Core components
- `@backstage/catalog-model` - Catalog model
- `@backstage/plugin-catalog` - Catalog plugin
- `@backstage/plugin-scaffolder` - Scaffolder plugin
- `@backstage/plugin-techdocs` - TechDocs plugin
- `@backstage/backend-common` - Backend common
- `@backstage/create-app` - App generator
- `@backstage/cli` - Backstage CLI

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Backstage usage*

- `app-config.yaml` - Backstage app config
- `app-config.local.yaml` - Local config
- `app-config.production.yaml` - Production config
- `catalog-info.yaml` - Entity catalog info
- `mkdocs.yml` - TechDocs config

### Configuration Directories
*Known directories that indicate Backstage usage*

- `packages/app/` - Frontend app
- `packages/backend/` - Backend app
- `plugins/` - Custom plugins

### Code Patterns

**Pattern**: `@backstage/|backstage\.io`
- Backstage package references
- Example: `import { useApi } from '@backstage/core-plugin-api'`

**Pattern**: `kind:\s*(Component|API|Resource|System|Domain|Group|User|Location|Template)`
- Backstage catalog kinds
- Example: `kind: Component`

**Pattern**: `apiVersion:\s*backstage\.io/v[0-9]+`
- Backstage API version
- Example: `apiVersion: backstage.io/v1alpha1`

**Pattern**: `spec:\s*\n\s*type:\s*(service|website|library|documentation)`
- Backstage component types
- Example: `type: service`

**Pattern**: `backstage\s+(dev|build|start)`
- Backstage CLI commands
- Example: `backstage dev`

**Pattern**: `techdocs:|catalog:|scaffolder:|kubernetes:`
- Backstage config sections
- Example: `techdocs:\n  builder: 'local'`

**Pattern**: `createPlugin|createApiFactory|createRouteRef`
- Backstage plugin patterns
- Example: `createPlugin({ id: 'my-plugin' })`

**Pattern**: `providesApis:|consumesApis:|dependsOn:`
- Backstage entity relationships
- Example: `providesApis:\n  - my-api`

---

## Environment Variables

- `BACKSTAGE_BASE_URL` - Base URL
- `POSTGRES_HOST` - Database host
- `POSTGRES_USER` - Database user
- `GITHUB_TOKEN` - GitHub integration token
- `AUTH_GITHUB_CLIENT_ID` - GitHub OAuth client ID

## Detection Notes

- Software catalog for all services
- TechDocs for documentation
- Scaffolder for service templates
- Plugin-based architecture
- Common integrations: GitHub, GitLab, K8s

---

## Secrets Detection

### Credentials

#### GitHub Token
**Pattern**: `GITHUB_TOKEN\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: GitHub personal access token

#### OAuth Client Secret
**Pattern**: `clientSecret:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: OAuth client secret for authentication

#### Database Password
**Pattern**: `POSTGRES_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: PostgreSQL database password

---

## TIER 3: Configuration Extraction

### Entity Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Backstage entity name
- Extracts: `entity_name`
- Example: `name: my-service`

### Owner Extraction

**Pattern**: `owner:\s*['"]?([a-zA-Z0-9_/-]+)['"]?`
- Entity owner
- Extracts: `owner`
- Example: `owner: team-platform`

### Lifecycle Extraction

**Pattern**: `lifecycle:\s*['"]?(experimental|production|deprecated)['"]?`
- Entity lifecycle stage
- Extracts: `lifecycle`
- Example: `lifecycle: production`
