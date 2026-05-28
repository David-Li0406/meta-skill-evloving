# Retool

**Category**: low-code-platforms
**Description**: Low-code platform for building internal tools and admin panels
**Homepage**: https://retool.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Retool SDK and utilities*

- `@retool/retool-cli` - Retool CLI for custom components
- `retool-sdk` - Retool SDK (if available)
- `@retool/custom-component-support` - Custom component library

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Retool usage*

- `retool.yaml` - Retool configuration
- `retool.json` - Retool configuration
- `.retool/` - Retool project directory
- `retool-custom-component.json` - Custom component config

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]@retool/`
- Retool SDK import
- Example: `import { useRetoolQuery } from '@retool/retool-sdk';`

### Code Patterns

**Pattern**: `retool\.io|app\.retool\.com`
- Retool URLs in code or config
- Example: `https://mycompany.retool.com/apps`

**Pattern**: `RETOOL_`
- Retool environment variables
- Example: `RETOOL_API_KEY`

---

## Environment Variables

- `RETOOL_API_KEY` - Retool API key for programmatic access
- `RETOOL_HOST` - Self-hosted Retool instance URL
- `RETOOL_LICENSE_KEY` - Enterprise license key
- `RETOOL_DB_HOST` - Database connection for self-hosted
- `RETOOL_DB_USER` - Database user
- `RETOOL_DB_PASSWORD` - Database password

## Detection Notes

- Retool is primarily a hosted platform with minimal code footprint
- Look for API endpoints calling retool.com or self-hosted URLs
- Custom components are the main code-detectable feature
- Self-hosted deployments have Docker/Kubernetes configurations

---

## Secrets Detection

### API Keys

#### Retool API Key
**Pattern**: `retool_api_[a-zA-Z0-9]{32,}`
**Severity**: high
**Description**: Retool API key for programmatic access
**Example**: `retool_api_abc123def456...`

#### Retool License Key
**Pattern**: `RETOOL_LICENSE_KEY\s*[=:]\s*['"]?([a-zA-Z0-9-]{36,})['"]?`
**Severity**: high
**Description**: Enterprise license key
**Context Required**: Near RETOOL or license references
