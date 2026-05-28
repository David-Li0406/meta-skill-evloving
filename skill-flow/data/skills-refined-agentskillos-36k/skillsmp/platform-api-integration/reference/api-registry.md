# RSP API Registry

This document provides a quick reference for all known Rubin Science Platform (RSP) APIs and their OpenAPI specifications.

## Primary APIs

| Service | Path Prefix | OpenAPI Spec | Purpose | Documentation |
|---------|-------------|--------------|---------|---------------|
| **Gafaelfawr** | `/auth/` | https://gafaelfawr.lsst.io/_static/openapi.json | Authentication, user management, token operations | https://gafaelfawr.lsst.io |
| **Times Square** | `/times-square/api/` | https://times-square.lsst.io/_static/openapi.json | Notebook execution, parameterization, rendering | https://times-square.lsst.io |

## API Details

### Gafaelfawr

**Purpose:** Authentication and authorization service for the Rubin Science Platform

**Key Features:**
- User authentication and profile management
- OAuth 2.0 token management
- Scope-based authorization
- CSRF protection for mutations
- Token lifecycle management

**Common Endpoints:**
- `GET /auth/api/v1/user-info` - Get authenticated user information
- `GET /auth/api/v1/login` - Get CSRF token and available scopes
- `GET /auth/api/v1/users/{username}/tokens` - List user's tokens
- `POST /auth/api/v1/users/{username}/tokens` - Create new token
- `DELETE /auth/api/v1/users/{username}/tokens/{key}` - Delete token
- `GET /auth/api/v1/users/{username}/token-change-history` - Token change history

**Authentication:**
- Cookie-based session authentication (automatic)
- CSRF tokens required for POST/DELETE operations
- Tokens have scoped permissions

**Implementation Examples:**
- `apps/squareone/src/hooks/useUserInfo.ts`
- `apps/squareone/src/hooks/useLoginInfo.ts`
- `apps/squareone/src/hooks/useUserTokens.ts`
- `apps/squareone/src/hooks/useTokenCreation.ts`
- `apps/squareone/src/hooks/useDeleteToken.ts`
- `apps/squareone/src/hooks/useTokenChangeHistory.ts`

### Times Square

**Purpose:** Parameterized Jupyter notebook execution and rendering service

**Key Features:**
- Execute notebooks with URL parameters
- Real-time rendering status via SSE
- GitHub integration for notebook source
- HTML and JSON rendering outputs
- Display settings customization

**Common Endpoints:**
- `GET /times-square/api/v1/pages` - List all available pages
- `GET /times-square/api/v1/pages/{page}` - Get page metadata
- `GET /times-square/api/v1/pages/{page}/html` - Get rendered HTML output
- `GET /times-square/api/v1/pages/{page}/htmlstatus` - Check rendering status
- `GET /times-square/api/v1/pages/{page}/htmlevents` - SSE stream for real-time updates
- `GET /times-square/api/v1/github` - GitHub integration information

**Authentication:**
- Cookie-based session authentication (via Gafaelfawr)
- No explicit tokens required
- No CSRF tokens needed for GET requests

**Implementation Examples:**
- `apps/squareone/src/hooks/useTimesSquarePage.ts`
- `apps/squareone/src/components/TimesSquareNotebookViewer/useHtmlStatus.ts`
- `apps/squareone/src/contexts/TimesSquareUrlParametersContext.tsx`
- `apps/squareone/src/contexts/TimesSquareHtmlEventsContext.tsx`

## OpenAPI Specification Pattern

Most RSP services follow this pattern for OpenAPI specs:

```
https://{service}.lsst.io/_static/openapi.json
```

For example:
- Gafaelfawr: `https://gafaelfawr.lsst.io/_static/openapi.json`
- Times Square: `https://times-square.lsst.io/_static/openapi.json`

## How to Use OpenAPI Specs

### 1. Download with WebFetch

Use Claude's WebFetch tool to retrieve and explore the specification:

```typescript
WebFetch({
  url: 'https://gafaelfawr.lsst.io/_static/openapi.json',
  prompt: 'Show me all endpoints for token management'
})
```

### 2. Find Endpoint Details

Query the specification for specific information:
- "What parameters does this endpoint accept?"
- "What is the response schema for this endpoint?"
- "What authentication is required?"
- "What HTTP methods are supported?"

### 3. Generate TypeScript Types

Extract schema definitions and convert them to TypeScript types for use in your hooks and components.

## Configuration in Squareone

### Runtime URLs

API base URLs are configured in `squareone.config.yaml`:

```yaml
# Development
timesSquareUrl: 'http://localhost:3000/times-square/api'

# Production
# timesSquareUrl: 'https://data.lsst.cloud/times-square/api'
```

Access via AppConfig:

```typescript
const config = useAppConfig();
const timesSquareUrl = config.timesSquareUrl;
```

### Development Rewrites

For local development, `next.config.js` includes rewrites to mock API endpoints:

```javascript
async rewrites() {
  return [
    {
      source: '/auth/api/v1/:path*',
      destination: '/api/dev/auth/v1/:path*',
    },
    {
      source: '/times-square/api/v1/:path*',
      destination: '/api/dev/times-square/v1/:path*',
    },
  ];
}
```

## Adding New APIs

When a new RSP service is added:

1. **Add to this registry** with OpenAPI spec URL
2. **Create mock endpoints** in `/pages/api/dev/`
3. **Set up rewrites** in `next.config.js`
4. **Create custom hooks** following SWR pattern
5. **Add TypeScript types** from OpenAPI schemas
6. **Document in SKILL.md** with integration patterns

## API Versioning

RSP APIs follow versioned URL patterns:

- `/api/v1/` - Version 1 (current)
- `/api/v2/` - Version 2 (future)

When APIs are updated:
- New versions are added alongside existing versions
- Breaking changes require new version
- Deprecation notices provided before removal

## Related Documentation

- [SKILL.md](../SKILL.md) - Comprehensive integration guide
- [hook-template.tsx](../examples/hook-template.tsx) - Standard hook pattern
- **data-fetching-patterns** skill - SWR patterns and best practices
- **times-square-integration** skill - Times Square specific patterns
