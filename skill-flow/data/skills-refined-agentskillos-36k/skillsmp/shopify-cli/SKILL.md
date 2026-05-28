---
name: Shopify CLI
description: This skill should be used when the user asks to "use shopify cli", "run shopify theme", "shopify app dev", "create a shopify theme", "push theme to shopify", "pull theme from shopify", "start theme dev server", "deploy shopify app", "initialize shopify project", or mentions Shopify CLI commands, theme development, or app development workflows.
version: 0.1.0
---

# Shopify CLI

Shopify CLI is a command-line tool for building Shopify apps, themes, and Hydrogen storefronts. It provides commands for local development, testing, and deployment.

## Installation

Install via npm (requires Node.js 18+):

```bash
npm install -g @shopify/cli @shopify/theme
```

Or via Homebrew on macOS:

```bash
brew tap shopify/shopify
brew install shopify-cli
```

## Command Structure

All commands follow the pattern: `shopify [topic] [command] [flags]`

Main topics:
- `theme` - Theme development commands
- `app` - App development commands
- `hydrogen` - Hydrogen storefront commands

## Theme Development

### Starting Local Development

Start a local development server with hot reload:

```bash
shopify theme dev --store your-store.myshopify.com
```

This uploads the theme as a development theme and returns a preview URL at `http://127.0.0.1:9292`. Development themes don't count toward theme limits and auto-delete after 7 days of inactivity.

Key flags:
- `--store` - Target store domain
- `--theme` - Use existing theme ID instead of creating dev theme
- `--host` - Network interface (default: 127.0.0.1)
- `--port` - Port number (default: 9292)
- `--live-reload` - Enable/disable live reload (default: hot-reload)

### Theme Commands Reference

| Command | Purpose |
|---------|---------|
| `theme init` | Clone a Git repo as theme starting point |
| `theme dev` | Start local dev server with hot reload |
| `theme push` | Upload local theme to store |
| `theme pull` | Download theme from store |
| `theme list` | Show all themes with IDs |
| `theme check` | Run Theme Check linter |
| `theme publish` | Make theme live |
| `theme delete` | Remove theme from store |
| `theme share` | Create shareable preview link |
| `theme package` | Create ZIP for Theme Store submission |

### Pushing and Pulling Themes

Push local changes to store:

```bash
shopify theme push --store your-store.myshopify.com
```

Pull theme from store:

```bash
shopify theme pull --store your-store.myshopify.com --theme THEME_ID
```

Use `--only` or `--ignore` flags to filter files:

```bash
shopify theme push --only "sections/*" --only "snippets/*"
shopify theme pull --ignore "config/settings_data.json"
```

### Theme Check (Linting)

Run Theme Check to validate Liquid code:

```bash
shopify theme check
```

Auto-fix issues where possible:

```bash
shopify theme check --auto-correct
```

## App Development

### Creating a New App

Initialize a new Shopify app:

```bash
shopify app init
```

This scaffolds an app with Remix, Prisma, and Polaris.

### Running App Locally

Start the local development server:

```bash
shopify app dev
```

This:
- Starts a local server with hot reload
- Creates a Cloudflare tunnel for OAuth callbacks
- Syncs app configuration with Partners dashboard

### App Commands Reference

| Command | Purpose |
|---------|---------|
| `app init` | Create new app from template |
| `app dev` | Start local dev server |
| `app deploy` | Deploy app to Shopify |
| `app info` | Show app configuration |
| `app generate extension` | Add new extension |
| `app function` | Manage Shopify Functions |
| `app env` | Manage environment variables |

### Generating Extensions

Add extensions to an existing app:

```bash
shopify app generate extension
```

Extension types include:
- Theme app extensions
- Checkout UI extensions
- Admin UI extensions
- Shopify Functions
- Web pixels

## Multi-Environment Configuration

Configure multiple environments in `shopify.theme.toml`:

```toml
[environments.development]
store = "dev-store.myshopify.com"
theme = "123456789"

[environments.production]
store = "prod-store.myshopify.com"
theme = "987654321"
```

Run commands against specific environments:

```bash
shopify theme push --environment production
shopify theme dev --environment development
```

## Authentication

Log in to Shopify:

```bash
shopify auth login --store your-store.myshopify.com
```

Log out:

```bash
shopify auth logout
```

Check current auth status:

```bash
shopify auth info
```

## Common Workflows

### Theme Development Workflow

1. Clone or init theme: `shopify theme init`
2. Start dev server: `shopify theme dev --store STORE`
3. Make changes (hot reload active)
4. Run linter: `shopify theme check`
5. Push to store: `shopify theme push`

### App Development Workflow

1. Create app: `shopify app init`
2. Start dev server: `shopify app dev`
3. Add extensions: `shopify app generate extension`
4. Deploy: `shopify app deploy`

## Troubleshooting

**Authentication issues**: Run `shopify auth logout` then `shopify auth login`

**Theme not syncing**: Check `.shopifyignore` file for excluded patterns

**Port conflicts**: Use `--port` flag to specify different port

**Permission errors**: Ensure store access via Partners dashboard or staff account

## Additional Resources

For detailed command documentation, run:

```bash
shopify help
shopify theme --help
shopify app --help
```
