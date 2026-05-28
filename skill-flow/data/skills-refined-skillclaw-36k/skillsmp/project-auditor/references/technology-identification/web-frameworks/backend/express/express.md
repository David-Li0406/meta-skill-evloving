# Express

**Category**: web-frameworks/backend
**Description**: Fast, unopinionated, minimalist web framework for Node.js
**Homepage**: https://www.npmjs.com/package/express

## Package Detection

### NPM
*Express framework package*

- `express`

### YARN
*Express via Yarn*

- `express`

### PNPM
*Express via pnpm*

- `express`

### Related Packages
- `express-validator`
- `express-session`
- `express-rate-limit`
- `express-async-handler`
- `body-parser`
- `morgan`
- `cors`
- `helmet`
- `compression`

## Import Detection

### Javascript
File extensions: .js, .mjs

**Pattern**: `const\s+express\s*=\s*require\(['"]express['"]\)`
- CommonJS require
- Example: `const express = require('express');`

**Pattern**: `import\s+express\s+from\s+['"]express['"]`
- ES6 default import
- Example: `import express from 'express';`

**Pattern**: `const\s+app\s*=\s*express\(\)`
- Express app initialization
- Example: `const app = express();`

**Pattern**: `app\.(get|post|put|delete|patch)\(['"]`
- Express route definition
- Example: `app.get('/api/users', handler);`

**Pattern**: `app\.use\(`
- Express middleware usage
- Example: `app.use(express.json());`

**Pattern**: `app\.listen\(`
- Express server start
- Example: `app.listen(3000, () => {});`

### Typescript
File extensions: .ts

**Pattern**: `import\s+express\s+from\s+['"]express['"]`
- ES6 import
- Example: `import express from 'express';`

**Pattern**: `import\s+\{\s*Request,\s*Response\s*\}\s+from\s+['"]express['"]`
- Express type imports
- Example: `import { Request, Response } from 'express';`

**Pattern**: `:\s*express\.Application`
- Express Application type
- Example: `const app: express.Application = express();`

## Environment Variables

*Server port configuration*

- `PORT`
- `SERVER_PORT`
- `APP_PORT`
- `HTTP_PORT`
*Environment configuration*

- `NODE_ENV`
- `ENVIRONMENT`
- `ENV`
*Session management*

- `SESSION_SECRET`
- `COOKIE_SECRET`
*CORS configuration*

- `CORS_ORIGIN`
- `ALLOWED_ORIGINS`
*Rate limiting*

- `RATE_LIMIT`
- `MAX_REQUESTS`

## Configuration Files

- `app.js`
- `server.js`
- `index.js`
- `src/app.js`
- `src/server.js`
- `routes/*.js`
- `routes/**/*.js`
- `api/*.js`
- `controllers/*.js`
- `middleware/*.js`
- `middlewares/*.js`

## Detection Notes

- Often used with body-parser, morgan, cors middleware
- Check for app.listen(), app.get(), app.post() patterns
- Look for require('express')() pattern

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 65% (MEDIUM)
