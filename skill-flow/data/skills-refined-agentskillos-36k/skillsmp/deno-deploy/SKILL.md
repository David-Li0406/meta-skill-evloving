---
name: deno-deploy
description: Deno Deploy deployment workflows - use when user says "deploy to deno deploy", "push to deno deploy", "ship to deno deploy", or asks about deploying Deno apps to Deno Deploy
---

# Deno Deploy

This skill provides guidance for deploying applications to Deno Deploy.

## IMPORTANT: Use `deno deploy`, NOT `deployctl`

**Always use the `deno deploy` command.** Do NOT use `deployctl`.

- `deployctl` is for Deno Deploy Classic (deprecated)
- `deno deploy` is the modern, integrated command built into the Deno CLI
- If you find yourself reaching for `deployctl`, stop and use `deno deploy` instead
- **Requires Deno >= 2.4.2** - the `deno deploy` subcommand was introduced in Deno 2.4

## Agent Workflow Guide

When a user asks to deploy to Deno Deploy, follow this decision tree:

### Step 0: Locate the App Directory (ALWAYS DO THIS FIRST)

Before running any checks, find where the Deno app is located:

```bash
# Check if deno.json exists in current directory
if [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then
  echo "APP_DIR: $(pwd)"
else
  # Look for deno.json in immediate subdirectories
  find . -maxdepth 2 -name "deno.json" -o -name "deno.jsonc" 2>/dev/null | head -5
fi
```

**Decision:**
- If `deno.json` is in the current directory → use current directory
- If `deno.json` found in a subdirectory → use that subdirectory (if multiple found, ask user which one)
- If no `deno.json` found → ask user where their app is located

**All subsequent commands must run from the app directory.** Either `cd` to it or use absolute paths.

### Step 1: Pre-Flight Checks (RUN FROM APP DIRECTORY)

**CRITICAL:** Run these checks BEFORE attempting any `deno deploy` commands. Many deploy CLI commands (including `deno deploy orgs`) fail without an org already configured - you cannot discover orgs via CLI.

```bash
# Check Deno version
deno --version | head -1

# Check for existing deploy config WITH org
grep -E '"org"|"app"' deno.json deno.jsonc 2>/dev/null || echo "NO_DEPLOY_CONFIG"

# Detect framework
if [ -d "islands" ] || [ -f "fresh.config.ts" ]; then echo "Framework: Fresh"; \
elif [ -f "astro.config.mjs" ] || [ -f "astro.config.ts" ]; then echo "Framework: Astro"; \
elif [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then echo "Framework: Next.js"; \
elif [ -f "nuxt.config.ts" ]; then echo "Framework: Nuxt"; \
elif [ -f "remix.config.js" ]; then echo "Framework: Remix"; \
elif [ -f "svelte.config.js" ]; then echo "Framework: SvelteKit"; \
elif [ -f "_config.ts" ]; then echo "Framework: Lume (check imports)"; \
else echo "Framework: Custom/Unknown"; fi
```

### Step 2: Route Based on State (FROM APP DIRECTORY)

**If `deploy.org` AND `deploy.app` exist in config:**
1. Run framework-specific build command (see Framework Deployment section)
2. Deploy: `deno deploy --prod`
3. Parse output for deployment URL

**If NO deploy config exists (no org/app found):**

⚠️ **DO NOT run `deno deploy` or `deno deploy orgs`** - they will fail with "No organization was selected" error.

**First, ask the user for their org name:**
> "What is your Deno Deploy organization name? You can find it by visiting https://console.deno.com - look at the URL, it will be something like `console.deno.com/YOUR-ORG-NAME`. For personal accounts, this is usually your username."

**Once you have the org name, run the create command yourself:**
1. Warn the user first: "I'm going to create the app now. **A browser window will open** - please complete the app creation there."
2. Run: `deno deploy create --org <ORG_NAME>`
3. The command will wait for browser completion, then auto-deploy to production

After the command completes, verify:
```bash
grep -E '"org"|"app"' deno.json deno.jsonc
```

### Step 3: Handle Common Errors

