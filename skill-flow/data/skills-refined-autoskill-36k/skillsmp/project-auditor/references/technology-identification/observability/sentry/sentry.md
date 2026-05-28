# Sentry

**Category**: observability
**Description**: Application monitoring and error tracking platform
**Homepage**: https://sentry.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Sentry JavaScript SDKs*

- `@sentry/browser` - Browser SDK
- `@sentry/node` - Node.js SDK
- `@sentry/react` - React SDK
- `@sentry/vue` - Vue.js SDK
- `@sentry/angular` - Angular SDK
- `@sentry/nextjs` - Next.js SDK
- `@sentry/remix` - Remix SDK
- `@sentry/svelte` - Svelte SDK
- `@sentry/gatsby` - Gatsby SDK
- `@sentry/serverless` - Serverless SDK
- `@sentry/electron` - Electron SDK
- `@sentry/react-native` - React Native SDK
- `@sentry/capacitor` - Capacitor SDK
- `@sentry/profiling-node` - Node.js profiling
- `@sentry/tracing` - Distributed tracing (legacy)
- `@sentry/integrations` - Additional integrations
- `@sentry/webpack-plugin` - Webpack source maps plugin
- `@sentry/vite-plugin` - Vite source maps plugin
- `@sentry/esbuild-plugin` - esbuild plugin
- `@sentry/rollup-plugin` - Rollup plugin
- `raven` - Legacy Sentry SDK (deprecated)
- `raven-js` - Legacy browser SDK (deprecated)

#### PYPI
*Sentry Python SDKs*

- `sentry-sdk` - Official Python SDK
- `raven` - Legacy Python SDK (deprecated)
- `sentry-sdk[flask]` - Flask integration
- `sentry-sdk[django]` - Django integration
- `sentry-sdk[celery]` - Celery integration
- `sentry-sdk[sqlalchemy]` - SQLAlchemy integration
- `sentry-sdk[tornado]` - Tornado integration
- `sentry-sdk[fastapi]` - FastAPI integration
- `sentry-sdk[starlette]` - Starlette integration
- `sentry-sdk[aiohttp]` - aiohttp integration
- `sentry-sdk[bottle]` - Bottle integration
- `sentry-sdk[falcon]` - Falcon integration
- `sentry-sdk[pyramid]` - Pyramid integration
- `sentry-sdk[httpx]` - HTTPX integration

#### GO
*Sentry Go SDK*

- `github.com/getsentry/sentry-go` - Official Go SDK
- `github.com/getsentry/raven-go` - Legacy Go SDK (deprecated)

#### MAVEN
*Sentry Java SDKs*

- `io.sentry:sentry` - Core Java SDK
- `io.sentry:sentry-spring-boot-starter` - Spring Boot starter
- `io.sentry:sentry-spring-boot-starter-jakarta` - Spring Boot 3+ starter
- `io.sentry:sentry-spring` - Spring integration
- `io.sentry:sentry-logback` - Logback integration
- `io.sentry:sentry-log4j2` - Log4j2 integration
- `io.sentry:sentry-jul` - Java Util Logging integration
- `io.sentry:sentry-servlet` - Servlet integration
- `io.sentry:sentry-android` - Android SDK
- `io.sentry:sentry-apollo` - Apollo GraphQL integration

#### RUBYGEMS
*Sentry Ruby SDKs*

- `sentry-ruby` - Core Ruby SDK
- `sentry-rails` - Rails integration
- `sentry-sidekiq` - Sidekiq integration
- `sentry-resque` - Resque integration
- `sentry-delayed_job` - Delayed Job integration
- `sentry-raven` - Legacy SDK (deprecated)

#### NUGET
*Sentry .NET SDKs*

- `Sentry` - Core .NET SDK
- `Sentry.AspNetCore` - ASP.NET Core integration
- `Sentry.Extensions.Logging` - Microsoft.Extensions.Logging integration
- `Sentry.Serilog` - Serilog integration
- `Sentry.NLog` - NLog integration
- `Sentry.Log4Net` - Log4Net integration
- `Sentry.EntityFramework` - Entity Framework integration
- `Sentry.Maui` - .NET MAUI integration

#### CARGO
*Sentry Rust SDK*

- `sentry` - Official Rust SDK
- `sentry-actix` - Actix integration
- `sentry-tower` - Tower integration
- `sentry-tracing` - Tracing integration

#### PACKAGIST
*Sentry PHP SDKs*

- `sentry/sentry` - Core PHP SDK
- `sentry/sentry-laravel` - Laravel integration
- `sentry/sentry-symfony` - Symfony integration

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Sentry usage*

