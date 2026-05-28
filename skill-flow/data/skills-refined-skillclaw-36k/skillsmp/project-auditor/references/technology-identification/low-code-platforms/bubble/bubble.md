# Bubble

**Category**: low-code-platforms
**Description**: Visual programming platform for building web applications without code
**Homepage**: https://bubble.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Bubble-related packages*

- `bubble-sdk` - Bubble SDK (if available)
- `@bubble.io/sdk` - Official SDK (if available)

---

## TIER 2: Deep Detection (File-based)

### Code Patterns

**Pattern**: `bubble\.io|\.bubbleapps\.io`
- Bubble platform URLs
- Example: `https://myapp.bubbleapps.io`

**Pattern**: `bubble_api_key|BUBBLE_API_KEY`
- Bubble API key references
- Example: `BUBBLE_API_KEY=...`

**Pattern**: `wf-api-version|X-Bubble-`
- Bubble API headers
- Example: `X-Bubble-Api-Token: ...`

**Pattern**: `bubbleapps\.io/api/[0-9.]+/wf/`
- Bubble workflow API endpoints
- Example: `https://myapp.bubbleapps.io/api/1.1/wf/`

---

## Environment Variables

- `BUBBLE_API_KEY` - Bubble Data API key
- `BUBBLE_APP_NAME` - Application name
- `BUBBLE_API_VERSION` - API version to use

## Detection Notes

- Bubble is primarily a hosted no-code platform
- Code detection focuses on API integrations
- Look for bubbleapps.io domain references
- Bubble plugins may expose JavaScript code
- Custom backend workflows use specific API patterns

---

## Secrets Detection

### API Keys

#### Bubble API Key
**Pattern**: `(?:bubble|BUBBLE).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-f0-9]{32,})['"]?`
**Severity**: high
**Description**: Bubble Data API key for backend access
**Example**: `BUBBLE_API_KEY=abc123def456789...`

### Validation

#### API Documentation
- **Data API**: https://manual.bubble.io/core-resources/api/data-api
- **Workflow API**: https://manual.bubble.io/core-resources/api/workflow-api
