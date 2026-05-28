# API Versioning and Deprecation Patterns

**Category**: code-security/api-versioning
**Description**: Detect API versioning issues, deprecated endpoints, sunset APIs
**Purpose**: Audit API version lifecycle and deprecation status

---

## Version Detection

### OpenAPI Version Definition

**Type**: regex
**Severity**: info
**Pattern**: `[\"']?openapi[\"']?\s*:\s*[\"'](\d+\.\d+\.\d+)[\"']`
- OpenAPI specification version
- Example: `openapi: "3.0.3"`
- Captures: OpenAPI version

### API Info Version

**Type**: regex
**Severity**: info
**Pattern**: `info:\s*\n(?:\s*[^:]+:[^\n]+\n)*?\s*version:\s*[\"']?([^\"'\n]+)[\"']?`
- API version from OpenAPI spec
- Example: `version: "2.1.0"`
- Captures: API version

### URL Version Pattern

**Type**: regex
**Severity**: info
**Pattern**: `/(?:api/)?v(\d+)(?:\.\d+)?/`
- Version in URL path
- Example: `/api/v2/users`
- Captures: Major version

### Header Version Pattern

**Type**: regex
**Severity**: info
**Pattern**: `[\"']?(?:api-version|x-api-version)[\"']?\s*[:=]\s*[\"']?(\d+(?:\.\d+)?)[\"']?`
- API version in headers
- Example: `x-api-version: 2.1`

---

## Deprecated Endpoints

### Deprecated Annotation (Java)

**Type**: semgrep
**Severity**: medium
**Languages**: [java]
**Pattern**: |
  @Deprecated
  @$MAPPING("/$PATH")
  public $RET $METHOD(...) { ... }
- Endpoint marked as deprecated
- Example: `@Deprecated @GetMapping("/users")`

### Deprecated Annotation (Python)

**Type**: semgrep
**Severity**: medium
**Languages**: [python]
**Pattern**: |
  @deprecated(...)
  @app.$METHOD("/$PATH")
  def $FUNC(...): ...
- Python deprecated endpoint decorator
- Check for deprecation library usage

### Deprecated Comment Marker

**Type**: regex
**Severity**: low
**Pattern**: `(?i)(?://|#|/\*)\s*(?:deprecated|sunset|legacy|obsolete|to.?be.?removed)`
- Code comment indicating deprecation
- Example: `// DEPRECATED: use /api/v2/users instead`

