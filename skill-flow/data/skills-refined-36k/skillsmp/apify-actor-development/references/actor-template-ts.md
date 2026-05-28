# TypeScript Actor Template Reference

This document describes the complete TypeScript actor template structure that serves as the starting point for all TypeScript-based Apify actors.

## Template Overview

The TypeScript empty template provides a minimal, production-ready structure for building Apify actors in TypeScript. It includes:

- Basic Actor skeleton with ES modules and TypeScript support
- Proper project structure with src/ directory
- Docker multi-stage build for optimized images
- Dependency management with npm
- TypeScript compilation and type checking
- Code quality tools (ESLint, Prettier)
- Actor configuration files

## Complete File Structure

```
ts-empty/
├── .actor/
│   └── actor.json                    # Actor metadata and configuration
├── src/
│   └── main.ts                       # Main actor logic and entry point
├── dist/                             # Compiled JavaScript output (generated)
│   └── main.js
├── .dockerignore                     # Docker build exclusions
├── .editorconfig                     # Editor configuration
├── .gitignore                        # Git exclusions
├── .prettierrc                       # Prettier configuration
├── .prettierignore                   # Prettier exclusions
├── Dockerfile                        # Container image definition (multi-stage)
├── eslint.config.mjs                 # ESLint configuration
├── tsconfig.json                     # TypeScript configuration
├── package.json                      # NPM dependencies and scripts
├── README.md                         # Project documentation
└── AGENTS.md                         # Agent-specific documentation
```

## File-by-File Reference

### `.actor/actor.json`

Actor metadata and platform configuration.

```json
{
    "actorSpecification": 1,
    "name": "ts-empty",
    "title": "Empty TypeScript project",
    "description": "Empty project in TypeScript.",
    "version": "0.0",
    "buildTag": "latest",
    "meta": {
        "templateId": "ts-empty-from-agent",
        "generatedBy": "<FILL-IN-MODEL>"
    },
    "dockerfile": "../Dockerfile"
}
```

**Key fields:**
- `actorSpecification`: Always `1` (current spec version)
- `name`: Actor identifier (lowercase, hyphens)
- `title`: Human-readable name shown in UI
- `description`: Short description for marketplace
- `version`: Semantic version (e.g., "1.0.0")
- `buildTag`: Docker tag for builds (usually "latest")
- `meta.templateId`: Template identifier (use `"ts-empty-from-agent"` for agent-generated actors)
- `meta.generatedBy`: **CRITICAL** - Must be filled with model name (e.g., "claude-sonnet-4-5-20250929")
- `dockerfile`: Path to Dockerfile (relative to .actor/)

**Important:**
- Always update `generatedBy` with the current model name
- Use `"ts-empty-from-agent"` as templateId for agent-created actors
- Use semantic versioning for `version`
- `name` must be URL-safe (lowercase, hyphens only)

### `src/main.ts`

Main actor logic and entry point in TypeScript.

```typescript
// Apify SDK - toolkit for building Apify Actors (Read more at https://docs.apify.com/sdk/js/)
import { Actor, log } from 'apify';
// Crawlee - web scraping and browser automation library (Read more at https://crawlee.dev)
// import { CheerioCrawler } from '@crawlee/cheerio';

// this is ESM project, and as such, it requires you to specify extensions in your relative imports
// read more about this here: https://nodejs.org/docs/latest-v18.x/api/esm.html#mandatory-file-extensions
// note that we need to use `.js` even when inside TS files
// import { router } from './routes.js';

// The init() call configures the Actor for its environment. It's recommended to start every Actor with an init()
await Actor.init();

log.info('Hello from the Actor!');
/**
 * Actor code
 */

// Gracefully exit the Actor process. It's recommended to quit all Actors with an exit()
await Actor.exit();
```

**Key points:**
- Uses ES modules with TypeScript syntax
- Always start with `await Actor.init()` for proper initialization
- Always end with `await Actor.exit()` for graceful shutdown
- Use `log` from `apify` package (automatically censors sensitive data)
- Relative imports must include `.js` extension (not `.ts`) in ESM
- Top-level `await` is supported
- Compiled to JavaScript in `dist/` directory

**Common patterns with types:**

