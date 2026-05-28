---
name: vercel-deploy
description: Deploy applications and websites to Vercel. Use this skill when the user requests deployment actions such as "Deploy my app", "Deploy this to production", "Create a preview deployment", or "Push this live". No authentication required - returns preview URL and claimable deployment link.
---

# Vercel Deploy

Deploy any project to Vercel instantly. No authentication required.

## How It Works

1. Packages your project into a tarball (excludes `node_modules` and `.git`).
2. Auto-detects framework from `package.json`.
3. Uploads to deployment service.
4. Returns **Preview URL** (live site) and **Claim URL** (transfer to your Vercel account).

## Usage

```bash
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh [path]
```

**Arguments:**
- `path` - Directory to deploy, or a `.tgz` file (defaults to current directory).

**Examples:**

```bash
# Deploy current directory
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh

# Deploy specific project
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project

# Deploy existing tarball
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project.tgz
```

## Output

```
Preparing deployment...
Detected framework: nextjs
Creating deployment package...
Deploying...
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

The script also outputs JSON to stdout for programmatic use:

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## Framework Detection

The script auto-detects frameworks from `package.json`. Supported frameworks include:

- **React**: Next.js, Gatsby, Create React App, Remix, React Router
- **Vue**: Nuxt, Vitepress, Vuepress, Gridsome
- **Svelte**: SvelteKit, Svelte, Sapper
- **Other Frontend**: Astro, Solid Start, Angular, Ember, Preact, Docusaurus
- **Backend**: Express, Hono, Fastify, NestJS, Elysia, h3, Nitro
- **Build Tools**: Vite, Parcel
- **And more**: Blitz, Hydrogen, RedwoodJS, Storybook, Sanity, etc.

For static HTML projects (no `package.json`), framework is set to `null`.

## Static HTML Projects

For projects without a `package.json`:
- If there's a single `.html` file not named `index.html`, it gets renamed automatically to ensure the page is served at the root URL (`/`).

## Present Results to User

Always show both URLs:

```
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...

View your site at the Preview URL.
To transfer this deployment to your Vercel account, visit the Claim URL.
```

## Troubleshooting

### Network Egress Error

If deployment fails due to network restrictions (common on claude.ai), tell the user:

```
Deployment failed due to network restrictions. To fix this:

1. Go to https://claude.ai/settings/capabilities
2. Add *.vercel.com to the allowed domains
3. Try deploying again
```

### Framework Not Detected

If the framework is not detected:
1. Check for the existence of `package.json`.
2. Ensure the framework package is included in dependencies.
3. Manually specify the `framework` parameter if necessary.

## Constraints

### Must
1. Display both URLs: Preview URL and Claim URL to the user.
2. Automatically detect the framework from `package.json`.
3. Provide clear error messages on deployment failure.

### Must Not
1. Include `node_modules` in the tarball.
2. Include the `.git` directory in the tarball.
3. Require authentication (claimable deploy).

## Best Practices

1. Automatically detect the framework for optimal settings.
2. Create a clean tarball by excluding `node_modules` and `.git` for faster uploads.
3. Clearly differentiate between the Preview URL and Claim URL in outputs.

## References

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel CLI](https://vercel.com/docs/cli)

## Metadata

- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-22
- **Compatible Platforms**: Claude (claude.ai)
- **Original Source**: vercel/agent-skills

## Tags
`#deployment` `#vercel` `#preview` `#production` `#hosting` `#serverless` `#infrastructure`