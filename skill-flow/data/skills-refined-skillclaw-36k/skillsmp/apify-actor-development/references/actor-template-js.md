# JavaScript Actor Template Reference

This document describes the complete JavaScript actor template structure that serves as the starting point for all JavaScript-based Apify actors.

## Template Overview

The JavaScript empty template provides a minimal, production-ready structure for building Apify actors in JavaScript (Node.js). It includes:

- Basic Actor skeleton with ES modules support
- Proper project structure with src/ directory
- Docker configuration optimized for Node.js
- Dependency management with npm
- Code quality tools (ESLint, Prettier)
- Actor configuration files

## Complete File Structure

```
js-empty/
├── .actor/
│   └── actor.json                    # Actor metadata and configuration
├── src/
│   └── main.js                       # Main actor logic and entry point
├── .dockerignore                     # Docker build exclusions
├── .editorconfig                     # Editor configuration
├── .gitignore                        # Git exclusions
├── .prettierrc                       # Prettier configuration
├── Dockerfile                        # Container image definition
├── eslint.config.mjs                 # ESLint configuration
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
    "name": "js-empty-project",
    "title": "Empty JavaScript project",
    "description": "Empty project in JavaScript.",
    "version": "0.0",
    "buildTag": "latest",
    "meta": {
        "templateId": "js-empty-from-agent",
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
- `meta.templateId`: Template identifier (use `"js-empty-from-agent"` for agent-generated actors)
- `meta.generatedBy`: **CRITICAL** - Must be filled with model name (e.g., "claude-sonnet-4-5-20250929")
- `dockerfile`: Path to Dockerfile (relative to .actor/)

**Important:**
- Always update `generatedBy` with the current model name
- Use `"js-empty-from-agent"` as templateId for agent-created actors
- Use semantic versioning for `version`
- `name` must be URL-safe (lowercase, hyphens only)

### `src/main.js`

Main actor logic and entry point.

```javascript
// Crawlee - web scraping and browser automation library (Read more at https://crawlee.dev)
// import { CheerioCrawler } from '@crawlee/cheerio';
// Apify SDK - toolkit for building Apify Actors (Read more at https://docs.apify.com/sdk/js/)
import { Actor, log } from 'apify';

// this is ESM project, and as such, it requires you to specify extensions in your relative imports
// read more about this here: https://nodejs.org/docs/latest-v18.x/api/esm.html#mandatory-file-extensions
// import { router } from './routes.js';

// The init() call configures the Actor for its environment. It's recommended to start every Actor with an init()
await Actor.init();

// eslint-disable-next-line no-console
log.info('Hello from the Actor!');
/**
 * Actor code
 */

// Gracefully exit the Actor process. It's recommended to quit all Actors with an exit()
await Actor.exit();
```

**Key points:**
- Uses ES modules (`import/export`) syntax
- Always start with `await Actor.init()` for proper initialization
- Always end with `await Actor.exit()` for graceful shutdown
- Use `log` from `apify` package (automatically censors sensitive data)
- Relative imports must include `.js` extension in ESM
- Top-level `await` is supported

**Common patterns:**

```javascript
import { Actor, log } from 'apify';

await Actor.init();

// 1. Get input
const input = await Actor.getInput() || {};
const { startUrls = [], maxItems = 100 } = input;

// 2. Process data
const results = [];
for (const { url } of startUrls) {
    // Scraping logic here
    results.push({ url });
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
    "name": "js-empty-project",
    "version": "0.0.1",
    "type": "module",
    "description": "This is a boilerplate of an Apify Actor.",
    "engines": {
        "node": ">=18.0.0"
    },
    "dependencies": {
        "apify": "^3.5.2",
        "@crawlee/cheerio": "^3.15.3"
    },
    "devDependencies": {
        "@apify/eslint-config": "^1.0.0",
        "eslint": "^9.29.0",
        "eslint-config-prettier": "^10.1.5",
        "prettier": "^3.5.3"
    },
    "scripts": {
        "start": "node ./src/main.js",
        "format": "prettier --write .",
        "format:check": "prettier --check .",
        "lint": "eslint",
        "lint:fix": "eslint --fix",
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
- `devDependencies`: Development tools (linting, formatting)
- `scripts`: Common commands
  - `start`: Run the actor locally
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
        "axios": "^1.6.0",
        "cheerio": "^1.0.0"
    }
}
```

### `Dockerfile`

Container image definition optimized for Node.js actors.

```dockerfile
# Specify the base Docker image. You can read more about
# the available images at https://docs.apify.com/sdk/js/docs/guides/docker-images
# You can also use any other image from Docker Hub.
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

