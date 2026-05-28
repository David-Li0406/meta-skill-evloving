# PostHog

**Category**: business-tools/analytics
**Homepage**: https://posthog.com

## Package Detection

### NPM
*PostHog JavaScript/Node.js SDKs*

- `posthog-js`
- `posthog-node`

### PYPI
*PostHog Python SDK*

- `posthog`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]posthog-js['"]`
- Type: esm_import

**Pattern**: `from\s+['"]posthog-node['"]`
- Type: esm_import

### Python

**Pattern**: `from\s+posthog`
- Type: python_import

## Environment Variables


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