| Error | Agent Response |
|-------|----------------|
| "No organization was selected" | You hit this because you didn't check config first. Ask user for org name (see Step 2). |
| "No entrypoint found" | Look for main.ts, mod.ts, src/main.ts, server.ts - suggest `--entrypoint` flag |
| "authorization required" | Token expired/missing - guide user to re-authenticate or set up CI/CD token |
| "Minimum Deno version required" | User needs to upgrade Deno: `deno upgrade` |

### Commands That Fail Without Org Context

These commands will error if no org is configured - **do not try them to "discover" orgs:**
- `deno deploy` (without --org flag)
- `deno deploy orgs`
- `deno deploy switch`
- `deno deploy env list`
- `deno deploy logs`

## Authentication

### Interactive Authentication (Default)

The first time you run `deno deploy`, it will open a browser for authentication:

```bash
deno deploy
# Opens: https://console.deno.com/auth?code=XXXX-XXXX
```

**Important - Browser Device Authorization Flow:**
- The CLI opens your browser and waits for you to complete authentication
- You MUST complete the authorization in your browser before the CLI can continue
- The CLI will NOT proceed automatically - it waits until you finish
- Credentials are stored in your system keyring after successful auth

**For Claude:** When running `deno deploy` commands, prompt the user:
> "Please complete the authorization in your browser, then let me know when you're done."

### Non-Interactive Authentication (CI/CD & Automation)

To deploy without browser interaction (for CI/CD pipelines or automated workflows):

1. **Create a Deploy Token in the web UI:**
   - Visit https://console.deno.com/account/access-tokens
   - Click "New Access Token"
   - Give it a descriptive name (e.g., "GitHub Actions CI")
   - Copy the token immediately (shown only once)

2. **Use the token:**
   ```bash
   # Option 1: Environment variable (recommended for CI/CD)
   export DENO_DEPLOY_TOKEN="your-token-here"
   deno deploy --prod

   # Option 2: Inline flag (for one-off commands)
   deno deploy --token "your-token-here" --prod
   ```

3. **For GitHub Actions:**
   ```yaml
   - name: Deploy to Deno Deploy
     env:
       DENO_DEPLOY_TOKEN: ${{ secrets.DENO_DEPLOY_TOKEN }}
     run: deno deploy --prod
   ```

**For Claude:** If the user wants fully automated deploys without browser prompts, ask:
> "Do you have a Deno Deploy access token set up? If not, you can create one at https://console.deno.com/account/access-tokens, then set it as the `DENO_DEPLOY_TOKEN` environment variable."

## First-Time Setup & Organization

### Finding Your Organization Name

The Deno Deploy CLI requires an organization context for most operations. To find your org name:

1. Visit https://console.deno.com
2. Your org is in the URL: `console.deno.com/YOUR-ORG-NAME`

**Note:** Commands like `deno deploy orgs` and `deno deploy switch` require an existing org context to work - this is a CLI limitation. Always find your org name from the console URL first.

### Setting Up Your First App

**Before creating:** Check if an app already exists by looking for a `deploy` key in deno.json:

```bash
cat deno.json | grep -A5 '"deploy"'
```

If no deploy config exists, create an app:

```bash
deno deploy create --org your-org-name
```

This opens a browser to create the app. **Important:**
- Complete the app creation in your browser
- The CLI waits until you finish - it won't proceed automatically
- The app name becomes your URL: `<app-name>.deno.dev`

**For Claude:** Prompt the user:
> "Please complete the app creation in your browser, then let me know when done."

**Verifying Success:** The CLI output may not clearly indicate success. After the user confirms completion, verify by checking deno.json:

```bash
cat deno.json | grep -A5 '"deploy"'
```

You should see output like:
```json
"deploy": {
  "org": "your-org-name",
  "app": "your-app-name"
}
```

If the `deploy` key exists with `org` and `app` values, the app was created successfully.

## Creating an App

Before your first deployment, create an app:

```bash
deno deploy create --org <organization-name>
```

This opens a browser to create the app in the Deno Deploy console. The app name becomes your URL: `<app-name>.deno.dev`