# Next, copy the remaining files and directories with the source code.
# Since we do this after NPM install, quick build will be really fast
# for most source file changes.
COPY --chown=myuser:myuser . ./

# Run the image.
CMD ["node", "src/main.js"]
```

**Key points:**
- Uses official Apify Node.js base image (Node.js 22)
- Runs as non-root user (`myuser`) for security
- Optimized layer caching: package files copied separately
- Checks preinstalled packages (Crawlee, Puppeteer, Playwright)
- Installs only production dependencies (`--omit=dev --omit=optional`)
- Executes actor with `node src/main.js`

**Available Node.js versions:**
- `apify/actor-node:22` (recommended)
- `apify/actor-node:20`
- `apify/actor-node:18`

**Build optimization:**
- Copy `package.json` and `package-lock.json` first for layer caching
- Dependencies are cached unless package files change
- Source code changes don't trigger dependency reinstall

### `eslint.config.mjs`

ESLint configuration for code quality.

```javascript
import { defineConfig } from '@apify/eslint-config';

export default defineConfig({
    rules: {
        // Add your custom rules here
    },
});
```

**Key points:**
- Uses Apify's ESLint configuration as base
- Configured for ES modules (`.mjs` extension)
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
- Ensures consistent code formatting
- Configured with Apify's style preferences
- Run with `npm run format` or `npm run format:check`
- Integrates with ESLint via `eslint-config-prettier`

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
.DS_Store
*.log
.env
```

**Key points:**
- Excludes version control (`.git/`)
- Excludes `node_modules/` (reinstalled in Docker)
- Excludes local storage directories
- Reduces Docker image size significantly

### `.gitignore`

Files to exclude from version control.

```
node_modules/
storage/
apify_storage/
.DS_Store
*.log
.env
dist/
```

**Key points:**
- Excludes dependencies (`node_modules/`)
- Excludes local storage directories
- Includes `.env` to prevent committing secrets
- Excludes build artifacts

### `README.md`

Development documentation for the project.

**Purpose:**
- Documents local development setup
- Explains how to run and test the actor
- Lists included features and resources
- Not shown in marketplace (use `.actor/ACTOR.md` for that)

**Key sections:**
- Project overview
- How to run locally
- How to deploy
- Available resources and documentation links

## Using the Template

### Step 1: Copy Template Files

```bash
# Create new actor directory
mkdir my-new-actor
cd my-new-actor

# Copy all template files including hidden ones
cp -r /path/to/js-empty/* .
cp -r /path/to/js-empty/.* .
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
        "templateId": "js-empty-from-agent",
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
npm install axios cheerio
# Or for browser automation
npm install @crawlee/playwright
```

### Step 5: Implement Logic

Edit `src/main.js`:

```javascript
import { Actor, log } from 'apify';
import { CheerioCrawler } from '@crawlee/cheerio';

await Actor.init();

// Get input
const input = await Actor.getInput() || {};
const { startUrls = [] } = input;

// Create crawler
const crawler = new CheerioCrawler({
    async requestHandler({ request, $ }) {
        log.info(`Processing ${request.url}`);

        // Extract data
        const title = $('h1').text();
        const price = $('.price').text();

        // Save data
        await Actor.pushData({
            url: request.url,
            title,
            price,
        });
    },
});

// Run crawler
await crawler.run(startUrls);

await Actor.exit();
```

### Step 6: Format and Lint

```bash
npm run format
npm run lint:fix
```

### Step 7: Test Locally

```bash
# Install Apify CLI if not installed
npm install -g apify-cli

# Run locally
apify run
```

### Step 8: Deploy

```bash
# Login to Apify
apify login

# Push to Apify platform
apify push
```

## Common Patterns

### HTTP Scraping with CheerioCrawler

