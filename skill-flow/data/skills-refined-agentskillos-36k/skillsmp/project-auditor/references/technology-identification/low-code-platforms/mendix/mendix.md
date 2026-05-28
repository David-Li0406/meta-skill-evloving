# Mendix

**Category**: low-code-platforms
**Description**: Enterprise low-code platform by Siemens
**Homepage**: https://mendix.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Mendix-related packages*

- `@mendix/pluggable-widgets-tools` - Mendix widget development tools
- `@mendix/widget-plugin-test-utils` - Testing utilities
- `mendix-client` - Mendix JavaScript client

#### MAVEN
*Mendix Java SDK*

- `com.mendix:mendix-api` - Mendix API
- `com.mendix:mendix-tools` - Mendix tools

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Mendix usage*

- `*.mpk` - Mendix project package
- `*.mpr` - Mendix project file
- `mendix.yml` - Mendix CI/CD configuration
- `m2ee.yaml` - Mendix runtime configuration
- `model/` - Mendix model directory

### Code Patterns

**Pattern**: `mendix\.com|mendixcloud\.com`
- Mendix platform URLs
- Example: `https://myapp.mendixcloud.com`

**Pattern**: `MENDIX_`
- Mendix environment variables
- Example: `MENDIX_API_KEY`

**Pattern**: `mx\.|mendix\.|Mendix\.`
- Mendix SDK/API references
- Example: `mx.data.get(...)`

**Pattern**: `/xas/|/mxruntime/`
- Mendix runtime endpoints
- Example: `https://app.mendixcloud.com/xas/`

---

## Environment Variables

- `MENDIX_API_KEY` - Mendix Platform API key
- `MENDIX_USERNAME` - Mendix account username
- `MENDIX_PASSWORD` - Mendix account password
- `MENDIX_APP_ID` - Application ID
- `M2EE_ADMIN_PORT` - Admin port for runtime
- `M2EE_ADMIN_PASS` - Admin password
- `DATABASE_URL` - Database connection string
- `BUILDPACK_XTRACE` - Enable debug mode

## Detection Notes

- Mendix uses proprietary .mpr and .mpk file formats
- Cloud deployments use mendixcloud.com
- Look for /xas/ endpoints for runtime APIs
- Custom widgets use @mendix packages
- M2EE is the Mendix runtime management tool

---

## Secrets Detection

### API Keys

#### Mendix Platform API Key
**Pattern**: `(?:mendix|MENDIX).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{32,})['"]?`
**Severity**: high
**Description**: Mendix Platform API key for deployments
**Example**: `MENDIX_API_KEY=abc123...`

#### M2EE Admin Password
**Pattern**: `M2EE_ADMIN_PASS(?:WORD)?\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Mendix runtime admin password
**Example**: `M2EE_ADMIN_PASS=secretpass`

### Validation

#### API Documentation
- **Platform APIs**: https://docs.mendix.com/apidocs-mxsdk/apidocs/
- **Deploy API**: https://docs.mendix.com/apidocs-mxsdk/apidocs/deploy-api/