```typescript
import { Actor, log } from 'apify';

interface Input {
    startUrls: { url: string }[];
    maxItems?: number;
}

interface Product {
    url: string;
    title: string;
    price?: string;
}

await Actor.init();

// 1. Get input with type safety
const input = (await Actor.getInput<Input>()) || { startUrls: [] };
const { startUrls, maxItems = 100 } = input;

// 2. Process data
const results: Product[] = [];
for (const { url } of startUrls) {
    results.push({ url, title: 'Example' });
}

// 3. Save output
await Actor.pushData(results);

log.info(`Processed ${results.length} items`);

await Actor.exit();
```

### `package.json`

NPM dependencies and scripts configuration.

```json
{
    "name": "ts-empty",
    "version": "0.0.1",
    "type": "module",
    "description": "This is an example of an Apify Actor.",
    "engines": {
        "node": ">=18.0.0"
    },
    "dependencies": {
        "apify": "^3.5.2",
        "@crawlee/cheerio": "^3.15.3"
    },
    "devDependencies": {
        "@apify/eslint-config": "^1.0.0",
        "@apify/tsconfig": "^0.1.1",
        "@types/node": "^22.15.32",
        "eslint": "^9.29.0",
        "eslint-config-prettier": "^10.1.5",
        "globals": "^16.2.0",
        "prettier": "^3.5.3",
        "tsx": "^4.20.3",
        "typescript": "^5.9.3",
        "typescript-eslint": "^8.34.1"
    },
    "scripts": {
        "start": "npm run start:dev",
        "start:prod": "node dist/main.js",
        "start:dev": "tsx src/main.ts",
        "build": "tsc",
        "lint": "eslint",
        "lint:fix": "eslint --fix",
        "format": "prettier --write .",
        "format:check": "prettier --check .",
        "test": "echo \"Error: oops, the Actor has no tests yet, sad!\" && exit 1"
    },
    "author": "It's not you it's me",
    "license": "ISC"
}
```

**Key fields:**
- `type`: Must be `"module"` for ES modules support
- `engines.node`: Minimum Node.js version (18.0.0+)
- `dependencies`: Runtime dependencies
  - `apify`: Apify SDK for actor development
  - `@crawlee/cheerio`: HTTP scraping with Cheerio (optional)
- `devDependencies`: Development and build tools
  - `typescript`: TypeScript compiler
  - `tsx`: Fast TypeScript execution for development
  - `@types/node`: Node.js type definitions
  - `@apify/tsconfig`: Shared TypeScript configuration
  - ESLint and Prettier for code quality
- `scripts`: Common commands
  - `start`: Run in development mode (uses `tsx`)
  - `start:prod`: Run compiled JavaScript
  - `start:dev`: Run TypeScript directly with `tsx`
  - `build`: Compile TypeScript to JavaScript
  - `format`: Format code with Prettier
  - `lint`: Check code with ESLint
  - `lint:fix`: Auto-fix ESLint issues

**Common additional dependencies:**

```json
{
    "dependencies": {
        "apify": "^3.5.2",
        "@crawlee/cheerio": "^3.15.3",
        "@crawlee/playwright": "^3.15.3",
        "@crawlee/puppeteer": "^3.15.3",
        "axios": "^1.6.0"
    },
    "devDependencies": {
        "@types/cheerio": "^0.22.35"
    }
}
```

### `tsconfig.json`

TypeScript compiler configuration.

```json
{
    "extends": "@apify/tsconfig",
    "compilerOptions": {
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "target": "ES2022",
        "outDir": "dist",
        "noUnusedLocals": false,
        "skipLibCheck": true,
        "lib": ["DOM"]
    },
    "include": ["./src/**/*"]
}
```

**Key points:**
- Extends Apify's shared TypeScript configuration
- `module: "NodeNext"`: Modern ES modules support
- `moduleResolution: "NodeNext"`: Node.js module resolution
- `target: "ES2022"`: Compile to modern JavaScript
- `outDir: "dist"`: Output directory for compiled files
- `include`: Only compile files in `src/` directory
- `lib: ["DOM"]`: Include DOM type definitions for browser APIs

**Why `.js` extensions in imports:**
- TypeScript requires `.js` extensions in import paths for ESM
- Even though source files are `.ts`, imports reference the compiled `.js` output
- This is a TypeScript ESM requirement, not a mistake

### `Dockerfile`

Multi-stage Docker build for optimized TypeScript actors.