```javascript
import { Actor, log } from 'apify';
import { CheerioCrawler } from '@crawlee/cheerio';

await Actor.init();

const input = await Actor.getInput() || {};
const { startUrls, maxItems = 100 } = input;

let itemCount = 0;

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: maxItems,
    async requestHandler({ request, $, enqueueLinks }) {
        log.info(`Scraping ${request.url}`);

        // Extract product data
        const products = [];
        $('.product-item').each((i, el) => {
            products.push({
                name: $(el).find('.product-name').text().trim(),
                price: $(el).find('.product-price').text().trim(),
                url: request.url,
            });
        });

        await Actor.pushData(products);
        itemCount += products.length;

        // Enqueue pagination links
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

### Browser Automation with PlaywrightCrawler

```javascript
import { Actor, log } from 'apify';
import { PlaywrightCrawler } from '@crawlee/playwright';

await Actor.init();

const input = await Actor.getInput() || {};
const { startUrls } = input;

const crawler = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
        log.info(`Processing ${request.url}`);

        // Wait for content
        await page.waitForSelector('.product-item');

        // Extract data
        const products = await page.$$eval('.product-item', (items) =>
            items.map((el) => ({
                name: el.querySelector('.product-name')?.textContent?.trim(),
                price: el.querySelector('.product-price')?.textContent?.trim(),
            }))
        );

        await Actor.pushData(products);
    },
});

await crawler.run(startUrls);

await Actor.exit();
```

### Input Validation

```javascript
import { Actor, log } from 'apify';

await Actor.init();

const input = await Actor.getInput() || {};

// Validate required fields
if (!input.startUrls || input.startUrls.length === 0) {
    throw new Error('startUrls is required and must not be empty');
}

if (input.maxItems && (input.maxItems < 1 || input.maxItems > 10000)) {
    throw new Error('maxItems must be between 1 and 10000');
}

log.info('Input validation passed');

// Continue with actor logic...

await Actor.exit();
```

## Best Practices

### Code Quality
- Use ES modules (`import/export`) consistently
- Always start with `Actor.init()` and end with `Actor.exit()`
- Use `log` instead of `console.log()`
- Handle errors gracefully with try/catch
- Add JSDoc comments for functions
- Run `npm run format` before committing
- Run `npm run lint:fix` before deploying

### Performance
- Use `CheerioCrawler` for static HTML (10x faster than browsers)
- Use `PlaywrightCrawler` only for JavaScript-heavy sites
- Batch data pushes when possible
- Set appropriate `maxRequestsPerCrawl`
- Configure concurrency based on crawler type:
  - HTTP (CheerioCrawler): 10-50
  - Browser (PlaywrightCrawler): 1-5

### Security
- Never hardcode secrets in source code
- Use environment variables or actor input
- Run as non-root user (already configured in Dockerfile)
- Validate all input data
- Use `.env` file for local secrets (never commit it)

### Dependency Management
- Use `^` for non-breaking updates: `"apify": "^3.5.2"`
- Test after dependency updates
- Keep `package-lock.json` in version control
- Use `npm audit` to check for vulnerabilities

## Troubleshooting

### Module Import Errors

```javascript
// Wrong - missing .js extension
import { router } from './routes';

// Correct - includes .js extension for ESM
import { router } from './routes.js';
```

### Actor Not Initializing

Ensure you have:
```javascript
await Actor.init();
// ... your code ...
await Actor.exit();
```

### Docker Build Fails

Check that:
- `package.json` and `package-lock.json` are properly formatted
- All dependencies are available on npm
- Node.js version in Dockerfile matches `engines.node` in package.json

### ESLint Errors

Run auto-fix:
```bash
npm run lint:fix
```

Or disable specific rules in `eslint.config.mjs`:
```javascript
export default defineConfig({
    rules: {
        'no-console': 'off',
    },
});
```

## Additional Resources

- [Apify SDK for JavaScript Documentation](https://docs.apify.com/sdk/js)
- [Crawlee Documentation](https://crawlee.dev)
- [Node.js Actor Tutorial](https://docs.apify.com/academy/node-js)
- [Actor Input Schema Guide](https://docs.apify.com/platform/actors/development/input-schema)
- [ES Modules Guide](https://nodejs.org/docs/latest-v18.x/api/esm.html)
