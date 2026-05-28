# Cloudflare

**Category**: cloud-providers
**Description**: Cloudflare Workers, R2, KV, and edge services
**Homepage**: https://www.cloudflare.com

## Package Detection

### NPM
*Cloudflare Workers tooling*

- `wrangler`
- `@cloudflare/workers-types`
- `@cloudflare/kv-asset-handler`
- `miniflare`

### PYPI
*Cloudflare Python SDK*

- `cloudflare`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@cloudflare/`
- Type: esm_import

**Pattern**: `require\(['"]wrangler['"]`
- Type: commonjs_require

## Environment Variables

*Cloudflare API token*

*Cloudflare account ID*

*Cloudflare API token (short)*

*Cloudflare zone ID*


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