```dockerfile
# Specify the base Docker image. You can read more about
# the available images at https://docs.apify.com/sdk/js/docs/guides/docker-images
# You can also use any other image from Docker Hub.
FROM apify/actor-node:22 AS builder

# Check preinstalled packages
RUN npm ls @crawlee/core apify puppeteer playwright

# Copy just package.json and package-lock.json
# to speed up the build using Docker layer cache.
COPY --chown=myuser:myuser package*.json ./

# Install all dependencies. Don't audit to speed up the installation.
RUN npm install --include=dev --audit=false

# Next, copy the source files using the user set
# in the base image.
COPY --chown=myuser:myuser . ./

# Install all dependencies and build the project.
# Don't audit to speed up the installation.
RUN npm run build

# Create final image
FROM apify/actor-node:22

# Check preinstalled packages
RUN npm ls @crawlee/core apify puppeteer playwright

# Copy just package.json and package-lock.json
# to speed up the build using Docker layer cache.
COPY --chown=myuser:myuser package*.json ./

# Install NPM packages, skip optional and development dependencies to
# keep the image small. Avoid logging too much and print the dependency
# tree for debugging
RUN npm --quiet set progress=false \
    && npm install --omit=dev --omit=optional \
    && echo "Installed NPM packages:" \
    && (npm list --omit=dev --all || true) \
    && echo "Node.js version:" \
    && node --version \
    && echo "NPM version:" \
    && npm --version \
    && rm -r ~/.npm

# Copy built JS files from builder image
COPY --from=builder --chown=myuser:myuser /usr/src/app/dist ./dist

# Next, copy the remaining files and directories with the source code.
# Since we do this after NPM install, quick build will be really fast
# for most source file changes.
COPY --chown=myuser:myuser . ./

# Run the image.
CMD ["node", "dist/main.js"]
```

**Key points:**
- **Multi-stage build**: Compiles TypeScript in builder stage, runs JavaScript in final stage
- Uses official Apify Node.js base image (Node.js 22)
- Runs as non-root user (`myuser`) for security
- **Builder stage**:
  - Installs all dependencies (including devDependencies)
  - Compiles TypeScript with `npm run build`
- **Final stage**:
  - Only installs production dependencies
  - Copies compiled `dist/` from builder
  - Much smaller final image (no TypeScript, no build tools)
- Executes actor with `node dist/main.js` (compiled JavaScript)

**Available Node.js versions:**
- `apify/actor-node:22` (recommended)
- `apify/actor-node:20`
- `apify/actor-node:18`

**Build optimization:**
- Multi-stage build reduces final image size by ~40%
- TypeScript source not included in final image
- Only compiled JavaScript and runtime dependencies

### `eslint.config.mjs`

ESLint configuration for TypeScript code quality.

```javascript
import { defineConfig } from '@apify/eslint-config';

export default defineConfig({
    rules: {
        // Add your custom rules here
    },
});
```

**Key points:**
- Uses Apify's ESLint configuration with TypeScript support
- Configured for ES modules (`.mjs` extension)
- Includes TypeScript-specific rules
- Can be customized with additional rules
- Run with `npm run lint` or `npm run lint:fix`

### `.prettierrc`

Prettier configuration for code formatting.

```json
{
    "singleQuote": true,
    "trailingComma": "all",
    "printWidth": 120,
    "tabWidth": 4
}
```

**Key points:**
- Ensures consistent code formatting for TypeScript
- Same configuration as JavaScript template
- Run with `npm run format` or `npm run format:check`
- Integrates with ESLint via `eslint-config-prettier`

### `.prettierignore`

Files to exclude from Prettier formatting.

```
dist/
node_modules/
```

**Key points:**
- Excludes compiled JavaScript in `dist/`
- Excludes dependencies
- Ensures only source files are formatted

### `.editorconfig`

Editor configuration for consistent coding style.

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
```

**Key points:**
- Works across different editors and IDEs
- Ensures consistent indentation (4 spaces)
- Unix-style line endings (LF)
- Removes trailing whitespace

### `.dockerignore`

Files to exclude from Docker builds.

```
.git/
.github/
node_modules/
storage/
apify_storage/
dist/
.DS_Store
*.log
.env
```

**Key points:**
- Excludes version control (`.git/`)
- Excludes `node_modules/` (reinstalled in Docker)
- Excludes `dist/` (rebuilt in Docker)
- Excludes local storage directories
- Reduces Docker build context size

### `.gitignore`

Files to exclude from version control.

```
node_modules/
storage/
apify_storage/
dist/
.DS_Store
*.log
.env
```

**Key points:**
- Excludes dependencies (`node_modules/`)
- Excludes compiled output (`dist/`)
- Excludes local storage directories
- Includes `.env` to prevent committing secrets

## Using the Template

### Step 1: Copy Template Files

```bash
# Create new actor directory
mkdir my-new-actor
cd my-new-actor