- `.sentryclirc` - Sentry CLI configuration
- `sentry.properties` - Sentry properties file
- `sentry.client.config.js` - Next.js client config
- `sentry.server.config.js` - Next.js server config
- `sentry.edge.config.js` - Next.js edge config
- `sentry.client.config.ts` - TypeScript client config
- `sentry.server.config.ts` - TypeScript server config

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`, `.mjs`

**Pattern**: `from\s+['"]@sentry/`
- Sentry SDK ES6 import
- Example: `import * as Sentry from '@sentry/browser';`

**Pattern**: `require\(['"]@sentry/`
- Sentry SDK CommonJS require
- Example: `const Sentry = require('@sentry/node');`

**Pattern**: `Sentry\.init\(`
- Sentry initialization
- Example: `Sentry.init({ dsn: '...' });`

**Pattern**: `Sentry\.captureException\(|Sentry\.captureMessage\(`
- Sentry error capture
- Example: `Sentry.captureException(error);`

#### Python
Extensions: `.py`

**Pattern**: `^import\s+sentry_sdk`
- sentry-sdk import
- Example: `import sentry_sdk`

**Pattern**: `^from\s+sentry_sdk\s+import`
- sentry-sdk from import
- Example: `from sentry_sdk import capture_exception`

**Pattern**: `sentry_sdk\.init\(`
- Sentry initialization
- Example: `sentry_sdk.init(dsn="...")`

**Pattern**: `sentry_sdk\.capture_exception\(`
- Exception capture
- Example: `sentry_sdk.capture_exception(e)`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/getsentry/sentry-go"`
- Sentry Go SDK import
- Example: `import sentry "github.com/getsentry/sentry-go"`

**Pattern**: `sentry\.Init\(`
- Sentry Go initialization
- Example: `sentry.Init(sentry.ClientOptions{...})`

#### Ruby
Extensions: `.rb`

**Pattern**: `require\s+['"]sentry-ruby['"]`
- Sentry Ruby require
- Example: `require 'sentry-ruby'`

**Pattern**: `Sentry\.init`
- Sentry Ruby initialization
- Example: `Sentry.init { |config| ... }`

#### Java
Extensions: `.java`

**Pattern**: `import\s+io\.sentry\.`
- Sentry Java import
- Example: `import io.sentry.Sentry;`

**Pattern**: `Sentry\.init\(`
- Sentry Java initialization
- Example: `Sentry.init(options -> { ... });`

### Code Patterns

**Pattern**: `dsn\s*[=:]\s*['"]https://[a-f0-9]+@[a-z0-9.]*sentry\.io/[0-9]+['"]`
- Sentry DSN configuration
- Example: `dsn: "https://abc123@o456.ingest.sentry.io/789"`

**Pattern**: `SENTRY_DSN\s*[=:]\s*['"]?https://`
- Sentry DSN environment variable
- Example: `SENTRY_DSN=https://...`

---

## Environment Variables

- `SENTRY_DSN` - Data Source Name (primary config)
- `SENTRY_ENVIRONMENT` - Environment name (prod, staging, etc.)
- `SENTRY_RELEASE` - Release/version identifier
- `SENTRY_AUTH_TOKEN` - Authentication token for API/CLI
- `SENTRY_ORG` - Organization slug
- `SENTRY_PROJECT` - Project slug
- `SENTRY_URL` - Self-hosted Sentry URL
- `SENTRY_TRACES_SAMPLE_RATE` - Performance monitoring sample rate
- `SENTRY_PROFILES_SAMPLE_RATE` - Profiling sample rate
- `SENTRY_DEBUG` - Enable debug mode
- `SENTRY_LOG_LEVEL` - SDK log level

## Detection Notes

- DSN (Data Source Name) is the primary configuration - always present
- Look for `@sentry/*` packages in package.json
- Framework-specific packages indicate integration depth
- Source map plugins indicate production error tracking
- Performance monitoring uses tracing packages
- Legacy `raven` packages indicate older installations needing update

---

## Secrets Detection

### API Keys and Tokens

#### Sentry DSN
**Pattern**: `https://([a-f0-9]{32})@([a-z0-9]+)(?:\.ingest)?\.sentry\.io/([0-9]+)`
**Severity**: medium
**Description**: Sentry Data Source Name - used to send events (public key)
**Example**: `https://abc123def456...@o789.ingest.sentry.io/123456`
**Note**: DSN contains a public key, not a secret - safe to expose in client-side code

#### Sentry Auth Token
**Pattern**: `sntrys_[A-Za-z0-9_]{64,}`
**Severity**: critical
**Description**: Sentry authentication token for API access
**Example**: `sntrys_eyJpYXQiOjE2...`

#### Legacy Sentry Auth Token
**Pattern**: `(?:SENTRY_AUTH_TOKEN|sentry[_-]?auth[_-]?token)\s*[=:]\s*['"]?([a-f0-9]{64})['"]?`
**Severity**: critical
**Description**: Legacy Sentry auth token format
**Example**: `SENTRY_AUTH_TOKEN=abc123def456...`

### Validation

#### API Documentation
- **API Reference**: https://docs.sentry.io/api/
- **Authentication**: https://docs.sentry.io/api/auth/

#### Validation Endpoint
**API**: List Projects
**Endpoint**: `https://sentry.io/api/0/projects/`
**Method**: GET
**Headers**: `Authorization: Bearer {auth_token}`
**Purpose**: Validates auth token and returns accessible projects

```bash
# Validate Sentry auth token
curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
     "https://sentry.io/api/0/projects/"
```

---

## TIER 3: Configuration Extraction

### DSN Component Extraction

**Pattern**: `https://([a-f0-9]+)@([a-z0-9.]+)\.sentry\.io/([0-9]+)`
- Sentry DSN components
- Extracts: `public_key`, `host`, `project_id`
- Example: `https://abc123@o456.ingest.sentry.io/789123`

### Organization/Project Extraction

**Pattern**: `(?:SENTRY_ORG|sentry[_.]org(?:anization)?)\s*[=:]\s*['"]?([a-z0-9-]+)['"]?`
- Organization slug
- Extracts: `org_slug`
- Example: `SENTRY_ORG=my-company`

**Pattern**: `(?:SENTRY_PROJECT|sentry[_.]project)\s*[=:]\s*['"]?([a-z0-9-]+)['"]?`
- Project slug
- Extracts: `project_slug`
- Example: `SENTRY_PROJECT=backend-api`

### Release Extraction

**Pattern**: `(?:SENTRY_RELEASE|release)\s*[=:]\s*['"]?([^'"}\s]+)['"]?`
- Release identifier
- Extracts: `release_version`
- Example: `SENTRY_RELEASE=v1.2.3`
