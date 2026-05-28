# Sentry

**Category**: monitoring
**Description**: Sentry error tracking and performance monitoring
**Homepage**: https://sentry.io

## Package Detection

### NPM
*Sentry JavaScript SDKs*

- `@sentry/node`
- `@sentry/browser`
- `@sentry/react`
- `@sentry/nextjs`
- `@sentry/vue`
- `@sentry/angular`

### PYPI
*Sentry Python SDK*

- `sentry-sdk`

### RUBYGEMS
*Sentry Ruby SDKs*

- `sentry-ruby`
- `sentry-rails`
- `sentry-sidekiq`

### MAVEN
*Sentry Java SDKs*

- `io.sentry:sentry`
- `io.sentry:sentry-spring-boot-starter`

### GO
*Sentry Go SDK*

- `github.com/getsentry/sentry-go`

### Related Packages
- `@sentry/tracing`
- `@sentry/profiling-node`
- `@sentry/integrations`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@sentry/(node|browser|react|nextjs|vue|angular)['"]`
- Type: esm_import

**Pattern**: `require\(['"]@sentry/(node|browser|react)['"]\)`
- Type: commonjs_require

**Pattern**: `import\s+\*\s+as\s+Sentry`
- Type: esm_import

### Python

**Pattern**: `import\s+sentry_sdk`
- Type: python_import

**Pattern**: `from\s+sentry_sdk`
- Type: python_import

### Go

**Pattern**: `"github\.com/getsentry/sentry-go"`
- Type: go_import

### Ruby

**Pattern**: `require\s+['"]sentry-ruby['"]`
- Type: ruby_require

## Environment Variables

*Sentry Data Source Name*

*Sentry authentication token for CLI/releases*

*Sentry organization slug*

*Sentry project slug*

*Environment name*

*Release version*

*Sentry DSN for Next.js public*


## Detection Notes

- Check for SENTRY_DSN environment variable
- Look for Sentry.init() calls in code
- Self-hosted option available

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