# Copy all template files including hidden ones
cp -r /path/to/ts-empty/* .
cp -r /path/to/ts-empty/.* .
```

### Step 2: Update Actor Configuration

Edit `.actor/actor.json`:

```json
{
    "actorSpecification": 1,
    "name": "my-scraper",
    "title": "My Product Scraper",
    "description": "Scrapes products from e-commerce sites.",
    "version": "1.0.0",
    "buildTag": "latest",
    "meta": {
        "templateId": "ts-empty-from-agent",
        "generatedBy": "claude-sonnet-4-5-20250929"  // Update with current model
    },
    "dockerfile": "../Dockerfile"
}
```

### Step 3: Install Dependencies

```bash
npm install
```

### Step 4: Add Additional Dependencies (if needed)

```bash
# Runtime dependencies
npm install axios

# Type definitions
npm install --save-dev @types/cheerio
```

### Step 5: Implement Logic

Edit `src/main.ts`:

```typescript
import { Actor, log } from 'apify';
import { CheerioCrawler } from '@crawlee/cheerio';

interface Input {
    startUrls: { url: string }[];
    maxItems?: number;
}

interface Product {
    url: string;
    title: string;
    price: string;
}

await Actor.init();

// Get input with type safety
const input = (await Actor.getInput<Input>()) || { startUrls: [] };
const { startUrls, maxItems = 100 } = input;

// Create crawler
const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxItems,
    async requestHandler({ request, $ }) {
        log.info(`Processing ${request.url}`);

        // Extract data with type safety
        const products: Product[] = [];
        $('.product-item').each((i, el) => {
            const title = $(el).find('.product-name').text().trim();
            const price = $(el).find('.product-price').text().trim();

            if (title && price) {
                products.push({
                    url: request.url,
                    title,
                    price,
                });
            }
        });

        await Actor.pushData(products);
    },
});

// Run crawler
await crawler.run(startUrls);

await Actor.exit();
```

### Step 6: Build TypeScript

```bash
npm run build
```

### Step 7: Format and Lint

```bash
npm run format
npm run lint:fix
```

### Step 8: Test Locally

```bash
# Run in development mode (TypeScript directly)
npm run start:dev

# Or run compiled version
npm run build
npm run start:prod

# Or use Apify CLI
apify run
```

### Step 9: Deploy

```bash
# Login to Apify
apify login

# Push to Apify platform (will compile TypeScript during Docker build)
apify push
```

## Common Patterns

### HTTP Scraping with Type Safety

```typescript
import { Actor, log } from 'apify';
import { CheerioCrawler, type CheerioCrawlingContext } from '@crawlee/cheerio';

interface Input {
    startUrls: { url: string }[];
    maxItems?: number;
}

interface Product {
    name: string;
    price: string;
    url: string;
    imageUrl?: string;
}

await Actor.init();

const input = (await Actor.getInput<Input>()) || { startUrls: [] };
const { startUrls, maxItems = 100 } = input;

let itemCount = 0;

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxItems,
    async requestHandler({ request, $, enqueueLinks }: CheerioCrawlingContext) {
        log.info(`Scraping ${request.url}`);

        // Extract product data with type safety
        const products: Product[] = [];
        $('.product-item').each((i, el) => {
            const name = $(el).find('.product-name').text().trim();
            const price = $(el).find('.product-price').text().trim();
            const imageUrl = $(el).find('img').attr('src');

            if (name && price) {
                products.push({
                    name,
                    price,
                    url: request.url,
                    imageUrl,
                });
            }
        });

        await Actor.pushData(products);
        itemCount += products.length;

        // Enqueue pagination
        if (itemCount < maxItems) {
            await enqueueLinks({
                selector: 'a.next-page',
                label: 'LISTING',
            });
        }
    },
});

await crawler.run(startUrls);

log.info(`Total items scraped: ${itemCount}`);

await Actor.exit();
```

### Browser Automation with TypeScript

```typescript
import { Actor, log } from 'apify';
import { PlaywrightCrawler, type PlaywrightCrawlingContext } from '@crawlee/playwright';

interface Product {
    name: string | null;
    price: string | null;
    url: string;
}

await Actor.init();

const input = await Actor.getInput() || {};
const { startUrls = [] } = input;

const crawler = new PlaywrightCrawler({
    async requestHandler({ request, page }: PlaywrightCrawlingContext) {
        log.info(`Processing ${request.url}`);

        // Wait for content
        await page.waitForSelector('.product-item');

        // Extract data with proper typing
        const products = await page.$$eval('.product-item', (items): Product[] =>
            items.map((el) => ({
                name: el.querySelector('.product-name')?.textContent?.trim() || null,
                price: el.querySelector('.product-price')?.textContent?.trim() || null,
                url: window.location.href,
            }))
        );

        // Filter out invalid products
        const validProducts = products.filter((p): p is Required<Product> =>
            p.name !== null && p.price !== null
        );

        await Actor.pushData(validProducts);
    },
});

await crawler.run(startUrls);

await Actor.exit();
```

### Creating Custom Types

```typescript
// src/types.ts
export interface ActorInput {
    startUrls: { url: string }[];
    maxItems?: number;
    proxyConfiguration?: {
        useApifyProxy?: boolean;
        apifyProxyGroups?: string[];
    };
}

export interface ScrapedProduct {
    name: string;
    price: string;
    currency: string;
    url: string;
    imageUrl?: string;
    inStock: boolean;
    rating?: number;
    reviewCount?: number;
}

export interface ActorOutput {
    products: ScrapedProduct[];
    totalScraped: number;
    failedUrls: string[];
}
```

```typescript
// src/main.ts
import { Actor, log } from 'apify';
import type { ActorInput, ScrapedProduct } from './types.js';  // Note: .js extension!

await Actor.init();

const input = (await Actor.getInput<ActorInput>()) || { startUrls: [] };

// Use typed interfaces throughout
const products: ScrapedProduct[] = [];

// ... scraping logic ...

await Actor.pushData(products);

await Actor.exit();
```

## Best Practices

### Code Quality
- Use explicit type annotations for public APIs
- Define interfaces for input/output data
- Use `async/await` consistently
- Always start with `Actor.init()` and end with `Actor.exit()`
- Use `log` instead of `console.log()`
- Handle errors gracefully with try/catch
- Add JSDoc comments for public functions
- Run `npm run format` before committing
- Run `npm run lint:fix` before deploying
- Run `npm run build` to catch type errors

### TypeScript-Specific
- Use `.js` extensions in imports (ESM requirement)
- Leverage type inference where possible
- Use `type` for simple types, `interface` for objects
- Enable strict mode in `tsconfig.json`
- Add type definitions for third-party libraries
- Use generics for reusable components
- Prefer `unknown` over `any` for safety

### Performance
- Use `CheerioCrawler` for static HTML (10x faster)
- Use `PlaywrightCrawler` only for JavaScript-heavy sites
- Compile TypeScript once in Docker (multi-stage build)
- Set appropriate `maxRequestsPerCrawl`
- Configure concurrency based on crawler type

### Security
- Never hardcode secrets in source code
- Use environment variables or actor input
- Validate all input data with type guards
- Run as non-root user (already configured)
- Use `.env` file for local secrets (never commit it)

### Dependency Management
- Keep TypeScript up to date (check breaking changes)
- Add `@types/*` packages for libraries without built-in types
- Use `^` for non-breaking updates
- Test after dependency updates
- Keep `package-lock.json` in version control

## Troubleshooting

### Module Import Errors in TypeScript

```typescript
// Wrong - missing .js extension
import { router } from './routes';

// Wrong - using .ts extension
import { router } from './routes.ts';

// Correct - using .js extension (refers to compiled output)
import { router } from './routes.js';
```

### Type Errors

Run TypeScript compiler to see all errors:
```bash
npm run build
```

### Cannot Find Module

Ensure you have type definitions installed:
```bash
npm install --save-dev @types/node
npm install --save-dev @types/cheerio  # If using cheerio
```

### Docker Build Fails

Check that:
- `npm run build` succeeds locally
- All dependencies are in `package.json`
- `tsconfig.json` is properly configured
- `dist/` directory is in `.dockerignore` (will be rebuilt)

### ESLint Errors in TypeScript

Run auto-fix:
```bash
npm run lint:fix
```

Or disable specific rules:
```javascript
// eslint.config.mjs
export default defineConfig({
    rules: {
        '@typescript-eslint/no-explicit-any': 'off',
    },
});
```

## Additional Resources

- [Apify SDK for JavaScript Documentation](https://docs.apify.com/sdk/js)
- [Crawlee Documentation](https://crawlee.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Node.js with TypeScript](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [Actor Input Schema Guide](https://docs.apify.com/platform/actors/development/input-schema)
- [ES Modules in TypeScript](https://www.typescriptlang.org/docs/handbook/modules.html)