### Express Deprecated Route

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)app\.(get|post|put|delete)\s*\(\s*['"]/(?:api/)?(?:v[01]/|legacy/|deprecated/|old/)`
- Explicitly deprecated or legacy routes
- Example: `app.get('/api/legacy/users', ...)`

### Sunset Header

**Type**: regex
**Severity**: high
**Pattern**: `[\"']?sunset[\"']?\s*[:=]\s*[\"']([^\"']+)[\"']`
- Sunset header indicating deprecation date
- Example: `Sunset: Sat, 31 Dec 2024 23:59:59 GMT`
- Captures: Sunset date

### Deprecation Header

**Type**: regex
**Severity**: medium
**Pattern**: `[\"']?deprecation[\"']?\s*[:=]\s*[\"']([^\"']+)[\"']`
- Deprecation header with date
- Example: `Deprecation: true`

---

## Version Lifecycle Issues

### Old API Version (v0)

**Type**: regex
**Severity**: high
**Pattern**: `/api/v0/`
- Version 0 APIs are typically pre-release
- Example: `/api/v0/experimental`
- Review for production readiness

### Old API Version (v1 with v3+ exists)

**Type**: regex
**Severity**: medium
**Pattern**: `/api/v1/`
- Legacy v1 endpoint
- Check if newer versions exist
- Review migration timeline

### Version Gap

**Type**: regex
**Severity**: low
**Pattern**: `/api/v[4-9]\d*/`
- High version number may indicate version skipping
- Review versioning strategy

### Date-Based Version

**Type**: regex
**Severity**: info
**Pattern**: `/api/(\d{4}-\d{2}-\d{2})/`
- Date-based API versioning
- Example: `/api/2024-01-15/`
- Captures: API date version

### Missing Version

**Type**: regex
**Severity**: medium
**Pattern**: `app\.(get|post|put|delete)\s*\(\s*['"]/api/(?!v\d)([^'"]+)['"]`
- Unversioned API endpoint
- Example: `/api/users` without version
- Recommendation: Add version prefix

---

## Breaking Change Indicators

### Response Schema Change Comment

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)(?://|#)\s*(?:breaking|schema.?change|response.?change|removed.?field)`
- Comment indicating breaking change
- Review backward compatibility

### Field Removal

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)(?://|#)\s*(?:removed|deleted|dropped)\s*(?:field|property|attribute)`
- Removed field indicator
- Example: `// removed field: legacyId`

### Endpoint Removal

**Type**: regex
**Severity**: high
**Pattern**: `(?i)(?://|#)\s*(?:removed|deleted|deprecated)\s*(?:endpoint|route|api)`
- Removed endpoint indicator
- Example: `// deprecated endpoint - use /v2/users`

---

## Documentation Indicators

### Deprecation Notice in Docs

**Type**: regex
**Severity**: info
**Pattern**: `(?i)(?:\*\*|##)\s*deprecated`
- Deprecation notice in markdown docs
- Example: `## Deprecated` or `**Deprecated**`

### Migration Guide Reference

**Type**: regex
**Severity**: info
**Pattern**: `(?i)migration|upgrade|transition.?(?:guide|doc|path)`
- Reference to migration documentation
- Example: `See migration guide for v2 upgrade`

### Sunset Date in Docs

**Type**: regex
**Severity**: high
**Pattern**: `(?i)sunset(?:ting)?\s*(?:on|date|by)?\s*:?\s*(\d{4}[-/]\d{2}[-/]\d{2}|\w+\s+\d{1,2},?\s+\d{4})`
- Sunset date mentioned in documentation
- Example: `Sunsetting on: 2024-12-31`
- Captures: Sunset date

---

## API Lifecycle Annotations

### OpenAPI Deprecated Flag

**Type**: regex
**Severity**: medium
**Pattern**: `deprecated:\s*true`
- OpenAPI deprecated operation flag
- Example: `deprecated: true`

### OpenAPI Extension x-sunset

**Type**: regex
**Severity**: high
**Pattern**: `x-sunset:\s*[\"']?([^\"'\n]+)[\"']?`
- Custom sunset extension in OpenAPI
- Example: `x-sunset: "2024-12-31"`
- Captures: Sunset date

### OpenAPI Extension x-deprecation-date

**Type**: regex
**Severity**: medium
**Pattern**: `x-deprecation-date:\s*[\"']?([^\"'\n]+)[\"']?`
- Custom deprecation date extension
- Example: `x-deprecation-date: "2024-06-01"`
- Captures: Deprecation date

---

## Version Configuration

### API Version Environment Variable

**Type**: regex
**Severity**: info
**Pattern**: `(?:API_VERSION|VERSION|API_V)\s*[:=]\s*[\"']?([^\"'\s]+)[\"']?`
- API version configuration
- Example: `API_VERSION=v2`
- Captures: Version value

### Default Version Configuration

**Type**: regex
**Severity**: info
**Pattern**: `(?i)default.?version\s*[:=]\s*[\"']?([^\"'\s]+)[\"']?`
- Default API version setting
- Example: `defaultVersion: 'v2'`

---

## Detection Confidence

**Version Detection**: 95%
**Deprecation Detection**: 85%
**Sunset Detection**: 80%
**Breaking Change Detection**: 70%

---

## References

- RFC 8594: The Sunset HTTP Header Field
- IETF Deprecation Header
- OpenAPI Specification (deprecated flag)
- Semantic Versioning
- API Versioning Best Practices