**Note:** The `create` command does NOT accept `--prod`. Use `--prod` only with `deno deploy` (the deploy command itself).

## Interactive Commands (Run in User's Terminal)

Some `deno deploy` commands are interactive and cannot be run through Claude's Bash tool. For these, ask the user to run them in their own terminal:

### Switching Organizations/Apps

```bash
deno deploy switch
```

This opens an interactive menu to select org and app. **Claude cannot run this** - ask the user:

> "Please run `deno deploy switch` in your terminal to select your organization and app. Let me know when you've completed the selection."

### Alternative: Use Explicit Flags

Instead of interactive selection, specify org/app directly:

```bash
deno deploy --org your-org-name --app your-app-name --prod
```

This bypasses the interactive flow and works through Claude.

## Deploying

### Production Deployment

```bash
deno deploy --prod
```

**Verifying Deployment Success:** The CLI output can be verbose. Look for these indicators of success:
- A URL containing `.deno.dev` or `.deno.net` - this is your live deployment
- A console URL like `https://console.deno.com/<org>/<app>/builds/<id>`
- The command exits with code 0 (no error)

After deployment, confirm success by extracting the production URL from the output. The format is typically:
`https://<app-name>.<org>.deno.net` or `https://<app-name>.deno.dev`

### Preview Deployment

```bash
deno deploy
```

Preview deployments create a unique URL for testing without affecting production.

### Targeting Specific Apps

```bash
deno deploy --org my-org --app my-app --prod
```

### Specifying an Entrypoint

If Deno Deploy can't find your main file:

```bash
deno deploy --entrypoint main.ts --prod
```

Or add to `deno.json`:

```json
{
  "deploy": {
    "entrypoint": "main.ts"
  }
}
```

## Static Site Deployment

For static sites (Lume, Vite builds, etc.), you have two options:

### Option 1: Direct Directory Deployment

Point Deno Deploy at your built directory. Configure in `deno.json`:

```json
{
  "deploy": {
    "entrypoint": "main.ts",
    "include": ["_site"]
  }
}
```

### Option 2: Custom Server Wrapper

Only needed if you want custom routing, headers, or logic:

```typescript
// serve.ts
import { serveDir } from "jsr:@std/http/file-server";

Deno.serve((req) =>
  serveDir(req, {
    fsRoot: "_site",
    quiet: true,
  })
);
```

Then deploy with:

```bash
deno deploy --entrypoint serve.ts --prod
```

## Environment Variables

### Add a Variable

```bash
deno deploy env add DATABASE_URL "postgres://..."
```

### List Variables

```bash
deno deploy env list
```

### Delete a Variable

```bash
deno deploy env delete DATABASE_URL
```

### Load from .env File

```bash
deno deploy env load .env.production
```

### Control Variable Contexts

Variables can apply to different environments:

```bash
# Set which contexts a variable applies to
deno deploy env update-contexts API_KEY Production Preview
```

Available contexts: `Production`, `Preview`, `Local`, `Build`

## Viewing Logs

### Stream Live Logs

```bash
deno deploy logs
```

### Filter by Date Range

```bash
deno deploy logs --start 2026-01-15 --end 2026-01-16
```

## Cloud Integrations

### AWS Integration

```bash
deno deploy setup-aws --org my-org --app my-app
```

### GCP Integration

```bash
deno deploy setup-gcp --org my-org --app my-app
```

## Framework-Specific Deployment

Deno Deploy supports multiple frameworks. The CLI auto-detects your framework and configures the build appropriately.

### Supported Frameworks

| Framework | Detection Files | Build Command | Notes |
|-----------|-----------------|---------------|-------|
| **Fresh** | `islands/`, `fresh.config.ts` | `deno task build` | Deno-native, island architecture |
| **Astro** | `astro.config.mjs`, `astro.config.ts` | `npm run build` or `deno task build` | Static or SSR |
| **Next.js** | `next.config.js`, `next.config.mjs` | `npm run build` | Requires `nodeModulesDir: "auto"` |
| **Nuxt** | `nuxt.config.ts` | `npm run build` | Vue SSR framework |
| **Remix** | `remix.config.js` | `npm run build` | React SSR framework |
| **SolidStart** | `app.config.ts` with solid | `npm run build` | SolidJS SSR |
| **SvelteKit** | `svelte.config.js` | `npm run build` | Svelte SSR framework |
| **Lume** | `_config.ts` with lume import | `deno task build` | Deno-native static site |

