# Fastify

**Category**: web-frameworks/backend
**Description**: Fast and low overhead web framework for Node.js - Up to 2x faster than Express

## Package Detection

### NPM
- `fastify`

### Related Packages
- `@fastify/autoload`
- `@fastify/jwt`
- `@fastify/cors`
- `@fastify/helmet`
- `@fastify/rate-limit`
- `@fastify/swagger`
- `fastify-plugin`

## Import Detection

### Javascript
File extensions: .js, .ts

**Pattern**: `import.*fastify|require\(['"]fastify['"]\)`
- Fastify framework import
- Example: `import Fastify from 'fastify';`

**Pattern**: `fastify\(\{|fastify\(\)`
- Fastify instance creation
- Example: `const app = fastify({ logger: true });`

**Pattern**: `\.register\(|fastify-plugin`
- Fastify plugin registration
- Example: `app.register(somePlugin);`

### Common Imports
- `fastify`
- `@fastify/autoload`
- `fastify-plugin`

## Environment Variables

*Common Fastify environment variables*

- `FASTIFY_PORT`
- `FASTIFY_ADDRESS`
- `FASTIFY_LOGGER`

## Configuration Files

- `fastify.config.js`
- `app.js`
- `server.js`

## Detection Notes

- Fastify is focused on performance
- Plugin-based architecture
- Built-in TypeScript support

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 50% (MEDIUM)
- **API Endpoint Detection**: 60% (MEDIUM)
