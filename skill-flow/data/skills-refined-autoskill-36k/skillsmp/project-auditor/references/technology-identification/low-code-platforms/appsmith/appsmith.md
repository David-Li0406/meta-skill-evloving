# Appsmith

**Category**: low-code-platforms
**Description**: Open-source low-code platform for building internal tools
**Homepage**: https://appsmith.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Appsmith SDK and utilities*

- `@appsmith/cli` - Appsmith CLI tool
- `appsmith-cli` - Alternative CLI package

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Appsmith usage*

- `.appsmith/` - Appsmith project directory
- `appsmith.json` - Appsmith configuration
- `docker-compose.yml` - Often contains Appsmith services

### Code Patterns

**Pattern**: `appsmith\.com|app\.appsmith\.com`
- Appsmith URLs in code or config
- Example: `https://app.appsmith.com/applications`

**Pattern**: `APPSMITH_`
- Appsmith environment variables
- Example: `APPSMITH_ENCRYPTION_PASSWORD`

**Pattern**: `appsmith/appsmith`
- Appsmith Docker image reference
- Example: `image: appsmith/appsmith:latest`

---

## Environment Variables

- `APPSMITH_ENCRYPTION_PASSWORD` - Encryption password for credentials
- `APPSMITH_ENCRYPTION_SALT` - Encryption salt
- `APPSMITH_MONGODB_URI` - MongoDB connection string
- `APPSMITH_REDIS_URL` - Redis connection URL
- `APPSMITH_MAIL_ENABLED` - Enable email notifications
- `APPSMITH_MAIL_HOST` - SMTP host
- `APPSMITH_MAIL_PORT` - SMTP port
- `APPSMITH_MAIL_USERNAME` - SMTP username
- `APPSMITH_MAIL_PASSWORD` - SMTP password
- `APPSMITH_GOOGLE_MAPS_API_KEY` - Google Maps API key
- `APPSMITH_DISABLE_TELEMETRY` - Disable telemetry

## Detection Notes

- Appsmith is often self-hosted via Docker
- Look for appsmith Docker images in compose files
- MongoDB and Redis are required dependencies
- API endpoints often reference internal Appsmith URLs
- Custom widgets may have Appsmith-specific imports

---

## Secrets Detection

### API Keys

#### Appsmith API Key
**Pattern**: `APPSMITH_API_KEY\s*[=:]\s*['"]?([a-zA-Z0-9_-]{32,})['"]?`
**Severity**: high
**Description**: Appsmith API key for programmatic access
**Example**: `APPSMITH_API_KEY=abc123def456...`

#### Appsmith Encryption Password
**Pattern**: `APPSMITH_ENCRYPTION_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Master encryption password for stored credentials
**Example**: `APPSMITH_ENCRYPTION_PASSWORD=supersecret`