### Fresh (Deno-Native)

```bash
deno task build
deno deploy --prod
```

### Astro

```bash
# If using npm
npm run build
deno deploy --prod

# If using Deno tasks
deno task build
deno deploy --prod
```

### Next.js

Next.js requires Node.js compatibility mode:

1. Ensure `deno.json` has:
   ```json
   {
     "nodeModulesDir": "auto"
   }
   ```

2. Build and deploy:
   ```bash
   npm install
   npm run build
   deno deploy --prod --allow-node-modules
   ```

### Nuxt / Remix / SvelteKit / SolidStart

These npm-based frameworks follow a similar pattern:

```bash
npm install
npm run build
deno deploy --prod
```

If you encounter issues with node_modules:
```bash
deno deploy --prod --allow-node-modules
```

### Lume (Static Sites)

```bash
deno task build
deno deploy --prod
```

### Custom / No Framework

For custom servers or apps without a recognized framework:

1. Ensure you have an entrypoint (e.g., `main.ts`, `server.ts`)
2. Deploy directly:
   ```bash
   deno deploy --entrypoint main.ts --prod
   ```

## Command Reference

| Command | Purpose |
|---------|---------|
| `deno deploy --prod` | Production deployment |
| `deno deploy` | Preview deployment |
| `deno deploy create --org <name>` | Create new app |
| `deno deploy env add <var> <value>` | Add environment variable |
| `deno deploy env list` | List environment variables |
| `deno deploy env delete <var>` | Delete environment variable |
| `deno deploy env load <file>` | Load vars from .env file |
| `deno deploy env update-contexts <var> [contexts]` | Set variable contexts |
| `deno deploy logs` | View deployment logs |
| `deno deploy setup-aws` | Configure AWS integration |
| `deno deploy setup-gcp` | Configure GCP integration |

## Common Issues

### "No organization was selected"

This error occurs because the CLI needs an organization context. Unfortunately, commands like `deno deploy orgs` also fail without this context.

**Solution:**

1. **Find your org name manually:** Visit https://console.deno.com - your org is in the URL path (e.g., `console.deno.com/donjo` means org is `donjo`)

2. **Specify org explicitly:**
   ```bash
   deno deploy --org your-org-name --prod
   ```

3. **Or create an app with org:**
   ```bash
   deno deploy create --org your-org-name
   # Complete the browser flow when prompted
   ```

**For Claude:** When you see this error, ask the user:
> "What is your Deno Deploy organization name? You can find it by visiting console.deno.com - look at the URL, it will be something like `console.deno.com/your-org-name`."

### "No entrypoint found"

Specify your entry file:

```bash
deno deploy --entrypoint main.ts --prod
```

Or add to `deno.json`:

```json
{
  "deploy": {
    "entrypoint": "main.ts"
  }
}
```

### Fresh "Build required" Error

Fresh 2.0 requires building before deployment:

```bash
deno task build
deno deploy --prod
```

### Environment Variable Errors

Check what's currently set:

```bash
deno deploy env list
```

Add missing variables:

```bash
deno deploy env add MISSING_VAR "value"
```

## Edge Runtime Notes

Deno Deploy runs on the edge (globally distributed). Keep in mind:

- **No persistent filesystem** - Use Deno KV for storage
- **Environment variables** - Must be set via `deno deploy env`, not .env files at runtime
- **Global distribution** - Code runs at the edge closest to users
- **Cold starts** - First request after idle may be slightly slower

## Documentation

- Official docs: https://docs.deno.com/deploy/
- CLI reference: https://docs.deno.com/runtime/reference/cli/deploy/
